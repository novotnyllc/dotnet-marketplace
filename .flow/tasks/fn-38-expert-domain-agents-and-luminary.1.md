# fn-38-expert-domain-agents-and-luminary.1 Create dotnet-async-performance-specialist agent (Toub-grounded)

## Description
Create `agents/dotnet-async-performance-specialist.md` — a domain-named agent for deep async/await and runtime performance analysis, grounded in Stephen Toub's expertise.

**Size:** M
**Files:** `agents/dotnet-async-performance-specialist.md`, `.claude-plugin/plugin.json`

## Approach
- Follow agent frontmatter pattern from `agents/dotnet-csharp-concurrency-specialist.md`
- Agent name: `dotnet-async-performance-specialist` (domain name, NOT person name)
- Include "Knowledge Sources" section citing Toub's .NET performance blog series, ConfigureAwait FAQ, and async internals deep-dives
- Include disclaimer: "This agent applies publicly documented guidance. It does not represent or speak for the named knowledge sources."
- Preloaded skills: `dotnet-csharp-async-patterns`, `dotnet-performance-patterns`, `dotnet-profiling`, `dotnet-channels`
- Decision tree covering: ValueTask vs Task, ConfigureAwait decisions, async overhead detection, ThreadPool tuning, IO.Pipelines vs Streams
- Explicit boundaries: "Does NOT handle thread synchronization primitives (use concurrency-specialist)" and "Does NOT handle general profiling workflow (use performance-analyst)"
- Tools: Read, Grep, Glob, Bash (analysis only, read-only)
- Model: sonnet
- Keep under 3,000 tokens total
- Register in `.claude-plugin/plugin.json` agents array

## Key context
- Scope boundary with existing `dotnet-csharp-concurrency-specialist`: that agent covers threading primitives, locks, Interlocked, concurrent collections. This new agent covers async/await performance, ValueTask, ConfigureAwait, IO.Pipelines.
- Scope boundary with existing `dotnet-performance-analyst`: that agent analyzes profiling data and benchmarks. This new agent provides domain-specific async performance guidance.
- Stephen Toub's ConfigureAwait FAQ: ConfigureAwait(false) no longer needed in ASP.NET Core app code (.NET Core+), but still recommended in library code targeting both Framework and Core.
## Acceptance
- [ ] Agent file created at `agents/dotnet-async-performance-specialist.md`
- [ ] Frontmatter includes name, description, model (sonnet), capabilities, tools
- [ ] "Knowledge Sources" section cites Toub's blog, ConfigureAwait FAQ, async internals
- [ ] Disclaimer language included ("does not represent or speak for")
- [ ] Decision tree covers ValueTask vs Task, ConfigureAwait, async overhead, ThreadPool
- [ ] Explicit boundaries: no overlap with concurrency-specialist or performance-analyst
- [ ] Preloaded skills listed with `[skill:...]` cross-references
- [ ] Agent under 3,000 tokens
- [ ] Registered in `.claude-plugin/plugin.json` agents array
- [ ] All four validation commands pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
