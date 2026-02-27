# fn-64.3 Consolidate dotnet-api (27 source skills)
<!-- Updated by plan-sync: fn-64.1 mapped 27 source skills to dotnet-api, not ~28 -->

## Description
Create consolidated `dotnet-api` skill directory. Merge 27 ASP.NET Core, data access, security, and service skills into one skill with companion files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-api/SKILL.md` + `references/*.md` (new), 27 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: ASP.NET Core development overview, routing table, scope/out-of-scope, ToC
- Create `references/` dir with one companion file per source skill (27 files total, per consolidation map from .1):
  - `references/minimal-apis.md` — endpoint design, filters, route groups, TypedResults
  - `references/middleware-patterns.md` — pipeline ordering, short-circuit, exception handling
  - `references/efcore-patterns.md` — DbContext, AsNoTracking, query splitting
  - `references/efcore-architecture.md` — read/write split, aggregate boundaries, N+1
  - `references/data-access-strategy.md` — EF Core vs Dapper vs ADO.NET decision matrix
  - `references/grpc.md` — proto, code-gen, streaming, auth (merge existing examples.md)
  - `references/realtime-communication.md` — SignalR, SSE, JSON-RPC, gRPC streaming
  - `references/resilience.md` — Polly v8, retry, circuit breaker, timeout
  - `references/http-client.md` — IHttpClientFactory, typed/named, DelegatingHandler
  - `references/api-versioning.md` — Asp.Versioning, URL/header/query, sunset
  - `references/openapi.md` — MS.AspNetCore.OpenApi, Swashbuckle, NSwag
  - `references/api-security.md` — Identity, OAuth/OIDC, JWT, CORS, rate limiting
  - `references/security-owasp.md` — OWASP Top 10 hardening for .NET
  - `references/secrets-management.md` — user secrets, env vars, rotation
  - `references/cryptography.md` — AES-GCM, RSA, ECDSA, hashing, key derivation
  - `references/background-services.md` — BackgroundService, IHostedService, lifecycle
  - `references/aspire-patterns.md` — AppHost, service discovery, components, dashboard
  - `references/semantic-kernel.md` — AI/LLM plugins, prompts, memory, agents
  - `references/architecture-patterns.md` — vertical slices, layered, pipelines, caching (merge existing examples.md)
  - `references/messaging-patterns.md` — MassTransit, Azure Service Bus, pub/sub, sagas
  - `references/service-communication.md` — REST vs gRPC vs SignalR decision matrix
  - `references/api-surface-validation.md` — PublicApiAnalyzers, Verify, ApiCompat
  - `references/library-api-compat.md` — binary/source compat, type forwarders, SemVer
  - `references/io-pipelines.md` — PipeReader/PipeWriter, backpressure, Kestrel
  - `references/agent-gotchas.md` — common agent mistakes in .NET code
  - `references/file-based-apps.md` — .NET 10, directives, csproj migration
  - `references/api-docs.md` — DocFX, OpenAPI-as-docs, versioned documentation
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- This is the second-largest consolidation (27 source skills) but content is well-organized by sub-domain
- `dotnet-aspnetcore-specialist` agent preloads 7 individual skills from this group — will preload `dotnet-api` and read specific companion files
- Security skills (OWASP, secrets, crypto) fold here since API security is the primary use case
- `dotnet-security-reviewer` agent preloads security skills — will need companion file path references

## Acceptance
- [ ] `skills/dotnet-api/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-api/references/` contains companion files from all merged source skills
- [ ] All 27 source API/data/security skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter
- [ ] No content lost from source skills

## Done summary
Consolidated 27 ASP.NET Core source skills into skills/dotnet-api with SKILL.md (routing table, scope, companion files ToC) and 27 companion reference files. Merged existing examples.md into grpc.md and architecture-patterns.md. Deleted all 27 source skill directories.
## Evidence
- Commits: c96b1ebae66b8c8cb8703167b83a8ee78a8ba10d
- Tests: ./scripts/validate-skills.sh
- PRs: