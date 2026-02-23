# Pitfalls

Lessons learned from NEEDS_WORK feedback. Things models tend to miss.

<!-- Entries added automatically by hooks or manually via `flowctl memory add` -->

## 2026-02-12 manual [pitfall]
When spec requires [skill:name] cross-reference syntax, use it for ALL skill references (catalog entries, routing targets, etc.) -- not just the first few. Bare text skill names are not machine-parseable.

## 2026-02-12 manual [pitfall]
.NET STS lifecycle is 18 months from GA (not 12). If GA Nov 2026, STS end is ~May 2028. Always calculate from actual GA date, not release year.

## 2026-02-12 manual [pitfall]
NuGet/MSBuild config files (Directory.Packages.props, nuget.config) resolve hierarchically upward, not just at solution root. Always instruct upward search for monorepo compatibility.

## 2026-02-12 manual [pitfall]
When documenting TFM patterns for platform detection (MAUI, Uno), use version-agnostic globs (net*-android) not hardcoded versions (net10.0-android) to avoid false negatives on older/newer TFMs.

## 2026-02-12 manual [pitfall]
Bash validation scripts that compare lines to exact strings (like '---') must normalize CRLF to LF first, or Windows-edited files will fail with false negatives.

## 2026-02-12 manual [pitfall]
macOS default /bin/bash is 3.2 (no associative arrays). Scripts using declare -A must guard with BASH_VERSINFO check or use #!/usr/bin/env bash + require Homebrew bash 4+.

## 2026-02-12 manual [pitfall]
BSD sort on macOS lacks GNU sort -z flag. Use find -print0 without sort, or sort in a portable way, when targeting cross-platform scripts.

## 2026-02-12 manual [pitfall]
Validation scripts that accept optional dependencies (e.g. PyYAML) produce environment-dependent behavior; use a single deterministic parser for CI parity

## 2026-02-12 manual [pitfall]
Path validation must use realpath (symlink-resolving) canonicalization, not just cd+pwd, to prevent symlink escape

## 2026-02-12 manual [pitfall]
GHA bash steps with set -e do NOT propagate non-zero exit from non-final pipeline commands; add 'set -o pipefail' before any pipe (e.g. script | tee) to avoid false-green CI

## 2026-02-12 manual [pitfall]
CI workflows must run the EXACT same validation commands as local -- do not inject CI-only env vars or flags; encode policy differences in the shared script with an opt-in override

## 2026-02-12 manual [pitfall]
Options pattern classes must use { get; set; } not { get; init; } because config binder and PostConfigure need to mutate properties after construction

## 2026-02-12 manual [pitfall]
Source generator AddSource hint names must include namespace to avoid collisions when same class name exists in different namespaces

## 2026-02-12 manual [pitfall]
When adding new skills, always register them in plugin.json skills array -- files on disk without registration are invisible to the plugin system

## 2026-02-12 manual [pitfall]
NuGet packageSourceMapping uses most-specific-pattern-wins: MyCompany.* beats * wildcard. Always explain precedence when documenting private feed configs to avoid dependency confusion FUD.

## 2026-02-12 manual [pitfall]
Trimming/AOT MSBuild properties differ by project type: apps use PublishTrimmed/PublishAot + EnableTrimAnalyzer/EnableAotAnalyzer; libraries use IsTrimmable/IsAotCompatible (which auto-enable analyzers). Mixing them up sets incorrect package metadata.

## 2026-02-12 manual [pitfall]
When documenting package replacements (e.g. Swashbuckle->OpenAPI), always note conditions where the old package is still needed -- unconditional 'replace X with Y' causes feature regressions in complex setups

## 2026-02-12 manual [pitfall]
ASP.NET shared-framework NuGet packages (e.g. Microsoft.AspNetCore.Mvc.Testing) must match the project TFM major version -- hardcoding a specific version in guidance will break users on different TFMs

