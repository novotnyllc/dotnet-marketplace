# fn-52-fill-skill-gaps-from-dotnet-skills.1 Add dotnet-slopwatch standalone skill

## Description
Create a standalone `dotnet-slopwatch` skill that instructs agents to **run** the `Slopwatch.Cmd` dotnet tool as an automated quality gate after code modifications.

**Size:** M
**Files:** `skills/agent-meta-skills/dotnet-slopwatch/SKILL.md`

## Approach

- Reference the external dotnet-skills slopwatch skill at `~/.claude/plugins/cache/dotnet-skills/dotnet-skills/1.2.0/skills/slopwatch/SKILL.md` for content structure
- Cover: tool installation (`Slopwatch.Cmd` v0.2.0 via `dotnet tool install`), `slopwatch analyze` usage, `.slopwatch/slopwatch.json` configuration, detection rules (SW001-SW006), Claude Code hook integration (`PostToolUse` on Write|Edit), CI/CD integration (GHA + ADO)
- Follow pattern at `skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md` for category conventions
- Cross-reference `[skill:dotnet-tool-management]` for general tool installation mechanics
- Frontmatter: `user-invocable: true` (users can invoke `/dotnet-slopwatch` to run quality gate on demand)
- BrighterCommand/Brighter uses hook: `slopwatch analyze -d . --hook` — include this pattern
- Note: cross-ref additions to 4 existing agent-meta-skills are owned by T4 (integration) per file-disjoint convention

## Key Context

- `Slopwatch.Cmd` is a real NuGet package (v0.2.0), installed as dotnet tool with command `slopwatch`
- 6 detection rules: SW001 (disabled tests), SW002 (warning suppression), SW003 (empty catch), SW004 (arbitrary delays), SW005 (project file slop), SW006 (CPM bypass)
- The existing embedded sections in 4 agent-meta-skills teach pattern recognition (reading code); the standalone skill teaches tool execution (running CLI). Both are valuable — don't delete existing content.
## Acceptance
- [ ] `skills/agent-meta-skills/dotnet-slopwatch/SKILL.md` exists with valid frontmatter
- [ ] `name: dotnet-slopwatch` matches directory name
- [ ] `description` under 120 characters
- [ ] `user-invocable: true` set in frontmatter
- [ ] Covers `Slopwatch.Cmd` NuGet installation (local + global)
- [ ] Covers `slopwatch analyze` command usage
- [ ] Covers `.slopwatch/slopwatch.json` configuration
- [ ] Documents all 6 detection rules (SW001-SW006)
- [ ] Includes Claude Code hook integration (PostToolUse on Write|Edit)
- [ ] Includes CI/CD integration (GitHub Actions + Azure Pipelines)
- [ ] Cross-references `[skill:dotnet-tool-management]` for tool mechanics
- [ ] Has ## Agent Gotchas section
- [ ] Has ## Prerequisites section
- [ ] Has ## References section
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
