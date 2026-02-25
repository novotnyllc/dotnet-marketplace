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

List result files in `tests/evals/results/`. For each eval type, check validity:
- `meta.backend` must NOT be `"anthropic-sdk"` (pre-.7). Valid backends include `"claude"`, `"codex"`, `"copilot"`, or any non-SDK backend.
- `meta.limit` must be absent or `null` for full-coverage runs (partial runs are usable for triage signal but not for baselines)
- Compare `summary` case/skill counts against expected dataset sizes:
  - Activation: 73 total cases (core_skills + negative_controls + specialized_skills)
  - Confusion: 7 groups, 36 group cases + 18 negative controls
  - Effectiveness: 12 rubric'd skills
  - Size impact: 11 candidates
- If `suite_summary.json` exists, prefer it as the centralized per-run status

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

**L4 Confusion** (quality bar: per-group>=60%, cross-activation<=35%, no never-activated, negative controls>=70%):
- List groups below 60% accuracy
- Identify cross-activation pairs and compute cross-activation rate
- Flag never-activated skills within groups
- Check negative control pass rates

**L5 Effectiveness** (quality bar: per-skill win_rate>=50%, no 0% without exception):
- List skills with 0% win rate (priority fixes)
- List skills below 50% win rate
- Identify common content quality issues
- **For each L5-failing skill**: read the rubric YAML and note which criteria are likely failing and why (rubric failure mode pre-analysis). This accelerates task .4 batch selection.

**L6 Size Impact** (quality bar: full>baseline in 55%+, no baseline sweep):
- Flag skills where baseline consistently beats full (sweeps all runs)
- Identify candidates where full content may be harmful

### Step 4: Write triage document

Create `tests/evals/results/triage.md` with:
- Summary of current state vs quality bar
- Priority 1 fixes (blocking quality bar)
- Priority 2 fixes (improvement opportunities)
- Specific skills to fix in each category
- Recommended batch order for .3 and .4
- **For L5 skills**: rubric failure mode analysis (which criteria fail, likely causes) so .4 batches start faster

### Step 5: Initialize eval-progress.json

Populate `tests/evals/eval-progress.json` under the `skills` key. Each entry uses per-dimension status tracking so .3/.4/.5 can independently track routing vs content fixes.

Entry schema at `skills[skill_name]`:
- `routing_status`: one of `untested`, `passing`, `needs-fix`, `fixed`, `verified`, `exception`
- `content_status`: one of `untested`, `passing`, `needs-fix`, `fixed`, `verified`, `exception`
- `overall_status`: derived from routing_status and content_status (both must be `passing`/`verified`/`exception` for overall to be `passing`)
- `fixed_tasks`: list of task IDs that edited this skill (e.g., `[".3", ".4"]`) -- provenance for .5 verification
- `eval_types`: which eval types have been run against this skill
- `agent`: the agent/session ID that last evaluated it (use `RALPH_SESSION_ID` env var if set, else `"manual"`)
- `run_ids`: list of result file run_ids where this skill appeared
- `notes`: brief description of the issue
- `fixed_by`: null (populated by .3/.4 when fixed -- commit SHA)
- `fixed_at`: null (populated by .3/.4 when fixed -- ISO timestamp)

Example structure:
```json
{
  "skills": {
    "dotnet-xunit": {
      "routing_status": "passing",
      "content_status": "needs-fix",
      "overall_status": "needs-fix",
      "fixed_tasks": [],
      "eval_types": ["activation", "confusion", "effectiveness"],
      "agent": "manual",
      "run_ids": ["activation_abc123", "effectiveness_def456"],
      "notes": "0% win rate on effectiveness; rubric criteria X and Y likely failing",
      "fixed_by": null,
      "fixed_at": null
    }
  }
}
```

**Status transition rules:**
- Task .3 sets `routing_status` to `fixed` (does NOT change `content_status`)
- Task .4 sets `content_status` to `fixed` (does NOT change `routing_status`)
- Task .5 sets `routing_status`/`content_status` to `verified` after re-verification
- `overall_status` is recomputed on each update: `passing` only when all non-`untested` dimensions are `passing`/`verified`/`exception`

This file is committed with the triage document and read by subsequent tasks (.3, .4, .5) to know what has been addressed and what remains.

## Key context

Existing results may show: L3 TPR=69%, FPR=28%, Accuracy=70% (below thresholds). L4 mostly passing. L5 has 4 skills at 0% win rate. L6 has 2 candidates where baseline beats full.

## Acceptance

- [ ] Existing result files inventoried (count per eval type, validity checked via `meta.backend != "anthropic-sdk"` and case counts)
- [ ] If no valid results exist, targeted diagnostics run with --limit (not full suite)
- [ ] Triage document written to `tests/evals/results/triage.md`
- [ ] L3 activation: specific failing skills listed with activation rates
- [ ] L4 confusion: groups below threshold listed, cross-activation rates computed, never-activated skills flagged
- [ ] L5 effectiveness: 0% win rate skills identified, below-50% skills listed, rubric failure modes analyzed
- [ ] L6 size impact: baseline-beats-full candidates flagged
- [ ] Priority batches defined for tasks .3 (routing fixes) and .4 (content fixes)
- [ ] Total CLI calls for this task documented (should be 0 if reusing existing results, ~68 max if diagnostics needed)
- [ ] `eval-progress.json` populated with per-dimension status tracking (`routing_status`, `content_status`, `fixed_tasks`)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass (no skill changes yet)

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
