# fn-60.1 Run initial eval suite and capture raw results

## Description

Run all 4 eval types against the current 131-skill catalog to establish the "before" state. This is the diagnostic baseline -- no fixes yet, just measurement.

**Size:** M
**Files:**
- `tests/evals/results/` (output directory, gitignored)

## Approach

Run each eval type in sequence with real API calls (ANTHROPIC_API_KEY required):

1. **L3 Activation**: `python3 tests/evals/run_activation.py` -- 73 cases, ~55 positive + 18 negative
2. **L4 Confusion**: `python3 tests/evals/run_confusion_matrix.py` -- 36 confusion + 18 negative controls
3. **L5 Effectiveness**: `python3 tests/evals/run_effectiveness.py --runs 3` -- 12 skills x 2 prompts x 3 runs
4. **L6 Size Impact**: `python3 tests/evals/run_size_impact.py` -- 11 candidates, 36 comparisons

Expected cost: ~$3-5 total (all haiku).

Save all result JSON files. Record key metrics from each run's summary output for the analysis task.

## Acceptance
- [ ] All 4 eval runners complete without errors (exit 0)
- [ ] Result JSON files exist in `tests/evals/results/` for all 4 eval types
- [ ] Key metrics captured: activation TPR/FPR/accuracy, confusion per-group accuracy, effectiveness per-skill win rates, size impact comparison results
- [ ] Total cost documented
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass (no changes to skills yet)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