## 2026-02-12 manual [pitfall]
Cross-reference skill IDs must use canonical names from target epic (e.g., dotnet-csharp-async-patterns not dotnet-async-patterns) — verify with grep against actual SKILL.md name: fields

## 2026-02-12 manual [pitfall]
Idempotency implementations must handle three states (no-record, in-progress, completed) -- check-then-act without guarding the in-progress state allows concurrent duplicate execution

## 2026-02-12 manual [pitfall]
Idempotency record finalization must be unconditional -- gating completion on specific IResult subtypes (e.g. IValueHttpResult) leaves non-value results (NoContent, Accepted) permanently stuck in in-progress state

## 2026-02-12 manual [pitfall]
IHttpClientFactory handler order: AddHttpMessageHandler first = outermost, AddStandardResilienceHandler last = innermost (wraps HTTP call). Retries do NOT re-execute outer DelegatingHandlers. Ensure all guidance in a skill is internally consistent on this point.

## 2026-02-12 manual [pitfall]
Skill code examples that use third-party NuGet APIs (extension methods, types) must list those packages explicitly -- AI agents cannot resolve unlisted packages and will produce non-compiling code

## 2026-02-12 manual [pitfall]
MSBuild container publish items (ContainerPort, ContainerEnvironmentVariable, ContainerLabel) must go in ItemGroup, not PropertyGroup -- they use Include= attribute syntax which is item metadata, not property syntax

## 2026-02-12 manual [pitfall]
Cross-task file edits (even single-line cross-refs) violate file-disjoint constraints — attribute such edits to the integration task, not the content-authoring task

## 2026-02-12 manual [pitfall]
When a boundary enforcement has multiple mechanisms (prose vs placeholder), pick ONE and normalize across ALL epic sections (matrix, decomposition, acceptance, task specs, quick commands) — mixed models cause reviewer churn

## 2026-02-12 manual [pitfall]
ConfigureHttpJsonOptions applies to Minimal APIs only, not MVC controllers -- controllers need .AddControllers().AddJsonOptions() as a separate registration

## 2026-02-12 manual [pitfall]
Code examples using IHubContext must pass user/entity IDs as method parameters -- do not reference variables from an outer scope that does not exist in the snippet

## 2026-02-12 manual [pitfall]
WebSocket endpoint examples must include app.UseWebSockets() middleware call -- ASP.NET Core requires it for upgrade handling before any WebSocket endpoint mapping

## 2026-02-12 manual [pitfall]
When multiple tasks in an epic each register entries in a shared file (e.g., plugin.json), assign sole ownership of that file to one integration task to avoid merge conflicts and weak parallelizability

## 2026-02-12 manual [pitfall]
xUnit [Collection("Name")] on a test class requires a matching [CollectionDefinition("Name")] marker class with ICollectionFixture<T> -- without it, fixture injection silently fails

## 2026-02-12 manual [pitfall]
Code examples using xUnit Skip.IfNot() require the Xunit.SkippableFact package and [SkippableFact] attribute -- plain [Fact] with Skip.IfNot() does not compile without this dependency

## 2026-02-12 manual [pitfall]
builder.WebHost.ConfigureKestrel() must be called BEFORE builder.Build() -- Kestrel/host config after Build() is invalid and silently ignored

## 2026-02-12 manual [pitfall]
Code examples using IOptionsMonitor must read CurrentValue at call site (not constructor) to actually observe runtime changes -- snapshotting in constructor defeats the purpose

## 2026-02-12 manual [pitfall]
DI singleton factory registrations only run when explicitly resolved -- for always-active subscriptions (IOptionsMonitor.OnChange), use IHostedService which the host guarantees to activate

## 2026-02-12 manual [pitfall]
Security code examples must use defensive parsing (TryFromBase64String, length validation) on attacker-controlled input -- avoid exception-driven rejection in auth paths

