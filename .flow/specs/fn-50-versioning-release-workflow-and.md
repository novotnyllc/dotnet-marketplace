# Versioning, Release Workflow, and Metadata Optimization

## Overview

Align the dotnet-artisan repo with the official Claude Code plugin marketplace schema and community best practices (modeled on gmickel-claude-marketplace). Four areas of work:

1. **Metadata optimization** — Restructure root `marketplace.json` to match the official Anthropic schema (`name`, `owner`, `metadata`, `$schema`). Enrich `plugin.json` with missing discoverability fields (`author`, `homepage`, `repository`, `license`, `keywords`). Use singular `category` (string) per the official pattern instead of `categories` (array).

2. **Script relocation** — Move validation scripts from `plugins/dotnet-artisan/scripts/` to repo top-level `scripts/`. These are repo-level CI/CD tooling, not plugin content distributed to users.

3. **Version bump automation** — Create a `scripts/bump.sh` script that accepts `patch|minor|major` and propagates the new version to all version-bearing files: `plugin.json` (canonical source of truth), per-plugin `marketplace.json`, root marketplace.json plugin entry, `README.md` badge, and `CHANGELOG.md` footer links. The bump script prints next-step instructions for tagging.

4. **Release workflow improvements** — Update `release.yml` to extract release notes from `CHANGELOG.md` dynamically (awk-based extraction) instead of the current static body. Add version consistency validation to CI. Extract duplicated root marketplace.json validation into a shared script. Fix CHANGELOG footer links to use the `dotnet-artisan/v*` tag format.

## Key Decisions

- **Version source of truth**: `plugins/dotnet-artisan/.claude-plugin/plugin.json` → `version` field (per Claude Code docs: plugin.json takes priority)
- **Tag format**: Keep existing `dotnet-artisan/v*` pattern (already in release.yml)
- **Per-plugin marketplace.json**: Keep it (removing would break validation). Treat it as metadata file; root marketplace.json is discovery file.
- **Category**: Use singular `category: "development"` in root marketplace.json plugin entries (official pattern). Keep `keywords` array for searchability.
- **No retroactive v0.1.0 tag**: Start fresh; fix CHANGELOG footer to note no release tag exists for 0.1.0.
- **`$schema` field**: Include `"$schema": "https://anthropic.com/claude-code/marketplace.schema.json"` (used by official repo).
- **Scripts at repo root**: Validation scripts live in `scripts/` at repo root, not inside the plugin directory. They are repo-level CI/CD tooling.

## Quick commands

```bash
# Validate after changes (from repo root)
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh

# Test bump script
./scripts/bump.sh patch

# Validate root marketplace.json
./scripts/validate-root-marketplace.sh
```

## Acceptance

- [ ] Root marketplace.json has `$schema`, `name`, `owner`, `metadata` fields matching official pattern
- [ ] Root marketplace.json plugin entries have `version`, `category`, `homepage`, `keywords`
- [ ] plugin.json has `author`, `homepage`, `repository`, `license`, `keywords`
- [ ] Validation scripts moved from `plugins/dotnet-artisan/scripts/` to `scripts/` at repo root
- [ ] `scripts/bump.sh` propagates version to all 5 locations (plugin.json, per-plugin marketplace.json, root marketplace.json, README badge, CHANGELOG footer)
- [ ] `release.yml` extracts version-specific section from CHANGELOG.md for release body
- [ ] CI validates version consistency across plugin.json and marketplace.json files
- [ ] Root marketplace.json validation extracted to shared script (used by validate.yml and release.yml)
- [ ] CHANGELOG.md footer links use `dotnet-artisan/v*` tag format
- [ ] `validate-marketplace.sh` updated for schema changes (`category` string instead of `categories` array)
- [ ] CONTRIBUTING.md documents release process and tag convention
- [ ] All validation commands pass from repo root: `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`

## References

- gmickel marketplace.json: uses `name`, `owner`, `metadata.version`, per-plugin `tags`/`homepage`
- gmickel `scripts/bump.sh`: jq-based version propagation, prints tagging instructions
- gmickel `release.yml`: awk-based CHANGELOG extraction into GitHub Release body
- Official Anthropic marketplace: `$schema`, `owner`, singular `category`, `homepage`
- Official docs: plugin.json version takes priority over marketplace entry version
- Jeffallan/claude-skills: validation gate before release, per-plugin `repository`/`license`/`keywords`
