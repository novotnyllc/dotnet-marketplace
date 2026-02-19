# fn-53-skill-routing-language-hardening.5 Normalize Foundation and High-Traffic Skills

## Description
Apply canonical routing language (from T2 style guide) to the foundation skills and all high-traffic skills listed in `tests/agent-routing/cases.json`. Normalize `AGENTS.md` cross-references. These are the most-routed skills and set the pattern for subsequent sweeps.

**Size:** M (heavy — ~16 skills plus AGENTS.md, but templated per-skill work)
**Files:**
- `skills/foundation/dotnet-advisor/SKILL.md` (edit)
- `skills/foundation/dotnet-version-detection/SKILL.md` (edit)
- `AGENTS.md` (edit -- normalize existing cross-references to `[skill:]` syntax)
- ~14 additional skills referenced in `tests/agent-routing/cases.json` (edit)
- Read-only: `docs/skill-routing-ownership-manifest.md` (task list), `docs/skill-routing-style-guide.md` (rules)

## Approach

- Read ownership manifest to confirm which skills belong to this task (T5 batch only)
- Apply style guide rules: scope/out-of-scope sections, cross-ref format, description normalization
- For `dotnet-advisor`: add routing markers (currently zero markers), update specialist routing section to use `[skill:]` syntax instead of bold text
- For `AGENTS.md`: normalize any bare-text skill/agent names in existing content to `[skill:]` syntax. Note: `AGENTS.md` contains plugin instructions and conventions (File Structure, Validation Commands, etc.) — it does NOT have a routing index or delegation patterns table. The delegation flow content lives in `README.md` which is out of scope for this epic.
- **Run similarity check** before AND after edits: `python3 scripts/validate-similarity.py --repo-root .` — use the T13 similarity report to identify high-overlap pairs in this batch and prioritize description differentiation. Confirm no new WARN pairs introduced.
- Run `./scripts/validate-skills.sh` after each batch of changes
- Track budget delta: record before/after description char counts

## Budget reduction target

T5 owns the primary budget reduction. Current total: 12,345 chars. Target: net reduction of ≥350 chars from this batch. Foundation skills like `dotnet-advisor` (currently the most verbose description) are the primary reduction source. Subsequent sweep tasks (T6-T9) must stay budget-neutral or budget-negative but are not expected to achieve significant reductions. Cumulative budget across T5-T9 completions must reach `CURRENT_DESC_CHARS < 12,000`.

## Catalog status markers

Do not change catalog status markers (`implemented`/`planned`) in `dotnet-advisor/SKILL.md` during normalization. T11 will audit their accuracy as part of content-preservation verification.

## Key context

- `dotnet-advisor` is the central router. Its SKILL.md has specialist references using `**name**` bold format (lines 334-338). Convert to `[skill:]`.
- `AGENTS.md` is a concise plugin instructions file (121 lines). Cross-Reference Syntax section (lines 54-62) already documents `[skill:]` convention. Scan for any bare-text violations in the rest of the file.
- The 14 cases.json skills are the highest-traffic paths. Getting these right first ensures routing test reliability.
- Memory pitfall: "Cross-reference IDs must be canonical" -- verify each ref against actual `SKILL.md` name: fields.
- T13's similarity report highlights the top overlap pairs. Use this data to prioritize which descriptions to differentiate most aggressively.

## Acceptance
- [ ] Foundation skills (`dotnet-advisor`, `dotnet-version-detection`) have scope/out-of-scope sections and canonical descriptions
- [ ] `dotnet-advisor` specialist routing uses `[skill:]` syntax (no bold-text agent names)
- [ ] `AGENTS.md` cross-references normalized to `[skill:]` syntax where applicable
- [ ] All ~14 high-traffic skills from `cases.json` normalized per style guide
- [ ] All cross-references use canonical `[skill:]` syntax (unified for skills and agents)
- [ ] Budget delta documented: net reduction of ≥350 chars from this batch. Total chars before vs after recorded. Target: `CURRENT_DESC_CHARS < 12,000`.
- [ ] **Similarity check**: Run similarity before and after this batch (same branch, same suppressions). `pairs_above_warn` does not increase and `unsuppressed_errors == 0`.
- [ ] `./scripts/validate-skills.sh` passes
- [ ] Existing routing test cases still pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