## 2026-02-12 manual [pitfall]
Use BinaryPrimitives (fixed endianness) instead of BitConverter (host-endian) when encoding data persisted or transmitted across platforms

## 2026-02-12 manual [pitfall]
Acceptance criteria must explicitly test EVERY scope item — reviewers flag any scope bullet not mirrored in AC as a gap

## 2026-02-12 manual [pitfall]
When documenting package replacements (e.g. Swashbuckle->OpenAPI), say 'preferred/default' not 'deprecated' unless the package is formally deprecated -- overstating removal misleads agents into breaking valid setups

## 2026-02-12 manual [pitfall]
grep example commands in skill docs must use POSIX character classes ([[:space:]] not \s) and -E flag for ERE -- BRE grep does not support \s and silently mismatches

## 2026-02-12 manual [pitfall]
SDK-style projects auto-include all *.cs files; TFM-conditional Compile Include without a preceding Compile Remove causes NETSDK1022 duplicate items

## 2026-02-12 manual [pitfall]
Package validation suppression uses ApiCompatSuppressionFile with generated CompatibilitySuppressions.xml, not a PackageValidationSuppression MSBuild item

## 2026-02-12 manual [pitfall]
dotnet publish --no-actual-publish is not a valid CLI switch; use 'dotnet build /p:EnableTrimAnalyzer=true /p:EnableAotAnalyzer=true' to run trim/AOT analysis without publishing

## 2026-02-12 manual [pitfall]
MVC controller [controller] route token resolves to class name -- versioned controllers like ProductsV2Controller produce /ProductsV2 not /products. Use explicit route segments for versioned controllers.

## 2026-02-13 manual [pitfall]
Microsoft.AspNetCore.OpenApi is a NuGet package included in default project templates, not part of the ASP.NET Core shared framework -- it requires an explicit PackageReference with version matching the target framework major

## 2026-02-13 manual [pitfall]
File magic-byte validation must use exact full signatures (PNG=8 bytes starting 0x89, WebP=RIFF+WEBP at offset 8) and handle files shorter than the header size without throwing

## 2026-02-13 manual [pitfall]
[GeneratedRegex] improves performance and AOT compat but does NOT eliminate catastrophic backtracking -- always combine with RegexOptions.NonBacktracking or a matchTimeout for ReDoS safety

## 2026-02-13 manual [pitfall]
Soft cross-refs (skills that may not exist yet) must be explicitly excluded from validation commands — don't mix them with hard cross-refs in acceptance checks or CI will fail

## 2026-02-13 manual [pitfall]
Agent Gotchas section must be internally consistent with the skill body -- if guidance is nuanced (e.g., cookie auth valid for same-origin), gotchas must not use absolute prohibitions that contradict it

## 2026-02-13 manual [pitfall]
MCP tool documentation must use fully qualified tool IDs (mcp__server__tool_name) in all actionable examples -- unprefixed shorthand causes call failures when agents invoke tools literally

## 2026-02-13 manual [pitfall]
WASM AOT and trimming have opposite size effects: trimming reduces download size, AOT increases artifact size (but improves runtime speed) -- do not conflate them as both reducing payload

## 2026-02-13 manual [pitfall]
Never hardcode secrets in CLI examples — always use env-var placeholders with a comment about CI secret storage

## 2026-02-13 manual [pitfall]
Native AOT trimming preservation uses ILLink descriptors (TrimmerRootDescriptor) and [DynamicDependency] attributes, NOT RD.xml (which is a legacy .NET Native/UWP format) -- using the wrong format produces files that are silently ignored

## 2026-02-13 manual [pitfall]
Hot Reload support for new methods improved in .NET 9+: instance methods on non-generic classes work partially, only static/generic require rebuild

## 2026-02-14 manual [pitfall]
Task JSON depends_on must mirror prose serial-execution claims — empty depends_on silently allows parallel execution by task runners

## 2026-02-14 manual [pitfall]
When fixing task specs, always sync the epic spec's Task Decomposition subsections to match -- reviewers flag cross-section inconsistency within the same epic spec file

## 2026-02-14 manual [pitfall]
WPF Fluent theme (.NET 9+) uses Application.ThemeMode property, not a ResourceDictionary merge -- the pack://application URI approach is incorrect and generates non-functional code

## 2026-02-14 manual [pitfall]
WinUI 3 does not expose a managed TaskbarManager API -- taskbar progress requires Win32 COM interop (ITaskbarList3 via CsWin32 or P/Invoke), unlike UWP which had Windows.UI.Shell.TaskbarManager

## 2026-02-14 manual [pitfall]
When a task spec says 'sole owner of file X modifications', the file MUST appear in the commit's changed files list even if no structural changes are needed -- touch it with description/documentation updates to evidence the verification was performed

## 2026-02-14 manual [pitfall]
When scope lists sub-features (e.g. lazy loading, Brotli), each must appear in a dedicated AC item or be explicitly included in an existing AC — implicit coverage via umbrella phrases gets flagged by reviewers

## 2026-02-14 manual [pitfall]
Code examples must not contradict their own Agent Gotchas section -- if a gotcha says 'do not hardcode X', the example must not hardcode X (e.g. TFM paths in CI workflows)

## 2026-02-14 manual [pitfall]
When skills have Agent Gotchas about shell practices (set -euo pipefail), all code examples in the same skill must demonstrate that practice -- reviewers flag self-contradictions

## 2026-02-14 manual [pitfall]
Empty task specs (all TBD) are unshippable - must include descriptions, file paths, acceptance criteria, and validation commands before review

## 2026-02-14 manual [pitfall]
Vague task titles (like 'Reference dotnet-skills material') need clarification - rename to explicit deliverables or risk implementer confusion

## 2026-02-14 manual [pitfall]
WAP projects (.wapproj) use a specialized project format with custom MSBuild imports, not Microsoft.NET.Sdk -- do not show them as SDK-style projects or agents will generate invalid project files

## 2026-02-14 manual [pitfall]
Windows SDK tool paths (signtool.exe, MakeAppx.exe) vary by installed SDK version -- use dynamic path discovery (Get-ChildItem with version sort) instead of hardcoding version-specific paths

## 2026-02-14 manual [pitfall]
After marking a task complete via flowctl, on-disk JSON files (task status, epic next_task, checkpoint) may not be fully synced -- always verify and manually update task JSON status, epic next_task advancement, and regenerate checkpoint with fresh spec content

## 2026-02-14 manual [pitfall]
Task JSON title and task markdown heading must match -- reviewers flag metadata/content title mismatches

## 2026-02-14 manual [pitfall]
Checkpoints embed epic spec verbatim -- regenerate checkpoint after spec updates or reviewers flag stale embedded specs

## 2026-02-14 manual [pitfall]
When building line-removal filters, regex-based whole-line deletion leaves orphaned markdown table headers (header+separator with no data rows) -- add a cleanup pass to strip empty table structures

## 2026-02-14 manual [pitfall]
Roslyn RegisterSymbolAction/RegisterSyntaxNodeAction have no state-passing overload -- do not fabricate two-parameter (context, state) callback signatures; use a closure inside RegisterCompilationStartAction instead

## 2026-02-14 manual [pitfall]
dotnet nuget inspect is not a valid CLI subcommand -- nupkg files are zip archives; use 'unzip -l' or NuGet Package Explorer for package content inspection

## 2026-02-15 manual [pitfall]
When grepping for Agent Gotchas sections, also check variant headings like 'Gotchas and Pitfalls' -- grep for 'Gotcha' not 'Agent Gotcha' to avoid false negatives on non-standard heading names

## 2026-02-15 manual [pitfall]
When counting Agent Gotchas items, grep for numbered list items (^\d+\.) or bold-prefixed bullets -- do not estimate from section-level regex that only captures top-level items; nested content inflates directive counts while deflating item counts

