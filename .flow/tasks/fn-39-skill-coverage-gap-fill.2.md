# fn-39-skill-coverage-gap-fill.2 Create dotnet-middleware-authoring and dotnet-domain-modeling skills

## Description
Create two new skills covering middleware and domain modeling gaps:

1. **dotnet-middleware-authoring** (`skills/api-development/dotnet-middleware-authoring/SKILL.md`) — ASP.NET Core middleware authoring patterns (IMiddleware vs RequestDelegate, pipeline ordering, branching with Map/MapWhen/UseWhen, endpoint routing integration, request/response buffering).
2. **dotnet-domain-modeling** (`skills/architecture/dotnet-domain-modeling/SKILL.md`) — DDD tactical patterns in C# (aggregate roots, entities, value objects, domain events, integration events, repository pattern with EF Core and Dapper, rich vs anemic domain models).

**Size:** M
**Files:** `skills/api-development/dotnet-middleware-authoring/SKILL.md`, `skills/architecture/dotnet-domain-modeling/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Each description under 120 characters
- dotnet-middleware-authoring cross-refs: `[skill:dotnet-minimal-apis]`, `[skill:dotnet-api-security]`, `[skill:dotnet-csharp-dependency-injection]`
- dotnet-middleware-authoring should reference Fowler's AspNetCoreDiagnosticScenarios and Lock's middleware blog as sources
- dotnet-domain-modeling cross-refs: `[skill:dotnet-efcore-patterns]`, `[skill:dotnet-architecture-patterns]`, `[skill:dotnet-efcore-architecture]`
- Use latest stable package versions
- No fn-N spec references in content
## Acceptance
- [ ] dotnet-middleware-authoring SKILL.md created with frontmatter
- [ ] Covers IMiddleware vs inline, pipeline ordering, branching, endpoint routing
- [ ] dotnet-domain-modeling SKILL.md created with frontmatter
- [ ] Covers aggregates, value objects, domain events, repository pattern
- [ ] Cross-references to related skills use `[skill:...]` syntax
- [ ] Both descriptions under 120 characters
- [ ] No fn-N spec references in content
- [ ] Package versions are latest stable
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
