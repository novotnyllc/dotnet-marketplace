# fn-63-full-eval-coverage-multi-label-routing.6 Full-coverage verification + save baselines

## Description
Final verification across all 131 skills and baseline generation.

**Step 1: Full-coverage activation verification.**
Run activation eval with all test cases (no --limit). Verify quality bar:
- Mean F1 >= 0.70 across all positive cases
- Per-case precision >= 0.50
- FPR <= 20% on negative controls
- No skill with 0% recall across all its test cases

If any threshold missed: investigate specific failing cases, fix or exception.

**Step 2: Full-coverage effectiveness verification.**
Run effectiveness for ALL rubric'd skills with `--runs 3` for statistical confidence. Verify:
- No skill at 0% win rate without documented exception (min n=6 judged cases)
- Per-skill win rate >= 50%
- Compute and report aggregate micro-average win rate

If threshold missed: fix content or refine rubric, re-run with `--regenerate`.

**Step 3: Size impact verification.**
Run size impact on expanded candidate list (add candidates for newly rubric'd skills). Verify:
- No baseline sweep (no skill where baseline wins all runs)
- full > baseline in >= 55% of comparisons

**Step 4: Save baselines.**
- Run each eval type in full-coverage mode (no --limit, --runs 3 for L5/L6)
- Save results to `tests/evals/baselines/`
- Verify `compare_baseline.py` compatibility with new multi-label activation format

**Step 5: Final audit.**
- eval-progress.json: all 131 skills should be `verified` or `exception`
- Set routing_status/content_status to `verified` for all passing skills
- Document all exceptions with rationale
- Confirm fn-58.4 (CI regression gate) is unblocked

**Note:** This task may need fn-62 complete for full-coverage runs. If subprocess timeouts persist, break into targeted batches and aggregate results.

**Depends on:** fn-63.5
**Size:** M
**Files:**
- `tests/evals/results/` (full-coverage results)
- `tests/evals/baselines/` (saved baselines)
- `tests/evals/eval-progress.json` (final audit)
- `tests/evals/datasets/size_impact/candidates.yaml` (expanded candidates)
## Acceptance
- [ ] Full-coverage activation run completed: mean F1 >= 0.70, FPR <= 20%, no 0-recall skills
- [ ] Full-coverage effectiveness run completed (--runs 3): all per-skill win rates >= 50% (or exception'd)
- [ ] Size impact verified: no baseline sweep, full > baseline >= 55%
- [ ] Baselines saved to tests/evals/baselines/
- [ ] compare_baseline.py works with new multi-label activation format
- [ ] eval-progress.json: all 131 skills verified or exception'd (0 untested, 0 needs-fix)
- [ ] All exceptions documented with rationale
- [ ] `validate-skills.sh && validate-marketplace.sh` pass
- [ ] fn-58.4 unblocked (baselines exist for CI regression gate)
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: