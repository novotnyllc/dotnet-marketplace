# fn-60.6 Save initial baselines and unblock fn-58.4

## Description

Save the passing eval results as initial baseline JSON files in `tests/evals/baselines/`. These baselines are used by `compare_baseline.py` for future regression detection. Then add this task as a dependency on fn-58.4 (CI workflow task).

**Size:** S
**Files:**
- `tests/evals/baselines/effectiveness_baseline.json` (new)
- `tests/evals/baselines/activation_baseline.json` (new)
- `tests/evals/baselines/confusion_baseline.json` (new)
- `tests/evals/baselines/size_impact_baseline.json` (new)

## Approach

1. Extract the `summary` object from each eval type's result JSON
2. Save with a small `meta` header (run_id, timestamp) as per fn-58.4 spec
3. Baseline format: `{"meta": {...}, "summary": {...}}`
4. `compare_baseline.py` ignores `cases` and `artifacts` fields -- only `summary` matters
5. Verify baseline files work with: `python3 tests/evals/compare_baseline.py --eval-type <type>`
6. Replace `.gitkeep` files in `baselines/` directory with real files
7. fn-58.4 already has this task listed as a dependency (added during epic creation)

## Acceptance
- [ ] All 4 baseline JSON files exist in `tests/evals/baselines/`
- [ ] Each baseline contains `meta` and `summary` keys
- [ ] `compare_baseline.py` runs without error against all 4 baseline types
- [ ] fn-58.4 has dependency on this task
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
