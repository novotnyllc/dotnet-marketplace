# fn-64.2 Consolidate dotnet-csharp (~22 source skills)

## Description
Create consolidated `dotnet-csharp` skill directory. Merge ~22 C# language skills into one skill with companion files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-csharp/SKILL.md` + `references/*.md` (new), ~22 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: overview, routing table with keyword hints, scope/out-of-scope, ToC to companion files (~3-5KB)
- Create `references/` dir with topic-named companion files. Expected files (per map from .1):
  - `references/modern-patterns.md` — records, pattern matching, init-only, file-scoped
  - `references/async-patterns.md` — async/await, ValueTask, ConfigureAwait
  - `references/dependency-injection.md` — DI registration, lifetime, Options pattern
  - `references/source-generators.md` — Roslyn incremental generators
  - `references/coding-standards.md` — conventions, code smells, analyzers, editorconfig
  - `references/serialization.md` — System.Text.Json, polymorphic, source generation
  - `references/concurrency.md` — threading, locks, channels, LINQ optimization
  - `references/domain-modeling.md` — aggregates, SOLID, validation, file I/O, native interop
  - (exact list per task .1 output)
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- `dotnet-csharp-async-patterns` is referenced by 4 agents (most-shared skill) — companion file must be easily discoverable from ToC
- `dotnet-csharp-coding-standards` is the baseline for all C# code reviews — put prominently in SKILL.md overview
- Several source skills have existing `details.md` or `examples.md` — absorb into appropriate companion files
- All project-setup content (scaffolding, artifacts output, add-analyzers, add-ci, add-testing, modernize) goes in `dotnet-tooling` (task .6), NOT here

## Acceptance
- [ ] `skills/dotnet-csharp/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-csharp/references/` contains companion files from all merged source skills
- [ ] All ~22 source C# skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter (name, description, license, user-invocable)
- [ ] No content lost from source skills

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
