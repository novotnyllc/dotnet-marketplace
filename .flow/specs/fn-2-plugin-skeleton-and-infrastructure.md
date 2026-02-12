# Plugin Skeleton and Infrastructure

## Overview

Create the foundational plugin structure for dotnet-artisan. This is the Wave 0 epic that blocks ALL other work. It establishes the plugin.json manifest, directory layout, router/advisor skill, version detection skill, project analysis skill, and validation infrastructure.

**Spec reference:** `docs/dotnet-artisan-spec.md` sections: Core Design Principles, Plugin Architecture, Foundation & Plugin Infrastructure

## Scope

**In scope:**
- `.claude-plugin/plugin.json` and `marketplace.json` manifests
- Directory structure: `skills/`, `agents/`, `hooks/`, `scripts/`
- `dotnet-advisor` router/index skill (compressed catalog, progressive disclosure)
- `dotnet-version-detection` skill (read TFMs, SDK versions, detect preview features)
- `dotnet-project-analysis` skill (solution structure, project refs, CPM)
- `plugin-self-publish` skill (plugin versioning, changelog, CI/CD)
- Validation scripts for SKILL.md frontmatter and cross-references
- Basic CI workflow skeleton (validate on push)

**Out of scope:**
- Actual .NET domain skills (Wave 1+)
- Hooks system (fn-23)
- MCP integration (fn-23)
- Cross-agent build pipeline (fn-24)
- README/CONTRIBUTING (fn-25)

## Approach

### Plugin Structure (validated via `/plugin-dev:plugin-structure`)

```
dotnet-artisan/
  .claude-plugin/
    plugin.json          # name, version, skills[], agents[], hooks
    marketplace.json     # marketplace metadata
  skills/
    foundation/
      dotnet-advisor/SKILL.md
      dotnet-version-detection/SKILL.md
      dotnet-project-analysis/SKILL.md
      plugin-self-publish/SKILL.md
    # Wave 1+ skills go in category dirs: core-csharp/, architecture/, etc.
  agents/
    dotnet-architect.md
  hooks/
    hooks.json           # Empty initially, populated by fn-23
  scripts/
    validate-skills.sh   # Frontmatter + cross-ref validation
    validate-marketplace.sh  # Plugin/marketplace JSON validation
  .mcp.json              # Empty initially, populated by fn-23
```

### Canonical plugin.json Schema

```json
{
  "name": "dotnet-artisan",
  "version": "0.1.0",
  "description": "...",
  "skills": ["skills/foundation/dotnet-advisor", "skills/foundation/dotnet-version-detection", ...],
  "agents": ["agents/dotnet-architect.md"],
  "hooks": "hooks/hooks.json",
  "mcpServers": ".mcp.json"
}
```

- `skills`: array of directory paths (each must contain `SKILL.md`)
- `agents`: array of file paths (each `.md` file with agent frontmatter)
- `hooks`: string path to hooks.json file
- `mcpServers`: string path to .mcp.json file

### Required SKILL.md Frontmatter (canonical set)

All SKILL.md files MUST have these frontmatter fields:
- `name` (string, required): skill identifier matching directory name
- `description` (string, required): trigger phrase, WHEN + WHEN NOT pattern

Optional frontmatter fields:
- `disable-model-invocation` (boolean): for side-effect-only skills
- `user-invocable` (boolean): whether user can invoke directly

This is the single source of truth for validation. `validate-skills.sh` enforces exactly these required fields.

### Cross-Reference Syntax

Skills cross-referencing other skills MUST use the format: `[skill:skill-name]` (e.g., `[skill:dotnet-version-detection]`). The `validate-skills.sh` script validates only this machine-parseable syntax.

### Context Budget Architecture

**Critical constraint:** Combined skill descriptions must stay under ~15,000 characters.

Strategy:
- Router skill (`dotnet-advisor`) gets a compressed catalog: ~50 chars per skill, organized by category
- Each skill description is a precise trigger phrase (WHEN + WHEN NOT pattern, ~120 chars)
- MCP Tool Search auto-activates when >10% context consumed (handles 80+ skills gracefully)
- Prototype and validate budget math in task fn-2.2

**Budget validation thresholds** (coherent across all files):
- `PROJECTED_SKILLS_COUNT`: 95 (derived from spec catalog, buffered up from ~90)
- `MAX_DESC_CHARS`: 120 (aggressive target per description, enforces compression)
- Projected max: 95 x 120 = 11,400 chars
- **WARN** at 12,000 chars (current or projected)
- **FAIL** at 15,000 chars (hard platform limit)
- Target: keep current combined descriptions under 12,000 chars

`validate-skills.sh` outputs stable keys for CI parsing:
```
CURRENT_DESC_CHARS=<N>
PROJECTED_DESC_CHARS=<N>
BUDGET_STATUS=OK|WARN|FAIL
```

### Router/Advisor Skill Design

The `dotnet-advisor` skill is always loaded. Its description triggers on ANY .NET-related query. Its body contains:
- Compressed catalog of ALL 19 planned categories as stubs (each with `implemented` or `planned` status)
- Decision logic: "if user is doing X, load skills Y and Z"
- Version detection trigger: "first, check what .NET version the project uses"
- Cross-references to specialist skills using `[skill:name]` syntax

### Version Detection Design

The `dotnet-version-detection` skill:
- Reads `.csproj` TargetFramework/TargetFrameworks
- Reads `global.json` for SDK version
- Reads `Directory.Build.props` for shared TFM settings
- Detects `<LangVersion>preview</LangVersion>` for preview features
- Detects `<EnablePreviewFeatures>true</EnablePreviewFeatures>` for .NET 11 features
- Outputs structured guidance: "This project targets net10.0 with C# 14. Use modern patterns."
- Multi-targeting: reports all TFMs, recommends highest for guidance, notes polyfill needs

**Precedence algorithm for TFM resolution:**
1. Direct `<TargetFramework>` value in .csproj (highest priority)
2. `<TargetFrameworks>` (semicolon-delimited) -- report all, guide on highest
3. `Directory.Build.props` shared TFM (if no per-project override)
4. MSBuild property expressions (e.g., `$(SomeTfm)`) -- emit "unresolved property" warning, fall back to `global.json` SDK version
5. `dotnet --version` as last resort

**Version-specific feature catalog:** Stored as a dated reference data section within SKILL.md (not inline detection logic). Tagged with `Last updated: YYYY-MM-DD` for staleness tracking. The skill detects versions; the data section maps versions to features.

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Context budget math fails | Router cannot function, whole architecture breaks | Projected budget validation (warn at 12k, fail at 15k), prototype in fn-2.2 |
| Plugin structure mismatch | Skills do not auto-discover | Use `/plugin-dev:plugin-structure` to validate |
| Description triggers too generic | Wrong skills load | Use `/plugin-dev:skill-reviewer` on each skill |
| Version detection edge cases (MSBuild property indirection) | Wrong .NET guidance | Precedence algorithm + unresolved property warnings |
| Cross-reference format not parseable | Validation misses broken refs | Canonical `[skill:name]` syntax, validated in CI |

## Non-functional targets

- Plugin loads in <2s
- Router skill description <500 chars
- Individual skill descriptions target <120 chars (enforced by projected budget math)
- Combined all-skill descriptions target <12,000 chars (warn), hard fail at 15,000 chars
- Validation scripts run in <5s (single-pass scan, no subprocess spawning, no network)
- Validation scripts output stable keys: CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS
- CI validation workflow runs in <2 min

## Quick commands

```bash
# Validate plugin structure
jq empty .claude-plugin/plugin.json

# Run skill validation (used both locally and in CI)
./scripts/validate-skills.sh

# Run marketplace validation
./scripts/validate-marketplace.sh

# Run all validation (same as CI)
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh

# Test locally by symlinking plugin
ln -sf $(pwd) ~/.claude/plugins/dotnet-artisan
```

## Acceptance

- [ ] `.claude-plugin/plugin.json` validates against canonical schema (skills=array of paths, agents=array of paths, hooks=string path, mcpServers=string path)
- [ ] `marketplace.json` has correct metadata (name, author, version, description)
- [ ] `dotnet-advisor` skill triggers on .NET-related queries and routes to all 19 categories (implemented/planned stubs)
- [ ] `dotnet-version-detection` skill correctly reads TFMs with defined precedence algorithm
- [ ] `dotnet-project-analysis` skill understands solution structure, uses canonical frontmatter and `[skill:name]` cross-refs
- [ ] Combined skill descriptions under 12,000 characters (warn), hard fail at 15,000
- [ ] Projected budget: 95 skills x 120 chars = 11,400 (under 12,000 warn threshold)
- [ ] Validation script catches malformed SKILL.md frontmatter (canonical required fields: name, description)
- [ ] Validation script validates `[skill:name]` cross-references
- [ ] Validation script outputs stable keys: CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS
- [ ] CI workflow runs exact same validation commands as local scripts
- [ ] Directory structure matches Claude Code plugin conventions
- [ ] All SKILL.md files have required frontmatter (name, description)
