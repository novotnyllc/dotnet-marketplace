# fn-42-restructure-repo-into-marketplace-with.3 Update CI workflows and per-plugin versioning

## Description
Update GitHub Actions workflows for the new marketplace structure. Remove dist generation steps. Implement per-plugin versioning with plugin-prefixed tags.

**Size:** S
**Files:** `.github/workflows/validate.yml`, `.github/workflows/release.yml`

## Approach

### validate.yml

- **JSON validation step**: Update paths — `plugins/dotnet-artisan/.claude-plugin/plugin.json`, `plugins/dotnet-artisan/.claude-plugin/marketplace.json`, `plugins/dotnet-artisan/hooks/hooks.json`, `plugins/dotnet-artisan/.mcp.json`. Also validate root `.claude-plugin/marketplace.json`.
- **Validate skills step**: Run from plugin directory: `cd plugins/dotnet-artisan && ./scripts/validate-skills.sh`
- **Validate marketplace step**: Run from plugin directory: `cd plugins/dotnet-artisan && ./scripts/validate-marketplace.sh`
- **Remove "Generate dist/ outputs" step**: No more `python3 scripts/generate_dist.py --strict`
- **Remove "Validate cross-agent conformance" step**: No more `python3 scripts/validate_cross_agent.py`
- **Job summary**: Keep the description budget metrics, remove dist-related metrics

### release.yml

- **Trigger**: Change from `v*` tags to `dotnet-artisan/v*` tags:
  ```yaml
  on:
    push:
      tags:
        - 'dotnet-artisan/v*'
  ```
- **Version extraction**: Parse version from `dotnet-artisan/v0.1.0` format
- **Remove Pages deployment**: No more `dist/` to deploy. Remove `configure-pages`, `upload-pages-artifact`, `deploy-pages` steps and `pages` concurrency group.
- **Remove permissions**: Drop `pages: write` and `id-token: write` (only needed for Pages)
- **Release body**: Update to reflect plugin-specific release (not cross-agent dist). Reference plugin install command.
- **Validation**: Run from plugin directory (same as validate.yml)

### Per-plugin versioning

- Version source of truth: `plugins/dotnet-artisan/.claude-plugin/plugin.json` `version` field
- Tag format: `dotnet-artisan/v0.1.0`
- GitHub Release name: `dotnet-artisan v0.1.0`
- Future plugins get their own tag prefix and release workflow (or a matrix workflow)

## Key Context

- Current validate.yml at `.github/workflows/validate.yml:1-72`
- Current release.yml at `.github/workflows/release.yml:1-97`
- Both currently run generate_dist.py and validate_cross_agent.py — both being deleted in Task .1
- Pages deployment served dist/ — no longer applicable

## Acceptance
- [ ] validate.yml validates JSON files at new paths (root marketplace + plugin manifests)
- [ ] validate.yml runs skill and marketplace validation from `plugins/dotnet-artisan/`
- [ ] validate.yml has no references to generate_dist.py or validate_cross_agent.py
- [ ] release.yml triggers on `dotnet-artisan/v*` tags
- [ ] release.yml has no Pages deployment steps
- [ ] release.yml creates GitHub Release with plugin-appropriate body
- [ ] Both workflows pass on current main branch state
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
