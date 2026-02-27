# fn-64.4 Consolidate dotnet-ui + dotnet-debugging (19 source skills)
<!-- Updated by plan-sync: fn-64.1 mapped 18 UI + 1 debugging = 19 total, not ~20 -->

## Description
Create consolidated `dotnet-ui` and `dotnet-debugging` skill directories. Merge 18 UI framework skills into `dotnet-ui` with companion files. Create `dotnet-debugging` by renaming `dotnet-windbg-debugging` (single source skill) and its 16 reference/ files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-ui/SKILL.md` + `references/*.md` (new), `skills/dotnet-debugging/SKILL.md` + `references/*.md` (new), 19 source skill dirs (delete)

## Approach

**dotnet-ui (~18 source skills):**
- Write SKILL.md: UI framework overview, framework decision tree, routing table, scope/out-of-scope, ToC
- Create `references/` dir with one companion file per source skill (18 files total, per consolidation map from .1):
  - `references/blazor-patterns.md` — hosting model, render mode, routing, streaming
  - `references/blazor-components.md` — lifecycle, state, JS interop, EditForm, QuickGrid
  - `references/blazor-auth.md` — AuthorizeView, Identity UI, OIDC flows
  - `references/blazor-testing.md` — bUnit rendering, events, JS mocking
  - `references/maui-development.md` — project structure, XAML, MVVM, platform (merge existing examples.md)
  - `references/maui-aot.md` — iOS/Catalyst Native AOT, size/startup gains
  - `references/maui-testing.md` — Appium, XHarness, platform validation
  - `references/uno-platform.md` — Extensions, MVUX, Toolkit, Hot Reload
  - `references/uno-targets.md` — WASM, iOS, Android, macOS, Windows, Linux
  - `references/uno-mcp.md` — tool detection, search-then-fetch, init
  - `references/uno-testing.md` — Playwright WASM, platform patterns
  - `references/wpf-modern.md` — Host builder, MVVM Toolkit, Fluent theme
  - `references/wpf-migration.md` — WPF/WinForms to .NET 8+, UWP to WinUI
  - `references/winui.md` — Windows App SDK, XAML, MSIX/unpackaged
  - `references/winforms-basics.md` — high-DPI, dark mode, DI, modernization
  - `references/accessibility.md` — SemanticProperties, ARIA, AutomationPeer
  - `references/localization.md` — .resx, IStringLocalizer, pluralization, RTL
  - `references/ui-chooser.md` — framework selection decision tree

**dotnet-debugging (1 source skill: `dotnet-windbg-debugging`):**
<!-- Updated by plan-sync: fn-64.1 mapped only 1 source skill to dotnet-debugging, not ~2 -->
- Rename skill directory from `dotnet-windbg-debugging` to `dotnet-debugging`
- Create new SKILL.md with overview + ToC (rewrite frontmatter: name `dotnet-debugging`, description ~350 chars)
- Rename `dotnet-windbg-debugging/reference/` to `dotnet-debugging/references/` (singular -> plural convention)
- **Cross-reference repair**: all out-of-scope references in WinDbg content (e.g., `dotnet-profiling`, `dotnet-gc-memory`) must be remapped to the new 8-skill names (e.g., `[skill:dotnet-tooling]` with "read references/profiling.md" or "read references/gc-memory.md" hints). No `[skill:old-name]` allowed.

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
- [ ] All 19 source UI/debugging skill directories deleted (18 UI + 1 debugging)
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter on both SKILL.md files
- [ ] No content lost from source skills

## Done summary
Consolidated 18 UI framework skills into skills/dotnet-ui/ (SKILL.md with routing table + 18 references/ companion files) and renamed dotnet-windbg-debugging to skills/dotnet-debugging/ (with reference/ to references/ rename). All cross-references remapped to new 8-skill names. Deleted all 19 source skill directories. plugin.json not modified (deferred to task .9).
## Evidence
- Commits: fdf5fc0, 0e485b6, 3eaba9f
- Tests: ./scripts/validate-skills.sh
- PRs: