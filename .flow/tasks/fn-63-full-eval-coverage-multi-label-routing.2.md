# fn-63-full-eval-coverage-multi-label-routing.2 Full activation eval, init progress, fix routing batch 1

## Description
Run activation eval across ALL test cases (existing 73 + ~150 auto-generated from task .1) and fix routing for the first batch of failing skills.

**Step 1: Run full activation eval.**
Execute `python3 tests/evals/run_activation.py` with all cases. Capture per-case F1/precision/recall. Use targeted `--skill` runs if full run hits timeout issues (fn-62 workaround).

**Step 2: Initialize eval-progress.json for all 131 skills.**
Add entries for all 131 skills (currently only 21 tracked). New entries start with `routing_status: "untested"`, `content_status: "untested"`. Preserve existing entries and their status. Set routing_status based on activation results:
- F1 >= 0.70 for all cases → `passing`
- F1 < 0.70 or 0 recall → `needs-fix`
- No test cases (fork-context skills) → `exception` with documented rationale

**Step 3: Triage failures.**
Sort failing skills by severity:
1. Skills with 0% recall (never activate) — highest priority
2. Skills with low precision (activate on wrong prompts) — high priority
3. Skills with moderate F1 but room for improvement — medium priority
Generate a triage summary in the task's done notes.

**Step 4: Fix routing descriptions batch 1 (~20-25 skills).**
Work in sub-batches of 3-5 skills:
- Edit `description:` frontmatter in SKILL.md
- Follow routing style guide at `docs/skill-routing-style-guide.md`
- Put differentiators early (first ~80 chars — routing index truncates at 120)
- Run `validate-skills.sh` after each sub-batch
- Verify with targeted `--skill` re-runs
- Update eval-progress.json: set routing_status to `fixed`, record commit SHA
- Commit each sub-batch separately

Process ~20-25 skills (the highest-priority half). Task .3 handles the rest.

**Depends on:** fn-63.1
**Size:** M
**Files:**
- `tests/evals/eval-progress.json` (expand to 131 skills + update routing_status)
- `skills/*/SKILL.md` (description edits for ~20-25 skills)
- `tests/evals/results/` (activation results)
## Acceptance
- [ ] Full activation eval run completed (all test cases, including auto-generated)
- [ ] eval-progress.json expanded to all 131 skills (no skill missing)
- [ ] Triage summary produced: skills sorted by severity (0-recall, low-precision, moderate-F1)
- [ ] ~20-25 highest-priority routing issues fixed in sub-batches of 3-5
- [ ] Each sub-batch verified with targeted `--skill` activation re-runs
- [ ] `validate-skills.sh` passes after each sub-batch (budget + similarity + frontmatter)
- [ ] `validate-marketplace.sh` passes
- [ ] Description budget neutral or reduced (no increase from pre-fix baseline)
- [ ] Each sub-batch committed separately with descriptive message
- [ ] eval-progress.json updated: fixed skills have routing_status = "fixed", fixed_by commit SHA, fixed_at timestamp
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: