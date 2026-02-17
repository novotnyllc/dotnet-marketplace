# fn-49-skill-guide-compliance-review.3 Enhance validation scripts for ongoing quality enforcement

## Description
Enhance `scripts/_validate_skills.py` to enforce the quality standards established in Tasks 1-2, preventing regression on front matter quality.

**Size:** M
**Files:** `scripts/_validate_skills.py`, `scripts/validate-skills.sh`

## Approach

1. Add name-directory consistency check: verify `name` field matches the skill's directory name
2. Add extra-frontmatter detection: warn on any fields beyond `name` and `description`
3. Add description quality heuristics: detect common filler phrases (especially "Covers", "helps with", "guide to"), missing technology keywords
3b. Add WHEN prefix regression check: warn if any description starts with "WHEN " (Task 2 removes all; this prevents reintroduction)
4. Keep all checks as warnings (not errors) to avoid breaking CI for edge cases
5. Update `validate-skills.sh` thresholds if needed
6. Ensure no existing validation behavior changes (backward compatible)

### New Checks to Add

| Check | Type | Implementation |
|-------|------|----------------|
| Name-directory match | Warning | Compare `name` value to last path segment of skill directory |
| Extra frontmatter fields | Warning | Flag any field not in `{name, description}` |
| Filler phrase detection | Warning | Check for common filler patterns: "Covers", "helps with", "guide to", "complete guide" (audit found "Covers" as the only instance; others are preventive) |
| WHEN prefix detection | Warning | Flag descriptions starting with "WHEN " — Task 2 removes all WHEN prefixes; this prevents regression |
| Description starts with verb or noun phrase | Info | Heuristic: after WHEN removal, descriptions start with varied patterns (verbs like "Writing...", noun phrases like "Async/await patterns.") — both are acceptable |

### Key context

- Validator uses a strict YAML subset parser (no PyYAML) at `scripts/_validate_skills.py`
- Single-pass, no subprocesses, no network — must stay environment-independent
- Same commands run locally and in CI
- Current stable output keys: `CURRENT_DESC_CHARS`, `PROJECTED_DESC_CHARS`, `BUDGET_STATUS` — do not change these
- Add new output keys for new checks (e.g., `NAME_DIR_MISMATCHES=0`, `WHEN_PREFIX_COUNT=0`)
- Follow existing code patterns in `_validate_skills.py` for warning/error reporting
## Acceptance
- [ ] Name-directory mismatch detection added (warning level)
- [ ] Extra frontmatter field detection added (warning level)
<!-- Updated by plan-sync: fn-49.1 found "Covers" as only filler instance; Task 2 removes all WHEN prefixes so Task 3 needs WHEN regression check; audit report at .flow/reports/fn-49.1-compliance-audit.md -->
- [ ] Filler phrase detection added (warning level, includes "Covers" pattern found by audit)
- [ ] All new checks produce warnings, not errors
- [ ] Existing output keys unchanged (`CURRENT_DESC_CHARS`, `PROJECTED_DESC_CHARS`, `BUDGET_STATUS`)
- [ ] WHEN prefix regression detection added (warning level)
- [ ] New output keys added for new checks (including `WHEN_PREFIX_COUNT`)
- [ ] `./scripts/validate-skills.sh` passes on current codebase
- [ ] No external dependencies added (no PyYAML, no network, no subprocesses)
- [ ] Validator remains single-pass
## Done summary
Added 4 quality enforcement checks to _validate_skills.py: name-directory consistency, extra frontmatter field detection, filler phrase detection ("Covers", "helps with", "guide to", "complete guide"), and WHEN prefix regression detection. All checks produce warnings (not errors) with new stable CI-parseable output keys (NAME_DIR_MISMATCHES, EXTRA_FIELD_COUNT, FILLER_PHRASE_COUNT, WHEN_PREFIX_COUNT). Existing output keys and behavior unchanged.
## Evidence
- Commits: 5bfbcb9a02bb94c1b647cb870b3333432130a47d
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: