## Description

Add `user-invocable: false` to the frontmatter of 113 implicit reference/convention/pattern skills. T3 handles the 4 detection skills separately. Keep 9 actionable command skills as user-invocable (default). `plugin-self-publish` is removed by T1.

**Size:** M (113 files, repetitive single-line addition)
**Files:** All `skills/<category>/<skill-name>/SKILL.md` except the 9 user-invocable skills AND the 4 detection skills (owned by T3).

## Approach

- For each of the 113 implicit skills, add `user-invocable: false` as a third frontmatter field after `description`
- **DO NOT modify** these 9 skills (they remain user-invocable by default):
  - `dotnet-advisor` (router, entry point)
  - `dotnet-scaffold-project` (scaffolds new projects)
  - `dotnet-add-ci` (adds CI pipelines)
  - `dotnet-add-testing` (adds test infrastructure)
  - `dotnet-add-analyzers` (adds static analysis)
  - `dotnet-modernize` (project audit/upgrade)
  - `dotnet-ui-chooser` (UI framework wizard)
  - `dotnet-data-access-strategy` (data access wizard)
  - `dotnet-version-upgrade` (version migration)
- **DO NOT modify** these 4 detection skills (owned exclusively by T3):
  - `skills/foundation/dotnet-version-detection`
  - `skills/foundation/dotnet-project-analysis`
  - `skills/agent-meta-skills/dotnet-solution-navigation`
  - `skills/agent-meta-skills/dotnet-build-analysis`
- `plugin-self-publish` no longer exists (removed by T1)
- Follow existing frontmatter pattern — fields go between `---` fences, one per line
- Do not change `name`, `description`, or any skill content
- Use `plugin.json` skills array as the canonical list to compute exact target set

## Key context

- The user-invocable list above covers skills that are actionable commands (scaffold, add, audit). All other skills are reference material Claude loads implicitly.
- `user-invocable: false` hides from `/` slash menu but Claude CAN still invoke them and descriptions remain in context budget.
- Validation (T1) must be updated first — otherwise `_validate_skills.py` rejects the new field.
- Classification of `dotnet-data-access-strategy` and `dotnet-version-upgrade` as user-invocable is borderline — can be revisited post-launch based on usage patterns.

## Acceptance

- [ ] 113 implicit skills have `user-invocable: false` in frontmatter
- [ ] 9 user-invocable skills listed above do NOT have `user-invocable: false`
- [ ] 4 detection skills listed above are NOT modified (T3 owns those files)
- [ ] No skill content (below frontmatter) is modified
- [ ] `validate-skills.sh && validate-marketplace.sh` pass clean

## Done summary
Added `user-invocable: false` frontmatter to 113 implicit reference/convention skills, keeping 9 actionable command skills user-invocable (default) and 4 detection skills untouched (T3-owned). All validation passes clean.
## Evidence
- Commits: 64da379878d0cb54a4705b1ea5115850dca46ace
- Tests: ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
- PRs: