# Contributing to dotnet-artisan

Welcome to **dotnet-artisan**, a Claude Code plugin for .NET development. It follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard for skill authoring and discovery.

Contributions are welcome across all areas: new skills, skill improvements, agent refinements, documentation, and tooling.

## Prerequisites

You need the following to contribute:

- **jq** -- Required for marketplace validation (`validate-marketplace.sh`)
- **Git** -- Standard version control

No .NET SDK is required for the plugin repo itself. The plugin provides guidance content (Markdown-based skills), not compiled code.

## Skill Authoring Guide

> **Comprehensive guide available:** For the full skill authoring how-to manual -- including quick start, writing effective descriptions, testing, common patterns, and troubleshooting -- see [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md).

The section below provides a quick reference. Skills are the primary content unit. Each skill is a `SKILL.md` file with structured frontmatter and rich guidance content.

### Directory Convention

All skills follow this directory structure within the plugin:

```
skills/<category>/<skill-name>/SKILL.md
```

For example: `skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md`

### SKILL.md Frontmatter

Every skill requires `name` and `description` frontmatter fields. Additional optional fields control skill visibility and execution:

```yaml
---
name: dotnet-csharp-async-patterns
description: Async/await patterns, cancellation, and parallel execution in modern C#
user-invocable: false
---
```

**Required fields:**
- **`name`** (string) -- Unique skill identifier, must match the directory name
- **`description`** (string) -- One-line summary; target under 120 characters

**Optional fields:**
- **`user-invocable`** (boolean) -- Set to `false` to hide from the `/` menu; default `true`
- **`disable-model-invocation`** (boolean) -- Set to `true` to prevent Claude from loading the skill
- **`context`** (string) -- Set to `fork` for isolated execution without conversation history
- **`model`** (string) -- Model override, e.g. `haiku` for lightweight detection tasks

See the [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the full field reference table.

The description budget of 120 characters per skill keeps the aggregate catalog within the context window budget (~12,000 characters for 130 skills).

### Cross-Reference Syntax

Reference other skills and agents using the unified cross-reference syntax:

```markdown
See [skill:dotnet-csharp-async-patterns] for async/await guidance.
Route to [skill:dotnet-security-reviewer] for security audit.
```

Use `[skill:name]` for ALL routable references (skills and agents) -- bare text names are not machine-parseable.

### Routing Language Rules

Descriptions must follow the **Action + Domain + Differentiator** formula using third-person declarative style. No WHEN prefix, no filler phrases. Every skill must have `## Scope` and `## Out of scope` sections with attributed cross-references. See [docs/skill-routing-style-guide.md](docs/skill-routing-style-guide.md) and [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for full details.

### Content Guidelines

- Use real .NET code examples, not pseudocode
- Include Mermaid diagrams for architectural concepts where appropriate
- Use YAML and Markdown formatting consistent with existing skills
- Add an **Agent Gotchas** section for common AI agent mistakes
- Mark scope boundaries with `## Scope` and `## Out of scope` headings, and include `[skill:]` attribution in out-of-scope bullets

### Skill Description Budget

The total context budget for all skill descriptions is 15,600 characters (with a warning threshold at 12,000). Each individual skill description should target under 120 characters. This ensures the full skill catalog fits within the context window when Claude Code loads the plugin.

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

Both validation commands must pass before a PR can be merged:

### 1. Skill Validation

```bash
./scripts/validate-skills.sh
```

Validates skill frontmatter structure, required fields (`name`, `description`), directory conventions, and cross-references.

### 2. Marketplace Validation

```bash
./scripts/validate-marketplace.sh
```

Validates `plugin.json` and `marketplace.json` consistency, skill registration, and agent registration.

Run both before submitting (from repo root):

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

### Root Marketplace Validation

A separate shared script validates the root `.claude-plugin/marketplace.json` schema. It is called by both `validate-marketplace.sh` and directly by CI workflows:

```bash
./scripts/validate-root-marketplace.sh
```

### Release

#### Version Management

The canonical version source of truth is `.claude-plugin/plugin.json`. The version field is propagated to five locations by the bump script:

1. `.claude-plugin/plugin.json` -- canonical source
2. `.claude-plugin/marketplace.json` -- root marketplace plugin entry `.plugins[].version`
3. `.claude-plugin/marketplace.json` -- root marketplace `metadata.version`
4. `README.md` -- version badge
5. `CHANGELOG.md` -- promote `[Unreleased]` section and update footer links

CI validates version consistency across the first three locations (3-way check in `validate.yml`).

#### Bump Script

Use `scripts/bump.sh` to increment the version and propagate to all locations:

```bash
./scripts/bump.sh <patch|minor|major> [plugin-name]
```

- The second argument defaults to `dotnet-artisan`
- The script prints next-step instructions for committing, tagging, and pushing

Example:

```bash
./scripts/bump.sh patch
# Review: git diff
# Commit: git add -A && git commit -m "chore(release): bump dotnet-artisan to v0.1.1"
# Tag:    git tag dotnet-artisan/v0.1.1 && git push origin main && git push origin dotnet-artisan/v0.1.1
```

#### Tag Convention

Tags follow the format `dotnet-artisan/vX.Y.Z` (plugin-scoped, not bare `vX.Y.Z`). This allows multiple plugins to coexist in the same repo with independent version histories.

#### Release Workflow

On tag push matching `dotnet-artisan/v*`, the `release.yml` workflow:

1. Verifies the tag version matches `plugin.json`
2. Runs `scripts/validate-root-marketplace.sh` (shared root marketplace validation)
3. Runs `scripts/validate-skills.sh` and `scripts/validate-marketplace.sh`
4. Extracts the version-specific section from `CHANGELOG.md` using awk
5. Creates a GitHub Release with the extracted notes and install instructions

## Publishing to Marketplace

### Prerequisites

- GitHub repository is public (or accessible to the marketplace)
- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` are valid
- A GitHub Release exists with the target version tag

### Publishing Steps

1. Ensure the latest release tag is pushed to the repository
2. The marketplace indexes plugins from GitHub Releases automatically
3. Verify the plugin appears in the marketplace after indexing

### Post-Publish Verification

After publishing, confirm:

- Plugin is discoverable by name (`dotnet-artisan`)
- Plugin metadata (description, keywords, categories) renders correctly
- All skills are listed and accessible

### Cross-Provider Change Policy

Skill content must behave correctly across all supported providers (Claude, Codex, Copilot). Any PR that modifies skill content, routing descriptions, or agent definitions must satisfy these requirements:

- **PR description must state:** targeted provider (if any) and expected behavior deltas across providers. Provider-targeted changes require explicit verification against non-target providers to confirm no regressions.
- **Attach CI artifact links** or paste per-provider summary lines for `claude`/`codex`/`copilot` from CI matrix output. Run `./test.sh --agents claude,codex,copilot` locally or reference the CI workflow artifacts.
- **If behavior intentionally diverges** between providers, update `provider-baseline.json` in the same PR with a justification comment explaining why the divergence is expected.

### Release Checklist

Before every release, verify:

- [ ] `plugin.json` version matches the tag
- [ ] `marketplace.json` version matches the tag
- [ ] `CHANGELOG.md` has entries for this version with correct date
- [ ] `validate-skills.sh` passes (exit code 0)
- [ ] `validate-marketplace.sh` passes (exit code 0)
- [ ] All SKILL.md files have required frontmatter (`name`, `description`)
- [ ] Budget status is OK or WARN (not FAIL)
- [ ] No broken cross-references (all `[skill:<name>]` refs resolve)
- [ ] Cross-provider verification: changes verified against `claude`/`codex`/`copilot` matrix

## Hooks and MCP Contributions

The plugin includes session hooks (session start context, post-edit validation) and MCP server integrations (Context7).

For guidance on contributing to hooks or MCP integrations, see [docs/hooks-and-mcp-guide.md](docs/hooks-and-mcp-guide.md).

## Code of Conduct

We are committed to providing a welcoming and inclusive experience for everyone. Contributors are expected to:

- Be respectful and constructive in discussions and code reviews
- Focus on technical merit and improving the plugin
- Welcome newcomers and help them get started

Thank you for contributing to dotnet-artisan.
