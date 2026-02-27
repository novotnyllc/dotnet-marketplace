# fn-64.5 Consolidate dotnet-testing + dotnet-devops (30 source skills)
<!-- Updated by plan-sync: fn-64.1 mapped 12 testing + 18 devops = 30 total, not ~29 -->

## Description
Create consolidated `dotnet-testing` and `dotnet-devops` skill directories. Merge 12 testing skills and 18 DevOps skills into their respective directories with companion files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-testing/SKILL.md` + `references/*.md` (new), `skills/dotnet-devops/SKILL.md` + `references/*.md` (new), 30 source skill dirs (delete)

## Approach

**dotnet-testing (12 source skills):**
<!-- Updated by plan-sync: fn-64.1 mapped 12 source skills to dotnet-testing, not ~11 -->
- Write SKILL.md: testing strategy overview, when to use which test type, routing table, scope/out-of-scope, ToC
- Create `references/` dir with one companion file per source skill (12 files total, per consolidation map from .1):
  - `references/testing-strategy.md` — unit vs integration vs E2E decision tree, test doubles
  - `references/xunit.md` — xUnit v3 Facts, Theories, fixtures, parallelism, IAsyncLifetime
  - `references/integration-testing.md` — WebApplicationFactory, Testcontainers, Aspire, fixtures
  - `references/snapshot-testing.md` — Verify complex outputs, scrubbing non-deterministic values
  - `references/playwright.md` — Playwright E2E, CI browser caching, trace viewer, codegen
  - `references/benchmarkdotnet.md` — setup, memory diagnosers, baselines, result analysis
  - `references/ci-benchmarking.md` — automated threshold alerts, baseline tracking, trend reports
  - `references/test-quality.md` — Coverlet code coverage, Stryker.NET mutation testing, flaky tests
  - `references/add-testing.md` — scaffold xUnit project, coverlet, test layout
  - `references/slopwatch.md` — Slopwatch CLI for LLM reward hacking detection
  - `references/aot-wasm.md` — Blazor/Uno WASM AOT compilation, size vs speed, lazy loading
  - `references/ui-testing-core.md` — page objects, test selectors, async waits, accessibility

**dotnet-devops (18 source skills):**
- Write SKILL.md: CI/CD and operational concerns overview, routing table, scope/out-of-scope, ToC
- Create `references/` dir with one companion file per source skill (18 files total, per consolidation map from .1):
  - `references/gha-build-test.md` — GitHub Actions .NET build/test, setup-dotnet, NuGet cache
  - `references/gha-deploy.md` — deploy from GHA to Azure, GitHub Pages, container registries
  - `references/gha-publish.md` — NuGet push, container images, signing, SBOM from GHA
  - `references/gha-patterns.md` — reusable workflows, composite actions, matrix, caching
  - `references/ado-build-test.md` — Azure DevOps .NET build/test, DotNetCoreCLI task
  - `references/ado-publish.md` — NuGet push, containers to ACR from ADO
  - `references/ado-patterns.md` — YAML pipelines, templates, variable groups, multi-stage (merge existing examples.md)
  - `references/ado-unique.md` — environments, approvals, service connections, pipelines
  - `references/containers.md` — multi-stage Dockerfiles, SDK container publish, rootless
  - `references/container-deployment.md` — Compose, health probes, CI/CD image pipelines
  - `references/nuget-authoring.md` — SDK-style csproj, source generators, multi-TFM, symbols
  - `references/msix.md` — MSIX creation, signing, Store submission, sideload, auto-update
  - `references/github-releases.md` — release creation, assets, notes, pre-release management
  - `references/release-management.md` — NBGV versioning, SemVer, changelogs, branching
  - `references/observability.md` — OpenTelemetry traces/metrics/logs, health checks (merge existing examples.md)
  - `references/structured-logging.md` — aggregation, queries, sampling, PII scrubbing, correlation
  - `references/add-ci.md` — CI/CD scaffold, GitHub Actions vs Azure DevOps detection
  - `references/github-docs.md` — README badges, CONTRIBUTING, issue/PR templates
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- `dotnet-testing-specialist` agent preloads 5 testing skills — will preload `dotnet-testing` and read companion files
- Framework-specific testing (bUnit, Appium, Playwright for Uno) goes in `dotnet-ui` references (task .4), NOT here — add cross-reference in scope section
- `dotnet-cloud-specialist` agent preloads container and CI/CD skills — will preload `dotnet-devops`
- GHA and ADO skills mirror each other — separate companion files for discoverability

## Acceptance
- [ ] `skills/dotnet-testing/SKILL.md` + `references/` created with all testing content
- [ ] `skills/dotnet-devops/SKILL.md` + `references/` created with all DevOps content
- [ ] Framework-specific testing content NOT in dotnet-testing (it's in dotnet-ui per task .4)
- [ ] All 30 source testing/devops skill directories deleted (12 testing + 18 devops)
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter on both SKILL.md files
- [ ] No content lost from source skills

## Done summary
Consolidated 12 testing source skills into `skills/dotnet-testing/` with SKILL.md router + 12 companion files in `references/`. Follows the canonical dotnet-csharp pattern with baseline dependency callout, most-shared companion callout, routing table, scope/OOS, and companion index. All cross-references updated to the consolidated 8-skill namespace. Description is 117 chars (under 120 limit). Validator passes with exit code 0.

Note: This covers only the dotnet-testing half of task .5. The dotnet-devops consolidation (18 skills) is the remaining half and has NOT been started yet. Source skill directory deletion is also deferred.
## Evidence
- Commits: b6f7ea1 feat(skills): consolidate dotnet-testing (12 skills into 1 broad skill), 6d76f01 fix: address review feedback on dotnet-testing skill consolidation
- Tests: validate-skills.sh exits 0; no FAIL/ERROR for dotnet-testing, Zero stale cross-references remaining in skills/dotnet-testing/references/, RepoPrompt impl-review verdict: SHIP
- PRs: