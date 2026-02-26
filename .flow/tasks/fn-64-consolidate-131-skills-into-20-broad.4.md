# fn-64-consolidate-131-skills-into-20-broad.4 Consolidate API and data skills: dotnet-api, dotnet-efcore

## Description
Create consolidated skill directories for API and data skills: `dotnet-api` and `dotnet-efcore`. Merge API-related skills (minimal-apis, api-versioning, openapi, api-security, input-validation, middleware-patterns, library-api-compat, api-surface-validation) and EF Core skills (efcore-patterns, efcore-architecture, data-access-strategy).

**Size:** M
**Files:** `skills/dotnet-api/SKILL.md` + `references/*.md` (new), `skills/dotnet-efcore/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~11 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- `dotnet-api` SKILL.md: ASP.NET Core API development overview, minimal APIs vs controllers, security, validation, versioning
- `dotnet-efcore` SKILL.md: EF Core patterns, architecture, data access strategy selection
- Include architecture-adjacent skills per mapping (architecture-patterns, resilience, http-client, etc. — exact placement from task .1)
## Acceptance
- [ ] `skills/dotnet-api/SKILL.md` + `references/` created with all merged API content
- [ ] `skills/dotnet-efcore/SKILL.md` + `references/` created with all merged data content
- [ ] All source skill directories for this batch deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on all SKILL.md files
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
