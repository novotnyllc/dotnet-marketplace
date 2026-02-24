# fn-60.7 Fix eval auth and add skill restore safety

## Description

Two infrastructure fixes before running evals:

1. **Auth**: `_common.py:get_client()` hard-requires `ANTHROPIC_API_KEY` env var via a pre-validation check. This double-validates what the SDK already checks internally. Fix: remove the pre-validation and let the SDK handle auth discovery. The Python Anthropic SDK checks `ANTHROPIC_API_KEY` internally when no explicit key is passed to `Anthropic()` -- removing our check means the SDK surfaces its own auth error if the key is missing, which is more actionable than our generic ValueError.

2. **Config api_key injection**: `load_config()` injects `cfg["api_key"] = os.environ.get("ANTHROPIC_API_KEY","")` into the cached config dict. This creates a stale-key risk if the env var changes and obscures debugging with empty strings. Remove this injection entirely -- `get_client()` should handle auth directly, not read from config cache.

3. **Skill restore**: Tasks .3 and .4 will modify skill SKILL.md files. Need a safe restore mechanism so originals can be recovered. Approach: git-based -- all modifications happen on a dedicated branch, and `git checkout -- skills/` restores originals. Document this in task specs.

**Size:** S
**Files:**
- `tests/evals/_common.py` -- fix `get_client()` to remove pre-validation; remove `api_key` injection from `load_config()`; update module and function docstrings to match new behavior
- `tests/evals/config.yaml` -- update comment: "ANTHROPIC_API_KEY (required unless using an explicit key param in code)"

## Approach

### Auth Fix

Change `get_client()` in `_common.py`:
- If an explicit `api_key` is passed, use it
- If `ANTHROPIC_API_KEY` env var is set, use it
- Otherwise, create `anthropic.Anthropic()` with no key arg -- the SDK checks `ANTHROPIC_API_KEY` internally and raises its own exception with a clear message if missing
- Remove the pre-validation `ValueError`

Change `load_config()` in `_common.py`:
- Remove `cfg["api_key"] = os.environ.get("ANTHROPIC_API_KEY","")` line
- Do NOT cache auth state in the config dict
- Any code that previously read `cfg["api_key"]` should use `get_client()` instead

Update docstrings:
- Module docstring: remove references to API key injection into config
- `load_config()` docstring: update to reflect that config loading no longer merges auth env vars
- `get_client()` docstring: document the auth resolution order (explicit param > env var > SDK default)

Update `config.yaml` comment to: "ANTHROPIC_API_KEY (required unless using an explicit key param in code)"

This makes the runners work with:
- `ANTHROPIC_API_KEY` env var (CI, explicit)
- Explicit key parameter (programmatic)

### Skill Restore Strategy

The eval runners (`run_*.py`) only READ skills from `REPO_ROOT/skills/` -- they never modify them. Skills are modified only in tasks .3 and .4 (manual edits to SKILL.md files).

Restore mechanism:
- All changes happen on the current branch (`evals`)
- At any point, `git checkout -- skills/` restores all skill files to their committed state
- Before starting fix tasks (.3/.4), commit the current clean state as a checkpoint
- After each fix batch, commit with a descriptive message
- If a fix batch makes things worse, `git revert` the commit

This mirrors test.sh's snapshot/restore pattern but uses git instead of rsync.

## Acceptance
- [ ] `get_client()` works when `ANTHROPIC_API_KEY` env var is set (standard path)
- [ ] `get_client()` works with explicit key parameter (programmatic path)
- [ ] `get_client()` without env var or explicit key surfaces an SDK-originated exception (not our custom ValueError pre-check) with an actionable message about missing credentials
- [ ] `load_config()` no longer injects `api_key` into config dict
- [ ] No remaining code reads `cfg["api_key"]` -- all auth goes through `get_client()`
- [ ] Module, `load_config()`, and `get_client()` docstrings updated to match new behavior
- [ ] Config comment updated to: "ANTHROPIC_API_KEY (required unless using an explicit key param in code)"
- [ ] `pip install -r tests/evals/requirements.txt` succeeds (anthropic SDK installable)
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works

## Done summary
Removed auth pre-validation and api_key config injection from _common.py. get_client() now delegates auth discovery entirely to the Anthropic SDK (explicit param > env var > SDK error). Removed unused os import. Updated all docstrings and config.yaml comment to reflect new auth behavior.
## Evidence
- Commits: 0260bc32887fa618c3324e1a53eaf4c3d1f6fd14
- Tests: python3 tests/evals/run_activation.py --dry-run, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: