# fn-52-fill-skill-gaps-from-dotnet-skills.3 Add C# design skills (API design, concurrency, type-design-perf)

## Description
Create 3 C# design skills: `dotnet-csharp-api-design`, `dotnet-csharp-concurrency-patterns`, `dotnet-csharp-type-design-performance`.

**Size:** M (3 related S skills)
**Files:** `skills/api-development/dotnet-csharp-api-design/SKILL.md`, `skills/core-csharp/dotnet-csharp-concurrency-patterns/SKILL.md`, `skills/core-csharp/dotnet-csharp-type-design-performance/SKILL.md`

## Approach

### dotnet-csharp-api-design
- Focus: **Design-time** API decisions (naming conventions, parameter ordering, return type patterns, error reporting, extension points, wire compatibility for serialized types)
- Differentiation from existing skills: `dotnet-library-api-compat` focuses on enforcement (binary/source compat tooling), `dotnet-api-surface-validation` focuses on CI detection. This skill covers the **design principles** that make APIs compatible in the first place.
- Follow pattern at `skills/api-development/dotnet-library-api-compat/SKILL.md`
- Cross-reference: `[skill:dotnet-library-api-compat]`, `[skill:dotnet-api-surface-validation]`, `[skill:dotnet-csharp-coding-standards]`

### dotnet-csharp-concurrency-patterns
- Focus: Thread synchronization primitives and concurrent data structures (lock, Monitor, SemaphoreSlim, Mutex, Interlocked, ConcurrentDictionary, ConcurrentQueue, ReaderWriterLockSlim, SpinLock)
- Include concurrency decision framework: when to use each primitive
- Differentiation: `dotnet-csharp-async-patterns` covers async/await and Task-based patterns. `dotnet-channels` covers producer/consumer. This skill covers **synchronization** and **thread-safe data access**.
- The `dotnet-csharp-concurrency-specialist` agent (200 lines) has substantial content — the skill should be the authoritative source; the agent can reference it.
- Cross-reference: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-channels]`

### dotnet-csharp-type-design-performance
- Focus: Upfront type design choices for performance (struct vs class decision matrix, sealed by default for library types, readonly struct, ref struct, Span<T>/Memory<T> selection, collection type selection including FrozenDictionary/.NET 8+)
- Differentiation: `dotnet-performance-patterns` covers optimization techniques (pooling, caching, async I/O). This skill covers **designing types correctly from the start**.
- Cross-reference: `[skill:dotnet-performance-patterns]`, `[skill:dotnet-csharp-modern-patterns]`, `[skill:dotnet-gc-memory]`

## Key Context

- All 3 skills: `user-invocable: false`
- Since .NET 8 is the baseline, FrozenDictionary is in-scope by default. Include a version note (e.g., "Requires .NET 8+") for readers on older TFMs, but no conditional compilation guidance needed.
- Concurrency specialist agent at `agents/dotnet-csharp-concurrency-specialist.md` line 28-29 lists preloaded skills — will be updated in T4 to include the new skill
## Acceptance
- [ ] `skills/api-development/dotnet-csharp-api-design/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-concurrency-patterns/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-type-design-performance/SKILL.md` exists with valid frontmatter
- [ ] All 3 `name` fields match directory names
- [ ] All 3 `description` fields under 120 characters
- [ ] All 3 have `user-invocable: false`
- [ ] API design skill covers naming, parameter ordering, return types, error patterns, extension points
- [ ] API design skill differentiates from library-api-compat (enforcement) and api-surface-validation (tooling)
- [ ] Concurrency skill covers lock, SemaphoreSlim, Interlocked, ConcurrentDictionary, ReaderWriterLockSlim
- [ ] Concurrency skill includes decision framework for choosing primitives
- [ ] Concurrency skill differentiates from async-patterns and channels
- [ ] Type-design-perf skill covers struct vs class matrix, sealed, readonly struct, Span/Memory, collection selection
- [ ] Type-design-perf skill differentiates from performance-patterns (optimization vs design)
- [ ] All 3 skills have ## Agent Gotchas, ## Prerequisites, ## References sections
- [ ] Appropriate cross-references to existing related skills
## Done summary
Created 3 C# design skills: dotnet-csharp-api-design (API naming, parameter ordering, return types, error patterns, extension points, wire compatibility), dotnet-csharp-concurrency-patterns (lock, SemaphoreSlim, Interlocked, ConcurrentDictionary, ReaderWriterLockSlim, SpinLock with decision framework), and dotnet-csharp-type-design-performance (struct vs class matrix, sealed by default, readonly struct, Span/Memory selection, FrozenDictionary collection selection).
## Evidence
- Commits: f50563a1441685d47ed557c53632ea0ab2a980bb
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: