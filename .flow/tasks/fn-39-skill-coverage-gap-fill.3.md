# fn-39-skill-coverage-gap-fill.3 Register skills, update advisor catalog, and validate budget

## Description
Register all 9 new skills in `.claude-plugin/plugin.json`, update the dotnet-advisor catalog to route to them, and verify the total description budget remains within the 15,000-character limit.

**Size:** M
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `AGENTS.md`

## Approach
- Add all 9 new skill paths to the `skills` array in `.claude-plugin/plugin.json`:
  - `skills/architecture/dotnet-messaging-patterns`
  - `skills/core-csharp/dotnet-io-pipelines`
  - `skills/api-development/dotnet-middleware-authoring`
  - `skills/architecture/dotnet-domain-modeling`
  - `skills/architecture/dotnet-structured-logging`
  - `skills/core-csharp/dotnet-linq-optimization`
  - `skills/performance/dotnet-gc-memory`
  - `skills/architecture/dotnet-aspire-patterns`
  - `skills/architecture/dotnet-semantic-kernel`
- Update `dotnet-advisor` skill catalog with routing entries for all 9 skills
- Run `python3 scripts/generate_dist.py --strict` to verify budget: 9 skills x ~120 chars = ~1,080 chars
- If budget exceeds 15,000 after combining with fn-31-36 additions, slim descriptions across ALL skills to fit (target <100 chars each where possible)
- Run all four validation commands
- Verify all cross-references resolve
## Approach
- Add all 4 new skill paths to the `skills` array in `.claude-plugin/plugin.json`
- Update `dotnet-advisor` skill catalog with routing entries for messaging, IO.Pipelines, middleware, domain modeling
- Run `python3 scripts/generate_dist.py --strict` to verify budget: 4 new skills x ~120 chars = ~480 chars added
- If budget exceeds 15,000, flag which skills have descriptions that can be shortened
- Run all four validation commands
- Verify all cross-references resolve
## Acceptance
- [ ] All 9 new skills registered in `.claude-plugin/plugin.json`
- [ ] dotnet-advisor catalog updated with routing for all 9 new skills
- [ ] Total description budget within 15,000 chars (verified by generate_dist.py)
- [ ] If budget tight, descriptions slimmed across all skills to fit
- [ ] All cross-references resolve (validated by validate-skills.sh)
- [ ] All four validation commands pass
- [ ] No fn-N spec references in content
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
