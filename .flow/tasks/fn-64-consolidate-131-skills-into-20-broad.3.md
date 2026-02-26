# fn-64-consolidate-131-skills-into-20-broad.3 Consolidate testing skills: dotnet-testing

## Description
Create consolidated `dotnet-api` skill directory. Merge ~28 ASP.NET Core, data access, security, and service skills into one skill with companion files. Remove source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-api/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~28 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: ASP.NET Core development overview, routing table, scope/out-of-scope, ToC
- Create `references/` dir. Expected companion files (per map from .1):
  - `references/minimal-apis.md` — endpoint design, filters, route groups
  - `references/middleware.md` — pipeline, custom middleware, request handling
  - `references/efcore.md` — patterns, architecture, data access strategy
  - `references/security.md` — OWASP, secrets management, cryptography, API security, input validation
  - `references/resilience.md` — Polly, HTTP client, retry, circuit breaker
  - `references/communication.md` — gRPC, SignalR, service communication
  - `references/architecture.md` — patterns, background services, domain modeling for services
  - `references/api-design.md` — versioning, OpenAPI, library compat, surface validation
  - `references/aspire.md` — .NET Aspire orchestration patterns
  - `references/semantic-kernel.md` — AI/LLM integration
  - (exact list per task .1 output)
- Remove old skill directories, update `plugin.json`

## Key context

- This is the second-largest consolidation (~28 source skills) but content is well-organized by sub-domain
- `dotnet-aspnetcore-specialist` agent preloads 7 individual skills from this group — will preload `dotnet-api` and read specific companion files
- Security skills (OWASP, secrets, crypto) fold here since API security is the primary use case
- `dotnet-security-reviewer` agent preloads security skills — will need companion file path references
## Approach

- Follow consolidation map from task .1
- SKILL.md: testing strategy overview, when to use which test type, scope/out-of-scope, ToC to companion files
- `references/xunit.md`, `references/integration-testing.md`, `references/snapshot-testing.md`, `references/playwright.md`, `references/test-quality.md` etc.
- Framework-specific testing content (bUnit, Appium, Playwright for Uno) stays with tasks .5

## Key context

- `dotnet-testing-specialist` agent preloads testing skills — will need updating in task .9
- Agent also delegates to framework-specific testing via Explicit Boundaries — those refs update in task .9
## Acceptance
- [ ] `skills/dotnet-api/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-api/references/` contains companion files from all merged source skills
- [ ] All ~28 source API/data/security skill directories deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter
- [ ] No content lost from source skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
