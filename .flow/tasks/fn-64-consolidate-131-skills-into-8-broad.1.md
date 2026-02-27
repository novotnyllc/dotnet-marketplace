# fn-64.1 Skill audit and 8-skill consolidation map

## Description
Read all 131 SKILL.md files and produce a definitive 8-skill consolidation map: which of the 131 source skills merge into which of the 8 target skills, what content goes in each SKILL.md vs references/ companion files, and the routing description for each target skill.

**Size:** M
**Files:** All 131 `skills/*/SKILL.md` (read-only), task spec output

## Approach

1. Read every SKILL.md frontmatter + body (description, scope, key content)
2. Assign each source skill to exactly one of the 8 target skills:
   - **dotnet-csharp** (~22): language patterns, async, DI, config, generators, standards, nullable, serialization, channels, LINQ, domain modeling, SOLID, concurrency, analyzers, editorconfig, file I/O, native interop, validation
   - **dotnet-api** (~28): ASP.NET Core, minimal APIs, middleware, EF Core, data access, gRPC, SignalR, resilience, HTTP client, API versioning, OpenAPI, security (OWASP, secrets, crypto), background services, Aspire, Semantic Kernel, architecture
   - **dotnet-ui** (~18): Blazor (patterns, components, auth, testing), MAUI (dev, AOT, testing), Uno (platform, targets, MCP, testing), WPF, WinUI, WinForms, accessibility, localization, UI chooser
   - **dotnet-testing** (~11): strategy, xUnit, integration, snapshot, Playwright, UI testing core, BenchmarkDotNet, test quality, CI benchmarking
   - **dotnet-devops** (~18): CI/CD (GHA 4 + ADO 4), containers (2), NuGet, MSIX, GitHub Releases, release mgmt, observability, structured logging
   - **dotnet-tooling** (~34): project setup, MSBuild, build, perf patterns, profiling, AOT/trimming, GC/memory, CLI apps, terminal UI, docs generation, tool mgmt, version detection/upgrade, solution nav, agent meta-skills
   - **dotnet-debugging** (~2): WinDbg + debugging patterns (standalone, user requirement)
   - **dotnet-advisor** (1): router — rewrite for 8 skills
3. For each target skill, document:
   - Routing description (aim for 300-400 chars with rich keywords)
   - SKILL.md content outline (overview, routing table with keyword hints, scope/out-of-scope, ToC)
   - `references/` companion file list with topic names
   - Which source SKILL.md files have existing companion files (details.md, examples.md, reference/) that need migration
4. Handle edge cases: user-invocable skills (11 currently), skills with existing companion files, cross-cutting skills that could go in multiple buckets
5. Identify gap analysis resolution: all previously unmapped skills must have explicit assignments

## Key context

- Only SKILL.md auto-loads on activation; companion files need explicit model reads
- SKILL.md must include ToC directing model to companion files
- `dotnet-windbg-debugging` already has `reference/` dir with 16 files — rename to `references/`
- 11 skills are currently user-invocable: true — decide which of the 8 target skills gets user-invocable
- With 8 skills, description budget drops from 75% to ~20% — each description gets 400+ chars

## Acceptance
- [ ] Every one of 131 current skills has explicit assignment to one of the 8 target skills
- [ ] Each target skill has: routing description (300-400 chars), SKILL.md content outline, references/ file list
- [ ] No skill left unassigned
- [ ] Edge cases resolved: user-invocable assignments, existing companion file migrations, cross-cutting skill placements
- [ ] Companion file naming convention documented (references/<topic>.md)

## Done summary
Produced the definitive 8-skill consolidation map (docs/consolidation-map-8-skills.md) mapping all 131 source skills to 8 target skills with routing descriptions, SKILL.md content outlines, explicit references/ companion file lists, edge case resolutions, user-invocable assignments, and diff-verified 1:1 assignment roster.
## Evidence
- Commits: 1b75dfe, 91c65ee, 5a85922, ff8f914, 72042ee
- Tests: diff verification: all 131 skill directories matched roster with zero diff, per-target count verification: 22+27+18+12+18+32+1+1=131
- PRs: