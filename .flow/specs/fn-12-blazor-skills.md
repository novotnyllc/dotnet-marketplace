# fn-12: Blazor Skills

## Problem/Goal
Add comprehensive Blazor development skills covering all hosting models (Server, WASM, Hybrid, Blazor Web App) with modern patterns for components, state management, and authentication. Enable dotnet-blazor-specialist agent to guide Blazor development without bias toward any single hosting model.

## Acceptance Checks
- [ ] `dotnet-blazor-patterns` skill covers all hosting models (Server, WASM, Hybrid, Auto/Streaming)
- [ ] `dotnet-blazor-components` skill covers component architecture, state management, JS interop, forms, validation
- [ ] `dotnet-blazor-auth` skill covers authentication/authorization across all hosting models
- [ ] `dotnet-blazor-specialist` agent configured with preloaded skills and delegation triggers
- [ ] Skills integrate with existing testing skills (bUnit references)
- [ ] Cross-references to dotnet-ui-chooser, dotnet-realtime-communication, dotnet-api-security

## Key Context
- Modern .NET 10 Blazor: WebAssembly preloading, form validation, diagnostics
- .NET 11 Preview 1: EnvironmentBoundary, Label/DisplayName, QuickGrid OnRowClick, SignalR ConfigureConnection, IHostedService in WASM
- No hosting model bias - present all options objectively
- Skills must be AOT-aware for Blazor WASM scenarios
