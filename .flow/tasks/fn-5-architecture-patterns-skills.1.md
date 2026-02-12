# fn-5-architecture-patterns-skills.1 Architecture patterns and background services skills

## Description
Create two architecture skills: `dotnet-architecture-patterns` (modern patterns for minimal API organization at scale, vertical slices, request pipeline, error handling, validation, caching strategy, idempotency/outbox guidance) and `dotnet-background-services` (BackgroundService, IHostedService, Channels-based producer/consumer, graceful shutdown).

## Acceptance
- [ ] `skills/architecture/dotnet-architecture-patterns/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/architecture/dotnet-background-services/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-architecture-patterns` covers vertical slices, minimal API organization, caching strategy, idempotency/outbox
- [ ] `dotnet-background-services` covers Channels-based producer/consumer, hosted service lifecycle, graceful shutdown
- [ ] Both skills cross-reference fn-3 skills using canonical IDs: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-dependency-injection]`
- [ ] Both skills contain out-of-scope boundary statements (DI/async → fn-3, scaffolding → fn-4)
- [ ] Skill `name` values are unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-5.6)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
