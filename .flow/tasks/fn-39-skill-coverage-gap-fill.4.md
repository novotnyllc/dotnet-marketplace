# fn-39-skill-coverage-gap-fill.4 Create dotnet-structured-logging, dotnet-linq-optimization, and dotnet-gc-memory skills

## Description
Create 3 new skills covering logging pipeline, LINQ, and memory management gaps:

1. **dotnet-structured-logging** (`skills/architecture/dotnet-structured-logging/SKILL.md`) — Log pipeline design and operations: log aggregation architecture (ELK/Seq/Loki), structured query patterns (Kibana KQL, Seq signal expressions), log sampling and volume management, PII scrubbing and destructuring policies, cross-service correlation beyond single-service scopes. **Distinct from** `dotnet-observability` which owns: Serilog/NLog/MEL basics, source-generated LoggerMessage, enrichers, single-service log scopes, sink configuration, and OTel logging export. This skill covers what happens _after_ log emission — the pipeline, query, and operations layer.
2. **dotnet-linq-optimization** (`skills/core-csharp/dotnet-linq-optimization/SKILL.md`) — LINQ performance patterns: IQueryable vs IEnumerable materialization, compiled queries for EF Core, deferred execution pitfalls, LINQ-to-Objects allocation patterns, when to drop to manual loops, Span-based alternatives.
3. **dotnet-gc-memory** (`skills/performance/dotnet-gc-memory/SKILL.md`) — GC and memory management: GC modes (workstation vs server), LOH/POH, Gen0/1/2 tuning, memory pressure, Span<T>/Memory<T> deep patterns beyond basics, ArrayPool/MemoryPool, weak references, finalizers vs IDisposable, memory profiling with dotMemory/PerfView.

**Size:** M
**Files:** `skills/architecture/dotnet-structured-logging/SKILL.md`, `skills/core-csharp/dotnet-linq-optimization/SKILL.md`, `skills/performance/dotnet-gc-memory/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Each description under 120 characters (target ~100 chars for budget headroom)
- dotnet-structured-logging cross-refs: `[skill:dotnet-observability]`, `[skill:dotnet-csharp-configuration]`
  - **Scope boundary:** This skill covers log pipeline/operations/queries. `dotnet-observability` covers log emission (MEL, Serilog, enrichers, sinks, OTel export). Add an explicit "Out of scope" section referencing `dotnet-observability` for emission topics.
- dotnet-linq-optimization cross-refs: `[skill:dotnet-efcore-patterns]`, `[skill:dotnet-performance-patterns]`
- dotnet-gc-memory cross-refs: `[skill:dotnet-performance-patterns]`, `[skill:dotnet-profiling]`, `[skill:dotnet-channels]`
- dotnet-gc-memory should reference Toub's GC/performance blog posts as knowledge source
- No fn-N spec references, latest stable package versions
## Acceptance
- [ ] dotnet-structured-logging SKILL.md created with frontmatter
- [ ] Covers log aggregation architecture, structured queries, sampling, PII scrubbing, cross-service correlation
- [ ] Has explicit "Out of scope" section referencing `dotnet-observability` for emission topics
- [ ] Distinct from dotnet-observability (no content overlap — pipeline/ops vs emission)
- [ ] dotnet-linq-optimization SKILL.md created with frontmatter
- [ ] Covers IQueryable vs IEnumerable, compiled queries, allocation patterns
- [ ] dotnet-gc-memory SKILL.md created with frontmatter
- [ ] Covers GC modes, LOH/POH, Span/Memory deep patterns, memory profiling
- [ ] All cross-references use `[skill:...]` syntax
- [ ] All descriptions under 120 characters
- [ ] All SKILL.md files under 5,000 words
- [ ] No fn-N spec references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
