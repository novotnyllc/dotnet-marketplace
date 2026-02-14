# fn-24: Cross-Agent Build Pipeline

## Problem/Goal
Create a Python-based generator and conformance validator that produces Claude Code plugin, GitHub Copilot instructions, and OpenAI Codex AGENTS.md from canonical SKILL.md source. Wire into CI for gating and GitHub Releases for distribution.

## Tooling Decision
**Python scripts extending the existing validation stack** — not a dotnet tool. Rationale:
- The repo has zero .NET source code; the entire validation stack is Python (`_validate_skills.py`) and bash
- Conformance checks are text-processing tasks where Python excels
- Avoids adding `setup-dotnet` to CI (~30-60s overhead) for a non-.NET repo
- Shares existing frontmatter parser and cross-reference resolver from `_validate_skills.py`
- Future: if the plugin ships .NET projects, a dotnet tool wrapper can delegate to these scripts

## dist/ Output Schema

```
dist/
  claude/                          # Claude Code plugin structure
    plugin.json                    # Copy from .claude-plugin/plugin.json
    marketplace.json               # Copy from .claude-plugin/marketplace.json
    skills/                        # Copy of skills/ directory
    agents/                        # Copy of agents/ directory
    hooks/                         # Copy of hooks/ directory (hooks.json + scripts)
    .mcp.json                      # Copy of .mcp.json
  copilot/
    .github/
      copilot-instructions.md      # Concatenated routing index + skill summaries
    skills/
      <skill-name>.md              # SKILL.md transformed with Copilot conventions
  codex/
    AGENTS.md                      # Top-level routing index by category
    skills/
      <category>/
        AGENTS.md                  # Per-category skill guidance
```

`dist/` is gitignored. Generated fresh on every CI run and attached to GitHub Releases.

## Cross-Agent Transformation Rules

| Source construct | Claude output | Copilot output | Codex output |
|-----------------|--------------|----------------|--------------|
| `[skill:name]` cross-ref | Preserved as-is | Converted to relative `../name/SKILL.md` link | Converted to section anchor `#name` |
| Agent reference | Preserved | Omitted (sentence removed) | Omitted (sentence removed) |
| Hook reference (e.g., "SessionStart hook detects...") | Preserved | Rewritten: "Detect manually by running `dotnet --version`" or omitted if no manual equivalent | Omitted |
| MCP tool reference (e.g., "use Context7 to look up...") | Preserved | Rewritten: "look up docs at [url]" or omitted | Omitted |
| `${CLAUDE_PLUGIN_ROOT}` path | Preserved | Omitted | Omitted |
| SKILL.md frontmatter (`name`, `description`) | Preserved | `name` → heading, `description` → first paragraph | `name` → heading, `description` → first paragraph |

**Rule**: After applying known transformations, remaining body content sections must be textually identical (modulo whitespace). Any unexpected diff = conformance failure.

## Cross-Agent Conformance Tests

Generation success ≠ behavioral equivalence. The pipeline includes a conformance test suite:

### Required Tests
1. **Routing parity**: Every canonical SKILL.md `description` field appears (possibly reformatted) in all generated agent formats
2. **Trigger coverage**: Deterministic corpus of queries tested against all formats (see Trigger Corpus below)
3. **Graceful degradation**: Claude-only features (hooks, MCP, agents) are cleanly omitted from Copilot/Codex outputs — no broken references, no dangling cross-refs, no orphan sentences
4. **Structural comparison**: After applying the transformation rules above, remaining content sections are textually identical (modulo whitespace/formatting). This is a deterministic text comparison, not semantic.
5. **Cross-reference integrity**: All `[skill:name]` references in generated outputs resolve to valid targets within that agent's format (directory for Claude, file for Copilot, section for Codex)

### Trigger Corpus
- Format: JSON array in `tests/trigger-corpus.json`
  ```json
  [
    {
      "query": "How do I set up dependency injection in my .NET app?",
      "expected_skill": "microsoft-extensions-dependency-injection",
      "category": "core-csharp"
    }
  ]
  ```
- Minimum: one entry per skill category (currently 19 categories → 19+ entries)
- Completeness check: CI validates every skill category has at least one corpus entry
- Maintenance: corpus must be updated when skills are added/removed/renamed

### Implementation
- Tests run via `python3 scripts/validate_cross_agent.py` (new script)
- CI gate: conformance failures block merge
- Report format: per-skill pass/fail with diff output for failures

## Failure Modes
- Generation failure for any format → CI fails, no partial output
- Conformance check failure → CI fails, merge blocked
- Partial `dist/` output is never published
- Release workflow only runs after all validation passes

## Versioning
Version source: git tags parsed by the generator script. `plugin.json` and `marketplace.json` version fields are stamped during generation. NBGV is not used (no .NET projects to integrate with); a simple `git describe --tags` approach suffices for v0.x.

## Acceptance Checks
- [ ] Python generator script produces `dist/claude/`, `dist/copilot/`, `dist/codex/` from canonical sources
- [ ] Conformance validator implements all 5 checks with deterministic pass/fail
- [ ] Trigger corpus covers all skill categories with completeness CI check
- [ ] `dist/` is gitignored
- [ ] GitHub Actions validate.yml runs generator + conformance checks on push
- [ ] Release workflow creates GitHub Release with dist/ artifacts on tag push
- [ ] Transformation rules documented and tested (hook/MCP/agent omission)
- [ ] Cross-references resolve correctly in each output format

## Dependencies
- fn-19 (CI/CD Skills) — pipeline patterns and workflow templates (done)
- fn-23 (Hooks & MCP Integration) — hooks/MCP content exists for conformance testing (done)

Both dependencies are satisfied. fn-24 is unblocked.

## Key Context
- Canonical source is `skills/` directory using SKILL.md format
- Cross-agent compatibility via build-time generation (not manual duplication)
- Inner loop validation prevents broken commits
- Existing validation stack: `_validate_skills.py`, `validate-skills.sh`, `validate-marketplace.sh`
