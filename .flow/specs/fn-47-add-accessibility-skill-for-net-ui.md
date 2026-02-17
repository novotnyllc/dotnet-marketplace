# fn-47 Add Accessibility Skill for .NET UI Frameworks

## Overview

Add a new `dotnet-accessibility` skill covering accessibility patterns across .NET UI frameworks. One cross-cutting skill with framework-specific sections. Covers Blazor, MAUI, and WinUI in depth; WPF, Uno, and TUI with brief guidance and cross-references.

**Visibility:** Implicit — auto-loaded by agents via advisor routing when accessibility context is detected. Not user-invocable (but may be loaded when users explicitly ask about accessibility).

## Scope

**In:** SKILL.md for `dotnet-accessibility` under `skills/ui-frameworks/`, plugin.json registration, advisor routing, cross-references to each UI framework skill.

**Out:** Modifying existing UI framework skills with inline accessibility content (they get cross-references only). Legal compliance advice (mention standards, do not provide legal guidance).

**Primary frameworks (in-depth):** Blazor (ARIA, keyboard nav), MAUI (SemanticProperties), WinUI (AutomationProperties, UI Automation).

**Secondary frameworks (brief + cross-ref):** WPF (AutomationPeer), Uno Platform (follows UWP patterns), TUI (screen reader limitations noted).

**Note:** This task is sized L due to covering 6 frameworks. Accept that it's larger than ideal M; scoping down to 3 in-depth + 3 brief keeps it manageable.

## Key Context

- MAUI: `SemanticProperties.Description`, `SemanticProperties.Hint`, `SemanticProperties.HeadingLevel` (preferred over legacy AutomationProperties)
- Blazor: Standard HTML ARIA attributes, `role`, `aria-label`, keyboard event handling
- WinUI: `AutomationProperties.Name`, UI Automation framework
- Uno: Follows UWP `AutomationProperties` pattern — brief section, cross-ref to WinUI
- TUI: Terminal screen reader support varies — be honest about platform constraints
- Standards to reference: WCAG 2.1/2.2 (no legal advice)
- Testing: Accessibility Insights (Windows), axe-core (web), VoiceOver (macOS/iOS), TalkBack (Android)
- Budget: target description ~90 chars. Total projected: 132 skills after batch.

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/ui-frameworks/dotnet-accessibility/SKILL.md` exists with valid frontmatter
- [ ] Covers cross-platform accessibility principles (semantic markup, keyboard nav, focus management, contrast)
- [ ] In-depth sections for Blazor, MAUI, WinUI
- [ ] Brief sections with cross-references for WPF, Uno, TUI
- [ ] Covers accessibility testing tools per platform
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from all 6 UI framework skills
- [ ] Integration task notes file contention with plugin.json/advisor shared files
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/accessibility
- https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview
- `skills/ui-frameworks/dotnet-blazor/SKILL.md`
- `skills/ui-frameworks/dotnet-maui/SKILL.md`
- `skills/ui-frameworks/dotnet-winui/SKILL.md`
- `skills/ui-frameworks/dotnet-wpf/SKILL.md`
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md`
- `skills/ui-frameworks/dotnet-tui-apps/SKILL.md`
