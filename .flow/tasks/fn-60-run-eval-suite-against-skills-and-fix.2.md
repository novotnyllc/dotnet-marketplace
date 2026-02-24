# fn-60.2 Analyze results and triage findings

## Description

Analyze the raw results from task .1 across all 4 eval types. Identify worst performers, common failure patterns, and produce a prioritized fix list. This analysis drives tasks .3 and .4.

**Depends on:** fn-60.1
**Size:** M
**Files:**
- No file changes -- analysis only, findings documented in this task's summary

## Approach

For each eval type, extract and document:

### L3 Activation
- Overall TPR, FPR, accuracy vs thresholds (TPR>=75%, FPR<=20%, accuracy>=70%) -- read from `summary._overall`
- Per-skill activation rates -- which skills are never found? Read from `artifacts.per_skill`
- Detection method breakdown (structured vs fallback vs parse_failure) -- read from `artifacts.detection_method_counts`
- False positives -- which negative controls failed?

### L4 Confusion
- Per-group accuracy vs threshold (>=60%) -- read from group-level summary
- Cross-activation rate per group vs threshold (<=35%)
- Flagged cross-activation pairs (>20% rate)
- Never-activated skills -- check `artifacts.findings[]` where `type == "never_activated"` (must be empty to meet quality bar, or document exception)
- Cross-check: `artifacts.confusion_matrices.<group>.matrix` column-sum == 0 indicates a never-activated skill
- Negative control pass rate vs threshold (>=70%)

### L5 Effectiveness
- Per-skill win rates vs threshold
- **Overall win rate**: sum(wins) / sum(non-error cases) across all skills (weighted by case count, excluding errors)
- **Mean improvement**: weighted mean by `n` across skills
- Check 0% win rate skills: flag for review but apply variance exception rule -- with only 6 cases per skill, 0% can occur by chance. Document exception with rationale if mean improvement is non-negative but wins are 0.
- Error rates -- any skills with generation/judge failures?
- Per-criterion breakdown -- which criteria drive wins/losses?

### L6 Size Impact
- Compute from `results.summary[skill].comparisons.full_vs_baseline` only (not full_vs_summary or other comparison types)
- **full > baseline rate**: aggregate `wins_full / (wins_full + wins_baseline + ties)` across all candidate skills (excluding error cases) vs threshold (>=55%)
- **Per-skill harmful check**: flag any candidate where baseline sweeps all runs (`wins_baseline == n`) in `full_vs_baseline` -- this indicates the full content is actively harmful for that skill
- full vs summary comparison -- informational only, not part of quality bar
- Size tier correlations -- do large skills benefit more from full content?

### Triage Output
- Prioritized list of skills to fix (worst first)
- Classification: description problem (L3/L4) vs content problem (L5)
- Estimated fix complexity per skill

## Acceptance
- [ ] All 4 eval type results analyzed using correct output paths (summary vs artifacts)
- [ ] Current metrics vs quality bar thresholds documented (including never-activated and negative-control checks)
- [ ] L5 0% win rate skills flagged with variance analysis (exception documented if mean improvement non-negative)
- [ ] L6 metrics computed exclusively from `full_vs_baseline` comparisons; "harmful" = baseline sweep (wins_baseline == n)
- [ ] Aggregation method for L5/L6 "overall" metrics explicitly stated (weighted by case count)
- [ ] Prioritized fix list with classification (description vs content)
- [ ] Fix list informs task .3 (routing fixes) and task .4 (content fixes)
- [ ] Any threshold adjustments documented with rationale

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
