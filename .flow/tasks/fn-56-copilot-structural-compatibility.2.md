# fn-56-copilot-structural-compatibility.2 Copilot-safe frontmatter migration

## Description

Migrate all 131 SKILL.md frontmatter files to be Copilot-safe. Address known Copilot CLI YAML parsing bugs that cause silent skill load failures. This task owns ALL frontmatter validation changes in `_validate_skills.py`.

**Size:** M
**Files:** skills/*/SKILL.md (131 files), scripts/_validate_skills.py (ALLOWED_FRONTMATTER_FIELDS, FIELD_TYPES, raw-frontmatter checks)

## Approach

1. **Verify metadata-last behavior** (FIRST, before implementing the check): Copilot bug #951 reports that `metadata:` as the last frontmatter field causes silent skill drop, but the exact semantics are ambiguous. Create two minimal test skills in a temp directory:
   - `test-meta-last/SKILL.md` — frontmatter with `metadata:` as the literal last YAML key
   - `test-meta-notlast/SKILL.md` — same frontmatter but with a dummy field after `metadata:`
   Minimal repro procedure (from `test.sh:prepare_copilot_plugin()`):
   - Create a temp directory with the minimum plugin structure Copilot requires:
     ```
     /tmp/test-meta-dir/
       .claude-plugin/
         plugin.json          # {"name":"test-meta","skills":["./skills/test-meta-last","./skills/test-meta-notlast"]}
         marketplace.json     # {"name":"test-meta","version":"0.0.1"}
       skills/
         test-meta-last/SKILL.md
         test-meta-notlast/SKILL.md
     ```
     Base these files on the repo's actual `.claude-plugin/plugin.json` and `marketplace.json` schema (copy and trim to 2 skills) so the only variable is metadata ordering.
   - `copilot plugin marketplace add /tmp/test-meta-dir`
   - `copilot plugin install test-meta@test-meta`
   - `copilot plugin marketplace list` — verify plugin appears
   - Test which skill(s) load and which silently drop
   - Record the exact commands and observed output as evidence
   Use the confirmed behavior to define the exact check logic in step 4. If Copilot CLI is unavailable, implement the check conservatively (ERROR if `metadata:` is last key) and document the assumption.

2. **Add `license: MIT` field** to all 131 SKILL.md files — Copilot bug #894 effectively requires this field. Add after `description:` and before any optional fields.

3. **Unquote description values** — Copilot bug #1024 breaks on `description: "quoted text"`. Remove surrounding double quotes from all description values. This includes `dotnet-advisor` and all other skills. Use **raw-line inspection** (not YAML parse) to detect quoting, since parsed YAML loses quote information.
   - Verify no description starts with YAML special characters (`{`, `[`, `*`, `&`, `!`, `%`, `@`, `` ` ``) after unquoting.
   - Verify no description contains mid-string YAML-unsafe patterns (`: ` followed by a value, ` #` interpreted as comment, leading `?`). If any exist, rewrite the description to avoid the hazard (e.g., rephrase or use different punctuation).
   - Single-quoted `dotnet-gha-patterns` also needs unquoting.
   - **YAML round-trip verification**: After unquoting, the migration script must parse each modified SKILL.md with Python `yaml.safe_load()` and verify the description value matches the intended plain text. This catches any case where unquoting introduced a parse error or altered the value. Use `python3 -m pip install --user pyyaml` for the migration script (one-off dependency, not committed to repo requirements).

4. **Add raw-frontmatter Copilot safety checks to `_validate_skills.py`** (in `process_file()`, before/alongside YAML parsing):
   - **BOM check**: `content.startswith("\ufeff")` → ERROR
   - **Quoted description**: regex for `description:\s*["']` on raw line → ERROR
   - **Missing license**: `license` not in parsed frontmatter → ERROR
   - **metadata ordering**: Enforce the invariant verified in step 1 → ERROR. Exact check logic derived from experiment evidence.

5. **Add `license` to both `ALLOWED_FRONTMATTER_FIELDS` and `FIELD_TYPES`** in `_validate_skills.py`. Set type to `str`.

6. Write a migration script (temporary, not committed) that processes all 131 files.

## Key context

- **Sequential dependency**: This task and T3 both edit `_validate_skills.py`. They must NOT run in parallel — changes must be rebased/merged sequentially (T2 first, then T3).
- All 131 skills currently use `description: "..."` (double-quoted). Copilot CLI #1024 fails on quoted descriptions.
- `_validate_skills.py` parses YAML and loses quoting info — raw-line checks are needed alongside the YAML parse
- The `EXTRA_FIELD_COUNT` baseline in `routing-warnings-baseline.json` will NOT be affected because `license` will be in the allowed set
- This task is the sole owner of all Copilot frontmatter checks in `_validate_skills.py` — T3 does NOT add frontmatter checks (only layout guard + similarity)
- After T1 flatten, `validate-similarity.py` will find zero skills until T3 fixes its glob — so this task validates with `_validate_skills.py` directly, not the full `validate-skills.sh`

## Done summary

_Populated by flowctl done._

## Evidence

_Populated by flowctl done._

## Acceptance
- [ ] metadata-ordering behavior verified with Copilot CLI test skills; exact command and observed output recorded as evidence (or conservative assumption documented if CLI unavailable)
- [ ] Validator enforces the verified metadata-ordering invariant as an ERROR
- [ ] All 131 SKILL.md files contain `license: MIT` in frontmatter
- [ ] No SKILL.md file has double-quoted or single-quoted `description:` value (verified by raw-line inspection)
- [ ] No SKILL.md file starts with UTF-8 BOM
- [ ] `license` added to both `ALLOWED_FRONTMATTER_FIELDS` and `FIELD_TYPES` in `_validate_skills.py`
- [ ] Raw-frontmatter Copilot safety checks added to validator as ERRORs (BOM, quoted description, missing license, metadata ordering)
- [ ] Frontmatter-only validation passes (before T3 similarity fix): `python3 scripts/_validate_skills.py --repo-root . --projected-skills 131 --max-desc-chars 120 --warn-threshold 12000 --fail-threshold 15600 --allow-planned-refs`
- [ ] Full `./scripts/validate-skills.sh` passes after T3 lands
- [ ] Spot-check 5 descriptions containing colons parse correctly with Python yaml
