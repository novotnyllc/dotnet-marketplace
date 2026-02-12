# fn-11-api-development-skills.1 Minimal APIs and versioning skills

## Description
Create the `dotnet-minimal-apis` and `dotnet-api-versioning` skills covering modern Minimal API development patterns and API versioning strategies. Update existing advisor catalog/routing entries and register in plugin.json.

**Size:** M
**Files:**
- `skills/api-development/dotnet-minimal-apis/SKILL.md` (new)
- `skills/api-development/dotnet-api-versioning/SKILL.md` (new)
- `.claude-plugin/plugin.json` (modify — ensure 2 skill paths present)
- `skills/foundation/dotnet-advisor/SKILL.md` (modify — update 2 existing catalog entries + routing)

## Approach
- Follow existing skill patterns at `skills/security/dotnet-security-owasp/SKILL.md` for structure and frontmatter conventions
- Use `[skill:...]` cross-reference syntax per fn-2 conventions
- Minimal APIs skill: route groups, endpoint filters, filter pipeline, OpenAPI 3.1, TypedResults, organization patterns (Carter, vertical slices). Cross-ref `[skill:dotnet-input-validation]` for validation, `[skill:dotnet-architecture-patterns]` for architectural patterns
- API versioning skill: URL segment versioning (preferred), header versioning, query string versioning. Use current `Asp.Versioning.Http` (minimal APIs) / `Asp.Versioning.Mvc` (controllers) package names; mention legacy `Microsoft.AspNetCore.Mvc.Versioning` only as migration context. Sunset headers.
- Update existing advisor catalog entries (lines 65-66) — fix versioning entry to use current package names (`Asp.Versioning.Http` / `Asp.Versioning.Mvc` instead of legacy `MS.AspNetCore.Mvc.Versioning`)
- Ensure both skills registered in plugin.json under `skills/api-development/` paths
- Verify no duplicate skill IDs in advisor after changes

## Key context
- Minimal APIs are Microsoft's official recommendation for new ASP.NET Core projects
- .NET 10 adds SSE, OpenAPI 3.1, and built-in validation to Minimal APIs
- Route groups are the preferred way to organize endpoints (replaces MapGet/MapPost chaining)
- Endpoint filter pipeline: IEndpointFilter for cross-cutting concerns (auth, validation, logging)
- TypedResults preferred over Results for OpenAPI metadata generation
- API versioning: `Asp.Versioning.Http` for Minimal APIs, `Asp.Versioning.Mvc` for controllers (current packages from https://github.com/dotnet/aspnet-api-versioning). Legacy `Microsoft.AspNetCore.Mvc.Versioning` is the predecessor.
- URL segment versioning (e.g., `/api/v1/`) is simplest and most widely adopted; header/query alternatives documented but URL preferred
- Existing advisor catalog entries at lines 65-66 and routing at lines 183-184 need updating, not duplicating
- Pitfall: ConfigureHttpJsonOptions applies to Minimal APIs only, not MVC controllers

## Acceptance
- [ ] Skill file exists at `skills/api-development/dotnet-minimal-apis/SKILL.md`
- [ ] Skill file exists at `skills/api-development/dotnet-api-versioning/SKILL.md`
- [ ] Both have frontmatter with `name` and `description` (under 120 chars each)
- [ ] Minimal APIs skill covers: route groups, endpoint filters, TypedResults, OpenAPI 3.1 integration, organization patterns for scale
- [ ] Minimal APIs skill references `[skill:dotnet-input-validation]` for validation depth
- [ ] Minimal APIs skill references `[skill:dotnet-architecture-patterns]` for architectural patterns
- [ ] API versioning skill uses current package names: `Asp.Versioning.Http` (minimal APIs), `Asp.Versioning.Mvc` (controllers)
- [ ] API versioning skill covers: URL versioning (preferred), header versioning, query string versioning, sunset policies
- [ ] Advisor catalog versioning entry updated from legacy `MS.AspNetCore.Mvc.Versioning` to `Asp.Versioning.Http` / `Asp.Versioning.Mvc`
- [ ] Both skills registered in `.claude-plugin/plugin.json` skills array
- [ ] No duplicate skill IDs in advisor catalog or routing sections
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created dotnet-minimal-apis skill (route groups, endpoint filters, TypedResults, OpenAPI 3.1, organization patterns) and dotnet-api-versioning skill (URL/header/query string versioning with Asp.Versioning.Http/Mvc, sunset policies). Updated advisor catalog entry and registered both in plugin.json.
## Evidence
- Commits: 574894e04e36e3a0dcd8bea94e38fb85dfb93bfc, 13ddff9eda28d17c48184d2defacc8809165967d
- Tests: ./scripts/validate-skills.sh
- PRs: