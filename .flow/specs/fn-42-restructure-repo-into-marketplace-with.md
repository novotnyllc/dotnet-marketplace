# fn-42 Restructure Repo into Marketplace with Plugin Subdirectories

## Overview

Restructure `novotnyllc/dotnet-marketplace` from a flat single-plugin repo into a **marketplace** that hosts plugins in subdirectories, following the `anthropics/claude-plugins-official` pattern. Move the entire dotnet-artisan plugin into `plugins/dotnet-artisan/`. Clean up stale artifacts from completed epics. Remove the dist generation pipeline entirely — source files ARE the plugin.

Users install via:
```
/plugin marketplace add novotnyllc/dotnet-marketplace
/plugin install dotnet-artisan
```

## Scope

**In Scope:**
- Delete stale files: fleet review docs, review reports, ralph run logs, dist/ pipeline (generate_dist.py, validate_cross_agent.py), dist/ output
- Move all dotnet-artisan content to `plugins/dotnet-artisan/` with its own `.claude-plugin/plugin.json`
- Delete root `.claude-plugin/plugin.json` atomically during the restructure (Task 2), not before
- Move plugin-specific docs (`docs/hooks-and-mcp-guide.md`, `docs/dotnet-artisan-spec.md`) into plugin
- Create root `.claude-plugin/marketplace.json` listing available plugins
- Per-plugin versioning (tag format: `dotnet-artisan/v*`)
- Update CI workflows for new structure (remove dist steps, per-plugin paths)
- Add `.agents/openai.yaml` at repo root for Codex skill discovery
- Add root marketplace.json validation to CI
- Update CHANGELOG.md with marketplace restructure entry

**Out of Scope:**
- Copilot/Codex platform-specific output generation (future epic)
- Adding additional plugins to the marketplace
- MCP registry or Copilot plugin marketplace registration
- Modifying any skill/agent content (purely structural, except fixing the README agent count from 9 to 14 during the move)

## Target Structure

```
/
├── .claude-plugin/
│   └── marketplace.json              # Root: lists available plugins
├── plugins/
│   └── dotnet-artisan/
│       ├── .claude-plugin/
│       │   ├── plugin.json           # Per-plugin manifest (122 skills, 14 agents)
│       │   └── marketplace.json      # Per-plugin metadata (author, keywords, etc.)
│       ├── skills/                   # 122 skills (22 categories, unchanged internally)
│       ├── agents/                   # 14 specialist agents
│       ├── hooks/
│       │   └── hooks.json            # Session hooks (uses ${CLAUDE_PLUGIN_ROOT})
│       ├── scripts/
│       │   ├── hooks/                # Hook shell scripts
│       │   ├── validate-skills.sh
│       │   ├── _validate_skills.py
│       │   └── validate-marketplace.sh
│       ├── tests/                    # Test suite (trigger-corpus.json, etc.)
│       ├── docs/                     # Plugin-specific docs
│       │   ├── hooks-and-mcp-guide.md
│       │   └── dotnet-artisan-spec.md
│       ├── .mcp.json                 # MCP server config
│       ├── AGENTS.md                 # Skill routing + agent delegation
│       ├── CLAUDE.md                 # Plugin instructions
│       └── CONTRIBUTING-SKILLS.md    # Skill authoring guide
├── .agents/
│   └── openai.yaml                   # Codex skill discovery metadata
├── .github/
│   └── workflows/                    # CI (validate.yml, release.yml)
├── .flow/                            # Planning (stays at root)
├── scripts/
│   └── ralph/                        # Dev tooling (stays at root, minus runs/)
├── README.md                         # Marketplace-level overview
├── CONTRIBUTING.md                   # Marketplace-level contribution guide
├── CHANGELOG.md
└── LICENSE
```

## Design Decisions

1. **Marketplace pattern**: Follow `anthropics/claude-plugins-official` — root `marketplace.json` with `"source": "./plugins/dotnet-artisan"`, each plugin has own `.claude-plugin/plugin.json`. Verify the exact marketplace.json schema from that repo before authoring; do not invent fields.

2. **No dist pipeline**: Source files ARE the final output. Claude Code reads directly from the plugin directory. No generation, no transformation, no build step for developers.

