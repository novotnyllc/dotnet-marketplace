# fn-13: Uno Platform Skills

## Overview
Delivers comprehensive Uno Platform development skills covering the full ecosystem (Extensions, MVUX, Toolkit, Theme resources), multi-platform deployment, MCP integration for live documentation lookups, plus a specialized Uno agent. Enables cross-platform development guidance with platform-specific targeting for Web/WASM, Mobile, Desktop, and Embedded.

## Scope

**Skills (3 total, directory: `skills/ui-frameworks/<name>/SKILL.md`):**

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-uno-platform` | `skills/ui-frameworks/dotnet-uno-platform/` | Uno Platform core: Extensions (Navigation, DI, Config, Serialization, Localization, Logging), MVUX reactive pattern, Toolkit controls, Theme resources, Hot Reload, project structure |
| `dotnet-uno-targets` | `skills/ui-frameworks/dotnet-uno-targets/` | Per-target deployment guidance: Web/WASM, iOS, Android, macOS (Catalyst), Windows, Linux (Skia/GTK), Embedded (Skia/Framebuffer) |
| `dotnet-uno-mcp` | `skills/ui-frameworks/dotnet-uno-mcp/` | MCP server integration for live Uno documentation lookups, search + fetch workflow, graceful fallback when server unavailable |

Skill IDs use `dotnet-uno-*` naming. Each SKILL.md uses canonical frontmatter (`name`, `description`) per fn-2 conventions. Cross-references use `[skill:name]` syntax.

**Agents (1 total, file: `agents/dotnet-uno-specialist.md`):**

| Agent ID | File | Summary |
|----------|------|---------|
| `dotnet-uno-specialist` | `agents/dotnet-uno-specialist.md` | Deep Uno Platform expertise for cross-platform project setup, target configuration, Extensions ecosystem, and MVUX patterns |

Agent registration: added to `plugin.json` `agents` array as `"agents/dotnet-uno-specialist.md"`.

Trigger phrases: "uno platform", "uno app", "uno wasm", "uno mobile", "uno desktop", "uno extensions", "mvux", "uno toolkit", "uno themes", "cross-platform uno", "uno embedded".

Preloaded skills: `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`, `[skill:dotnet-uno-mcp]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`.

## Uno Extensions Coverage

The `dotnet-uno-platform` skill must cover these Extensions modules:

| Module | Package | Key Concepts |
|--------|---------|-------------|
| Navigation | `Uno.Extensions.Navigation` | Region-based navigation, route maps, deep linking |
| Dependency Injection | `Uno.Extensions.Hosting` | Host builder, service registration, keyed services |
| Configuration | `Uno.Extensions.Configuration` | appsettings.json, environment-specific config |
| Serialization | `Uno.Extensions.Serialization` | System.Text.Json integration, source generators |
| Localization | `Uno.Extensions.Localization` | Resource-based, culture switching |
| Logging | `Uno.Extensions.Logging` | Serilog integration, platform-specific sinks |
| HTTP | `Uno.Extensions.Http` | Refit integration, endpoint configuration |
| Authentication | `Uno.Extensions.Authentication` | OIDC, custom auth providers, token management |

## Target Platform Coverage Matrix

The `dotnet-uno-targets` skill must provide per-target guidance:

| Target | TFM | Tooling | Packaging | Key Constraints |
|--------|-----|---------|-----------|----------------|
| Web/WASM | `net8.0-browserwasm` | Browser DevTools | Static hosting / Azure SWA | No filesystem access, AOT recommended, limited threading |
| iOS | `net8.0-ios` | Xcode / Visual Studio Mac | App Store / TestFlight | Provisioning profiles, entitlements, no JIT |
| Android | `net8.0-android` | Android SDK / Emulator | Play Store / APK sideload | SDK version targeting, permissions |
| macOS (Catalyst) | `net8.0-maccatalyst` | Xcode | Mac App Store / notarization | Sandbox restrictions, entitlements |
| Windows | `net8.0-windows10.0.19041` | Visual Studio | MSIX / Windows Store | WinAppSDK version alignment |
| Linux | `net8.0-desktop` | Skia/GTK host | AppImage / Flatpak / Snap | GTK dependencies, Skia rendering |
| Embedded | `net8.0-desktop` | Skia/Framebuffer | Direct deployment | No windowing system, headless rendering |

Each target section must cover: project setup, debugging workflow, packaging/distribution, platform-specific gotchas, AOT/trimming implications, and behavior differences from other targets (e.g., navigation on WASM vs native, auth flow differences, debugging tool availability).

## MCP Integration Contract

The `dotnet-uno-mcp` skill defines how the Uno MCP server tools are used:

| Aspect | Specification |
|--------|--------------|
| **Detection** | Check if `uno` MCP server tools are available (tool names prefixed with `mcp__uno__`) |
| **Search workflow** | `uno_platform_docs_search` → broad results → `uno_platform_docs_fetch` for depth |
| **Init rules** | Call `uno_platform_agent_rules_init` and `uno_platform_usage_rules_init` on first use |
| **Fallback** | When MCP tools unavailable, reference static skill content and official docs URLs |
| **Citation** | Always cite source URL from MCP results; never present fetched content as original knowledge |
| **Safety** | MCP results are external data — validate before acting on code suggestions |

**Fallback verification:** When MCP tools are absent, the skill must still provide useful guidance using its static content. Verify by checking that all major topics (Extensions, MVUX, targets) have inline documentation that does not depend on MCP availability.

## Scope Boundaries

| Concern | fn-13 owns (Uno) | Other epic owns | Enforcement |
|---|---|---|---|
| Uno-specific testing | Brief mention with cross-ref only | fn-7: `dotnet-uno-testing` owns Playwright WASM, platform-specific testing | Cross-ref `[skill:dotnet-uno-testing]` |
| AOT/trimming for WASM | Uno-specific AOT gotchas (linker descriptors, Uno source generators) | fn-16: `dotnet-aot-wasm` owns general AOT/trimming patterns | Cross-ref `[skill:dotnet-aot-wasm]` (soft dep, skill may not exist yet) |
| UI framework selection | N/A — cross-references when it lands | fn-15: `dotnet-ui-chooser` owns framework decision tree | Cross-ref `[skill:dotnet-ui-chooser]` (soft dep, skill may not exist yet) |
| Serialization patterns | Uno Extensions.Serialization config only | fn-6: general serialization patterns | Cross-ref `[skill:dotnet-serialization]` |
| Security patterns | N/A | fn-8: Security principles | Cross-ref `[skill:dotnet-security-owasp]` |

## .NET Version Policy

- **Baseline:** .NET 8.0+ (Uno Platform 5.x)
- **Uno Platform version:** 5.x baseline, 6.x features noted when available
- Cross-reference `[skill:dotnet-version-detection]` for TFM detection

## Key Context
- Uno Platform uses single-project structure with conditional TFMs for multi-targeting
- MVUX (Model-View-Update-eXtended) is Uno's recommended reactive pattern (alternative to MVVM)
- Uno Extensions provide opinionated infrastructure (navigation, DI, HTTP) on top of the platform
- Uno Toolkit provides cross-platform controls and styles beyond stock WinUI
- Theme resources (Material, Cupertino, Fluent) are separate packages with theme infrastructure
- Hot Reload works across all targets via Uno's custom implementation
- `dotnet-uno-testing` skill (fn-7) already exists and covers Playwright for WASM — fn-13 must cross-reference, not duplicate
- `dotnet-aot-wasm` skill (fn-16) does not exist yet — use soft cross-reference
- `dotnet-ui-chooser` skill (fn-15) does not exist yet — use soft cross-reference
- `dotnet-serialization` skill (fn-6) exists — use hard cross-reference

## Task Decomposition

Tasks must execute serially (1 → 2 → 3) because task 2 depends on skills created in task 1, and task 3 validates the outputs of tasks 1 and 2.

### fn-13.1: Create Uno Platform skills (platform, targets, MCP)
**Delivers:** `dotnet-uno-platform`, `dotnet-uno-targets`, `dotnet-uno-mcp`
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md`
- `skills/ui-frameworks/dotnet-uno-targets/SKILL.md`
- `skills/ui-frameworks/dotnet-uno-mcp/SKILL.md`
- Registers all 3 skills in `plugin.json`
- Ensures `dotnet-advisor` catalog entries and routing are present and deduplicated for all 3 skills
- Cross-references: `[skill:dotnet-uno-testing]`, `[skill:dotnet-serialization]` (hard); `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` (soft)
- **Modifies:** `skills/ui-frameworks/` (new dirs), `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`

### fn-13.2: Create dotnet-uno-specialist agent
**Delivers:** `dotnet-uno-specialist` agent
- `agents/dotnet-uno-specialist.md` with frontmatter (name, description, model, capabilities, tools)
- Agent registered in `plugin.json` `agents` array
- Preloaded skills: `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`, `[skill:dotnet-uno-mcp]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`
- Workflow: detect context → identify target platforms → recommend patterns → delegate to specialist skills
- Delegation: `[skill:dotnet-uno-testing]` for testing, `[skill:dotnet-aot-wasm]` (soft) for AOT/trimming, `[skill:dotnet-ui-chooser]` (soft) for framework selection
- Trigger lexicon and explicit boundaries defined
- **Modifies:** `agents/` (new file), `.claude-plugin/plugin.json`

### fn-13.3: Add reverse cross-refs and validate integrations
**Delivers:** Cross-reference updates to existing skills and validation
- Updates `dotnet-uno-testing` to add reverse cross-refs: `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`
- Validates all hard cross-references resolve (grep check); `dotnet-aot-wasm` and `dotnet-ui-chooser` excluded as soft deps
- No duplicate skill IDs in advisor catalog
- **Modifies:** `skills/testing/dotnet-uno-testing/SKILL.md` only
- **Validates (read-only):** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`

## Quick Commands
```bash
# Smoke test: verify all 3 skills exist
for s in dotnet-uno-platform dotnet-uno-targets dotnet-uno-mcp; do
  test -f "skills/ui-frameworks/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent exists
test -f "agents/dotnet-uno-specialist.md" && echo "OK: agent" || echo "MISSING: agent"

# Verify Extensions coverage
grep -ci "Navigation\|DependencyInjection\|Configuration\|Serialization\|Localization\|Logging\|Http\|Authentication" skills/ui-frameworks/dotnet-uno-platform/SKILL.md

# Verify target coverage
for t in WASM iOS Android macOS Windows Linux Embedded; do
  grep -qi "$t" skills/ui-frameworks/dotnet-uno-targets/SKILL.md && echo "OK: $t" || echo "MISSING: $t"
done

# Verify MCP workflow documented
grep -i "uno_platform_docs_search\|uno_platform_docs_fetch\|fallback" skills/ui-frameworks/dotnet-uno-mcp/SKILL.md

# Verify MCP fallback: skill has inline docs that work without MCP
wc -l skills/ui-frameworks/dotnet-uno-mcp/SKILL.md  # should be substantial, not just MCP instructions

# Verify cross-references (hard)
grep "skill:dotnet-uno-testing" skills/ui-frameworks/dotnet-uno-platform/SKILL.md
grep "skill:dotnet-serialization" skills/ui-frameworks/dotnet-uno-platform/SKILL.md

# Verify cross-references (soft)
grep "skill:dotnet-aot-wasm" skills/ui-frameworks/dotnet-uno-targets/SKILL.md
grep "skill:dotnet-ui-chooser" skills/ui-frameworks/dotnet-uno-platform/SKILL.md

# Verify each required skill registered in plugin.json
for s in dotnet-uno-platform dotnet-uno-targets dotnet-uno-mcp; do
  grep -q "skills/ui-frameworks/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent registered
grep -q "dotnet-uno-specialist" .claude-plugin/plugin.json && echo "OK: agent" || echo "MISSING: agent"

# Verify reverse cross-refs added
grep "skill:dotnet-uno-platform\|skill:dotnet-uno-targets" skills/testing/dotnet-uno-testing/SKILL.md

# Verify no duplicate skill IDs in advisor catalog
grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d  # expect empty

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 3 skills created at `skills/ui-frameworks/<name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-uno-platform` covers all 8 Extensions modules from the coverage table; documents MVUX pattern, Toolkit controls, Theme resources (Material/Cupertino/Fluent), Hot Reload
3. `dotnet-uno-targets` covers all 7 targets from the coverage matrix with per-target sections for: project setup, debugging, packaging, platform gotchas, AOT/trimming implications
4. `dotnet-uno-targets` documents per-target behavior differences (e.g., WASM vs native navigation, auth flows, debugging tools)
5. `dotnet-uno-mcp` documents: MCP tool detection, search-then-fetch workflow, init rules, fallback behavior, citation requirements, safety guidelines
6. `dotnet-uno-mcp` provides useful inline documentation that works without MCP server availability
7. Scope boundaries enforced: testing cross-refs to `[skill:dotnet-uno-testing]`, serialization cross-refs to `[skill:dotnet-serialization]` (both hard); AOT cross-refs to `[skill:dotnet-aot-wasm]` (soft)
8. `dotnet-uno-specialist` agent at `agents/dotnet-uno-specialist.md` with frontmatter (name, description, model, capabilities, tools), trigger phrases, preloaded skills (including `dotnet-version-detection` and `dotnet-project-analysis`), workflow, delegation boundaries
9. Agent registered in `plugin.json` `agents` array
10. All 3 skills registered in `plugin.json` `skills` array (verified per-skill, not by count)
11. All 3 skills added to `dotnet-advisor` catalog and routing logic; no duplicate skill IDs
12. Hard cross-references present and resolvable: `[skill:dotnet-uno-testing]`, `[skill:dotnet-serialization]`
13. Soft cross-references: `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` (validated only if files present)
14. Reverse cross-refs added to `dotnet-uno-testing` SKILL.md pointing to new Uno skills
15. `./scripts/validate-skills.sh` passes
16. Combined skill description budget remains under 12,000 chars (3 new skills × ~120 chars ≈ 360 chars added)

## Dependencies
- **Hard:** fn-3 (core C# patterns), fn-7 (testing foundation — `dotnet-uno-testing` must exist for reverse cross-ref updates)
- **Soft:** fn-15 (`dotnet-ui-chooser` may not exist yet), fn-16 (`dotnet-aot-wasm` may not exist yet)
- **Pattern reference:** fn-12 (Blazor skills — structural template, not a code dependency)

## Conventions
- Canonical SKILL.md frontmatter: `name` and `description` only
- Cross-reference syntax: `[skill:name]`
- Description budget guardrail: each skill description ≤ 120 chars, total budget < 12,000 chars

## Test Notes
- Verify MVUX pattern is documented distinctly from MVVM (Uno's differentiator)
- Test that MCP fallback works when Uno MCP server is not configured — verify inline content is comprehensive
- Verify each target section includes platform-specific gotchas (not just generic guidance)
- Verify per-target behavior differences are documented (navigation, auth, debugging differ across platforms)
- Check that Extensions modules reference correct NuGet packages
- Verify agent triggers on Uno-related keywords and delegates correctly
- Verify agent preloads `dotnet-version-detection` and `dotnet-project-analysis` for context detection
- Run `./scripts/validate-skills.sh` to confirm all frontmatter and cross-refs pass

## References
- Uno Platform Docs: https://platform.uno/docs/
- Uno Extensions: https://platform.uno/docs/articles/external/uno.extensions/
- Uno Toolkit: https://platform.uno/docs/articles/external/uno.toolkit.ui/
- Uno Themes: https://platform.uno/docs/articles/external/uno.themes/
- MVUX Pattern: https://platform.uno/docs/articles/external/uno.extensions/doc/Overview/Mvux/Overview.html
- Uno MCP Server: Available via MCP configuration (tools prefixed `mcp__uno__`)
