# fn-29-fleet-skill-review-and-improvement-sweep.4 Audit Batch C: Testing, CI/CD

## Description

Review all skills in: testing (10), cicd (8) — 18 skills total. Evaluate each against the 11-dimension rubric from `docs/fleet-review-rubric.md`. Produce findings report using the same structure as batch-a-findings.md (summary table, per-skill evaluations, cross-cutting observations, recommended changes).

### Files

- **Input:** All `SKILL.md` files under `skills/testing/`, `skills/cicd/`
- **Rubric:** `docs/fleet-review-rubric.md`
- **Reference template:** `docs/review-reports/batch-a-findings.md`
- **Output:** `docs/review-reports/batch-c-findings.md`

## Acceptance
- [ ] All 18 skills in batch evaluated against all 11 rubric dimensions
- [ ] Findings report at `docs/review-reports/batch-c-findings.md` follows batch-a-findings.md structure: Summary table (Skills reviewed, Clean, Needs Work, Critical), Current Description Budget Impact, per-skill sections (verdict + issues + proposed changes), cross-cutting observations, recommended changes
- [ ] Each skill has a pass/warn/fail rating per dimension with justification
- [ ] Cross-references validated (all `[skill:name]` refs point to existing skills)
- [ ] Description lengths measured and aggregate budget impact noted
- [ ] Issues tagged by severity: Critical (broken refs, budget violations), High, Low

## Done summary
Audited all 18 Batch C skills (10 testing, 8 CI/CD) against the 11-dimension fleet review rubric. Produced findings report at docs/review-reports/batch-c-findings.md with 1 Clean, 14 Needs Work, 3 Critical, and 23 total issues. Key findings: systematic bare cross-references across all CI/CD skills, 3 testing descriptions exceeding 140-char fail threshold, and xUnit v3 IAsyncLifetime inconsistency in dotnet-maui-testing.
## Evidence
- Commits: f263764a8b82705348e4a26c77a22d7b10da97a3
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: