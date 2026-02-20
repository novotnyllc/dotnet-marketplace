#:property TargetFramework=net10.0
#:property PublishAot=false

using System.Diagnostics;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

internal static class ResultStatus
{
    public const string Pass = "pass";
    public const string Fail = "fail";
    public const string Infra = "infra_error";
}

internal static class FailureKinds
{
    public const string SkillNotLoaded = "skill_not_loaded";
    public const string MissingSkillFileEvidence = "missing_skill_file_evidence";
    public const string MissingActivityEvidence = "missing_activity_evidence";
    public const string MixedEvidenceMissing = "mixed_evidence_missing";
    public const string Unknown = "unknown";
}

internal static class FailureCategories
{
    public const string Timeout = "timeout";
    public const string Transport = "transport";
    public const string Assertion = "assertion";
}

internal static class Program
{
    private static async Task<int> Main(string[] args)
    {
        RunnerOptions options;
        try
        {
            options = RunnerOptions.Parse(args);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"ERROR: {ex.Message}");
            RunnerOptions.PrintHelp();
            return 2;
        }

        if (options.ShowHelp)
        {
            RunnerOptions.PrintHelp();
            return 0;
        }

        return await new AgentRoutingRunner(options).RunAsync();
    }
}

internal sealed class AgentRoutingRunner
{
    private static readonly string[] DefaultAgents = ["claude", "codex", "copilot"];

    private static readonly string[] DefaultAnyEvidence =
    [
        "tool_use",
        "read_file",
        "file_search",
        "command_execution",
        "function_call",
        "mcp:",
        "Glob ",
        "Grep ",
        "Read(",
        "Grep(",
        "Glob(",
        "Bash(",
        "shell(",
        "Starting remote MCP client for github-mcp-server",
        "Invalid MCP config for plugin \"dotnet-artisan\""
    ];

    private static readonly Regex ClaudeSkillFieldRegex = new("\"skill\":\"([^\"]+)\"", RegexOptions.Compiled);
    private static readonly Regex ClaudeLaunchingSkillRegex = new("Launching skill:\\s*([A-Za-z0-9._:-]+)", RegexOptions.Compiled | RegexOptions.IgnoreCase);

