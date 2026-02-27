# fn-60.6 Save baselines and unblock fn-58.4

## Description

Run a single full-coverage pass per eval type (no `--limit`) to produce clean baseline results, verify they meet quality bars, then save them for future regression tracking. Verify `compare_baseline.py` works against them. Unblock fn-58.4 (CI workflow).

**Depends on:** fn-60.5
**Size:** M
**Files:**
- `tests/evals/baselines/activation_baseline.json` (new)
- `tests/evals/baselines/confusion_baseline.json` (new)
- `tests/evals/baselines/effectiveness_baseline.json` (new)
- `tests/evals/baselines/size_impact_baseline.json` (new)
- `tests/evals/compare_baseline.py` (read-only verification)

## Approach

### Step 1: Full-coverage baseline runs

Run each eval type WITHOUT `--limit` using the canonical config to produce complete results suitable for baselines:

```bash
python3 tests/evals/run_activation.py
python3 tests/evals/run_confusion_matrix.py
python3 tests/evals/run_effectiveness.py --runs 3
python3 tests/evals/run_size_impact.py --runs 3
```

**Canonical config:** Baselines must be generated using `config.yaml` defaults (`cli.default: claude`, `model` as configured -- typically `haiku`). Record the backend and model in the baseline commit message for future comparability.

Verify each result has `meta.limit` absent or `null` (confirming full coverage).

### CLI call estimate

- Activation: ~73 calls (73 cases)
- Confusion: ~54 calls (7 groups x ~5 cases + 18 negative controls)
- Effectiveness: ~72 calls (12 skills x 2 prompts x 3 runs)
- Size impact: ~99 calls (11 candidates x 3 comparison types x 3 runs)
- Total: ~298 calls

### Step 2: Verify quality bars on full results
<!-- Updated by plan-sync: fn-60.2 established error exclusion policy for quality bar metrics -->

Before saving as baselines, confirm the full-coverage results meet all quality bars. Apply the **error exclusion policy** (from triage): exclude `detection_method: error` cases from metric computation. Track error rate separately; if > 10%, flag run as degraded and re-run after increasing CLI timeout.

- **L3**: TPR >= 75%, FPR <= 20%, Accuracy >= 70% (excluding error cases)
- **L4**: Per-group >= 60%, cross-activation <= 35%, no never-activated, negative controls >= 70%
- **L5**: No 0% win rate without exception, per-skill >= 50% (excluding error cases)
- **L6**: full > baseline >= 55%, no baseline sweep

**If any threshold fails:** This indicates the sampling-based .5 verification missed a tail failure. Loop back: identify failing skills, fix in a targeted batch (following .3/.4 workflow), re-run full coverage, and re-check. Do not save failing results as baselines.

### Step 3: Copy to baselines directory

```bash
mkdir -p tests/evals/baselines/
cp tests/evals/results/<latest_activation>.json tests/evals/baselines/activation_baseline.json
cp tests/evals/results/<latest_confusion>.json tests/evals/baselines/confusion_baseline.json
cp tests/evals/results/<latest_effectiveness>.json tests/evals/baselines/effectiveness_baseline.json
cp tests/evals/results/<latest_size_impact>.json tests/evals/baselines/size_impact_baseline.json
```

### Step 4: Verify compare_baseline.py

Run `compare_baseline.py` against each baseline to confirm it:
- Loads the baseline file successfully
- Parses the summary schema
- Produces a comparison output (even if "no previous baseline" for first run)

### Step 5: Commit and document

- Commit baseline files
- Note in commit message: source result files, backend/model used, full coverage confirmation
- Document baseline coverage (full dataset, run counts) in commit message

## Key context

- compare_baseline.py uses "latest result file by mtime" for comparison, and loads baselines from the configured baselines directory
- fn-58.4 depends on these baseline files existing to set up CI regression gates
- Memory decision: "CI baseline regression gates must handle schema evolution: new entries absent from the baseline should be treated as 'new coverage', not hard failures"
- Mixing backends across baseline vs comparison runs can create noise -- canonical config ensures consistency

## Acceptance

- [ ] Full-coverage runs completed for all 4 eval types (no --limit, `meta.limit` absent)
- [ ] Full-coverage results meet ALL quality bars (L3, L4, L5, L6) -- verified before saving
- [ ] All 4 baseline files exist in `tests/evals/baselines/`
- [ ] `compare_baseline.py` loads each baseline without error
- [ ] `compare_baseline.py` produces comparison output for each eval type
- [ ] Baseline files committed with documentation of source result files, backend/model, and coverage
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] fn-58.4 dependency is satisfied (baseline files in expected location with expected schema)

## Done summary
Fixed `--mcp-config "{}"` bug in `_common.py` that caused all eval CLI calls to return empty responses (the `{}` JSON lacks the required `mcpServers` key). `--strict-mcp-config` alone blocks MCP server loading. Also cleaned stale generation cache entries left by buggy runs.

Ran full-coverage eval suites (no `--limit`) for all 4 types with backend=claude, model=haiku, seed=42:

- **L3 Activation**: TPR=100%, FPR=16.67%, Accuracy=95.89% — PASS
- **L4 Confusion**: 100% accuracy all 7 groups, 100% negative controls — PASS
- **L5 Effectiveness**: all 12 skills ≥83.3% win rate, 0% errors — PASS
- **L6 Size Impact**: no baseline sweeps, all skills n≥2 — PASS

Saved baselines to `tests/evals/baselines/`, verified `compare_baseline.py` loads all 4 without error, validated with `validate-skills.sh` and `validate-marketplace.sh`.
## Evidence
- Commits: bc86e97, ee10c46
- Tests: compare_baseline.py: all 4 types = no regressions
- PRs: