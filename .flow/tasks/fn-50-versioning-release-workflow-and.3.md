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

**validate-marketplace.sh** updates:
- Update recommended field checks: `categories` (array) → `category` (string) for root marketplace.json
- Add check for new required fields in root marketplace.json: `$schema`, `name`, `owner`
- Add check for new plugin.json fields: `author`, `homepage`, `repository`, `license`, `keywords`
- Ensure stable output keys are maintained for CI parsing
- Update any internal path assumptions for running from repo root (done partially in task .4)

**CONTRIBUTING.md** — Expand "Release" section:
- Document tag naming convention (`dotnet-artisan/vX.Y.Z`)
- Document bump script usage (`./scripts/bump.sh patch|minor|major`)
- Document release workflow behavior (tag → validate → extract CHANGELOG → GitHub Release)
- Add "Version Management" subsection explaining version source of truth and sync
- Update validation commands to use repo-root paths

**CLAUDE.md** (root) — Update "File Structure" and "Validation" sections:
- Document the new marketplace.json schema fields
- Document the new plugin.json fields
- Add `scripts/bump.sh` and `scripts/validate-root-marketplace.sh` to file structure
- Update validation commands to `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- Update file structure to show scripts at repo root

**CHANGELOG.md** — Fix footer links:
- Change `[unreleased]: .../compare/v0.1.0...HEAD` to `.../compare/dotnet-artisan/v0.1.0...HEAD`
- Change `[0.1.0]: .../releases/tag/v0.1.0` to note that no release tag exists for 0.1.0 (or remove)
- Add entry in `[Unreleased]` section for this epic's changes

## Key context

- validate-marketplace.sh uses stable output keys (CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS) that CI parses — preserve these
- CONTRIBUTING.md currently has a minimal "Release" section at lines 143-145
- CLAUDE.md references `plugin.json` schema at lines 45-50
- Per memory: "When updating counts in prose (README, AGENTS.md, CLAUDE.md), also grep for counts inside Mermaid diagram blocks"
- Scripts are now at repo root `scripts/` (moved in task .4) — all doc references must match
## Approach

**validate-marketplace.sh** updates:
- Update recommended field checks: `categories` (array) → `category` (string) for root marketplace.json
- Add check for new required fields in root marketplace.json: `$schema`, `name`, `owner`
- Add check for new plugin.json fields: `author`, `homepage`, `repository`, `license`, `keywords`
- Ensure stable output keys are maintained for CI parsing

**CONTRIBUTING.md** — Expand "Release" section:
- Document tag naming convention (`dotnet-artisan/vX.Y.Z`)
- Document bump script usage (`./scripts/bump.sh patch|minor|major`)
- Document release workflow behavior (tag → validate → extract CHANGELOG → GitHub Release)
- Add "Version Management" subsection explaining version source of truth and sync

**CLAUDE.md** (root) — Update "File Structure" and "Validation" sections:
- Document the new marketplace.json schema fields
- Document the new plugin.json fields
- Add `scripts/bump.sh` and `scripts/validate-root-marketplace.sh` to file structure
- Update validation commands section to include root marketplace validation

**CHANGELOG.md** — Fix footer links:
- Change `[unreleased]: .../compare/v0.1.0...HEAD` to `.../compare/dotnet-artisan/v0.1.0...HEAD`
- Change `[0.1.0]: .../releases/tag/v0.1.0` to note that no release tag exists for 0.1.0 (or remove)
- Add entry in `[Unreleased]` section for this epic's changes

## Key context

- validate-marketplace.sh uses stable output keys (CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS) that CI parses — preserve these
- CONTRIBUTING.md currently has a minimal "Release" section at lines 143-145
- CLAUDE.md references `plugin.json` schema at lines 45-50
- Per memory: "When updating counts in prose (README, AGENTS.md, CLAUDE.md), also grep for counts inside Mermaid diagram blocks"
## Acceptance
- [ ] `validate-marketplace.sh` validates `category` (string) instead of `categories` (array)
- [ ] `validate-marketplace.sh` checks for new plugin.json fields (author, homepage, repository, license, keywords)
- [ ] `validate-marketplace.sh` passes with the updated JSON files from task 1
- [ ] CONTRIBUTING.md "Release" section documents bump script, tag convention, and workflow
- [ ] CONTRIBUTING.md validation commands reference `./scripts/` paths
- [ ] CLAUDE.md file structure section includes new scripts at repo root and updated schema
- [ ] CLAUDE.md validation commands use `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- [ ] CHANGELOG.md footer links use `dotnet-artisan/v*` tag format (or note no tag for 0.1.0)
- [ ] CHANGELOG.md `[Unreleased]` section documents this epic's changes
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` both pass end-to-end from repo root
- [ ] Stable CI output keys preserved in validate-marketplace.sh
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
