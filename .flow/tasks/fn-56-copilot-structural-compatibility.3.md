# fn-56-copilot-structural-compatibility.3 Update validators and baselines for flat layout

## Description

Update layout-dependent validation scripts (similarity detector, marketplace validator) and regenerate all baselines for the flat directory structure. This task does NOT add frontmatter checks (owned by T2).

**Size:** M
**Files:** scripts/validate-similarity.py, scripts/similarity-baseline.json, scripts/routing-warnings-baseline.json, scripts/validate-marketplace.sh, scripts/_validate_skills.py (layout guard only)

## Approach

1. **Fix `validate-similarity.py` glob** (CRITICAL): `collect_skill_descriptions()` uses `skills_dir.glob("*/*/SKILL.md")` which finds ZERO skills after flatten. Change to `skills_dir.glob("*/SKILL.md")`. Also fix `category = skill_md.parent.parent.name` which would become `"skills"` for every skill — remove the `category` and `same_category` fields from the report entirely since categories no longer exist in the flat layout. This avoids misleading noise in baselines.

2. **Remove same-category boost**: The `+0.15` boost for skills in the same parent directory is meaningless after flatten (all skills share parent `skills/`). Remove it entirely — simpler and avoids false positive grouping.

3. **Add flat layout guard to `_validate_skills.py`**: ERROR if any SKILL.md is found more than 1 level deep under `skills/` (catches accidental re-nesting). This is the ONLY change to `_validate_skills.py` in this task.

4. **Verify `validate-marketplace.sh`** works with flat `./skills/<skill-name>` paths. It iterates `plugin.json` `skills[]` array and checks each resolves to a directory with SKILL.md — should work unchanged after T1's plugin.json update, but run and verify.

5. **Regenerate `similarity-baseline.json`** by running the updated similarity validator.

6. **Regenerate `routing-warnings-baseline.json`** by running `./scripts/validate-skills.sh` after T1 and T2 changes are in place.

## Key context

- **Sequential dependency**: This task and T2 both edit `_validate_skills.py`. They must NOT run in parallel — T2 lands first (frontmatter checks), then T3 adds layout guard. Rebase T3 onto T2 before starting.
- `validate-similarity.py` is the highest-risk file: both `glob("*/*/SKILL.md")` and `category = skill_md.parent.parent.name` are layout-coupled
- Frontmatter safety checks (BOM, quoted desc, license, metadata) are owned by T2 — do NOT duplicate them here
- The `routing-warnings-baseline.json` may change due to layout-induced warning count deltas; Copilot frontmatter checks are ERRORs and do not affect warning baselines

## Acceptance
- [ ] `validate-similarity.py` glob changed from `*/*/SKILL.md` to `*/SKILL.md`
- [ ] Same-category boost removed from `validate-similarity.py`
- [ ] `category` and `same_category` fields removed from similarity report (no longer meaningful after flatten)
- [ ] `validate-similarity.py` finds all 131 skills on flat layout
- [ ] Flat layout guard added to `_validate_skills.py`: ERROR if SKILL.md found >1 level deep under skills/
- [ ] `validate-marketplace.sh` passes on flat layout
- [ ] `similarity-baseline.json` regenerated for flat layout
- [ ] `routing-warnings-baseline.json` regenerated for flat layout + T2 frontmatter checks
- [ ] Full validation suite: `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` green

## Done summary

## Evidence
