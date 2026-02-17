# fn-49-skill-guide-compliance-review.3 Enhance validation scripts for ongoing quality enforcement

## Description
Enhance `scripts/_validate_skills.py` to enforce the quality standards established in Tasks 1-2, preventing regression on front matter quality.

**Size:** M
**Files:** `scripts/_validate_skills.py`, `scripts/validate-skills.sh`

## Approach

1. Add name-directory consistency check: verify `name` field matches the skill's directory name
2. Add extra-frontmatter detection: warn on any fields beyond `name` and `description`
3. Add description quality heuristics: detect common filler phrases, missing technology keywords
4. Keep all checks as warnings (not errors) to avoid breaking CI for edge cases
5. Update `validate-skills.sh` thresholds if needed
6. Ensure no existing validation behavior changes (backward compatible)

### New Checks to Add

| Check | Type | Implementation |
|-------|------|----------------|
| Name-directory match | Warning | Compare `name` value to last path segment of skill directory |
| Extra frontmatter fields | Warning | Flag any field not in `{name, description}` |
| Filler phrase detection | Warning | Check for common filler patterns: "helps with", "guide to", "complete guide" |
| Description starts with verb | Info | Heuristic: third-person descriptions typically start with a verb |

### Key context

- Validator uses a strict YAML subset parser (no PyYAML) at `scripts/_validate_skills.py`
- Single-pass, no subprocesses, no network — must stay environment-independent
- Same commands run locally and in CI
- Current stable output keys: `CURRENT_DESC_CHARS`, `PROJECTED_DESC_CHARS`, `BUDGET_STATUS` — do not change these
- Add new output keys for new checks (e.g., `NAME_DIR_MISMATCHES=0`)
- Follow existing code patterns in `_validate_skills.py` for warning/error reporting
## Acceptance
- [ ] Name-directory mismatch detection added (warning level)
- [ ] Extra frontmatter field detection added (warning level)
- [ ] Filler phrase detection added (warning level)
- [ ] All new checks produce warnings, not errors
- [ ] Existing output keys unchanged (`CURRENT_DESC_CHARS`, `PROJECTED_DESC_CHARS`, `BUDGET_STATUS`)
- [ ] New output keys added for new checks
- [ ] `./scripts/validate-skills.sh` passes on current codebase
- [ ] No external dependencies added (no PyYAML, no network, no subprocesses)
- [ ] Validator remains single-pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
