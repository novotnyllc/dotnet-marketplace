# fn-12: Blazor Skills

## Overview
Delivers comprehensive Blazor development skills covering all hosting models and render modes, plus a specialized Blazor agent. Covers component architecture, state management, authentication, and modern .NET 10/11 Blazor features with AOT awareness.

## Scope

**Skills (3 total, directory: `skills/ui-frameworks/<name>/SKILL.md`):**

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-blazor-patterns` | `skills/ui-frameworks/dotnet-blazor-patterns/` | Blazor hosting models, render modes, project setup, routing, SSR/streaming, AOT-safe patterns |
| `dotnet-blazor-components` | `skills/ui-frameworks/dotnet-blazor-components/` | Component architecture, state management, JS interop, EditForm validation, QuickGrid |
| `dotnet-blazor-auth` | `skills/ui-frameworks/dotnet-blazor-auth/` | Authentication/authorization across all hosting models: AuthorizeView, CascadingAuthenticationState, Identity UI, external providers |

Skill IDs use `dotnet-blazor-*` naming. Each SKILL.md uses canonical frontmatter (`name`, `description`) per fn-2 conventions. Cross-references use `[skill:name]` syntax.

**Agents (1 total, file: `agents/dotnet-blazor-specialist.md`):**

| Agent ID | File | Summary |
|----------|------|---------|
| `dotnet-blazor-specialist` | `agents/dotnet-blazor-specialist.md` | Deep Blazor expertise for component design, hosting model selection, state management, and auth patterns |

Agent registration: added to `plugin.json` `agents` array as `"agents/dotnet-blazor-specialist.md"`.

Trigger phrases: "blazor component", "blazor app", "render mode", "interactive server", "interactive webassembly", "blazor auth", "editform", "blazor state", "blazor routing", "signalr blazor".

Preloaded skills: `[skill:dotnet-blazor-patterns]`, `[skill:dotnet-blazor-components]`, `[skill:dotnet-blazor-auth]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`.

## Hosting Model & Render Mode Coverage Matrix

All three skills must address these models/modes where relevant:

| Model/Mode | Pattern | Description |
|---|---|---|
| Blazor Server | `InteractiveServer` | Server-side rendering with SignalR circuit |
| Blazor WebAssembly | `InteractiveWebAssembly` | Client-side .NET runtime in browser |
| Blazor Web App (Auto) | `InteractiveAuto` | Server on first load, WASM after download |
| Blazor Web App (SSR) | Static SSR | No interactivity, streaming rendering |
| Blazor Hybrid | Native + WebView | MAUI/WPF/WinForms host with Blazor UI |

Each skill must document per-mode behavior differences (e.g., auth flows differ between Server and WASM; JS interop timing differs; state persistence varies).

## Scope Boundaries

| Concern | fn-12 owns (Blazor) | Other epic owns | Enforcement |
|---|---|---|---|
| Auth UI patterns | AuthorizeView, CascadingAuthenticationState, Identity UI scaffolding, client-side token handling | fn-11: API-level auth (JWT, OAuth/OIDC, passkeys) | Cross-ref `[skill:dotnet-api-security]` |
| SignalR in Blazor | Blazor circuit management, Hub connection from components | fn-6: SignalR as standalone communication pattern | Cross-ref `[skill:dotnet-realtime-communication]` |
| bUnit testing | Brief mention with cross-ref only | fn-7: `dotnet-blazor-testing` owns bUnit patterns | Cross-ref `[skill:dotnet-blazor-testing]` |
| UI framework selection | N/A — cross-references when it lands | fn-15: `dotnet-ui-chooser` owns framework decision tree | Cross-ref `[skill:dotnet-ui-chooser]` (soft dep, skill may not exist yet) |
| E2E testing | N/A | fn-7: `dotnet-playwright` owns browser-based testing | Cross-ref `[skill:dotnet-playwright]` |
| OWASP security | N/A | fn-8: Security principles | Cross-ref `[skill:dotnet-security-owasp]` |

## AOT & Trimming Guidance

Skills must document AOT-safe patterns for Blazor WASM scenarios:
- Source-generator-first serialization (System.Text.Json source gen, not reflection)
- Trim-safe JS interop patterns (avoid dynamic dispatch)
- Linker configuration for preserving types used in components
- Anti-patterns: reflection-based DI, dynamic type loading, runtime code generation
- `[DynamicallyAccessedMembers]` annotations where reflection is unavoidable

## .NET Version Policy

- **Baseline:** .NET 8.0+ (Blazor Web App model introduced in .NET 8)
- **.NET 10 features** (stable): WebAssembly preloading, enhanced form validation, diagnostics middleware — document as available when `net10.0` TFM detected
- **.NET 11 preview features**: EnvironmentBoundary, Label/DisplayName, QuickGrid OnRowClick, SignalR ConfigureConnection, IHostedService in WASM — mark each as `<!-- net11-preview -->` with fallback guidance for net10.0. Each preview feature section must include a source link to the official announcement or documentation.

## Key Context
- No hosting model bias — present all options objectively with trade-off analysis
- Blazor Web App is the default template in .NET 8+ (replaces separate Server/WASM templates)
- Render modes can be set globally, per-page, or per-component
- Static SSR + streaming rendering are distinct from interactive modes
- Enhanced navigation and form handling in .NET 8+ affect all hosting models
- `dotnet-blazor-testing` skill (fn-7) already exists and covers bUnit — fn-12 must cross-reference, not duplicate
- `dotnet-realtime-communication` skill (fn-6) already exists and is complete — fn-12 covers only Blazor-specific SignalR circuit patterns
- `dotnet-ui-chooser` is referenced in advisor catalog but may not exist yet — use soft cross-reference

## Task Decomposition

Tasks are ordered and must execute serially (1 → 2 → 3) because later tasks depend on earlier deliverables and all modify shared files (`plugin.json`, advisor catalog).

### fn-12.1: Create Blazor skills (patterns, components, auth)
**Delivers:** `dotnet-blazor-patterns`, `dotnet-blazor-components`, `dotnet-blazor-auth`
- `skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md`
- `skills/ui-frameworks/dotnet-blazor-components/SKILL.md`
- `skills/ui-frameworks/dotnet-blazor-auth/SKILL.md`
- Registers all 3 skills in `plugin.json`
- Adds catalog entries and routing in `dotnet-advisor` for all 3 skills
- Cross-references: `[skill:dotnet-blazor-testing]`, `[skill:dotnet-realtime-communication]`, `[skill:dotnet-api-security]`, `[skill:dotnet-ui-chooser]` (soft), `[skill:dotnet-playwright]`

### fn-12.2: Create dotnet-blazor-specialist agent
**Delivers:** `dotnet-blazor-specialist` agent
- `agents/dotnet-blazor-specialist.md` with frontmatter (name, description, model, capabilities, tools)
- Agent registered in `plugin.json` `agents` array
- Preloaded skills: `[skill:dotnet-blazor-patterns]`, `[skill:dotnet-blazor-components]`, `[skill:dotnet-blazor-auth]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`
- Workflow: detect context → assess hosting model → recommend patterns → delegate to specialist skills
- Delegation: `[skill:dotnet-blazor-testing]` for bUnit, `[skill:dotnet-playwright]` for E2E, `[skill:dotnet-api-security]` for auth backend, `[skill:dotnet-realtime-communication]` for standalone SignalR
- Trigger lexicon and explicit boundaries defined

### fn-12.3: Integrate with existing testing and communication skills
**Delivers:** Cross-reference updates to existing skills
- Updates `dotnet-blazor-testing` to add reverse cross-refs: `[skill:dotnet-blazor-patterns]`, `[skill:dotnet-blazor-components]`
- Updates `dotnet-realtime-communication` to add Blazor cross-ref if not already present
- Validates all hard cross-references resolve (grep check); `dotnet-ui-chooser` excluded as soft dep
- No duplicate skill IDs in advisor catalog

**Note on shared files:** Tasks fn-12.1, fn-12.2, fn-12.3 all modify `.claude-plugin/plugin.json` and/or `skills/foundation/dotnet-advisor/SKILL.md`. Serial ordering (1 → 2 → 3) naturally serializes these edits.

## Quick Commands
```bash
# Smoke test: verify all 3 skills exist
for s in dotnet-blazor-patterns dotnet-blazor-components dotnet-blazor-auth; do
  test -f "skills/ui-frameworks/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent exists
test -f "agents/dotnet-blazor-specialist.md" && echo "OK: agent" || echo "MISSING: agent"

# Verify hosting model coverage
for s in dotnet-blazor-patterns dotnet-blazor-components dotnet-blazor-auth; do
  echo "=== $s ==="
  grep -ci "InteractiveServer\|InteractiveWebAssembly\|InteractiveAuto\|Static SSR\|Hybrid" "skills/ui-frameworks/$s/SKILL.md"
done

# Verify AOT patterns documented
grep -i "AOT\|trimming\|source.gen" skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md

# Verify .NET 11 preview items marked
grep "net11-preview" skills/ui-frameworks/dotnet-blazor-components/SKILL.md

# Verify .NET 11 preview items have source links
grep -A2 "net11-preview" skills/ui-frameworks/dotnet-blazor-components/SKILL.md | grep -c "http"

# Verify cross-references (explicit per-skill checks)
grep "skill:dotnet-blazor-testing" skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md
grep "skill:dotnet-realtime-communication" skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md
grep "skill:dotnet-api-security" skills/ui-frameworks/dotnet-blazor-auth/SKILL.md

# Verify each required skill registered in plugin.json
for s in dotnet-blazor-patterns dotnet-blazor-components dotnet-blazor-auth; do
  grep -q "skills/ui-frameworks/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent registered
grep -q "dotnet-blazor-specialist" .claude-plugin/plugin.json && echo "OK: agent" || echo "MISSING: agent"

# Verify reverse cross-refs added
grep "skill:dotnet-blazor-patterns\|skill:dotnet-blazor-components" skills/testing/dotnet-blazor-testing/SKILL.md

# Verify no duplicate skill IDs in advisor catalog
grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d  # expect empty

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 3 skills created at `skills/ui-frameworks/<name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-blazor-patterns` covers all 5 hosting models/render modes from the coverage matrix; documents routing, enhanced navigation, streaming rendering
3. `dotnet-blazor-components` covers component lifecycle, state management (cascading values, DI, browser storage), JS interop, EditForm validation, QuickGrid
4. `dotnet-blazor-auth` covers AuthorizeView, CascadingAuthenticationState, Identity UI scaffolding, role/policy-based auth, per-hosting-model auth flow differences
5. Each skill documents per-render-mode behavior differences where relevant
6. AOT-safe patterns documented: source-gen serialization, trim-safe JS interop, linker config, anti-patterns
7. .NET 11 preview features marked with `<!-- net11-preview -->` and each includes a source link to official documentation/announcement
8. `dotnet-blazor-specialist` agent at `agents/dotnet-blazor-specialist.md` with frontmatter (name, description, model, capabilities, tools), trigger phrases, preloaded skills (including `dotnet-version-detection` and `dotnet-project-analysis`), workflow, delegation boundaries
9. Agent registered in `plugin.json` `agents` array
10. All 3 skills registered in `plugin.json` `skills` array (verified per-skill, not by count)
11. All 3 skills added to `dotnet-advisor` catalog and routing logic; no duplicate skill IDs
12. Hard cross-references present and resolvable: `[skill:dotnet-blazor-testing]`, `[skill:dotnet-realtime-communication]`, `[skill:dotnet-api-security]`, `[skill:dotnet-playwright]`
13. Soft cross-reference: `[skill:dotnet-ui-chooser]` (may not exist yet; validated only if file present)
14. Reverse cross-refs added to `dotnet-blazor-testing` SKILL.md pointing to new Blazor skills
15. `./scripts/validate-skills.sh` passes
16. Combined skill description budget remains under 12,000 chars (3 new skills × ~120 chars ≈ 360 chars added)

## Dependencies
- **Hard:** fn-3 (core C# patterns), fn-6 (serialization/communication — `dotnet-realtime-communication` edited in fn-12.3), fn-7 (testing foundation — `dotnet-blazor-testing` must exist for reverse cross-ref updates)
- **Soft:** fn-11 (API development — `dotnet-api-security` referenced but not modified), fn-15 (`dotnet-ui-chooser` may not exist yet)

## Test Notes
- Verify no hosting model bias — each model presented with trade-offs, not recommendations
- Test that Blazor Web App (Auto) render mode is documented as the modern default template
- Verify auth skill distinguishes between server-side auth (cookie-based) and client-side auth (token-based)
- Check that JS interop patterns are AOT-safe (no reflection-based dispatch)
- Verify bUnit content is cross-referenced, not duplicated from `dotnet-blazor-testing`
- Validate agent triggers on Blazor-related keywords and delegates correctly
- Verify agent preloads `dotnet-version-detection` and `dotnet-project-analysis` for context detection
- Run `./scripts/validate-skills.sh` to confirm all frontmatter and cross-refs pass

## References
- Blazor Overview: https://learn.microsoft.com/en-us/aspnet/core/blazor/?view=aspnetcore-10.0
- Blazor Render Modes: https://learn.microsoft.com/en-us/aspnet/core/blazor/components/render-modes?view=aspnetcore-10.0
- Blazor Authentication: https://learn.microsoft.com/en-us/aspnet/core/blazor/security/?view=aspnetcore-10.0
- Blazor State Management: https://learn.microsoft.com/en-us/aspnet/core/blazor/state-management?view=aspnetcore-10.0
- Blazor JS Interop: https://learn.microsoft.com/en-us/aspnet/core/blazor/javascript-interoperability/?view=aspnetcore-10.0
- bUnit Documentation: https://bunit.dev/
- .NET AOT Deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
