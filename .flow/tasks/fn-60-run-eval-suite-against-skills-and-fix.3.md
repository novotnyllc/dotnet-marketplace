# fn-60.3 Fix routing descriptions in batches with verification

## Description

Fix skill descriptions (frontmatter) to improve L3 activation routing and L4 confusion disambiguation. Work in batches of 3-5 skills. After each batch: verify with targeted `--skill` re-runs, run `validate-skills.sh` to check budget/similarity, and commit.

**Depends on:** fn-60.2
**Size:** M
**Files:**
- `skills/*/SKILL.md` (frontmatter description edits only — NOT body content)
- `tests/evals/results/` (targeted re-run results)
- `tests/evals/eval-progress.json` (read for batch selection, update after each batch)

## Approach

### Batch workflow (repeat for each batch of 3-5 skills)

1. **Select batch**: Pick 3-5 skills from the triage priority list (task .2 output)
2. **Edit descriptions**: Modify the `description:` frontmatter field in each skill's SKILL.md
   - Follow routing style guide at `docs/skill-routing-style-guide.md`
   - Action + Domain + Differentiator formula
   - Keep under 120 chars per description
3. **Validate**: `./scripts/validate-skills.sh` — check budget (12K warn / 15.6K fail), similarity, and frontmatter
4. **Verify with targeted re-runs**:
   - L3: `python3 tests/evals/run_activation.py --skill <name>` for each edited skill
   - L4: `python3 tests/evals/run_confusion_matrix.py --group <group>` for affected confusion groups
5. **Update eval-progress.json**: For each edited skill, set `status` to `fixed`, record `agent` (use `RALPH_SESSION_ID` env var if set, else `"manual"`), add the re-run `run_ids`, and note what was changed
6. **Commit batch**: `git add skills/*/SKILL.md tests/evals/eval-progress.json && git commit -m "fix(skills): improve routing for <batch summary>"`

### Constraints

- **Budget neutral**: Total description budget must not increase from pre-fix baseline (target staying under 12,000 chars). Check in validate-skills.sh.
- **Similarity compliance**: Must not re-introduce similarity violations cleared by fn-53. Check via `scripts/similarity-baseline.json`.
- **Description only**: Do NOT edit skill body content in this task — that's task .4. Isolating description vs content changes allows attribution of improvements.

### Expected batch count

Based on typical triage findings: 2-3 batches of 3-5 skills each (6-15 total edits). The exact count depends on task .2 findings.

## Key context

- Confusion runner uses `--group <name>`, not `--skill`. Groups are domain categories (e.g., "testing", "api", "security").
- Activation `--skill <name>` also includes all 18 negative controls alongside the filtered skill's cases. This is expected — it tests that the model doesn't falsely activate on negatives.
- Description edits don't invalidate effectiveness/size_impact generation caches (those keys include body hash, not description).

## Acceptance

- [ ] All priority-1 routing skills from triage (task .2) have been fixed
- [ ] Each batch verified with targeted `--skill` (activation) and `--group` (confusion) re-runs
- [ ] `./scripts/validate-skills.sh` passes after each batch (budget + similarity + frontmatter)
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] Total description budget is neutral or reduced (no increase from pre-fix baseline)
- [ ] Each batch committed separately with descriptive message
- [ ] Re-run results saved in `tests/evals/results/` with descriptive filenames
- [ ] Targeted L3 activation re-runs show improvement for edited skills (activation rate up or misrouting resolved)
- [ ] L4 confusion re-runs show improvement for affected groups (per-group accuracy up or cross-activation down)
- [ ] `eval-progress.json` updated after each batch with agent ID, run_ids, and status

## Done summary

## Evidence
- Commits:
- Tests:
- PRs:
