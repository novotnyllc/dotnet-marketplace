# Fill Skill Gaps from dotnet-skills

## Overview

The external `dotnet-skills` plugin (Aaronontheweb/dotnet-skills, 344 stars) contains skills not covered by dotnet-artisan. Excluding Akka-specific content, this epic adds 4 new skills that fill the most impactful gaps. Four candidates were dropped after overlap/scope analysis (playwright-ci-caching overlaps with `dotnet-playwright` CI section; verify-email-snapshots overlaps with `dotnet-snapshot-testing` email section; aspire-mailpit and mjml-email-templates removed from scope).

The highest-value addition is **dotnet-slopwatch** — a standalone skill that instructs agents to **run** the `Slopwatch.Cmd` dotnet tool (NuGet v0.3.3) as an automated quality gate after code modifications. Currently, slopwatch anti-patterns are only embedded as documentation sections in 4 agent-meta-skills; the actual CLI tool is not referenced anywhere.

## Scope

### In Scope — 4 New Skills

| Skill | Category | Size | Rationale |
|-------|----------|------|-----------|
| `dotnet-slopwatch` | `agent-meta-skills` | M | Agent-executed quality gate using `Slopwatch.Cmd` tool. Covers install, analyze, configure, CI hooks. Existing embedded sections in 4 skills stay but get `[skill:dotnet-slopwatch]` cross-refs (added by T4). |
| `dotnet-csharp-api-design` | `api-development` | S | Public API design principles: naming, parameter ordering, return types, error patterns, extension points, wire compatibility. Complementary to existing `dotnet-library-api-compat` (enforcement) and `dotnet-api-surface-validation` (tooling). |
| `dotnet-csharp-concurrency-patterns` | `core-csharp` | S | Concurrency beyond async/await: lock, SemaphoreSlim, Interlocked, ConcurrentDictionary, ReaderWriterLockSlim, decision framework. Fills the gap where `dotnet-csharp-concurrency-specialist` agent exists but has no corresponding skill. |
| `dotnet-csharp-type-design-performance` | `core-csharp` | S | Type design for performance: struct vs class decision matrix, sealed by default, readonly struct, Span/Memory, collection type selection (Dictionary vs FrozenDictionary vs ImmutableDictionary). Focus on upfront design choices, not optimization techniques (covered by `dotnet-performance-patterns`). |

### Out of Scope

- **Akka.NET skills** — Different domain, maintained by dotnet-skills
- **playwright-ci-caching** — `dotnet-playwright` already has CI Browser Caching section (line 263+)
- **verify-email-snapshots** — `dotnet-snapshot-testing` already has email verification section (lines 306-351)
- **dotnet-aspire-mailpit** — Removed from scope
- **dotnet-mjml-email-templates** — Removed from scope
- **docfx-specialist agent** — DocFX well-covered across 9 existing skills; `dotnet-docs-generator` agent exists
- **New categories** — All 4 skills fit existing categories
- **Changing existing skill content** — Only adding `[skill:dotnet-slopwatch]` cross-references to 4 agent-meta-skills (owned by T4 integration task)

### Scope Boundary Table

| Concern | This Epic Owns | Other Epic Owns |
|---------|---------------|-----------------|
| Slopwatch tool integration | Standalone skill with install/run/configure | fn-9: Embedded anti-pattern documentation (stays) |
| API design principles | Design-time API decisions | fn-11: Enforcement tooling (`dotnet-library-api-compat`, `dotnet-api-surface-validation`) |
| Concurrency patterns | Skill knowledge base | Existing: Agent delegation (`dotnet-csharp-concurrency-specialist` agent) |
| Type design for perf | Upfront type selection | fn-18: Optimization techniques (`dotnet-performance-patterns`) |

## Dependencies

- **fn-2** (Plugin Skeleton) — DONE. Infrastructure for skill creation.
- **fn-51** (Frontmatter) — DONE. Establishes `user-invocable: false` pattern.

No blocking dependencies. All prerequisite epics are complete.

## .NET Version Policy

- Baseline: .NET 8 (LTS)
- Since .NET 8 is the baseline, FrozenDictionary is in-scope by default. Include version notes (e.g., "Requires .NET 8+") for readers on older TFMs, but no conditional compilation guidance needed.

## Conventions

- All 4 new skills use `user-invocable: false` (reference skills, not `/`-menu commands)
- `dotnet-slopwatch` additionally gets `user-invocable: true` — users should be able to invoke `/dotnet-slopwatch` to run the quality gate on demand
- All skills follow `dotnet-` prefix naming
- Cross-references use `[skill:skill-name]` syntax
- Description budget: current 11,681 / 15,360 chars. Adding 4 skills at ~90 chars avg = ~360 chars → ~12,041 (near WARN 12,000, well under FAIL 15,360)
- `--projected-skills` in `validate-skills.sh` updated from 126 to 130
- Cross-ref edits to existing skills owned by T4 (integration) per file-disjoint convention — content-authoring tasks (T1, T3) only create new files

## Quick Commands

```bash
# Validate all skills after changes
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh

# Check budget impact
./scripts/validate-skills.sh 2>&1 | grep -E 'CURRENT_DESC_CHARS|BUDGET_STATUS'

# Verify new skills registered
jq '.skills | length' plugins/dotnet-artisan/.claude-plugin/plugin.json

# Verify all 4 new skills reachable from plugin.json
jq -r '.skills[]' plugins/dotnet-artisan/.claude-plugin/plugin.json | grep -c 'slopwatch\|api-design\|concurrency-patterns\|type-design'

# Verify slopwatch cross-references
grep -r '\[skill:dotnet-slopwatch\]' plugins/dotnet-artisan/skills/agent-meta-skills/
```

## Task Decomposition

| Task | Deliverables | Files |
|------|-------------|-------|
| T1: Slopwatch standalone skill | `dotnet-slopwatch` SKILL.md | `skills/agent-meta-skills/dotnet-slopwatch/SKILL.md` |
| T3: C# design skills | `dotnet-csharp-api-design` + `dotnet-csharp-concurrency-patterns` + `dotnet-csharp-type-design-performance` SKILL.md files | `skills/api-development/dotnet-csharp-api-design/SKILL.md`, `skills/core-csharp/dotnet-csharp-concurrency-patterns/SKILL.md`, `skills/core-csharp/dotnet-csharp-type-design-performance/SKILL.md` |
| T4: Integration & docs | plugin.json registration, slopwatch cross-refs in 4 existing skills, doc count updates, Mermaid labels, validation script update, agent preloaded skills, trigger-corpus verification | `plugin.json`, `README.md`, `AGENTS.md`, `CLAUDE.md` (root + plugin), `CONTRIBUTING-SKILLS.md`, `validate-skills.sh`, `dotnet-csharp-concurrency-specialist.md`, 4 existing agent-meta-skills |

## Acceptance

- [ ] 4 new SKILL.md files exist with valid frontmatter (`name` + `description`, name matches directory)
- [ ] All 4 skills registered in `plugin.json` `skills` array
- [ ] `dotnet-slopwatch` references `Slopwatch.Cmd` NuGet package with install, analyze, and hook configuration
- [ ] `dotnet-slopwatch` has `user-invocable: true` (agents and users can invoke it)
- [ ] Remaining 3 skills have `user-invocable: false`
- [ ] 4 existing agent-meta-skills have `[skill:dotnet-slopwatch]` cross-references added (owned by T4)
- [ ] `dotnet-csharp-concurrency-specialist` agent preloaded skills updated to include `[skill:dotnet-csharp-concurrency-patterns]`
- [ ] `--projected-skills` in `validate-skills.sh` updated from 126 to 130
- [ ] README.md, AGENTS.md, CLAUDE.md (root + plugin) skill/category counts updated (126→130)
- [ ] README.md Mermaid node labels updated: `Skills` subgraph (126→130), `CC` (16→18), `AD` (8→9), `AM` (4→5)
- [ ] CONTRIBUTING-SKILLS.md budget math updated with recalculated average and total from actual validation output
- [ ] Each description under 120 characters
- [ ] `./scripts/validate-skills.sh` passes (exit 0)
- [ ] `./scripts/validate-marketplace.sh` passes (exit 0)
- [ ] Trigger-corpus.json verified: all categories receiving new skills have at least one corpus entry
- [ ] No broken cross-references
- [ ] Budget CURRENT_DESC_CHARS < 15,360 (FAIL threshold)

## References

- External dotnet-skills slopwatch skill: `~/.claude/plugins/cache/dotnet-skills/dotnet-skills/1.2.0/skills/slopwatch/SKILL.md`
- Slopwatch.Cmd NuGet: v0.3.3, commands: `slopwatch`, package: `Slopwatch.Cmd`
- BrighterCommand/Brighter slopwatch hook: PostToolUse Write|Edit → `slopwatch analyze -d . --hook`
- CONTRIBUTING-SKILLS.md: `plugins/dotnet-artisan/CONTRIBUTING-SKILLS.md`
- Existing overlap files:
  - `skills/testing/dotnet-playwright/SKILL.md` (CI caching, line 263+)
  - `skills/testing/dotnet-snapshot-testing/SKILL.md` (email verification, lines 306-351)
  - `skills/performance/dotnet-performance-patterns/SKILL.md` (struct/class/sealed)
  - `skills/api-development/dotnet-library-api-compat/SKILL.md` (compat enforcement)
  - `agents/dotnet-csharp-concurrency-specialist.md` (concurrency agent, 200 lines)
