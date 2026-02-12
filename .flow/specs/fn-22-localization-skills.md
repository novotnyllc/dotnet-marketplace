# fn-22: Localization Skills

## Problem/Goal
Add comprehensive internationalization and localization skill covering full i18n stack including .resx resources, modern alternatives (JSON resources, source generators), IStringLocalizer, date/number formatting, RTL support, pluralization, and UI framework integration.

## Acceptance Checks
- [ ] `dotnet-localization` skill covers full i18n stack (.resx + modern alternatives, IStringLocalizer, formatting, RTL, pluralization)
- [ ] Skill covers UI framework integration (Blazor, MAUI, Uno, WPF)
- [ ] Research-based on current .NET community practices (Feb 2026)
- [ ] Cross-references to UI framework skills, architecture patterns

## Key Context
- Research current .NET localization best practices (community has evolved beyond just .resx)
- Source generator approaches may exist for compile-time resource validation
- Different UI frameworks have different localization integration patterns
- RTL and pluralization are often overlooked but critical for proper i18n
