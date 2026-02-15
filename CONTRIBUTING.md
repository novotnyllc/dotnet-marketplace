# Contributing to dotnet-artisan

Welcome to **dotnet-artisan**, a Claude Code plugin for .NET development. This plugin follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard for skill authoring and discovery.

Contributions are welcome across all areas: new skills, skill improvements, agent refinements, documentation, and tooling.

## Prerequisites

You need the following to contribute:

- **Python 3** -- Required for validation scripts (`generate_dist.py`, `validate_cross_agent.py`)
- **jq** -- Required for marketplace validation (`validate-marketplace.sh`)
- **Git** -- Standard version control

No .NET SDK is required for the plugin repo itself. The plugin provides guidance content (Markdown-based skills), not compiled code.

## Skill Authoring Guide

> **Comprehensive guide available:** For the full skill authoring how-to manual -- including quick start, writing effective descriptions, testing, common patterns, and troubleshooting -- see [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md).

The section below provides a quick reference. Skills are the primary content unit. Each skill is a `SKILL.md` file with structured frontmatter and rich guidance content.

### Directory Convention

All skills follow this directory structure:

```
skills/<category>/<skill-name>/SKILL.md
```

For example: `skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md`

### SKILL.md Frontmatter

Every skill requires frontmatter with exactly two required fields:

```yaml
---
name: dotnet-csharp-async-patterns
description: Async/await patterns, cancellation, and parallel execution in modern C#
---
```

- **`name`** (required) -- Unique skill identifier, must match the directory name
- **`description`** (required) -- One-line summary; target under 120 characters

The description budget of 120 characters per skill keeps the aggregate catalog within the context window budget (~12,000 characters for 100 skills).

### Cross-Reference Syntax

Reference other skills using the cross-reference syntax:

```markdown
See [skill:dotnet-csharp-async-patterns] for async/await guidance.
```

This syntax enables machine-parseable skill references. The cross-agent build pipeline resolves these to platform-appropriate links or inline text.

### Content Guidelines

- Use real .NET code examples, not pseudocode
- Include Mermaid diagrams for architectural concepts where appropriate
- Use YAML and Markdown formatting consistent with existing skills
- Add an **Agent Gotchas** section for common AI agent mistakes
- Mark scope boundaries clearly: use an "**Out of scope:**" paragraph with epic ownership attribution when a topic is covered by another skill

### Skill Description Budget

The total context budget for all skill descriptions is 15,000 characters (with a warning threshold at 12,000). Each individual skill description should target under 120 characters. This ensures the full skill catalog fits within the context window when Claude Code loads the plugin.

## Agent Authoring

Agents are specialist personas that combine multiple skills with domain expertise. To contribute an agent:

### Agent File Structure

Place agent files at:

```
agents/<agent-name>.md
```

### Agent Frontmatter

```yaml
---
name: dotnet-example-specialist
description: Brief description of the agent's domain expertise
capabilities:
  - capability-one
  - capability-two
tools:
  - Read
  - Grep
  - Glob
---
```

Required frontmatter fields: `name`, `description`, `capabilities`, and `tools`.

### Agent Content

- Define preloaded skills (including foundation skills like `dotnet-version-detection` and `dotnet-project-analysis`)
- Specify a workflow with numbered steps
- Include trigger lexicon for routing from `dotnet-advisor`
- Keep agent toolsets aligned with workflow steps (do not reference tools not declared in frontmatter)

## PR Process

1. **Fork** the repository
2. **Branch** from `main` with a descriptive branch name
3. **Implement** your changes following the conventions above
4. **Validate locally** -- Run all validation commands (see below)
5. **Submit PR** with a clear description of changes

## Validation Requirements

All four validation commands must pass before a PR can be merged:

### 1. Skill Validation

```bash
./scripts/validate-skills.sh
```

Validates skill frontmatter structure, required fields (`name`, `description`), and directory conventions.

### 2. Marketplace Validation

```bash
./scripts/validate-marketplace.sh
```

Validates `plugin.json` and `marketplace.json` consistency, skill registration, and agent registration.

### 3. Cross-Agent Distribution

```bash
python3 scripts/generate_dist.py --strict
```

Generates platform-specific outputs in `dist/` (Claude, Copilot, Codex) and validates cross-references are resolvable.

### 4. Cross-Agent Conformance

```bash
python3 scripts/validate_cross_agent.py
```

Validates that generated distribution outputs conform to each target platform's requirements, including manifest schema and SHA256 checksum correctness.

Run all four before submitting:

```bash
./scripts/validate-skills.sh && \
./scripts/validate-marketplace.sh && \
python3 scripts/generate_dist.py --strict && \
python3 scripts/validate_cross_agent.py
```

### Release and Deployment

On tag push (`v*`), the `release.yml` workflow validates the plugin, generates cross-agent outputs, deploys `dist/` to GitHub Pages, and creates a GitHub Release for changelog notes. The deployed content is available at `https://novotnyllc.github.io/dotnet-marketplace/` with a `manifest.json` at the root for auto-update polling.

See the [Cross-Agent Support](README.md#cross-agent-support) section of the README for Pages URLs, polling contract, and one-time repository setup instructions.

## Hooks and MCP Contributions

The plugin includes session hooks (session start context, post-edit validation) and MCP server integrations (Context7, Uno Platform, Microsoft Learn).

For guidance on contributing to hooks or MCP integrations, see [docs/hooks-and-mcp-guide.md](docs/hooks-and-mcp-guide.md).

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Contributors are expected to:

- Be respectful and constructive in discussions and code reviews
- Focus on technical merit and improving the plugin
- Welcome newcomers and help them get started

Thank you for contributing to dotnet-artisan.
