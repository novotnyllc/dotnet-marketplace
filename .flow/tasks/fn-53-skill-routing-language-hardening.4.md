# fn-53-skill-routing-language-hardening.4 Routing Test Assertion Hardening

## Description
Tighten routing test evidence patterns in `check-skills.cs` to require skill-specific proof rather than generic matches. Update `cases.json` evidence patterns. Update `docs/agent-routing-tests.md` with refined evidence hierarchy.

**Size:** M
**Files:**
- `tests/agent-routing/check-skills.cs` (edit)
- `tests/agent-routing/cases.json` (edit)
- `docs/agent-routing-tests.md` (edit)

## Approach

- **Existing hardening already in place:** The runner already extracts `"Launching skill:"` and `{"skill":"..."}` evidence tokens (`check-skills.cs:75-77, 854-891`) and avoids requiring SKILL.md reads for Claude (`check-skills.cs:800-819`). Do not duplicate this.
- **What's actually missing:** Non-Claude agents (Codex, Copilot) use file-evidence tokens. Current patterns accept generic `"SKILL.md"` matches that could be incidental. Tighten to require `"<expectedSkill>/SKILL.md"` (skill-specific file path).
- Update `cases.json` evidence patterns to use skill-specific file paths for non-Claude evidence
- Keep Claude evidence patterns unchanged (already use definitive `Launching skill:` / `{"skill":"..."}` tokens)
- Update `docs/agent-routing-tests.md` "Evidence currently gates on" section with refined evidence hierarchy distinguishing Claude vs non-Claude evidence
- Test against existing 14 cases to ensure no false negatives from stricter evidence

## Verification strategy

T4's primary job is hardening the assertion logic and evidence patterns. For local validation during development, use `--agents claude` (single agent) to verify the 14 cases pass with hardened assertions. Full multi-agent verification (claude + codex + copilot, 42 invocations) is deferred to T11's integration check. This avoids the 63-minute serial test run during T4 development.

## Key context

- Current evidence patterns like `"dotnet-xunit"` and `"SKILL.md"` match incidental mentions, not just skill invocations
- Claude target evidence: `"Launching skill: dotnet-xunit"` or `"skill":"dotnet-xunit"` — already implemented
- Non-Claude target evidence: `"dotnet-xunit/SKILL.md"` (skill-specific file path) — needs tightening
- Only 14 test cases exist covering ~10% of 130 skills. This task hardens assertions, not coverage.

## Acceptance
- [ ] Non-Claude evidence patterns in `cases.json` use skill-specific file paths (not generic `"SKILL.md"`)
- [ ] Claude evidence patterns remain unchanged (already use definitive proof)
- [ ] `check-skills.cs` assertion logic handles skill-specific file-evidence tokens correctly
- [ ] `docs/agent-routing-tests.md` updated with evidence hierarchy (Claude vs non-Claude)
- [ ] All 14 existing test cases pass with hardened assertions (verified with `--agents claude` for local validation)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
