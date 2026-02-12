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
