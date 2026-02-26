# fn-64-consolidate-131-skills-into-20-broad.4 Consolidate API and data skills: dotnet-api, dotnet-efcore

## Description
Create consolidated `dotnet-ui` and `dotnet-debugging` skill directories. Merge ~18 UI framework skills into `dotnet-ui` with companion files. Update `dotnet-debugging` to absorb `dotnet-windbg-debugging` content and its 16 reference/ files. Remove source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-ui/SKILL.md` + `references/*.md` (new), `skills/dotnet-debugging/SKILL.md` + `references/*.md` (updated), `.claude-plugin/plugin.json`, ~20 source skill dirs (delete)

## Approach

**dotnet-ui (~18 source skills):**
- Write SKILL.md: UI framework overview, framework decision tree, routing table, scope/out-of-scope, ToC
- Create `references/` dir. Expected companion files:
  - `references/blazor-patterns.md` — components, render modes, state management
  - `references/blazor-auth.md` — authentication flows, AuthorizeView
  - `references/blazor-testing.md` — bUnit patterns
  - `references/maui.md` — development, platform-specific, Xamarin migration
  - `references/maui-aot.md` — Native AOT on iOS/Catalyst
  - `references/maui-testing.md` — Appium patterns
  - `references/uno-platform.md` — setup, Extensions, MVUX, Toolkit, theming
  - `references/uno-targets.md` — deployment, target configuration
  - `references/uno-mcp.md` — MCP server integration
  - `references/uno-testing.md` — Playwright patterns
  - `references/desktop.md` — WPF modern, WinUI 3, WinForms
  - `references/wpf-migration.md` — WPF/WinForms to .NET 8+ migration
  - `references/accessibility.md` — cross-framework accessibility patterns
  - `references/localization.md` — .resx, cultures, resource management
  - `references/ui-chooser.md` — framework selection decision tree
  - (exact list per task .1 output)

**dotnet-debugging (~2 source skills):**
- Update existing SKILL.md or create new one with overview + ToC
- `dotnet-windbg-debugging` already has `reference/` dir with 16 files — rename to `references/` to match convention
- Absorb any other debugging-related content per task .1 map

## Key context

- `dotnet-ui-chooser` is a router skill (decision tree for framework selection) — becomes the SKILL.md routing table section
- `dotnet-uno-mcp` queries Uno MCP server — content goes in `references/uno-mcp.md`
- `dotnet-accessibility` is cross-cutting but primarily UI-relevant — place in dotnet-ui
- `dotnet-localization` is cross-cutting but UI-adjacent — place in dotnet-ui
- Each UI framework specialist agent (blazor, maui, uno) preloads from this group
## Approach

- Follow consolidation map from task .1
- `dotnet-api` SKILL.md: ASP.NET Core API development overview, minimal APIs vs controllers, security, validation, versioning
- `dotnet-efcore` SKILL.md: EF Core patterns, architecture, data access strategy selection
- Include architecture-adjacent skills per mapping (architecture-patterns, resilience, http-client, etc. — exact placement from task .1)
## Acceptance
- [ ] `skills/dotnet-ui/SKILL.md` exists with overview, framework decision tree, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-ui/references/` contains companion files for all UI frameworks
- [ ] `skills/dotnet-debugging/SKILL.md` exists (standalone per user requirement)
- [ ] `skills/dotnet-debugging/references/` has migrated windbg reference/ content (renamed to references/)
- [ ] All ~20 source UI/debugging skill directories deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on both SKILL.md files
- [ ] No content lost from source skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
