# Add Proper Skill Frontmatter Across All Skills

## Overview

fn-49 was instructed to optimize UX and mark implicit skills appropriately, but `user-invocable: false` was never actually set on any skill. Currently all 127 skills have only `name` + `description` frontmatter (except `plugin-self-publish` which has `disable-model-invocation: true`). This epic:

1. **Removes `plugin-self-publish`** from the plugin (it's repo-level publishing instructions, not a .NET skill) and moves its content to repo-level instructions
2. **Adds `user-invocable: false`** on 117 implicit/reference skills (hides from `/` menu)
3. **Adds `context: fork` + `model: haiku`** on 4 detection/analysis skills (isolated execution, cheaper model)
4. **Adds dynamic context (`!` syntax)** on detection skills that benefit from runtime project data
5. **Updates validation + documentation** to accept and describe the expanded frontmatter

## Scope

### In scope
- Remove `plugin-self-publish` from plugin; move content to repo-level instructions (e.g., CONTRIBUTING.md or a repo-level CLAUDE.md section)
- Add `user-invocable: false` to 113 skills that are reference/convention content (T2 scope)
- Add `user-invocable: false` + `context: fork` + `model: haiku` + dynamic context to 4 detection skills (T3 scope — T3 owns these files exclusively)
- Keep 9 skills user-invocable (actionable commands users would type as `/` commands)
- Update `_validate_skills.py` `ALLOWED_FRONTMATTER_FIELDS` to accept new fields, with type validation for boolean/string fields
- Update `CONTRIBUTING-SKILLS.md`, plugin `CLAUDE.md`, and root `CLAUDE.md` with expanded frontmatter spec

### Out of scope
- Changing skill descriptions or content (covered by fn-49)
- Adding `allowed-tools` restrictions (agent-level concern, defer)
- Adding `agent` field to skills (requires agent system changes)
- Adding `hooks` field to skills (no current need)

## User-invocable classification

**Keep user-invocable (default true) — 9 actionable command skills:**
- `dotnet-advisor` — Router skill, always loaded, entry point for users
- `dotnet-scaffold-project` — Scaffolds new projects
- `dotnet-add-ci` — Adds CI/CD pipelines
- `dotnet-add-testing` — Adds test infrastructure
- `dotnet-add-analyzers` — Adds static analysis
- `dotnet-modernize` — Audits/upgrades projects
- `dotnet-ui-chooser` — UI framework selection wizard
- `dotnet-data-access-strategy` — Data access selection wizard (borderline — revisit post-launch based on usage)
- `dotnet-version-upgrade` — Version migration tool (borderline — revisit post-launch based on usage)

**Remove from plugin:**
- `plugin-self-publish` — Not a .NET skill; repo-level publishing instructions. Remove from plugin, move content to repo-level docs.

**Set `user-invocable: false` — 117 skills total:**
- 113 handled by T2 (all implicit skills except the 4 detection skills)
- 4 handled by T3 (detection skills get `user-invocable: false` PLUS `context: fork` + `model: haiku`)

**Math:** 127 current - 1 removed (`plugin-self-publish`) = 126 remaining. 126 - 9 user-invocable = 117 implicit. Of those 117: 113 in T2, 4 in T3. No file overlap.

## Detection skills for `context: fork`

These skills run as self-contained detection/analysis producing structured output. They don't need conversation history and benefit from isolated execution with a cheaper model.

**T3 owns these 4 files exclusively** (T2 does not touch them):

| Skill | Registered path | `context: fork` | `model` | Dynamic context (`!`) |
|-------|----------------|-----------------|---------|----------------------|
| `dotnet-version-detection` | `skills/foundation/dotnet-version-detection` | yes | haiku | `! dotnet --version 2>/dev/null` |
| `dotnet-project-analysis` | `skills/foundation/dotnet-project-analysis` | yes | haiku | `! find . -maxdepth 3 \( -name "*.csproj" -o -name "*.sln" -o -name "*.slnx" \) 2>/dev/null \| head -20` |
| `dotnet-solution-navigation` | `skills/agent-meta-skills/dotnet-solution-navigation` | yes | haiku | `! find . -maxdepth 2 \( -name "*.sln" -o -name "*.slnx" \) 2>/dev/null \| head -5` |
| `dotnet-build-analysis` | `skills/agent-meta-skills/dotnet-build-analysis` | yes | haiku | none |

### Dynamic context syntax

Dynamic context uses the `!` prefix on a code fence in the skill body. The preprocessor runs the shell command and replaces the block with its output before Claude sees the content. Example target for `dotnet-version-detection`:

```
---
name: dotnet-version-detection
description: Detects installed .NET SDK and runtime versions, TFMs, and global.json constraints
user-invocable: false
context: fork
model: haiku
---

<!-- Dynamic context: injected at load time -->
```! dotnet --version 2>/dev/null
```

# dotnet-version-detection
...rest of skill content...
```

## Key constraints

- **Validation first**: `_validate_skills.py` line 30 `ALLOWED_FRONTMATTER_FIELDS = {"name", "description"}` must be expanded BEFORE or WITH skill changes, otherwise CI fails
- **Type validation**: T1 should add type checking for boolean fields (`user-invocable`, `disable-model-invocation`) and string fields (`context`, `model`) to catch quoted-string booleans like `user-invocable: "false"`
- **Budget impact**: Removing `plugin-self-publish` (which had `disable-model-invocation: true`, so its description was NOT in context) does not change the context budget. Adding `user-invocable: false` does NOT remove descriptions from context budget — only `disable-model-invocation: true` does. This is purely UX decluttering.
- **`context: fork` caution**: NOT appropriate for reference/convention skills — they need conversation context to be useful. Only use on self-contained detection tasks.
- **File ownership**: T1 owns validation/docs + plugin-self-publish removal. T2 owns 113 implicit skill files. T3 owns 4 detection skill files. No overlap between T2 and T3.

## Quick commands

```bash
cd plugins/dotnet-artisan
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] `plugin-self-publish` removed from plugin (SKILL.md deleted, removed from plugin.json skills array)
- [ ] `plugin-self-publish` content moved to repo-level instructions
- [ ] 113 implicit skills have `user-invocable: false` in frontmatter (T2)
- [ ] 4 detection skills have `user-invocable: false` + `context: fork` + `model: haiku` (T3)
- [ ] 9 user-invocable skills do NOT have `user-invocable: false`
- [ ] 3 detection skills have working dynamic context `!` commands (version-detection, project-analysis, solution-navigation)
- [ ] `_validate_skills.py` accepts all new frontmatter fields with type validation for booleans/strings
- [ ] `validate-skills.sh && validate-marketplace.sh` pass clean (now with 126 skills)
- [ ] `CONTRIBUTING-SKILLS.md` documents expanded frontmatter spec
- [ ] Plugin `CLAUDE.md` updated with new frontmatter fields
- [ ] Root `CLAUDE.md` updated with new frontmatter fields
- [ ] Dynamic context `!` commands verified: each produces output or graceful empty output without errors in a shell

## References

- Official frontmatter spec: https://code.claude.com/docs/en/skills#frontmatter-reference
- `_validate_skills.py:30` — `ALLOWED_FRONTMATTER_FIELDS`
- `CONTRIBUTING-SKILLS.md:82-90` — Current frontmatter docs ("No other frontmatter fields are recognized")
- `plugins/dotnet-artisan/CLAUDE.md:7-20` — "Every skill requires exactly two frontmatter fields"
- fn-49 (completed) — Optimized descriptions but missed `user-invocable` field
