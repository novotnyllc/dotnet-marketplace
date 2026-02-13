# fn-12-blazor-skills.2 Create dotnet-blazor-specialist agent

## Description
Create the `dotnet-blazor-specialist` agent following the pattern established by `dotnet-architect.md` and `dotnet-csharp-concurrency-specialist.md`. The agent provides deep Blazor expertise and delegates to specialist skills.

### File targets
- `agents/dotnet-blazor-specialist.md` — agent definition with full frontmatter
- `.claude-plugin/plugin.json` — add to `agents` array

### Agent frontmatter schema
```yaml
name: dotnet-blazor-specialist
description: "Guides Blazor development across all hosting models (Server, WASM, Hybrid, Auto). Component design, state management, authentication, and render mode selection. Triggers on: blazor component, render mode, blazor auth, editform, blazor state."
model: sonnet
capabilities:
  - Analyze Blazor project structure and hosting model
  - Recommend render mode per component
  - Guide component architecture and state management
  - Advise on authentication patterns per hosting model
  - Assess AOT/trimming readiness for WASM
tools:
  - Read
  - Grep
  - Glob
  - Bash
```

### Preloaded skills
- `[skill:dotnet-version-detection]` — detect TFM for version-aware guidance
- `[skill:dotnet-project-analysis]` — understand solution structure and dependencies
- `[skill:dotnet-blazor-patterns]` — hosting models, render modes, AOT
- `[skill:dotnet-blazor-components]` — component architecture, state, JS interop
- `[skill:dotnet-blazor-auth]` — authentication across hosting models

### Workflow
1. **Detect context** — Run `[skill:dotnet-version-detection]` to determine TFM. Read project files via `[skill:dotnet-project-analysis]` to identify current hosting model and dependencies.
2. **Assess hosting model** — Identify render modes in use, check for Hybrid (MAUI WebView) vs Web App.
3. **Recommend patterns** — Based on hosting model and requirements, recommend component patterns, state management, and auth approach.
4. **Delegate** — `[skill:dotnet-blazor-testing]` for bUnit, `[skill:dotnet-playwright]` for E2E, `[skill:dotnet-api-security]` for auth backend, `[skill:dotnet-realtime-communication]` for standalone SignalR.

### Trigger lexicon
"blazor component", "blazor app", "render mode", "interactive server", "interactive webassembly", "interactive auto", "blazor auth", "editform", "blazor state", "blazor routing", "signalr blazor", "blazor hybrid", "blazor wasm"

### Explicit boundaries
- Does NOT own bUnit testing (delegates to `dotnet-blazor-testing`)
- Does NOT own API-level auth (delegates to `dotnet-api-security`)
- Does NOT own standalone SignalR patterns (delegates to `dotnet-realtime-communication`)
- Uses Bash only for read-only commands — never modify project files

## Acceptance
- [ ] Agent file at `agents/dotnet-blazor-specialist.md` with frontmatter (name, description, model, capabilities, tools)
- [ ] Preloaded skills section references: `dotnet-version-detection`, `dotnet-project-analysis`, `dotnet-blazor-patterns`, `dotnet-blazor-components`, `dotnet-blazor-auth`
- [ ] Workflow section with 4 steps (detect, assess, recommend, delegate)
- [ ] Trigger lexicon documented
- [ ] Delegation boundaries explicitly defined
- [ ] Agent registered in `plugin.json` `agents` array
- [ ] Agent follows pattern of `dotnet-architect.md` (frontmatter + preloaded skills + workflow + guidelines)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
