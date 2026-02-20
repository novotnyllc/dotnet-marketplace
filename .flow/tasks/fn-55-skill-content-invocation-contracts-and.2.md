# fn-55-skill-content-invocation-contracts-and.2 Add invocation-contract compliance checks to validator

## Description
Add structural invocation-contract checks with fence-aware section extraction (applied to all section checks for consistency), stable grep-friendly markers, and STRICT_INVOCATION toggle.

**Size:** M
**Files:** `scripts/_validate_skills.py`, `scripts/validate-skills.sh`

## Approach

- **Fence-awareness for ALL section checks:** Make `has_section_header()`, `extract_oos_items()`, and new `extract_scope_items()` all fence-aware. Same `in_fence` toggle (lines starting with ```) applied consistently. This ensures all scope/OOS-related checks agree on what "real markdown structure" means — no contradictory output.
- Add `extract_scope_items(content)`: section-bounded (enter `^## Scope$`, exit next `^## `), fence-aware, `- ` only
- Contract checks (all fence-aware):
  1. Scope ≥1 `- ` bullet
  2. OOS ≥1 `- ` bullet
  3. OOS contains ≥1 `[skill:<id>]` string — this is a NEW dedicated check, separate from STRICT_REFS. STRICT_REFS checks resolution (does the referenced skill exist); this check verifies presence of `[skill:` string inside OOS bullets regardless of resolution.
- **Stable output format:** Contract warnings use `INVOCATION_CONTRACT:` prefix in the warning message. Exact format matches existing validator convention:
  ```
  WARN:  skills/<cat>/<name>/SKILL.md -- INVOCATION_CONTRACT: Scope section has 0 unordered bullets (requires ≥1)
  WARN:  skills/<cat>/<name>/SKILL.md -- INVOCATION_CONTRACT: Out of scope section has 0 unordered bullets (requires ≥1)
  WARN:  skills/<cat>/<name>/SKILL.md -- INVOCATION_CONTRACT: No OOS bullet contains [skill:] reference
  ```
  This enables T3's grep-based acceptance to filter by skill path and marker prefix.
- **Summary key:** `_validate_skills.py` emits `INVOCATION_CONTRACT_WARN_COUNT=<N>` to stdout. `validate-skills.sh` propagates this to output.
- **STRICT_INVOCATION mechanism:** `_validate_skills.py` reads `STRICT_INVOCATION` env var directly. When `1`, contract warnings become errors (exit 1). Default WARN (exit 0).
- **validate-skills.sh header comments:** Add documentation of STRICT_INVOCATION and STRICT_REFS toggles with explicit independence statement.
- **Warning duplication note:** A skill missing `## Scope` entirely will produce both the existing `missing '## Scope' section` warning AND the new `INVOCATION_CONTRACT: Scope section has 0 unordered bullets` warning. This is expected and correct — the warnings serve distinct purposes (structural presence vs contract compliance). No deduplication needed during rollout.

## Key context

- Legacy `has_section_header()` and `extract_oos_items()` are currently fence-naive — making them fence-aware is a correctness fix that prevents false counts from fenced examples
- Stable `INVOCATION_CONTRACT:` prefix enables T3 to verify per-file compliance via grep
- Rule #3 presence check is independent of STRICT_REFS resolution check — both can be enabled/disabled separately

## Acceptance
- [ ] `has_section_header()`, `extract_oos_items()`, and `extract_scope_items()` ALL fence-aware
- [ ] `extract_scope_items()`: section-bounded, fence-aware, `- ` only
- [ ] Rule #3 implemented as dedicated check: OOS bullet `[skill:]` presence, independent of STRICT_REFS
- [ ] Contract warnings use exact format: `WARN:  <path> -- INVOCATION_CONTRACT: <description>`
- [ ] Scope: `- ` only; numbered/fenced lines excluded
- [ ] OOS: `- ` only, fence-aware; `[skill:]` presence fence-aware
- [ ] Default WARN (exit 0); STRICT_INVOCATION=1 → ERROR (exit 1) — toggle verified by exit code
- [ ] `INVOCATION_CONTRACT_WARN_COUNT` emitted by `_validate_skills.py` (Python)
- [ ] validate-skills.sh header comments document STRICT_INVOCATION and STRICT_REFS as independent toggles
- [ ] Existing checks still pass (fence-awareness is a correctness improvement, not behavior change for well-formed skills)
