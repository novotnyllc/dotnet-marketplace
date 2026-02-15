# fn-29-fleet-skill-review-and-improvement-sweep.8 Consolidate findings and prioritize changes

## Description

Merge all 6 batch findings reports into a single prioritized improvement plan at `docs/review-reports/consolidated-findings.md`. Categorize issues as Critical/High-value/Low-priority. Identify cross-cutting patterns. Calculate projected description budget impact for all proposed description changes.

### Files

- **Input:** `docs/review-reports/batch-{a,b,c,d,e,f}-findings.md`
- **Output:** `docs/review-reports/consolidated-findings.md`

## Acceptance
- [ ] All 6 batch findings merged into consolidated report
- [ ] Issues categorized: Critical (broken cross-refs, missing descriptions, budget violations), High-value (better triggers, clearer instructions), Low-priority (formatting, wording)
- [ ] Cross-cutting patterns identified (issues affecting many skills similarly)
- [ ] Projected description budget calculation included: current total, proposed total, delta vs 12K warn / 15K fail thresholds
- [ ] Each proposed change tagged with affected skill name and priority

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
