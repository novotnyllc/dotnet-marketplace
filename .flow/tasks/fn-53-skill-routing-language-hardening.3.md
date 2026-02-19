# fn-53-skill-routing-language-hardening.3 Validator and Compliance Report Hardening

## Description
Extend `_validate_skills.py` with new routing-language quality checks for SKILL.md files AND agent files (via separate code paths). Create a standalone compliance report script. Define CI policy: zero errors, zero new warnings vs committed baseline file. **Own the integration of T13's similarity script into `validate-skills.sh` and CI workflow.**

**Size:** M
**Files:**
- `scripts/_validate_skills.py` (edit)
- `scripts/validate-skills.sh` (edit — T3 is the sole owner of this file. Update header docs for new output keys, add invocation of T13's `validate-similarity.py`, report similarity output keys)
- `scripts/skill-routing-report.py` (new — compliance report)
- `scripts/routing-warnings-baseline.json` (new — committed baseline)
- `.github/workflows/validate.yml` (edit — set `STRICT_REFS=1`, add new output key parsing, add similarity check step invoking T13's script)

## Approach

- New validator checks for SKILL.md files:
  - Scope section presence (`## Scope` header required)
  - Out-of-scope section presence (`## Out of scope` header required)
  - Out-of-scope attribution format (each out-of-scope item should reference owning skill via `[skill:]`)
  - Self-referential cross-link detection (skill referencing itself) — **error**
  - Cross-reference cycle detection (post-processing phase) — **informational report only, NOT an error** (see implementation note below)
- New validator checks for agent files (dedicated code path — NOT reusing the SKILL YAML parser):
  - **Dedicated `parse_agent_frontmatter()` function** that extracts `name:` and `description:` scalar fields from agent frontmatter, handling plain values, quoted strings, and block scalars. Does NOT attempt sequences.
  - Extract `[skill:]` refs from all `agents/*.md` and validate against the union of `valid_skill_dirs` + agent file stems
  - Detect bare-text skill/agent references using an **allowlist of known IDs**. Only flag tokens matching known IDs. This avoids false positives on .NET CLI tools.
  - New stable output key: `AGENT_BARE_REF_COUNT`
- New validator check for `AGENTS.md`:
  - Detect bare `dotnet-[a-z-]+` names matching known skill/agent IDs not wrapped in `[skill:]` syntax
  - New stable output key: `AGENTSMD_BARE_REF_COUNT`
- Cross-reference validation resolves `[skill:]` refs against the **union** of skill directory names + agent file stems
- **Budget status fix**: Update `_validate_skills.py` to compute `BUDGET_STATUS` from `CURRENT_DESC_CHARS` only. `PROJECTED_DESC_CHARS` is still printed but does NOT influence `BUDGET_STATUS`. This aligns with the epic spec's rule: `CURRENT_DESC_CHARS < 12,000`.
- **Docstring update**: Re-number and extend the module docstring (lines 3-17) to list all new checks consistently. Fix existing "6." duplication.
- New stable CI-parseable output keys: `MISSING_SCOPE_COUNT`, `MISSING_OOS_COUNT`, `SELF_REF_COUNT`, `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`
- Compliance report script: reads all SKILL.md files, outputs JSON with per-skill compliance metrics
- Baseline file: JSON with current warning counts, committed to repo. CI compares against baseline.
- CI strict mode: set `STRICT_REFS=1` in `validate.yml`
- **Similarity integration** (T3 owns this): Update `validate-skills.sh` to invoke `scripts/validate-similarity.py` (built by T13) and report its output keys. Update `.github/workflows/validate.yml` to parse similarity keys and fail if similarity check fails. T13 must complete before T3 can test this integration, but T3 can implement the wiring with the documented interface.

## Cycle detection implementation

After all files are processed, build a directed cross-reference graph. Run cycle detection (DFS). Report cycles as informational output (not errors). Only self-references are errors.

## Agent file validation — separate code path

Use `parse_agent_frontmatter()` that handles plain scalars, quoted strings, and block scalars for `name:` and `description:` only. Factor into a shared helper module (`scripts/_agent_frontmatter.py`) imported by both `_validate_skills.py` and T13's `validate-similarity.py`.

## Key context

- Current validator checks 8 things. New checks extend this list.
- Follow existing patterns: `FILLER_PHRASES` list, new checks should follow same structure.
- Agent files are currently NOT processed by `_validate_skills.py`. This task adds that capability.
- Memory pitfall: "Hand-authored YAML configuration files require CI validation rules"
- T13 builds `scripts/validate-similarity.py`. T3 wires it into `validate-skills.sh` and `validate.yml`.

## Agent validation gating strategy

Agent bare-ref counts (`AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`) are **reported as informational output** by T3's validator, NOT as validation errors. This prevents a deadlock: T3 (wave 3) adds agent scanning before T10 (wave 5) normalizes agent files. The CI gate for agent bare-ref counts becomes mandatory only after T10 completes — T12 tightens the gate as part of final CI enforcement.

## Acceptance
- [ ] `_validate_skills.py` has new checks: scope presence, out-of-scope presence, out-of-scope attribution, self-referential refs (error), cycle detection (informational report, NOT error)
- [ ] `_validate_skills.py` module docstring updated and consistently numbered for all checks (old + new)
- [ ] `_validate_skills.py` computes `BUDGET_STATUS` from `CURRENT_DESC_CHARS` only (projected is informational, not part of status)
- [ ] `_validate_skills.py` has agent file scanning via dedicated `parse_agent_frontmatter()` (handles plain, quoted, block scalars; NOT subset YAML parser)
- [ ] Agent bare-ref detection uses allowlist of known skill/agent IDs
- [ ] Cross-reference validation resolves against union of skill IDs + agent IDs
- [ ] `_validate_skills.py` has AGENTS.md scanning: detects bare known IDs not in `[skill:]` syntax
- [ ] New stable output keys documented in `validate-skills.sh` header (including `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`)
- [ ] `scripts/skill-routing-report.py` generates per-skill compliance JSON (includes cycle report)
- [ ] `scripts/routing-warnings-baseline.json` committed with current counts
- [ ] `STRICT_REFS=1` set in `.github/workflows/validate.yml`
- [ ] `validate-skills.sh` invokes T13's `scripts/validate-similarity.py` and reports similarity output keys (`MAX_SIMILARITY_SCORE`, `PAIRS_ABOVE_WARN`, `PAIRS_ABOVE_ERROR`)
- [ ] `.github/workflows/validate.yml` parses all new output keys (validator + similarity) and fails on similarity check failure
- [ ] `./scripts/validate-skills.sh` passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
