# fn-7-testing-foundation-skills.4 Plugin registration and fn-7 reconciliation

## Description
Register all 10 testing skills in plugin.json and reconcile all fn-7 TODO placeholders across the `skills/` directory.

**No new skills created.** This task is integration-only.

**Integration work:**
- Register all 10 `skills/testing/*` entries in `.claude-plugin/plugin.json` (sole owner of plugin.json changes for fn-7)
- Replace ALL `<!-- TODO: fn-7 reconciliation -->` and `<!-- TODO(fn-7): ... -->` placeholders in `skills/` with canonical `[skill:...]` cross-references
- Update `skills/architecture/FN7-RECONCILIATION.md` verification commands to include serialization scope
- Update `dotnet-add-testing` fn-7 references to use canonical `[skill:...]` syntax

**File ownership:** This task is the sole owner of `plugin.json` modifications for fn-7. It also modifies (but does not own) `skills/architecture/FN7-RECONCILIATION.md`, `skills/project-structure/dotnet-add-testing/SKILL.md`, and the 14 architecture/serialization skills containing fn-7 TODOs.

**Depends on:** Tasks 1, 2, 3 (needs all 10 skill files to exist before registration and reconciliation).

## Acceptance
- [ ] All 10 testing skills registered in `.claude-plugin/plugin.json` (verify: `grep -c "skills/testing/" .claude-plugin/plugin.json` = 10)
- [ ] Zero fn-7 TODO placeholders remain in `skills/`: `grep -rl "TODO.*fn-7\|fn-7.*TODO" skills/` returns empty
- [ ] `dotnet-add-testing` "What is Next" section uses `[skill:dotnet-xunit]`, `[skill:dotnet-integration-testing]`, etc. instead of "fn-7"
- [ ] `FN7-RECONCILIATION.md` updated to include serialization scope and post-reconciliation verification covering `skills/` (not just `skills/architecture/`)
- [ ] Cross-reference validation: `grep -rl "\[skill:dotnet-integration-testing\]" skills/` returns >=4 files

## Done summary
Registered all 10 testing skills in plugin.json and reconciled all fn-7 TODO placeholders across 14 architecture/serialization skills and dotnet-add-testing with canonical [skill:...] cross-references. Updated FN7-RECONCILIATION.md to include serialization scope and broader verification commands.
## Evidence
- Commits: 876dafec123a2a08d23da486910056660867a732
- Tests: grep -c skills/testing/ .claude-plugin/plugin.json = 10, grep -rl TODO.*fn-7 skills/ = empty, grep -rl [skill:dotnet-integration-testing] skills/ = 20 files
- PRs: