# Skill Coverage Gap Fill

## Overview
Add all identified missing skills from the gap analysis. Covers messaging/event-driven, System.IO.Pipelines, middleware authoring, DDD/domain modeling, structured logging, LINQ optimization, GC/memory management, .NET Aspire patterns, and Semantic Kernel AI integration. These represent the coverage gaps not addressed by existing epics (fn-30 through fn-37).

**Budget note:** Currently at 12,458/15,000 chars with 101 skills. This epic adds 9 skills (~1,080 chars). If combined with fn-31-36 additions the budget may be tight — the registration task (fn-39.3) will slim descriptions across all skills if needed to stay within 15,000 chars.

## Scope

### New Skills (9 total)
1. **dotnet-messaging-patterns** (`skills/architecture/`) — Durable messaging: pub/sub, competing consumers, dead-letter queues, saga patterns, delivery guarantees. Azure Service Bus, RabbitMQ, MassTransit.
2. **dotnet-io-pipelines** (`skills/core-csharp/`) — System.IO.Pipelines: PipeReader/PipeWriter, backpressure, protocol parsing, Kestrel integration. Toub-grounded.
3. **dotnet-middleware-authoring** (`skills/api-development/`) — IMiddleware vs RequestDelegate, pipeline ordering/branching, endpoint routing, body buffering. Fowler/Lock-grounded.
4. **dotnet-domain-modeling** (`skills/architecture/`) — DDD tactical patterns: aggregates, value objects, domain events, repository with EF Core/Dapper, rich vs anemic models.
5. **dotnet-structured-logging** (`skills/architecture/`) — Serilog vs NLog vs MEL, enrichers, correlation IDs, semantic logging, sink configuration. Distinct from observability skill.
6. **dotnet-linq-optimization** (`skills/core-csharp/`) — IQueryable vs IEnumerable, compiled queries, deferred execution pitfalls, allocation patterns, Span alternatives.
7. **dotnet-gc-memory** (`skills/performance/`) — GC modes, LOH/POH, Gen0/1/2 tuning, Span/Memory deep patterns, ArrayPool/MemoryPool, memory profiling. Toub-grounded.
8. **dotnet-aspire-patterns** (`skills/architecture/`) — .NET Aspire orchestration: AppHost, service discovery, component model, dashboard, health checks. Distinct from container skills.
9. **dotnet-semantic-kernel** (`skills/architecture/`) — Semantic Kernel for AI/LLM orchestration: kernel setup, plugins, prompt templates, memory/vector stores, agents.

## Design Constraints
- Each skill description under 120 characters
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Use `[skill:skill-name]` cross-reference syntax
- All package version references use latest stable
- No fn-N spec references in content
- Skills must be self-contained
- Register all new skills in `.claude-plugin/plugin.json`
- If total budget exceeds 15,000 chars, slim descriptions across ALL skills (not just new ones)

## Quick commands
```bash
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] All 9 new skills created with valid SKILL.md frontmatter
- [ ] All 9 skills registered in plugin.json
- [ ] All cross-references valid
- [ ] Description budget within 15,000 chars (or descriptions slimmed to fit)
- [ ] No fn-N spec references in any content
- [ ] All four validation commands pass

## References
- Stephen Toub IO.Pipelines: https://devblogs.microsoft.com/dotnet/system-io-pipelines-high-performance-io-in-net/
- David Fowler AspNetCoreDiagnosticScenarios: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios
- MassTransit: https://masstransit.io/
- Azure Service Bus patterns: https://learn.microsoft.com/en-us/azure/service-bus-messaging/
- Microsoft Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/
- .NET Aspire: https://learn.microsoft.com/en-us/dotnet/aspire/
