# fn-60.2 Analyze eval results and triage failing skills

## Description

Check existing result files from prior runs. If valid post-.7 results exist, analyze them directly without new CLI calls. If not, run targeted diagnostics with `--limit` to get quick signal. Produce a prioritized triage document listing which skills need routing fixes (L3/L4) and which need content fixes (L5/L6).

**Depends on:** fn-60.1
**Size:** M
**Files:**
- `tests/evals/results/` (read existing results)
- `tests/evals/results/triage.md` (new: triage document)
- `tests/evals/eval-progress.json` (initialize with triage findings)

## Approach

### Step 1: Inventory existing results

List result files in `tests/evals/results/`. For each eval type, check:
- Does a non-aborted result exist (`ABORTED=0` in meta or full case count)?
- Was it produced with the current CLI-based runner (post-.7)?
- Check `meta.backend` field — should be `claude` (not `anthropic-sdk` which was pre-.7)

### Step 2: Quick targeted diagnostic (if needed)

If existing results are missing or pre-.7, run targeted diagnostics:
- L3 activation: `--limit 20` (~20 CLI calls) for a representative sample
- L4 confusion: `--limit 3` (3 groups, ~15 CLI calls) for group-level signal
- L5 effectiveness: `--limit 4 --runs 1` (4 skills, ~24 CLI calls) for quick signal
- L6 size impact: `--limit 3 --runs 1` (3 candidates, ~9 CLI calls)

Total worst case: ~68 CLI calls for diagnostic coverage.

### Step 3: Triage analysis

For each eval type, extract findings:

**L3 Activation** (quality bar: TPR>=75%, FPR<=20%, Accuracy>=70%):
- List skills with lowest activation rates
- List cases where wrong skill was activated
- Identify description patterns causing misrouting

**L4 Confusion** (quality bar: per-group>=60%, no never-activated):
- List groups below 60% accuracy
- Identify cross-activation pairs
- Flag never-activated skills within groups

**L5 Effectiveness** (quality bar: win_rate>=50%, no 0% without exception):
- List skills with 0% win rate (priority fixes)
- List skills below 50% win rate
- Identify common content quality issues

**L6 Size Impact** (quality bar: full>baseline in 55%+):
- Flag skills where baseline consistently beats full
- Identify candidates where full content may be harmful

### Step 4: Write triage document

Create `tests/evals/results/triage.md` with:
- Summary of current state vs quality bar
- Priority 1 fixes (blocking quality bar)
- Priority 2 fixes (improvement opportunities)
- Specific skills to fix in each category
- Recommended batch order for .3 and .4

### Step 5: Initialize eval-progress.json

Populate `tests/evals/eval-progress.json` with an entry per skill from triage findings. Each entry records:
- `eval_types`: which eval types have been run against this skill (from existing results)
- `status`: one of `untested`, `passing`, `needs-routing-fix`, `needs-content-fix`, `fixed`, `exception`
- `agent`: the agent/session ID that last evaluated it (use `RALPH_SESSION_ID` env var if set, else `"manual"`)
- `run_ids`: list of result file run_ids where this skill appeared
- `fix_task`: which task is responsible for fixing (`.3` for routing, `.4` for content)
- `notes`: brief description of the issue

This file is committed with the triage document and read by subsequent tasks (.3, .4, .5) to know what's been done and what remains.

## Key context

Existing results may show: L3 TPR=69%, FPR=28%, Accuracy=70% (below thresholds). L4 mostly passing. L5 has 4 skills at 0% win rate. L6 has 2 candidates where baseline beats full.

## Acceptance

- [ ] Existing result files inventoried (count per eval type, post-.7 validity checked)
- [ ] If no valid results exist, targeted diagnostics run with --limit (not full suite)
- [ ] Triage document written to `tests/evals/results/triage.md`
- [ ] L3 activation: specific failing skills listed with activation rates
- [ ] L4 confusion: groups below threshold listed, never-activated skills flagged
- [ ] L5 effectiveness: 0% win rate skills identified, below-50% skills listed
- [ ] L6 size impact: baseline-beats-full candidates flagged
- [ ] Priority batches defined for tasks .3 (routing fixes) and .4 (content fixes)
- [ ] Total CLI calls for this task documented (should be 0 if reusing existing results, ~68 max if diagnostics needed)
- [ ] `eval-progress.json` populated with per-skill entries from triage findings
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass (no skill changes yet)

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
