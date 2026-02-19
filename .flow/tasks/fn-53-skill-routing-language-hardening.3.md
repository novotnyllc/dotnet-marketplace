# fn-53-skill-routing-language-hardening.3 Validator and Compliance Report Hardening

## Description
Extend `_validate_skills.py` with new routing-language quality checks for SKILL.md files AND agent files (via separate code paths). Create a standalone compliance report script. Define CI policy: zero errors, zero new warnings vs committed per-key baseline file. **Own the integration of T13's similarity script into `validate-skills.sh` and CI workflow.** Create the shared `_agent_frontmatter.py` module (sole owner).

**Size:** M
**Files:**
- `scripts/_validate_skills.py` (edit)
- `scripts/_agent_frontmatter.py` (new — **T3 creates and owns this file**. Shared agent frontmatter parser imported by both T3 and T13)
- `scripts/validate-skills.sh` (edit — T3 is the sole owner. Remove `exec`, add similarity wiring, update header docs)
- `scripts/skill-routing-report.py` (new — compliance report)
- `scripts/routing-warnings-baseline.json` (new — committed per-key baseline)
- `.github/workflows/validate.yml` (edit — set `STRICT_REFS=1`, add new output key parsing, add similarity check step)

## Approach

- New validator checks for SKILL.md files:
  - Scope section presence (`## Scope` header required)
  - Out-of-scope section presence (`## Out of scope` header required)
  - Out-of-scope attribution format (each out-of-scope item should reference owning skill via `[skill:]`)
  - Self-referential cross-link detection (skill referencing itself) — **error**
  - Cross-reference cycle detection (post-processing phase) — **informational report only, NOT an error** (see implementation note below)
- **Known IDs set**: Build once at startup: `{skill directory names} ∪ {agent file stems}`. Validate that the intersection is empty (emit error if any ID collision between skill and agent). Use this set for all cross-reference validation and bare-ref detection.
- New validator checks for agent files (dedicated code path — NOT reusing the SKILL YAML parser):
  - **`scripts/_agent_frontmatter.py` module (T3 creates)**: Parsing contract: parse only top-level `name:` and `description:` with zero indentation. Support plain scalars, single-quoted strings, double-quoted strings, and block scalars (`|`/`>`). Return `None` for unparseable fields. Ignore sequences, flow constructs, nested mappings entirely. T13 imports this module as-is.
  - Extract `[skill:]` refs from all `agents/*.md` and validate against the known IDs set
  - Detect bare-text skill/agent references using the known IDs allowlist. **Exclusion rule**: ignore any occurrence within `[skill:...]` spans and link URLs before scanning — a naive match on `dotnet-foo` would false-positive on every valid `[skill:dotnet-foo]`. Implementation: strip `[skill:...]` patterns from text before bare-ref matching.
  - New stable output key: `AGENT_BARE_REF_COUNT`
- New validator check for `AGENTS.md`:
  - Detect bare `dotnet-[a-z-]+` names matching known IDs not wrapped in `[skill:]` syntax. Same exclusion rule: strip `[skill:...]` spans before scanning. Uses same known IDs allowlist.
  - New stable output key: `AGENTSMD_BARE_REF_COUNT`
- Cross-reference validation resolves `[skill:]` refs against the known IDs set
- **Budget status fix**: Update `_validate_skills.py` to compute `BUDGET_STATUS` from `CURRENT_DESC_CHARS` only: `OK` if `< 12,000`, `WARN` if `>= 12,000`, `FAIL` if `>= 15,600`. `PROJECTED_DESC_CHARS` is still printed but does NOT influence `BUDGET_STATUS`.
- **Docstring update**: Re-number and extend the module docstring to list all new checks consistently. Fix existing "6." duplication.
- New stable CI-parseable output keys: `MISSING_SCOPE_COUNT`, `MISSING_OOS_COUNT`, `SELF_REF_COUNT`, `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`
- Compliance report script: reads all SKILL.md files, outputs JSON with per-skill compliance metrics
- **Per-key baseline**: `scripts/routing-warnings-baseline.json` contains individual stable key counters (e.g., `{"version": 1, "keys": {"MISSING_SCOPE_COUNT": 0, ...}}`), NOT the aggregate `Warnings: N` total. CI compares each key against its baseline value independently.
- CI strict mode: set `STRICT_REFS=1` in `validate.yml`
- **Wrapper `exec` removal**: Current `validate-skills.sh` uses `exec python3 _validate_skills.py ...` which replaces the shell process. T3 must replace `exec` with a regular invocation, capture the validator exit code in a variable, then run the guarded similarity check, and compose a final exit code (non-zero if either check fails).
- **Similarity integration (phase 1 — error-only)**: After removing `exec`, add guarded similarity invocation: `if [[ -f scripts/validate-similarity.py ]]; then python3 scripts/validate-similarity.py --repo-root "$REPO_ROOT" --suppressions scripts/similarity-suppressions.json 2>&1; fi`. The `2>&1` captures similarity stderr keys into stdout for the existing CI capture mechanism. No `--baseline` flag in phase 1 (error-only mode). Update `.github/workflows/validate.yml` to parse similarity keys and fail if similarity check exits non-zero.

## Cycle detection implementation

After all files are processed, build a directed cross-reference graph. Run cycle detection (DFS). Report cycles as informational output (not errors). Only self-references are errors.

## Key context

- Current validator checks 8 things. New checks extend this list.
- Follow existing patterns: `FILLER_PHRASES` list, new checks should follow same structure.
- Agent files are currently NOT processed by `_validate_skills.py`. This task adds that capability.
- Memory pitfall: "Hand-authored YAML configuration files require CI validation rules"
- T13 builds `scripts/validate-similarity.py`. T3 wires it into `validate-skills.sh` and `validate.yml`.
- T3 lands similarity wiring with file-existence guard. Full integration testing happens in T11.
- T3 creates `_agent_frontmatter.py`; T13 imports it. No file overlap between parallel tasks.

## Agent validation gating strategy

Agent bare-ref counts (`AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`) are **reported as informational output** by T3's validator, NOT as validation errors. This prevents a deadlock: T3 (wave 3) adds agent scanning before T10 (wave 5) normalizes agent files. The CI gate for agent bare-ref counts becomes mandatory only after T10 completes — T12 tightens the gate as part of final CI enforcement.

## Acceptance
- [ ] `_validate_skills.py` has new checks: scope presence, out-of-scope presence, out-of-scope attribution, self-referential refs (error), cycle detection (informational report, NOT error)
- [ ] `_validate_skills.py` module docstring updated and consistently numbered for all checks (old + new)
- [ ] `_validate_skills.py` computes `BUDGET_STATUS` from `CURRENT_DESC_CHARS` only (projected is informational, not part of status)
- [ ] `_validate_skills.py` builds known IDs set (skill dirs ∪ agent stems) and emits error if intersection is non-empty
- [ ] `scripts/_agent_frontmatter.py` created by T3 with documented parsing contract (plain, quoted, block scalars; returns None for unparseable)
- [ ] `_validate_skills.py` has agent file scanning importing `_agent_frontmatter.py`
- [ ] Agent and AGENTS.md bare-ref detection uses known IDs allowlist with `[skill:...]` span exclusion
- [ ] Cross-reference validation resolves against known IDs set (skill dirs + agent stems)
- [ ] New stable output keys documented in `validate-skills.sh` header (including `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`)
- [ ] `scripts/skill-routing-report.py` generates per-skill compliance JSON (includes cycle report)
- [ ] `scripts/routing-warnings-baseline.json` committed with per-key counts (not aggregate)
- [ ] `STRICT_REFS=1` set in `.github/workflows/validate.yml`
- [ ] `validate-skills.sh` `exec` removed; validator exit code captured; final exit code composes validator + similarity results
- [ ] `validate-skills.sh` invokes T13's script with file-existence guard, error-only mode (no --baseline), stderr captured to stdout via `2>&1`
- [ ] `.github/workflows/validate.yml` parses all new output keys (validator + similarity) and fails on similarity exit code non-zero
- [ ] `./scripts/validate-skills.sh` passes
## Done summary
Extended _validate_skills.py with 7 new routing-language quality checks (scope/out-of-scope presence, attribution, self-referential cross-links, cycle detection, agent bare-ref detection, AGENTS.md bare-ref detection), created shared _agent_frontmatter.py parser module, skill-routing-report.py compliance tool, per-key routing-warnings-baseline.json, updated validate-skills.sh to remove exec and wire similarity detection with file-existence guard, and set STRICT_REFS=1 in CI with all new output keys parsed.
## Evidence
- Commits: 0905970, b5b6b23
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, STRICT_REFS=1 ./scripts/validate-skills.sh, python3 scripts/skill-routing-report.py --repo-root .
- PRs: