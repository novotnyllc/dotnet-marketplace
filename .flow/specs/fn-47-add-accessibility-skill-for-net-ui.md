# fn-47 Add Accessibility Skill for .NET UI Frameworks

## Overview

Add a new `dotnet-accessibility` skill covering accessibility patterns across .NET UI frameworks. One cross-cutting skill with framework-specific sections rather than per-framework additions (avoids budget bloat and touching 6+ completed epics).

## Scope

**In:** SKILL.md for `dotnet-accessibility` under `skills/ui-frameworks/`, plugin.json registration, advisor routing, cross-references to each UI framework skill.

**Out:** Modifying existing UI framework skills with inline accessibility content (they get cross-references only). Legal compliance advice (mention standards, do not provide legal guidance).

**Frameworks covered:** Blazor (ARIA, keyboard nav), MAUI (SemanticProperties), Uno Platform (AutomationProperties), WPF/WinUI (AutomationPeer, UI Automation), Terminal UI (screen reader considerations for Terminal.Gui/Spectre.Console).

## Key Context

- MAUI: `SemanticProperties.Description`, `SemanticProperties.Hint`, `SemanticProperties.HeadingLevel` (preferred over legacy AutomationProperties)
- Blazor: Standard HTML ARIA attributes, `role`, `aria-label`, keyboard event handling
- WPF/WinUI: `AutomationPeer`, `AutomationProperties.Name`, UI Automation framework
- Uno: Follows UWP `AutomationProperties` pattern
- TUI: Terminal screen reader support varies by platform; Terminal.Gui has some support
- Standards to reference: WCAG 2.1/2.2, but no legal compliance advice
- Testing: Accessibility Insights (Windows), axe-core (web), VoiceOver (macOS/iOS), TalkBack (Android)

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/ui-frameworks/dotnet-accessibility/SKILL.md` exists with valid frontmatter
- [ ] Covers cross-platform accessibility principles (semantic markup, keyboard nav, focus management, contrast)
- [ ] Has framework-specific sections for Blazor, MAUI, Uno, WPF/WinUI, TUI
- [ ] Covers accessibility testing tools per platform
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-blazor`, `dotnet-maui`, `dotnet-uno-platform`, `dotnet-winui`, `dotnet-wpf`, `dotnet-tui-apps`
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/accessibility
- https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview
- `skills/ui-frameworks/dotnet-blazor/SKILL.md` (Blazor cross-ref)
- `skills/ui-frameworks/dotnet-maui/SKILL.md` (MAUI cross-ref)
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md` (Uno cross-ref)
- `skills/ui-frameworks/dotnet-winui/SKILL.md` (WinUI cross-ref)
- `skills/ui-frameworks/dotnet-wpf/SKILL.md` (WPF cross-ref)
- `skills/ui-frameworks/dotnet-tui-apps/SKILL.md` (TUI cross-ref)
