# fn-50-versioning-release-workflow-and.4 Move validation scripts from plugin dir to repo top-level

## Description
Move validation scripts from `plugins/dotnet-artisan/scripts/` to repo top-level `scripts/`. These are repo-level tooling (CI/CD validation), not plugin content distributed to users.

**Size:** S
**Files:**
- `plugins/dotnet-artisan/scripts/validate-skills.sh` → `scripts/validate-skills.sh`
- `plugins/dotnet-artisan/scripts/_validate_skills.py` → `scripts/_validate_skills.py`
- `plugins/dotnet-artisan/scripts/validate-marketplace.sh` → `scripts/validate-marketplace.sh`
- `.github/workflows/validate.yml` (update script paths)
- `.github/workflows/release.yml` (update script paths)
- `CLAUDE.md` (root — update validation commands section)
- `plugins/dotnet-artisan/CLAUDE.md` (update or remove script references)
- `CONTRIBUTING.md` (update validation commands)

## Approach

1. `git mv` all three scripts from `plugins/dotnet-artisan/scripts/` to `scripts/`
2. Remove empty `plugins/dotnet-artisan/scripts/` directory
3. Update all path references in CI workflows (`validate.yml`, `release.yml`)
4. Update `CLAUDE.md` validation commands from `cd plugins/dotnet-artisan && ./scripts/...` to `./scripts/...`
5. Update `CONTRIBUTING.md` validation commands similarly
6. Update `plugins/dotnet-artisan/CLAUDE.md` if it references scripts path
7. Scripts may use relative paths internally (e.g., `cd` to plugin dir) — update any internal path assumptions to work from repo root

## Key context

- The scripts use `SCRIPT_DIR` / `PLUGIN_DIR` variables internally — these need updating to resolve from repo root
- `validate-marketplace.sh` validates both root marketplace.json and per-plugin marketplace.json — paths inside may be relative
- `_validate_skills.py` is called by `validate-skills.sh` — the internal reference must stay consistent
- CI workflows currently `cd plugins/dotnet-artisan` before running scripts — this changes to running from repo root
## Acceptance
- [ ] All three scripts moved to `scripts/` at repo root
- [ ] `plugins/dotnet-artisan/scripts/` directory removed
- [ ] `validate.yml` references `scripts/validate-skills.sh` and `scripts/validate-marketplace.sh`
- [ ] `release.yml` references updated script paths
- [ ] Scripts work correctly from repo root (internal path resolution updated)
- [ ] `CLAUDE.md` validation commands use new paths
- [ ] `CONTRIBUTING.md` validation commands use new paths
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` passes from repo root
## Done summary
Moved validation scripts (validate-skills.sh, _validate_skills.py, validate-marketplace.sh) from plugins/dotnet-artisan/scripts/ to repo-root scripts/. Updated internal path resolution to use PLUGIN_DIR for plugin-relative paths. Updated CI workflows (validate.yml, release.yml) to run scripts from repo root. Updated documentation (CLAUDE.md, CONTRIBUTING.md, plugins/dotnet-artisan/CLAUDE.md) with new script locations.
## Evidence
- Commits: 6978ceaf2743544b7ea921cfb96542f5d0781c28
- Tests: ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
- PRs: