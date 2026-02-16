---
name: plugin-self-publish
description: "WHEN maintaining or publishing dotnet-artisan itself. Versioning, changelog, CI/CD. WHEN NOT user .NET projects."
disable-model-invocation: true
---

# plugin-self-publish

Manages dotnet-artisan plugin versioning, changelog generation, and publishing workflow. This is a **side-effect command** -- it documents the process for maintaining the plugin itself, not for building .NET applications.

**Cross-references:** [skill:dotnet-advisor] (router), [skill:dotnet-version-detection] (version detection), [skill:dotnet-project-analysis] (project analysis)

---

## Versioning Strategy

dotnet-artisan follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes to skill interfaces, plugin.json schema, or agent behavior that requires user action
- **MINOR** (0.X.0): New skills, new categories, non-breaking enhancements to existing skills
- **PATCH** (0.0.X): Bug fixes, documentation corrections, typo fixes, validation improvements

### Version Location

The single source of truth for the plugin version is `.claude-plugin/plugin.json`:

```json
{
  "version": "0.1.0"
}
```

Update this value when preparing a release. The `marketplace.json` version MUST match.

### Pre-1.0 Convention

While the plugin is in initial development (0.x.y), minor version bumps may include breaking changes. Document these clearly in the changelog.

---

## Changelog Format

Maintain `CHANGELOG.md` in the repository root using the [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format:

```markdown
# Changelog

All notable changes to dotnet-artisan will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New skill: dotnet-csharp-modern-patterns (C# 14/15 features)

### Changed
- Updated dotnet-advisor catalog with new category stubs

### Fixed
- validate-skills.sh now handles SKILL.md files with CRLF line endings

## [0.1.0] - 2026-02-11

### Added
- Initial plugin skeleton with plugin.json and marketplace.json
- Foundation skills: dotnet-advisor, dotnet-version-detection, dotnet-project-analysis, plugin-self-publish
- Validation scripts: validate-skills.sh, validate-marketplace.sh
- dotnet-architect agent
```

### Changelog Rules

1. Every PR that changes user-facing behavior MUST update the `[Unreleased]` section
2. Use these categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`
3. When releasing, move `[Unreleased]` entries to the new version section with the release date
4. Link comparison URLs at the bottom of the file

---

## GitHub Releases Workflow

### Preparing a Release

1. **Update versions**: Set the new version in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
2. **Update changelog**: Move `[Unreleased]` entries to a new version section with today's date
3. **Run validation**: Execute both validation scripts to confirm everything passes:
   ```bash
   ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
   ```
4. **Commit**: `git commit -am "chore(release): prepare v0.2.0"`
5. **Tag**: `git tag v0.2.0`
6. **Push**: `git push origin main --tags`

### GitHub Release

Create a GitHub Release from the tag:

```bash
gh release create v0.2.0 \
  --title "v0.2.0" \
  --notes-file /tmp/release-notes.md
```

The release notes should be extracted from the changelog section for that version.

### Release Checklist

Before every release, verify:

- [ ] `plugin.json` version matches the tag
- [ ] `marketplace.json` version matches the tag
- [ ] `CHANGELOG.md` has entries for this version with correct date
- [ ] `validate-skills.sh` passes (exit code 0)
- [ ] `validate-marketplace.sh` passes (exit code 0)
- [ ] All SKILL.md files have required frontmatter (name, description)
- [ ] Budget status is OK or WARN (not FAIL)
- [ ] No broken cross-references (all `[skill:<name>]` refs resolve)

---

## Marketplace Publishing

### Prerequisites

- GitHub repository is public (or accessible to the marketplace)
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` are valid
- A GitHub Release exists with the target version tag

### Publishing Steps

1. Ensure the latest release tag is pushed to the repository
2. The marketplace indexes plugins from GitHub Releases automatically
3. Verify the plugin appears in the marketplace after indexing

### Post-Publish Verification

After publishing, confirm:
- Plugin is discoverable by name (`dotnet-artisan`)
- Plugin metadata (description, keywords, categories) renders correctly
- All skills are listed and accessible

---

## Validation Infrastructure

Two validation scripts ensure plugin integrity. Both are designed for identical use in local development and CI.

### validate-skills.sh

Validates all `SKILL.md` files in the repository:
- Required frontmatter: `name`, `description`
- YAML frontmatter is well-formed
- Cross-references using `[skill:<name>]` syntax point to existing skill directories
- Context budget tracking with stable output keys

Run: `./scripts/validate-skills.sh`

### validate-marketplace.sh

Validates plugin manifest and marketplace metadata:
- `plugin.json` schema compliance (skills, agents, hooks, mcpServers)
- `marketplace.json` completeness
- All referenced paths exist on disk

Run: `./scripts/validate-marketplace.sh`

### CI Integration

Both scripts run in CI on every push. The CI workflow invokes:

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

Same commands, same behavior, same exit codes as local development.
