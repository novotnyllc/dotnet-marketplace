# fn-42 Restructure Repo into Marketplace with Plugin Subdirectories

## Overview

Restructure `novotnyllc/dotnet-marketplace` from a flat single-plugin repo into a **marketplace** that hosts plugins in subdirectories, following the `anthropics/claude-code` pattern. Move the entire dotnet-artisan plugin into `plugins/dotnet-artisan/`. Clean up stale artifacts from completed epics. Remove the dist generation pipeline entirely — source files ARE the plugin.

Users install via:
```
/plugin marketplace add novotnyllc/dotnet-marketplace
/plugin install dotnet-artisan
```

Skills are also available individually:
```
npx skills add novotnyllc/dotnet-marketplace/plugins/dotnet-artisan
```

## Scope

**In Scope:**
- Delete stale files: fleet review docs, review reports, ralph run logs, dist/ pipeline (generate_dist.py, validate_cross_agent.py)
- Move all dotnet-artisan content to `plugins/dotnet-artisan/` with its own `.claude-plugin/plugin.json`
- Create root `.claude-plugin/marketplace.json` listing available plugins
- Per-plugin versioning (tag format: `dotnet-artisan/v*`)
- Update CI workflows for new structure (remove dist steps, per-plugin paths)
- Add `.agents/openai.yaml` at repo root for Codex skill discovery
- Extract cross-ref validation from removed generate_dist.py into validate-skills.sh

**Out of Scope:**
- Copilot/Codex platform-specific output generation (future epic)
- Adding additional plugins to the marketplace
- MCP registry or Copilot plugin marketplace registration

## Target Structure

```
/
├── .claude-plugin/
│   └── marketplace.json              # Root: lists available plugins
├── plugins/
│   └── dotnet-artisan/
│       ├── .claude-plugin/
│       │   ├── plugin.json           # Per-plugin manifest (121 skills, 14 agents)
│       │   └── marketplace.json      # Per-plugin metadata (author, keywords, etc.)
│       ├── skills/                   # 121 skills (22 categories, unchanged internally)
│       ├── agents/                   # 14 specialist agents
│       ├── hooks/
│       │   └── hooks.json            # Session hooks (uses ${CLAUDE_PLUGIN_ROOT})
│       ├── scripts/
│       │   ├── hooks/                # Hook shell scripts
│       │   ├── validate-skills.sh    # Skill validation
│       │   ├── _validate_skills.py   # Skill validation (Python)
│       │   └── validate-marketplace.sh
│       ├── tests/                    # Test suite
│       ├── .mcp.json                 # MCP server config
│       ├── AGENTS.md                 # Skill routing + agent delegation
│       ├── CLAUDE.md                 # Plugin instructions
│       └── CONTRIBUTING-SKILLS.md    # Skill authoring guide
├── .agents/
│   └── openai.yaml                   # Codex skill discovery metadata
├── .github/
│   └── workflows/                    # CI (validate.yml, release.yml)
├── .flow/                            # Planning (stays at root)
├── README.md                         # Marketplace-level overview
├── CONTRIBUTING.md                   # Marketplace-level contribution guide
├── CHANGELOG.md
└── LICENSE
```

## Design Decisions

1. **Marketplace pattern**: Follow `anthropics/claude-code` — root `marketplace.json` with `"source": "./plugins/dotnet-artisan"`, each plugin has own `.claude-plugin/plugin.json`. This is the officially supported multi-plugin pattern.

2. **No dist pipeline**: Source files ARE the final output. Claude Code reads directly from the plugin directory. No generation, no transformation, no build step for developers.

3. **Hooks use `${CLAUDE_PLUGIN_ROOT}`**: Already platform-relative. When installed, `CLAUDE_PLUGIN_ROOT` resolves to the plugin's cached location. No path changes needed inside hooks.json or hook scripts.

4. **Per-plugin versioning**: Version in `plugins/dotnet-artisan/.claude-plugin/plugin.json`. Tag format: `dotnet-artisan/v0.1.0`. Release workflow scoped to plugin-prefixed tags.

5. **Skill paths unchanged inside plugin**: All paths in plugin.json are relative to the plugin root. Moving the plugin to a subdirectory doesn't change any internal references — `skills/foundation/dotnet-advisor` stays the same.

6. **Cross-ref validation preserved**: The `[skill:name]` cross-reference validation that was embedded in generate_dist.py is extracted into validate-skills.sh (or _validate_skills.py). No validation coverage is lost.

7. **openai.yaml at repo root**: `.agents/openai.yaml` stays at the repo root for Codex skill discovery. Minimal metadata file — interface (display name, description) and policy fields.

## Quick commands

```bash
# From plugin directory
cd plugins/dotnet-artisan
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] `plugins/dotnet-artisan/` contains the complete plugin (121 skills, 14 agents, hooks, scripts, .mcp.json)
- [ ] Root `.claude-plugin/marketplace.json` lists dotnet-artisan with `"source": "./plugins/dotnet-artisan"`
- [ ] `plugins/dotnet-artisan/.claude-plugin/plugin.json` has all skill/agent/hook/mcp paths (relative to plugin root, unchanged)
- [ ] `plugins/dotnet-artisan/.claude-plugin/marketplace.json` has plugin metadata (author, keywords, categories)
- [ ] Per-plugin version in plugin manifest; release workflow uses `dotnet-artisan/v*` tag pattern
- [ ] Stale files deleted: `docs/fleet-review-rubric.md`, `docs/review-reports/`, `scripts/ralph/runs/`, `dist/`, `scripts/generate_dist.py`, `scripts/validate_cross_agent.py`
- [ ] `.gitignore` updated (no `dist/` entry)
- [ ] CI `validate.yml` runs validation from plugin subdirectory, no dist steps
- [ ] CI `release.yml` uses per-plugin tags, no Pages deployment of dist
- [ ] `[skill:name]` cross-ref validation preserved in validate-skills.sh
- [ ] `.agents/openai.yaml` exists at repo root with valid Codex metadata
- [ ] Hooks work correctly with `${CLAUDE_PLUGIN_ROOT}` from the subdirectory location
- [ ] `npx skills add novotnyllc/dotnet-marketplace/plugins/dotnet-artisan` discovers all 121 skills

## References

- `anthropics/claude-code` marketplace pattern: root `marketplace.json` → `./plugins/<name>/`
- Claude Code plugin docs: `.claude-plugin/marketplace.json` schema with `metadata.pluginRoot`
- `vercel-labs/skills` subdirectory support: `owner/repo/path` in `npx skills add`
- Codex openai.yaml schema: https://developers.openai.com/codex/skills/
