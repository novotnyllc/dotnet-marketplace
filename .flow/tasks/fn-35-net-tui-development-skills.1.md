# fn-35-net-tui-development-skills.1 Create Terminal.Gui TUI skill

## Description
Create skills/tui/dotnet-terminal-gui/SKILL.md covering Terminal.Gui for building full terminal user interfaces. Cover layout system, views, menus, dialogs, event handling, color themes, cross-platform considerations. Include Agent Gotchas, Prerequisites, and References sections per canonical SKILL.md structure.

**Size:** M
**Files:** skills/tui/dotnet-terminal-gui/SKILL.md

## Approach
- Frontmatter: `name: dotnet-terminal-gui`, `description` under 120 chars
- Application lifecycle: Application.Init(), Application.Run(), Application.Shutdown()
- Layout: Computed layout (Pos/Dim), Absolute positioning
- Core views: Window, FrameView, Label, TextField, TextView, Button, ListView, TableView
- Menus and dialogs: MenuBar, StatusBar, Dialog, MessageBox
- Event handling: key bindings, mouse events
- Color themes and styling
- Cross-platform: Windows/macOS/Linux terminal compatibility
- Agent Gotchas: TUI-specific pitfalls (threading, terminal state cleanup, layout gotchas)
- Prerequisites: Terminal.Gui NuGet package, net8.0+ baseline
- References: GitHub repo, NuGet page, official docs
- Cross-references: `[skill:dotnet-spectre-console]` for rich output alternative, `[skill:dotnet-csharp-async-patterns]` for async TUI patterns, `[skill:dotnet-native-aot]` for AOT considerations
- Latest stable Terminal.Gui package

## Acceptance
- [ ] SKILL.md frontmatter has `name` and `description` (under 120 chars)
- [ ] Application lifecycle documented
- [ ] Layout system (Computed + Absolute) covered
- [ ] Core views with usage patterns
- [ ] Menus and dialogs covered
- [ ] Event handling and key bindings
- [ ] Agent Gotchas section with TUI-specific pitfalls
- [ ] Prerequisites section with package requirements
- [ ] References section with GitHub repo and NuGet links
- [ ] Cross-references use `[skill:skill-name]` syntax
- [ ] No fn-N spec references in content
- [ ] Latest stable package version

## Verification
```bash
grep -c "## Agent Gotchas" skills/tui/dotnet-terminal-gui/SKILL.md  # expect 1
grep -c "## Prerequisites" skills/tui/dotnet-terminal-gui/SKILL.md  # expect 1
grep -c "## References" skills/tui/dotnet-terminal-gui/SKILL.md  # expect 1
grep -c "\[skill:" skills/tui/dotnet-terminal-gui/SKILL.md  # expect >= 2
grep "description:" skills/tui/dotnet-terminal-gui/SKILL.md | wc -c  # expect < 130
```

## Done summary
Created Terminal.Gui v2 TUI skill (skills/tui/dotnet-terminal-gui/SKILL.md) covering instance-based application lifecycle, unified Pos/Dim layout system, core views (Window, Label, TextField, TextView, Button, ListView, CheckBox, RadioGroup, DatePicker, NumericUpDown, ColorPicker), MenuBar with MenuBarItem, StatusBar with v2 Shortcut API, Dialog/MessageBox/FileDialog, command-pattern key bindings, TrueColor themes with ConfigurationManager, adornments, cross-platform compatibility, and 11 Agent Gotchas.
## Evidence
- Commits: d390a641b7f08f0d9e16e03f1fa6b1eef6ed3b0b, 934e891bcdff91ad491af2e33fb8cdf956b1cb1d
- Tests: ./scripts/validate-skills.sh
- PRs: