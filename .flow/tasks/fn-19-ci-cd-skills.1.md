# fn-19-ci-cd-skills.1 Create GitHub Actions skills (patterns, build-test, publish, deploy)

## Description
Create 4 GitHub Actions skills covering composable workflow patterns, build/test workflows, publishing workflows, and deployment patterns. These skills provide depth beyond the starter templates in `[skill:dotnet-add-ci]`.

**Files created:**
- `skills/cicd/dotnet-gha-patterns/SKILL.md`
- `skills/cicd/dotnet-gha-build-test/SKILL.md`
- `skills/cicd/dotnet-gha-publish/SKILL.md`
- `skills/cicd/dotnet-gha-deploy/SKILL.md`

**Cross-references required:**
- `[skill:dotnet-native-aot]` (fn-16) for AOT publish workflows in `dotnet-gha-publish`
- `[skill:dotnet-cli-release-pipeline]` (fn-17) scope boundary in `dotnet-gha-patterns`
- `[skill:dotnet-containers]` (fn-5) for container publish in `dotnet-gha-publish`
- `[skill:dotnet-ci-benchmarking]` (fn-18) for benchmark integration in `dotnet-gha-build-test`
- `[skill:dotnet-add-ci]` (fn-4) scope boundary in `dotnet-gha-patterns`
- `[skill:dotnet-container-deployment]` (fn-5) for deploy context in `dotnet-gha-deploy`
- `[skill:dotnet-testing-strategy]` (fn-7) for test reporting context in `dotnet-gha-build-test`

All skills must have `name` and `description` frontmatter. Each skill must contain out-of-scope boundary statements. Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-19.3).

## Acceptance
- [ ] `skills/cicd/dotnet-gha-patterns/SKILL.md` exists with valid frontmatter (name, description)
- [ ] GHA patterns skill covers:
  - Reusable workflows (`workflow_call`) with inputs/outputs/secrets
  - Composite actions for shared steps
  - Matrix builds (`strategy.matrix`) with multi-TFM and multi-OS
  - Path-based triggers (`paths`, `paths-ignore`)
  - Concurrency groups for duplicate run cancellation
  - Environment protection rules
  - NuGet and SDK caching strategies (`actions/cache`)
  - `workflow_dispatch` inputs for manual triggers
- [ ] `skills/cicd/dotnet-gha-build-test/SKILL.md` exists with valid frontmatter
- [ ] GHA build-test skill covers:
  - `actions/setup-dotnet` v4 (multi-version, NuGet auth)
  - NuGet restore caching
  - `dotnet test` with result publishing (dorny/test-reporter or equivalent)
  - Code coverage upload (Codecov/Coveralls)
  - Multi-TFM matrix (net8.0, net9.0)
  - Test sharding for large projects
- [ ] `skills/cicd/dotnet-gha-publish/SKILL.md` exists with valid frontmatter
- [ ] GHA publish skill covers:
  - NuGet push to nuget.org and GitHub Packages
  - Container image build + push (GHCR, DockerHub, ACR)
  - Artifact signing
  - SBOM generation
  - Conditional publishing on tags/releases
- [ ] `skills/cicd/dotnet-gha-deploy/SKILL.md` exists with valid frontmatter
- [ ] GHA deploy skill covers:
  - GitHub Pages deployment for docs (Starlight/Docusaurus)
  - Container registry push patterns
  - Azure Web Apps via `azure/webapps-deploy`
  - GitHub Environments with protection rules
  - Rollback patterns
- [ ] All 4 skills cross-reference `[skill:dotnet-add-ci]` with scope boundary (starter vs depth)
- [ ] `dotnet-gha-publish` cross-references `[skill:dotnet-native-aot]` for AOT builds
- [ ] `dotnet-gha-publish` cross-references `[skill:dotnet-containers]` for container builds
- [ ] `dotnet-gha-patterns` cross-references `[skill:dotnet-cli-release-pipeline]` with scope boundary
- [ ] Each skill contains out-of-scope boundary statements
- [ ] Validation: `grep -q "^name:" skills/cicd/dotnet-gha-*/SKILL.md`
- [ ] Validation: `grep -q "^description:" skills/cicd/dotnet-gha-*/SKILL.md`

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
