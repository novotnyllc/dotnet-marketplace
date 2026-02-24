# fn-60.2 Analyze results and triage findings

## Description

Analyze the raw results from task .1 across all 4 eval types. Identify worst performers, common failure patterns, and produce a prioritized fix list. This analysis drives tasks .3 and .4.

**Size:** M
**Files:**
- No file changes -- analysis only, findings documented in this task's done summary

## Approach

For each eval type, extract and document:

### L3 Activation
- Overall TPR, FPR, accuracy vs thresholds (TPR>=75%, FPR<=20%, accuracy>=70%)
- Per-skill activation rates -- which skills are never found?
- Detection method breakdown -- how many structured vs fallback vs parse_failure?
- False positives -- which negative controls failed?

### L4 Confusion
- Per-group accuracy vs threshold (>=60%)
- Cross-activation rate per group vs threshold (<=35%)
- Flagged cross-activation pairs (>20% rate)
- Low-discrimination skills and "never-activated" skills
- Negative control pass rate vs threshold (>=70%)

### L5 Effectiveness
- Per-skill win rates vs threshold (overall >=50%)
- Mean improvement per skill -- any negative (skill makes things worse)?
- Error rates -- any skills with generation/judge failures?
- Per-criterion breakdown -- which criteria drive wins/losses?

### L6 Size Impact
- full vs baseline win rate vs threshold (>=55%)
- Any skills where baseline beats full?
- full vs summary comparison -- is full always better?
- Size tier correlations -- do large skills benefit more from full content?

### Triage Output
- Prioritized list of skills to fix (worst first)
- Classification: description problem (L3/L4) vs content problem (L5)
- Estimated fix complexity per skill

## Acceptance
- [ ] All 4 eval type results analyzed
- [ ] Current metrics vs quality bar thresholds documented
- [ ] Prioritized fix list with classification (description vs content)
- [ ] Fix list informs task .3 (routing fixes) and task .4 (content fixes)
- [ ] Any threshold adjustments documented with rationale

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
