# fn-29-fleet-skill-review-and-improvement-sweep.8 Consolidate findings and prioritize changes

## Description

Merge all 6 batch findings reports (batch-{a,b,c,d,e,f}-findings.md) into a single prioritized improvement plan at `docs/review-reports/consolidated-findings.md`. Parse the findings from each batch using the proven structure: summary metrics, per-skill issues table, cross-cutting observations, and recommended changes. Categorize issues as Critical (broken cross-refs, budget violations), High-value (missing sections, clarity improvements), or Low-priority (formatting, minor wording). Identify cross-cutting patterns across all batches. Calculate projected description budget impact for all proposed description changes using aggregate current totals from each batch's "Current Description Budget Impact" section.

### Files

- **Input:** `docs/review-reports/batch-{a,b,c,d,e,f}-findings.md`
- **Output:** `docs/review-reports/consolidated-findings.md`

## Acceptance
- [ ] All 6 batch findings reports (batch-a through batch-f) merged into consolidated report
- [ ] Issues categorized with consistent severity levels: Critical (broken cross-refs, missing descriptions, budget violations), High (missing sections, significant clarity gaps), Low (formatting, minor wording, monitoring suggestions)
- [ ] Cross-cutting patterns identified from batch-level observations (issues affecting multiple skills or categories similarly)
- [ ] Projected description budget calculation included: aggregate current total from all 6 batches, proposed total after all recommended changes, delta vs 12K warn / 15K fail thresholds
- [ ] Each proposed change tagged with affected skill name, category, and priority level
- [ ] Reference batch-a-findings.md severity categorization pattern (Critical/High/Low) for consistency

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
