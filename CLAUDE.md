# dotnet-marketplace -- Marketplace Instructions

This repository is a Claude Code plugin marketplace hosting .NET development plugins. It follows the [marketplace pattern](https://github.com/anthropics/claude-plugins-official) with plugins in `plugins/<name>/`.

For skill routing, discovery, and agent delegation, see [AGENTS.md](AGENTS.md).

## Repository Layout

- **`plugins/dotnet-artisan/`** -- The dotnet-artisan plugin (130 skills, 14 agents). See [plugins/dotnet-artisan/CLAUDE.md](plugins/dotnet-artisan/CLAUDE.md) for plugin-specific instructions.
- **`.claude-plugin/marketplace.json`** -- Root marketplace listing (lists available plugins)
- **`.agents/openai.yaml`** -- Codex discovery metadata (for `$skill-installer`)
- **`.github/workflows/`** -- CI/CD workflows
- **`scripts/`** -- Validation scripts and dev tooling (repo-level)
- **`.flow/`** -- Task planning (repo-level)

## Validation

### SKILL.md Frontmatter

```yaml
---
name: dotnet-example-skill
description: One-line summary under 120 characters
user-invocable: false
---
```

**Required fields:**
- `name` (string) -- must match the directory name
- `description` (string) -- target under 120 characters to stay within the context budget (~12,000 chars for 130 skills)

**Optional fields ([frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)):**
- `user-invocable` (boolean) -- set to `false` to hide from the `/` menu; default `true`
- `disable-model-invocation` (boolean) -- set to `true` to prevent Claude from loading the skill
- `context` (string) -- set to `fork` for isolated execution without conversation history
- `model` (string) -- model override, e.g. `haiku` for lightweight detection tasks

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
plugins/dotnet-artisan/                    # Plugin directory
  skills/<category>/<skill-name>/SKILL.md  # 130 skills across 22 categories
  agents/<agent-name>.md                   # 14 specialist agents
  hooks/hooks.json                         # Session hooks (start context, post-edit)
  .mcp.json                                # MCP server integrations
  .claude-plugin/plugin.json               # Plugin manifest (version source of truth)
.claude-plugin/marketplace.json            # Root marketplace discovery (lists available plugins)
.agents/openai.yaml                        # Codex discovery metadata
scripts/validate-skills.sh                 # Skill frontmatter and budget validation
scripts/validate-marketplace.sh            # Plugin.json and marketplace.json validation
scripts/validate-root-marketplace.sh       # Root marketplace.json shared validation (used by CI)
scripts/bump.sh                            # Version bump and propagation script
```

### Marketplace Schema

Root `.claude-plugin/marketplace.json` fields: `$schema`, `name`, `description`, `owner` (object with `name`, `url`), `metadata` (object with `description`, `version`), `plugins` (array with per-plugin `name`, `source`, `description`, `version`, `author`, `license`, `category`, `homepage`, `keywords`).

### Plugin Schema

`plugins/dotnet-artisan/.claude-plugin/plugin.json` fields: `name`, `version` (canonical source of truth), `description`, `author` (object with `name`, `url`), `homepage`, `repository`, `license`, `keywords`, `skills` (array of dir paths), `agents` (array of file paths), `hooks` (string path), `mcpServers` (string path).

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
5. **CI validates** -- The `validate.yml` workflow runs the same validation commands plus `scripts/validate-root-marketplace.sh` and a 3-way version consistency check on push and PR

## References

- See [AGENTS.md](AGENTS.md) for skill routing index and agent delegation patterns
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, PR process, and skill authoring quick reference
- See [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the comprehensive skill authoring how-to manual
- See [README.md](README.md) for the full skill catalog, architecture diagrams, and installation instructions

---

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
