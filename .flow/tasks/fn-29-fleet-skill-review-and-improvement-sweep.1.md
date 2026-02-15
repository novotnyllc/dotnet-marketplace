# fn-29-fleet-skill-review-and-improvement-sweep.1 Create review rubric and coordination plan

## Description

Produce `docs/fleet-review-rubric.md` containing the evaluation rubric (11 dimensions), scoring guidance (pass/warn/fail per dimension), per-skill output template (structured markdown), category batch assignments with accurate counts (99 skills across 18 categories), and self-contained worker agent instructions.

The 11 rubric dimensions are: Description Quality, Description Triggering, Instruction Clarity, Progressive Disclosure, Cross-References, Error Handling, Examples, Composability, Consistency, Registration & Budget, Progressive Disclosure Compliance.

### Files

- **Output:** `docs/fleet-review-rubric.md`
- **Input refs:** `CONTRIBUTING-SKILLS.md`, `CLAUDE.md`, `.claude-plugin/plugin.json`

## Acceptance
- [ ] `docs/fleet-review-rubric.md` exists with all 11 rubric dimensions and scoring guidance
- [ ] Per-skill output template uses structured markdown with pass/warn/fail per dimension
- [ ] Category batch assignments match actual plugin.json skill count (99)
- [ ] Worker agent instructions are self-contained (agent needs only rubric + CONTRIBUTING-SKILLS.md)
- [ ] Run `./scripts/validate-skills.sh` to baseline current state

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
