# fn-5-architecture-patterns-skills.4 Data access skills

## Description
Create three data access skills: `dotnet-efcore-patterns` (tactical: DbContext lifecycle, AsNoTracking, query splitting, migrations, interceptors), `dotnet-efcore-architecture` (strategic: read/write split, aggregate boundaries, repository policy, N+1 governance, row limits), and `dotnet-data-access-strategy` (decision framework for EF Core vs Dapper vs ADO.NET with AOT compatibility).

## Acceptance
- [ ] `skills/architecture/dotnet-efcore-patterns/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/architecture/dotnet-efcore-architecture/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/architecture/dotnet-data-access-strategy/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-efcore-patterns` covers DbContext lifecycle, AsNoTracking, query splitting, migrations, interceptors (tactical)
- [ ] `dotnet-efcore-architecture` covers read/write split, aggregate boundaries, repository policy, N+1 governance (strategic)
- [ ] `dotnet-data-access-strategy` provides EF Core vs Dapper vs ADO.NET decision framework with AOT compatibility
- [ ] EF Core skills contain deferred fn-7 testing cross-ref placeholders (non-blocking)
- [ ] All skills contain out-of-scope boundary statements where applicable
- [ ] Skill `name` values are unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-5.6)

## Done summary
Created three data access skills: dotnet-efcore-patterns (tactical EF Core patterns covering DbContext lifecycle, AsNoTracking, query splitting, migrations, interceptors, compiled queries, connection resiliency), dotnet-efcore-architecture (strategic patterns covering read/write split, aggregate boundaries, repository policy, N+1 governance, row limits, projections), and dotnet-data-access-strategy (decision framework for EF Core vs Dapper vs ADO.NET with performance tradeoffs, AOT compatibility, and hybrid approaches).
## Evidence
- Commits: 8404cf2, cbc4a35, fc47dc5
- Tests: frontmatter validation (name+description), repo-wide skill name uniqueness check, fn-7 placeholder grep, out-of-scope boundary grep, canonical fn-3 cross-ref grep
- PRs: