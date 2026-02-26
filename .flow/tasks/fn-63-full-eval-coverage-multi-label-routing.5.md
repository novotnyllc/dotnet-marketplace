# fn-63-full-eval-coverage-multi-label-routing.5 Rubric expansion batch 3 + remaining content fixes

## Description
Final rubric expansion batch covering all remaining skills. By end of this task, every skill that can have a rubric has one.

**Step 1: Generate rubrics batch 3 (remaining ~55 skills).**
Use `generate_rubrics.py` for all skills that still lack rubrics. This is the largest batch — work in sub-batches of ~15 skills each for the generation, then evaluate in sub-batches of 3-5.

Some skills may not be suitable for effectiveness rubrics:
- dotnet-advisor (meta-router, doesn't produce domain content)
- 4 fork-context detection skills (produce detection results, not domain advice)
- Skills where description-only is sufficient (very narrow scope)

Mark these as `content_status: "exception"` with documented rationale.

**Step 2: Run effectiveness, fix content batch 3.**
Same workflow as tasks .3/.4: run, fix below-50% in sub-batches of 3-5, verify with `--regenerate`.

**Step 3: Content audit.**
Review eval-progress.json: every skill should now have both `routing_status` and `content_status` set to something other than `untested`. Produce a summary:
- Count by status: passing / fixed / needs-fix / exception
- List any remaining `untested` skills (should be 0)
- List any remaining `needs-fix` skills (should be actively in progress or exception'd)

**Depends on:** fn-63.4
**Size:** M
**Files:**
- `skills/*/SKILL.md` (body content edits)
- `tests/evals/rubrics/*.yaml` (~55 new rubrics)
- `tests/evals/eval-progress.json`
## Acceptance
- [ ] Rubrics exist for all skills that can have them (documented exceptions for ~5 unsuitable skills)
- [ ] Effectiveness run completed for all new rubrics
- [ ] Content fixed for all skills below 50% win rate (or exception'd with rationale)
- [ ] Every skill in eval-progress.json has routing_status != "untested" AND content_status != "untested"
- [ ] Content audit summary produced: count by status, 0 remaining untested
- [ ] Each sub-batch committed separately
- [ ] `validate-skills.sh && validate-marketplace.sh` pass
- [ ] eval-progress.json fully populated for all 131 skills
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: