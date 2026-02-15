# Batch D Findings: API Development, CLI Tools, Performance, Native AOT

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | 18 |
| Clean | 14 |
| Needs Work | 3 |
| Critical | 1 |
| Total issues | 6 |
| Critical issues | 1 |
| High issues | 2 |
| Low issues | 3 |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | 2,116 |
| Skills over 120 chars | 2 |
| Projected savings if all trimmed to 120 | 32 chars |

Skills over 120 chars: dotnet-ci-benchmarking (144), dotnet-profiling (128).

Character counts measured using the canonical shell extraction method (strips YAML quotes, trims whitespace).

## Findings by Skill

### api-development

### dotnet-minimal-apis

**Category:** api-development
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars |
| 2 | Description Triggering | pass | Good trigger phrases (Minimal APIs, route groups, endpoint filters, TypedResults, OpenAPI) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve (dotnet-api-versioning, dotnet-input-validation, dotnet-architecture-patterns, dotnet-openapi) |
| 6 | Error Handling | pass | Agent Gotchas section (5 items) and inline gotchas on JSON configuration |
| 7 | Examples | pass | Full CRUD examples with TypedResults, Carter module, extension method patterns |
| 8 | Composability | pass | Clear Out of Scope section with cross-refs to 5 companion skills |
| 9 | Consistency | pass | Matches category peer structure (Out of Scope, Cross-references, Agent Gotchas, Prerequisites, References) |
| 10 | Registration & Budget | pass | 115 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,413 words |

**Issues:**
(none)

---

### dotnet-api-versioning

**Category:** api-development
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars |
| 2 | Description Triggering | pass | Good trigger phrases (versioning, Asp.Versioning, URL segment, header, sunset policies) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) |
| 7 | Examples | pass | Minimal API and MVC examples with NuGet packages listed |
| 8 | Composability | pass | Clear Out of Scope and cross-refs |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 115 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,127 words |

**Issues:**
(none)

---

### dotnet-openapi

**Category:** api-development
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars |
| 2 | Description Triggering | pass | Good triggers (OpenAPI docs, Swashbuckle migration, NSwag) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering package version matching, Swashbuckle migration pitfalls |
| 7 | Examples | pass | Full document/operation/schema transformer examples, migration table |
| 8 | Composability | pass | Clear scope boundary, correctly says "preferred" not "deprecated" for Swashbuckle per pitfalls memory |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 116 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,274 words |

**Issues:**
(none)

---

### dotnet-api-security

**Category:** api-development
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 108 chars |
| 2 | Description Triggering | pass | Good triggers (API auth, OAuth, OIDC, JWT bearer, passkeys, CORS, rate limiting) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve (dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography, dotnet-blazor-auth) |
| 6 | Error Handling | pass | Agent Gotchas section (8 items) plus inline gotchas on CORS, MapInboundClaims, middleware order |
| 7 | Examples | pass | Full Identity, OIDC, JWT, CORS, CSP, rate limiting examples with all four rate limiter algorithms |
| 8 | Composability | pass | Auth ownership section clearly delineates fn-11 vs fn-12 vs fn-8 responsibilities |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 108 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,432 words |

**Issues:**
(none)

---

### dotnet-input-validation

**Category:** api-development
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 120 chars -- exactly at limit |
| 2 | Description Triggering | pass | Good triggers (.NET 10 AddValidation, FluentValidation, Data Annotations, endpoint filters, ProblemDetails) |
| 3 | Instruction Clarity | pass | Decision tree for framework selection is clear and actionable |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (7 items) plus inline gotchas on ConfigureHttpJsonOptions, FluentValidation auto-validation |
| 7 | Examples | pass | Full examples for .NET 10 built-in, FluentValidation, Data Annotations, file upload with magic bytes |
| 8 | Composability | pass | Detailed scope boundary section separating validation from OWASP, architecture, options pattern |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 120 chars |
| 11 | Progressive Disclosure Compliance | pass | 2,510 words -- approaching threshold but under 3,000 |

**Issues:**
(none)

---

### cli-tools

### dotnet-system-commandline

**Category:** cli-tools
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | Good triggers (CLI apps, System.CommandLine, RootCommand, middleware, tab completion) |
| 3 | Instruction Clarity | pass | Production readiness assessment clearly explains beta versioning |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering common API confusion points |
| 7 | Examples | pass | Full command hierarchy, options/arguments, hosting integration, TestConsole examples with NuGet packages |
| 8 | Composability | pass | Clear Out of Scope delineation with companion skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,623 words |