    private readonly RunnerOptions _options;
    private readonly object _progressLock = new();
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };

    public AgentRoutingRunner(RunnerOptions options)
    {
        _options = options;
    }

    public async Task<int> RunAsync()
    {
        var batchRunId = Guid.NewGuid().ToString();

        // Create batch artifact directory — runner is sole owner of this directory.
        var batchDir = Path.GetFullPath(Path.Combine(_options.ArtifactsRoot, batchRunId));
        Directory.CreateDirectory(batchDir);

        // Protocol output: ARTIFACT_DIR is always emitted (not suppressed by --no-progress).
        // Raw line on stderr — no prefix, no timestamp, no brackets.
        Console.Error.WriteLine($"ARTIFACT_DIR={batchDir}");

        if (!File.Exists(_options.InputPath))
        {
            Console.Error.WriteLine($"ERROR: Cases file not found: {_options.InputPath}");
            return 1;
        }

        var cases = await LoadCasesAsync(_options.InputPath);

        if (_options.Categories.Count > 0)
        {
            cases =
            [
                .. cases.Where(c => _options.Categories.Contains(c.Category))
            ];
        }

        if (_options.CaseIds.Count > 0)
        {
            cases =
            [
                .. cases.Where(c => _options.CaseIds.Contains(c.CaseId))
            ];
        }

        if (cases.Count == 0)
        {
            Console.Error.WriteLine("ERROR: No cases to execute after filtering.");
            return 1;
        }

        var agents = _options.Agents.Count > 0
            ? _options.Agents.Select(a => a.Trim().ToLowerInvariant()).Where(a => a.Length > 0).Distinct().ToArray()
            : DefaultAgents;

        // Capture log snapshots once per agent per batch (before scheduling work items).
        var agentLogSnapshots = new Dictionary<string, Dictionary<string, LogFileState>>(StringComparer.OrdinalIgnoreCase);
        if (_options.EnableLogScan)
        {
            foreach (var agent in agents)
            {
                agentLogSnapshots[agent] = CaptureLogSnapshot(agent);
            }
        }

        var work = new List<(int Index, string Agent, CaseDefinition TestCase)>(cases.Count * agents.Length);
        var runIndex = 0;
        foreach (var testCase in cases)
        {
            foreach (var agent in agents)
            {
                work.Add((runIndex, agent, testCase));
                runIndex++;
            }
        }

        var totalRuns = work.Count;
        var maxParallel = Math.Min(_options.MaxParallel, totalRuns);
        LogProgress($"[batch:{batchRunId}] Starting {totalRuns} runs ({cases.Count} cases x {agents.Length} agents), max_parallel={maxParallel}, log_scan={_options.EnableLogScan}.");
        var results = await ExecuteWorkAsync(work, totalRuns, maxParallel, batchRunId, agentLogSnapshots);
        LogProgress($"[batch:{batchRunId}] Run matrix completed.");

        var summary = new Summary
        {
            Total = results.Count,
            Pass = results.Count(r => r.Status == ResultStatus.Pass),
            Fail = results.Count(r => r.Status == ResultStatus.Fail),
            InfraError = results.Count(r => r.Status == ResultStatus.Infra)
        };

        var envelope = new ResultEnvelope
        {
            BatchRunId = batchRunId,
            GeneratedAtUtc = DateTimeOffset.UtcNow,
            Summary = summary,
            Results = results,
            Options = new ResultOptions
            {
                Input = _options.InputPath,
                Agents = agents,
                Categories = _options.Categories.OrderBy(x => x).ToArray(),
                CaseIds = _options.CaseIds.OrderBy(x => x).ToArray(),
                TimeoutSeconds = _options.TimeoutSeconds,
                MaxParallel = maxParallel,
                LogMaxFiles = _options.LogMaxFiles,
                LogMaxBytes = _options.LogMaxBytes,
                Progress = _options.Progress,
                ArtifactsRoot = _options.ArtifactsRoot,
                EnableLogScan = _options.EnableLogScan
            }
        };

        var payload = JsonSerializer.Serialize(envelope, _jsonOptions);
        Console.WriteLine(payload);

        // Always write results.json to batch directory (unconditional — source of truth).
        var batchResultsPath = Path.Combine(batchDir, "results.json");
        await File.WriteAllTextAsync(batchResultsPath, payload + Environment.NewLine);

        // Always write proof log to batch directory (unconditional).
        var batchProofLogPath = Path.Combine(batchDir, "tool-use-proof.log");
        await WriteProofLogAsync(results, batchProofLogPath, batchRunId);

        // Backward compat: --proof-log writes an additional copy.
        var extraProofLogPath = ResolveProofLogPath();
        if (!string.IsNullOrWhiteSpace(extraProofLogPath) &&
            !string.Equals(Path.GetFullPath(extraProofLogPath!), Path.GetFullPath(batchProofLogPath), StringComparison.OrdinalIgnoreCase))
        {
            await WriteProofLogAsync(results, extraProofLogPath!, batchRunId);
        }

        // Backward compat: --output writes an additional copy.
        if (!string.IsNullOrWhiteSpace(_options.OutputPath))
        {
            var outputPath = _options.OutputPath!;
            if (!string.Equals(Path.GetFullPath(outputPath), Path.GetFullPath(batchResultsPath), StringComparison.OrdinalIgnoreCase))
            {
                var outputDir = Path.GetDirectoryName(outputPath);
                if (!string.IsNullOrWhiteSpace(outputDir))
                {
                    Directory.CreateDirectory(outputDir);
                }

                await File.WriteAllTextAsync(outputPath, payload + Environment.NewLine);
            }
        }

        if (summary.Fail > 0)
        {
            return 1;
        }

        if (_options.FailOnInfra && summary.InfraError > 0)
        {
            return 1;
        }

        return 0;
    }

    private async Task<List<AgentResult>> ExecuteWorkAsync(
        List<(int Index, string Agent, CaseDefinition TestCase)> work,
        int totalRuns,
        int maxParallel,
        string batchRunId,
        Dictionary<string, Dictionary<string, LogFileState>> agentLogSnapshots)
    {
        var semaphore = new SemaphoreSlim(maxParallel, maxParallel);
        var results = new AgentResult[totalRuns];
        var started = 0;
        var completed = 0;
        var pass = 0;
        var fail = 0;
        var infra = 0;

        var tasks = work.Select(async item =>
        {
            var unitRunId = Guid.NewGuid().ToString();
            LogProgress($"[batch:{batchRunId}] [unit:{unitRunId}] {item.Agent}:{item.TestCase.CaseId} -> queued");

            await semaphore.WaitAsync();
            try
            {
                var startedOrdinal = Interlocked.Increment(ref started);
                LogProgress($"[batch:{batchRunId}] [unit:{unitRunId}] {item.Agent}:{item.TestCase.CaseId} -> running [{startedOrdinal}/{totalRuns}]");

                // Use per-agent-per-batch log snapshot (captured once before scheduling).
                agentLogSnapshots.TryGetValue(item.Agent, out var snapshot);
                var result = await RunCaseAsync(item.Agent, item.TestCase, unitRunId, snapshot);
                results[item.Index] = result;

                string lifecycleState;
                switch (result.Status)
                {
                    case ResultStatus.Pass:
                        Interlocked.Increment(ref pass);
                        lifecycleState = result.TimedOut ? "timeout" : "completed";
                        break;
                    case ResultStatus.Fail:
                        Interlocked.Increment(ref fail);
                        lifecycleState = result.TimedOut ? "timeout" : "failed";
                        break;
                    default:
                        Interlocked.Increment(ref infra);
                        lifecycleState = result.TimedOut ? "timeout" : "failed";
                        break;
                }

                var completedOrdinal = Interlocked.Increment(ref completed);
                LogProgress(
                    $"[batch:{batchRunId}] [unit:{unitRunId}] {item.Agent}:{item.TestCase.CaseId} -> {lifecycleState} " +
                    $"[{completedOrdinal}/{totalRuns}] status={result.Status} duration_ms={result.DurationMs} " +
                    $"timed_out={result.TimedOut} summary(pass={pass}, fail={fail}, infra={infra})");
            }
            finally
            {
                semaphore.Release();
            }
        });

        await Task.WhenAll(tasks);
        return [.. results];
    }

    private void LogProgress(string message)
    {
        if (!_options.Progress)
        {
            return;
        }

        lock (_progressLock)
        {
            Console.Error.WriteLine($"[check-skills] {DateTimeOffset.UtcNow:HH:mm:ss} {message}");
        }
    }

    private async Task<AgentResult> RunCaseAsync(
        string agent,
        CaseDefinition testCase,
        string unitRunId,
        Dictionary<string, LogFileState>? batchSnapshot)
    {
        var startedAtUtc = DateTimeOffset.UtcNow;
        var started = Stopwatch.StartNew();

        var template = ResolveAgentTemplate(agent);
        if (string.IsNullOrWhiteSpace(template))
        {
            return AgentResult.Infra(
                agent,
                testCase,
                "No command template configured.",
                started.ElapsedMilliseconds,
                source: "none",
                unitRunId: unitRunId,
                timedOut: false);
        }

        var command = BuildShellCommand(template, testCase.Prompt);
        var exec = await ExecuteCommandAsync(command, _options.TimeoutSeconds);
        var combined = CombineOutput(exec.Stdout, exec.Stderr);

        if (!exec.Started)
        {
            return AgentResult.Infra(
                agent,
                testCase,
                exec.ErrorMessage ?? "failed to start process",
                started.ElapsedMilliseconds,
                source: "none",
                unitRunId: unitRunId,
                command: command,
                exitCode: exec.ExitCode,
                outputExcerpt: TrimExcerpt(combined),
                timedOut: exec.TimedOut);
        }

        // Detect "command not found" (exit 127) or "permission denied" (exit 126)
        // from bash -- these indicate a missing or non-executable CLI binary,
        // which is a transport failure, not an assertion failure.
        if (IsCommandNotFound(exec))
        {
            return AgentResult.Infra(
                agent,
                testCase,
                $"CLI not found or not executable (exit code {exec.ExitCode})",
                started.ElapsedMilliseconds,
                source: "none",
                unitRunId: unitRunId,
                command: command,
                exitCode: exec.ExitCode,
                outputExcerpt: TrimExcerpt(combined),
                timedOut: exec.TimedOut);
        }

        var outputEval = EvaluateEvidence(combined, testCase, "cli_output", agent);
        if (outputEval.Success)
        {
            return AgentResult.Pass(
                agent,
                testCase,
                started.ElapsedMilliseconds,
                source: "cli_output",
                outputEval,
                command,
                exec.ExitCode,
                TrimExcerpt(combined),
                exec.TimedOut,
                unitRunId: unitRunId);
        }

        // Log fallback: only attempt when log scanning is enabled and snapshot is available.
        if (_options.EnableLogScan && batchSnapshot is not null)
        {
            var logEval = await TryFindEvidenceInLogsAsync(agent, testCase, startedAtUtc, batchSnapshot);
            if (logEval.Success)
            {
                return AgentResult.Pass(
                    agent,
                    testCase,
                    started.ElapsedMilliseconds,
                    source: "log_fallback",
                    logEval,
                    command,
                    exec.ExitCode,
                    TrimExcerpt(combined),
                    exec.TimedOut,
                    unitRunId: unitRunId);
            }

            var failedEval = EvidenceEvaluation.Merge(outputEval, logEval);
            var failureReason = exec.TimedOut
                ? "command timed out"
                : exec.ExitCode != 0
                    ? $"agent command returned exit code {exec.ExitCode}"
                    : null;

            return AgentResult.Fail(
                agent,
                testCase,
                started.ElapsedMilliseconds,
                source: "cli_output+log_fallback",
                failedEval,
                command,
                exec.ExitCode,
                TrimExcerpt(combined),
                exec.TimedOut,
                unitRunId: unitRunId,
                error: failureReason);
        }

        // No log fallback — fail based on CLI output only.
        var cliFailureReason = exec.TimedOut
            ? "command timed out"
            : exec.ExitCode != 0
                ? $"agent command returned exit code {exec.ExitCode}"
                : null;

        return AgentResult.Fail(
            agent,
            testCase,
            started.ElapsedMilliseconds,
            source: "cli_output",
            outputEval,
            command,
            exec.ExitCode,
            TrimExcerpt(combined),
            exec.TimedOut,
            unitRunId: unitRunId,
            error: cliFailureReason);
    }

    private static string ResolveAgentTemplate(string agent)
    {
        var env = Environment.GetEnvironmentVariable($"AGENT_{agent.ToUpperInvariant()}_TEMPLATE");
        if (!string.IsNullOrWhiteSpace(env))
        {
            return env;
        }

        return agent switch
        {
            "claude" => "claude -p --verbose --output-format stream-json --include-partial-messages --permission-mode bypassPermissions {prompt} --disallowed-tools AskUserQuestion --disallowed-tools EnterPlanMode",
            "codex" => "codex -a never exec --json {prompt}",
            "copilot" => "copilot -p {prompt} --allow-all-tools --no-ask-user --log-level debug",
            _ => string.Empty
        };
    }

    private static string BuildShellCommand(string template, string prompt)
    {
        var quotedPrompt = ShellQuote(prompt);

        return template.Contains("{prompt}", StringComparison.Ordinal)
            ? template.Replace("{prompt}", quotedPrompt, StringComparison.Ordinal)
            : template + " " + quotedPrompt;
    }

    private static string ShellQuote(string value)
    {
        return "'" + value.Replace("'", "'\"'\"'") + "'";
    }

    private async Task<EvidenceEvaluation> TryFindEvidenceInLogsAsync(
        string agent,
        CaseDefinition testCase,
        DateTimeOffset startedAtUtc,
        Dictionary<string, LogFileState> snapshot)
    {
        var notBeforeUtc = startedAtUtc.UtcDateTime.AddMinutes(-2);
        var roots = ResolveLogRoots(agent)
            .Select(ExpandHome)
            .Where(Directory.Exists)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToArray();

        if (roots.Length == 0)
        {
            return EvaluateEvidence(string.Empty, testCase, "log_fallback", agent);
        }

        var candidates = new List<FileInfo>();

        foreach (var root in roots)
        {
            try
            {
                foreach (var path in Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories))
                {
                    FileInfo info;
                    try
                    {
                        info = new FileInfo(path);
                    }
                    catch
                    {
                        continue;
                    }

                    if (!IsLogLike(info))
                    {
                        continue;
                    }

                    if (snapshot.TryGetValue(info.FullName, out var previous) &&
                        info.LastWriteTimeUtc <= previous.LastWriteUtc &&
                        info.Length <= previous.Length)
                    {
                        continue;
                    }

                    if (info.LastWriteTimeUtc < notBeforeUtc)
                    {
                        continue;
                    }

                    candidates.Add(info);
                }
            }
            catch
            {
                // Continue to next root.
            }
        }

        foreach (var file in candidates.OrderByDescending(f => f.LastWriteTimeUtc).Take(_options.LogMaxFiles))
        {
            string content;
            try
            {
                if (snapshot.TryGetValue(file.FullName, out var previous))
                {
                    content = await ReadChangedTextAsync(file.FullName, previous.Length, _options.LogMaxBytes);
                }
                else
                {
                    content = await ReadTailTextAsync(file.FullName, _options.LogMaxBytes);
                }
            }
            catch
            {
                continue;
            }

            var eval = EvaluateEvidence(content, testCase, file.FullName, agent);
            if (eval.Success)
            {
                return eval with { MatchedLogFile = file.FullName };
            }
        }

        return EvaluateEvidence(string.Empty, testCase, "log_fallback", agent);
    }

    private static IEnumerable<string> ResolveLogRoots(string agent)
    {
        var env = Environment.GetEnvironmentVariable($"AGENT_{agent.ToUpperInvariant()}_LOG_DIRS");
        if (!string.IsNullOrWhiteSpace(env))
        {
            return env.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
        }

        return agent switch
        {
            "claude" => ["~/.claude"],
            "codex" => ["~/.codex"],
            "copilot" => ["~/.copilot", "~/.config/github-copilot", "~/.local/share/github-copilot"],
            _ => []
        };
    }

    private static string ExpandHome(string path)
    {
        if (path.StartsWith("~/", StringComparison.Ordinal))
        {
            var home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            return Path.Combine(home, path[2..]);
        }

        return path;
    }

    private static bool IsLogLike(FileInfo info)
    {
        if (!info.Exists || info.Length <= 0)
        {
            return false;
        }

        var ext = info.Extension.ToLowerInvariant();
        return ext is ".json" or ".jsonl" or ".log" or ".txt" or ".md" || string.IsNullOrEmpty(ext);
    }

    private static async Task<string> ReadTailTextAsync(string path, int maxBytes)
    {
        await using var stream = File.Open(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);

        if (stream.Length > maxBytes)
        {
            stream.Seek(-maxBytes, SeekOrigin.End);
        }

        using var reader = new StreamReader(stream, Encoding.UTF8, detectEncodingFromByteOrderMarks: true);
        return await reader.ReadToEndAsync();
    }

    private static async Task<string> ReadChangedTextAsync(string path, long previousLength, int maxBytes)
    {
        await using var stream = File.Open(path, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete);
        var fileLength = stream.Length;

        if (previousLength < 0 || previousLength >= fileLength)
        {
            return await ReadTailTextAsync(path, maxBytes);
        }

        var deltaLength = fileLength - previousLength;
        var start = previousLength;
        if (deltaLength > maxBytes)
        {
            start = fileLength - maxBytes;
        }

        stream.Seek(start, SeekOrigin.Begin);
        using var reader = new StreamReader(stream, Encoding.UTF8, detectEncodingFromByteOrderMarks: true);
        return await reader.ReadToEndAsync();
    }

    private Dictionary<string, LogFileState> CaptureLogSnapshot(string agent)
    {
        var snapshot = new Dictionary<string, LogFileState>(StringComparer.OrdinalIgnoreCase);
        var roots = ResolveLogRoots(agent)
            .Select(ExpandHome)
            .Where(Directory.Exists)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToArray();

        foreach (var root in roots)
        {
            try
            {
                foreach (var path in Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories))
                {
                    FileInfo info;
                    try
                    {
                        info = new FileInfo(path);
                    }
                    catch
                    {
                        continue;
                    }

                    if (!IsLogLike(info))
                    {
                        continue;
                    }

                    snapshot[info.FullName] = new LogFileState(info.Length, info.LastWriteTimeUtc);
                }
            }
            catch
            {
                // Ignore inaccessible trees.
            }
        }

        return snapshot;
    }

    private static EvidenceEvaluation EvaluateEvidence(string text, CaseDefinition testCase, string proofSource, string agent)
    {
        var requiredAll = BuildRequiredAllEvidence(testCase, agent);
        var requiredAny = BuildRequiredAnyEvidence(testCase);
        var requiredAllSearchText = BuildRequiredAllSearchText(text, agent);
        var claudeLaunchedSkills = string.Equals(agent, "claude", StringComparison.OrdinalIgnoreCase)
            ? ExtractClaudeLaunchedSkills(requiredAllSearchText)
            : new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        var matchedAll = new List<string>();
        var missingAll = new List<string>();
        foreach (var token in requiredAll)
        {
            var isMatched = string.Equals(agent, "claude", StringComparison.OrdinalIgnoreCase) &&
                            LooksLikeDotnetSkillId(token)
                ? claudeLaunchedSkills.Contains(token)
                : ContainsInsensitive(requiredAllSearchText, token);

            if (isMatched)
            {
                matchedAll.Add(token);
            }
            else
            {
                missingAll.Add(token);
            }
        }

        if (string.Equals(agent, "copilot", StringComparison.OrdinalIgnoreCase) &&
            testCase.RequireSkillFile &&
            !string.IsNullOrWhiteSpace(testCase.ExpectedSkill))
        {
            var copilotSkillLineToken = $"copilot_plugin_skill_path({testCase.ExpectedSkill}/SKILL.md)";
            var hasCopilotPluginSkillPath = ContainsLineWithAll(
                text,
                ".copilot/installed-plugins",
                $"{testCase.ExpectedSkill}/SKILL.md");

            if (hasCopilotPluginSkillPath)
            {
                if (!matchedAll.Contains(copilotSkillLineToken, StringComparer.OrdinalIgnoreCase))
                {
                    matchedAll.Add(copilotSkillLineToken);
                }
            }
            else if (!missingAll.Contains(copilotSkillLineToken, StringComparer.OrdinalIgnoreCase))
            {
                missingAll.Add(copilotSkillLineToken);
            }
        }

        var matchedAny = new List<string>();
        var missingAny = new List<string>();

        if (requiredAny.Count > 0)
        {
            foreach (var token in requiredAny)
            {
                if (ContainsInsensitive(text, token))
                {
                    matchedAny.Add(token);
                }
            }

            if (matchedAny.Count == 0)
            {
                missingAny.AddRange(requiredAny);
            }
        }

        var requiredAllProofLines = ExtractToolUseProofLines(requiredAllSearchText, matchedAll, proofSource);
        var requiredAnyProofLines = ExtractToolUseProofLines(text, matchedAny, proofSource);
        var proofLines = MergeProofLines(requiredAllProofLines, requiredAnyProofLines);

        return new EvidenceEvaluation(
            Success: missingAll.Count == 0 && missingAny.Count == 0,
            MatchedAll: matchedAll,
            MissingAll: missingAll,
            MatchedAny: matchedAny,
            MissingAny: missingAny,
            MatchedLogFile: null,
            ToolUseProofLines: proofLines);
    }

    private static List<ToolUseProofLine> ExtractToolUseProofLines(string text, List<string> tokens, string source)
    {
        var lines = text.Replace("\r", string.Empty).Split('\n');
        var proofs = new List<ToolUseProofLine>();

        foreach (var token in tokens)
        {
            if (string.IsNullOrWhiteSpace(token))
            {
                continue;
            }

            var candidates = new List<(int LineNumber, string Line, int Score)>();

            for (var i = 0; i < lines.Length; i++)
            {
                var line = lines[i];
                if (string.IsNullOrWhiteSpace(line) || !ContainsInsensitive(line, token))
                {
                    continue;
                }

                var score = ScoreProofLine(line, token);
                candidates.Add((i + 1, line, score));
            }

            foreach (var candidate in candidates
                         .OrderByDescending(c => c.Score)
                         .ThenBy(c => c.LineNumber)
                         .Take(2))
            {
                proofs.Add(new ToolUseProofLine
                {
                    Token = token,
                    Source = source,
                    LineNumber = candidate.LineNumber,
                    Line = candidate.Line.Length <= 500 ? candidate.Line : candidate.Line[..500] + "..."
                });

                if (proofs.Count >= 30)
                {
                    return proofs;
                }
            }
        }

        return proofs;
    }

    private static int ScoreProofLine(string line, string token)
    {
        var score = 0;

        if (LooksLikeDotnetSkillId(token))
        {
            // Prefer definitive skill invocation evidence over incidental mentions.
            if (ContainsInsensitive(line, "\"name\":\"Skill\"") &&
                ContainsInsensitive(line, $"\"skill\":\"{token}\""))
            {
                score += 1000;
            }

            if (ContainsInsensitive(line, "Launching skill:") &&
                ContainsInsensitive(line, token))
            {
                score += 900;
            }

            if (ContainsInsensitive(line, "Base directory for this skill:") &&
                ContainsInsensitive(line, token))
            {
                score += 700;
            }
        }

        if (ContainsInsensitive(line, "tool_use"))
        {
            score += 100;
        }

        if (ContainsInsensitive(line, "command_execution") ||
            ContainsInsensitive(line, "read_file") ||
            ContainsInsensitive(line, "mcp_tool_call"))
        {
            score += 60;
        }

        if (ContainsInsensitive(line, token))
        {
            score += 10;
        }

        return score;
    }

    private static List<ToolUseProofLine> MergeProofLines(List<ToolUseProofLine> first, List<ToolUseProofLine> second)
    {
        var merged = new List<ToolUseProofLine>(first);
        foreach (var line in second)
        {
            if (!merged.Any(x =>
                    string.Equals(x.Token, line.Token, StringComparison.OrdinalIgnoreCase) &&
                    string.Equals(x.Source, line.Source, StringComparison.OrdinalIgnoreCase) &&
                    x.LineNumber == line.LineNumber &&
                    string.Equals(x.Line, line.Line, StringComparison.Ordinal)))
            {
                merged.Add(line);
            }
        }

        return merged;
    }

    private string? ResolveProofLogPath()
    {
        if (!string.IsNullOrWhiteSpace(_options.ProofLogPath))
        {
            return _options.ProofLogPath;
        }

        if (!string.IsNullOrWhiteSpace(_options.OutputPath))
        {
            return _options.OutputPath + ".proof.log";
        }

        return null;
    }

    private static async Task WriteProofLogAsync(List<AgentResult> results, string proofLogPath, string batchRunId)
    {
        var dir = Path.GetDirectoryName(proofLogPath);
        if (!string.IsNullOrWhiteSpace(dir))
        {
            Directory.CreateDirectory(dir);
        }

        var sb = new StringBuilder();
        sb.AppendLine($"# Tool-Use Proof Log");
        sb.AppendLine($"# Generated UTC: {DateTimeOffset.UtcNow:O}");
        sb.AppendLine($"# Batch Run ID: {batchRunId}");
        sb.AppendLine();

        foreach (var result in results)
        {
            sb.AppendLine($"=== agent={result.Agent} case_id={result.CaseId} unit_run_id={result.UnitRunId} status={result.Status} source={result.Source}");
            if (!string.IsNullOrWhiteSpace(result.FailureKind))
            {
                sb.AppendLine($"failure_kind={result.FailureKind}");
            }

            if (!string.IsNullOrWhiteSpace(result.FailureCategory))
            {
                sb.AppendLine($"failure_category={result.FailureCategory}");
            }

            if (!string.IsNullOrWhiteSpace(result.Error))
            {
                sb.AppendLine($"error={result.Error}");
            }

            if (result.MatchedEvidence.Count > 0)
            {
                sb.AppendLine("matched_evidence=" + string.Join(", ", result.MatchedEvidence));
            }

            if (result.MissingEvidence.Count > 0)
            {
                sb.AppendLine("missing_evidence=" + string.Join(", ", result.MissingEvidence));
            }

            sb.AppendLine("tool_use_proof_lines:");
            if (result.ToolUseProofLines.Count == 0)
            {
                sb.AppendLine("  (none)");
            }
            else
            {
                foreach (var proof in result.ToolUseProofLines)
                {
                    sb.AppendLine($"  [{proof.Token}] {proof.Source}:{proof.LineNumber} {proof.Line}");
                }
            }

            sb.AppendLine();
        }

        await File.WriteAllTextAsync(proofLogPath, sb.ToString());
    }

    private static List<string> BuildRequiredAllEvidence(CaseDefinition testCase, string agent)
    {
        var all = new List<string>();
        var isClaude = string.Equals(agent, "claude", StringComparison.OrdinalIgnoreCase);

        AddDistinct(all, testCase.RequiredAllEvidence);
        AddDistinct(all, testCase.RequiredEvidence);

        if (!string.IsNullOrWhiteSpace(testCase.ExpectedSkill))
        {
            AddDistinct(all, [testCase.ExpectedSkill]);
        }

        if (testCase.RequireSkillFile)
        {
            // Claude does not reliably emit SKILL.md file read traces.
            // For Claude, require definitive Skill-tool invocation instead.
            if (!isClaude)
            {
                if (!string.IsNullOrWhiteSpace(testCase.ExpectedSkill))
                {
                    // Skill-specific path only — prevents false-positive matches
                    // from incidental SKILL.md mentions in unrelated output.
                    AddDistinct(all, [$"{testCase.ExpectedSkill}/SKILL.md"]);
                }
                else
                {
                    // Fallback to generic when no expected skill is set.
                    AddDistinct(all, ["SKILL.md"]);
                }
            }
        }

        if (isClaude)
        {
            all.RemoveAll(token =>
                string.Equals(token, "SKILL.md", StringComparison.OrdinalIgnoreCase) ||
                token.EndsWith("/SKILL.md", StringComparison.OrdinalIgnoreCase));
        }

        return all;
    }

    private static List<string> BuildRequiredAnyEvidence(CaseDefinition testCase)
    {
        var any = new List<string>();

        AddDistinct(any, DefaultAnyEvidence);
        AddDistinct(any, testCase.RequiredAnyEvidence);
        return any;
    }

    private static void AddDistinct(List<string> destination, IEnumerable<string> source)
    {
        foreach (var token in source)
        {
            if (string.IsNullOrWhiteSpace(token))
            {
                continue;
            }

            if (!destination.Contains(token, StringComparer.OrdinalIgnoreCase))
            {
                destination.Add(token);
            }
        }
    }

    private static bool LooksLikeDotnetSkillId(string token)
    {
        return token.StartsWith("dotnet-", StringComparison.OrdinalIgnoreCase);
    }

    private static HashSet<string> ExtractClaudeLaunchedSkills(string text)
    {
        var launched = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var lines = text.Replace("\r", string.Empty).Split('\n');

        foreach (var line in lines)
        {
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            if (ContainsInsensitive(line, "\"name\":\"Skill\""))
            {
                foreach (Match match in ClaudeSkillFieldRegex.Matches(line))
                {
                    if (match.Groups.Count < 2)
                    {
                        continue;
                    }

                    AddSkillVariants(launched, match.Groups[1].Value);
                }
            }

            foreach (Match match in ClaudeLaunchingSkillRegex.Matches(line))
            {
                if (match.Groups.Count < 2)
                {
                    continue;
                }

                AddSkillVariants(launched, match.Groups[1].Value);
            }
        }

        return launched;
    }

    private static void AddSkillVariants(HashSet<string> set, string rawSkill)
    {
        if (string.IsNullOrWhiteSpace(rawSkill))
        {
            return;
        }

        var skill = rawSkill.Trim();
        set.Add(skill);

        var lastColon = skill.LastIndexOf(':');
        if (lastColon >= 0 && lastColon + 1 < skill.Length)
        {
            set.Add(skill[(lastColon + 1)..]);
        }
    }

    private static bool ContainsInsensitive(string source, string token)
    {
        return source.Contains(token, StringComparison.OrdinalIgnoreCase);
    }

    private static string BuildRequiredAllSearchText(string text, string agent)
    {
        var lines = text.Replace("\r", string.Empty).Split('\n');
        var sb = new StringBuilder();

        foreach (var line in lines)
        {
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            if (IsMetadataNoiseForRequiredAll(line, agent))
            {
                continue;
            }

            sb.AppendLine(line);
        }

        return sb.ToString();
    }

    private static bool IsMetadataNoiseForRequiredAll(string line, string agent)
    {
        if (ContainsInsensitive(line, "\"type\":\"system\"") ||
            ContainsInsensitive(line, "\"type\":\"queue-operation\"") ||
            ContainsInsensitive(line, "\"subtype\":\"init\"") ||
            ContainsInsensitive(line, "\"subtype\":\"hook_"))
        {
            return true;
        }

        if (!string.Equals(agent, "claude", StringComparison.OrdinalIgnoreCase))
        {
            return false;
        }

        return ContainsInsensitive(line, "[DEBUG] Hooks:") ||
               ContainsInsensitive(line, "Hook SessionStart:startup") ||
               ContainsInsensitive(line, "Skill prompt: showing") ||
               ContainsInsensitive(line, "Attempting to load skills from plugin") ||
               ContainsInsensitive(line, "Loading from skillPath:") ||
               ContainsInsensitive(line, "Loaded 1 skills from plugin") ||
               ContainsInsensitive(line, "Sending 230 skills via attachment");
    }

    private static bool ContainsLineWithAll(string text, params string[] tokens)
    {
        var lines = text.Replace("\r", string.Empty).Split('\n');
        foreach (var line in lines)
        {
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            var matchesAll = true;
            foreach (var token in tokens)
            {
                if (!ContainsInsensitive(line, token))
                {
                    matchesAll = false;
                    break;
                }
            }

            if (matchesAll)
            {
                return true;
            }
        }

        return false;
    }

    /// <summary>
    /// Detects bash "command not found" (exit 127) or "permission denied" (exit 126)
    /// which indicate a missing or non-executable CLI binary -- a transport failure.
    /// </summary>
    private static bool IsCommandNotFound(ExecutionResult exec)
    {
        if (exec.ExitCode is not (126 or 127))
        {
            return false;
        }

        var stderr = exec.Stderr ?? string.Empty;
        return ContainsInsensitive(stderr, "command not found") ||
               ContainsInsensitive(stderr, "No such file or directory") ||
               ContainsInsensitive(stderr, "Permission denied");
    }

    private static string CombineOutput(string? stdout, string? stderr)
    {
        return (stdout ?? string.Empty) + "\n" + (stderr ?? string.Empty);
    }

    private static string? TrimExcerpt(string? text)
    {
        if (string.IsNullOrWhiteSpace(text))
        {
            return null;
        }

        var normalized = text.Replace("\r", string.Empty);
        return normalized.Length <= 2500 ? normalized : normalized[..2500] + "...";
    }

    private async Task<List<CaseDefinition>> LoadCasesAsync(string path)
    {
        await using var stream = File.OpenRead(path);

        var list = await JsonSerializer.DeserializeAsync<List<CaseDefinition>>(stream, _jsonOptions);
        if (list is { Count: > 0 })
        {
            return list;
        }

        stream.Position = 0;
        var wrapped = await JsonSerializer.DeserializeAsync<CasesDocument>(stream, _jsonOptions);
        return wrapped?.Cases ?? [];
    }

    private static async Task<ExecutionResult> ExecuteCommandAsync(string command, int timeoutSeconds)
    {
        using var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = "/bin/bash",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            }
        };

        process.StartInfo.ArgumentList.Add("-lc");
        process.StartInfo.ArgumentList.Add(command);

        try
        {
            if (!process.Start())
            {
                return new ExecutionResult(false, -1, string.Empty, string.Empty, false, "Process.Start returned false");
            }

            var stdoutTask = process.StandardOutput.ReadToEndAsync();
            var stderrTask = process.StandardError.ReadToEndAsync();

            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(timeoutSeconds));

            try
            {
                await process.WaitForExitAsync(timeout.Token);
            }
            catch (OperationCanceledException)
            {
                try
                {
                    process.Kill(entireProcessTree: true);
                }
                catch
                {
                    // Ignore kill failure.
                }

                var timedOutStdout = await stdoutTask;
                var timedOutStderr = await stderrTask;

                return new ExecutionResult(true, process.HasExited ? process.ExitCode : -1, timedOutStdout, timedOutStderr, true, null);
            }

            var stdout = await stdoutTask;
            var stderr = await stderrTask;

            return new ExecutionResult(true, process.ExitCode, stdout, stderr, false, null);
        }
        catch (Exception ex)
        {
            return new ExecutionResult(false, -1, string.Empty, string.Empty, false, ex.Message);
        }
    }
}

