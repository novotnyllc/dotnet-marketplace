# fn-64-consolidate-131-skills-into-20-broad.6 Consolidate DevOps skills: dotnet-cicd-gha, dotnet-cicd-ado, dotnet-containers, dotnet-packaging

## Description
Create consolidated skill directories for DevOps skills: `dotnet-cicd-gha`, `dotnet-cicd-ado`, `dotnet-containers`, and `dotnet-packaging`.

**Size:** M
**Files:** `skills/dotnet-cicd-gha/SKILL.md` + `references/*.md` (new), `skills/dotnet-cicd-ado/SKILL.md` + `references/*.md` (new), `skills/dotnet-containers/SKILL.md` + `references/*.md` (new), `skills/dotnet-packaging/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~14 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- `dotnet-cicd-gha` merges: gha-patterns, gha-build-test, gha-publish, gha-deploy
- `dotnet-cicd-ado` merges: ado-patterns, ado-build-test, ado-publish, ado-unique
- `dotnet-containers` merges: containers, container-deployment
- `dotnet-packaging` merges: nuget-authoring, msix, github-releases, release-management
## Acceptance
- [ ] 4 consolidated skill directories created with SKILL.md + references/
- [ ] All source skill directories for this batch deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on all SKILL.md files
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
