# fn-38-expert-domain-agents-and-luminary.5 Enrich existing agents with luminary-sourced knowledge

## Description
Enrich existing agents with luminary-sourced knowledge. Rather than creating new agents for every luminary, fold their expertise into the agents that already cover their domains.

**Size:** M
**Files:** `agents/dotnet-blazor-specialist.md`, `agents/dotnet-architect.md`, `agents/dotnet-performance-analyst.md`, `skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md`, `skills/core-csharp/dotnet-csharp-modern-patterns/SKILL.md`

## Approach
Luminaries mapped to existing agents:
- **Damian Edwards** (Razor/Blazor) → enrich `dotnet-blazor-specialist` with component design patterns, Blazor rendering guidance, Edwards' Razor patterns. Add Knowledge Sources section.
- **Steve Smith / Ardalis** (Clean Architecture, SOLID) → enrich `dotnet-architect` with Clean Architecture guidance, SOLID decision framework. Add Knowledge Sources section.
- **Mads Torgersen** (C# language design) → enrich `dotnet-csharp-coding-standards` and `dotnet-csharp-modern-patterns` skills with language design rationale references, NOT the concurrency specialist (Torgersen's expertise is language design broadly, not concurrency). C# Language Design Notes as source.
- **Andrew Lock** (ASP.NET Core config, middleware) → aspnetcore-specialist already has Knowledge Sources section citing Lock's blog (added in fn-38.2). Enrich decision tree entries in aspnetcore-specialist with Lock's configuration/host-builder patterns and enrich relevant middleware skills (`dotnet-middleware-patterns` is already a preloaded skill). Do NOT duplicate the existing Knowledge Sources entry.
<!-- Updated by plan-sync: fn-38.2 already added Andrew Lock Knowledge Sources to aspnetcore-specialist -->
- **Nick Chapsas** (modern .NET patterns, clean code) → attribution in relevant skills, not a separate agent
- **Jimmy Bogard** (MediatR, vertical slices, DDD patterns) → attribution in domain modeling and architecture skills. Note: MediatR is now commercial for commercial use.
- **Stephen Cleary** (async best practices) → enrich async-performance-specialist and async-patterns skill with Cleary's "Concurrency in C#" guidance

For each enrichment:
- Add "Knowledge Sources" section if not present
- Add relevant decision tree entries grounded in luminary guidance
- Do NOT rename agents or change their core scope
- Do NOT impersonate — use "grounded in guidance from" pattern
## Acceptance
- [ ] dotnet-blazor-specialist enriched with Damian Edwards component design patterns
- [ ] dotnet-architect enriched with Steve Smith/Ardalis Clean Architecture + SOLID guidance
- [ ] Mads Torgersen C# language design rationale referenced in `dotnet-csharp-coding-standards` and/or `dotnet-csharp-modern-patterns` skills
- [ ] Andrew Lock middleware/config guidance enriched in aspnetcore-specialist decision tree (Knowledge Sources entry already present from fn-38.2) and relevant middleware skills
- [ ] Jimmy Bogard DDD/vertical slice guidance attributed in domain modeling content
- [ ] Stephen Cleary async best practices referenced in async-related content
- [ ] All enrichments use "Knowledge Sources" sections with proper attribution
- [ ] No agents renamed or core scope changed
- [ ] All four validation commands pass
## Done summary
Enriched 5 existing agents and 6 skills with luminary-sourced Knowledge Sources sections covering 9 luminaries (Edwards, Smith/Ardalis, Torgersen, Lock, Bogard, Cleary, Chapsas, Toub, Fowler). Added actionable decision tree entries to aspnetcore-specialist (Lock config/host-builder patterns) and Edwards-grounded component design patterns to blazor-specialist. All enrichments use "grounded in guidance from" attribution pattern with disclaimers; no agents renamed or core scope changed.
## Evidence
- Commits: 42acfa4b5e6e9b8e20fc6e12e6dae8f5e29d23d5, 18b2f10a0ae8de6acb338c3a298ce49630d9fd51
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: