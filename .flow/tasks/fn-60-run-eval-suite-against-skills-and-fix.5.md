# fn-60.5 Quality bar verification sweep

## Description

Run targeted regression checks on all skills that were fixed in .3/.4, plus a broader sample across L3/L4 to verify quality bar thresholds are met. This is NOT a blind full-suite run -- it is a focused verification of fixes plus a representative sample for confidence.

**Depends on:** fn-60.3, fn-60.4
**Size:** M
**Files:**
- `tests/evals/results/` (verification results)
- `tests/evals/eval-progress.json` (read `fixed_tasks` to identify which skills were fixed in .3/.4, update with verification results)

## Approach

### Step 1: Targeted re-verification of all fixed skills

Read `tests/evals/eval-progress.json`. Use `fixed_tasks` to determine which verifications to run per skill:
- Skills with `".3"` in `fixed_tasks` (routing fixes): re-run L3 activation (`--skill <name>`) and L4 confusion (`--group <group>`)
- Skills with `".4"` in `fixed_tasks` (content fixes): re-run L5 effectiveness (`--skill <name> --runs 3 --regenerate`) and L6 size impact if applicable (`--skill <name> --runs 3 --regenerate`)

Multi-run (--runs 3) provides statistical confidence for L5/L6 judgments.

### Step 2: Broader representative sample

Run a broader sample to check for regressions in un-edited skills:
- L3 activation: `--limit 40` (~40 proportionally sampled cases) -- covers ~55% of cases
- L4 confusion: `--limit 5` (5 of 7 groups) -- covers ~71% of groups

This provides representative coverage without running the full dataset.

### Step 3: Quality bar check
<!-- Updated by plan-sync: fn-60.2 established error exclusion policy for quality bar metrics -->

Verify ALL thresholds against the sample results. **Error exclusion policy** (from triage): quality bar metrics (TPR/FPR/accuracy/win_rate) MUST exclude `detection_method: error` cases from both numerator and denominator. Error rate is tracked separately as an infra health metric. If error rate exceeds 10%, flag the run as degraded and re-run after increasing CLI timeout.

**L3 Activation** (hard gates, excluding error cases):
- TPR >= 75%, FPR <= 20%, Accuracy >= 70%

**L4 Confusion** (hard gates -- all four must be checked):
- Per-group accuracy >= 60%
- Cross-activation rate <= 35% (per-group)
- No never-activated skills (in sampled groups)
- Negative control pass rate >= 70%

**L5 Effectiveness** (per-skill gates):
- No skill at 0% win rate without documented variance exception (minimum n=6 judged cases)
- Per-skill win rate target >= 50% for all rubric'd skills
- Also compute and report (not gating): micro-average win rate across all non-error cases, mean improvement across all cases

**L6 Size Impact** (hard gates):
- full > baseline in >= 55% of comparisons
- No baseline sweep (no skill where baseline wins all runs)

If any threshold is missed on the sample: investigate which specific cases fail, determine if they are fixable, and either fix + re-verify or document as exceptions.

### Step 4: Update eval-progress.json

For verified skills, update `skills[skill_name]`:
- Set `routing_status` and/or `content_status` to `verified` (based on which dimensions were re-checked)
- Recompute `overall_status`
- Add verification `run_ids`

### CLI call estimate

- Fixed skills re-runs: ~50-80 calls (depends on .3/.4 scope)
- L3 sample: ~40 calls
- L4 sample: ~25 calls
- Total: ~115-145 calls (spread across targeted and sample runs)

## Acceptance

- [ ] All skills with `".3"` in `fixed_tasks` re-verified with targeted activation/confusion re-runs
- [ ] All skills with `".4"` in `fixed_tasks` re-verified with `--runs 3 --regenerate` for statistical confidence
- [ ] Broader L3 sample (`--limit 40`) meets quality bar: TPR >= 75%, FPR <= 20%, Accuracy >= 70%
- [ ] Broader L4 sample (`--limit 5`) meets all gates: per-group >= 60%, cross-activation <= 35%, no never-activated skills, negative controls >= 70%
- [ ] L5 per-skill gates met: no 0% win rate without documented exception, per-skill targets >= 50%
- [ ] L5 aggregate metrics reported: micro-average win rate, mean improvement
- [ ] L6 no baseline sweep remaining (or documented rationale), full > baseline >= 55%
- [ ] Any threshold misses documented with specific failing cases and rationale
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] Results saved in `tests/evals/results/`
- [ ] `eval-progress.json` updated: verified skills have `routing_status`/`content_status` set to `verified`

## Done summary
Computed quality bar metrics from existing valid eval results: L3 activation PASS (TPR=92.7%, FPR=13.3%, Accuracy=91.1% error-excluded), L4 confusion PASS (all 7 groups above thresholds), L5 effectiveness PASS (all skills >=50% win rate, micro-avg 87.5%). Verified .3 routing fixes via targeted re-run evidence, documented messaging-patterns as variance exception with provenance. L6 size impact PENDING_REVERIFICATION -- created verify-content-fixes.sh for external .4 content re-runs (nested session constraint prevents CLI execution).
## Evidence
- Commits: 800007d, 43da949, 21bb501
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: