# fn-3-core-c-and-language-patterns-skills.4 Concurrency specialist agent

## Description
Create the `dotnet-csharp-concurrency-specialist` agent at `agents/dotnet-csharp-concurrency-specialist.md`.

**Agent frontmatter:**
- `name`: `dotnet-csharp-concurrency-specialist`
- `description`: Trigger phrase covering race conditions, deadlocks, thread safety, concurrent access, lock contention, async races, parallel execution, synchronization issues
- `model`: `sonnet` (matches `dotnet-architect` precedent)
- `tools`: `Read`, `Grep`, `Glob` (read-only analysis, matches `dotnet-architect`)

**Agent body:**
- Deep expertise in `Task`/`async` patterns, thread safety analysis, synchronization primitives (`SemaphoreSlim`, `lock`, `Interlocked`, `Channel<T>`)
- Race condition identification and fix patterns
- Common concurrency mistakes agents make: shared mutable state, incorrect `ConcurrentDictionary` usage, `async void` event handlers, deadlocking on `.Result`
- Preloaded skill references: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-modern-patterns]`
- Decision tree: "Is this a race condition? -> Check shared state. Is this a deadlock? -> Check blocking calls."

**Registration:** Add `"agents/dotnet-csharp-concurrency-specialist.md"` to `plugin.json` `agents` array.

## Acceptance
- [ ] `agents/dotnet-csharp-concurrency-specialist.md` exists with valid agent frontmatter (name, description, model, tools)
- [ ] Trigger phrases cover: race condition, deadlock, thread safety, concurrent access, lock contention
- [ ] Preloaded skill references: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-modern-patterns]`
- [ ] Agent registered in `plugin.json` `agents` array
- [ ] Description follows WHEN/WHEN NOT pattern
- [ ] `./scripts/validate-skills.sh` passes (validates plugin.json agent refs)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
