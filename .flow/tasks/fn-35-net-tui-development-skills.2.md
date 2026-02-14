# fn-35-net-tui-development-skills.2 Create Spectre.Console skill

## Description
Create skills/tui/dotnet-spectre-console/SKILL.md covering Spectre.Console for rich console output and Spectre.Console.Cli for command-line application structure.

**Size:** M
**Files:** skills/tui/dotnet-spectre-console/SKILL.md, .claude-plugin/plugin.json

## Approach
- Rich output: AnsiConsole.MarkupLine, tables, trees, panels, rules, figlet text
- Progress: AnsiConsole.Progress(), status spinners, multi-task progress
- Prompts: TextPrompt, SelectionPrompt, MultiSelectionPrompt, ConfirmationPrompt
- Live displays: AnsiConsole.Live() for updating content
- Spectre.Console.Cli: command hierarchy, settings classes, DI, type converters
- Latest stable Spectre.Console package
- Cross-ref to [skill:dotnet-terminal-gui] for full TUI alternative
## Acceptance
- [ ] Rich output patterns documented
- [ ] Progress and prompts covered
- [ ] Spectre.Console.Cli framework covered
- [ ] Latest stable package version
- [ ] Cross-ref to Terminal.Gui
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
