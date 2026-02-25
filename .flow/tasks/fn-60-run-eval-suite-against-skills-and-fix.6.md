# fn-60.6 Save baselines and unblock fn-58.4

## Description

Save verified eval results as baseline files for future regression tracking. Verify `compare_baseline.py` works against them. Unblock fn-58.4 (CI workflow).

**Depends on:** fn-60.5
**Size:** S
**Files:**
- `tests/evals/baselines/activation_baseline.json` (new)
- `tests/evals/baselines/confusion_baseline.json` (new)
- `tests/evals/baselines/effectiveness_baseline.json` (new)
- `tests/evals/baselines/size_impact_baseline.json` (new)
- `tests/evals/compare_baseline.py` (read-only verification)

## Approach

### Step 1: Select best result files

For each eval type, select the most representative result file from `tests/evals/results/`:
- Prefer the latest non-aborted, non-limited result (full coverage if available from .5)
- If only limited/targeted results exist, use the broadest one and document the coverage in the baseline metadata
- The result file's `summary` schema must be stable (compare_baseline.py compatibility)

### Step 2: Copy to baselines directory

```
cp tests/evals/results/<best_activation>.json tests/evals/baselines/activation_baseline.json
cp tests/evals/results/<best_confusion>.json tests/evals/baselines/confusion_baseline.json
cp tests/evals/results/<best_effectiveness>.json tests/evals/baselines/effectiveness_baseline.json
cp tests/evals/results/<best_size_impact>.json tests/evals/baselines/size_impact_baseline.json
```

### Step 3: Verify compare_baseline.py

Run `compare_baseline.py` against each baseline to confirm it:
- Loads the baseline file successfully
- Parses the summary schema
- Produces a comparison output (even if "no previous baseline" for first run)

### Step 4: Commit and document

- Commit baseline files
- Note in commit message which result files were used as sources
- Document baseline coverage (full dataset vs partial) in commit message

## Key context

- compare_baseline.py uses "latest result file by mtime" for comparison, and loads baselines from the configured baselines directory
- fn-58.4 depends on these baseline files existing to set up CI regression gates
- Memory decision: "CI baseline regression gates must handle schema evolution: new entries absent from the baseline should be treated as 'new coverage', not hard failures"

## Acceptance

- [ ] All 4 baseline files exist in `tests/evals/baselines/`
- [ ] `compare_baseline.py` loads each baseline without error
- [ ] `compare_baseline.py` produces comparison output for each eval type
- [ ] Baseline files committed with documentation of source result files
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] fn-58.4 dependency is satisfied (baseline files in expected location with expected schema)

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