## 2026-02-15 manual [pitfall]
Per rubric, Clean requires ALL 11 dimensions at pass -- any warn dimension makes the skill Needs Work, not Clean. Verify rubric scoring rules before assigning overall ratings.

## 2026-02-15 manual [pitfall]
Stale 'not yet landed' or 'planned' references to skills that have since shipped must be rated same severity across batches -- inconsistent severity for identical patterns causes reviewer churn

## 2026-02-15 manual [pitfall]
Proposed replacement descriptions in audit reports must have character counts verified with the same measurement tool used for existing descriptions -- off-by-one from wc -c vs echo -n piping causes reviewer distrust

## 2026-02-15 manual [pitfall]
When a rubric dimension uses '~N' (approximate threshold), values clearly below the threshold (e.g., 2,226 vs ~3,000) should be rated pass, not warn -- warn is for values actually near the boundary

## 2026-02-15 manual [pitfall]
When counting issues in audit summary tables, reconcile per-skill Issues sections with Recommended Changes sections -- monitoring-only notes and consolidated items can cause count mismatches

## 2026-02-15 manual [pitfall]
When computing aggregate savings from per-item deltas in a consolidation report, verify the per-tier breakdown sums match the individual line items in each priority table -- off-by-one tier misallocations (e.g. an item listed in Low but counted as High) corrupt sub-totals even when the grand total is correct

## 2026-02-15 manual [pitfall]
When planning new skills, always check plugin.json and skills/ tree for existing skills that overlap — enhance existing over creating duplicates

## 2026-02-15 manual [pitfall]
Recursive validation/traversal examples must use IsSimpleType helper covering all common value types (DateTime, DateOnly, Guid, enums, Nullable<T>) and track visited objects to prevent circular reference stack overflow -- naive IsPrimitive+string checks miss most BCL types

## 2026-02-15 manual [pitfall]
When using conditional compilation guards for Roslyn API features, verify the version gate matches the version boundary table -- CollectionExpression is Roslyn 4.8 (VS 17.8), not 4.4 (VS 17.4); cross-check code examples against version tables in the same document

## 2026-02-15 manual [pitfall]
dotnet_analyzer_diagnostic.category-Style.severity is invalid -- 'Style' is not a valid .NET analyzer category; use Design, Documentation, Globalization, Interoperability, Maintainability, Naming, Performance, SingleFile, Reliability, Security, or Usage; IDE rules use per-rule dotnet_diagnostic.IDE*.severity instead

## 2026-02-15 manual [pitfall]
Channel producer examples using fire-and-forget Task.Run must propagate errors via TryComplete(exception) not just TryComplete() in finally -- otherwise consumer blocks forever on silent producer failure

## 2026-02-15 manual [pitfall]
Minimal API endpoints returning IAsyncEnumerable<T> should return the enumerable directly, not wrapped in Results.Ok() -- wrapping may buffer the entire sequence instead of streaming

## 2026-02-15 manual [pitfall]
MSBuild double-import sentinel guards must place content properties inside the \!= 'true' condition block alongside the sentinel -- a separate == 'true' block runs on every import because the sentinel is already set after first evaluation

## 2026-02-15 manual [pitfall]
IIncrementalTask signals that MSBuild engine should pre-filter inputs (passing only changed items) -- the task does NOT do its own timestamp comparison; the engine handles change detection via target-level Inputs/Outputs

## 2026-02-15 manual [pitfall]
ToolTask.GenerateFullPathToTool() must not return null -- return ToolName to let the OS resolve via PATH, or return a full path; null causes NullReferenceException or tool-not-found errors

## 2026-02-15 manual [pitfall]
Mermaid diagram node IDs must be unique across the ENTIRE graph including all subgraphs -- reusing an ID (e.g. BS for both an agent and a skill category) causes nodes to merge silently

## 2026-02-15 manual [pitfall]
When documenting pre-release library APIs, verify every code example against the actual source code on the development branch -- LLM training data mixes v1 and v2 patterns, causing v1 API leaks (removed types, changed constructors, new required parameters) in ostensibly v2-targeted documentation

## 2026-02-15 manual [pitfall]
flowctl epic set-plan may silently fail to write spec file -- always verify with cat/read after set-plan

## 2026-02-15 manual [pitfall]
ApiCompatSuppressionFile is an MSBuild ItemGroup item, not a PropertyGroup property -- using PropertyGroup syntax silently does nothing; use <ItemGroup><ApiCompatSuppressionFile Include="..." /></ItemGroup>

## 2026-02-16 manual [pitfall]
Before adding a new skill, always check existing skills for content overlap — existing dotnet-middleware-patterns covered 100% of proposed dotnet-middleware-authoring content

## 2026-02-16 manual [pitfall]
Azure.Messaging.ServiceBus 7.x uses ServiceBusReceiverOptions with SubQueue.DeadLetter to access DLQ -- do not use EntityNameHelper.FormatDeadLetterPath which belongs to the older Microsoft.Azure.ServiceBus package

## 2026-02-16 manual [pitfall]
OTel Collector tail_sampling processor operates on traces (spans), not logs -- use filter/transform processors for log volume management

## 2026-02-16 manual [pitfall]
Semantic Kernel agent InvokeAsync requires a thread object (ChatHistoryAgentThread or similar) -- do not pass bare strings directly; thread-based invocation is mandatory for all SK agent types

## 2026-02-16 manual [pitfall]
When creating a skill in a new category directory, also add a trigger corpus entry for that category in tests/trigger-corpus.json -- the corpus completeness check requires every category to have at least one routing entry

## 2026-02-16 manual [pitfall]
When updating skill/category counts in prose (README, AGENTS.md, CLAUDE.md), also grep for the same counts inside Mermaid diagram blocks -- diagrams embed counts in node labels that are easy to miss

## 2026-02-17 manual [pitfall]
Path.Join was introduced in .NET Core 2.1, not .NET 8 -- its rooted-path safety behavior is original; only newer Span overloads were added in .NET 6/8

## 2026-02-17 manual [pitfall]
FileOptions.DeleteOnClose behavior differs across platforms -- Windows guarantees OS-level deletion on handle close; Linux/macOS delete during Dispose and may leave orphans on SIGKILL

## 2026-02-17 manual [pitfall]
When plan-syncing task specs from epic changes, always deduplicate — flowctl appends new sections without removing old ones, creating contradictory duplicate Approach/Key Context sections that reviewers flag as Major issues

## 2026-02-17 manual [pitfall]
When splitting destructive operations across tasks (e.g., deleting a file in T1, creating replacement in T2), ensure atomicity — either delete and replace in the same task, or explicitly document that feature-branch workflow makes intermediate breakage acceptable in BOTH the epic AND the task spec

## 2026-02-17 manual [pitfall]
Specification reviews for exploratory features (e.g., community conventions like .agents/openai.yaml) must verify schema authenticity with authoritative sources before task approval; fallback patterns mitigate risk but should be explicitly documented

## 2026-02-17 manual [pitfall]
When computing budget savings for items excluded via disable flags, only count active items in the savings math -- inactive items do not affect the budget even if they share the same pattern being optimized

## 2026-02-17 manual [pitfall]
When counting findings in a severity summary table, ensure the count matches the actual numbered findings in the body -- off-by-one from late additions (e.g. M-9 added after M-1..M-8) is a common reviewer catch

## 2026-02-17 manual [pitfall]
BSD sed on macOS requires sed -i '' (space + empty string) syntax; GNU uses sed -i.bak (no space). Use portable sed > tmpfile && mv tmpfile pattern instead of sed -i in cross-platform scripts

## 2026-02-19 manual [pitfall]
Parallel tasks sharing a created file must have explicit sole-owner assignment; the other task imports only. Otherwise merge conflicts are guaranteed.

## 2026-02-19 manual [pitfall]
When ownership manifests repartition work across tasks, update ALL downstream task specs (titles, descriptions, category lists, filenames) to match -- not just the ones flagged in the first review round

## 2026-02-19 manual [pitfall]
Style guide docs that describe future validator behavior must clearly separate 'current behavior' from 'canonical policy' with distinct subsections -- mixing them causes repeated reviewer churn even after adding qualifying notes

## 2026-02-19 manual [pitfall]
When validating artifacts with both a user-facing name field and a filesystem-canonical ID (directory name, file stem), always use the canonical ID for graph operations (self-ref detection, cycle graphs, cross-ref resolution) -- frontmatter names may diverge from canonical IDs

## 2026-02-19 manual [pitfall]
JSON config parsers must validate root type (list vs dict) before calling .get() or iterating -- wrong root type causes AttributeError that bypasses intended exit-code handling

## 2026-02-19 manual [pitfall]
When loading JSON config files, always validate field types (isinstance checks) and fail loudly (exit 2) on schema violations — truthy checks alone miss non-string types and whitespace-only strings

## 2026-02-19 manual [pitfall]
Style guide 'Action + Domain + Differentiator' formula requires a verb-led description (present-tense verb or participle first) -- noun-phrase leads violate the formula even if they contain domain keywords

## 2026-02-19 manual [pitfall]
When adding pre-processing logic to a shared utility function's call site, centralize it in the utility itself so all callers benefit and logic does not drift between scan paths

## 2026-02-19 manual [pitfall]
When generating migration/audit reports with automated scripts, cross-check summary tables against per-item detail tables for internal consistency -- regex-based token counts may not match validator allowlist-based counts, causing contradictions reviewers flag

## 2026-02-19 manual [pitfall]
Shell boolean env vars using -n (non-empty) test treat '0' as truthy -- use explicit '= "1"' check when docs promise '0' means disabled

## 2026-02-19 manual [pitfall]
GHA steps with 'script | tee file' followed by output-parsing commands lose the script exit code -- capture it before parsing and exit with it at the end

## 2026-02-20 manual [pitfall]
dotnet-script and dotnet run --file are different invocations; this repo uses file-based apps via dotnet run --file, not dotnet-script

## 2026-02-20 manual [pitfall]
GITHUB_BASE_REF is empty for workflow_dispatch and schedule triggers — only populated for pull_request events. Baseline comparison designs must account for the actual workflow trigger types.

## 2026-02-20 manual [pitfall]
When running CLI tools via /bin/bash -lc, exit code 127 (command not found) and 126 (permission denied) indicate the binary is missing/non-executable -- the process still 'starts' (bash starts) so Started=true; detect these via exit code + stderr patterns to avoid misclassifying transport failures as assertion failures

## 2026-02-20 manual [pitfall]
When normalizing path separators for matching, apply the same normalization at EVERY code path that touches the same tokens -- partial normalization (e.g. in scoring but not in presence checks) creates false negatives on the un-normalized paths

## 2026-02-20 manual [pitfall]
When a new function is designated 'single source of truth' for a classification, all upstream presence/filtering checks must delegate to it or use its same regexes -- parallel brittle checks with different tolerance (e.g. whitespace) create disagreement

## 2026-02-20 manual [pitfall]
When a 'diagnostics-only' mode suppresses a pass promotion, do not merge the diagnostic source's MatchedAll/MissingAll into the gating source -- only merge observability data (proof lines, TokenHits, log file) to avoid contradictory success+fail state

## 2026-02-20 manual [pitfall]
When a policy (e.g. tier cap) must constrain how data is gated, apply the constraint DURING evaluation (before the pass/fail decision), not AFTER -- post-hoc patching of metadata without recomputing the gating decision leaves the original decision unchanged

