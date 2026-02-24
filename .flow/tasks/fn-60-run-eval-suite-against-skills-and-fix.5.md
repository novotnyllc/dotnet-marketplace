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
   - `python3 tests/evals/run_size_impact.py --runs 3 --regenerate`

2. Verify coverage completeness (runners exit 0 but may abort on cost cap -- see fn-60.1 acceptance for per-runner completeness checks). Re-run with raised cap if any runner aborted.

3. Compare results against ALL quality bar thresholds:
   - L3: TPR>=75%, FPR<=20%, accuracy>=70% (from `summary._overall`)
   - L4: per-group accuracy>=60%, cross-activation<=35%, no never-activated skills (check `artifacts.findings[]` where `type == "never_activated"` -- must be empty or exception documented), negative control pass rate>=70%
   - L5: overall win rate>=50% (sum wins / sum non-error cases across skills), mean improvement>0 (weighted by n), no skill at 0% win rate
   - L6 (computed exclusively from `full_vs_baseline` comparisons):
     - Aggregate: `wins_full / (wins_full + wins_baseline + ties)` >= 55% across all candidates
     - Per-skill: no candidate where baseline sweeps all runs (`wins_baseline == n`) -- this indicates harmful skill content

4. If any threshold is missed:
   - Identify the specific failures
   - Make targeted fixes (another iteration of .3/.4 work)
   - Rerun the failing eval type only
   - Document the iteration in the summary

5. If a threshold proves systematically unachievable (e.g., haiku consistently can't route to certain skills), document the rationale and adjust the threshold.

## Acceptance
- [ ] All 4 eval types re-run with fresh results and verified complete (no cost-cap aborts)
- [ ] Results compared against ALL quality bar thresholds including:
  - L4 "no never-activated skills" via `artifacts.findings[]` (or documented exception with rationale)
  - L4 negative control pass rate >= 70%
  - L5 no skill at 0% win rate
  - L5/L6 aggregation uses weighted method (sum wins / sum non-error cases)
  - L6 per-skill guard: no candidate where baseline sweeps all runs in `full_vs_baseline`
- [ ] All thresholds met OR documented rationale for exceptions
- [ ] Before/after comparison documented (initial run vs final run)
- [ ] Total cost across all iterations documented
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass
