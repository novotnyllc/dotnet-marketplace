# fn-29-fleet-skill-review-and-improvement-sweep.2 Audit Batch A: Foundation, Core C#, Project Structure

## Description

Review all skills in: foundation (4), core-csharp (9), project-structure (6), release-management (1) — 20 skills total. Evaluate each against the 11-dimension rubric from `docs/fleet-review-rubric.md`. Produce findings report.

### Files

- **Input:** All `SKILL.md` files under `skills/foundation/`, `skills/core-csharp/`, `skills/project-structure/`, `skills/release-management/`
- **Rubric:** `docs/fleet-review-rubric.md`
- **Output:** `docs/review-reports/batch-a-findings.md`

## Acceptance
- [ ] All 20 skills in batch evaluated against all 11 rubric dimensions
- [ ] Findings report at `docs/review-reports/batch-a-findings.md` uses the per-skill output template
- [ ] Each skill has a pass/warn/fail rating per dimension with justification
- [ ] Cross-references validated (all `[skill:name]` refs point to existing skills)
- [ ] Description lengths measured and aggregate budget impact noted

## Done summary
Audited all 20 Batch A skills (foundation/4, core-csharp/9, project-structure/6, release-management/1) against the 11-dimension rubric. Produced findings report at docs/review-reports/batch-a-findings.md with per-skill evaluations: Clean=11, Needs Work=6, Critical=3. Key findings: 3 descriptions over 140 chars (fail), 2 broken cross-refs in dotnet-advisor, 1 stale planned reference, 1 non-portable grep flag.
## Evidence
- Commits: ec40d55, ad9af29471e2dee3d151c5b1cf0828e1349d3247
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: