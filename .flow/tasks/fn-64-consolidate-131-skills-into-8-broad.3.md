# fn-64.3 Consolidate dotnet-api (~28 source skills)

## Description
Create consolidated `dotnet-api` skill directory. Merge ~28 ASP.NET Core, data access, security, and service skills into one skill with companion files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-api/SKILL.md` + `references/*.md` (new), ~28 source skill dirs (delete)

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
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- This is the second-largest consolidation (~28 source skills) but content is well-organized by sub-domain
- `dotnet-aspnetcore-specialist` agent preloads 7 individual skills from this group — will preload `dotnet-api` and read specific companion files
- Security skills (OWASP, secrets, crypto) fold here since API security is the primary use case
- `dotnet-security-reviewer` agent preloads security skills — will need companion file path references

## Acceptance
- [ ] `skills/dotnet-api/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-api/references/` contains companion files from all merged source skills
- [ ] All ~28 source API/data/security skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter
- [ ] No content lost from source skills

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
