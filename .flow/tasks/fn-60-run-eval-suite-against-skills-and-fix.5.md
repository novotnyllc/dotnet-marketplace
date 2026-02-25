# fn-60.5 Quality bar verification sweep

## Description

Run targeted regression checks on all skills that were fixed in .3/.4, plus a broader sample across L3/L4 to verify quality bar thresholds are met. This is NOT a blind full-suite run — it's a focused verification of fixes plus a representative sample for confidence.

**Depends on:** fn-60.3, fn-60.4
**Size:** M
**Files:**
- `tests/evals/results/` (verification results)
- `tests/evals/eval-progress.json` (read to identify which skills were fixed in .3/.4, update with verification results)

## Approach

### Step 1: Targeted re-verification of all fixed skills

Read `tests/evals/eval-progress.json` to get the list of skills with `status: "fixed"` from .3 and .4. Re-run each eval type on those skills/groups:
- L3 activation: `--skill <name>` for each skill edited in .3 (confirm routing improvements held)
- L4 confusion: `--group <group>` for each group affected in .3
- L5 effectiveness: `--skill <name> --runs 3 --regenerate` for each skill edited in .4 (multi-run for statistical confidence)
- L6 size impact: `--skill <name> --runs 3 --regenerate` for each candidate addressed in .4

### Step 2: Broader representative sample

Run a broader sample to check for regressions in un-edited skills:
- L3 activation: `--limit 40` (~40 proportionally sampled cases) — covers ~55% of cases
- L4 confusion: `--limit 5` (5 of 7 groups) — covers ~71% of groups

This provides representative coverage without running the full dataset. If the sample meets thresholds, the full dataset almost certainly does too.

### Step 3: Quality bar check

Verify thresholds against the sample results:
- L3: TPR >= 75%, FPR <= 20%, Accuracy >= 70%
- L4: Per-group accuracy >= 60%, negative controls >= 70%
- L5: Overall win rate >= 50%, no 0% without exception
- L6: full > baseline in >= 55%, no baseline sweep

If any threshold is missed on the sample: investigate which specific cases fail, determine if they're fixable, and either fix + re-verify or document as exceptions.

### CLI call estimate

- Fixed skills re-runs: ~50-80 calls (depends on .3/.4 scope)
- L3 sample: ~40 calls
- L4 sample: ~25 calls
- Total: ~115-145 calls (spread across targeted and sample runs)

## Acceptance

- [ ] All skills edited in .3 re-verified with targeted activation/confusion re-runs
- [ ] All skills edited in .4 re-verified with `--runs 3 --regenerate` for statistical confidence
- [ ] Broader L3 sample (`--limit 40`) meets quality bar: TPR >= 75%, FPR <= 20%, Accuracy >= 70%
- [ ] Broader L4 sample (`--limit 5`) meets quality bar: per-group >= 60%, negative controls >= 70%
- [ ] L5 overall win rate >= 50% (no 0% win rate without documented exception)
- [ ] L6 no baseline sweep remaining (or documented rationale)
- [ ] Any threshold misses documented with specific failing cases and rationale
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] Results saved in `tests/evals/results/`
- [ ] `eval-progress.json` updated with verification results and final status per skill

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
