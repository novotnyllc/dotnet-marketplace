# fn-42-restructure-repo-into-marketplace-with.3 Update CI workflows and per-plugin versioning

## Description
Update GitHub Actions workflows for the new marketplace structure. Remove dist generation steps. Implement per-plugin versioning with plugin-prefixed tags. Add root marketplace.json validation directly in CI.

**Size:** S
**Files:** `.github/workflows/validate.yml`, `.github/workflows/release.yml`

## Approach

### validate.yml

- **Root marketplace.json validation**: Validate root `.claude-plugin/marketplace.json` directly in the workflow — check JSON is valid and each plugin in the `plugins[]` array has a `source` path pointing to a directory containing `.claude-plugin/plugin.json`. This is the only place root marketplace.json is validated (not in validate-marketplace.sh).
- **Plugin-level JSON validation**: Validate `plugins/dotnet-artisan/.claude-plugin/plugin.json`, `plugins/dotnet-artisan/.claude-plugin/marketplace.json`, `plugins/dotnet-artisan/hooks/hooks.json`, `plugins/dotnet-artisan/.mcp.json`
- **Validate skills step**: `cd plugins/dotnet-artisan && ./scripts/validate-skills.sh`
- **Validate marketplace step**: `cd plugins/dotnet-artisan && ./scripts/validate-marketplace.sh` (validates per-plugin manifests only)
- **Remove** "Generate dist/ outputs" and "Validate cross-agent conformance" steps entirely
- **Job summary**: Keep description budget metrics, remove dist-related metrics

### release.yml

- **Trigger**: Change from `v*` to `dotnet-artisan/v*` tags
- **Version extraction**: Parse version from `dotnet-artisan/v0.1.0` format
- **Remove Pages deployment**: Drop `configure-pages`, `upload-pages-artifact`, `deploy-pages` steps and `pages` concurrency group
- **Remove permissions**: Drop `pages: write` and `id-token: write` (only needed for Pages)
- **Release body**: Update to reference plugin install command, not dist URLs
- **Validation**: Run from plugin directory (same as validate.yml)

### Per-plugin versioning

- Version source of truth: `plugins/dotnet-artisan/.claude-plugin/plugin.json` `version` field
- Tag format: `dotnet-artisan/v0.1.0`
- GitHub Release name: `dotnet-artisan v0.1.0`

## Key Context

- Current validate.yml at `.github/workflows/validate.yml:1-72`
- Current release.yml at `.github/workflows/release.yml:1-97`
- Both currently reference generate_dist.py and validate_cross_agent.py (deleted in Task 1)
- Work happens on feature branch — intermediate CI failures on the branch are OK

## Acceptance
- [ ] validate.yml validates root marketplace.json (JSON valid + source paths resolve) directly in workflow
- [ ] validate.yml validates plugin-level JSON files at new paths
- [ ] validate.yml runs skill and marketplace validation from `plugins/dotnet-artisan/`
- [ ] validate.yml has no references to generate_dist.py or validate_cross_agent.py
- [ ] release.yml triggers on `dotnet-artisan/v*` tags
- [ ] release.yml has no Pages deployment steps or pages permissions
- [ ] release.yml creates GitHub Release with plugin install instructions in body
- [ ] Both workflows pass on the restructured branch
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