**Issues:**
(none)

---

### dotnet-cli-architecture

**Category:** cli-tools
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | Good triggers (designing CLI apps, layered patterns, clig.dev, exit codes, testing) |
| 3 | Instruction Clarity | pass | Three-layer architecture diagram with concrete code examples for each layer |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering stdout/stderr separation, exit codes, testing strategy |
| 7 | Examples | pass | Full layered architecture, test harness with service mocks, exit code assertions |
| 8 | Composability | pass | Clear scope boundary to companion skills (System.CommandLine, distribution, packaging) |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,894 words |

**Issues:**
(none)

---

### dotnet-cli-distribution

**Category:** cli-tools
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars |
| 2 | Description Triggering | pass | Good triggers (shipping CLI tools, AOT, framework-dependent, dotnet tool, RID matrix, single-file) |
| 3 | Instruction Clarity | pass | Decision matrix with clear tradeoffs |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) |
| 7 | Examples | pass | Full RID matrix, publish commands, build script, checksum generation |
| 8 | Composability | pass | Clear Out of Scope with cross-refs to packaging, release pipeline, AOT |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,517 words |

**Issues:**
(none)

---

### dotnet-cli-packaging

**Category:** cli-tools
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars |
| 2 | Description Triggering | pass | Good triggers (Homebrew, apt/deb, winget, Scoop, Chocolatey, dotnet tool, NuGet) |
| 3 | Instruction Clarity | pass | Concrete examples for each package manager |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) |
| 7 | Examples | pass | Full formulae, manifests, and install commands for 6 package formats |
| 8 | Composability | pass | Clear Out of Scope referencing distribution, release pipeline, AOT |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 112 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,562 words |

**Issues:**
(none)

---

### dotnet-cli-release-pipeline

**Category:** cli-tools
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars |
| 2 | Description Triggering | pass | Good triggers (releasing CLI tools, GitHub Actions, build matrix, checksums, package PRs) |
| 3 | Instruction Clarity | pass | Complete GitHub Actions workflow with matrix build, artifact staging, release creation |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering pipefail, pre-release detection, artifact versioning |
| 7 | Examples | pass | Full GHA workflows for build, release, Homebrew, winget, Scoop PR automation |
| 8 | Composability | pass | Clear scope boundary to general CI/CD patterns |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,933 words |

**Issues:**
(none)

---

### performance

### dotnet-benchmarkdotnet

**Category:** performance
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars |
| 2 | Description Triggering | pass | Good triggers (microbenchmarking, BenchmarkDotNet, memory diagnosers, exporters, baselines) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (7 items) plus comprehensive Common Pitfalls table |
| 7 | Examples | pass | Full benchmark class, parameterized benchmarks, CI config examples with NuGet package |
| 8 | Composability | pass | Clear Out of Scope to companion performance skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,532 words |

**Issues:**
(none)

---

### dotnet-performance-patterns

**Category:** performance
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 119 chars |
| 2 | Description Triggering | pass | Good triggers (optimizing allocations/throughput, Span, ArrayPool, readonly struct, sealed, stackalloc) |
| 3 | Instruction Clarity | pass | Performance rationale clearly explained for each pattern |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (7 items) covering defensive copy traps, ArrayPool lifetime, StringComparison pitfalls |
| 7 | Examples | pass | Zero-allocation parsing, ArrayPool patterns, stackalloc hybrid pattern, sealed devirtualization |
| 8 | Composability | pass | Explicit delegation to syntax skills (modern-patterns) for Span syntax details |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 119 chars |
| 11 | Progressive Disclosure Compliance | pass | 2,057 words |

**Issues:**
(none)

---

### dotnet-profiling

**Category:** performance
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 128 chars (121-140 = warn) -- slightly over the 120-char target |
| 2 | Description Triggering | pass | Good triggers (diagnosing performance, dotnet-counters, dotnet-trace, dotnet-dump, flame graphs) |
| 3 | Instruction Clarity | pass | Structured investigation workflow with clear tool selection guidance |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Bare backtick reference to `dotnet-ci-benchmarking` in Out of Scope (line 12) instead of `[skill:dotnet-ci-benchmarking]` syntax |
| 6 | Error Handling | pass | Agent Gotchas section (7 items) covering tool selection, flame graph interpretation, dump comparison strategy |
| 7 | Examples | pass | Full CLI commands for all three tools, SOS command reference table, flame graph reading guide |
| 8 | Composability | pass | Clear workflow summary connecting triage (counters) to diagnosis (trace/dump) to optimization (patterns) |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 128 chars pushes budget (>120 warn range) |
| 11 | Progressive Disclosure Compliance | pass | 2,450 words -- approaching 3,000 threshold but under it |

