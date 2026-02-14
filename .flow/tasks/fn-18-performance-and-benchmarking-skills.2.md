# fn-18-performance-and-benchmarking-skills.2 Profiling and CI benchmarking skills

## Description
Create two diagnostic and automation skills: `dotnet-profiling` for analyzing performance with .NET diagnostic tools and `dotnet-ci-benchmarking` for continuous benchmark regression detection. These skills enable ongoing performance monitoring and investigation.

**Files created:**
- `skills/performance/dotnet-profiling/SKILL.md`
- `skills/performance/dotnet-ci-benchmarking/SKILL.md`

**Cross-references required:**
- `[skill:dotnet-observability]` (fn-5) for OpenTelemetry metrics correlation
- Deferred fn-19 placeholders in `dotnet-ci-benchmarking` for CI/CD workflow cross-refs

Both skills must have `name` and `description` frontmatter. Does NOT touch `plugin.json` (handled by fn-18.4).

## Acceptance
- [ ] `skills/performance/dotnet-profiling/SKILL.md` exists with valid frontmatter (name, description)
- [ ] Profiling skill covers dotnet-counters:
  - Real-time metric monitoring (CPU, memory, GC, threadpool)
  - `dotnet-counters monitor` command syntax
  - Custom EventCounters
- [ ] Profiling skill covers dotnet-trace:
  - Event tracing and flame graph generation
  - CPU sampling vs instrumentation
  - Speedscope/PerfView flame graph analysis
  - Allocation tracking with `--profile gc-collect`
- [ ] Profiling skill covers dotnet-dump:
  - Memory dump capture and analysis
  - SOS commands (!dumpheap, !gcroot, !finalizequeue)
  - Heap dump analysis for memory leaks
- [ ] Profiling skill cross-references `[skill:dotnet-observability]` for GC/threadpool metrics interpretation
- [ ] `skills/performance/dotnet-ci-benchmarking/SKILL.md` exists with valid frontmatter
- [ ] CI benchmarking skill covers:
  - Baseline file management (BenchmarkDotNet.Exporters.Json)
  - GitHub Actions artifact upload/download for baseline comparison
  - Regression detection patterns (threshold-based alerts)
  - YAML snippets for benchmark workflow integration
- [ ] CI benchmarking skill includes placeholder comments for fn-19 cross-refs (format: `<!-- TODO(fn-19): Add [skill:dotnet-github-actions] cross-ref when fn-19 lands -->`)
- [ ] Both skills include "Out of scope" sections with fn-5/fn-19 boundary statements
- [ ] Validation: `grep -q "^name:" skills/performance/dotnet-profiling/SKILL.md`
- [ ] Validation: `grep -q "^name:" skills/performance/dotnet-ci-benchmarking/SKILL.md`
- [ ] Validation: `grep -l "TODO.*fn-19\|placeholder.*fn-19" skills/performance/dotnet-ci-benchmarking/SKILL.md`

## Done summary
Created `dotnet-profiling` and `dotnet-ci-benchmarking` skills with comprehensive coverage of diagnostic tools and continuous benchmarking workflows. Profiling skill covers dotnet-counters, dotnet-trace (flame graphs, CPU sampling, allocation tracking), and dotnet-dump (SOS commands, memory leak investigation). CI benchmarking skill covers baseline management, GitHub Actions workflows with YAML snippets, threshold-based regression detection, and alerting strategies. Both cross-reference [skill:dotnet-observability]; CI benchmarking includes deferred fn-19 placeholders.
## Evidence
- Commits: bea0e8a79cd157cc20917952100eedc1fd697038
- Tests: ./scripts/validate-skills.sh, grep -q '^name:' skills/performance/dotnet-profiling/SKILL.md, grep -q '^name:' skills/performance/dotnet-ci-benchmarking/SKILL.md, grep -l 'TODO.*fn-19' skills/performance/dotnet-ci-benchmarking/SKILL.md
- PRs: