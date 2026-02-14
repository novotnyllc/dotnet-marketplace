# fn-24.2 Create cross-agent conformance validator with trigger corpus

## Description
Create `scripts/validate_cross_agent.py` — a Python script that validates behavioral equivalence across the three generated `dist/` outputs. Implements the 5 conformance checks from the epic spec:

1. **Routing parity**: Every canonical SKILL.md `description` appears (possibly reformatted) in all generated formats
2. **Trigger coverage**: Run deterministic corpus (`tests/trigger-corpus.json`) against all formats; verify expected skill matches
3. **Graceful degradation**: Claude-only features (hooks, MCP, agents) are absent from Copilot/Codex outputs — no broken references, dangling cross-refs, or orphan sentences referencing removed features
4. **Structural comparison**: After applying known transformations, remaining content sections are textually identical (modulo whitespace). Deterministic text comparison, not semantic.
5. **Cross-reference integrity**: `[skill:name]` references are handled per format — preserved as-is in Claude output, resolved to relative file links (`../name/SKILL.md`) in Copilot, resolved to section anchors (`#name`) in Codex
<!-- Updated by plan-sync: fn-24.1 preserves [skill:name] unchanged in Claude output (no directory resolution), converts to ../name/SKILL.md for Copilot, and #name anchors for Codex -->

Also create `tests/trigger-corpus.json` with the initial trigger corpus:
- Minimum one entry per skill category (19+ entries)
- Format: `[{"query": "...", "expected_skill": "...", "category": "..."}]`
- CI completeness check: every skill category must have at least 1 corpus entry

The script integrates with the existing `_validate_skills.py` frontmatter parser for SKILL.md parsing.

## Files touched
- `scripts/validate_cross_agent.py` (new)
- `tests/trigger-corpus.json` (new)

## Acceptance
- [ ] `python3 scripts/validate_cross_agent.py` runs all 5 conformance checks against `dist/`
- [ ] Routing parity: detects missing skill descriptions in any format
- [ ] Trigger coverage: validates corpus entries match expected skills
- [ ] Graceful degradation: detects hook/MCP/agent references in non-Claude outputs
- [ ] Structural comparison: flags unexpected content differences after transformation
- [ ] Cross-reference integrity: validates `[skill:name]` preserved in Claude, relative file link in Copilot, section anchor in Codex
- [ ] Trigger corpus has 19+ entries covering all skill categories
- [ ] Completeness check: CI fails if any category lacks a corpus entry
- [ ] Per-skill pass/fail report with diff output for failures
- [ ] No .NET SDK dependency (pure Python)

## Done summary
Created cross-agent conformance validator (scripts/validate_cross_agent.py) implementing 5 conformance checks plus corpus completeness, and trigger corpus (tests/trigger-corpus.json) with 21 entries covering all 19 skill categories. Validator detects routing parity gaps, trigger coverage mismatches, Claude-only feature leaks, structural mismatches after transformation, and cross-reference integrity issues across Claude/Copilot/Codex dist/ outputs.

## Evidence
commits: 2cfb55d38a549c6248b82193bf2cc336277f80f1
tests: python3 scripts/validate_cross_agent.py --repo-root /Users/claire/dev/dotnet-marketplace
