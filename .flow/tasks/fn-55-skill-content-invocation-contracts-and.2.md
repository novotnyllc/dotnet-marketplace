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
  3. OOS contains ≥1 `[skill:<id>]` string
- **Stable grep marker:** Contract warnings use `INVOCATION_CONTRACT:` prefix in warning line for path-scoped filtering:
  `skills/<cat>/<name>/SKILL.md: INVOCATION_CONTRACT: Scope section has 0 unordered bullets (requires ≥1)`
- STRICT_INVOCATION mechanism: `_validate_skills.py` reads env var. Truthy → contract warnings become errors.
- Default WARN (exit 0); STRICT_INVOCATION=1 → ERROR (exit 1)
- `INVOCATION_CONTRACT_WARN_COUNT=<N>` in validate-skills.sh output

## Key context

- Legacy `has_section_header()` and `extract_oos_items()` are currently fence-naive — making them fence-aware is a correctness fix that prevents false counts from fenced examples
- Stable `INVOCATION_CONTRACT:` prefix enables T3 to verify per-file compliance via grep

## Acceptance
- [ ] `has_section_header()`, `extract_oos_items()`, and `extract_scope_items()` ALL fence-aware
- [ ] `extract_scope_items()`: section-bounded, fence-aware, `- ` only
- [ ] Contract warnings use `INVOCATION_CONTRACT:` stable prefix — verifiable: grep output
- [ ] Scope: `- ` only; numbered/fenced lines excluded
- [ ] OOS: `- ` only, fence-aware; `[skill:]` presence fence-aware
- [ ] Default WARN (exit 0); STRICT_INVOCATION=1 → ERROR (exit 1) — toggle verified by exit code
- [ ] `INVOCATION_CONTRACT_WARN_COUNT` in output
- [ ] Existing checks still pass (fence-awareness is a correctness improvement, not behavior change for well-formed skills)
