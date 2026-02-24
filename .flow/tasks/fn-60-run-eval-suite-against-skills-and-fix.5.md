# fn-60.5 Rerun eval suite and validate against quality bar

## Description

Full rerun of all 4 eval types after fixes from tasks .3 and .4. Validate results against the quality bar thresholds defined in the epic spec. If thresholds are not met, do one more targeted fix-and-rerun iteration.

**Size:** M
**Files:**
- `tests/evals/results/` (output directory, gitignored)

## Approach

1. Run all 4 eval types with `--regenerate` flag (where applicable) to ensure fresh generations:
   - `python3 tests/evals/run_activation.py`
   - `python3 tests/evals/run_confusion_matrix.py`
   - `python3 tests/evals/run_effectiveness.py --runs 3 --regenerate`
   - `python3 tests/evals/run_size_impact.py --regenerate`

2. Compare results against quality bar thresholds:
   - L3: TPR>=75%, FPR<=20%, accuracy>=70%
   - L4: per-group accuracy>=60%, cross-activation<=35%, negative control pass rate>=70%
   - L5: overall win rate>=50%, mean improvement>0, no skill at 0% win rate
   - L6: full>baseline in >=55% of comparisons

3. If any threshold is missed:
   - Identify the specific failures
   - Make targeted fixes (another iteration of .3/.4 work)
   - Rerun the failing eval type only
   - Document the iteration in the done summary

4. If a threshold proves systematically unachievable (e.g., haiku consistently can't route to certain skills), document the rationale and adjust the threshold.

## Acceptance
- [ ] All 4 eval types re-run with fresh results
- [ ] Results compared against quality bar thresholds
- [ ] All thresholds met OR documented rationale for exceptions
- [ ] Before/after comparison documented (initial run vs final run)
- [ ] Total cost across all iterations documented
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