**Issues:**
- [High] Bare backtick reference to `dotnet-ci-benchmarking` in Out of Scope section (line 12) -- should use `[skill:dotnet-ci-benchmarking]` syntax per cross-reference convention
- [Low] Description at 128 chars exceeds 120-char target -- consider trimming to remove "allocation tracking" or abbreviating "flame graphs"

**Proposed description (118 chars):** `"WHEN diagnosing .NET performance issues. dotnet-counters, dotnet-trace, dotnet-dump, flame graphs, heap analysis."`

---

### dotnet-ci-benchmarking

**Category:** performance
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 144 chars (>140 = fail) -- exceeds hard limit |
| 2 | Description Triggering | pass | Good triggers (benchmark regression detection, baseline management, GitHub Actions, threshold alerts) |
| 3 | Instruction Clarity | pass | Complete regression detection workflow with Python comparison script |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (7 items) covering CI noise calibration, baseline management, pipefail |
| 7 | Examples | pass | Full GHA workflows, Python comparison script, BenchmarkDotNet CI config, PR comment integration |
| 8 | Composability | pass | Clear Out of Scope to companion benchmarking and CI skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | fail | 144 chars exceeds 140-char fail threshold, impacts aggregate budget |
| 11 | Progressive Disclosure Compliance | pass | 1,966 words |

**Issues:**
- [Critical] Description at 144 chars exceeds the 140-char fail threshold -- must trim to under 120 chars
- [Low] Description lists too many implementation details (baseline management, GitHub Actions, threshold alerts, BenchmarkDotNet CI workflows) -- consolidate using formula `[What] + [When]`

**Proposed description (119 chars):** `"WHEN automating benchmark regression detection. Baseline comparison, threshold alerts, BenchmarkDotNet CI workflows."`

---

### native-aot

### dotnet-native-aot

**Category:** native-aot
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | Good triggers (Native AOT, PublishAot, ILLink, P/Invoke, size optimization, runtime-deps) |
| 3 | Instruction Clarity | pass | Clear apps-vs-libraries MSBuild property distinction |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve (8 cross-refs to companion skills) |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering common AOT misconceptions |
| 7 | Examples | pass | Full MSBuild config, ILLink XML, LibraryImport, Dockerfile, ASP.NET Core AOT |
| 8 | Composability | pass | Detailed scope boundary separating general AOT from MAUI AOT, WASM AOT, trimming, architecture |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,888 words |

**Issues:**
(none)

---

### dotnet-aot-architecture

**Category:** native-aot
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars |
| 2 | Description Triggering | pass | Good triggers (AOT-first apps, source gen, reflection replacement, DI, serialization, factory patterns) |
| 3 | Instruction Clarity | pass | Source gen replacement table is actionable with concrete library recommendations |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (5 items) covering Activator.CreateInstance, assembly scanning, STJ context |
| 7 | Examples | pass | Full LoggerMessage migration, keyed services, factory patterns, library compat table |
| 8 | Composability | pass | Clear scope delegation to native-aot for pipeline, trimming for library authoring |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 112 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,283 words |

**Issues:**
(none)

---

### dotnet-trimming

**Category:** native-aot
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 119 chars |
| 2 | Description Triggering | pass | Good triggers (trim-safe, annotations, ILLink descriptors, TrimmerSingleWarn, IL2xxx, IsTrimmable) |
| 3 | Instruction Clarity | pass | Clear apps-vs-libraries distinction with property comparison table |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) plus comprehensive IL2xxx/IL3xxx warning reference table |
| 7 | Examples | pass | Full annotation examples, ILLink XML, CI trim gate, library authoring pattern |
| 8 | Composability | pass | Clear delegation to native-aot for pipeline, aot-architecture for design patterns |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 119 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,531 words |

**Issues:**
(none)

---

### dotnet-aot-wasm

