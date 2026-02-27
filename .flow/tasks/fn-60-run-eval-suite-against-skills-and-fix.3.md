# fn-60.3 Fix routing descriptions in batches with verification

## Description

Fix skill descriptions (frontmatter) to improve L3 activation routing. Work in batches of 3-5 skills. After each batch: verify with targeted `--skill` re-runs, run `validate-skills.sh` to check budget/similarity, and commit.
<!-- Updated by plan-sync: fn-60.2 found L4 confusion already passing (all 7 groups >= 60%). No confusion disambiguation fixes needed; focus is L3 activation only. -->

**Depends on:** fn-60.2
**Size:** M
**Files:**
- `skills/*/SKILL.md` (frontmatter description edits only -- NOT body content)
- `tests/evals/results/` (targeted re-run results)
- `tests/evals/eval-progress.json` (read for batch selection, update after each batch)

## Approach

### Batch workflow (repeat for each batch of 3-5 skills)

1. **Select batch**: Pick 3-5 skills from the triage priority list where `routing_status == "needs-fix"` (task .2 output)
2. **Edit descriptions**: Modify the `description:` frontmatter field in each skill's SKILL.md
   - Follow routing style guide at `docs/skill-routing-style-guide.md`
   - Action + Domain + Differentiator formula
   - **Put the differentiator early (first ~80 chars)** -- routing indices truncate descriptions at 120 chars with `...`. Differentiators placed late will never influence routing.
   - Keep under 120 chars per description
3. **Validate**: `./scripts/validate-skills.sh` -- check budget (12K warn / 15.6K fail), similarity, and frontmatter
4. **Verify with targeted re-runs**:
   - L3: `python3 tests/evals/run_activation.py --skill <name>` for each edited skill
   - L4: `python3 tests/evals/run_confusion_matrix.py --group <group>` for affected confusion groups
5. **Update eval-progress.json**: For each edited skill in `skills[skill_name]`:
   - Set `routing_status` to `fixed` (do NOT change `content_status`)
   - Append `".3"` to `fixed_tasks`
   - Set `fixed_by` to commit SHA, `fixed_at` to ISO timestamp
   - Record `agent`, add re-run `run_ids`, update `notes`
   - Recompute `overall_status`
6. **Commit batch**: `git add skills/*/SKILL.md tests/evals/eval-progress.json && git commit -m "fix(skills): improve routing for <batch summary>"`

### Constraints

- **Budget neutral**: Total description budget must not increase from pre-fix baseline (target staying under 12,000 chars). Check in validate-skills.sh.
- **Similarity compliance**: Must not re-introduce similarity violations cleared by fn-53. Check via `scripts/similarity-baseline.json`.
- **Description only**: Do NOT edit skill body content in this task -- that is task .4. Isolating description vs content changes allows attribution of improvements.

### Expected batch count
<!-- Updated by plan-sync: fn-60.2 found 5 routing skills, not 6-15 -->

Per triage (task .2): 5 skills in 2 batches:
- **Batch 1** (3 skills -- false positives, highest impact): `dotnet-container-deployment`, `dotnet-messaging-patterns`, `dotnet-architecture-patterns`
- **Batch 2** (2 skills -- false negatives, moderate impact): `dotnet-system-commandline`, `dotnet-resilience`

None of these 5 routing-fix skills appear in the confusion matrix dataset. Confusion verification (`--group`) is not applicable; use activation-only targeted runs.

## Key context

- Confusion runner uses `--group <name>`, not `--skill`. Groups are domain categories (e.g., "testing", "api", "security").
- Activation `--skill <name>` also includes all 18 negative controls alongside the filtered skill's cases. This is expected -- it tests that the model does not falsely activate on negatives.
- Description edits do not invalidate effectiveness/size_impact generation caches (those keys include body hash, not description).

## Acceptance

- [ ] All priority-1 routing skills from triage (task .2) have been fixed
- [ ] Each batch verified with targeted `--skill` (activation) and `--group` (confusion) re-runs
- [ ] `./scripts/validate-skills.sh` passes after each batch (budget + similarity + frontmatter)
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] Total description budget is neutral or reduced (no increase from pre-fix baseline)
- [ ] Each batch committed separately with descriptive message
- [ ] Re-run results saved in `tests/evals/results/` (referenced by run_id in eval-progress.json)
- [ ] Targeted L3 activation re-runs show improvement for edited skills (activation rate up or misrouting resolved)
- [ ] L4 confusion re-runs show improvement for affected groups (per-group accuracy up or cross-activation down)
- [ ] `eval-progress.json` updated: `skills[name].routing_status = "fixed"`, `fixed_tasks` includes `".3"`, `fixed_by`, `fixed_at`

## Done summary
Fixed routing descriptions for 5 skills in 2 batches with targeted verification. Batch 1 (container-deployment, messaging-patterns, architecture-patterns) committed in 5a00da0. Batch 2 (system-commandline, resilience) committed in 92fb8b8/46db510. 4 of 5 skills verified as fixed via targeted activation re-runs; dotnet-messaging-patterns remains needs-fix (neg-018 partially improved but still failing). eval-progress.json updated with accurate status, run_ids referencing post-fix verification runs, and commit evidence. Budget neutral at 11683 chars (OK, under 12000).
## Evidence
- Commits: 5a00da0, 92fb8b8, 2c99165, 46db510, de9b8e7
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: