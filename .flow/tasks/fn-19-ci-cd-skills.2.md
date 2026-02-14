# fn-19-ci-cd-skills.2 Create Azure DevOps skills (patterns, build-test, publish, unique features)

## Description
Create 4 Azure DevOps skills covering composable pipeline patterns, build/test pipelines, publishing pipelines, and ADO-unique features. These skills mirror the GHA skill structure where patterns overlap, while `dotnet-ado-unique` covers features exclusive to Azure DevOps.

**Files created:**
- `skills/cicd/dotnet-ado-patterns/SKILL.md`
- `skills/cicd/dotnet-ado-build-test/SKILL.md`
- `skills/cicd/dotnet-ado-publish/SKILL.md`
- `skills/cicd/dotnet-ado-unique/SKILL.md`

**Cross-references required:**
- `[skill:dotnet-native-aot]` (fn-16) for AOT publish pipelines in `dotnet-ado-publish`
- `[skill:dotnet-cli-release-pipeline]` (fn-17) scope boundary in `dotnet-ado-patterns`
- `[skill:dotnet-containers]` (fn-5) for container publish in `dotnet-ado-publish`
- `[skill:dotnet-add-ci]` (fn-4) scope boundary in `dotnet-ado-patterns`
- `[skill:dotnet-testing-strategy]` (fn-7) for test reporting context in `dotnet-ado-build-test`

All skills must have `name` and `description` frontmatter. Each skill must contain out-of-scope boundary statements. Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-19.3).

## Acceptance
- [ ] `skills/cicd/dotnet-ado-patterns/SKILL.md` exists with valid frontmatter (name, description)
- [ ] ADO patterns skill covers:
  - Template references (`extends`, `stages`, `jobs`, `steps`)
  - Variable groups and variable templates
  - Pipeline decorators
  - Conditional insertion (`${{ if }}`, `${{ each }}`)
  - Multi-stage pipelines (build → test → deploy)
  - Pipeline triggers (CI, PR, scheduled)
- [ ] `skills/cicd/dotnet-ado-build-test/SKILL.md` exists with valid frontmatter
- [ ] ADO build-test skill covers:
  - `DotNetCoreCLI@2` task (build, test, pack)
  - NuGet restore with Azure Artifacts feeds (`NuGetAuthenticate@1`)
  - Test result publishing (`PublishTestResults@2`)
  - Code coverage (`PublishCodeCoverageResults@2`)
  - Multi-TFM matrix strategy
- [ ] `skills/cicd/dotnet-ado-publish/SKILL.md` exists with valid frontmatter
- [ ] ADO publish skill covers:
  - NuGet push to Azure Artifacts and nuget.org
  - Container image build + push to ACR (`Docker@2`)
  - Artifact staging (`PublishBuildArtifacts@1` / `PublishPipelineArtifact@1`)
  - Pipeline artifacts for release pipelines
- [ ] `skills/cicd/dotnet-ado-unique/SKILL.md` exists with valid frontmatter
- [ ] ADO unique skill covers:
  - Environments with approvals and gates (pre-deployment checks, business hours)
  - Deployment groups vs environments (when to use each)
  - Service connections (Azure Resource Manager, Docker Registry, NuGet)
  - Classic release pipelines (legacy migration guidance to YAML)
  - Variable groups and library (linked to Azure Key Vault)
  - Pipeline decorators
  - Azure Artifacts universal packages
- [ ] All 4 skills cross-reference `[skill:dotnet-add-ci]` with scope boundary
- [ ] `dotnet-ado-publish` cross-references `[skill:dotnet-native-aot]` for AOT builds
- [ ] `dotnet-ado-publish` cross-references `[skill:dotnet-containers]` for container builds
- [ ] `dotnet-ado-patterns` cross-references `[skill:dotnet-cli-release-pipeline]` with scope boundary
- [ ] Each skill contains out-of-scope boundary statements
- [ ] Validation: `grep -q "^name:" skills/cicd/dotnet-ado-*/SKILL.md`
- [ ] Validation: `grep -q "^description:" skills/cicd/dotnet-ado-*/SKILL.md`

## Done summary
Created 4 Azure DevOps SKILL.md files (dotnet-ado-patterns, dotnet-ado-build-test, dotnet-ado-publish, dotnet-ado-unique) with comprehensive ADO pipeline examples, cross-references to dotnet-add-ci/dotnet-native-aot/dotnet-containers/dotnet-cli-release-pipeline, and out-of-scope boundary statements.
## Evidence
- Commits: aa1f12caf956e1b3e3a19ed1d6366d06e1b8e2e7, f90a475830b2318ef513ed014e044f7e424a7d24
- Tests: ./scripts/validate-skills.sh, grep -q '^name:' skills/cicd/dotnet-ado-*/SKILL.md, grep -q '^description:' skills/cicd/dotnet-ado-*/SKILL.md, grep -rh '^name:' skills/*/*/SKILL.md | sort | uniq -d
- PRs: