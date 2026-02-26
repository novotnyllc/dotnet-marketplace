# fn-64-consolidate-131-skills-into-20-broad.2 Consolidate core language skills: dotnet-csharp, dotnet-debugging, dotnet-project-setup

## Description
Create consolidated `dotnet-csharp` skill directory. Merge ~22 C# language skills into one skill with companion files. Remove source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-csharp/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~22 source skill dirs (delete)

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
- Remove old skill directories after content migrated
- Update `plugin.json`: remove old paths, add `skills/dotnet-csharp`

## Key context

- `dotnet-csharp-async-patterns` is referenced by 4 agents (most-shared skill) — companion file must be easily discoverable from ToC
- `dotnet-csharp-coding-standards` is the baseline for all C# code reviews — put prominently in SKILL.md overview
- Several source skills have existing `details.md` or `examples.md` — absorb into appropriate companion files
## Approach

- Follow consolidation map from task .1
- For each consolidated skill: write SKILL.md (overview + scope + routing ToC, ~2-5KB), create `references/` dir with topic-named companion files from source skills
- `dotnet-debugging` stays standalone per user requirement — consolidate `dotnet-windbg-debugging` (with its existing 16 `reference/` files) plus any other debugging content
- Remove old skill directories after content is migrated
- Update `plugin.json` skills array: remove old paths, add new paths

## Key context

- `dotnet-csharp` merges ~11 skills: modern-patterns, coding-standards, async-patterns, nullable-reference-types, dependency-injection, configuration, source-generators, code-smells, roslyn-analyzers, editorconfig, and others per mapping
- `dotnet-project-setup` merges ~8 skills: project-structure, artifacts-output, scaffold-project, add-analyzers, add-ci, add-testing, modernize, and others per mapping
- `dotnet-windbg-debugging` already has `reference/` dir with 16 files — rename to `references/` to match convention
## Acceptance
- [ ] `skills/dotnet-csharp/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-csharp/references/` contains companion files from all merged source skills
- [ ] All ~22 source C# skill directories deleted
- [ ] `plugin.json` updated: old paths removed, new path added
- [ ] Valid frontmatter (name, description, license, user-invocable)
- [ ] No content lost from source skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
