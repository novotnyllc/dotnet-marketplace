# fn-5: Architecture Patterns Skills

## Overview
Delivers practical modern architecture patterns including minimal API organization, background services, resilience (Polly v8), HTTP client best practices, observability, EF Core data access, and container deployment. These are **architecture-focused** skills that teach patterns and best practices. DI/async patterns live in fn-3; project scaffolding in fn-4; deep CI/CD in fn-19; deep testing in fn-7.

## Scope
**Skills (10 total):**
- `dotnet-architecture-patterns` — Practical, modern patterns: minimal API organization at scale, vertical slices, request pipeline, error handling, validation, caching strategy, idempotency/outbox guidance
- `dotnet-background-services` — BackgroundService, IHostedService, System.Threading.Channels for producer/consumer, graceful shutdown
- `dotnet-resilience` — Polly v8 + Microsoft.Extensions.Resilience + Microsoft.Extensions.Http.Resilience (the modern stack; supersedes Microsoft.Extensions.Http.Polly)
- `dotnet-http-client` — IHttpClientFactory + resilience pipelines: typed clients, named clients, DelegatingHandlers, testing
- `dotnet-observability` — OpenTelemetry (traces, metrics, logs), Serilog/MS.Extensions.Logging structured logging, health checks, custom metrics
- `dotnet-efcore-patterns` — EF Core tactical patterns: DbContext lifecycle, AsNoTracking by default, query splitting, migrations, interceptors
- `dotnet-efcore-architecture` — EF Core strategic patterns: separate read/write models, aggregate boundaries, repository policy, N+1 governance, row limits
- `dotnet-data-access-strategy` — Choosing data access approach: EF Core vs Dapper vs raw ADO.NET, performance tradeoffs, AOT compatibility
- `dotnet-containers` — Container best practices: multi-stage Dockerfiles, `dotnet publish` container images (.NET 8+), rootless, health checks
- `dotnet-container-deployment` — Deploying .NET containers: Kubernetes basics (Deployment + Service + probe YAML), Docker Compose for local dev, CI/CD integration

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills.

## Scope Boundaries

| Concern | fn-5 owns (architecture patterns) | Other epic owns (depth) | Enforcement |
|---|---|---|---|
| DI / async | Cross-references `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-dependency-injection]` | fn-3: owns DI and async patterns | Each skill must contain cross-ref; grep validates |
| Project scaffolding | Cross-references `[skill:dotnet-scaffold-project]` | fn-4: owns scaffolding skills | Grep validates cross-ref presence |
| CI/CD | Container CI integration only | fn-19: composable workflows, matrix builds, deploy pipelines | Container skills must state "advanced CI patterns → fn-19" |
| Testing | Deferred cross-refs to fn-7 skills (`dotnet-integration-testing`, `dotnet-snapshot-testing`) — added when fn-7 lands | fn-7: owns testing strategies and frameworks | Placeholder comments in EF Core/observability skills; fn-7 reconciliation task replaces placeholders with canonical IDs |
| Version upgrades | N/A | fn-10: migration paths, polyfill strategies, multi-targeting | N/A |

## Task Decomposition

### fn-5.1: Architecture patterns and background services skills (parallelizable)
**Delivers:** `dotnet-architecture-patterns`, `dotnet-background-services`
- `skills/architecture/dotnet-architecture-patterns/SKILL.md`
- `skills/architecture/dotnet-background-services/SKILL.md`
- Both require `name` and `description` frontmatter
- Does NOT touch `plugin.json` (handled by fn-5.6)

### fn-5.2: Resilience and HTTP client skills (parallelizable)
**Delivers:** `dotnet-resilience`, `dotnet-http-client`
- `skills/architecture/dotnet-resilience/SKILL.md`
- `skills/architecture/dotnet-http-client/SKILL.md`
- Does NOT touch `plugin.json` (handled by fn-5.6)

