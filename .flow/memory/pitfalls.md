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
