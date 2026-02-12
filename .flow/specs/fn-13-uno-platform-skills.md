# fn-13: Uno Platform Skills

## Problem/Goal
Add comprehensive Uno Platform skills covering full ecosystem (Extensions, MVUX, Toolkit, Theme resources), multi-platform deployment, and MCP integration for live documentation lookups. Enable dotnet-uno-specialist agent to guide cross-platform development with Uno.

## Acceptance Checks
- [ ] `dotnet-uno-platform` skill covers Extensions (Navigation, DI, Config, Serialization), MVUX, Toolkit, themes
- [ ] `dotnet-uno-targets` skill covers deployment by target: Web/WASM, Mobile, Desktop, Embedded
- [ ] `dotnet-uno-mcp` skill leverages Uno MCP server, works standalone if unavailable
- [ ] `dotnet-uno-specialist` agent configured with preloaded skills
- [ ] Cross-references to dotnet-ui-chooser, dotnet-aot-wasm, dotnet-uno-testing

## Key Context
- Uno Platform MCP server integration for live doc lookups
- Multi-platform targeting requires platform-specific guidance
- WASM target benefits from AOT compilation
- Skills must detect if Uno MCP is available and adapt accordingly
