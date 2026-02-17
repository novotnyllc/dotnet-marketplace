# fn-47-add-accessibility-skill-for-net-ui.1 Author dotnet-accessibility SKILL.md

## Description
Author `skills/ui-frameworks/dotnet-accessibility/SKILL.md` covering accessibility patterns across all .NET UI frameworks. Single cross-cutting skill with framework-specific sections.

**Size:** M
**Files:** `skills/ui-frameworks/dotnet-accessibility/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/ui-frameworks/dotnet-blazor/SKILL.md` for style
- Cross-platform principles section: semantic markup, keyboard navigation, focus management, color contrast
- Framework sections: Blazor (ARIA), MAUI (SemanticProperties), Uno (AutomationProperties), WPF/WinUI (AutomationPeer), TUI (screen reader notes)
- Testing tools section: Accessibility Insights, axe-core, VoiceOver, TalkBack
- Reference standards: WCAG 2.1/2.2 (but no legal advice)
- Reference: https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/accessibility

## Key context

- MAUI uses `SemanticProperties` (preferred) over legacy `AutomationProperties`
- Blazor uses standard HTML accessibility (ARIA, keyboard events, roles)
- WPF/WinUI use `AutomationPeer` and `AutomationProperties.Name`
- iOS/Android: VoiceOver and TalkBack integration via MAUI SemanticProperties
- TUI screen reader support is limited — be honest about platform constraints
## Acceptance
- [ ] SKILL.md exists at `skills/ui-frameworks/dotnet-accessibility/`
- [ ] Valid frontmatter with `name` and `description` (under 120 chars)
- [ ] Covers cross-platform accessibility principles
- [ ] Has framework-specific sections for Blazor, MAUI, Uno, WPF/WinUI, TUI
- [ ] Covers accessibility testing tools per platform
- [ ] References WCAG standards without providing legal advice
- [ ] Cross-reference syntax used for all related UI framework skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
