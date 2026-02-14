# fn-18: Performance and Benchmarking Skills

## Overview
Delivers comprehensive performance and benchmarking skills covering BenchmarkDotNet, performance-oriented architecture patterns, profiling tools, and continuous benchmarking in CI. Enables dotnet-performance-analyst and dotnet-benchmark-designer agents for specialized performance work.

## Scope
**Skills (4 total):**
- `dotnet-benchmarkdotnet` — BenchmarkDotNet setup, custom configs, memory diagnosers, exporters, baselines, CI integration
- `dotnet-performance-patterns` — Performance-focused architecture: Span<T>, Memory<T>, ArrayPool, zero-alloc patterns, struct design (readonly struct, ref struct, in parameters), sealed class performance rationale
- `dotnet-profiling` — Diagnostic tools: dotnet-counters, dotnet-trace, dotnet-dump, memory profiling, allocation analysis, flame graphs
- `dotnet-ci-benchmarking` — Continuous benchmarking: baseline comparison, regression detection, alerting, GitHub Actions integration

**Agents (2 total):**
- `dotnet-performance-analyst` — Analyzes profiling results and benchmark comparisons, suggests optimizations
- `dotnet-benchmark-designer` — Designs effective benchmarks, avoids common pitfalls (dead code elimination, measurement bias)

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills.

## Scope Boundaries

| Concern | fn-18 owns (performance) | Other epic owns (related) | Enforcement |
|---|---|---|---|
| Language syntax | Performance context for Span/Memory/sealed | fn-3: syntax examples in `dotnet-csharp-modern-patterns` and `dotnet-csharp-coding-standards` | Cross-reference fn-3 skills; don't re-teach syntax |
| Caching architecture | How to benchmark caching | fn-5: `dotnet-architecture-patterns` covers HybridCache setup | Cross-reference `[skill:dotnet-architecture-patterns]` for caching strategy |
| Serialization benchmarks | How to benchmark serialization | fn-6: `dotnet-serialization` provides perf guidance | Cross-reference `[skill:dotnet-serialization]`; show benchmark setup, not serialization APIs |
| AOT performance | AOT-specific perf characteristics | fn-16: `dotnet-native-aot`, `dotnet-aot-architecture` | Cross-reference for AOT compilation; focus on measuring AOT impact |
| EF Core query perf | Benchmarking queries | fn-5: `dotnet-efcore-patterns` has tactical query optimization | Cross-reference for query patterns; show benchmark setup |
| CI/CD workflows | Benchmark automation workflows | fn-19: composable workflows, matrix builds | Cross-reference fn-19 when it lands; fn-18 focuses on benchmark integration points |
| Observability metrics | Interpreting GC/threadpool metrics | fn-5: `dotnet-observability` covers OpenTelemetry setup | Cross-reference for metrics collection; focus on profiling analysis |

## Task Decomposition

### fn-18.1: Performance skills (BenchmarkDotNet and patterns) — parallelizable
**Delivers:** `dotnet-benchmarkdotnet`, `dotnet-performance-patterns`
- `skills/performance/dotnet-benchmarkdotnet/SKILL.md`
- `skills/performance/dotnet-performance-patterns/SKILL.md`
- Both require `name` and `description` frontmatter
- Cross-references fn-3 (`dotnet-csharp-modern-patterns`, `dotnet-csharp-coding-standards`) for syntax foundation
- Cross-references fn-16 (`dotnet-native-aot`) for AOT performance characteristics
- Does NOT touch `plugin.json` (handled by fn-18.4)

### fn-18.2: Profiling and CI benchmarking skills — parallelizable
**Delivers:** `dotnet-profiling`, `dotnet-ci-benchmarking`
- `skills/performance/dotnet-profiling/SKILL.md`
- `skills/performance/dotnet-ci-benchmarking/SKILL.md`
- Cross-references fn-5 (`dotnet-observability`) for metrics correlation
- `dotnet-ci-benchmarking` includes placeholder comments for fn-19 CI/CD workflow cross-refs (deferred)
- Does NOT touch `plugin.json` (handled by fn-18.4)

### fn-18.3: Performance agents — parallelizable
**Delivers:** `dotnet-performance-analyst`, `dotnet-benchmark-designer`
- `agents/dotnet-performance-analyst.md`
- `agents/dotnet-benchmark-designer.md`
- **dotnet-performance-analyst**: Persona is a performance engineer analyzing profiling data (dotnet-trace, dotnet-dump output), interpreting benchmark comparisons, identifying bottlenecks. Loads `[skill:dotnet-profiling]`, `[skill:dotnet-benchmarkdotnet]`, `[skill:dotnet-observability]`.
- **dotnet-benchmark-designer**: Persona is a benchmarking specialist designing effective benchmarks, avoiding dead code elimination, choosing correct memory diagnosers. Loads `[skill:dotnet-benchmarkdotnet]`, `[skill:dotnet-performance-patterns]`.
- Agents must have frontmatter compatible with existing agents (see `agents/dotnet-architect.md` for reference)
- Does NOT touch `plugin.json` (handled by fn-18.4)

### fn-18.4: Integration — plugin registration, advisor catalog update, validation (depends on fn-18.1, fn-18.2, fn-18.3)
**Delivers:** Plugin registration and validation for all 4 skills + 2 agents
- Registers all 4 skill paths in `.claude-plugin/plugin.json` under `skills` array
- Registers both agent paths in `.claude-plugin/plugin.json` under `agents` array
- Updates `skills/foundation/dotnet-advisor/SKILL.md` section 9 (Performance & Benchmarking) from `planned` to implemented with live cross-refs
- Runs repo-wide skill name uniqueness check (validates against existing `skills/*/*/SKILL.md`)
- Runs `./scripts/validate-skills.sh`
- Validates cross-references are present:
  - fn-3 skills (modern patterns, coding standards)
  - fn-5 skills (observability, architecture, EF Core)
  - fn-6 skills (serialization)
  - fn-16 skills (native AOT)
- Validates deferred fn-19 placeholder comments exist in `dotnet-ci-benchmarking`
- Single owner of `plugin.json` — eliminates merge conflicts

**fn-19 Reconciliation:** When fn-19 lands, a follow-up task must replace deferred placeholder comments in `dotnet-ci-benchmarking` with canonical `[skill:...]` cross-references for CI/CD workflows and validate via grep.

## Key Context
- **BenchmarkDotNet v0.14+** is the .NET industry standard for microbenchmarking
- **Diagnostic tools** (`dotnet-counters`, `dotnet-trace`, `dotnet-dump`) are built into .NET SDK 6.0+ — no separate install
- **Performance patterns** extend (not duplicate) fn-3's `dotnet-csharp-modern-patterns` and `dotnet-csharp-coding-standards` with performance-focused rationale
- **CI benchmarking** prevents regressions by comparing against baselines (BenchmarkDotNet.Exporters for JSON output, GitHub Actions artifacts)
- **Profiling analysis** focuses on interpreting data (flame graphs, allocation tracking) — collection covered by fn-5 observability
- Existing dotnet-skills plugin has `csharp-type-design-performance` — fn-18 skills will supersede this with canonical `dotnet-performance-patterns`

