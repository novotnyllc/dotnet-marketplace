# fn-22-localization-skills.2 Create comprehensive localization skill with UI framework integration

## Description
Create `skills/localization/dotnet-localization/SKILL.md` covering the full .NET i18n stack based on task 1 research findings. Register the skill in plugin.json and update the dotnet-advisor catalog. Skill must include core localization sections plus UI framework integration subsections that cross-reference existing framework skills.

## Acceptance
- [ ] `skills/localization/dotnet-localization/SKILL.md` created with valid frontmatter (`name: dotnet-localization`, `description` ≤120 chars)
- [ ] SKILL.md contains core sections: .resx Resources, Modern Alternatives (JSON/source generators), IStringLocalizer patterns, Date/Number Formatting, RTL Support, Pluralization
- [ ] SKILL.md contains UI framework integration sections: Blazor, MAUI, Uno, WPF
- [ ] SKILL.md contains cross-references: `[skill:dotnet-blazor-components]`, `[skill:dotnet-maui-development]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-wpf-modern]`
- [ ] UI framework subsections provide architectural overview and cross-reference, not duplicated implementation detail
- [ ] `.claude-plugin/plugin.json` updated: `skills/localization/dotnet-localization` added to skills array
- [ ] `skills/foundation/dotnet-advisor/SKILL.md` section 14 updated: localization entry status from planned to present
- [ ] `./scripts/validate-skills.sh` passes (exit 0)
- [ ] `./scripts/validate-marketplace.sh` passes (exit 0)
- [ ] `STRICT_REFS=1 ./scripts/validate-skills.sh` passes (exit 0) — all cross-references resolve

## Files Touched
- `skills/localization/dotnet-localization/SKILL.md` (new)
- `.claude-plugin/plugin.json` (edit — add to skills array)
- `skills/foundation/dotnet-advisor/SKILL.md` (edit — update catalog status)

## Done summary
Created comprehensive `dotnet-localization` SKILL.md covering .resx resources, modern alternatives (JSON, source generators for AOT), IStringLocalizer patterns, date/number/currency formatting, RTL support, pluralization engines (MessageFormat.NET, SmartFormat.NET), and UI framework integration subsections for Blazor, MAUI, Uno Platform, and WPF with cross-references to framework-specific skills. Registered in plugin.json and updated advisor catalog section 14 from `planned` to `implemented`.
## Evidence
- Commits: 66d3215a9e3b9c2ff36e4eb2e7d42f0c69e2b4a5, f6307a75925e9f2f3a8f288bc1b354614958a055
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, STRICT_REFS=1 ./scripts/validate-skills.sh
- PRs: