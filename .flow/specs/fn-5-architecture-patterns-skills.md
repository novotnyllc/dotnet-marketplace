# fn-5: Architecture Patterns Skills

## Overview
Delivers practical modern architecture patterns including minimal API organization, background services, resilience (Polly v8), HTTP client best practices, observability, data access, and container deployment.

## Scope
**Skills:**
- `dotnet-architecture-patterns` - Practical, modern patterns: minimal API organization, vertical slices, request pipeline, error handling, validation
- `dotnet-background-services` - BackgroundService, IHostedService, System.Threading.Channels for producer/consumer
- `dotnet-resilience` - Polly v8 + Microsoft.Extensions.Resilience + Microsoft.Extensions.Http.Resilience (the modern stack; supersedes Microsoft.Extensions.Http.Polly)
- `dotnet-http-client` - IHttpClientFactory + resilience pipelines: typed clients, named clients, DelegatingHandlers, testing
- `dotnet-observability` - OpenTelemetry (traces, metrics, logs), Serilog/MS.Extensions.Logging structured logging, health checks, custom metrics
- `dotnet-efcore-patterns` - EF Core best practices: DbContext lifecycle, AsNoTracking by default, query splitting, migrations, interceptors
- `dotnet-efcore-architecture` - EF Core architecture: separate read/write models, avoiding N+1, row limits, repository patterns
- `dotnet-data-access-strategy` - Choosing data access approach: EF Core vs Dapper vs raw ADO.NET, performance tradeoffs, AOT compat
- `dotnet-containers` - Container best practices: multi-stage Dockerfiles, `dotnet publish` container images (.NET 8+), rootless, health checks
- `dotnet-container-deployment` - Deploying .NET containers: Kubernetes basics, Docker Compose for local dev, CI/CD integration

## Key Context
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Microsoft.Extensions.Http.Polly is superseded by Microsoft.Extensions.Http.Resilience ([migration guide](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/resilience/migration-guide)) — do not use for new projects
- Polly v8.6.5 is the definitive standard (standard pipeline: rate limiter -> total timeout -> retry -> circuit breaker -> attempt timeout)
- Vertical slice architecture is increasingly mainstream
- OpenTelemetry is the standard observability approach in .NET 10

## Quick Commands
```bash
# Smoke test: verify resilience skill mentions superseded packages
grep -i "supersed\|migration" skills/architecture/dotnet-resilience.md

# Validate observability patterns
grep -i "OpenTelemetry" skills/architecture/dotnet-observability.md

# Test cross-references between HTTP client and resilience
grep -r "dotnet-resilience" skills/architecture/dotnet-http-client.md
```

## Acceptance Criteria
1. All 10 skills written with standard depth and frontmatter
2. Architecture patterns skill covers vertical slices, minimal API organization at scale
3. Background services skill documents channels-based patterns and hosted service lifecycle
4. Resilience skill recommends Polly v8 + MS.Extensions.Http.Resilience, notes Microsoft.Extensions.Http.Polly is superseded
5. HTTP client skill integrates resilience pipelines with typed/named clients
6. Observability skill covers OpenTelemetry setup for traces/metrics/logs plus structured logging
7. Skills reference ASP.NET Core best practices and async guidance
8. EF Core skills cover DbContext lifecycle, AsNoTracking, migrations, query splitting, N+1 prevention
9. Data access strategy skill provides clear decision framework for EF Core vs Dapper vs ADO.NET
10. Container skills cover multi-stage Dockerfiles, dotnet publish images, health checks, and basic K8s manifests

## Test Notes
- Verify resilience skill detects and warns about superseded Polly packages
- Test that HTTP client skill cross-references resilience for pipeline configuration
- Validate observability skill recommends OpenTelemetry over legacy approaches
- Verify EF Core skills cross-reference testing skills for integration testing with Testcontainers
- Verify container skills reference health check patterns from observability skill

## References
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Polly v8 documentation: https://www.pollydocs.org/
- OpenTelemetry .NET: https://opentelemetry.io/docs/languages/net/
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- EF Core Best Practices: https://learn.microsoft.com/en-us/ef/core/performance/
- .NET Container Images: https://learn.microsoft.com/en-us/dotnet/core/docker/build-container
