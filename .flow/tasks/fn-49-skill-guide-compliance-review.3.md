# fn-49-skill-guide-compliance-review.3 Update validation scripts and verify all fixes pass

## Description
Add any new structural checks to `validate-skills.sh` that were identified in the audit. Verify all fixes from fn-49.2 pass validation.

**Size:** S
**Files:** `scripts/validate-skills.sh`, `scripts/_validate_skills.py`

## Approach

- Review audit findings for checkable patterns (e.g., section headers, word count ranges)
- Add validation checks that are automatable and deterministic
- Run full validation suite to confirm all fixes pass
- Update `--projected-skills` count if skills were added/removed

## Key context

- Validation must be: single-pass, no subprocesses, no network, same locally and in CI
- Do not add checks that are subjective or require content understanding
## Acceptance
- [ ] New structural checks added to validation scripts (if applicable)
- [ ] All four validation scripts pass with all fn-49.2 fixes
- [ ] `--projected-skills` count accurate
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
