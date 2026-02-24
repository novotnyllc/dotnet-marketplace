# fn-60.1 Run initial eval suite and capture raw results

## Description

Run all 4 eval types against the current 131-skill catalog to establish the "before" state. This is the diagnostic baseline -- no fixes yet, just measurement.

**Size:** M
**Files:**
- `tests/evals/results/` (output directory, gitignored)

## Approach

Run each eval type in sequence using CLI-based invocations (task .7 replaces SDK calls with subprocess calls to `claude`/`codex`/`copilot`). CLI clients are already authenticated locally -- no API key setup needed.

1. **L3 Activation**: `python3 tests/evals/run_activation.py` -- 73 cases, ~55 positive + 18 negative
2. **L4 Confusion**: `python3 tests/evals/run_confusion_matrix.py` -- 36 confusion + 18 negative controls
3. **L5 Effectiveness**: `python3 tests/evals/run_effectiveness.py --runs 3` -- 12 skills x 2 prompts x 3 runs = 72 cases; each case = 2 generations + 1 judgment = ~216 CLI calls
4. **L6 Size Impact**: `python3 tests/evals/run_size_impact.py --runs 3` -- 11 candidates, ~99 comparisons with runs=3

Or use the suite runner: `./tests/evals/run_suite.sh`

**Important**: All runners are "informational, always exit 0" -- they can also abort on cost/call cap while still writing a partial results JSON. Exit 0 + file existence does NOT guarantee full completion. Always verify coverage completeness (see acceptance).

Save all result JSON files. Record key metrics from each run's summary output for the analysis task.

**Dry-run is NOT acceptable**: This task requires real CLI calls producing real results. Dry-run mode is only for verifying dataset/config, not for task completion.

## Acceptance
- [ ] All 4 eval runners complete with real CLI calls (not dry-run) without errors (exit 0) AND without cost-cap abort
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
- [ ] Total cost documented (if available from CLI output; otherwise call count documented)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass (no changes to skills yet)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
