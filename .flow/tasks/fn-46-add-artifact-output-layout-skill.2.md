# fn-46-add-artifact-output-layout-skill.2 Integrate dotnet-artifacts-output into plugin registry and routing

## Description
Register `dotnet-artifacts-output` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references to/from `dotnet-project-structure`, `dotnet-containers`, `dotnet-gha-build-test`.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/project-structure/dotnet-project-structure/SKILL.md`, `skills/architecture/dotnet-containers/SKILL.md`, `skills/ci-cd/dotnet-gha-build-test/SKILL.md`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-artifacts-output]` cross-references in project-structure, containers, CI skills
- Update `--projected-skills` count in validation
## Acceptance
- [ ] plugin.json includes `skills/project-structure/dotnet-artifacts-output`
- [ ] `dotnet-advisor` has routing entry for artifacts output
- [ ] Cross-references added in `dotnet-project-structure`, `dotnet-containers`, `dotnet-gha-build-test`
- [ ] All four validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
