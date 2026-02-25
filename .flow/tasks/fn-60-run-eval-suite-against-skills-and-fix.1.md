# fn-60.1 Add --limit flag to eval runners and smoke test pipeline

## Description

Add a `--limit N` argparse flag to all 4 eval runners so case volume can be capped for safe progressive evaluation. Then smoke test the pipeline with `--limit 2` to verify everything works after the .7/.8/.9 CLI migration.

**Depends on:** fn-60.7, fn-60.8, fn-60.9
**Size:** M
**Files:**
- `tests/evals/run_activation.py` (add --limit, proportional sampling)
- `tests/evals/run_confusion_matrix.py` (add --limit, per-group semantics)
- `tests/evals/run_effectiveness.py` (add --limit, per-skill semantics)
- `tests/evals/run_size_impact.py` (add --limit, per-candidate semantics)
- `tests/evals/run_suite.sh` (parse and pass --limit through to runners)
- `tests/evals/_common.py` (optional: shared limit helper)

## Approach

### --limit semantics per runner

Each runner interprets `--limit N` based on its primary iteration unit:

- **Activation**: N total cases, but use stratified sampling: if both positive and negative pools exist post-filter, include at least 1 from each pool before filling remaining slots by seeded shuffle-then-slice. This prevents small limits from yielding all-negative or all-positive sets. Follow the openai/evals pattern: `random.Random(seed).shuffle(indices); indices = indices[:limit]` after stratification guarantees.
- **Confusion**: N groups (each group retains all its cases). With 7 groups, `--limit 2` runs 2 complete groups. Negative controls are included proportionally (e.g., `--limit 2` includes `ceil(18 * 2/7)` negative controls).
- **Effectiveness**: N skills (each skill retains all prompts x runs). With 12 rubric'd skills, `--limit 3` evaluates 3 complete skills.
- **Size impact**: N candidates (each candidate retains all comparison types x runs). With 11 candidates, `--limit 3` evaluates 3 complete candidates.

### Deterministic sampling

All sampling uses `random.Random(seed)` where seed = `config.yaml:rng.default_seed` (accessed via `cfg["rng"]["default_seed"]`, or overridden with `--seed` CLI arg) combined with a runner-specific salt (e.g., `seed + hash("activation")`) to ensure:
- Same `--limit N` always selects the same subset for a given seed
- Different runners select independently (no correlated subsets)
- Results are reproducible across runs for triage comparison

### Result metadata

When `--limit` is used, record in the result JSON:
- `meta.limit`: N (the limit value)
- `meta.aborted`: bool (true if run was cut short by budget or fail-fast, false if completed cleanly)

Follow pattern at `_common.py:build_run_metadata()`. The `meta.aborted` field enables triage (task .2) to distinguish partial vs full runs without parsing stdout.

### Validation

- `--limit 0` and negative values: reject with argparse error
- `--limit` exceeds dataset size: silently cap (follow lm-eval-harness)
- `--limit` combined with `--skill`/`--group`: filter first, then `--limit` caps the filtered set
- Warn when `--limit` is used: print `"WARNING: --limit is for development/testing. Full-dataset runs needed for baselines."` to stderr (follow lm-eval-harness)

### run_suite.sh update

Parse `--limit=N` in run_suite.sh and pass `--limit N` to each runner invocation. Currently run_suite.sh rejects unknown args, so the parsing must be added explicitly.

### Smoke test

After implementing `--limit`, run each runner with `--limit 2 --runs 1` to confirm end-to-end pipeline works:
```
python3 tests/evals/run_activation.py --limit 2
python3 tests/evals/run_confusion_matrix.py --limit 2
python3 tests/evals/run_effectiveness.py --limit 2 --runs 1
python3 tests/evals/run_size_impact.py --limit 2 --runs 1
```

Each should complete with exit 0, produce a result JSON, and emit TOTAL_CALLS/COST_USD/ABORTED/N_CASES/FAIL_FAST on stdout.

## Acceptance

- [ ] All 4 runners accept `--limit N` argparse flag (integer > 0)
- [ ] Activation `--limit` uses stratified sampling: at least 1 positive and 1 negative when both pools exist, then seeded shuffle-then-slice for remaining slots
- [ ] Confusion `--limit N` limits to N groups (not N total cases)
- [ ] Effectiveness `--limit N` limits to N skills
- [ ] Size impact `--limit N` limits to N candidates
- [ ] Sampling is deterministic: same seed + limit always produces same subset (seed from `config.yaml:rng.default_seed`)
- [ ] `--limit` exceeding dataset size silently caps without error
- [ ] `--limit 0` and negative values produce argparse error
- [ ] When `--limit` is used, result JSON includes `meta.limit: N` and `meta.aborted: bool`
- [ ] Warning message printed to stderr when `--limit` is used
- [ ] `run_suite.sh --limit=N` parses and passes --limit to all 4 runners
- [ ] Smoke test passes: each runner with `--limit 2 --runs 1` exits 0, produces result JSON, emits stdout keys
- [ ] `--dry-run` still works (no regression)
- [ ] `--limit` combined with `--skill`/`--group` works (filter first, then cap)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass (no skill changes yet)

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
