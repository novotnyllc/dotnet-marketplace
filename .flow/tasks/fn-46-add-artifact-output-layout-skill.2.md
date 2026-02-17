# fn-46-add-artifact-output-layout-skill.2 Integrate dotnet-artifacts-output into plugin registry and routing

## Description
Register `dotnet-artifacts-output` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/project-structure/dotnet-project-structure/SKILL.md`, `skills/architecture/dotnet-containers/SKILL.md`, `skills/ci-cd/dotnet-gha-build-test/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-artifacts-output]` cross-references in project-structure, containers, CI skills
- Update `--projected-skills` in validate-skills.sh

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files.** Run integration tasks sequentially.
## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-artifacts-output]` cross-references in project-structure, containers, CI skills
- Update `--projected-skills` count in validation
## Acceptance
- [ ] plugin.json includes `skills/project-structure/dotnet-artifacts-output`
- [ ] `dotnet-advisor` has routing entry for artifacts output
- [ ] Cross-references added in `dotnet-project-structure`, `dotnet-containers`, `dotnet-gha-build-test`
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
Integrated dotnet-artifacts-output skill into plugin registry and routing: registered in plugin.json, added catalog entry and routing rule in dotnet-advisor, added bidirectional cross-references in dotnet-project-structure, dotnet-containers, and dotnet-gha-build-test, and incremented --projected-skills to 126 with --fail-threshold adjusted to 15200.
## Evidence
- Commits: b28f48e93d416a730fa7e5bcce8c8c6ea3d6de86
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: