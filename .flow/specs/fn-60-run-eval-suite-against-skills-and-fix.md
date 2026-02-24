# Run Eval Suite Against Skills and Fix to Quality Bar

## Overview

Epic fn-58 built a comprehensive offline evaluation framework with 4 runners (activation, confusion, effectiveness, size impact), 12 rubrics, 73 activation cases, 36 confusion cases, and 11 size impact candidates. But it never actually **ran** the evals or **fixed** anything based on the results.

This epic closes the loop: run all 4 eval types against the current 131-skill catalog, analyze failures, fix skill descriptions and content until they hit a reasonable quality bar, and save initial baselines for future regression tracking.

## Quality Bar ("Good Enough" Thresholds)

These thresholds account for the inherent difficulty of each eval type and the fact that we're routing across 131 skills with a small (haiku) model. Perfect scores are not expected.

### L3 Activation
- **TPR >= 75%** -- 3/4 positive cases route to the correct skill
- **FPR <= 20%** -- negative controls mostly rejected
- **Accuracy >= 70%** -- overall correctness across positive + negative

### L4 Confusion
- **Per-group accuracy >= 60%** -- overlapping skills are inherently hard
- **Cross-activation rate <= 35%** -- some confusion is expected within groups
- **No "never-activated" skills** -- every skill in a group gets predicted at least once
- **Negative control pass rate >= 70%**

### L5 Effectiveness
- **Overall win rate >= 50%** -- enhanced beats baseline at least half the time
- **Mean improvement > 0** -- net positive across all skills
- **No individual skill has 0% win rate** (every skill should help at least sometimes)

### L6 Size Impact
- **full > baseline** in >= 55% of comparisons
- **No skill where baseline consistently beats full** (that would mean skill content is harmful)

These thresholds are deliberately achievable. If initial results are dramatically below them, it signals description/content problems to fix, not unrealistic targets. If results exceed them, great -- the bar may be raised later.

## Scope

**In scope:**
- Running all 4 eval types (activation, confusion, effectiveness, size impact)
- Analyzing results to identify worst-performing skills, descriptions, and confusion pairs
- Fixing skill frontmatter descriptions to improve activation routing
- Fixing overlapping skill descriptions to reduce cross-activation
- Improving skill content for skills with poor effectiveness scores
- Re-running evals to validate fixes
- Saving initial baseline JSON files for regression tracking
- Blocking fn-58.4 (CI workflow) on this epic's completion

**Out of scope:**
- Adding new rubrics beyond the existing 12
- Adding new activation/confusion test cases
- Setting up CI (that's fn-58.4, which this blocks)

## Approach

### Prerequisites (task .7)

**Auth**: `_common.py:get_client()` currently hard-requires `ANTHROPIC_API_KEY` env var. Fix this to let the Anthropic SDK handle auth discovery -- the local client is already authenticated and doesn't need an explicit key. The SDK checks env vars itself; the pre-validation just gets in the way.

**Skill loading**: Eval runners already load skills from `REPO_ROOT/skills/` (the local checkout). No plugin installation needed -- skills are read directly from the repo, not from any installed plugin location.

**Skill restore**: Tasks .3/.4 modify SKILL.md files. Restore mechanism is git-based:
- Commit clean state before starting fixes
- Each fix batch gets its own commit
- `git checkout -- skills/` restores any file to its committed state
- `git revert <commit>` undoes an entire fix batch if it makes things worse

### Iteration Strategy

This is an iterative improve-measure loop:

1. **Run** all 4 eval types against current skills
2. **Analyze** -- identify worst performers, common failure patterns
3. **Fix** -- targeted description edits, content improvements
4. **Re-run** -- verify improvement, check for regressions
5. **Save baselines** once thresholds are met

Expect 1-3 fix-rerun iterations. Focus on high-leverage fixes first (description clarity for activation/confusion, content quality for effectiveness).

### Cost Expectations

Using haiku for generation and judging (per config.yaml):
- Activation: ~73 API calls = ~$0.10-0.20
- Confusion: ~54 API calls = ~$0.10-0.15
- Effectiveness: ~24 generations + 24 baselines + 24 judgments = ~$1-2
- Size impact: ~36 generations + 36 judgments = ~$1-2
- Total per full run: ~$2-4
- Budget for 3 iterations: ~$12

### Fix Priority

1. **Activation failures** -- fix descriptions so the model can find skills
2. **Confusion cross-activations** -- differentiate overlapping skills
3. **Effectiveness losses** -- improve content for skills that underperform baseline
4. **Size impact anomalies** -- investigate skills where baseline beats full

## Quick Commands

```bash
# Run each eval type
python3 tests/evals/run_activation.py
python3 tests/evals/run_confusion_matrix.py
python3 tests/evals/run_effectiveness.py --runs 3
python3 tests/evals/run_size_impact.py

# Run a single skill/group
python3 tests/evals/run_activation.py --skill dotnet-xunit
python3 tests/evals/run_confusion_matrix.py --group testing
python3 tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3

# Dry-run (no API calls)
python3 tests/evals/run_activation.py --dry-run
```

## Acceptance

- [ ] All 4 eval types have been run at least once with real API calls
- [ ] Results analyzed and findings documented per task
- [ ] Skill descriptions fixed where activation/confusion results indicated problems
- [ ] Skill content improved where effectiveness results showed regression vs baseline
- [ ] Re-run results meet the quality bar thresholds above (or document rationale for exceptions)
- [ ] Initial baseline JSON files saved to `tests/evals/baselines/`
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass
- [ ] fn-58.4 unblocked (has dependency on this epic's final task)

## Risks

| Risk | Mitigation |
|------|------------|
| Auth not discoverable | Task .7 fixes `_common.py` to use SDK auth discovery; no explicit key needed |
| Skill modifications need restore | Git-based: commit before fixes, `git checkout -- skills/` to restore |
| Cost overrun from multiple iterations | Haiku pricing is cheap (~$3/run); generation caching avoids re-generation |
| Fixing one skill breaks another | Re-run full suite after each fix batch; baselines track regressions |
| Quality bar too high for haiku | Thresholds designed for haiku; can lower if systematically unachievable |
| Description changes break copilot smoke tests | Run `validate-skills.sh` after each change batch |
