# fn-60.4 Fix effectiveness content and L6 issues in batches

## Description

Fix skill body content for skills with poor L5 effectiveness scores. Also address L6 size impact issues where baseline beats full. Work in batches of 3-4 skills. Use `--skill X --runs 1 --regenerate` to verify each batch.

**Depends on:** fn-60.3
**Size:** M
**Files:**
- `skills/*/SKILL.md` (body content edits -- sections below frontmatter)
- `tests/evals/results/` (targeted re-run results)
- `tests/evals/eval-progress.json` (read for batch selection, update after each batch)

## Approach

### Effectiveness fix workflow (batches of 3-4 skills)

1. **Select batch**: Pick 3-4 skills where `content_status == "needs-fix"` from eval-progress.json. Prioritize 0% win rate skills first. Use the rubric failure mode pre-analysis from triage (task .2) to inform which criteria to target.
2. **Analyze failure mode**: Read the skill's rubric YAML (`tests/evals/rubrics/<skill>.yaml`) to understand what the eval tests. Read the effectiveness result details to see what the baseline does better.
3. **Edit content**: Improve the skill body in SKILL.md. Focus on the specific rubric criteria the skill is failing on.
4. **Verify**: `python3 tests/evals/run_effectiveness.py --skill <name> --runs 1 --regenerate`
   - MUST use `--regenerate` after body edits (cache keys include body hash; stale cache = false results)
   - With `--runs 1`: 2 prompts per skill = 6 CLI calls (2 generations + 2 baselines + 2 judge calls)
5. **Validate**: `./scripts/validate-skills.sh` -- ensure no structural regressions
6. **Update eval-progress.json**: For each edited skill in `skills[skill_name]`:
   - Set `content_status` to `fixed` (do NOT change `routing_status`)
   - Append `".4"` to `fixed_tasks`
   - Set `fixed_by` to commit SHA, `fixed_at` to ISO timestamp
   - Record `agent`, add re-run `run_ids`, update `notes`
   - Recompute `overall_status`
7. **Commit batch**: `git add skills/*/SKILL.md tests/evals/eval-progress.json && git commit -m "fix(skills): improve effectiveness for <batch summary>"`

### Size impact fix workflow (if flagged in triage)

For candidates where baseline consistently beats full (sweeps all runs):
1. Investigate: is the full content introducing noise that confuses the model?
2. Fix: trim or restructure the body content
3. Verify: `python3 tests/evals/run_size_impact.py --skill <name> --runs 1 --regenerate`

### Expected scope

- L5 priority: ~4 skills at 0% win rate, ~3-4 more below 50% = 2-3 batches
- L6 priority: ~2 candidates flagged = 1 batch
- Total CLI calls: ~60-90 (6 calls per skill x 10-15 skills)

## Key context

- **MUST use --regenerate after body edits** -- effectiveness and size_impact cache generations keyed by body hash. Without --regenerate, stale cached outputs produce meaningless comparisons. (Memory pitfall: generation cache keys must include ALL inputs that affect output.)
- Description edits from task .3 do NOT invalidate these caches (description is not in the hash). Only body content changes require --regenerate.
- L5 quality bar: no skill at 0% win rate (unless documented variance exception with n=6 cases). Per-skill target >= 50% win rate. L6: no candidate where baseline sweeps all runs.

## Acceptance

- [ ] All 0% win rate skills from triage (task .2) have been fixed or documented as variance exceptions
- [ ] Each batch verified with `--skill X --runs 1 --regenerate` (effectiveness)
- [ ] L6 flagged candidates addressed (no baseline sweep remaining, or documented rationale)
- [ ] `--regenerate` used on every re-run after body edits (no stale cache results)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] Each batch committed separately with descriptive message
- [ ] Re-run results saved in `tests/evals/results/` (referenced by run_id in eval-progress.json)
- [ ] No NEW 0% win rate skills introduced by the changes
- [ ] `eval-progress.json` updated: `skills[name].content_status = "fixed"`, `fixed_tasks` includes `".4"`, `fixed_by`, `fixed_at`

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
