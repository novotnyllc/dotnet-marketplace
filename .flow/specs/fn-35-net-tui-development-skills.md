# .NET TUI Development Skills

## Overview
Add skills for building terminal user interfaces (TUI) in .NET. Two major frameworks exist: Terminal.Gui (Miguel de Icaza) and Spectre.Console (Patrik Svensson). Both are actively maintained and serve different use cases.

## Scope
- **Terminal.Gui skill** — Full TUI framework: windows, menus, dialogs, views, layout (Computed vs Absolute), event handling, color themes, mouse support. Cross-platform (Windows/macOS/Linux).
- **Spectre.Console skill** — Rich console output: tables, trees, progress bars, prompts, markup, live displays, canvas, charts. Also covers Spectre.Console.Cli for command-line parsing.

### Scope Boundary Table

| Concern | Owner | Other epic/skill |
|---|---|---|
| Full TUI applications (windows, menus, views) | `[skill:dotnet-terminal-gui]` | — |
| Rich console output (tables, trees, progress) | `[skill:dotnet-spectre-console]` | — |
| Spectre.Console.Cli command parsing | `[skill:dotnet-spectre-console]` | Scope boundary with `[skill:dotnet-system-commandline]` |
| System.CommandLine parsing | — | `[skill:dotnet-system-commandline]` (cli-tools) |
| CLI app structure & distribution | — | `[skill:dotnet-cli-architecture]`, `[skill:dotnet-cli-distribution]` (cli-tools) |
| Blazor/web UI | — | `[skill:dotnet-blazor-patterns]` (ui-frameworks) |

### Out of Scope
- System.CommandLine patterns — covered by `[skill:dotnet-system-commandline]`
- CLI application architecture and distribution — covered by `[skill:dotnet-cli-architecture]` and `[skill:dotnet-cli-distribution]`
- Web UI frameworks — covered by `[skill:dotnet-blazor-patterns]`
- Native AOT trimming details — covered by `[skill:dotnet-native-aot]` (cross-referenced where relevant)

## .NET Version Policy
- Target baseline: `net8.0+`
- Package versions: latest stable releases of Terminal.Gui and Spectre.Console
- Both libraries support .NET 8+ and .NET 9+

## Dependencies
- **Hard:** none
- **Soft:** fn-17 (CLI tools) for scope boundary alignment with `[skill:dotnet-system-commandline]`

## Conventions
- Skill names use `dotnet-` prefix: `dotnet-terminal-gui`, `dotnet-spectre-console`
- SKILL.md frontmatter: `name` and `description` only
- Cross-references use `[skill:skill-name]` syntax
- Skill descriptions target under 120 characters

## Task Decomposition

| Task | Deliverables | Files |
|---|---|---|
| .1 Terminal.Gui skill | SKILL.md with lifecycle, layout, views, menus, events, themes, Agent Gotchas, References, Prerequisites | `skills/tui/dotnet-terminal-gui/SKILL.md` |
| .2 Spectre.Console skill | SKILL.md with rich output, progress, prompts, CLI, Agent Gotchas, References, Prerequisites | `skills/tui/dotnet-spectre-console/SKILL.md` |
| .3 Integration | Register skills in plugin.json, update README/CLAUDE.md/AGENTS.md counts, add trigger-corpus entries, run validation | `.claude-plugin/plugin.json`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `scripts/trigger-corpus.json` |

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Terminal.Gui skill covering lifecycle, layout, views, menus, event handling, themes
- [ ] Spectre.Console skill covering rich output, prompts, tables, progress, CLI
- [ ] Each skill has canonical SKILL.md structure: frontmatter, overview, content sections, Agent Gotchas, Prerequisites, References
- [ ] Each skill description under 120 characters
- [ ] Scope boundary with `[skill:dotnet-system-commandline]` documented in Spectre.Console skill
- [ ] Cross-references use `[skill:skill-name]` syntax: async patterns, Terminal.Gui ↔ Spectre.Console, system-commandline, cli-architecture, native-aot
- [ ] Both skills registered in plugin.json
- [ ] README.md updated with new TUI category and skill counts
- [ ] CLAUDE.md updated with new counts
- [ ] AGENTS.md routing index updated with TUI category
- [ ] Trigger corpus entries added for TUI skill routing
- [ ] No fn-N spec references in skill content
- [ ] Budget constraint respected (~240 chars addition within 15,000 limit)
- [ ] All validation commands pass

## References
- Terminal.Gui GitHub — https://github.com/gui-cs/Terminal.Gui
- Spectre.Console GitHub — https://github.com/spectreconsole/spectre.console