## 2026-02-20 manual [pitfall]
When merging evidence from multiple sources (CLI + logs), a full Merge that unions MatchedAll can eliminate MissingAll tokens from one source even when the other source also failed -- in fail+fail paths, merge only diagnostic fields and keep the primary source's gating decision

## 2026-02-20 manual [pitfall]
When adding a new classification category (e.g. optional_only), ensure the detection condition is actually reachable -- walk through the control flow to verify the branch can be entered, and add a self-test that exercises it

## 2026-02-20 manual [pitfall]
When iterating a matrix of (case, provider) in CI summarize jobs, a missing result row for a specific tuple must be a hard failure -- silently skipping with 'continue' produces misleading OK rows and bypasses baseline completeness checks

## 2026-02-20 manual [pitfall]
When a validation rule checks 'at least one item has property X', do not guard it behind 'if count >= 1' -- any() on an empty sequence correctly returns False (vacuous failure), and the guard silently suppresses the warning for the empty case

## 2026-02-20 manual [pitfall]
Negative control test cases (disallowed/optional skills) must use temptation prompts that naturally overlap with the disallowed/optional skill domain -- prompts that avoid the domain will never trigger the skill, making the test case untestable

## 2026-02-21 manual [pitfall]
When scanning raw frontmatter lines for key patterns, only check column-0 (non-indented) lines -- indented lines may be block scalar content and produce false positives on key-like patterns

## 2026-02-21 manual [pitfall]
When documenting behaviors observed in upstream issue trackers (not locally measured), use qualified language like 'upstream reports suggest' and 'implementation-defined' rather than 'verified' or definitive claims -- reviewers flag overclaimed verification

## 2026-02-21 manual [pitfall]
When updating required-fields lists in one doc, grep ALL docs for the same field list pattern and update them all atomically -- partial updates create contributor-facing inconsistencies that reviewers catch across rounds

## 2026-02-21 manual [pitfall]
When spec says 'verify X behavior' and the tool IS available locally, run the actual test and capture output as evidence — reviewers will block on 'deferred to later' if the tool is present

## 2026-02-21 manual [pitfall]
When a CI comparison script silently degrades on missing data (e.g. ref baseline not found), it can bypass the regression gate entirely -- always hard-fail on missing inputs that would disable the gate

## 2026-02-21 manual [pitfall]
In GitHub Actions steps with 'set -euo pipefail', capturing exit codes (cmd; EXIT=$?) is dead code -- the shell exits on non-zero before the assignment. Use 'set +e' before the command, then 'set -e' after capturing the exit code.

## 2026-02-21 manual [pitfall]
GitHub Actions expressions like github.event.pull_request.head.repo.fork are undefined on push events (not just null). Jobs referencing PR-only context must guard with 'if: github.event_name == pull_request' or use null-safe expressions.

## 2026-02-21 manual [pitfall]
Heredocs inside GitHub Actions YAML 'run:' blocks break YAML parsing when the delimiter (e.g. PY, EOF) appears at column 1. Use single-line python -c commands or write to a temp script file instead.

## 2026-02-23 manual [pitfall]
Regex-based JSON extraction from LLM responses fails on nested objects and braces inside strings; use json.JSONDecoder.raw_decode() scanning instead

## 2026-02-23 manual [pitfall]
Generation cache keys must include ALL inputs that affect output (model, temperature, prompt content hash) -- not just the semantic identifier -- to prevent silent stale reuse when parameters change

## 2026-02-23 manual [pitfall]
When a runner emits summary dicts consumed by a comparator, keep comparator-facing entries to a single well-known key (e.g. _overall) and put per-entity breakdowns in artifacts -- comparators iterate all summary keys as entity IDs

## 2026-02-23 manual [pitfall]
When multiple code paths conditionally assign a variable (e.g. fallback_cost inside an if/else), initialize the variable BEFORE the branch to prevent UnboundLocalError on the paths that skip assignment
