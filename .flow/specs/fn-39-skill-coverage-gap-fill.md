# Skill Coverage Gap Fill

## Overview
Add identified missing skills from the gap analysis. Covers messaging/event-driven, System.IO.Pipelines, DDD/domain modeling, structured logging, LINQ optimization, GC/memory management, .NET Aspire patterns, and Semantic Kernel AI integration. These represent the coverage gaps not addressed by existing epics (fn-30 through fn-37).

**Note:** The original gap analysis identified middleware authoring as a gap, but review confirmed that the existing `dotnet-middleware-patterns` skill already covers IMiddleware vs convention-based, pipeline ordering, Map/MapWhen/UseWhen branching, body buffering, short-circuit, and exception handling comprehensively. That skill is dropped from this epic. The count is 8 new skills.

**Budget note:** Currently at ~12,458/15,000 chars with 113 skills. This epic adds 8 skills (~960 chars for descriptions at ~120 chars each). Projected total: ~13,418/15,000 chars. Target new skill descriptions at ~100 chars where possible to maintain headroom. Task fn-39.3 will validate actual budget and slim descriptions across ALL skills if needed.

## Scope

### New Skills (8 total)
1. **dotnet-messaging-patterns** (`skills/architecture/`) — Durable messaging: pub/sub, competing consumers, dead-letter queues, saga patterns, delivery guarantees. Azure Service Bus, RabbitMQ, MassTransit.
2. **dotnet-io-pipelines** (`skills/core-csharp/`) — System.IO.Pipelines: PipeReader/PipeWriter, backpressure, protocol parsing, Kestrel integration. Toub-grounded.
3. **dotnet-domain-modeling** (`skills/architecture/`) — DDD tactical patterns: aggregates, value objects, domain events, repository with EF Core/Dapper, rich vs anemic models.
4. **dotnet-structured-logging** (`skills/architecture/`) — Log pipeline design: aggregation architecture (ELK/Seq), structured query patterns, log sampling strategies, PII scrubbing/destructuring, cross-service correlation. **Distinct from** `dotnet-observability` which owns Serilog/MEL basics, source-generated LoggerMessage, enrichers, single-service scopes, and OTel logging export. This skill covers what happens _after_ log emission.
5. **dotnet-linq-optimization** (`skills/core-csharp/`) — IQueryable vs IEnumerable, compiled queries, deferred execution pitfalls, allocation patterns, Span alternatives.
6. **dotnet-gc-memory** (`skills/performance/`) — GC modes, LOH/POH, Gen0/1/2 tuning, Span/Memory deep patterns, ArrayPool/MemoryPool, memory profiling. Toub-grounded.
7. **dotnet-aspire-patterns** (`skills/architecture/`) — .NET Aspire orchestration: AppHost, service discovery, component model, dashboard, health checks. Distinct from container skills.
8. **dotnet-semantic-kernel** (`skills/ai/`) — Semantic Kernel for AI/LLM orchestration: kernel setup, plugins, prompt templates, memory/vector stores, agents. Placed under `ai/` category as a domain-specific capability distinct from architecture patterns.

### Dropped from original plan
- **dotnet-middleware-authoring** — Existing `dotnet-middleware-patterns` skill already covers all planned content (IMiddleware vs RequestDelegate, pipeline ordering/branching, body buffering, endpoint routing). No new skill needed.

## Design Constraints
- Each skill description under 120 characters (target ~100 chars for budget headroom)
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Use `[skill:skill-name]` cross-reference syntax
- All package version references use latest stable
- No fn-N spec references in content
- Skills must be self-contained
- SKILL.md content under 5,000 words per CONTRIBUTING-SKILLS.md
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
- [ ] All 8 new skills created with valid SKILL.md frontmatter
- [ ] All 8 skills registered in plugin.json
- [ ] All cross-references valid
- [ ] Description budget within 15,000 chars (or descriptions slimmed to fit)
- [ ] No fn-N spec references in any content
- [ ] All SKILL.md files under 5,000 words
- [ ] All four validation commands pass

## References
- Stephen Toub IO.Pipelines: https://devblogs.microsoft.com/dotnet/system-io-pipelines-high-performance-io-in-net/
- MassTransit: https://masstransit.io/
- Azure Service Bus patterns: https://learn.microsoft.com/en-us/azure/service-bus-messaging/
- Microsoft Semantic Kernel: https://learn.microsoft.com/en-us/semantic-kernel/
- .NET Aspire: https://learn.microsoft.com/en-us/dotnet/aspire/
