# fn-15-desktop-frameworks-skills.1 Create desktop framework skills (WinUI, WPF, WinForms)

## Description
Create three desktop framework skills: `dotnet-winui`, `dotnet-wpf-modern`, and `dotnet-winforms-basics`. Each skill covers modern .NET 8+ patterns for the respective Windows desktop framework.

**Delivers:**
- `skills/ui-frameworks/dotnet-winui/SKILL.md` — WinUI 3 / Windows App SDK patterns
- `skills/ui-frameworks/dotnet-wpf-modern/SKILL.md` — WPF on .NET 8+ with Host builder, MVVM Toolkit
- `skills/ui-frameworks/dotnet-winforms-basics/SKILL.md` — WinForms on .NET 8+ basics, high-DPI, dark mode

**Modifies:**
- `skills/ui-frameworks/` (3 new directories with SKILL.md files only)
- Does NOT modify `plugin.json` or `dotnet-advisor` — task 3 owns all registration

**Content requirements per epic spec:**
- `dotnet-winui`: 7 topics from WinUI Content Coverage table (Project Setup, XAML Patterns, MVVM, Packaging, Windows Integration, UWP Migration, Agent Gotchas)
- `dotnet-wpf-modern`: 6 topics from WPF Modern Content Coverage table (.NET 8+ Differences, MVVM Toolkit, Performance, Modern C#, Theming, Agent Gotchas)
- `dotnet-winforms-basics`: 6 topics from WinForms Basics Content Coverage table (.NET 8+ Differences, High-DPI, Dark Mode, When to Use, Modernization Tips, Agent Gotchas)

**Cross-references:**
- Hard: `[skill:dotnet-ui-testing-core]` for desktop testing
- Soft: `[skill:dotnet-native-aot]` (may not exist yet), `[skill:dotnet-ui-chooser]` (created in task 2)

**Conventions:**
- Canonical frontmatter: `name` and `description` only
- Description ≤ 120 chars each
- Agent Gotchas section in each skill
- `[skill:name]` cross-reference syntax throughout

## Acceptance
- [ ] `skills/ui-frameworks/dotnet-winui/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/ui-frameworks/dotnet-wpf-modern/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/ui-frameworks/dotnet-winforms-basics/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-winui` covers all 7 topics: Project Setup, XAML Patterns, MVVM, Packaging, Windows Integration, UWP Migration, Agent Gotchas
- [ ] `dotnet-winui` documents both MSIX and unpackaged (`WindowsPackageType=None`) deployment
- [ ] `dotnet-wpf-modern` covers all 6 topics: .NET 8+ Differences, MVVM Toolkit, Performance, Modern C#, Theming, Agent Gotchas
- [ ] `dotnet-wpf-modern` documents Host builder / DI pattern
- [ ] `dotnet-winforms-basics` covers all 6 topics: .NET 8+ Differences, High-DPI, Dark Mode, When to Use, Modernization Tips, Agent Gotchas
- [ ] `dotnet-winforms-basics` documents dark mode as experimental with .NET 11 finalization target
- [ ] Hard cross-refs: `[skill:dotnet-ui-testing-core]` present in each skill
- [ ] Soft cross-refs: `[skill:dotnet-native-aot]`, `[skill:dotnet-ui-chooser]` present (with "may not exist yet" qualifier)
- [ ] Each skill description ≤ 120 chars
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
