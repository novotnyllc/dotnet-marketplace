## Description

Add `user-invocable: false` + `context: fork` + `model: haiku` to 4 detection/analysis skills, plus dynamic context (`!` shell preprocessing) where runtime project data improves results. T3 owns these 4 files exclusively — T2 does not touch them.

**Size:** S
**Files:**
- `skills/foundation/dotnet-version-detection/SKILL.md`
- `skills/foundation/dotnet-project-analysis/SKILL.md`
- `skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md`
- `skills/agent-meta-skills/dotnet-build-analysis/SKILL.md`

## Approach

- Add `user-invocable: false`, `context: fork`, and `model: haiku` to frontmatter of each detection skill
- Add dynamic context (`!` command) preprocessing where beneficial — uses code fence with `!` prefix in the skill body, below frontmatter. The preprocessor runs the shell command and replaces the block with its output before Claude sees the content.

### Concrete syntax example (target for `dotnet-version-detection`)

```markdown
---
name: dotnet-version-detection
description: Detects installed .NET SDK and runtime versions, TFMs, and global.json constraints
user-invocable: false
context: fork
model: haiku
---

```! dotnet --version 2>/dev/null
```

# dotnet-version-detection
...rest of existing skill content unchanged...
```

### Dynamic context per skill

- `dotnet-version-detection`: `! dotnet --version 2>/dev/null`
- `dotnet-project-analysis`: `! find . -maxdepth 3 \( -name "*.csproj" -o -name "*.sln" -o -name "*.slnx" \) 2>/dev/null | head -20`
- `dotnet-solution-navigation`: `! find . -maxdepth 2 \( -name "*.sln" -o -name "*.slnx" \) 2>/dev/null | head -5`
- `dotnet-build-analysis`: no dynamic context needed (analyzes build output provided in conversation)

## Key context

- `model: haiku` only takes effect with `context: fork` — this is required
- `context: fork` skills get their own context window — conversation history is NOT passed
- These 4 skills are the only ones where fork makes sense — reference/convention skills NEED conversation context
- Note: `dotnet-solution-navigation` and `dotnet-build-analysis` are under `skills/agent-meta-skills/`, NOT `skills/foundation/` — use registered paths from `plugin.json`
- All `!` commands use `2>/dev/null` to gracefully handle missing tools/projects

## Acceptance

- [ ] 4 detection skills have `user-invocable: false` + `context: fork` + `model: haiku` in frontmatter
- [ ] `dotnet-version-detection` has dynamic context `! dotnet --version 2>/dev/null`
- [ ] `dotnet-project-analysis` has dynamic context for project file listing
- [ ] `dotnet-solution-navigation` has dynamic context for solution file listing
- [ ] `dotnet-build-analysis` has `context: fork` + `model: haiku` (no dynamic context)
- [ ] Dynamic context verified: each `!` command manually run in shell produces output or empty output without errors
- [ ] Existing skill content below frontmatter is unchanged (only frontmatter and dynamic context block added)
- [ ] `validate-skills.sh && validate-marketplace.sh` pass clean

## Done summary

_To be filled on completion._

## Evidence

_To be filled on completion._
