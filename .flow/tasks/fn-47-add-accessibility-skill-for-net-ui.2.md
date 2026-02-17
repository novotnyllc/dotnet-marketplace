# fn-47-add-accessibility-skill-for-net-ui.2 Integrate dotnet-accessibility into plugin registry and routing

## Description
Register `dotnet-accessibility` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references to/from all 6 UI framework skills.

**Size:** M (8 files: plugin.json + advisor + 6 UI framework skills)
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/ui-frameworks/dotnet-blazor/SKILL.md`, `skills/ui-frameworks/dotnet-maui/SKILL.md`, `skills/ui-frameworks/dotnet-uno-platform/SKILL.md`, `skills/ui-frameworks/dotnet-winui/SKILL.md`, `skills/ui-frameworks/dotnet-wpf/SKILL.md`, `skills/ui-frameworks/dotnet-tui-apps/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-accessibility]` cross-references in each UI framework skill
- Update `--projected-skills` in validate-skills.sh

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files.** Run integration tasks sequentially.
## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor`
- Add `[skill:dotnet-accessibility]` cross-references in each UI framework skill
- Update `--projected-skills` count in validation
## Acceptance
- [ ] plugin.json includes `skills/ui-frameworks/dotnet-accessibility`
- [ ] `dotnet-advisor` has routing entry for accessibility
- [ ] Cross-references added in all 6 UI framework skills
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
