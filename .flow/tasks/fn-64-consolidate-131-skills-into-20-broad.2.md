# fn-64-consolidate-131-skills-into-20-broad.2 Consolidate core language skills: dotnet-csharp, dotnet-debugging, dotnet-project-setup

## Description
Create consolidated skill directories for core language skills: `dotnet-csharp`, `dotnet-debugging`, and `dotnet-project-setup`. Remove the source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-csharp/SKILL.md` + `references/*.md` (new), `skills/dotnet-debugging/SKILL.md` + `references/*.md` (new), `skills/dotnet-project-setup/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~25 source skill dirs (delete)

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
- [ ] `skills/dotnet-csharp/SKILL.md` exists with overview, scope, out-of-scope, and ToC to references/
- [ ] `skills/dotnet-csharp/references/` contains companion files from all merged source skills
- [ ] `skills/dotnet-debugging/SKILL.md` exists (standalone, user requirement)
- [ ] `skills/dotnet-debugging/references/` migrates windbg-debugging reference/ content
- [ ] `skills/dotnet-project-setup/SKILL.md` exists with overview and ToC
- [ ] `skills/dotnet-project-setup/references/` contains companion files
- [ ] All source skill directories for this batch deleted
- [ ] `plugin.json` updated with new paths, old paths removed
- [ ] All SKILL.md files have valid frontmatter (name, description, license, user-invocable)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
