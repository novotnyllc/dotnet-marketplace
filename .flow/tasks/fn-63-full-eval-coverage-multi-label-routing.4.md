# fn-63-full-eval-coverage-multi-label-routing.4 Rubric expansion batch 2 + content fixes

## Description
Continue rubric expansion and content fixes. Second batch of ~30 skills.

**Step 1: Generate rubrics batch 2 (~30 skills).**
Use `generate_rubrics.py` from task .3 for the next priority tranche. Same quality criteria: domain-specific, weighted, schema-validated.

**Step 2: Run effectiveness, fix content batch 2.**
For each newly rubric'd skill: run `--skill X --runs 1 --regenerate`. Fix content for skills below 50% win rate in sub-batches of 3-5:
- Analyze why baseline outperforms (noise, low signal-to-noise, contradicts model knowledge)
- Trim or restructure body content for signal density
- MUST use `--regenerate` after body edits (cache keys include body hash)
- Verify fix with targeted re-run
- Update eval-progress.json: content_status to `fixed`

**Step 3: Refine suspicious rubrics.**
Flag rubrics that produce suspicious results:
- 100% win rate across all prompts = rubric criteria too easy or generic → tighten criteria
- 0% win rate = rubric criteria impossible or misaligned with skill content → rewrite or exception
- Verify refined rubrics with re-runs

Progress checkpoint: ~72 skills should have rubrics (12 original + ~30 from .3 + ~30 from .4).

**Depends on:** fn-63.3
**Size:** M
**Files:**
- `skills/*/SKILL.md` (body content edits)
- `tests/evals/rubrics/*.yaml` (~30 new + refined rubrics)
- `tests/evals/eval-progress.json`
## Acceptance
- [ ] ~30 additional rubrics generated and validated
- [ ] Effectiveness run completed for all new rubrics
- [ ] Content fixed for skills below 50% win rate (batch 2)
- [ ] Suspicious rubrics (100% or 0% win rate) flagged and refined
- [ ] MUST use --regenerate on every re-run after body edits
- [ ] Each sub-batch committed separately
- [ ] `validate-skills.sh && validate-marketplace.sh` pass
- [ ] eval-progress.json updated for all processed skills
- [ ] Progress: ~72 skills with rubrics total
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: