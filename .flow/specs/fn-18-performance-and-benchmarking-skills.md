# fn-18: Performance and Benchmarking Skills

## Problem/Goal
Add comprehensive performance and benchmarking skills covering BenchmarkDotNet, performance-oriented architecture patterns, profiling tools, and continuous benchmarking in CI. Enable dotnet-performance-analyst and dotnet-benchmark-designer agents.

## Acceptance Checks
- [ ] `dotnet-benchmarkdotnet` skill covers setup, custom configs, memory diagnosers, exporters, baselines, CI integration
- [ ] `dotnet-performance-patterns` skill covers performance architecture (Span<T>, pooling, zero-alloc, struct design, sealed classes)
- [ ] `dotnet-profiling` skill covers dotnet-counters, dotnet-trace, dotnet-dump, memory profiling, allocation analysis
- [ ] `dotnet-ci-benchmarking` skill covers continuous benchmarking (comparison, regression detection, alerting)
- [ ] `dotnet-performance-analyst` agent analyzes profiling results and benchmark comparisons
- [ ] `dotnet-benchmark-designer` agent designs effective benchmarks
- [ ] Cross-references to AOT skills, serialization, architecture patterns

## Key Context
- BenchmarkDotNet is the industry standard
- Performance patterns reference existing dotnet-skills material
- CI benchmarking prevents performance regressions
- Profiling tools are built into .NET SDK
