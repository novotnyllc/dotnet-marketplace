# fn-53-skill-routing-language-hardening.4 Routing Test Assertion Hardening

## Description
Improve routing test assertions in `check-skills.cs` to prefer definitive evidence (Skill tool invocation, `Launching skill:` lines) over incidental text mentions. Update `cases.json` evidence patterns. Update `docs/agent-routing-tests.md` with new evidence hierarchy.

**Size:** M
**Files:**
- `tests/agent-routing/check-skills.cs` (edit)
- `tests/agent-routing/cases.json` (edit)
- `docs/agent-routing-tests.md` (edit)

## Approach

- Replace string-presence evidence patterns with skill-invocation-specific patterns
- Follow pattern at `check-skills.cs` for `required_all_evidence` / `required_any_evidence` fields
- Update `docs/agent-routing-tests.md` "Evidence currently gates on" section with new evidence hierarchy
- Test against existing 14 cases to ensure no false negatives from stricter evidence

## Key context

- Current evidence uses patterns like `"dotnet-xunit"` and `"SKILL.md"` which match incidental mentions, not just skill invocations
- Target: `"Launching skill: dotnet-xunit"` or `"skill":"dotnet-xunit"` as definitive proof
- Only 14 test cases exist covering ~10% of 130 skills. This task hardens assertions, not coverage.
## Acceptance
- [ ] Evidence patterns in `cases.json` use definitive skill-invocation proof (not incidental text mentions)
- [ ] `check-skills.cs` assertion logic prefers tool-invocation evidence
- [ ] `docs/agent-routing-tests.md` updated with evidence hierarchy
- [ ] All 14 existing test cases still pass with hardened assertions
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
