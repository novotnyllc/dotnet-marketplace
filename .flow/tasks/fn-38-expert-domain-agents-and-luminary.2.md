# fn-38-expert-domain-agents-and-luminary.2 Create dotnet-aspnetcore-specialist agent (Fowler-grounded)

## Description
Create `agents/dotnet-aspnetcore-specialist.md` — a domain-named agent for ASP.NET Core architecture, middleware, and backend design patterns, grounded in David Fowler's expertise.

**Size:** M
**Files:** `agents/dotnet-aspnetcore-specialist.md`, `.claude-plugin/plugin.json`

## Approach
- Follow agent frontmatter pattern from `agents/dotnet-csharp-concurrency-specialist.md`
- Agent name: `dotnet-aspnetcore-specialist` (domain name, NOT person name)
- Include "Knowledge Sources" section citing Fowler's AspNetCoreDiagnosticScenarios repo, Andrew Lock's middleware blog series, and official ASP.NET Core documentation
- Include disclaimer language
- Preloaded skills: `dotnet-minimal-apis`, `dotnet-api-security`, `dotnet-architecture-patterns`, `dotnet-resilience`, `dotnet-http-client`, `dotnet-csharp-dependency-injection`
- Decision tree covering: middleware vs endpoint filter, minimal APIs vs controllers, DI lifetime selection, request pipeline optimization, diagnostic scenario identification
- Explicit boundaries: "Does NOT handle Blazor/Razor (use blazor-specialist)", "Does NOT handle security auditing (use security-reviewer)", "Does NOT handle async performance internals (use async-performance-specialist)"
- Tools: Read, Grep, Glob, Bash (analysis only)
- Model: sonnet
- Keep under 3,000 tokens total
- Register in `.claude-plugin/plugin.json` agents array

## Key context
- David Fowler's AspNetCoreDiagnosticScenarios covers async guidance, middleware anti-patterns, DI pitfalls. The agent should distill these into decision rules.
- Andrew Lock's blog series "Exploring ASP.NET Core" provides deep middleware and configuration patterns.
- This agent complements dotnet-architect (which is a routing/architecture agent) by providing deep ASP.NET Core-specific analysis.
- Fowler also maintains dotnet-skillz Claude Code plugin — reference for patterns but adapt to our structure.
## Acceptance
- [ ] Agent file created at `agents/dotnet-aspnetcore-specialist.md`
- [ ] Frontmatter includes name, description, model (sonnet), capabilities, tools
- [ ] "Knowledge Sources" section cites Fowler's diagnostic scenarios, Lock's blog, official docs
- [ ] Disclaimer language included
- [ ] Decision tree covers middleware vs endpoint filter, minimal APIs vs controllers, DI lifetimes
- [ ] Explicit boundaries: no overlap with blazor-specialist, security-reviewer, async-performance-specialist
- [ ] Preloaded skills listed with `[skill:...]` cross-references
- [ ] Agent under 3,000 tokens
- [ ] Registered in `.claude-plugin/plugin.json` agents array
- [ ] All four validation commands pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