## Quick Commands
```bash
# Validate all 4 skills exist with frontmatter
for s in dotnet-benchmarkdotnet dotnet-performance-patterns dotnet-profiling dotnet-ci-benchmarking; do
  test -f "skills/performance/$s/SKILL.md" && \
  grep -q "^name:" "skills/performance/$s/SKILL.md" && \
  grep -q "^description:" "skills/performance/$s/SKILL.md" && \
  echo "OK: $s" || echo "MISSING: $s"
done

# Validate agents exist
for a in dotnet-performance-analyst dotnet-benchmark-designer; do
  test -f "agents/$a.md" && echo "OK: $a" || echo "MISSING: $a"
done

# Repo-wide skill name uniqueness check
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Validate cross-references to fn-3 (coding patterns foundation)
grep -r "\[skill:dotnet-csharp-modern-patterns\]" skills/performance/
grep -r "\[skill:dotnet-csharp-coding-standards\]" skills/performance/

# Validate cross-references to fn-5 (architecture foundation)
grep -r "\[skill:dotnet-observability\]" skills/performance/
grep -r "\[skill:dotnet-architecture-patterns\]" skills/performance/
grep -r "\[skill:dotnet-efcore-patterns\]" skills/performance/

# Validate cross-references to fn-6 (serialization)
grep -r "\[skill:dotnet-serialization\]" skills/performance/

# Validate cross-references to fn-16 (AOT)
grep -r "\[skill:dotnet-native-aot\]" skills/performance/

# Validate deferred fn-19 placeholders
grep -l "TODO.*fn-19\|placeholder.*fn-19\|deferred.*fn-19" skills/performance/dotnet-ci-benchmarking/SKILL.md

# Validate advisor catalog updated
grep -A 10 "### 9. Performance & Benchmarking" skills/foundation/dotnet-advisor/SKILL.md | grep -v "planned"

# Canonical validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 4 skills exist at `skills/performance/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. BenchmarkDotNet skill covers [Benchmark] attributes, memory diagnosers, exporters (JSON/HTML), baselines, and CI integration with artifact upload
3. Performance patterns skill covers Span<T>/Memory<T>/ArrayPool usage, readonly struct/ref struct design, in parameters, sealed class performance rationale (JIT devirtualization), and zero-allocation patterns
4. Profiling skill covers dotnet-counters (real-time metrics), dotnet-trace (flame graphs, CPU sampling), dotnet-dump (memory heap analysis, SOS commands), and allocation tracking
5. CI benchmarking skill covers baseline comparison workflows, regression detection (threshold-based), alerting on perf degradation, and GitHub Actions integration with artifacts
6. Both agents exist at `agents/<agent-name>.md` with appropriate frontmatter and persona definitions
7. Performance analyst agent loads profiling, benchmarking, and observability skills; focuses on analyzing data and suggesting optimizations
8. Benchmark designer agent loads benchmarking and performance pattern skills; focuses on designing valid benchmarks and avoiding pitfalls
9. Skills cross-reference fn-3 skills (`dotnet-csharp-modern-patterns`, `dotnet-csharp-coding-standards`) for syntax foundation — not re-teaching
10. Skills cross-reference fn-5 skills (`dotnet-observability`, `dotnet-architecture-patterns`, `dotnet-efcore-patterns`) where applicable
11. Skills cross-reference fn-6 (`dotnet-serialization`) for serialization benchmark examples
12. Skills cross-reference fn-16 (`dotnet-native-aot`) for AOT performance characteristics
13. `dotnet-ci-benchmarking` includes deferred placeholder comments for fn-19 CI/CD workflow cross-refs (non-blocking)
14. All 4 skills and 2 agents registered in `.claude-plugin/plugin.json`
15. `skills/foundation/dotnet-advisor/SKILL.md` section 9 updated from `planned` to implemented
16. `./scripts/validate-skills.sh` passes for all 4 skills
17. Skill `name` frontmatter values are unique repo-wide (no duplicates across all `skills/*/*/SKILL.md`)
18. Tasks fn-18.1, fn-18.2, fn-18.3 are fully parallelizable (file-disjoint, no shared file edits)
19. Task fn-18.4 (integration) depends on fn-18.1, fn-18.2, fn-18.3 and is the single owner of `plugin.json`

## Test Notes
- Verify BenchmarkDotNet skill includes memory diagnoser setup and interpretation guidance
- Verify performance patterns skill adds **why** (perf rationale) beyond fn-3's **how** (syntax)
- Verify profiling skill focuses on analysis (reading flame graphs, heap dumps) not just tool invocation
- Verify CI benchmarking skill includes actual GitHub Actions YAML snippets for artifact upload
- Verify agents have distinct personas and don't duplicate each other's scope
- Verify advisor catalog update includes all 4 skill cross-refs
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide

## References
- [BenchmarkDotNet Documentation](https://benchmarkdotnet.org/)
- [.NET Diagnostic Tools](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/)
- [Performance Best Practices for .NET](https://learn.microsoft.com/en-us/dotnet/framework/performance/)
- [Writing High-Performance .NET Code (book)](https://www.writinghighperf.net/)
- [dotnet-trace flame graphs](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace)
- [System.Diagnostics.Metrics](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/metrics)
