# .NET TUI Development Skills

## Overview
Add skills for building terminal user interfaces (TUI) in .NET. Two major frameworks exist: Terminal.Gui (Miguel de Icaza) and Spectre.Console (Patrik Svensson). Both are actively maintained and serve different use cases.

## Scope
- **Terminal.Gui skill** — Full TUI framework: windows, menus, dialogs, views, layout (Computed vs Absolute), event handling, color themes, mouse support. Cross-platform (Windows/macOS/Linux).
- **Spectre.Console skill** — Rich console output: tables, trees, progress bars, prompts, markup, live displays, canvas, charts. Also covers Spectre.Console.Cli for command-line parsing.
- Consider whether to create one combined TUI skill or two separate ones (budget impact: 1 skill = ~120 chars, 2 = ~240 chars)

**Package version policy**: Use latest stable versions of Terminal.Gui and Spectre.Console.

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Terminal.Gui skill covering layout, views, event handling, themes
- [ ] Spectre.Console skill covering rich output, prompts, tables, CLI
- [ ] Cross-references between TUI skills and `[skill:dotnet-csharp-async-patterns]` for async TUI patterns
- [ ] No fn-N spec references
- [ ] Budget constraint respected
- [ ] All validation commands pass

## References
- Terminal.Gui GitHub — https://github.com/gui-cs/Terminal.Gui
- Spectre.Console GitHub — https://github.com/spectreconsole/spectre.console
