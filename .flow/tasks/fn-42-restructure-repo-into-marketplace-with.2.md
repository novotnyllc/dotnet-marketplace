# fn-42-restructure-repo-into-marketplace-with.2 Restructure into marketplace with plugin subdirectory

## Description
Move all dotnet-artisan plugin content into `plugins/dotnet-artisan/`. Delete root plugin.json atomically (replacement created in same task). Create the root marketplace structure. Update all documentation and validation scripts. Update CHANGELOG.md.

**Size:** M (large M — involves ~140+ file moves, 3 new manifests, doc rewrites, validation script confirmation)
**Files:** Entire repo structure, `.claude-plugin/marketplace.json` (root), `plugins/dotnet-artisan/.claude-plugin/plugin.json`, `plugins/dotnet-artisan/.claude-plugin/marketplace.json`, docs, validation scripts, CHANGELOG.md

## Approach

### File Moves (git mv for history preservation)

Move INTO `plugins/dotnet-artisan/`:
- `skills/` (all 22 categories, 122 skills)
- `agents/` (14 specialist agents)
- `hooks/` (hooks.json)
- `scripts/hooks/` (post-edit-dotnet.sh, session-start-context.sh)
- `scripts/validate-skills.sh`, `scripts/_validate_skills.py`, `scripts/validate-marketplace.sh`
- `.mcp.json`
- `tests/`
- `AGENTS.md` (skill routing + agent delegation)
- `CONTRIBUTING-SKILLS.md`
- `docs/hooks-and-mcp-guide.md` → `plugins/dotnet-artisan/docs/`
- `docs/dotnet-artisan-spec.md` → `plugins/dotnet-artisan/docs/`

**Important**: Use `git mv` for each move to preserve file history. Do all moves before modifying content to keep git tracking renames cleanly.

### Root plugin.json Deletion

Delete `.claude-plugin/plugin.json` in this task (not Task 1). The replacement marketplace.json and per-plugin plugin.json are created in the same task, so there is no window where the repo lacks a discoverable manifest.

### Manifest Changes

**Root `.claude-plugin/marketplace.json`** (NEW — marketplace listing):
Follow the `anthropics/claude-plugins-official` pattern. **Before authoring, verify the exact marketplace.json schema from that repo** — do not invent fields like `"metadata": {"pluginRoot": ...}`. Contains marketplace name, owner, and plugins array with source paths.

**`plugins/dotnet-artisan/.claude-plugin/plugin.json`** (MOVED — paths unchanged):
All skill, agent, hook, and MCP paths are relative to the plugin root. Since the internal structure stays the same, NO path changes needed inside plugin.json.

**`plugins/dotnet-artisan/.claude-plugin/marketplace.json`** (MOVED — per-plugin metadata):
The existing marketplace.json (author, keywords, categories) moves here as per-plugin metadata.

### Documentation Updates

**Root `README.md`**: Rewrite as marketplace overview — what plugins are available, how to install, link to plugin READMEs.

**`plugins/dotnet-artisan/README.md`**: Move current root README.md content here (skill catalog, architecture, installation). Update path references. Fix agent count from 9 to 14 (pre-existing error, minimal content fix during move).

**Root `CLAUDE.md`**: Rewrite as minimal marketplace instructions. Point to plugin subdirectories for plugin-specific instructions.

**`plugins/dotnet-artisan/CLAUDE.md`**: Move current CLAUDE.md here. Update file paths in "File Structure" and "Validation Commands" sections.

**Root `CONTRIBUTING.md`**: Keep at root. Update to remove dist generation references. Point to plugin-specific CONTRIBUTING-SKILLS.md.

**`CHANGELOG.md`**: Add an [Unreleased] entry documenting the marketplace restructure (moved to plugins/, removed dist pipeline, per-plugin versioning). Historical 0.1.0 entries remain as-is for accuracy.

### Validation Scripts

Move `validate-skills.sh`, `_validate_skills.py`, `validate-marketplace.sh` into `plugins/dotnet-artisan/scripts/`. They use `$(dirname "$0")/..` for REPO_ROOT — after the move, this resolves to the plugin root, which is correct.

**No cross-ref extraction needed**: `_validate_skills.py` already validates `[skill:name]` cross-references (lines 130-131, 293-305).

**Validation split**: `validate-marketplace.sh` validates only per-plugin manifests (run from plugin dir). Root `marketplace.json` validation (JSON valid + source paths resolve) happens in the CI workflow (Task 3), not in this script.

### trigger-corpus.json

Moves with the plugin to `plugins/dotnet-artisan/tests/`. Its only consumer (`validate_cross_agent.py`) is deleted in Task 1. It remains as test data that could be consumed by future skill validation enhancements — not deleted, but noted as currently without an active consumer.

### What Does NOT Change

- Internal skill/agent/hook content (SKILL.md files, agent .md files, hook scripts)
- Plugin.json skill/agent path arrays (already relative to plugin root)
- Hook `${CLAUDE_PLUGIN_ROOT}` references
- `.mcp.json` content (context7 MCP servers)

## Key Context

- `anthropics/claude-plugins-official` is the canonical pattern: `plugins/{name}/.claude-plugin/plugin.json`
- Claude Code caches the plugin directory — all files must be self-contained within it
- `CLAUDE_PLUGIN_ROOT` is set at install time — resolves to the plugin cached location
- `validate-skills.sh` line 32: `REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)` — after move, this = plugin root
- `_validate_skills.py` line 233: `skills_dir = repo_root / "skills"` — works since skills/ is inside plugin root

## Acceptance
- [ ] `plugins/dotnet-artisan/` contains: skills/ (122), agents/ (14), hooks/, scripts/, tests/, docs/, .mcp.json
- [ ] Root `.claude-plugin/plugin.json` is DELETED (done in this task, not Task 1)
- [ ] Root `.claude-plugin/marketplace.json` lists dotnet-artisan with `"source": "./plugins/dotnet-artisan"` — schema verified against `anthropics/claude-plugins-official`
- [ ] `plugins/dotnet-artisan/.claude-plugin/plugin.json` present with unchanged internal paths
- [ ] `plugins/dotnet-artisan/.claude-plugin/marketplace.json` has per-plugin metadata
- [ ] Root README.md is marketplace-level; plugin README.md has skill catalog (agent count corrected to 14)
- [ ] Root CLAUDE.md is minimal marketplace instructions; plugin CLAUDE.md has plugin instructions
- [ ] `plugins/dotnet-artisan/AGENTS.md` has skill routing and agent delegation
- [ ] Plugin docs moved: `plugins/dotnet-artisan/docs/hooks-and-mcp-guide.md`, `plugins/dotnet-artisan/docs/dotnet-artisan-spec.md`
- [ ] Validation scripts work from plugin directory: `cd plugins/dotnet-artisan && ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- [ ] No root-level orphaned files from the plugin (skills/, agents/, hooks/, .mcp.json etc. removed from root)
- [ ] Empty `docs/` directory at root removed (if no files remain)
- [ ] CHANGELOG.md updated with [Unreleased] entry for marketplace restructure
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