3. **Hooks use `${CLAUDE_PLUGIN_ROOT}`**: Already platform-relative. When installed, `CLAUDE_PLUGIN_ROOT` resolves to the plugin's cached location. No path changes needed inside hooks.json or hook scripts.

4. **Per-plugin versioning**: Version in `plugins/dotnet-artisan/.claude-plugin/plugin.json`. Tag format: `dotnet-artisan/v0.1.0`. Release workflow scoped to plugin-prefixed tags.

5. **Skill paths unchanged inside plugin**: All paths in plugin.json are relative to the plugin root. Moving the plugin to a subdirectory doesn't change any internal references — `skills/foundation/dotnet-advisor` stays the same.

6. **Root plugin.json deleted atomically**: The old root `.claude-plugin/plugin.json` is deleted in Task 2 (the restructure task) at the same time the replacement marketplace.json and per-plugin plugin.json are created. This prevents any window where the repo has no discoverable manifest.

7. **Dev tooling stays at root**: `scripts/ralph/` (minus `runs/`) stays at repo root since it's repo-level dev tooling, not plugin content. `.flow/` stays at root.

8. **Feature branch workflow**: All tasks happen on a feature branch. Intermediate CI breakage is acceptable — only the final PR merge must pass.

9. **Validation split**: `validate-marketplace.sh` validates only per-plugin manifests (run from plugin dir). Root `marketplace.json` validation (JSON valid + source paths resolve) happens in the CI workflow directly.

10. **trigger-corpus.json**: Moves with the plugin to `plugins/dotnet-artisan/tests/`. Its only consumer (`validate_cross_agent.py`) is deleted. It remains as test data that could be used by future skill validation — not deleted, but noted as currently without an active consumer.

## Quick commands

```bash
# From plugin directory
cd plugins/dotnet-artisan
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
# Root marketplace validation (in CI)
jq empty .claude-plugin/marketplace.json
```

## Acceptance

- [ ] `plugins/dotnet-artisan/` contains the complete plugin (122 skills, 14 agents, hooks, scripts, .mcp.json)
- [ ] Root `.claude-plugin/marketplace.json` lists dotnet-artisan with `"source": "./plugins/dotnet-artisan"` — schema verified against `anthropics/claude-plugins-official`
- [ ] Root `.claude-plugin/plugin.json` is DELETED (no ambiguous discovery)
- [ ] `plugins/dotnet-artisan/.claude-plugin/plugin.json` has all skill/agent/hook/mcp paths (relative to plugin root, unchanged)
- [ ] `plugins/dotnet-artisan/.claude-plugin/marketplace.json` has plugin metadata (author, keywords, categories)
- [ ] Per-plugin version in plugin manifest; release workflow uses `dotnet-artisan/v*` tag pattern
- [ ] Stale files deleted: `docs/fleet-review-rubric.md`, `docs/review-reports/`, `scripts/ralph/runs/`, `dist/`, `scripts/generate_dist.py`, `scripts/validate_cross_agent.py`
- [ ] `.gitignore` updated (no `dist/` entry; no new entries needed — existing root patterns cover build artifacts globally)
- [ ] CI `validate.yml` validates root marketplace.json AND runs plugin validation from subdirectory, no dist steps
- [ ] CI `release.yml` uses per-plugin tags, no Pages deployment
- [ ] `.agents/openai.yaml` exists at repo root with valid, parseable YAML
- [ ] Hooks work correctly with `${CLAUDE_PLUGIN_ROOT}` from the subdirectory location
- [ ] Plugin-specific docs moved: `docs/hooks-and-mcp-guide.md`, `docs/dotnet-artisan-spec.md` → `plugins/dotnet-artisan/docs/`
- [ ] CHANGELOG.md updated with [Unreleased] entry documenting the marketplace restructure

## References

- `anthropics/claude-plugins-official` marketplace pattern: root `marketplace.json` → `./plugins/<name>/`
- `trailofbits/skills-curated` uses same `plugins/` + per-plugin `.claude-plugin/` pattern
- Codex openai.yaml schema: `.agents/openai.yaml` at repo root
- Agent Skills spec: https://agentskills.io/specification
