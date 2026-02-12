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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
