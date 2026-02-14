# fn-19: CI/CD Skills

## Overview
Delivers comprehensive CI/CD skills for GitHub Actions and Azure DevOps covering composable patterns, build/test/publish workflows, deployment patterns, and platform-unique features. These are **depth skills** that go beyond the starter templates in `[skill:dotnet-add-ci]` (fn-4). Support both platforms equally with reusable, composable patterns. CLI-specific release pipelines are owned by fn-17 (`[skill:dotnet-cli-release-pipeline]`); fn-19 owns general CI/CD patterns.

## Scope
**Skills (8 total):**
- `dotnet-gha-patterns` — Composable GitHub Actions: reusable workflows (`workflow_call`), composite actions, matrix builds, path-based triggers, concurrency groups, environment protection rules, caching strategies (NuGet, SDK), workflow_dispatch inputs
- `dotnet-gha-build-test` — .NET build + test workflows: `actions/setup-dotnet`, NuGet restore caching, `dotnet test` with result publishing (dorny/test-reporter), code coverage upload (Codecov/Coveralls), multi-TFM matrix, test sharding for large projects
- `dotnet-gha-publish` — Publishing workflows: NuGet push to nuget.org and GitHub Packages, container image build + push to GHCR/DockerHub/ACR, artifact signing with NuGet signing, SBOM generation, conditional publishing on tags/releases
- `dotnet-gha-deploy` — Deployment patterns: GitHub Pages for docs (Starlight/Docusaurus), container registry push, Azure Web Apps via `azure/webapps-deploy`, AWS/GCP deploy actions, GitHub Environments with protection rules, rollback patterns
- `dotnet-ado-patterns` — Composable Azure DevOps YAML: template references (`extends`, `stages`), variable groups and templates, pipeline decorators, conditional insertion, multi-stage pipelines, pipeline triggers (CI/PR/scheduled)
- `dotnet-ado-build-test` — ADO build + test pipelines: `DotNetCoreCLI@2` task, NuGet restore with Azure Artifacts feeds, test result publishing (`PublishTestResults@2`), code coverage (`PublishCodeCoverageResults@2`), multi-TFM matrix strategy
- `dotnet-ado-publish` — ADO publishing pipelines: NuGet push to Azure Artifacts and nuget.org, container image build + push to ACR (`Docker@2`), artifact staging (`PublishBuildArtifacts@1`), pipeline artifacts for release pipelines
- `dotnet-ado-unique` — ADO-specific features not in GHA: Environments with approvals and gates, deployment groups vs environments, service connections (Azure, Docker, NuGet), classic release pipelines (legacy migration guidance), variable groups and library, pipeline decorators, Azure Artifacts universal packages

**Agents:** None for this epic. CI/CD guidance is delivered through skills only. The `dotnet-architect` agent can load CI/CD skills contextually via `[skill:dotnet-gha-*]` or `[skill:dotnet-ado-*]` references.

**Naming convention:** All skills use `dotnet-` prefix. `gha` = GitHub Actions, `ado` = Azure DevOps. Noun style for reference skills.

## Dependencies

**Hard epic dependencies:**
- fn-16 (Native AOT): `[skill:dotnet-native-aot]` must exist for AOT build workflow cross-refs in publish skills
- fn-17 (CLI Tools): `[skill:dotnet-cli-release-pipeline]` must exist for scope boundary cross-refs

**Soft epic dependencies:**
- fn-18 (Performance): `[skill:dotnet-ci-benchmarking]` has deferred `<!-- TODO(fn-19) -->` placeholders to resolve — fn-19.3 reconciliation
- fn-5 (Architecture): `[skill:dotnet-containers]`, `[skill:dotnet-container-deployment]` for container build/deploy cross-refs — already shipped
- fn-11 (API Development): `[skill:dotnet-minimal-apis]` for API deployment context — already shipped
- fn-4 (Project Structure): `[skill:dotnet-add-ci]` provides starter templates; fn-19 skills extend with depth

## .NET Version Policy

**Baseline:** .NET 8.0+ (LTS, mainstream CI support)

| Component | Version | Notes |
|-----------|---------|-------|
| GitHub Actions `setup-dotnet` | v4 | Supports .NET 8/9/10, multi-version install, NuGet auth |
| ADO `DotNetCoreCLI@2` | Current | Built-in .NET task, supports custom SDK versions |
| Container publish | .NET 8+ | SDK container builds (`dotnet publish` with `PublishContainer`) |
| Native AOT CI | .NET 8+ | AOT publish in CI pipelines |
| SBOM generation | .NET 8+ | `dotnet sbom` tool or Microsoft SBOM action |

## Conventions

