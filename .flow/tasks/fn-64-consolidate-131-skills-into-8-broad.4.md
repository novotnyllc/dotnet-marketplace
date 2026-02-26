# fn-64.4 Consolidate dotnet-ui + dotnet-debugging (~20 source skills)

## Description
Create consolidated `dotnet-ui` and `dotnet-debugging` skill directories. Merge ~18 UI framework skills into `dotnet-ui` with companion files. Create `dotnet-debugging` by absorbing `dotnet-windbg-debugging` content and its 16 reference/ files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-ui/SKILL.md` + `references/*.md` (new), `skills/dotnet-debugging/SKILL.md` + `references/*.md` (new), ~20 source skill dirs (delete)

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
- Create new SKILL.md with overview + ToC
- Rename `dotnet-windbg-debugging/reference/` to `dotnet-debugging/references/` (singular → plural convention)
- Absorb any other debugging-related content per task .1 map
- **Cross-reference repair**: all out-of-scope references in WinDbg content (e.g., `dotnet-profiling`, `dotnet-gc-memory`) must be remapped to the new 8-skill names (e.g., `[skill:dotnet-tooling]` with "read references/performance.md" hints). No `[skill:old-name]` allowed.

## Key context

- `dotnet-ui-chooser` is a router skill (decision tree for framework selection) — becomes the SKILL.md routing table section
- `dotnet-uno-mcp` queries Uno MCP server — content goes in `references/uno-mcp.md`
- `dotnet-accessibility` is cross-cutting but primarily UI-relevant — place in dotnet-ui
- `dotnet-localization` is cross-cutting but UI-adjacent — place in dotnet-ui
- Each UI framework specialist agent (blazor, maui, uno) preloads from this group
- `reference/` → `references/` rename: grep for `/reference/` path assumptions in scripts/tests before renaming

## Acceptance
- [ ] `skills/dotnet-ui/SKILL.md` exists with overview, framework decision tree, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-ui/references/` contains companion files for all UI frameworks
- [ ] `skills/dotnet-debugging/SKILL.md` exists (standalone per user requirement)
- [ ] `skills/dotnet-debugging/references/` has migrated windbg content (renamed from `reference/` to `references/`)
- [ ] All cross-references in debugging content remapped to 8-skill names (no `[skill:old-name]`)
- [ ] All ~20 source UI/debugging skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter on both SKILL.md files
- [ ] No content lost from source skills

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
