# fn-63-full-eval-coverage-multi-label-routing.3 Fix routing batch 2 + start rubric expansion

## Description
Continue routing fixes for remaining failing skills from task .2's triage, then start expanding effectiveness rubrics.

**Step 1: Fix remaining routing issues (~20-25 skills).**
Pick up where task .2 left off. Same sub-batch workflow: 3-5 skills per batch, edit descriptions, validate, verify with targeted `--skill` runs, commit.

All skills should have `routing_status != "untested"` in eval-progress.json by end of this step (either `passing`, `fixed`, or `exception`).

**Step 2: Generate effectiveness rubrics batch 1 (~30 skills).**
Write `tests/evals/scripts/generate_rubrics.py` that:
- Reads skill SKILL.md body content
- Extracts key concepts, API names, patterns, and best practices
- Uses LLM (haiku) to generate rubric YAML: 2-3 test_prompts + 3-5 weighted criteria
- Criteria must be specific to the skill's domain (not generic "produces correct code")
- Weights must sum to 1.0 ± 0.01
- Validates against `rubric_schema.yaml`
- Outputs to `tests/evals/rubrics/<skill-name>.yaml`

Prioritize rubrics for:
1. Skills with highest activation rates (most frequently routed to)
2. Skills with largest body content (most to evaluate)
3. Skills in existing fn-60 eval-progress.json with `content_status: "needs-fix"`

**Step 3: Run effectiveness on new rubrics, fix content batch 1 (~10-15 skills).**
For each newly rubric'd skill: run `--skill X --runs 1 --regenerate`, check win_rate. Fix content for skills below 50% win rate in sub-batches of 3-5. Update eval-progress.json content_status.

**Depends on:** fn-63.2
**Size:** M
**Files:**
- `skills/*/SKILL.md` (description + body edits)
- `tests/evals/scripts/generate_rubrics.py` (new)
- `tests/evals/rubrics/*.yaml` (~30 new rubrics)
- `tests/evals/eval-progress.json`
## Acceptance
- [ ] All remaining routing failures from task .2 triage addressed (fixed or exception'd)
- [ ] All 131 skills have routing_status != "untested" in eval-progress.json
- [ ] `generate_rubrics.py` script exists and produces valid rubric YAML
- [ ] ~30 new effectiveness rubrics generated and validated against schema
- [ ] Effectiveness run completed for new rubrics
- [ ] Content fixed for skills below 50% win rate (batch 1)
- [ ] Each sub-batch committed separately
- [ ] `validate-skills.sh && validate-marketplace.sh` pass
- [ ] eval-progress.json updated: content_status set for rubric'd skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