### fn-5.3: Observability skill (parallelizable)
**Delivers:** `dotnet-observability`
- `skills/architecture/dotnet-observability/SKILL.md`
- Does NOT touch `plugin.json` (handled by fn-5.6)

### fn-5.4: Data access skills (parallelizable)
**Delivers:** `dotnet-efcore-patterns`, `dotnet-efcore-architecture`, `dotnet-data-access-strategy`
- `skills/architecture/dotnet-efcore-patterns/SKILL.md`
- `skills/architecture/dotnet-efcore-architecture/SKILL.md`
- `skills/architecture/dotnet-data-access-strategy/SKILL.md`
- `dotnet-efcore-patterns` = tactical: DbContext, queries, migrations, interceptors
- `dotnet-efcore-architecture` = strategic: read/write split, aggregate boundaries, repository policy, N+1 governance
- `dotnet-data-access-strategy` provides clear decision framework for EF Core vs Dapper vs ADO.NET
- Does NOT touch `plugin.json` (handled by fn-5.6)

### fn-5.5: Container skills (parallelizable)
**Delivers:** `dotnet-containers`, `dotnet-container-deployment`
- `skills/architecture/dotnet-containers/SKILL.md`
- `skills/architecture/dotnet-container-deployment/SKILL.md`
- `dotnet-containers` covers multi-stage Dockerfiles, dotnet publish images, rootless, health checks
- `dotnet-container-deployment` covers Kubernetes Deployment + Service + probe YAML, Docker Compose, CI/CD integration
- Cross-references `[skill:dotnet-observability]` for health check patterns
- Does NOT touch `plugin.json` (handled by fn-5.6)

### fn-5.6: Integration — plugin registration, validation, and cross-reference audit (depends on fn-5.1–fn-5.5)
**Delivers:** Plugin registration and validation for all 10 skills
- Registers all 10 skill paths in `.claude-plugin/plugin.json`
- Runs repo-wide AND catalog-level uniqueness check on skill `name` frontmatter (validates against existing `skills/*/*/SKILL.md` names and marketplace naming conventions)
- Runs `./scripts/validate-skills.sh`
- Validates boundary cross-references are present in each skill
- Validates "out-of-scope" statements for fn-3 (DI/async), fn-4 (scaffolding), fn-7 (testing), fn-19 (CI/CD)
- Verifies deferred fn-7 testing cross-ref placeholders are present
- Single owner of `plugin.json` — eliminates merge conflicts

**fn-7 Reconciliation:** When fn-7 lands, a follow-up task must replace deferred placeholder comments with canonical `[skill:...]` cross-references and validate via grep. This reconciliation is tracked as a dependency note in fn-7's spec.

## Key Context
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Microsoft.Extensions.Http.Polly is superseded by Microsoft.Extensions.Http.Resilience ([migration guide](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/resilience/migration-guide)) — do not use for new projects
- Polly v8.6.5 is the definitive standard (standard pipeline: rate limiter -> total timeout -> retry -> circuit breaker -> attempt timeout)
- Vertical slice architecture is increasingly mainstream
- OpenTelemetry is the standard observability approach in .NET 10

## Quick Commands
```bash
# Validate all 10 skills exist with frontmatter
for s in dotnet-architecture-patterns dotnet-background-services dotnet-resilience dotnet-http-client dotnet-observability dotnet-efcore-patterns dotnet-efcore-architecture dotnet-data-access-strategy dotnet-containers dotnet-container-deployment; do
  test -f "skills/architecture/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate frontmatter has required fields (name AND description)
for s in skills/architecture/*/SKILL.md; do
  grep -q "^name:" "$s" && grep -q "^description:" "$s" && echo "OK: $s" || echo "MISSING FRONTMATTER: $s"
done

# Repo-wide skill name uniqueness check (all skills across all categories)
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty (no duplicates)

# Canonical frontmatter validation (single command)
./scripts/validate-skills.sh

# Verify resilience skill mentions superseded packages
grep -i "supersed\|migration" skills/architecture/dotnet-resilience/SKILL.md

# Verify cross-references use canonical fn-3 IDs
grep -r "\[skill:dotnet-csharp-async-patterns\]" skills/architecture/
grep -r "\[skill:dotnet-csharp-dependency-injection\]" skills/architecture/

# Verify boundary cross-references
grep -r "\[skill:dotnet-resilience\]" skills/architecture/dotnet-http-client/SKILL.md
grep -r "\[skill:dotnet-observability\]" skills/architecture/dotnet-container-deployment/SKILL.md

# Verify out-of-scope statements
grep -l "fn-3\|DI patterns\|async patterns" skills/architecture/*/SKILL.md | wc -l  # expect >= 2
grep -l "fn-7\|testing patterns" skills/architecture/*/SKILL.md | wc -l  # expect >= 2

# Verify deferred fn-7 placeholders exist
grep -rl "TODO.*fn-7\|placeholder.*fn-7\|deferred.*fn-7" skills/architecture/*/SKILL.md | wc -l  # expect >= 3
```

## Acceptance Criteria
1. All 10 skills exist at `skills/architecture/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. Architecture patterns skill covers vertical slices, minimal API organization at scale, caching strategy, idempotency/outbox guidance
3. Background services skill documents Channels-based producer/consumer patterns, hosted service lifecycle, and graceful shutdown
4. Resilience skill recommends Polly v8 + MS.Extensions.Http.Resilience, explicitly notes Microsoft.Extensions.Http.Polly is superseded
5. HTTP client skill integrates resilience pipelines with typed/named clients, cross-references `[skill:dotnet-resilience]`
6. Observability skill covers OpenTelemetry setup for traces/metrics/logs plus structured logging
7. EF Core patterns skill covers DbContext lifecycle, AsNoTracking, migrations, query splitting, interceptors (tactical)
8. EF Core architecture skill covers read/write split, aggregate boundaries, repository policy, N+1 governance (strategic)
9. Data access strategy skill provides clear decision framework for EF Core vs Dapper vs ADO.NET with AOT compatibility notes
10. Container skills cover multi-stage Dockerfiles, dotnet publish images, health checks, and Kubernetes Deployment + Service + probe YAML
11. Skills cross-reference fn-3 skills using canonical IDs (`dotnet-csharp-async-patterns`, `dotnet-csharp-dependency-injection`) — not re-teach
12. Each skill contains explicit out-of-scope boundary statements for related epics (fn-3 DI/async, fn-4 scaffolding, fn-7 testing, fn-19 CI/CD) where applicable
13. All 10 skills registered in `.claude-plugin/plugin.json` (single integration task fn-5.6)
14. `./scripts/validate-skills.sh` passes for all 10 skills
15. Skill `name` frontmatter values are unique repo-wide (no duplicates across all `skills/*/*/SKILL.md`)
16. Testing cross-refs to fn-7 skills are deferred (placeholder comments, non-blocking) with reconciliation tracked
17. Tasks fn-5.1–fn-5.5 are fully parallelizable (file-disjoint, no shared file edits)

## Test Notes
- Verify resilience skill detects and warns about superseded Polly packages
- Test that HTTP client skill cross-references resilience for pipeline configuration
- Validate observability skill recommends OpenTelemetry over legacy approaches
- Verify container deployment skill includes Kubernetes Deployment + Service + probe YAML examples
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide
- Verify boundary cross-references use canonical fn-3 IDs (not shorthand)
- Verify out-of-scope boundary statements are present where applicable
- Verify deferred fn-7 placeholder comments exist in EF Core and observability skills
- Verify `plugin.json` contains all 10 architecture skill paths after fn-5.6

## References
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Polly v8 documentation: https://www.pollydocs.org/
- OpenTelemetry .NET: https://opentelemetry.io/docs/languages/net/
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- EF Core Best Practices: https://learn.microsoft.com/en-us/ef/core/performance/
- .NET Container Images: https://learn.microsoft.com/en-us/dotnet/core/docker/build-container
