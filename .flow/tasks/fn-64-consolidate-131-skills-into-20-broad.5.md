# fn-64-consolidate-131-skills-into-20-broad.5 Consolidate UI framework skills: dotnet-blazor, dotnet-uno, dotnet-maui, dotnet-desktop

## Description
Create consolidated `dotnet-testing` and `dotnet-devops` skill directories. Merge ~11 testing skills and ~18 DevOps skills into their respective directories with companion files. Remove source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-testing/SKILL.md` + `references/*.md` (new), `skills/dotnet-devops/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~29 source skill dirs (delete)

## Approach

**dotnet-testing (~11 source skills):**
- Write SKILL.md: testing strategy overview, when to use which test type, routing table, scope/out-of-scope, ToC
- Create `references/` dir. Expected companion files:
  - `references/xunit.md` — xUnit v3, Fact/Theory, fixtures, assertions
  - `references/integration-testing.md` — WebApplicationFactory, Testcontainers
  - `references/snapshot-testing.md` — Verify patterns
  - `references/playwright.md` — browser testing, page objects
  - `references/ui-testing-core.md` — cross-framework UI testing patterns
  - `references/benchmarkdotnet.md` — microbenchmark design, CI benchmarking
  - `references/test-quality.md` — coverage, CRAP analysis, mutation testing
  - (exact list per task .1 output)

**dotnet-devops (~18 source skills):**
- Write SKILL.md: CI/CD and operational concerns overview, routing table, scope/out-of-scope, ToC
- Create `references/` dir. Expected companion files:
  - `references/gha-patterns.md` — GitHub Actions workflows, build/test/publish/deploy
  - `references/ado-patterns.md` — Azure DevOps YAML pipelines, build/test/publish, ADO-specific features
  - `references/containers.md` — Dockerfiles, multi-stage builds, container deployment, Kubernetes
  - `references/packaging.md` — NuGet authoring, MSIX, GitHub Releases, release management
  - `references/observability.md` — OpenTelemetry, structured logging, metrics, health endpoints
  - (exact list per task .1 output)

## Key context

- `dotnet-testing-specialist` agent preloads 5 testing skills — will preload `dotnet-testing` and read companion files
- Framework-specific testing (bUnit, Appium, Playwright for Uno) goes in `dotnet-ui` references, NOT here — add cross-reference in scope section
- `dotnet-cloud-specialist` agent preloads container and CI/CD skills — will preload `dotnet-devops`
- GHA and ADO skills mirror each other — separate companion files for discoverability
## Approach

- Follow consolidation map from task .1
- `dotnet-blazor` merges: blazor-patterns, blazor-components, blazor-auth, blazor-testing
- `dotnet-uno` merges: uno-platform, uno-targets, uno-mcp, uno-testing
- `dotnet-maui` merges: maui-development, maui-aot, maui-testing
- `dotnet-desktop` merges: winui, wpf-modern, wpf-migration, winforms-basics, accessibility, ui-chooser
- Framework-testing content goes in `references/testing.md` within each UI skill

## Key context

- `dotnet-uno-mcp` is special: it queries Uno MCP server. Its content becomes `references/mcp.md` inside `dotnet-uno`
- `dotnet-ui-chooser` is a router skill (decision tree); place inside `dotnet-desktop` or keep standalone per task .1 mapping
- `dotnet-accessibility` is cross-cutting; placement per task .1 mapping
## Acceptance
- [ ] `skills/dotnet-testing/SKILL.md` + `references/` created with all testing content
- [ ] `skills/dotnet-devops/SKILL.md` + `references/` created with all DevOps content
- [ ] Framework-specific testing content NOT in dotnet-testing (it's in dotnet-ui per task .4)
- [ ] All ~29 source testing/devops skill directories deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on both SKILL.md files
- [ ] No content lost from source skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
