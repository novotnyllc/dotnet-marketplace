# fn-42-restructure-repo-into-marketplace-with.2 Restructure into marketplace with plugin subdirectory

## Description
Move all dotnet-artisan plugin content into `plugins/dotnet-artisan/`. Create the root marketplace structure. Update all documentation and validation scripts.

**Size:** M
**Files:** Entire repo structure, `.claude-plugin/marketplace.json` (root), `plugins/dotnet-artisan/.claude-plugin/plugin.json`, `plugins/dotnet-artisan/.claude-plugin/marketplace.json`, `README.md`, `CLAUDE.md`, `AGENTS.md`, validation scripts

## Approach

### File Moves (git mv for history preservation)

Move INTO `plugins/dotnet-artisan/`:
- `skills/` (all 22 categories, 121 skills)
- `agents/` (14 specialist agents)
- `hooks/` (hooks.json)
- `scripts/hooks/` (post-edit-dotnet.sh, session-start-context.sh)
- `scripts/validate-skills.sh`, `scripts/_validate_skills.py`, `scripts/validate-marketplace.sh`
- `.mcp.json`
- `tests/`
- `AGENTS.md` (skill routing + agent delegation)
- `CONTRIBUTING-SKILLS.md`

### Manifest Changes

**Root `.claude-plugin/marketplace.json`** (NEW — marketplace listing):
```json
{
  "name": "novotnyllc-dotnet-marketplace",
  "description": "Marketplace for .NET development plugins",
  "author": {
    "name": "Claire Novotny LLC",
    "url": "https://github.com/novotnyllc"
  },
  "repository": "https://github.com/novotnyllc/dotnet-marketplace",
  "license": "MIT",
  "metadata": {
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "dotnet-artisan",
      "source": "./plugins/dotnet-artisan",
      "description": "Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications"
    }
  ]
}
```

**`plugins/dotnet-artisan/.claude-plugin/plugin.json`** (MOVED — paths unchanged):
All skill, agent, hook, and MCP paths are relative to the plugin root. Since the internal structure stays the same, NO path changes are needed. The `hooks` field references `hooks/hooks.json`, which in turn uses `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/...` — all self-relative.

**`plugins/dotnet-artisan/.claude-plugin/marketplace.json`** (MOVED — per-plugin metadata):
The existing marketplace.json (author, keywords, categories) moves here. This becomes the per-plugin metadata.

### Documentation Splits

**Root `README.md`**: Marketplace overview — what plugins are available, how to install (`/plugin marketplace add novotnyllc/dotnet-marketplace`), link to each plugin's README.

**`plugins/dotnet-artisan/README.md`**: Move current root README.md content here (skill catalog, architecture, installation).

**Root `CLAUDE.md`**: Minimal — marketplace-level instructions, point to plugin subdirectories.

**`plugins/dotnet-artisan/CLAUDE.md`**: Move current CLAUDE.md here. Update file paths in the "File Structure" and "Validation Commands" sections to reflect the new location.

**Root `CONTRIBUTING.md`**: Keep at root, update references.

### Validation Scripts

Move `validate-skills.sh`, `_validate_skills.py`, `validate-marketplace.sh` into `plugins/dotnet-artisan/scripts/`. They already work relative to the plugin directory structure. Update any hardcoded paths.

**Cross-ref validation**: Extract `[skill:name]` cross-reference validation from the deleted `generate_dist.py` and add it to `_validate_skills.py`. This check verifies that every `[skill:name]` reference points to an actual skill directory.

### What Does NOT Change

- Internal skill/agent/hook content (SKILL.md files, agent .md files, hook scripts)
- Plugin.json skill/agent path arrays (already relative to plugin root)
- Hook `${CLAUDE_PLUGIN_ROOT}` references
- `.mcp.json` content (context7 MCP servers)

## Key Context

- `anthropics/claude-code` is the reference pattern: root marketplace.json with `"source": "./plugins/<name>/"`
- Claude Code caches the plugin directory — all files must be self-contained within it
- `npx skills add novotnyllc/dotnet-marketplace/plugins/dotnet-artisan` supports subdirectory paths
- Git mv preserves file history for blame/log
- CLAUDE_PLUGIN_ROOT is set by Claude Code at install time — always resolves to the plugin's cached location

## Acceptance
- [ ] `plugins/dotnet-artisan/` contains: skills/ (121), agents/ (14), hooks/, scripts/, tests/, .mcp.json
- [ ] Root `.claude-plugin/marketplace.json` lists dotnet-artisan with correct source path
- [ ] `plugins/dotnet-artisan/.claude-plugin/plugin.json` present with unchanged internal paths
- [ ] `plugins/dotnet-artisan/.claude-plugin/marketplace.json` has per-plugin metadata
- [ ] Root README.md is marketplace-level; plugin README.md has skill catalog
- [ ] Root CLAUDE.md is minimal; plugin CLAUDE.md has plugin instructions
- [ ] `plugins/dotnet-artisan/AGENTS.md` has skill routing and agent delegation
- [ ] Validation scripts work from plugin directory: `cd plugins/dotnet-artisan && ./scripts/validate-skills.sh`
- [ ] `[skill:name]` cross-ref validation added to _validate_skills.py
- [ ] Validation passes: `cd plugins/dotnet-artisan && ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh`
- [ ] No root-level orphaned files from the plugin (skills/, agents/, hooks/ etc. removed from root)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
