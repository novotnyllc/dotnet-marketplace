# fn-60.1 Run initial eval suite and capture raw results

## Description

Run all 4 eval types against the current 131-skill catalog to establish the "before" state. This is the diagnostic baseline -- no fixes yet, just measurement.

**Size:** M
**Files:**
- `tests/evals/results/` (output directory, gitignored)

## Approach

Run each eval type in sequence with real API calls. Auth requires `ANTHROPIC_API_KEY` env var (or SDK-supported auth -- see task .7 for details):

1. **L3 Activation**: `python3 tests/evals/run_activation.py` -- 73 cases, ~55 positive + 18 negative
2. **L4 Confusion**: `python3 tests/evals/run_confusion_matrix.py` -- 36 confusion + 18 negative controls
3. **L5 Effectiveness**: `python3 tests/evals/run_effectiveness.py --runs 3` -- 12 skills x 2 prompts x 3 runs = 72 cases; each case = 2 generations + 1 judgment = ~216 API calls
4. **L6 Size Impact**: `python3 tests/evals/run_size_impact.py --runs 3` -- 11 candidates, ~99 comparisons with runs=3

Expected cost per full suite run: ~$5-9 total (all haiku). Effectiveness and size impact are the costliest runners. Note: `config.yaml:cost.max_cost_per_run` is a per-runner-invocation cap. If it aborts mid-run, raise the cap or reduce `--runs`.

**Important**: All runners are "informational, always exit 0" -- they can also abort on cost cap while still writing a partial results JSON. Exit 0 + file existence does NOT guarantee full completion. Always verify coverage completeness (see acceptance).

Save all result JSON files. Record key metrics from each run's summary output for the analysis task.

## Acceptance
- [ ] All 4 eval runners complete without errors (exit 0) AND without cost-cap abort
- [ ] Coverage completeness verified for each runner:
  - Activation: `summary._overall.n` matches expected dataset case count; no "ABORT" in output
  - Confusion: per-group `summary[group].n` matches expected group case count; `_negative_controls.n` matches expected negative case count
  - Effectiveness: per-skill `summary[skill].total_cases == len(rubric.test_prompts) * runs`; `errors == 0` (or explicitly documented)
  - Size impact: per-skill comparison counts match expected `runs` for each comparison type
- [ ] Result JSON files exist in `tests/evals/results/` for all 4 eval types
- [ ] Key metrics captured:
  - L3: activation TPR/FPR/accuracy (from `summary._overall`)
  - L4: confusion per-group accuracy, negative control pass rate, never-activated count (from `artifacts.findings` where `type == "never_activated"`)
  - L5: effectiveness per-skill win rates, confirmation no skill has 0% win rate
  - L6: size impact `full_vs_baseline` results per candidate
- [ ] Total cost documented (sum across all 4 runner invocations)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass (no changes to skills yet)

## Done summary

Created run_suite.sh orchestration script that runs all 4 eval types (activation, confusion, effectiveness, size impact) in sequence with proper input validation, per-spec run counts (1 for activation/confusion, configurable N for effectiveness/size_impact), runner failure tracking, exact result file capture, and resilient suite summary JSON generation. All 4 runners verified working in dry-run mode. Actual API execution requires ANTHROPIC_API_KEY to be set in the environment.

## Evidence

- Commits: 0958c78, a9c371f
- Tests: validate-skills.sh PASS, validate-marketplace.sh PASS, all 4 runners dry-run PASS, run_suite.sh dry-run PASS, input validation PASS
