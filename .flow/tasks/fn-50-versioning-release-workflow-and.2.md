# fn-50-versioning-release-workflow-and.2 Add bump script, improve release workflow, and version validation

## Description
Create a version bump script and improve the release workflow. Add version consistency validation to CI.

**Size:** M
**Files:**
- `scripts/bump.sh` (NEW)
- `.github/workflows/release.yml`
- `scripts/validate-root-marketplace.sh` (NEW — extracted from inline CI)
- `.github/workflows/validate.yml` (update to use shared script)

## Approach

**Bump script** (`scripts/bump.sh`):
- Accept args: `<patch|minor|major> [plugin-name]` (default plugin: `dotnet-artisan`)
- Use `jq` to read current version from `plugins/<plugin>/.claude-plugin/plugin.json`
- Compute new semver (pure bash arithmetic or jq)
- Propagate new version to:
  1. `plugins/<plugin>/.claude-plugin/plugin.json` (canonical)
  2. `plugins/<plugin>/.claude-plugin/marketplace.json`
  3. `.claude-plugin/marketplace.json` (root, matching plugin entry by name)
  4. `plugins/<plugin>/README.md` (badge regex replacement)
  5. `.claude-plugin/marketplace.json` `metadata.version` (marketplace-level version)
- Update CHANGELOG.md: promote `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`, add new `[Unreleased]` section, update footer comparison links using `dotnet-artisan/v*` tag format
- Print next-step instructions: commit, push, `git tag dotnet-artisan/vX.Y.Z && git push origin dotnet-artisan/vX.Y.Z`
- Follow pattern from gmickel `scripts/bump.sh`

**Release workflow** — update `release.yml`:
- Replace static release body with awk-based CHANGELOG extraction (extract section between `## [VERSION]` and next `## [`)
- Use shared validation script instead of inline bash
- Add version-tag consistency check: verify tag version matches plugin.json version

**Shared validation script** (`scripts/validate-root-marketplace.sh`):
- Extract the duplicated root marketplace.json validation from `validate.yml` and `release.yml`
- Validate required fields: `name`, `owner.name`, `plugins` array, per-plugin `name`/`source`
- Check recommended fields: `$schema`, `metadata`, per-plugin `version`/`category`/`keywords`

**CI version check** — add step to `validate.yml`:
- Compare version in plugin.json vs per-plugin marketplace.json vs root marketplace.json plugin entry
- Fail if versions diverge

## Key context

- Uses awk to extract CHANGELOG sections: `awk '/^## \['"$VERSION"'\]/{flag=1;next}/^## \[/{flag=0}flag'`
- Current release.yml already triggers on `dotnet-artisan/v*` tags — keep that pattern
- Bump script must handle the case where no tags exist yet (first release)
- Scripts now live at repo root `scripts/` (moved in task .4)
## Approach

**Bump script** (`scripts/bump.sh`):
- Accept args: `<patch|minor|major> [plugin-name]` (default plugin: `dotnet-artisan`)
- Use `jq` to read current version from `plugins/<plugin>/.claude-plugin/plugin.json`
- Compute new semver (pure bash arithmetic or jq)
- Propagate new version to:
  1. `plugins/<plugin>/.claude-plugin/plugin.json` (canonical)
  2. `plugins/<plugin>/.claude-plugin/marketplace.json`
  3. `.claude-plugin/marketplace.json` (root, matching plugin entry by name)
  4. `plugins/<plugin>/README.md` (badge regex replacement)
  5. `.claude-plugin/marketplace.json` `metadata.version` (marketplace-level version)
- Update CHANGELOG.md: promote `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`, add new `[Unreleased]` section, update footer comparison links using `dotnet-artisan/v*` tag format
- Print next-step instructions: commit, push, `git tag dotnet-artisan/vX.Y.Z && git push origin dotnet-artisan/vX.Y.Z`
- Follow pattern from gmickel `scripts/bump.sh`

**Release workflow** — update `release.yml`:
- Replace static release body with awk-based CHANGELOG extraction (extract section between `## [VERSION]` and next `## [`)
- Use shared validation script instead of inline bash
- Add version-tag consistency check: verify tag version matches plugin.json version

**Shared validation script** (`scripts/validate-root-marketplace.sh`):
- Extract the duplicated root marketplace.json validation from `validate.yml` (lines 22-45) and `release.yml` (lines 32-45)
- Validate required fields: `name`, `owner.name`, `plugins` array, per-plugin `name`/`source`
- Check recommended fields: `$schema`, `metadata`, per-plugin `version`/`category`/`keywords`

**CI version check** — add step to `validate.yml`:
- Compare version in plugin.json vs per-plugin marketplace.json vs root marketplace.json plugin entry
- Fail if versions diverge

## Key context

- Uses awk to extract CHANGELOG sections: `awk '/^## \['"$VERSION"'\]/{flag=1;next}/^## \[/{flag=0}flag'`
- Current release.yml already triggers on `dotnet-artisan/v*` tags — keep that pattern
- Bump script must handle the case where no tags exist yet (first release)
- Root marketplace.json validation is currently duplicated in validate.yml and release.yml — consolidate
## Acceptance
- [ ] `scripts/bump.sh` exists, is executable, and accepts `patch|minor|major`
- [ ] Bump script updates all 5 version locations consistently
- [ ] Bump script promotes CHANGELOG `[Unreleased]` to versioned section with date
- [ ] Bump script updates CHANGELOG footer links with `dotnet-artisan/v*` format
- [ ] Bump script prints tagging instructions after completion
- [ ] `release.yml` extracts version-specific CHANGELOG section for release body
- [ ] `release.yml` verifies tag version matches plugin.json version
- [ ] `scripts/validate-root-marketplace.sh` exists and validates root marketplace.json
- [ ] `validate.yml` and `release.yml` both use the shared validation script
- [ ] `validate.yml` includes version consistency check across JSON files
- [ ] Bump script handles first-release scenario (no prior tags)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
