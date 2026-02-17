# fn-49-skill-guide-compliance-review.2 Fix non-compliant skills identified in audit

## Description
Fix all critical and warning findings from the audit in fn-49.1. Batch fixes by category.

**Size:** M (scope depends on audit findings — may need splitting)
**Files:** Multiple `SKILL.md` files, agent `.md` files, `CONTRIBUTING-SKILLS.md`

## Approach

- Fix critical findings first (structural issues, missing sections)
- Fix warning findings (depth gaps, cross-reference gaps, trigger pattern gaps)
- Update `CONTRIBUTING-SKILLS.md` if skill guide introduces conventions not yet documented
- Batch by category to stay efficient
- If >30 skills need fixes: split into fn-49.2a (critical) and fn-49.2b (warnings) with separate PRs

## Key context

- Preserve existing content; restructure, do not rewrite from scratch
- Stay within description budget (~12,000 char warn threshold)
## Approach

- Fix critical findings first (structural issues, missing sections)
- Fix warning findings (depth gaps, cross-reference gaps, trigger pattern gaps)
- Update `CONTRIBUTING-SKILLS.md` if the skill guide introduces conventions not yet documented
- Batch by category to stay efficient

## Key context

- This task scope is determined by fn-49.1 findings — may be split further if findings are extensive
- Preserve existing content; restructure, do not rewrite from scratch
- Stay within description budget (~12,000 char warn threshold)
## Acceptance
- [ ] All critical findings fixed
- [ ] All warning findings fixed (or split into fn-49.2b if >30 skills)
- [ ] CONTRIBUTING-SKILLS.md updated if new conventions discovered
- [ ] No skill descriptions exceed 120 characters
- [ ] All validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
