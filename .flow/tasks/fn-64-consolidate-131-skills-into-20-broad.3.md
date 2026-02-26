# fn-64-consolidate-131-skills-into-20-broad.3 Consolidate testing skills: dotnet-testing

## Description
Create consolidated `dotnet-testing` skill directory. Merge all testing-related skills (strategy, xunit, integration, snapshot, test-quality, playwright, ui-testing-core). Framework-specific testing skills (blazor-testing, maui-testing, uno-testing) go to their respective UI framework groups (tasks .5), not here.

**Size:** M
**Files:** `skills/dotnet-testing/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~7 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- SKILL.md: testing strategy overview, when to use which test type, scope/out-of-scope, ToC to companion files
- `references/xunit.md`, `references/integration-testing.md`, `references/snapshot-testing.md`, `references/playwright.md`, `references/test-quality.md` etc.
- Framework-specific testing content (bUnit, Appium, Playwright for Uno) stays with tasks .5

## Key context

- `dotnet-testing-specialist` agent preloads testing skills — will need updating in task .9
- Agent also delegates to framework-specific testing via Explicit Boundaries — those refs update in task .9
## Acceptance
- [ ] `skills/dotnet-testing/SKILL.md` exists with overview, scope, out-of-scope, ToC
- [ ] `skills/dotnet-testing/references/` contains companion files from merged testing skills
- [ ] Framework-specific testing skills NOT merged here (left for task .5)
- [ ] All source testing skill directories deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on SKILL.md
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
