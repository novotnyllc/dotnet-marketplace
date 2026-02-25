# Run Eval Suite Against Skills and Fix to Quality Bar

## Overview

Epic fn-58 built a comprehensive offline evaluation framework with 4 runners (activation, confusion, effectiveness, size impact), 12 rubrics, 73 activation cases, 36 confusion cases, and 11 size impact candidates. Tasks .7/.8/.9 migrated to CLI-based invocations, fixed probe reliability, and added fail-fast error classification.

This epic closes the loop: analyze eval results, fix skill descriptions and content in small batches with verification at each step, and save baselines for regression tracking.

**Core principle: NEVER run all skills blindly.** Work progressively:
1. Smoke test the pipeline (2 cases per runner)
2. Analyze existing results or run targeted diagnostics
3. Fix skills in batches of 3-5, verifying each batch
4. Save baselines from verified results

## Approach: Progressive Batched Evaluation

### Phase 1: Infrastructure + Smoke (Task .1)
Add `--limit N` flag to all 4 runners so case volume can be capped. Smoke test with `--limit 2` to verify the pipeline works end-to-end after .7/.8/.9 fixes.

### Phase 2: Analyze + Triage (Task .2)
Check existing result files in `tests/evals/results/`. If valid post-.7 results exist, analyze them directly (no new CLI calls). If not, run quick targeted diagnostics (`--limit 20` activation, `--limit 3` confusion groups). Produce a prioritized triage of failing skills.

### Phase 3: Fix Routing in Batches (Task .3)
Fix skill descriptions (frontmatter) for activation/confusion issues. Work in batches of 3-5 skills. After each batch: targeted `--skill X` re-run to verify, `validate-skills.sh` to check budget/similarity, commit.

### Phase 4: Fix Content in Batches (Task .4)
Fix skill body content for effectiveness issues. Work in batches of 3-4 skills. Use `--skill X --runs 1 --regenerate` to verify. Run L6 size impact on flagged candidates.

### Phase 5: Quality Bar Verification (Task .5)
Targeted regression check on all fixed skills. Broader sample on L3/L4 (`--limit 30-40`). Verify quality bar thresholds are met.

### Phase 6: Save Baselines (Task .6)
Save verified results as baselines. Confirm `compare_baseline.py` compatibility. Unblock fn-58.4.

## Quality Bar Thresholds

### L3 Activation
- TPR >= 75%, FPR <= 20%, Accuracy >= 70%

### L4 Confusion
- Per-group accuracy >= 60%, Cross-activation <= 35%, No never-activated skills, Negative control pass rate >= 70%

### L5 Effectiveness
- Overall win rate >= 50%, Mean improvement > 0, No 0% win rate without documented variance exception

### L6 Size Impact
- full > baseline in >= 55% of full_vs_baseline comparisons, No skill where baseline consistently beats full

## Quick Commands

```bash
# Smoke test (2 cases per runner)
python3 tests/evals/run_activation.py --limit 2
python3 tests/evals/run_confusion_matrix.py --limit 2
python3 tests/evals/run_effectiveness.py --limit 2 --runs 1
python3 tests/evals/run_size_impact.py --limit 2 --runs 1

# Targeted single-skill eval
python3 tests/evals/run_activation.py --skill dotnet-xunit
python3 tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 1

# Targeted confusion group
python3 tests/evals/run_confusion_matrix.py --group testing

# Dry-run (no CLI calls)
python3 tests/evals/run_activation.py --dry-run

# Validate skills after edits
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Scope

**In scope:**
- Adding --limit flag to eval runners for batch control
- Analyzing eval results to identify failing skills
- Fixing skill descriptions (frontmatter) for routing quality
- Fixing skill body content for effectiveness
- Saving baselines for regression tracking
- Unblocking fn-58.4

**Out of scope:**
- Adding new rubrics, test cases, or eval types
- CI workflow setup (fn-58.4)
- Full-suite unattended runs (use targeted batches instead)

## Acceptance

- [ ] All 4 runners support `--limit N` flag
- [ ] Pipeline validated via smoke test (--limit 2)
- [ ] Eval results analyzed and failing skills identified
- [ ] Skill descriptions fixed where routing results indicated problems
- [ ] Skill content improved where effectiveness showed regression vs baseline
- [ ] Quality bar thresholds met (or documented rationale for exceptions)
- [ ] Baselines saved to `tests/evals/baselines/`
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] fn-58.4 unblocked

## Risks

| Risk | Mitigation |
|------|------------|
| Existing results invalid after .7-.9 changes | Smoke test validates pipeline; re-run targeted diagnostics if needed |
| Description edits break other skills | validate-skills.sh after each batch; targeted re-runs |
| --limit produces unrepresentative samples | Proportional sampling for activation; per-entity semantics for others |
| Quality bar unachievable with haiku | Thresholds designed for haiku; documented exceptions allowed |
| Body edits invalidate generation cache | Use --regenerate flag after content changes |
