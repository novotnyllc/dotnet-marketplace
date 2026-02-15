# Expert Domain Agents and Luminary Attribution

## Overview
Create domain-named specialist agents grounded in the expertise of prominent .NET luminaries (Stephen Toub, David Fowler, Damian Edwards, Steve Smith, Mads Torgersen, Andrew Lock, Jimmy Bogard, Stephen Cleary, Nick Chapsas). Add source attribution to existing skills and agents. All agents are named by domain, not by person — following Anthropic's usage policy and community best practices.

**Key principle:** Capture expertise, not persona. Agents are "grounded in guidance from" — they do not claim to represent or speak for any individual.

## Scope

### New Agents (5 total)
1. **dotnet-async-performance-specialist** — Deep async/await and runtime performance analysis. Grounded in Stephen Toub's .NET performance blog series, ConfigureAwait FAQ, and async internals guidance. Covers: ValueTask correctness, ConfigureAwait decisions, async overhead detection, ThreadPool tuning, IO.Pipelines patterns, Channel selection.
2. **dotnet-aspnetcore-specialist** — ASP.NET Core architecture, middleware, and backend patterns. Grounded in David Fowler's AspNetCoreDiagnosticScenarios and Andrew Lock's middleware blog series. Covers: middleware authoring, DI anti-patterns, minimal API design, request pipeline optimization, diagnostic scenarios.
3. **dotnet-testing-specialist** — Test architecture and strategy. Covers: test pyramid design, E2E architecture, test data management, microservice testing, when to use integration vs unit vs E2E.
4. **dotnet-cloud-specialist** — Cloud deployment and .NET Aspire orchestration. Covers: AKS/Azure deployment, GitHub Actions pipelines, Aspire service discovery, distributed tracing, infrastructure-as-code.
5. **dotnet-code-review-agent** — General code review combining performance, security, architecture, and correctness. Routes to specialist agents for deep dives.

### Existing Agent Enrichment
- **dotnet-blazor-specialist** ← Damian Edwards (Razor/Blazor component design patterns)
- **dotnet-architect** ← Steve Smith/Ardalis (Clean Architecture, SOLID decision framework)
- **dotnet-csharp-concurrency-specialist** ← Mads Torgersen (C# language design rationale)
- **dotnet-performance-analyst** ← Stephen Cleary async patterns, Nick Chapsas modern .NET patterns
- Architecture/domain skills ← Jimmy Bogard (DDD, vertical slices; note MediatR is commercial)

### Luminary Attribution on Skills
Add "Knowledge Sources" or "References" sections to 6+ existing skills citing authoritative luminary sources.

### Routing Updates
- Update `dotnet-advisor` catalog to route to all new agents
- Update `AGENTS.md` delegation table with new agent triggers and boundaries

## Design Constraints
- Agent names are domain-based, NEVER person-based
- Each agent includes a "Knowledge Sources" section listing luminaries as sources, with disclaimer
- Agent descriptions include "grounded in [source]" language
- Agents use read-only tools (Read, Grep, Glob, Bash) — analysis only
- Each agent < 3,000 tokens for composability
- Follow frontmatter pattern from `agents/dotnet-csharp-concurrency-specialist.md`
- Budget impact: 0 chars for agents (agents are separate from skill description budget)

## Quick commands
```bash
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] 5 new domain-named agents created (async-performance, aspnetcore, testing, cloud, code-review)
- [ ] All new agents follow frontmatter pattern with Knowledge Sources and disclaimer
- [ ] 4+ existing agents enriched with luminary-sourced knowledge
- [ ] 7 luminaries covered: Toub, Fowler, Edwards, Smith, Torgersen, Lock, Cleary (plus Bogard, Chapsas via attribution)
- [ ] Attribution references added to 6+ existing skills
- [ ] dotnet-advisor catalog updated with all new agent routing
- [ ] AGENTS.md updated with all new agent entries
- [ ] No agent named after a person
- [ ] All agents under 3,000 tokens
- [ ] All four validation commands pass
- [ ] No fn-N spec references in any content

## References
- `agents/dotnet-csharp-concurrency-specialist.md` — template for agent frontmatter and structure
- `agents/dotnet-performance-analyst.md` — template for analysis agent workflow
- `CONTRIBUTING.md:69-104` — agent authoring conventions
- `AGENTS.md:32-64` — agent delegation table
- Stephen Toub's .NET Performance Blog: https://devblogs.microsoft.com/dotnet/author/toub/
- Stephen Toub's ConfigureAwait FAQ: https://devblogs.microsoft.com/dotnet/configureawait-faq/
- David Fowler's AspNetCoreDiagnosticScenarios: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios
- Andrew Lock's blog: https://andrewlock.net/
- Steve Smith/Ardalis Clean Architecture: https://github.com/ardalis/CleanArchitecture
- Anthropic Usage Policy (impersonation prohibition): https://www.anthropic.com/legal/aup