internal sealed class RunnerOptions
{
    public string InputPath { get; init; } = "tests/agent-routing/cases.json";
    public string? OutputPath { get; init; }
    public string? ProofLogPath { get; init; }
    public string ArtifactsRoot { get; init; } = "tests/agent-routing/artifacts";
    public int TimeoutSeconds { get; init; } = 90;
    public int MaxParallel { get; init; } = 4;
    public int LogMaxFiles { get; init; } = 60;
    public int LogMaxBytes { get; init; } = 300_000;
    public bool Progress { get; init; } = true;
    public bool EnableLogScan { get; init; } = true;
    public bool FailOnInfra { get; init; }
    public bool ShowHelp { get; init; }
    public HashSet<string> Agents { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public HashSet<string> Categories { get; init; } = new(StringComparer.OrdinalIgnoreCase);
    public HashSet<string> CaseIds { get; init; } = new(StringComparer.OrdinalIgnoreCase);

    public static RunnerOptions Parse(string[] args)
    {
        string input = "tests/agent-routing/cases.json";
        string? output = null;
        string? proofLog = null;
        string artifactsRoot = "tests/agent-routing/artifacts";
        int timeoutSeconds = 90;
        int logMaxFiles = 60;
        int logMaxBytes = 300_000;
        bool progress = true;
        bool failOnInfra = false;
        bool showHelp = false;
        var agents = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var categories = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var caseIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        // MAX_CONCURRENCY: default 4, env fallback, --max-parallel flag precedence
        int maxParallel = 4;
        var envMaxConcurrency = Environment.GetEnvironmentVariable("MAX_CONCURRENCY");
        if (!string.IsNullOrWhiteSpace(envMaxConcurrency) &&
            int.TryParse(envMaxConcurrency, out var envParsed) && envParsed > 0)
        {
            maxParallel = envParsed;
        }

        bool maxParallelExplicit = false;
        bool? enableLogScanExplicit = null;

        for (var i = 0; i < args.Length; i++)
        {
            var arg = args[i];
            switch (arg)
            {
                case "-h":
                case "--help":
                    showHelp = true;
                    break;
                case "--input":
                    input = ReadValue(args, ref i, "--input");
                    break;
                case "--output":
                    output = ReadValue(args, ref i, "--output");
                    break;
                case "--proof-log":
                    proofLog = ReadValue(args, ref i, "--proof-log");
                    break;
                case "--artifacts-root":
                    artifactsRoot = ReadValue(args, ref i, "--artifacts-root");
                    break;
                case "--timeout-seconds":
                    timeoutSeconds = ParsePositiveInt(ReadValue(args, ref i, "--timeout-seconds"), "--timeout-seconds");
                    break;
                case "--max-parallel":
                    maxParallel = ParsePositiveInt(ReadValue(args, ref i, "--max-parallel"), "--max-parallel");
                    maxParallelExplicit = true;
                    break;
                case "--log-max-files":
                    logMaxFiles = ParsePositiveInt(ReadValue(args, ref i, "--log-max-files"), "--log-max-files");
                    break;
                case "--log-max-bytes":
                    logMaxBytes = ParsePositiveInt(ReadValue(args, ref i, "--log-max-bytes"), "--log-max-bytes");
                    break;
                case "--no-progress":
                    progress = false;
                    break;
                case "--enable-log-scan":
                    enableLogScanExplicit = true;
                    break;
                case "--disable-log-scan":
                    enableLogScanExplicit = false;
                    break;
                case "--agents":
                    AddCsv(ReadValue(args, ref i, "--agents"), agents);
                    break;
                case "--category":
                case "--categories":
                    AddCsv(ReadValue(args, ref i, arg), categories);
                    break;
                case "--case":
                case "--case-id":
                    AddCsv(ReadValue(args, ref i, arg), caseIds);
                    break;
                case "--run-all":
                    break;
                case "--fail-on-infra":
                    failOnInfra = true;
                    break;
                default:
                    throw new ArgumentException($"Unknown argument: {arg}");
            }
        }

        // --enable-log-scan: explicit flag wins, otherwise on when serial (maxParallel==1), off when parallel
        bool enableLogScan = enableLogScanExplicit ?? (maxParallel == 1);

        return new RunnerOptions
        {
            InputPath = input,
            OutputPath = output,
            ProofLogPath = proofLog,
            ArtifactsRoot = artifactsRoot,
            TimeoutSeconds = timeoutSeconds,
            MaxParallel = maxParallel,
            LogMaxFiles = logMaxFiles,
            LogMaxBytes = logMaxBytes,
            Progress = progress,
            EnableLogScan = enableLogScan,
            FailOnInfra = failOnInfra,
            ShowHelp = showHelp,
            Agents = agents,
            Categories = categories,
            CaseIds = caseIds
        };
    }

    private static string ReadValue(string[] args, ref int index, string flag)
    {
        if (index + 1 >= args.Length)
        {
            throw new ArgumentException($"Missing value for {flag}");
        }

        index++;
        return args[index];
    }

    private static int ParsePositiveInt(string raw, string flag)
    {
        if (!int.TryParse(raw, out var parsed) || parsed <= 0)
        {
            throw new ArgumentException($"Invalid {flag} value: {raw}");
        }

        return parsed;
    }

    private static void AddCsv(string raw, HashSet<string> target)
    {
        foreach (var part in raw.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
        {
            target.Add(part);
        }
    }

    public static void PrintHelp()
    {
        Console.WriteLine(
            """
            Agent skill routing checker (live only)

            Usage:
              dotnet run --file tests/agent-routing/check-skills.cs -- [options]

            Options:
              --input <path>            Cases file path (default: tests/agent-routing/cases.json)
              --agents <csv>            Agents filter (default: claude,codex,copilot)
              --category <csv>          Category filter
              --case-id <csv>           Case-id filter
              --timeout-seconds <int>   Per-invocation timeout (default: 90)
              --max-parallel <int>      Max concurrent case/agent runs (default: 4)
                                        Precedence: --max-parallel flag > MAX_CONCURRENCY env > default 4
              --log-max-files <int>     Max recent log files scanned (default: 60)
              --log-max-bytes <int>     Max bytes read from each log file tail (default: 300000)
              --no-progress             Disable stderr lifecycle progress output
              --output <path>           Optional additional JSON output path (backward compat)
              --proof-log <path>        Optional additional proof log path (backward compat)
              --artifacts-root <path>   Base directory for per-batch artifact isolation
                                        (default: tests/agent-routing/artifacts)
              --enable-log-scan         Enable log file scanning (default: on when serial, off when parallel)
              --disable-log-scan        Disable log file scanning
              --fail-on-infra           Exit non-zero when infra_error exists
              --help                    Show this help

            Environment:
              MAX_CONCURRENCY           Fallback for --max-parallel (flag takes precedence)
              AGENT_<NAME>_TEMPLATE     Command template override per agent
              AGENT_<NAME>_LOG_DIRS     Log directory override per agent (path-separator delimited)

            Artifacts:
              Results and proof logs are always written to <artifacts-root>/<batch_run_id>/.
              ARTIFACT_DIR=<path> is emitted on stderr as protocol output (always, even with --no-progress).
            """);
    }
}

internal sealed record CasesDocument
{
    [JsonPropertyName("cases")]
    public List<CaseDefinition> Cases { get; init; } = [];
}

internal sealed record CaseDefinition
{
    [JsonPropertyName("case_id")]
    public string CaseId { get; init; } = string.Empty;

    [JsonPropertyName("category")]
    public string Category { get; init; } = string.Empty;

    [JsonPropertyName("prompt")]
    public string Prompt { get; init; } = string.Empty;

    [JsonPropertyName("expected_skill")]
    public string ExpectedSkill { get; init; } = string.Empty;

    [JsonPropertyName("required_all_evidence")]
    public string[] RequiredAllEvidence { get; init; } = [];

    [JsonPropertyName("required_any_evidence")]
    public string[] RequiredAnyEvidence { get; init; } = [];

    [JsonPropertyName("required_evidence")]
    public string[] RequiredEvidence { get; init; } = [];

    [JsonPropertyName("require_skill_file")]
    public bool RequireSkillFile { get; init; } = true;
}

internal sealed record EvidenceEvaluation(
    bool Success,
    List<string> MatchedAll,
    List<string> MissingAll,
    List<string> MatchedAny,
    List<string> MissingAny,
    string? MatchedLogFile,
    List<ToolUseProofLine> ToolUseProofLines)
{
    public List<string> MatchedEvidence =>
    [
        .. MatchedAll,
        .. MatchedAny.Where(token => !MatchedAll.Contains(token, StringComparer.OrdinalIgnoreCase))
    ];

    public List<string> MissingEvidence =>
    [
        .. MissingAll,
        .. (MissingAny.Count > 0
            ? new[] { $"any_of({string.Join("|", MissingAny)})" }
            : Array.Empty<string>())
    ];

    public static EvidenceEvaluation Merge(EvidenceEvaluation first, EvidenceEvaluation second)
    {
        var matchedAll = new List<string>(first.MatchedAll);
        foreach (var token in second.MatchedAll)
        {
            if (!matchedAll.Contains(token, StringComparer.OrdinalIgnoreCase))
            {
                matchedAll.Add(token);
            }
        }

        var matchedAny = new List<string>(first.MatchedAny);
        foreach (var token in second.MatchedAny)
        {
            if (!matchedAny.Contains(token, StringComparer.OrdinalIgnoreCase))
            {
                matchedAny.Add(token);
            }
        }

        var missingAll = first.MissingAll
            .Where(token => !matchedAll.Contains(token, StringComparer.OrdinalIgnoreCase))
            .ToList();

        var missingAny = first.MissingAny.Count == 0 || second.MatchedAny.Count > 0
            ? new List<string>()
            : new List<string>(first.MissingAny);

        return new EvidenceEvaluation(
            Success: missingAll.Count == 0 && missingAny.Count == 0,
            MatchedAll: matchedAll,
            MissingAll: missingAll,
            MatchedAny: matchedAny,
            MissingAny: missingAny,
            MatchedLogFile: second.MatchedLogFile ?? first.MatchedLogFile,
            ToolUseProofLines: MergeProofLines(first.ToolUseProofLines, second.ToolUseProofLines));
    }

    private static List<ToolUseProofLine> MergeProofLines(List<ToolUseProofLine> first, List<ToolUseProofLine> second)
    {
        var merged = new List<ToolUseProofLine>(first);
        foreach (var line in second)
        {
            if (!merged.Any(x =>
                    string.Equals(x.Token, line.Token, StringComparison.OrdinalIgnoreCase) &&
                    string.Equals(x.Source, line.Source, StringComparison.OrdinalIgnoreCase) &&
                    x.LineNumber == line.LineNumber &&
                    string.Equals(x.Line, line.Line, StringComparison.Ordinal)))
            {
                merged.Add(line);
            }
        }

        return merged;
    }
}

internal sealed class ToolUseProofLine
{
    [JsonPropertyName("token")]
    public string Token { get; init; } = string.Empty;

    [JsonPropertyName("source")]
    public string Source { get; init; } = string.Empty;

    [JsonPropertyName("line_number")]
    public int LineNumber { get; init; }

    [JsonPropertyName("line")]
    public string Line { get; init; } = string.Empty;
}

internal sealed record ExecutionResult(
    bool Started,
    int ExitCode,
    string? Stdout,
    string? Stderr,
    bool TimedOut,
    string? ErrorMessage);

internal sealed record LogFileState(long Length, DateTime LastWriteUtc);

internal sealed class ResultEnvelope
{
    [JsonPropertyName("batch_run_id")]
    public string BatchRunId { get; init; } = string.Empty;

    [JsonPropertyName("generated_at_utc")]
    public DateTimeOffset GeneratedAtUtc { get; init; }

    [JsonPropertyName("summary")]
    public Summary Summary { get; init; } = new();

    [JsonPropertyName("options")]
    public ResultOptions Options { get; init; } = new();

    [JsonPropertyName("results")]
    public List<AgentResult> Results { get; init; } = [];
}

internal sealed class ResultOptions
{
    [JsonPropertyName("input")]
    public string Input { get; init; } = string.Empty;

    [JsonPropertyName("agents")]
    public string[] Agents { get; init; } = [];

    [JsonPropertyName("categories")]
    public string[] Categories { get; init; } = [];

    [JsonPropertyName("case_ids")]
    public string[] CaseIds { get; init; } = [];

    [JsonPropertyName("timeout_seconds")]
    public int TimeoutSeconds { get; init; }

    [JsonPropertyName("max_parallel")]
    public int MaxParallel { get; init; }

    [JsonPropertyName("log_max_files")]
    public int LogMaxFiles { get; init; }

    [JsonPropertyName("log_max_bytes")]
    public int LogMaxBytes { get; init; }

    [JsonPropertyName("progress")]
    public bool Progress { get; init; }

    [JsonPropertyName("artifacts_root")]
    public string ArtifactsRoot { get; init; } = string.Empty;

    [JsonPropertyName("enable_log_scan")]
    public bool EnableLogScan { get; init; }
}

internal sealed class Summary
{
    [JsonPropertyName("total")]
    public int Total { get; init; }

    [JsonPropertyName("pass")]
    public int Pass { get; init; }

    [JsonPropertyName("fail")]
    public int Fail { get; init; }

    [JsonPropertyName("infra_error")]
    public int InfraError { get; init; }
}

internal sealed class AgentResult
{
    [JsonPropertyName("unit_run_id")]
    public string UnitRunId { get; init; } = string.Empty;

    [JsonPropertyName("agent")]
    public string Agent { get; init; } = string.Empty;

    [JsonPropertyName("case_id")]
    public string CaseId { get; init; } = string.Empty;

    [JsonPropertyName("category")]
    public string Category { get; init; } = string.Empty;

    [JsonPropertyName("status")]
    public string Status { get; init; } = string.Empty;

    [JsonPropertyName("expected_skill")]
    public string ExpectedSkill { get; init; } = string.Empty;

    [JsonPropertyName("source")]
    public string Source { get; init; } = "none";

    [JsonPropertyName("matched_evidence")]
    public List<string> MatchedEvidence { get; init; } = [];

    [JsonPropertyName("missing_evidence")]
    public List<string> MissingEvidence { get; init; } = [];

    [JsonPropertyName("matched_log_file")]
    public string? MatchedLogFile { get; init; }

    [JsonPropertyName("tool_use_proof_lines")]
    public List<ToolUseProofLine> ToolUseProofLines { get; init; } = [];

    [JsonPropertyName("error")]
    public string? Error { get; init; }

    [JsonPropertyName("duration_ms")]
    public long DurationMs { get; init; }

    [JsonPropertyName("command")]
    public string? Command { get; init; }

    [JsonPropertyName("exit_code")]
    public int? ExitCode { get; init; }

    [JsonPropertyName("output_excerpt")]
    public string? OutputExcerpt { get; init; }

    [JsonPropertyName("timed_out")]
    public bool TimedOut { get; init; }

    [JsonPropertyName("failure_kind")]
    public string? FailureKind { get; init; }

    [JsonPropertyName("failure_category")]
    public string? FailureCategory { get; init; }

    public static AgentResult Pass(
        string agent,
        CaseDefinition testCase,
        long durationMs,
        string source,
        EvidenceEvaluation evidence,
        string? command,
        int? exitCode,
        string? outputExcerpt,
        bool timedOut,
        string unitRunId,
        string? error = null)
    {
        return new AgentResult
        {
            UnitRunId = unitRunId,
            Agent = agent,
            CaseId = testCase.CaseId,
            Category = testCase.Category,
            Status = ResultStatus.Pass,
            ExpectedSkill = testCase.ExpectedSkill,
            Source = source,
            MatchedEvidence = evidence.MatchedEvidence,
            MissingEvidence = evidence.MissingEvidence,
            MatchedLogFile = evidence.MatchedLogFile,
            ToolUseProofLines = evidence.ToolUseProofLines,
            Error = error,
            DurationMs = durationMs,
            Command = command,
            ExitCode = exitCode,
            OutputExcerpt = outputExcerpt,
            TimedOut = timedOut,
            FailureKind = null,
            FailureCategory = null
        };
    }

    public static AgentResult Fail(
        string agent,
        CaseDefinition testCase,
        long durationMs,
        string source,
        EvidenceEvaluation evidence,
        string? command,
        int? exitCode,
        string? outputExcerpt,
        bool timedOut,
        string unitRunId,
        string? error = null)
    {
        var failureKind = ClassifyFailure(testCase, evidence);
        var failureCategory = ClassifyFailureCategory(timedOut, started: true, status: ResultStatus.Fail);

        return new AgentResult
        {
            UnitRunId = unitRunId,
            Agent = agent,
            CaseId = testCase.CaseId,
            Category = testCase.Category,
            Status = ResultStatus.Fail,
            ExpectedSkill = testCase.ExpectedSkill,
            Source = source,
            MatchedEvidence = evidence.MatchedEvidence,
            MissingEvidence = evidence.MissingEvidence,
            MatchedLogFile = evidence.MatchedLogFile,
            ToolUseProofLines = evidence.ToolUseProofLines,
            Error = error,
            DurationMs = durationMs,
            Command = command,
            ExitCode = exitCode,
            OutputExcerpt = outputExcerpt,
            TimedOut = timedOut,
            FailureKind = failureKind,
            FailureCategory = failureCategory
        };
    }

    public static AgentResult Infra(
        string agent,
        CaseDefinition testCase,
        string error,
        long durationMs,
        string source,
        string unitRunId,
        string? command = null,
        int? exitCode = null,
        string? outputExcerpt = null,
        EvidenceEvaluation? evidence = null,
        bool timedOut = false)
    {
        var failureCategory = ClassifyFailureCategory(timedOut, started: false, status: ResultStatus.Infra);

        return new AgentResult
        {
            UnitRunId = unitRunId,
            Agent = agent,
            CaseId = testCase.CaseId,
            Category = testCase.Category,
            Status = ResultStatus.Infra,
            ExpectedSkill = testCase.ExpectedSkill,
            Source = source,
            MatchedEvidence = evidence?.MatchedEvidence ?? [],
            MissingEvidence = evidence?.MissingEvidence ?? [],
            MatchedLogFile = evidence?.MatchedLogFile,
            ToolUseProofLines = evidence?.ToolUseProofLines ?? [],
            Error = error,
            DurationMs = durationMs,
            Command = command,
            ExitCode = exitCode,
            OutputExcerpt = outputExcerpt,
            TimedOut = timedOut,
            FailureKind = null,
            FailureCategory = failureCategory
        };
    }

    /// <summary>
    /// Deterministic failure category mapping with priority order: timeout > transport > assertion > null.
    /// Orthogonal to routing mismatch failure_kind.
    /// </summary>
    internal static string? ClassifyFailureCategory(bool timedOut, bool started, string status)
    {
        // Priority 1: timeout
        if (timedOut)
        {
            return FailureCategories.Timeout;
        }

        // Priority 2: transport (process failed to start, CLI missing, or infra_error status)
        if (!started || string.Equals(status, ResultStatus.Infra, StringComparison.Ordinal))
        {
            return FailureCategories.Transport;
        }

        // Priority 3: assertion (evidence gating failed, not timed out)
        if (string.Equals(status, ResultStatus.Fail, StringComparison.Ordinal))
        {
            return FailureCategories.Assertion;
        }

        // Pass results have no failure category
        return null;
    }

    private static string ClassifyFailure(CaseDefinition testCase, EvidenceEvaluation evidence)
    {
        var missingSkill = evidence.MissingAll.Contains(testCase.ExpectedSkill, StringComparer.OrdinalIgnoreCase);
        // Detect missing skill-file evidence as any missing token ending with "/SKILL.md".
        // This handles both skill-specific paths (e.g. "dotnet-xunit/SKILL.md") and
        // the legacy generic "SKILL.md" token (when no ExpectedSkill is set).
        var missingSkillFile = evidence.MissingAll.Any(token =>
            token.EndsWith("/SKILL.md", StringComparison.OrdinalIgnoreCase) ||
            string.Equals(token, "SKILL.md", StringComparison.OrdinalIgnoreCase));
        var missingAny = evidence.MissingAny.Count > 0;

        if (missingSkill && !missingAny)
        {
            return FailureKinds.SkillNotLoaded;
        }

        if (missingSkill && missingAny)
        {
            return FailureKinds.MixedEvidenceMissing;
        }

        if (missingSkillFile && !missingAny && !missingSkill)
        {
            return FailureKinds.MissingSkillFileEvidence;
        }

        if (missingAny && !missingSkill && !missingSkillFile)
        {
            return FailureKinds.MissingActivityEvidence;
        }

        return FailureKinds.Unknown;
    }
}
