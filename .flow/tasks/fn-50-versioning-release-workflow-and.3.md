# fn-50-versioning-release-workflow-and.3 Update validation scripts, docs, and CHANGELOG references

## Description
Update validation scripts, documentation, and CHANGELOG to reflect the new schema, new script locations, and release process.

**Size:** M
**Files:**
- `scripts/validate-marketplace.sh` (now at repo root, moved in task .4)
- `CONTRIBUTING.md`
- `CLAUDE.md` (root)
- `CHANGELOG.md`
- `plugins/dotnet-artisan/README.md` (if badge/release notes section needed)

## Approach

<!-- Updated by plan-sync: fn-50-versioning-release-workflow-and.2 already added root marketplace.json validation to validate-marketplace.sh (lines 244-308) AND created scripts/validate-root-marketplace.sh as a separate shared script. The `categories` (array) to `category` (string) change is already done in validate-root-marketplace.sh. validate.yml already calls validate-root-marketplace.sh and has a 3-way version consistency check. CHANGELOG footer links are auto-fixed by bump.sh when a version bump is run. -->

**validate-marketplace.sh** updates:
- Root marketplace.json checks (`name`, `description`, `owner.name`, `plugins`, `metadata`, `$schema`) already added by task .2 (lines 244-308) — review for completeness, do not duplicate
- `categories` (array) to `category` (string) already handled by `scripts/validate-root-marketplace.sh` (line 98) — verify `validate-marketplace.sh` root section is consistent
- Reconcile overlap: root marketplace validation now exists in BOTH `validate-marketplace.sh` (lines 244-308) and `scripts/validate-root-marketplace.sh` — decide whether to keep both or deduplicate
- Add check for new plugin.json fields: `author`, `homepage`, `repository`, `license`, `keywords` (not yet done)
- Ensure stable output keys are maintained for CI parsing

**CONTRIBUTING.md** — Expand "Release" section:
- Document tag naming convention (`dotnet-artisan/vX.Y.Z`)
- Document bump script usage (`./scripts/bump.sh <patch|minor|major> [plugin-name]`, default plugin: `dotnet-artisan`)
- Document release workflow behavior (tag push triggers: validate -> verify tag matches plugin.json -> extract CHANGELOG section via awk -> GitHub Release with install instructions)
- Document that `scripts/validate-root-marketplace.sh` runs as a separate shared validation step in both `validate.yml` and `release.yml`
- Add "Version Management" subsection explaining: plugin.json is canonical source of truth; bump.sh propagates to 5 locations (plugin.json, root marketplace plugin entry, root marketplace metadata.version, README badge, CHANGELOG)
- Document version consistency check in `validate.yml` (3-way: plugin.json vs root marketplace plugin entry vs root marketplace metadata.version)
- Update validation commands to use repo-root paths

**CLAUDE.md** (root) — Update "File Structure" and "Validation" sections:
- Document the new marketplace.json schema fields
- Document the new plugin.json fields
- Add `scripts/bump.sh` and `scripts/validate-root-marketplace.sh` to file structure
- Update validation commands to `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- Note that `./scripts/validate-root-marketplace.sh` also exists as a standalone check (used by CI workflows directly)
- Update file structure to show scripts at repo root

**CHANGELOG.md** — Fix footer links:
- Verify current state: `bump.sh` auto-fixes old `v0.1.0` format to `dotnet-artisan/v0.1.0` during bumps (lines 195-199), so links may already be correct if a bump was run
- If not yet bumped: change `[unreleased]: .../compare/v0.1.0...HEAD` to `.../compare/dotnet-artisan/v0.1.0...HEAD`
- If not yet bumped: change `[0.1.0]: .../releases/tag/v0.1.0` to note that no release tag exists for 0.1.0 (or remove)
- Add entry in `[Unreleased]` section for this epic's changes

## Key context

- validate-marketplace.sh uses stable output keys (CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS) that CI parses — preserve these
- CONTRIBUTING.md currently has a minimal "Release" section at lines 143-145
- CLAUDE.md references `plugin.json` schema at lines 45-50
- Per memory: "When updating counts in prose (README, AGENTS.md, CLAUDE.md), also grep for counts inside Mermaid diagram blocks"
- Scripts are now at repo root `scripts/` (moved in task .4) — all doc references must match
- Root marketplace validation exists in TWO places after task .2: `validate-marketplace.sh` (lines 244-308) and `scripts/validate-root-marketplace.sh` — task .3 should reconcile this overlap
- `validate.yml` already calls `scripts/validate-root-marketplace.sh` (line 23-25) and has version consistency check (lines 55-89)
- `release.yml` already calls `scripts/validate-root-marketplace.sh` (line 51-53) and verifies tag version matches plugin.json (lines 32-48)
- bump.sh accepts `<patch|minor|major> [plugin-name]` (not `patch|minor|major` without brackets)
## Acceptance
- [ ] Root marketplace.json validation in `validate-marketplace.sh` (lines 244-308) is reconciled with `scripts/validate-root-marketplace.sh` (no conflicting or duplicated logic)
- [ ] `validate-marketplace.sh` validates `category` (string) — already done in `validate-root-marketplace.sh`; verify consistency in `validate-marketplace.sh` root section
- [ ] `validate-marketplace.sh` checks for new plugin.json fields (author, homepage, repository, license, keywords)
- [ ] `validate-marketplace.sh` passes with the updated JSON files from task 1
- [ ] CONTRIBUTING.md "Release" section documents bump script (`./scripts/bump.sh <patch|minor|major> [plugin-name]`), tag convention (`dotnet-artisan/vX.Y.Z`), and workflow
- [ ] CONTRIBUTING.md documents version source of truth (plugin.json) and 5 propagation targets
- [ ] CONTRIBUTING.md validation commands reference `./scripts/` paths
- [ ] CLAUDE.md file structure section includes `scripts/bump.sh`, `scripts/validate-root-marketplace.sh`, and updated schema
- [ ] CLAUDE.md validation commands use `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- [ ] CHANGELOG.md footer links use `dotnet-artisan/v*` tag format (or note no tag for 0.1.0) — check if bump.sh already fixed these
- [ ] CHANGELOG.md `[Unreleased]` section documents this epic's changes
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` both pass end-to-end from repo root
- [ ] Stable CI output keys preserved in validate-marketplace.sh
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
