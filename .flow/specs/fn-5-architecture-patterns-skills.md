# fn-5: Architecture Patterns Skills

## Overview
Delivers practical modern architecture patterns including minimal API organization, background services, resilience (Polly v8), HTTP client best practices, and observability.

## Scope
**Skills:**
- `dotnet-architecture-patterns` - Practical, modern patterns: minimal API organization, vertical slices, request pipeline, error handling, validation
- `dotnet-background-services` - BackgroundService, IHostedService, System.Threading.Channels for producer/consumer
- `dotnet-resilience` - Polly v8 + Microsoft.Extensions.Resilience + Microsoft.Extensions.Http.Resilience (NOT Microsoft.Extensions.Http.Polly - deprecated)
- `dotnet-http-client` - IHttpClientFactory + resilience pipelines: typed clients, named clients, DelegatingHandlers, testing
- `dotnet-observability` - OpenTelemetry (traces, metrics, logs), Serilog/MS.Extensions.Logging structured logging, health checks, custom metrics

## Key Context
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Microsoft.Extensions.Http.Polly is DEPRECATED - use Microsoft.Extensions.Http.Resilience
- Polly v8.6.5 is the definitive standard (standard pipeline: rate limiter -> total timeout -> retry -> circuit breaker -> attempt timeout)
- Vertical slice architecture is increasingly mainstream
- OpenTelemetry is the standard observability approach in .NET 10

## Quick Commands
```bash
# Smoke test: verify resilience skill warns about deprecated packages
grep -i "deprecated" skills/architecture/dotnet-resilience.md

# Validate observability patterns
grep -i "OpenTelemetry" skills/architecture/dotnet-observability.md

# Test cross-references between HTTP client and resilience
grep -r "dotnet-resilience" skills/architecture/dotnet-http-client.md
```

## Acceptance Criteria
1. All 5 skills written with standard depth and frontmatter
2. Architecture patterns skill covers vertical slices, minimal API organization at scale
3. Background services skill documents channels-based patterns and hosted service lifecycle
4. Resilience skill explicitly warns against Microsoft.Extensions.Http.Polly, recommends Polly v8 + MS.Extensions.Http.Resilience
5. HTTP client skill integrates resilience pipelines with typed/named clients
6. Observability skill covers OpenTelemetry setup for traces/metrics/logs plus structured logging
7. Skills reference ASP.NET Core best practices and async guidance

## Test Notes
- Verify resilience skill detects and warns about deprecated Polly packages
- Test that HTTP client skill cross-references resilience for pipeline configuration
- Validate observability skill recommends OpenTelemetry over legacy approaches

## References
- ASP.NET Core Best Practices: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0
- Polly v8 documentation: https://www.pollydocs.org/
- OpenTelemetry .NET: https://opentelemetry.io/docs/languages/net/
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
