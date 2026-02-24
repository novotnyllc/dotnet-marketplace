# fn-60.4 Fix effectiveness issues for low-scoring skills

## Description

Based on the analysis from task .2, improve skill content for skills where the enhanced (with-skill) output loses to or ties with the baseline (without-skill) output in L5 effectiveness evals.

**Size:** M
**Files:**
- `skills/*/SKILL.md` -- content improvements for underperforming skills (body, not frontmatter)

## Approach

### Content Fixes
- For skills with 0% win rate: investigate what the judge criteria expect vs what the skill provides
- For skills with <50% win rate: identify which criteria the skill loses on (per_criterion_breakdown)
- Common patterns to check:
  - Skill content is too generic (not specific enough for the eval prompts)
  - Skill content is outdated (references old APIs or patterns)
  - Skill content lacks concrete examples that would help generation
  - Scope section doesn't cover the test prompt topic

### Fix Strategy
- Prioritize skills where wins_enhanced=0 (total failures)
- For partial failures: check which rubric criteria drive the losses
- Add or improve examples, code patterns, or specific guidance
- Do NOT rewrite entire skills -- targeted improvements only

### Validation
- Spot-check individual skills: `python3 tests/evals/run_effectiveness.py --skill <name> --runs 3 --regenerate`
- `./scripts/validate-skills.sh` after changes

## Acceptance
- [ ] All skills with 0% win rate from .2 analysis have been investigated and improved
- [ ] Skills with <50% win rate have targeted content improvements
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] Individual skill re-runs show improvement (documented in done summary)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
