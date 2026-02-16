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
- **Andrew Lock** (ASP.NET Core config, middleware) → fold into the new `dotnet-aspnetcore-specialist` and relevant middleware skills. Blog series as source.
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
- [ ] Andrew Lock middleware/config guidance folded into aspnetcore-specialist and skills
- [ ] Jimmy Bogard DDD/vertical slice guidance attributed in domain modeling content
- [ ] Stephen Cleary async best practices referenced in async-related content
- [ ] All enrichments use "Knowledge Sources" sections with proper attribution
- [ ] No agents renamed or core scope changed
- [ ] All four validation commands pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
