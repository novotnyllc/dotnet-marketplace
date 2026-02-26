# fn-64-consolidate-131-skills-into-20-broad.5 Consolidate UI framework skills: dotnet-blazor, dotnet-uno, dotnet-maui, dotnet-desktop

## Description
Create consolidated skill directories for UI framework skills: `dotnet-blazor`, `dotnet-uno`, `dotnet-maui`, and `dotnet-desktop`. Each absorbs its framework-specific testing skill (blazor-testing, uno-testing, maui-testing) and all sub-skills.

**Size:** M
**Files:** `skills/dotnet-blazor/SKILL.md` + `references/*.md` (new), `skills/dotnet-uno/SKILL.md` + `references/*.md` (new), `skills/dotnet-maui/SKILL.md` + `references/*.md` (new), `skills/dotnet-desktop/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~15 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- `dotnet-blazor` merges: blazor-patterns, blazor-components, blazor-auth, blazor-testing
- `dotnet-uno` merges: uno-platform, uno-targets, uno-mcp, uno-testing
- `dotnet-maui` merges: maui-development, maui-aot, maui-testing
- `dotnet-desktop` merges: winui, wpf-modern, wpf-migration, winforms-basics, accessibility, ui-chooser
- Framework-testing content goes in `references/testing.md` within each UI skill

## Key context

- `dotnet-uno-mcp` is special: it queries Uno MCP server. Its content becomes `references/mcp.md` inside `dotnet-uno`
- `dotnet-ui-chooser` is a router skill (decision tree); place inside `dotnet-desktop` or keep standalone per task .1 mapping
- `dotnet-accessibility` is cross-cutting; placement per task .1 mapping
## Acceptance
- [ ] `skills/dotnet-blazor/SKILL.md` + `references/` created (includes blazor-testing content)
- [ ] `skills/dotnet-uno/SKILL.md` + `references/` created (includes uno-testing, uno-mcp content)
- [ ] `skills/dotnet-maui/SKILL.md` + `references/` created (includes maui-testing content)
- [ ] `skills/dotnet-desktop/SKILL.md` + `references/` created (includes WPF, WinUI, WinForms, accessibility)
- [ ] All source skill directories for this batch deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on all SKILL.md files
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
