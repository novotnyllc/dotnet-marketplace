# fn-39-skill-coverage-gap-fill.3 Register skills, update advisor catalog, and validate budget

## Description
Register all 8 new skills in `.claude-plugin/plugin.json`, update the dotnet-advisor catalog to route to them, and verify the total description budget remains within the 15,000-character limit. Currently at 113 skills; this adds 8 for a total of 121.

**Size:** M
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `AGENTS.md`

## Approach
- Add all 8 new skill paths to the `skills` array in `.claude-plugin/plugin.json`:
  - `skills/architecture/dotnet-messaging-patterns`
  - `skills/core-csharp/dotnet-io-pipelines`
  - `skills/architecture/dotnet-domain-modeling` (NOTE: description is 124 chars, 4 over limit — will need trim in this task)
  - `skills/architecture/dotnet-structured-logging`
  - `skills/core-csharp/dotnet-linq-optimization`
  - `skills/performance/dotnet-gc-memory`
  - `skills/architecture/dotnet-aspire-patterns`
  - `skills/ai/dotnet-semantic-kernel`
- Update `dotnet-advisor` skill catalog with routing entries for all 8 skills (follow the existing routing entry format in `skills/foundation/dotnet-advisor/SKILL.md`)
- Run `./scripts/validate-skills.sh` first to get actual `CURRENT_DESC_CHARS` before deciding on slimming
- Budget math: 121 skills × 120 chars = 14,520 chars (under 15,000 but only 480 chars headroom). dotnet-domain-modeling description is 4 chars over at 124 — trim to 120 chars. If actual budget exceeds 15,000, slim descriptions across ALL skills (target ~100 chars each where possible)
- Run all four validation commands
- Verify all cross-references resolve
<!-- Updated by plan-sync: fn-39-skill-coverage-gap-fill.2 description is 124 chars, not 120 as required -->
## Acceptance
- [ ] All 8 new skills registered in `.claude-plugin/plugin.json`
- [ ] dotnet-advisor catalog updated with routing for all 8 new skills
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
