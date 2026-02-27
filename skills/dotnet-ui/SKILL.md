---
name: dotnet-ui
description: Builds .NET UI applications across all frameworks. Covers Blazor (patterns, components, auth, testing), MAUI (development, AOT, testing), Uno Platform (core, targets, MCP, testing), WPF (modern and migration), WinUI 3, WinForms, accessibility, localization, and UI framework selection. Includes XAML, MVVM, render modes, and platform-specific deployment.
license: MIT
user-invocable: true
---

# dotnet-ui

## Overview

.NET UI development across Blazor, MAUI, Uno Platform, WPF, WinUI 3, and WinForms. This skill covers framework selection, component architecture, XAML patterns, MVVM, platform-specific deployment, accessibility, and localization. Each framework area has a dedicated companion file with deep guidance.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Blazor patterns | hosting model, render mode, routing, streaming, prerender | references/blazor-patterns.md |
| Blazor components | lifecycle, state, JS interop, EditForm, QuickGrid | references/blazor-components.md |
| Blazor auth | AuthorizeView, Identity UI, OIDC flows | references/blazor-auth.md |
| Blazor testing | bUnit, rendering, events, JS mocking | references/blazor-testing.md |
| MAUI development | project structure, XAML, MVVM, platform services | references/maui-development.md |
| MAUI AOT | iOS/Catalyst, Native AOT, trimming | references/maui-aot.md |
| MAUI testing | Appium, XHarness, platform validation | references/maui-testing.md |
| Uno Platform | Extensions, MVUX, Toolkit, Hot Reload | references/uno-platform.md |
| Uno targets | WASM, iOS, Android, macOS, Windows, Linux | references/uno-targets.md |
| Uno MCP | tool detection, search-then-fetch, init | references/uno-mcp.md |
| Uno testing | Playwright WASM, platform patterns | references/uno-testing.md |
| WPF modern | Host builder, MVVM Toolkit, Fluent theme | references/wpf-modern.md |
| WPF migration | WPF/WinForms to .NET 8+, UWP to WinUI | references/wpf-migration.md |
| WinUI | Windows App SDK, XAML, MSIX/unpackaged | references/winui.md |
| WinForms | high-DPI, dark mode, DI, modernization | references/winforms-basics.md |
| Accessibility | SemanticProperties, ARIA, AutomationPeer | references/accessibility.md |
| Localization | .resx, IStringLocalizer, pluralization, RTL | references/localization.md |
| UI chooser | framework selection decision tree | references/ui-chooser.md |

## Scope

- Blazor (Server, WASM, Hybrid, Auto) -- hosting models, render modes, components, auth, testing
- MAUI mobile/desktop -- project structure, XAML/MVVM, platform services, Native AOT, testing
- Uno Platform cross-platform -- Extensions, MVUX, Toolkit, target platforms, MCP integration, testing
- WPF on .NET 8+ -- modern patterns, Host builder, MVVM Toolkit, migration from .NET Framework
- WinUI 3 / Windows App SDK -- XAML patterns, MSIX packaging, UWP migration
- WinForms on .NET 8+ -- high-DPI, dark mode, DI, modernization
- Accessibility across all UI frameworks -- SemanticProperties, ARIA, AutomationPeer
- Localization -- .resx resources, IStringLocalizer, source generators, pluralization, RTL
- UI framework selection decision tree

## Out of scope

- Server-side auth middleware and API security configuration -- see [skill:dotnet-api]
- Non-UI testing strategy (unit, integration, E2E architecture) -- see [skill:dotnet-testing]
- Cross-framework UI test patterns (page objects, selectors) -- see [skill:dotnet-testing]
- Playwright browser automation (non-framework-specific) -- see [skill:dotnet-testing]
- Backend API patterns and architecture -- see [skill:dotnet-api]
- Native AOT compilation (non-MAUI) -- see [skill:dotnet-tooling]
- Console UI (Terminal.Gui, Spectre.Console) -- see [skill:dotnet-tooling]

## Companion Files

- `references/blazor-patterns.md` -- Hosting models, render modes, routing, streaming, prerendering, AOT-safe patterns
- `references/blazor-components.md` -- Lifecycle methods, state management, JS interop, EditForm, QuickGrid
- `references/blazor-auth.md` -- Login/logout flows, AuthorizeView, Identity UI, OIDC, role and policy auth
- `references/blazor-testing.md` -- bUnit component rendering, events, cascading params, JS interop mocking
- `references/maui-development.md` -- Project structure, XAML/MVVM patterns, Shell navigation, platform services
- `references/maui-aot.md` -- iOS/Catalyst Native AOT pipeline, size/startup gains, library compatibility
- `references/maui-testing.md` -- Appium 2.x device automation, XHarness, platform validation
- `references/uno-platform.md` -- Extensions ecosystem, MVUX pattern, Toolkit controls, Hot Reload
- `references/uno-targets.md` -- Per-target guidance for WASM, iOS, Android, macOS, Windows, Linux
- `references/uno-mcp.md` -- MCP tool detection, search-then-fetch workflow, init rules, fallback
- `references/uno-testing.md` -- Playwright for WASM, platform-specific test patterns, runtime heads
- `references/wpf-modern.md` -- Host builder, MVVM Toolkit, Fluent theme, performance, modern C#
- `references/wpf-migration.md` -- WPF/WinForms to .NET 8+, UWP to WinUI, Upgrade Assistant
- `references/winui.md` -- Windows App SDK, x:Bind, x:Load, MSIX/unpackaged, UWP migration
- `references/winforms-basics.md` -- High-DPI scaling, dark mode, DI patterns, modernization
- `references/accessibility.md` -- SemanticProperties, ARIA attributes, AutomationPeer, per-platform testing
- `references/localization.md` -- .resx resources, IStringLocalizer, source generators, pluralization, RTL
- `references/ui-chooser.md` -- Decision tree across Blazor, MAUI, Uno, WinUI, WPF, WinForms
