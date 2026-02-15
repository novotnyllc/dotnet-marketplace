# fn-29-fleet-skill-review-and-improvement-sweep.7 Audit Batch F: Documentation, Packaging, Localization

## Description

Review all skills in: documentation (5), packaging (3), localization (1) — 9 skills total. Evaluate each against the 11-dimension rubric from `docs/fleet-review-rubric.md`. Produce findings report using the same structure as batch-a-findings.md (summary table, per-skill evaluations, cross-cutting observations, recommended changes).

### Files

- **Input:** All `SKILL.md` files under `skills/documentation/`, `skills/packaging/`, `skills/localization/`
- **Rubric:** `docs/fleet-review-rubric.md`
- **Reference template:** `docs/review-reports/batch-a-findings.md`
- **Output:** `docs/review-reports/batch-f-findings.md`

## Acceptance
- [ ] All 9 skills in batch evaluated against all 11 rubric dimensions
- [ ] Findings report at `docs/review-reports/batch-f-findings.md` follows batch-a-findings.md structure: Summary table (Skills reviewed, Clean, Needs Work, Critical), Current Description Budget Impact, per-skill sections (verdict + issues + proposed changes), cross-cutting observations, recommended changes
- [ ] Each skill has a pass/warn/fail rating per dimension with justification
- [ ] Cross-references validated (all `[skill:name]` refs point to existing skills)
- [ ] Description lengths measured and aggregate budget impact noted
- [ ] Issues tagged by severity: Critical (broken refs, budget violations), High, Low

## Done summary
Audited all 9 skills in Batch F (documentation: 5, packaging: 3, localization: 1) against the 11-dimension review rubric. Produced findings report at docs/review-reports/batch-f-findings.md with 7 Clean, 2 Needs Work, 0 Critical. Key finding: dotnet-nuget-authoring has bare-text skill references needing [skill:] syntax fix. All descriptions within 120-char budget (985 total chars).
## Evidence
- Commits: 4938da35945e31e3366a5c36ce4f7e1ba6cbde0e, 35c34a9c8b99f1ede83cd4f1df68b5e2aa33c05e, b31501fbc16021476f5e90acd7f311c73ed29628
- Tests: ./scripts/validate-skills.sh
- PRs: