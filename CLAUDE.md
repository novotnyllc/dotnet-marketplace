# dotnet-marketplace -- Marketplace Instructions

This repository is a Claude Code plugin marketplace hosting .NET development plugins. It follows the [marketplace pattern](https://github.com/anthropics/claude-plugins-official) with plugins in `plugins/<name>/`.

## Repository Layout

- **`plugins/dotnet-artisan/`** -- The dotnet-artisan plugin (127 skills, 14 agents). See [plugins/dotnet-artisan/CLAUDE.md](plugins/dotnet-artisan/CLAUDE.md) for plugin-specific instructions.
- **`.claude-plugin/marketplace.json`** -- Root marketplace listing (lists available plugins)
- **`.github/workflows/`** -- CI/CD workflows
- **`scripts/`** -- Validation scripts and dev tooling (repo-level)
- **`.flow/`** -- Task planning (repo-level)

## Validation

```yaml
---
name: dotnet-example-skill
description: One-line summary under 120 characters
---
```

- `name` (required) -- must match the directory name
- `description` (required) -- target under 120 characters to stay within the context budget (~12,000 chars for 127 skills)

### Cross-Reference Syntax

Reference other skills using machine-parseable syntax:

```markdown
See [skill:dotnet-csharp-async-patterns] for async/await guidance.
```

Use `[skill:skill-name]` for ALL skill references -- bare text skill names are not machine-parseable.

### Description Budget

- Per-skill description: under 120 characters
- Total context budget: 15,000 characters (warning threshold at 12,000)

## File Structure

```
skills/<category>/<skill-name>/SKILL.md   # 127 skills across 22 categories
agents/<agent-name>.md                     # 14 specialist agents
hooks/hooks.json                           # Session hooks (start context, post-edit)
.mcp.json                                  # MCP server integrations
.claude-plugin/plugin.json                 # Plugin manifest
.claude-plugin/marketplace.json            # Marketplace discovery (lists available plugins)
.agents/openai.yaml                        # Codex discovery metadata
scripts/                                   # Validation scripts
```

Key directories:
- **`skills/`** -- All skill content organized by category (foundation, core-csharp, architecture, testing, etc.)
- **`agents/`** -- Specialist agent definitions with frontmatter, preloaded skills, and workflows
- **`hooks/`** -- Session lifecycle hooks
- **`scripts/`** -- Validation scripts
- **`.claude-plugin/`** -- Plugin manifest and marketplace metadata

## Validation Commands

Both commands must pass before committing changes (run from repo root):

```bash
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
```

Run both in sequence:

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Contributing

1. **Edit skills** -- Modify or create `SKILL.md` files under `skills/<category>/<skill-name>/`
2. **Register in plugin.json** -- Add new skill paths to the `skills` array in `.claude-plugin/plugin.json`
3. **Validate locally** -- Run both validation commands above
4. **Commit** -- Use conventional commit messages with appropriate scope
5. **CI validates** -- The `validate.yml` workflow runs the same validation commands plus root marketplace.json validation on push and PR

## References

- See [AGENTS.md](AGENTS.md) for skill routing index and agent delegation patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, PR process, and skill authoring quick reference
- See [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the comprehensive skill authoring how-to manual
- See [README.md](README.md) for the full skill catalog, architecture diagrams, and installation instructions
