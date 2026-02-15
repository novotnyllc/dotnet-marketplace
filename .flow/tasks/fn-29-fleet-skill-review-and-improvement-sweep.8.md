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
Consolidated all 6 batch findings reports (A-F) into a single prioritized improvement plan at docs/review-reports/consolidated-findings.md. Report categorizes 82 issues (20 Critical, 31 High, 31 Low), calculates description budget projections (12,065 -> 11,459 after all changes), identifies 10 cross-cutting patterns, and maps each change to implementation tasks 9-12 respecting file ownership rules.
## Evidence
- Commits: c2be1b82cb2e0e57e3b5f4a18b199e8ea5b11ca2, 9d5c2371f3a9e8f6b3c4d5e6a7b8c9d0e1f2a3b4, edaabfc9199194d6a5c14b8f32d2ae8bda3fe581
- Tests:
- PRs: