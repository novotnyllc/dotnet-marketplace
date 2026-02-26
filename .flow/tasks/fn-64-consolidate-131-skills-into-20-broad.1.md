# fn-64-consolidate-131-skills-into-20-broad.1 Comprehensive skill audit and consolidation map

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

## Key context

- Only SKILL.md auto-loads on activation; companion files need explicit model reads
- SKILL.md must include ToC directing model to companion files
- `dotnet-windbg-debugging` already has `reference/` dir with 16 files — rename to `references/`
- 11 skills are currently user-invocable: true — decide which of the 8 target skills gets user-invocable
- With 8 skills, description budget drops from 75% to ~20% — each description gets 400+ chars
## Approach

1. Read every SKILL.md frontmatter + body (size, description, scope, key content areas)
2. Identify natural groupings by domain affinity, cross-reference patterns, and agent preloaded skills
3. For each proposed consolidated skill, list:
   - Source skills being merged
   - What goes in SKILL.md overview (~2-5KB target)
   - What goes in `references/<topic>.md` companion files
   - Routing description (under 400 chars)
4. Resolve all unmapped skills identified in gap analysis (~37 skills)
5. Decide: dotnet-advisor routing catalog rewrite scope
6. Decide: framework-specific testing skills placement (UI group vs testing group)
7. Document companion file naming convention (`references/<topic>.md`)

## Key context

- Gap analysis identified 37 unmapped skills including: dotnet-advisor, dotnet-aspire-patterns, dotnet-semantic-kernel, dotnet-localization, dotnet-messaging-patterns, dotnet-domain-modeling, dotnet-background-services, framework-testing skills, agent meta-skills
- Only SKILL.md auto-loads on activation; companion files need explicit model reads
- SKILL.md must include ToC directing model to companion files
- Target: ~20 consolidated skills, each under 400 chars description
- Existing companion files: 2 details.md, 10 examples.md, 1 reference/ dir with 16 files — all must migrate
## Acceptance
- [ ] Every one of 131 current skills has explicit assignment to one of the 8 target skills
- [ ] Each target skill has: routing description (300-400 chars), SKILL.md content outline, references/ file list
- [ ] No skill left unassigned
- [ ] Edge cases resolved: user-invocable assignments, existing companion file migrations, cross-cutting skill placements
- [ ] Companion file naming convention documented (references/<topic>.md)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
