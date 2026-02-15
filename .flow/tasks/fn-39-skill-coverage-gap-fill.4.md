# fn-39-skill-coverage-gap-fill.4 Create dotnet-structured-logging, dotnet-linq-optimization, and dotnet-gc-memory skills

## Description
Create 3 new skills covering logging, LINQ, and memory management gaps:

1. **dotnet-structured-logging** (`skills/architecture/dotnet-structured-logging/SKILL.md`) — Structured logging deep dive: Serilog vs NLog vs Microsoft.Extensions.Logging, log enrichers, semantic logging, correlation IDs, log levels strategy, structured query patterns, sink configuration. Distinct from dotnet-observability (which covers OpenTelemetry/distributed tracing).
2. **dotnet-linq-optimization** (`skills/core-csharp/dotnet-linq-optimization/SKILL.md`) — LINQ performance patterns: IQueryable vs IEnumerable materialization, compiled queries for EF Core, deferred execution pitfalls, LINQ-to-Objects allocation patterns, when to drop to manual loops, Span-based alternatives.
3. **dotnet-gc-memory** (`skills/performance/dotnet-gc-memory/SKILL.md`) — GC and memory management: GC modes (workstation vs server), LOH/POH, Gen0/1/2 tuning, memory pressure, Span<T>/Memory<T> deep patterns beyond basics, ArrayPool/MemoryPool, weak references, finalizers vs IDisposable, memory profiling with dotMemory/PerfView.

**Size:** M
**Files:** `skills/architecture/dotnet-structured-logging/SKILL.md`, `skills/core-csharp/dotnet-linq-optimization/SKILL.md`, `skills/performance/dotnet-gc-memory/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Each description under 120 characters
- dotnet-structured-logging cross-refs: `[skill:dotnet-observability]`, `[skill:dotnet-csharp-configuration]`
- dotnet-linq-optimization cross-refs: `[skill:dotnet-efcore-patterns]`, `[skill:dotnet-performance-patterns]`
- dotnet-gc-memory cross-refs: `[skill:dotnet-performance-patterns]`, `[skill:dotnet-profiling]`
- dotnet-gc-memory should reference Toub's GC/performance blog posts as knowledge source
- No fn-N spec references, latest stable package versions
## Acceptance
- [ ] dotnet-structured-logging SKILL.md created with frontmatter
- [ ] Covers Serilog, NLog, MEL, enrichers, correlation IDs, sinks
- [ ] Distinct from dotnet-observability (no overlap)
- [ ] dotnet-linq-optimization SKILL.md created with frontmatter
- [ ] Covers IQueryable vs IEnumerable, compiled queries, allocation patterns
- [ ] dotnet-gc-memory SKILL.md created with frontmatter
- [ ] Covers GC modes, LOH/POH, Span/Memory deep patterns, memory profiling
- [ ] All cross-references use `[skill:...]` syntax
- [ ] All descriptions under 120 characters
- [ ] No fn-N spec references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