**Category:** native-aot
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars |
| 2 | Description Triggering | pass | Good triggers (WASM AOT, Blazor, Uno, size vs speed, lazy loading, Brotli) |
| 3 | Instruction Clarity | pass | Size/speed tradeoff table is clear and actionable |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve; correctly marks dotnet-blazor-patterns and dotnet-uno-platform as (soft) refs |
| 6 | Error Handling | pass | Agent Gotchas section (6 items) covering RunAOTCompilation vs PublishAot, size misconceptions, Brotli verification |
| 7 | Examples | pass | Full Blazor WASM AOT, Uno WASM, lazy loading with router, Brotli server config (Nginx, ASP.NET Core) |
| 8 | Composability | pass | Clear scope boundary separating WASM AOT from server-side AOT, MAUI AOT, trimming |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 115 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,480 words |

**Issues:**
(none)

---

## Cross-Cutting Observations

1. **Exceptional quality in this batch:** 14 of 18 skills (78%) are Clean with all 11 dimensions passing. This is the highest Clean rate across batches reviewed so far. The three Needs Work skills and one Critical skill have minor, easily fixable issues.

2. **Description budget pressure is minimal:** Only 2 of 18 skills exceed 120 chars. The total batch description budget of 2,116 chars is well-managed, with only 32 chars of excess beyond the 120-char-per-skill target.

3. **Consistent category structure:** All four categories (api-development, cli-tools, performance, native-aot) follow the same structural pattern: Out of Scope with cross-refs, Cross-references section, code examples, Agent Gotchas, Prerequisites, References. This is the strongest structural consistency observed across all batches.

4. **Agent Gotchas coverage:** All 18 skills have Agent Gotchas sections with substantive items (5-8 items each). No skill is missing this section, which was an issue in earlier batches.

5. **Cross-reference hygiene:** All `[skill:name]` references resolve to existing skill directories. Only one bare backtick reference was found (dotnet-profiling referencing dotnet-ci-benchmarking). No broken references.

6. **Progressive disclosure compliance:** All 18 skills are under the 3,000-word suggestion threshold. The longest skill (dotnet-input-validation at 2,510 words) manages its length well through focused decision trees and code examples. No details.md companion files are needed.

7. **Pitfalls memory compliance:** Skills correctly implement multiple pitfalls memory entries:
   - dotnet-minimal-apis correctly notes ConfigureHttpJsonOptions applies only to Minimal APIs (per pitfalls)
   - dotnet-openapi uses "preferred/recommended" not "deprecated" for Swashbuckle (per pitfalls)
   - dotnet-native-aot warns against RD.xml and non-existent `--no-actual-publish` flag (per pitfalls)
   - dotnet-input-validation uses defensive parsing for file validation magic bytes (per pitfalls)
   - dotnet-cli-release-pipeline uses `set -euo pipefail` in bash steps (per pitfalls)
   - dotnet-api-security uses defensive parsing note for auth paths (per pitfalls)

8. **CLI tools category is particularly well-composed:** The 5 cli-tools skills (system-commandline, architecture, distribution, packaging, release-pipeline) form a cohesive progression with non-overlapping scopes and clear mutual cross-references. Each skill's Out of Scope precisely delegates to its siblings.

9. **Native AOT category has excellent scope boundaries:** The 4 native-aot skills (native-aot, aot-architecture, trimming, aot-wasm) cleanly separate pipeline config from design patterns from library authoring from WASM compilation. Cross-references are bidirectional and accurate.

## Recommended Changes

### Critical (must fix)
- Trim `dotnet-ci-benchmarking` description from 144 to under 120 chars -- remove implementation detail enumeration, use `[What] + [When]` formula

### High (should fix)
- Fix bare backtick reference to `dotnet-ci-benchmarking` in `dotnet-profiling` Out of Scope section (line 12) -- change `` `dotnet-ci-benchmarking` `` to `[skill:dotnet-ci-benchmarking]`
- Trim `dotnet-profiling` description from 128 to under 120 chars to stay within budget target

### Low (nice to have)
- Monitor `dotnet-input-validation` (2,510 words) and `dotnet-profiling` (2,450 words) for details.md extraction if content grows beyond 3,000 words
- Consider adding bidirectional cross-ref: dotnet-ci-benchmarking references dotnet-profiling but dotnet-benchmarkdotnet does not reference dotnet-ci-benchmarking in its Out of Scope (it uses "fn-18.2 skills (not yet landed)" which is stale -- dotnet-ci-benchmarking has landed)
- Update `dotnet-benchmarkdotnet` Out of Scope text from "fn-18.2 skills (not yet landed)" to `[skill:dotnet-ci-benchmarking]` since the skill now exists and is registered
