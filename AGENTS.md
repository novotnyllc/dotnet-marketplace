# dotnet-artisan -- Plugin Instructions

<!-- BEGIN FLOW-NEXT -->
## Flow-Next

This project uses Flow-Next for task tracking. Use `.flow/bin/flowctl` instead of markdown TODOs or TodoWrite.

**Quick commands:**
```bash
.flow/bin/flowctl list                # List all epics + tasks
.flow/bin/flowctl epics               # List all epics
.flow/bin/flowctl tasks --epic fn-N   # List tasks for epic
.flow/bin/flowctl ready --epic fn-N   # What's ready
.flow/bin/flowctl show fn-N.M         # View task
.flow/bin/flowctl start fn-N.M        # Claim task
.flow/bin/flowctl done fn-N.M --summary-file s.md --evidence-json e.json
```

**Rules:**
- Use `.flow/bin/flowctl` for ALL task tracking
- Do NOT create markdown TODOs or use TodoWrite
- Re-anchor (re-read spec + status) before every task

**More info:** `.flow/bin/flowctl --help` or read `.flow/usage.md`
<!-- END FLOW-NEXT -->


This directory contains **dotnet-artisan**, a Claude Code plugin providing 131 skills and 14 specialist agents for .NET development. It follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard.

## Key Conventions

### SKILL.md Frontmatter

Every skill requires `name` and `description` frontmatter fields. Additional optional fields control skill visibility and execution:

```yaml
---
name: dotnet-example-skill
description: One-line summary under 120 characters
user-invocable: false
---
```

**Required fields:**
- `name` (string) -- must match the directory name
- `description` (string) -- target under 120 characters to stay within the context budget (~12,000 chars for 131 skills)

**Optional fields:**
- `user-invocable` (boolean) -- set to `false` to hide from the `/` menu; default `true`
- `disable-model-invocation` (boolean) -- set to `true` to prevent Claude from loading the skill
- `context` (string) -- set to `fork` for isolated execution without conversation history
- `model` (string) -- model override, e.g. `haiku` for lightweight detection tasks

### Cross-Reference Syntax

Reference skills and agents using machine-parseable syntax:

```markdown
See [skill:dotnet-csharp-async-patterns] for async/await guidance.
Route to [skill:dotnet-security-reviewer] for security audit.
```

Use `[skill:name]` for ALL routable references (skills and agents) -- bare text names are not machine-parseable. The validator resolves references against the union of skill directory names and agent file stems.

### Routing Language Rules

Descriptions must follow the **Action + Domain + Differentiator** formula using third-person declarative style. No WHEN prefix, no filler phrases. Every skill must have `## Scope` and `## Out of scope` sections. See [docs/skill-routing-style-guide.md](docs/skill-routing-style-guide.md) for the full canonical rules.

### Description Budget

- Per-skill description: under 120 characters
- Total context budget: 15,600 characters (warning threshold at 12,000)

## File Structure

```
skills/<skill-name>/SKILL.md               # 131 skills (flat layout)
agents/<agent-name>.md                     # 14 specialist agents
hooks/hooks.json                           # Session hooks (start context, post-edit)
.mcp.json                                  # MCP server integrations
.claude-plugin/plugin.json                 # Plugin manifest
.claude-plugin/marketplace.json            # Marketplace metadata
scripts/                                   # Hook shell scripts
tests/                                     # Test data
docs/                                      # Plugin-specific documentation
```

Key directories:
- **`skills/`** -- All skill content in a flat layout (one directory per skill, no category subdirectories)
- **`agents/`** -- Specialist agent definitions with frontmatter, preloaded skills, and workflows
- **`hooks/`** -- Session lifecycle hooks
- **`scripts/`** -- Hook shell scripts
- **`.claude-plugin/`** -- Plugin manifest (plugin.json) and metadata (marketplace.json)

## Validation Commands

Both commands must pass before committing changes (run from repo root):

```bash
# 1. Validate skill frontmatter, required fields, directory conventions
./scripts/validate-skills.sh

# 2. Validate plugin.json and marketplace.json consistency
./scripts/validate-marketplace.sh
```

Run both in sequence:

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Development Workflow

1. **Edit skills** -- Modify or create `SKILL.md` files under `skills/<skill-name>/`
2. **Register in plugin.json** -- Add new skill paths to the `skills` array in `.claude-plugin/plugin.json`
3. **Validate locally** -- Run both validation commands above
4. **Commit** -- Use conventional commit messages with appropriate scope
5. **CI validates** -- The `validate.yml` workflow runs the same validation commands on push and PR

## References

- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and PR process
- See [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the comprehensive skill authoring how-to manual
- See [README.md](README.md) for the full skill catalog, architecture diagrams, and installation instructions

