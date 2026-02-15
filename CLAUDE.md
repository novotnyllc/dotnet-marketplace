# dotnet-artisan -- Plugin Instructions

This repository contains **dotnet-artisan**, a Claude Code plugin providing 101 skills across 19 categories and 9 specialist agents for .NET development. It follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard.

## Key Conventions

### SKILL.md Frontmatter

Every skill requires exactly two frontmatter fields:

```yaml
---
name: dotnet-example-skill
description: One-line summary under 120 characters
---
```

- `name` (required) -- must match the directory name
- `description` (required) -- target under 120 characters to stay within the context budget (~12,000 chars for 100 skills)

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
skills/<category>/<skill-name>/SKILL.md   # 101 skills across 19 categories
agents/<agent-name>.md                     # 9 specialist agents
hooks/hooks.json                           # Session hooks (start context, post-edit)
.mcp.json                                  # MCP server integrations
.claude-plugin/plugin.json                 # Plugin manifest
scripts/                                   # Validation and build scripts
dist/                                      # Generated cross-agent outputs (not checked in)
```

Key directories:
- **`skills/`** -- All skill content organized by category (foundation, core-csharp, architecture, testing, etc.)
- **`agents/`** -- Specialist agent definitions with frontmatter, preloaded skills, and workflows
- **`hooks/`** -- Session lifecycle hooks
- **`scripts/`** -- Validation scripts and cross-agent distribution generator
- **`.claude-plugin/`** -- Plugin metadata (plugin.json, marketplace.json)
- **`dist/`** -- Generated output for Claude, Copilot, and Codex (produced by `generate_dist.py`)

## Validation Commands

All four commands must pass before committing changes:

```bash
# 1. Validate skill frontmatter, required fields, directory conventions
./scripts/validate-skills.sh

# 2. Validate plugin.json and marketplace.json consistency
./scripts/validate-marketplace.sh

# 3. Generate cross-agent distribution and validate cross-references
python3 scripts/generate_dist.py --strict

# 4. Validate generated outputs conform to target platform requirements
python3 scripts/validate_cross_agent.py
```

Run all four in sequence:

```bash
./scripts/validate-skills.sh && \
./scripts/validate-marketplace.sh && \
python3 scripts/generate_dist.py --strict && \
python3 scripts/validate_cross_agent.py
```

## Development Workflow

1. **Edit skills** -- Modify or create `SKILL.md` files under `skills/<category>/<skill-name>/`
2. **Register in plugin.json** -- Add new skill paths to the `skills` array in `.claude-plugin/plugin.json`
3. **Validate locally** -- Run all four validation commands above
4. **Commit** -- Use conventional commit messages with appropriate scope
5. **CI validates** -- The `validate.yml` workflow runs the same validation commands on push and PR

## References

- See [AGENTS.md](AGENTS.md) for skill routing index and agent delegation patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, PR process, and skill authoring quick reference
- See [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the comprehensive skill authoring how-to manual
- See [README.md](README.md) for the full skill catalog, architecture diagrams, and installation instructions
