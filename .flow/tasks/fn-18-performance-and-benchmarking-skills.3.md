# fn-18-performance-and-benchmarking-skills.3 Performance agents

## Description
Create two specialized performance agents: `dotnet-performance-analyst` for analyzing profiling data and benchmarks, and `dotnet-benchmark-designer` for designing effective benchmarks. These agents provide expert guidance for performance-critical work.

**Files created:**
- `agents/dotnet-performance-analyst.md`
- `agents/dotnet-benchmark-designer.md`

**Agent definitions:**
- **dotnet-performance-analyst**: Performance engineer persona. Analyzes profiling data (dotnet-trace flame graphs, dotnet-dump heap analysis), interprets benchmark comparisons, identifies bottlenecks, suggests optimizations. Loads `[skill:dotnet-profiling]`, `[skill:dotnet-benchmarkdotnet]`, `[skill:dotnet-observability]`.
- **dotnet-benchmark-designer**: Benchmarking specialist persona. Designs effective benchmarks, avoids common pitfalls (dead code elimination, measurement bias), chooses correct memory diagnosers, validates benchmark methodology. Loads `[skill:dotnet-benchmarkdotnet]`, `[skill:dotnet-performance-patterns]`.

Both agents must have frontmatter compatible with existing agents (see `agents/dotnet-architect.md` for reference structure). Does NOT touch `plugin.json` (handled by fn-18.4).

## Acceptance
- [ ] `agents/dotnet-performance-analyst.md` exists with appropriate frontmatter (compatible with existing agent format)
- [ ] Performance analyst agent defines:
  - Persona: Senior performance engineer specializing in .NET diagnostics
  - Triggers: Performance analysis, profiling investigation, benchmark interpretation
  - Skills loaded: `dotnet-profiling`, `dotnet-benchmarkdotnet`, `dotnet-observability`
  - Specialization: Reading flame graphs, heap dump analysis, regression root cause analysis
- [ ] Performance analyst agent includes example prompts (e.g., "Analyze this dotnet-trace output", "Why is this benchmark showing regression?")
- [ ] `agents/dotnet-benchmark-designer.md` exists with appropriate frontmatter
- [ ] Benchmark designer agent defines:
  - Persona: Benchmarking methodology expert for .NET applications
  - Triggers: Benchmark design, methodology review, measurement validation
  - Skills loaded: `dotnet-benchmarkdotnet`, `dotnet-performance-patterns`
  - Specialization: Avoiding dead code elimination, choosing diagnosers, baseline setup
- [ ] Benchmark designer agent includes example prompts (e.g., "Design a benchmark for this algorithm", "Review this benchmark for pitfalls")
- [ ] Both agents have distinct, non-overlapping scopes
- [ ] Both agents cross-reference the skills they load using `[skill:...]` syntax
- [ ] Validation: `test -f agents/dotnet-performance-analyst.md`
- [ ] Validation: `test -f agents/dotnet-benchmark-designer.md`
- [ ] Validation: Both agents follow existing agent frontmatter/structure conventions

## Done summary
Created `dotnet-performance-analyst` and `dotnet-benchmark-designer` agents with distinct personas and skill loads. Performance analyst focuses on analyzing profiling data (flame graphs, heap dumps, benchmark comparisons) and loads dotnet-profiling, dotnet-benchmarkdotnet, dotnet-observability. Benchmark designer focuses on designing valid benchmarks and avoiding methodology pitfalls (dead code elimination, constant folding, measurement bias) and loads dotnet-benchmarkdotnet, dotnet-performance-patterns.
## Evidence
- Commits: c899a6a2b603182dcfe891e06c063a6e0429f5fc
- Tests: ./scripts/validate-skills.sh, test -f agents/dotnet-performance-analyst.md, test -f agents/dotnet-benchmark-designer.md, grep -q '^name:' agents/dotnet-performance-analyst.md, grep -q '^name:' agents/dotnet-benchmark-designer.md
- PRs: