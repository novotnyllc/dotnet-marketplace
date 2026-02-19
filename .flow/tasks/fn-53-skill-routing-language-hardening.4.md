# fn-53-skill-routing-language-hardening.4 Routing Test Assertion Hardening

## Description
Tighten routing test evidence patterns in `check-skills.cs` to require skill-specific proof rather than generic matches. Update `cases.json` evidence patterns, `BuildRequiredAllEvidence()`, AND `ClassifyFailure()` to enforce the new invariant. Update `docs/agent-routing-tests.md` with refined evidence hierarchy.

**Size:** M
**Files:**
- `tests/agent-routing/check-skills.cs` (edit)
- `tests/agent-routing/cases.json` (edit)
- `docs/agent-routing-tests.md` (edit)

## Approach

- **Existing hardening already in place:** The runner already extracts `"Launching skill:"` and `{"skill":"..."}` evidence tokens (`check-skills.cs:75-77, 854-891`) and avoids requiring SKILL.md reads for Claude (`check-skills.cs:800-819`). Do not duplicate this.
- **Three code changes required:**
  1. **`cases.json` patterns**: Update non-Claude evidence patterns to use skill-specific file paths (`"<expectedSkill>/SKILL.md"`) instead of generic `"SKILL.md"`.
  2. **`BuildRequiredAllEvidence()` code**: Update to stop adding generic `"SKILL.md"` when `ExpectedSkill` is present for non-Claude agents. New invariant: when `ExpectedSkill` is set, require **only** the skill-specific path (`"<expectedSkill>/SKILL.md"`), not generic `"SKILL.md"`. This prevents false-positive matches from incidental SKILL.md mentions.
  3. **`ClassifyFailure()` code**: Currently detects `MissingSkillFileEvidence` via `MissingAll.Contains("SKILL.md")`. After change #2, the generic string won't be in the required set. Update to: detect missing skill-file evidence as any missing token that `EndsWith("/SKILL.md")`. This preserves the failure taxonomy guarantee for downstream CI/reporting. Claude agents remain excluded from skill-file evidence as designed.
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
- `BuildRequiredAllEvidence()` currently injects both generic `"SKILL.md"` and skill-specific paths — T4 changes to skill-specific only
- `ClassifyFailure()` must be updated to match the new evidence pattern, otherwise missing skill-file evidence will be misclassified as `unknown`

## Acceptance
- [ ] Non-Claude evidence patterns in `cases.json` use skill-specific file paths (not generic `"SKILL.md"`)
- [ ] `BuildRequiredAllEvidence()` updated: when `ExpectedSkill` is present, only require skill-specific path, not generic `"SKILL.md"`
- [ ] `ClassifyFailure()` updated: detect missing skill-file evidence via `EndsWith("/SKILL.md")` instead of `Contains("SKILL.md")`
- [ ] Claude evidence patterns remain unchanged (already use definitive proof)
- [ ] `check-skills.cs` assertion logic handles skill-specific file-evidence tokens correctly
- [ ] `docs/agent-routing-tests.md` updated with evidence hierarchy (Claude vs non-Claude)
- [ ] All 14 existing test cases pass with hardened assertions (verified with `--agents claude` for local validation)
## Done summary
Hardened routing test evidence assertions: replaced generic "SKILL.md" tokens with skill-specific file paths in all 14 cases.json entries, updated BuildRequiredAllEvidence() to require only skill-specific paths when ExpectedSkill is set, updated ClassifyFailure() to detect missing skill-file evidence via EndsWith("/SKILL.md"), and documented the Claude vs non-Claude evidence hierarchy with failure taxonomy in docs/agent-routing-tests.md.
## Evidence
- Commits: f032e1e349344b94859436f55d0b5f266ce7a06a
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: