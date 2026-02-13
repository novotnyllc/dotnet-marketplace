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
