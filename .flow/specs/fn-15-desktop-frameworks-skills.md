# fn-15: Desktop Frameworks Skills

## Problem/Goal
Add skills for Windows desktop frameworks (WinUI, WPF, WinForms) including modern .NET Core patterns, migration guidance, and decision support. Enable agents to guide framework selection and modernization.

## Acceptance Checks
- [ ] `dotnet-winui` skill covers WinUI 3 development patterns for Windows desktop
- [ ] `dotnet-wpf-modern` skill covers WPF on .NET Core with MVVM Toolkit and modern patterns
- [ ] `dotnet-wpf-migration` skill provides context-dependent migration (WinUI for Windows-only, Uno for cross-platform)
- [ ] `dotnet-winforms-basics` skill covers WinForms on .NET Core basics plus high-level migration tips
- [ ] `dotnet-ui-chooser` skill updated with desktop framework decision tree
- [ ] Cross-references between all desktop skills and dotnet-ui-chooser

## Key Context
- WPF/WinForms on .NET Core are modernized but Windows-only
- WinUI 3 is modern Windows-native framework
- Migration paths depend on cross-platform requirements
- dotnet-ui-chooser must incorporate desktop framework selection logic