- **Frontmatter:** Required fields are `name` and `description` only
- **Cross-reference syntax:** `[skill:skill-name]` for all skill references
- **Description budget:** Target < 120 characters per skill description
- **Out-of-scope format:** "**Out of scope:**" paragraph with epic ownership attribution
- **Code examples:** Platform-specific YAML (GitHub Actions or ADO YAML)
- **Platform parity:** Both platforms supported equally — no bias toward either

## Scope Boundaries

| Concern | fn-19 owns | Other epic owns | Enforcement |
|---------|-----------|-----------------|-------------|
| CLI release pipeline | General GHA/ADO CI patterns used by CLI pipelines | fn-17: `dotnet-cli-release-pipeline` (CLI-specific build→package→release) | Cross-ref `[skill:dotnet-cli-release-pipeline]`; no re-teach CLI packaging |
| Benchmark CI workflows | General CI workflow patterns for benchmarking | fn-18: `dotnet-ci-benchmarking` (benchmark-specific integration) | Resolve `<!-- TODO(fn-19) -->` placeholders with canonical `[skill:dotnet-gha-patterns]` cross-refs |
| Container build/push | GHA/ADO container build + registry push workflows | fn-5: `dotnet-containers` (Dockerfile, SDK containers), `dotnet-container-deployment` (orchestration) | Cross-ref `[skill:dotnet-containers]`; no re-teach Dockerfile/SDK container setup |
| AOT build in CI | CI pipeline configuration for AOT publish step | fn-16: `dotnet-native-aot` (AOT MSBuild properties, ILLink) | Cross-ref `[skill:dotnet-native-aot]`; no re-teach AOT config |
| API deployment | GHA/ADO deploy workflows for web apps | fn-11: API-level concerns (routing, versioning, security) | Cross-ref where relevant; fn-19 owns the deployment pipeline |
| Starter CI templates | Advanced/composable CI patterns | fn-4: `dotnet-add-ci` (starter templates for basic build/test/pack) | `dotnet-add-ci` scope boundary already points to fn-19 |
| Test result publishing | CI test reporting and coverage upload | fn-7/fn-8: testing strategy and quality | Cross-ref test skills; fn-19 owns CI pipeline integration |

## Cross-Reference Classification

| Target Skill | Type | Used By | Notes |
|---|---|---|---|
| `[skill:dotnet-native-aot]` | Hard | `dotnet-gha-publish`, `dotnet-ado-publish` | AOT publish step in CI |
| `[skill:dotnet-cli-release-pipeline]` | Hard | `dotnet-gha-patterns`, `dotnet-ado-patterns` | Scope boundary |
| `[skill:dotnet-containers]` | Soft | `dotnet-gha-publish`, `dotnet-ado-publish` | Container build context |
| `[skill:dotnet-container-deployment]` | Soft | `dotnet-gha-deploy` | Container deploy context |
| `[skill:dotnet-ci-benchmarking]` | Soft | `dotnet-gha-patterns` | Benchmark CI cross-ref |
| `[skill:dotnet-add-ci]` | Soft | `dotnet-gha-patterns`, `dotnet-ado-patterns` | Starter template context |
| `[skill:dotnet-testing-strategy]` | Soft | `dotnet-gha-build-test`, `dotnet-ado-build-test` | Test reporting context |

## Task Decomposition

### fn-19.1: Create GitHub Actions skills (patterns, build-test, publish, deploy) — parallelizable with fn-19.2
**Delivers:** `dotnet-gha-patterns`, `dotnet-gha-build-test`, `dotnet-gha-publish`, `dotnet-gha-deploy`
- `skills/cicd/dotnet-gha-patterns/SKILL.md`
- `skills/cicd/dotnet-gha-build-test/SKILL.md`
- `skills/cicd/dotnet-gha-publish/SKILL.md`
- `skills/cicd/dotnet-gha-deploy/SKILL.md`
- All require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-native-aot]` (fn-16) for AOT publish workflows
  - `[skill:dotnet-cli-release-pipeline]` (fn-17) scope boundary
  - `[skill:dotnet-containers]` (fn-5) for container publish workflows
  - `[skill:dotnet-ci-benchmarking]` (fn-18) for benchmark CI integration
  - `[skill:dotnet-add-ci]` (fn-4) scope boundary (starter vs depth)
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-19.3)

### fn-19.2: Create Azure DevOps skills (patterns, build-test, publish, unique features) — parallelizable with fn-19.1
**Delivers:** `dotnet-ado-patterns`, `dotnet-ado-build-test`, `dotnet-ado-publish`, `dotnet-ado-unique`
- `skills/cicd/dotnet-ado-patterns/SKILL.md`
- `skills/cicd/dotnet-ado-build-test/SKILL.md`
- `skills/cicd/dotnet-ado-publish/SKILL.md`
- `skills/cicd/dotnet-ado-unique/SKILL.md`
- All require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-native-aot]` (fn-16) for AOT publish pipelines
  - `[skill:dotnet-cli-release-pipeline]` (fn-17) scope boundary
  - `[skill:dotnet-containers]` (fn-5) for container publish pipelines
  - `[skill:dotnet-add-ci]` (fn-4) scope boundary (starter vs depth)
- `dotnet-ado-unique` must cover: Environments with approvals/gates, deployment groups, service connections, classic release pipelines (migration), variable groups, pipeline decorators, Azure Artifacts
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-19.3)

### fn-19.3: Integration — plugin registration, advisor catalog, validation, cross-reference reconciliation (depends on fn-19.1, fn-19.2)
**Delivers:** Plugin registration, advisor update, cross-reference reconciliation, validation
- Registers all 8 skill paths in `.claude-plugin/plugin.json` under `skills` array
- Updates `skills/foundation/dotnet-advisor/SKILL.md` section 17 (CI/CD) from `planned` to `implemented`
- **fn-18 reconciliation:** Replace all `<!-- TODO(fn-19) -->` placeholders in `skills/performance/dotnet-ci-benchmarking/SKILL.md` with canonical `[skill:dotnet-gha-patterns]` cross-references (5 placeholders at lines 16, 104, 226, 389, 503)
- **Existing fn-19 references:** Update bare "fn-19" mentions in other skills to canonical `[skill:dotnet-gha-*]` / `[skill:dotnet-ado-*]` cross-refs where appropriate
- Runs repo-wide skill name uniqueness check
- Runs `./scripts/validate-skills.sh`
- Validates cross-references present in all 8 skills
- Single owner of `plugin.json` — eliminates merge conflicts

**Execution order:** fn-19.1 and fn-19.2 are parallelizable (file-disjoint, no shared file edits). fn-19.3 depends on both fn-19.1 and fn-19.2.

## Key Context
- GitHub Actions and Azure DevOps are the two dominant CI/CD platforms for .NET development
- Both platforms support YAML-based pipeline definitions with composability features
- GitHub Actions: reusable workflows (`workflow_call`), composite actions, environment protection rules
- Azure DevOps: template expressions (`extends`, `each`), Environments with approvals/gates, classic release pipelines (legacy), service connections, Azure Artifacts
- ADO has unique features with no GHA equivalent: deployment groups, pipeline decorators, variable groups (linked to Azure Key Vault), classic release management
- `dotnet-add-ci` (fn-4) provides starter templates; fn-19 skills provide composable depth patterns
- fn-17's `dotnet-cli-release-pipeline` is CLI-specific; fn-19 covers general .NET CI/CD
- fn-18's `dotnet-ci-benchmarking` has 5 deferred `<!-- TODO(fn-19) -->` placeholders referencing `dotnet-github-actions` — fn-19.3 must update these to canonical `[skill:dotnet-gha-patterns]` since the actual skill name differs
- Multiple existing skills reference "fn-19" in out-of-scope statements — fn-19.3 should update canonical ones to `[skill:...]` syntax
- `actions/setup-dotnet` v4 supports .NET 8/9/10, multi-version installs, and NuGet auth configuration
- SDK container builds (`dotnet publish` with container support) reduce Dockerfile maintenance

## Quick Commands
```bash
# Validate all 8 skills exist with frontmatter
for s in dotnet-gha-patterns dotnet-gha-build-test dotnet-gha-publish dotnet-gha-deploy \
         dotnet-ado-patterns dotnet-ado-build-test dotnet-ado-publish dotnet-ado-unique; do
  test -f "skills/cicd/$s/SKILL.md" && \
  grep -q "^name:" "skills/cicd/$s/SKILL.md" && \
  grep -q "^description:" "skills/cicd/$s/SKILL.md" && \
  echo "OK: $s" || echo "MISSING: $s"
done

# Repo-wide skill name uniqueness
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Verify fn-18 deferred placeholders resolved (after fn-19.3)
grep -r "TODO(fn-19)" skills/performance/  # expect empty after fn-19.3

# Verify scope boundary statements in all 8 skills
grep -l "Out of scope\|out of scope\|Scope boundary" skills/cicd/*/SKILL.md | wc -l  # expect 8

# Verify cross-references
grep -r "\[skill:dotnet-native-aot\]" skills/cicd/
grep -r "\[skill:dotnet-cli-release-pipeline\]" skills/cicd/
grep -r "\[skill:dotnet-ci-benchmarking\]" skills/cicd/
grep -r "\[skill:dotnet-containers\]" skills/cicd/
grep -r "\[skill:dotnet-add-ci\]" skills/cicd/

# Verify plugin.json registration (after fn-19.3)
for s in dotnet-gha-patterns dotnet-gha-build-test dotnet-gha-publish dotnet-gha-deploy \
         dotnet-ado-patterns dotnet-ado-build-test dotnet-ado-publish dotnet-ado-unique; do
  grep -q "skills/cicd/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify advisor section 17 updated (after fn-19.3)
grep "### 17. CI/CD" skills/foundation/dotnet-advisor/SKILL.md | grep -v "planned"

# Canonical validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 8 skills exist at `skills/cicd/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-gha-patterns` covers reusable workflows (`workflow_call`), composite actions, matrix builds, path-based triggers, concurrency groups, environment protection rules, caching strategies
3. `dotnet-gha-build-test` covers `actions/setup-dotnet` v4, NuGet restore caching, `dotnet test` with result publishing, code coverage upload, multi-TFM matrix
4. `dotnet-gha-publish` covers NuGet push (nuget.org + GitHub Packages), container image push (GHCR/DockerHub/ACR), artifact signing, SBOM generation, conditional publish on tags
5. `dotnet-gha-deploy` covers GitHub Pages, container registries, Azure Web Apps, GitHub Environments with protection rules, rollback patterns
6. `dotnet-ado-patterns` covers template references (`extends`, `stages`), variable groups/templates, pipeline decorators, multi-stage pipelines, CI/PR/scheduled triggers
7. `dotnet-ado-build-test` covers `DotNetCoreCLI@2`, Azure Artifacts feed restore, test result publishing, code coverage, multi-TFM matrix
8. `dotnet-ado-publish` covers NuGet push to Azure Artifacts and nuget.org, container push to ACR, artifact staging, pipeline artifacts
9. `dotnet-ado-unique` covers Environments with approvals/gates, deployment groups, service connections, classic release pipelines (migration), variable groups, pipeline decorators, Azure Artifacts universal packages
10. GHA publish and ADO publish skills cross-reference `[skill:dotnet-native-aot]` for AOT publish workflows — do not re-teach AOT config
11. GHA and ADO pattern skills cross-reference `[skill:dotnet-cli-release-pipeline]` with scope boundary statement
12. GHA and ADO build-test skills reference `[skill:dotnet-ci-benchmarking]` for benchmark CI integration
13. GHA and ADO publish skills cross-reference `[skill:dotnet-containers]` for container build context — do not re-teach Dockerfile
14. Each skill contains explicit out-of-scope boundary statements for related epics
15. All 8 skills registered in `.claude-plugin/plugin.json` (fn-19.3)
16. `skills/foundation/dotnet-advisor/SKILL.md` section 17 updated from `planned` to `implemented` (fn-19.3)
17. All `<!-- TODO(fn-19) -->` placeholders in `skills/performance/dotnet-ci-benchmarking/SKILL.md` replaced with canonical `[skill:dotnet-gha-patterns]` cross-refs (fn-19.3)
18. `./scripts/validate-skills.sh` passes for all 8 skills
19. Skill `name` frontmatter values are unique repo-wide (no duplicates)
20. fn-19.1 and fn-19.2 are fully parallelizable (file-disjoint, no shared file edits)
21. fn-19.3 depends on fn-19.1 + fn-19.2 and is the single owner of `plugin.json`

## Test Notes
- Verify GHA pattern skill includes actual reusable workflow YAML example
- Verify ADO pattern skill includes actual pipeline template YAML example
- Verify GHA/ADO build-test skills include multi-TFM matrix YAML examples
- Verify GHA/ADO publish skills include container push and NuGet push YAML examples
- Verify `dotnet-ado-unique` covers ADO-exclusive features not available in GHA
- Verify scope boundary statements clearly differentiate fn-19 from fn-4 (starter), fn-17 (CLI), fn-18 (benchmarks)
- Verify fn-18 `dotnet-ci-benchmarking` TODO placeholders reference `dotnet-gha-patterns` (not `dotnet-github-actions`)
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide

## References
- GitHub Actions: https://docs.github.com/en/actions
- Reusable workflows: https://docs.github.com/en/actions/using-workflows/reusing-workflows
- Composite actions: https://docs.github.com/en/actions/sharing-automations/creating-actions/creating-a-composite-action
- actions/setup-dotnet: https://github.com/actions/setup-dotnet
- Azure Pipelines YAML: https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema
- ADO Environments: https://learn.microsoft.com/en-us/azure/devops/pipelines/process/environments
- ADO Template expressions: https://learn.microsoft.com/en-us/azure/devops/pipelines/process/templates
- .NET CI best practices: https://learn.microsoft.com/en-us/dotnet/devops/dotnet-build-github-actions
- SDK container builds: https://learn.microsoft.com/en-us/dotnet/core/docker/publish-as-container
