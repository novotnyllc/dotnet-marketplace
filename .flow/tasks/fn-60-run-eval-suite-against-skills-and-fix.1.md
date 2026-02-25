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
- `tests/evals/run_suite.sh` (pass --limit through to runners)
- `tests/evals/_common.py` (optional: shared limit helper)

## Approach

### --limit semantics per runner

Each runner interprets `--limit N` based on its primary iteration unit:

- **Activation**: N total cases, but use proportional sampling (shuffle with seeded RNG, then slice) so the limited set contains both positive and negative cases. Follow the openai/evals pattern: `random.Random(seed).shuffle(indices); indices = indices[:limit]`. Without this, `--limit 5` would get 5 core_skills and 0 negatives (files load alphabetically: core_skills, negative_controls, specialized_skills).
- **Confusion**: N groups (each group retains all its cases). With 7 groups, `--limit 2` runs 2 complete groups. Negative controls are included proportionally (e.g., `--limit 2` includes `ceil(18 * 2/7)` negative controls).
- **Effectiveness**: N skills (each skill retains all prompts × runs). With 12 rubric'd skills, `--limit 3` evaluates 3 complete skills.
- **Size impact**: N candidates (each candidate retains all comparison types × runs). With 11 candidates, `--limit 3` evaluates 3 complete candidates.

### Result metadata

When `--limit` is used, record `meta.limit: N` in the result JSON so reviewers know a result came from a partial run. Follow pattern at `_common.py:build_run_metadata()`.

### Validation

- `--limit 0` and negative values: reject with argparse error
- `--limit` exceeds dataset size: silently cap (follow lm-eval-harness)
- `--limit` combined with `--skill`/`--group`: `--skill` filters first, then `--limit` caps the filtered set
- Warn when `--limit` is used: print `"WARNING: --limit is for development/testing. Full-dataset runs needed for baselines."` to stderr (follow lm-eval-harness)

### run_suite.sh update

Add `--limit=N` passthrough: `run_suite.sh --limit=5` passes `--limit 5` to each runner invocation.

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
- [ ] Activation `--limit` uses proportional sampling (seeded shuffle-then-slice) so limited sets include positive and negative cases
- [ ] Confusion `--limit N` limits to N groups (not N total cases)
- [ ] Effectiveness `--limit N` limits to N skills
- [ ] Size impact `--limit N` limits to N candidates
- [ ] `--limit` exceeding dataset size silently caps without error
- [ ] `--limit 0` and negative values produce argparse error
- [ ] When `--limit` is used, result JSON includes `meta.limit: N`
- [ ] Warning message printed to stderr when `--limit` is used
- [ ] `run_suite.sh --limit=N` passes --limit to all 4 runners
- [ ] Smoke test passes: each runner with `--limit 2 --runs 1` exits 0, produces result JSON, emits stdout keys
- [ ] `--dry-run` still works (no regression)
- [ ] `--limit` combined with `--skill`/`--group` works (filter first, then cap)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass (no skill changes yet)

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
