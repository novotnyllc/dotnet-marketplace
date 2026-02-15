# fn-35-net-tui-development-skills.2 Create Spectre.Console skill

## Description
Create skills/tui/dotnet-spectre-console/SKILL.md covering Spectre.Console for rich console output and Spectre.Console.Cli for command-line application structure. Include scope boundary with System.CommandLine, Agent Gotchas, Prerequisites, and References sections per canonical SKILL.md structure.

**Size:** M
**Files:** skills/tui/dotnet-spectre-console/SKILL.md

## Approach
- Frontmatter: `name: dotnet-spectre-console`, `description` under 120 chars
- Rich output: AnsiConsole.MarkupLine, tables, trees, panels, rules, figlet text
- Progress: AnsiConsole.Progress(), status spinners, multi-task progress
- Prompts: TextPrompt, SelectionPrompt, MultiSelectionPrompt, ConfirmationPrompt
- Live displays: AnsiConsole.Live() for updating content
- Spectre.Console.Cli: command hierarchy, settings classes, DI, type converters
- Scope boundary: "For System.CommandLine patterns, see `[skill:dotnet-system-commandline]`"
- Agent Gotchas: console output pitfalls (ANSI support detection, CI environments, redirected output)
- Prerequisites: Spectre.Console NuGet package, net8.0+ baseline
- References: GitHub repo, NuGet page, official docs
- Cross-references: `[skill:dotnet-terminal-gui]` for full TUI alternative, `[skill:dotnet-system-commandline]` for scope boundary, `[skill:dotnet-cli-architecture]` for CLI structure, `[skill:dotnet-csharp-async-patterns]` for async patterns, `[skill:dotnet-csharp-dependency-injection]` for DI with Spectre.Console.Cli
- Latest stable Spectre.Console package

## Acceptance
- [ ] SKILL.md frontmatter has `name` and `description` (under 120 chars)
- [ ] Rich output patterns documented (markup, tables, trees, panels)
- [ ] Progress and prompts covered
- [ ] Live displays covered
- [ ] Spectre.Console.Cli framework covered (commands, settings, DI)
- [ ] Scope boundary with `[skill:dotnet-system-commandline]` documented
- [ ] Agent Gotchas section with console output pitfalls
- [ ] Prerequisites section with package requirements
- [ ] References section with GitHub repo and NuGet links
- [ ] Cross-references use `[skill:skill-name]` syntax
- [ ] No fn-N spec references in content
- [ ] Latest stable package version

## Verification
```bash
grep -c "## Agent Gotchas" skills/tui/dotnet-spectre-console/SKILL.md  # expect 1
grep -c "## Prerequisites" skills/tui/dotnet-spectre-console/SKILL.md  # expect 1
grep -c "## References" skills/tui/dotnet-spectre-console/SKILL.md  # expect 1
grep "dotnet-system-commandline" skills/tui/dotnet-spectre-console/SKILL.md  # expect scope boundary mention
grep -c "\[skill:" skills/tui/dotnet-spectre-console/SKILL.md  # expect >= 4
grep "description:" skills/tui/dotnet-spectre-console/SKILL.md | wc -c  # expect < 130
```

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
