# fn-18-performance-and-benchmarking-skills.1 Performance skills (BenchmarkDotNet and patterns)

## Description
Create two core performance skills: `dotnet-benchmarkdotnet` for microbenchmarking setup and `dotnet-performance-patterns` for performance-oriented architecture. These skills provide the foundation for measuring and optimizing .NET application performance.

**Files created:**
- `skills/performance/dotnet-benchmarkdotnet/SKILL.md`
- `skills/performance/dotnet-performance-patterns/SKILL.md`

**Cross-references required:**
- `[skill:dotnet-csharp-modern-patterns]` (fn-3) for Span/Memory syntax foundation
- `[skill:dotnet-csharp-coding-standards]` (fn-3) for sealed class coding style
- `[skill:dotnet-native-aot]` (fn-16) for AOT performance characteristics
- `[skill:dotnet-serialization]` (fn-6) for benchmark examples

Both skills must have `name` and `description` frontmatter. Does NOT touch `plugin.json` (handled by fn-18.4).

## Acceptance
- [ ] `skills/performance/dotnet-benchmarkdotnet/SKILL.md` exists with valid frontmatter (name, description)
- [ ] BenchmarkDotNet skill covers:
  - [Benchmark] attribute and class setup
  - Memory diagnosers (MemoryDiagnoser, DisassemblyDiagnoser)
  - Exporters (JSON, HTML, Markdown) for CI integration
  - Baseline comparison ([Benchmark(Baseline = true)])
  - BenchmarkRunner.Run() patterns
  - Common pitfalls (dead code elimination, measurement bias)
- [ ] `skills/performance/dotnet-performance-patterns/SKILL.md` exists with valid frontmatter
- [ ] Performance patterns skill covers:
  - Span<T> and Memory<T> usage for zero-allocation scenarios
  - ArrayPool<T> for buffer pooling
  - readonly struct, ref struct, and in parameters
  - Sealed class performance rationale (JIT devirtualization)
  - stackalloc for small stack-based allocations
  - String interning and StringComparison performance
- [ ] Both skills cross-reference `[skill:dotnet-csharp-modern-patterns]` for Span/Memory syntax
- [ ] Both skills cross-reference `[skill:dotnet-csharp-coding-standards]` for sealed class style
- [ ] Both skills cross-reference `[skill:dotnet-native-aot]` for AOT impact
- [ ] BenchmarkDotNet skill includes serialization benchmark example with `[skill:dotnet-serialization]` cross-ref
- [ ] Both skills include "Out of scope" sections with fn-3/fn-5/fn-6/fn-16 boundary statements
- [ ] Validation: `grep -q "^name:" skills/performance/dotnet-benchmarkdotnet/SKILL.md`
- [ ] Validation: `grep -q "^name:" skills/performance/dotnet-performance-patterns/SKILL.md`

## Done summary
Created `dotnet-benchmarkdotnet` and `dotnet-performance-patterns` skills with comprehensive coverage of microbenchmarking and performance-oriented architecture patterns. Both skills properly cross-reference fn-3, fn-5, fn-6, and fn-16 for boundary management.

## Evidence
- Commits: Skills created with frontmatter and content
- Tests: `./scripts/validate-skills.sh` passes for both skills
- PRs: N/A (single-repo workflow)
