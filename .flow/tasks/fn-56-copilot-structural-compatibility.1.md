# fn-56-copilot-structural-compatibility.1 Atomic flatten of skills directory

## Description

Move all 131 skill directories from `skills/<category>/<skill-name>/` to `skills/<skill-name>/` in a single atomic commit. Update all path references that depend on the nested layout.

**Size:** M
**Files:** skills/ (131 directories moved), .claude-plugin/plugin.json (all entries in `skills[]`), test.sh (find depth), .agents/openai.yaml (default_prompt path pattern), scripts/validate-skills.sh (projected count)

## Approach

1. **Preflight collision check**: Build a map of `<skill-name> -> source paths`. Hard-fail if any duplicate skill names exist across categories before running any `git mv`. (Currently all 131 names are unique, but this guard prevents silent overwrites.)

2. **Flatten via `git mv`**: Write a shell script that iterates all `skills/<category>/<skill-name>/` directories and runs `git mv` for each to `skills/<skill-name>/` — preserves git history.

3. **Update all entries in `.claude-plugin/plugin.json`** `skills` array from `./skills/<category>/<skill-name>` to `./skills/<skill-name>`. Verify count with `jq '.skills|length'`.

4. **Fix `test.sh` Codex sync**: Change `find "$REPO_ROOT/skills" -mindepth 2 -maxdepth 2 -type d` to `-mindepth 1 -maxdepth 1 -type d`. Additionally, add a `SKILL.md` existence check inside each found directory to avoid syncing non-skill directories.

5. **Update `.agents/openai.yaml`** — change `skills/<category>/<skill-name>/` to `skills/<skill-name>/` in both `default_prompt` and `short_description`. Update skill count to 131 in both fields.

6. **Update `scripts/validate-skills.sh`** — change `--projected-skills 130` to `--projected-skills 131`.

7. **Remove empty category directories** (25 dirs including `containers/`, `data-access/`).

8. **Preserve companion files**: `details.md` (2 skills), `reference/` (windbg - 16 files), `scripts/` (version-detection). `git mv` of the parent directory handles this automatically.

9. **Verify skill count preserved**: `find skills -name SKILL.md -maxdepth 2 | wc -l` must equal 131.

10. All operations in a single commit.

## Key context

- `_validate_skills.py` `skills_dir.rglob("SKILL.md")` finds skills at any depth — works after flatten
- `_validate_skills.py` extracts IDs from `f.parent.name` (directory name only) — no change needed
- `validate-similarity.py` `collect_skill_descriptions()` uses `glob("*/*/SKILL.md")` — finds ZERO skills after flatten. Fixed in T3, not here.
- `test.sh` Codex sync `find` command with `-mindepth 2 -maxdepth 2` is the primary depth-sensitive command
- Intermediate commits may fail CI (similarity validator breaks until T3 lands) — this is expected; the PR must be green at the end

## Acceptance
- [ ] Preflight collision check runs and passes (no duplicate skill names)
- [ ] All 131 skills exist at `skills/<skill-name>/SKILL.md` (one level deep)
- [ ] No `skills/<category>/<skill-name>/SKILL.md` paths remain
- [ ] No empty category directories remain under `skills/`
- [ ] All `plugin.json` skill paths updated to `./skills/<skill-name>` format (verified via `jq '.skills|length'`)
- [ ] `test.sh` find command uses `-mindepth 1 -maxdepth 1` with SKILL.md existence check
- [ ] `.agents/openai.yaml` `default_prompt` and `short_description` both reflect 131 + flat layout
- [ ] `scripts/validate-skills.sh` uses `--projected-skills 131`
- [ ] Companion files (details.md, reference/, scripts/) preserved with their skills
- [ ] `git log --follow` works for at least 3 sampled skill files (history preserved)
- [ ] Skill count: `find skills -name SKILL.md -maxdepth 2 | wc -l` equals 131
- [ ] Single commit containing all changes
