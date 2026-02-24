# fn-60.7 Fix eval auth and add skill restore safety

## Description

Two infrastructure fixes before running evals:

1. **Auth**: `_common.py:get_client()` hard-requires `ANTHROPIC_API_KEY` env var. This breaks on machines where the Anthropic SDK picks up auth via default mechanisms (e.g., key in shell profile, SDK auto-discovery). Fix: let the SDK handle auth discovery instead of pre-validating.

2. **Skill restore**: Tasks .3 and .4 will modify skill SKILL.md files. Need a safe restore mechanism so originals can be recovered. Approach: git-based -- all modifications happen on a dedicated branch, and `git checkout -- skills/` restores originals. Document this in task specs.

**Size:** S
**Files:**
- `tests/evals/_common.py` -- fix `get_client()` to not hard-require ANTHROPIC_API_KEY
- `tests/evals/config.yaml` -- update comment about auth

## Approach

### Auth Fix

Change `get_client()` in `_common.py`:
- If an explicit `api_key` is passed, use it
- If `ANTHROPIC_API_KEY` env var is set, use it
- Otherwise, create `anthropic.Anthropic()` with no key arg -- let the SDK handle auth discovery
- Remove the pre-validation `ValueError` -- let the SDK raise its own error if auth fails

This makes the runners work with:
- `ANTHROPIC_API_KEY` env var (CI, explicit)
- SDK default auth (local development)
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
- [ ] `get_client()` works without `ANTHROPIC_API_KEY` env var when SDK has default auth
- [ ] `get_client()` still works WITH `ANTHROPIC_API_KEY` env var (backward compat)
- [ ] Config comment updated to reflect auth flexibility
- [ ] `pip install -r tests/evals/requirements.txt` succeeds (anthropic SDK installable)
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
