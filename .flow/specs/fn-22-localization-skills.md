# fn-22: Localization Skills

## Problem/Goal
Add comprehensive internationalization and localization skill covering full i18n stack including .resx resources, modern alternatives (JSON resources, source generators), IStringLocalizer, date/number formatting, RTL support, pluralization, and UI framework integration.

## Dependencies
- **Hard**: fn-3 (Core C# and Language Patterns Skills) — provides foundational DI patterns used by IStringLocalizer registration
- **Soft**: fn-5 (UI Framework Skills) — framework-specific skills that fn-22 cross-references for deep integration patterns

## .NET Version Policy
- Baseline: net8.0 (localization APIs stable since .NET 5; IStringLocalizer since .NET Core 1.0)
- Version-gated: Note any .NET 10+ localization changes if discovered during research

## Scope Boundary Table

| Concern | Owner | Cross-ref |
|---------|-------|-----------|
| .resx resources, satellite assemblies, resource managers | fn-22 (`dotnet-localization`) | — |
| Modern alternatives (JSON resources, source generators) | fn-22 (`dotnet-localization`) | — |
| IStringLocalizer, IViewLocalizer, IHtmlLocalizer patterns | fn-22 (`dotnet-localization`) | — |
| Date/number/currency formatting (CultureInfo) | fn-22 (`dotnet-localization`) | — |
| RTL layout support patterns | fn-22 (`dotnet-localization`) | — |
| Pluralization engines and patterns | fn-22 (`dotnet-localization`) | — |
| Blazor localization (@inject IStringLocalizer, CultureProvider) | fn-22 subsection (overview + bridge) | [skill:dotnet-blazor-components] |
| MAUI localization (AppResources, x:Static) | fn-22 subsection (overview + bridge) | [skill:dotnet-maui-development] |
| Uno localization (.resw, x:Uid, UseLocalization()) | fn-22 subsection (overview + bridge) | [skill:dotnet-uno-platform] |
| WPF localization (LocBaml, resource dictionaries) | fn-22 subsection (overview + bridge) | [skill:dotnet-wpf-modern] |
| General DI patterns for IStringLocalizer registration | fn-3 | cross-ref only |

## Acceptance Checks
- [ ] `skills/localization/dotnet-localization/SKILL.md` exists with valid frontmatter (`name: dotnet-localization`, `description` ≤120 chars)
- [ ] SKILL.md contains sections for: .resx Resources, Modern Alternatives, IStringLocalizer, Date/Number Formatting, RTL Support, Pluralization
- [ ] SKILL.md contains UI framework integration sections for: Blazor, MAUI, Uno, WPF
- [ ] SKILL.md contains cross-references: `[skill:dotnet-blazor-components]`, `[skill:dotnet-maui-development]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-wpf-modern]`
- [ ] `validate-skills.sh` passes (exit 0)
- [ ] `validate-marketplace.sh` passes (exit 0)
- [ ] `plugin.json` includes `skills/localization/dotnet-localization` in skills array
- [ ] `dotnet-advisor` SKILL.md section 14 status updated from `planned` to entry present

## Task Decomposition

| Task | Deliverables | Files touched |
|------|-------------|---------------|
| fn-22.1 | Research findings (done-summary) | None (research only) |
| fn-22.2 | `dotnet-localization` SKILL.md, plugin.json registration, advisor catalog update | `skills/localization/dotnet-localization/SKILL.md` (new), `.claude-plugin/plugin.json` (edit), `skills/foundation/dotnet-advisor/SKILL.md` (edit) |

## Cross-reference Classification
- **Hard refs (must resolve)**: `[skill:dotnet-blazor-components]`, `[skill:dotnet-maui-development]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-wpf-modern]`
- **Soft refs (informational)**: `[skill:dotnet-configuration]`, `[skill:dotnet-di-registration]`

## Key Context
- Research current .NET localization best practices (community has evolved beyond just .resx)
- Source generator approaches may exist for compile-time resource validation
- Different UI frameworks have different localization integration patterns
- RTL and pluralization are often overlooked but critical for proper i18n
- Uno Platform already has localization patterns in `dotnet-uno-platform` (.resw, x:Uid, ILocalizationService). The fn-22 Uno subsection should provide architectural overview and cross-reference, not duplicate implementation detail
- Similarly, other UI framework skills may already contain localization subsections; fn-22 should bridge and cross-reference rather than duplicate
