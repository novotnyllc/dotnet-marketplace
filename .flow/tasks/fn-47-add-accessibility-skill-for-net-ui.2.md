# fn-47-add-accessibility-skill-for-net-ui.2 Integrate dotnet-accessibility into plugin registry and routing

<!-- Updated by plan-sync: fn-47-add-accessibility-skill-for-net-ui.1 used actual skill directory names, not short aliases; TUI skills are under skills/tui/ not skills/ui-frameworks/ -->
## Description
Register `dotnet-accessibility` in plugin.json, add routing entry in `dotnet-advisor`, and add `[skill:dotnet-accessibility]` cross-references to/from the UI framework and TUI skills that the new skill cross-references.

**Size:** M (11 files: plugin.json + advisor + 8 UI/TUI framework skills + validate-skills.sh)
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-components/SKILL.md`, `skills/ui-frameworks/dotnet-maui-development/SKILL.md`, `skills/ui-frameworks/dotnet-uno-platform/SKILL.md`, `skills/ui-frameworks/dotnet-winui/SKILL.md`, `skills/ui-frameworks/dotnet-wpf-modern/SKILL.md`, `skills/tui/dotnet-terminal-gui/SKILL.md`, `skills/tui/dotnet-spectre-console/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-accessibility]` cross-references in each of: `dotnet-blazor-patterns`, `dotnet-blazor-components`, `dotnet-maui-development`, `dotnet-uno-platform`, `dotnet-winui`, `dotnet-wpf-modern`, `dotnet-terminal-gui`, `dotnet-spectre-console`
- Update `--projected-skills` in validate-skills.sh

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files.** Run integration tasks sequentially.

## Key context from fn-47.1 implementation

The completed SKILL.md cross-references these skills: `[skill:dotnet-blazor-patterns]`, `[skill:dotnet-blazor-components]`, `[skill:dotnet-maui-development]`, `[skill:dotnet-winui]`, `[skill:dotnet-wpf-modern]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`, `[skill:dotnet-terminal-gui]`, `[skill:dotnet-spectre-console]`, `[skill:dotnet-ui-chooser]`. Add reciprocal `[skill:dotnet-accessibility]` cross-references to the 8 framework skills listed above (excluding `dotnet-uno-targets` and `dotnet-ui-chooser` which are chooser/target skills, not framework skills needing accessibility back-references).
## Acceptance
- [ ] plugin.json includes `skills/ui-frameworks/dotnet-accessibility`
- [ ] `dotnet-advisor` has routing entry for accessibility
- [ ] Cross-references added in all 8 framework skills: dotnet-blazor-patterns, dotnet-blazor-components, dotnet-maui-development, dotnet-uno-platform, dotnet-winui, dotnet-wpf-modern, dotnet-terminal-gui, dotnet-spectre-console
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
Registered dotnet-accessibility in plugin.json (127 skills), added routing entry in dotnet-advisor (catalog + Building UI section), added reciprocal [skill:dotnet-accessibility] cross-references in all 8 framework/TUI skills, and updated validate-skills.sh projected count to 127 with fail threshold bumped to 15360.
## Evidence
- Commits: 043ef872113b39221ddf2c76d54f5413e93c0099
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: