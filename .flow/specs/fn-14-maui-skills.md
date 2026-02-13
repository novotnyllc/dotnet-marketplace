# fn-14: MAUI Skills

## Overview
Delivers MAUI development skills covering modern patterns with honest current-state assessment, Native AOT on iOS/Mac Catalyst, and .NET 11 improvements (XAML source gen, CoreCLR for Android). Includes a specialist agent for platform-specific guidance. Skills present migration options (WinUI for Windows-only, Uno for cross-platform) and document known caveats.

## Scope

**Skills (2 total, directory: `skills/ui-frameworks/<name>/SKILL.md`):**

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-maui-development` | `skills/ui-frameworks/dotnet-maui-development/` | MAUI patterns, current-state assessment, platform-specific guidance, .NET 11 XAML source gen, CoreCLR for Android |
| `dotnet-maui-aot` | `skills/ui-frameworks/dotnet-maui-aot/` | MAUI Native AOT on iOS/Mac Catalyst: size/startup improvements, library compatibility, opt-out mechanisms |

Skill IDs use `dotnet-maui-*` naming. Each SKILL.md uses canonical frontmatter (`name`, `description`) per fn-2 conventions. Cross-references use `[skill:name]` syntax.

**Agents (1 total, file: `agents/dotnet-maui-specialist.md`):**

| Agent ID | File | Summary |
|----------|------|---------|
| `dotnet-maui-specialist` | `agents/dotnet-maui-specialist.md` | Deep MAUI expertise including platform-specific issues, migration guidance, and AOT optimization |

Agent registration: added to `plugin.json` `agents` array as `"agents/dotnet-maui-specialist.md"`.

Trigger phrases: "maui", "maui app", "maui xaml", "maui native aot", "maui ios", "maui android", "maui catalyst", "maui windows", "xamarin migration", "maui hot reload", "maui aot".

Preloaded skills: `[skill:dotnet-maui-development]`, `[skill:dotnet-maui-aot]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`.

## MAUI Development Content Coverage

The `dotnet-maui-development` skill must cover these topics:

| Topic | Key Concepts |
|-------|-------------|
| Project Structure | Single-project with platform folders, conditional compilation, resource management |
| XAML Patterns | XAML data binding, MVVM with CommunityToolkit.Mvvm, Shell navigation, ContentPage lifecycle |
| Platform Services | Platform-specific code via partial classes, conditional compilation, dependency injection |
| Current State (Feb 2026) | Production-ready with caveats: VS 2026 Android toolchain bugs, iOS 26.x compatibility gaps |
| Growth Metrics | 36% YoY user growth, 557% community PR increase, strong enterprise traction |
| Migration Options | WinUI for Windows-only, Uno Platform for web/Linux targets, when to choose each |
| .NET 11: XAML Source Gen | Default in .NET 11 Preview 1, replaces XAMLC, AOT-friendly, revert with `<MauiXamlInflator>XamlC</MauiXamlInflator>` |
| .NET 11: CoreCLR for Android | Default runtime for Android Release builds, replaces Mono, opt out with `<UseMonoRuntime>true</UseMonoRuntime>` |
| `dotnet run` Device Selection | .NET 11: interactive target framework and device selection |
| Hot Reload | XAML Hot Reload, C# Hot Reload limitations per platform |

## MAUI AOT Content Coverage

The `dotnet-maui-aot` skill must cover:

| Topic | Key Concepts |
|-------|-------------|
| iOS/Mac Catalyst AOT | Native AOT compilation pipeline, publish profile, entitlements |
| Size Reduction | Up to 50% app size reduction vs interpreter mode |
| Startup Improvement | Up to 50% faster cold startup |
| Library Compatibility | Many libraries don't support AOT — compatibility matrix, common failures |
| Opt-out Mechanisms | `<PublishAot>false</PublishAot>`, per-assembly trimming overrides |
| Trimming Interplay | Trim warnings, RD.xml for reflection, source generator alternatives |
| Testing AOT Builds | Verifying AOT builds work on device, common AOT-only failures |

## Scope Boundaries

| Concern | fn-14 owns (MAUI) | Other epic owns | Enforcement |
|---|---|---|---|
| MAUI-specific testing | Brief mention with cross-ref only | fn-7: `dotnet-maui-testing` owns Appium, XHarness, platform-specific testing | Cross-ref `[skill:dotnet-maui-testing]` (hard) |
| General Native AOT patterns | MAUI-specific AOT (iOS/Catalyst pipeline) | fn-16: `dotnet-native-aot` owns general AOT patterns and architecture | Cross-ref `[skill:dotnet-native-aot]` (soft dep, skill may not exist yet) |
| WASM AOT | N/A (MAUI doesn't target WASM) | fn-16: `dotnet-aot-wasm` | Cross-ref `[skill:dotnet-aot-wasm]` (soft dep, skill may not exist yet) |
| UI framework selection | Presents migration options only | fn-15: `dotnet-ui-chooser` owns framework decision tree | Cross-ref `[skill:dotnet-ui-chooser]` (soft dep, skill may not exist yet) |

## .NET Version Policy

- **Baseline:** .NET 8.0+ (MAUI ships with .NET 8+)
- **.NET 11 Preview 1:** XAML source gen default, CoreCLR for Android default, `dotnet run` device selection
- Cross-reference `[skill:dotnet-version-detection]` for TFM detection

## Key Context
- Production-ready with caveats (36% YoY growth, 557% community PR increase)
- .NET 11 Preview 1: XAML source gen default, CoreCLR for Android default
- Native AOT: 50% size/startup improvement on iOS/Mac Catalyst, library compatibility gaps
- Skills must present migration options (WinUI for Windows-only, Uno for cross-platform)
- `dotnet-maui-testing` skill (fn-7) already exists — fn-14 must cross-reference, not duplicate
- `dotnet-native-aot` skill (fn-16) does not exist yet — use soft cross-reference
- `dotnet-ui-chooser` skill (fn-15) does not exist yet — use soft cross-reference

## Task Decomposition

Tasks must execute serially (1 → 2 → 3) because task 2 depends on skills created in task 1, and task 3 validates the outputs of tasks 1 and 2.

### fn-14.1: Create MAUI development and AOT skills
**Delivers:** `dotnet-maui-development`, `dotnet-maui-aot`
- `skills/ui-frameworks/dotnet-maui-development/SKILL.md`
- `skills/ui-frameworks/dotnet-maui-aot/SKILL.md`
- Registers both skills in `plugin.json`
- Verifies existing `dotnet-advisor` catalog entries for both skills; ensures entries match and are deduplicated
- Cross-references: `[skill:dotnet-maui-testing]` (hard); `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` (soft)
- .NET 11 content (XAML source gen, CoreCLR for Android, `dotnet run` device selection) included in skill content
- **Modifies:** `skills/ui-frameworks/` (new dirs), `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md` (verify/deduplicate)

### fn-14.2: Create dotnet-maui-specialist agent
**Delivers:** `dotnet-maui-specialist` agent
- `agents/dotnet-maui-specialist.md` with frontmatter (name, description, model, capabilities, tools)
- Agent registered in `plugin.json` `agents` array
- Preloaded skills: `[skill:dotnet-maui-development]`, `[skill:dotnet-maui-aot]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`
- Workflow: detect context → identify platform targets → recommend patterns → delegate to specialist skills
- Delegation: `[skill:dotnet-maui-testing]` for testing, `[skill:dotnet-native-aot]` (soft) for general AOT, `[skill:dotnet-ui-chooser]` (soft) for framework selection
- Trigger lexicon and explicit boundaries defined
- **Modifies:** `agents/` (new file), `.claude-plugin/plugin.json`

### fn-14.3: Add reverse cross-refs and validate integrations
**Delivers:** Cross-reference updates to existing skills and validation
- Updates `dotnet-maui-testing` to add reverse cross-refs: `[skill:dotnet-maui-development]`, `[skill:dotnet-maui-aot]`
- Validates all hard cross-references resolve (grep check); `dotnet-native-aot`, `dotnet-aot-wasm`, `dotnet-ui-chooser` excluded as soft deps
- No duplicate skill IDs in advisor catalog
- **Modifies:** `skills/testing/dotnet-maui-testing/SKILL.md` only
- **Validates (read-only):** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`

## Quick Commands
```bash
# Smoke test: verify both skills exist
for s in dotnet-maui-development dotnet-maui-aot; do
  test -f "skills/ui-frameworks/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent exists
test -f "agents/dotnet-maui-specialist.md" && echo "OK: agent" || echo "MISSING: agent"

# Verify MAUI development content coverage
grep -ci "XAML\|MVVM\|Shell\|Hot Reload\|CoreCLR\|source gen" skills/ui-frameworks/dotnet-maui-development/SKILL.md

# Verify AOT content coverage
grep -ci "Native AOT\|size reduction\|startup\|library compat\|trimming" skills/ui-frameworks/dotnet-maui-aot/SKILL.md

# Verify .NET 11 content in development skill
grep -i "MauiXamlInflator\|UseMonoRuntime\|dotnet run" skills/ui-frameworks/dotnet-maui-development/SKILL.md

# Verify cross-references (hard)
grep "skill:dotnet-maui-testing" skills/ui-frameworks/dotnet-maui-development/SKILL.md

# Verify cross-references (soft)
grep "skill:dotnet-native-aot\|skill:dotnet-aot-wasm\|skill:dotnet-ui-chooser" skills/ui-frameworks/dotnet-maui-aot/SKILL.md

# Verify skills registered in plugin.json
for s in dotnet-maui-development dotnet-maui-aot; do
  grep -q "skills/ui-frameworks/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent registered
grep -q "dotnet-maui-specialist" .claude-plugin/plugin.json && echo "OK: agent" || echo "MISSING: agent"

# Verify reverse cross-refs added
grep "skill:dotnet-maui-development\|skill:dotnet-maui-aot" skills/testing/dotnet-maui-testing/SKILL.md

# Verify no duplicate skill IDs in advisor catalog
grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d  # expect empty

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. Both skills created at `skills/ui-frameworks/<name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-maui-development` covers all 10 topics from the Development Content Coverage table
3. `dotnet-maui-development` includes .NET 11 content: XAML source gen default, CoreCLR for Android default, `dotnet run` device selection
4. `dotnet-maui-development` provides honest current-state assessment (VS 2026 issues, iOS gaps, growth metrics)
5. `dotnet-maui-development` presents migration options (WinUI, Uno Platform) with decision guidance
6. `dotnet-maui-aot` covers all 7 topics from the AOT Content Coverage table
7. `dotnet-maui-aot` documents opt-out mechanisms (`PublishAot`, `UseMonoRuntime`, `MauiXamlInflator`)
8. Scope boundaries enforced: testing cross-refs to `[skill:dotnet-maui-testing]` (hard); AOT cross-refs to `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]` (soft)
9. `dotnet-maui-specialist` agent at `agents/dotnet-maui-specialist.md` with frontmatter (name, description, model, capabilities, tools), trigger phrases, preloaded skills (4 total), workflow, delegation boundaries
10. Agent registered in `plugin.json` `agents` array
11. Both skills registered in `plugin.json` `skills` array (verified per-skill)
12. Both skills present in `dotnet-advisor` catalog and routing logic; no duplicate skill IDs
13. Hard cross-references present and resolvable: `[skill:dotnet-maui-testing]`
14. Soft cross-references: `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` (validated only if files present)
15. Reverse cross-refs added to `dotnet-maui-testing` SKILL.md pointing to new MAUI skills
16. `./scripts/validate-skills.sh` passes
17. Combined skill description budget remains under 12,000 chars (2 new skills × ~120 chars ≈ 240 chars added)

## Dependencies
- **Hard:** fn-3 (core C# patterns), fn-7 (testing foundation — `dotnet-maui-testing` must exist for reverse cross-ref updates)
- **Soft:** fn-15 (`dotnet-ui-chooser` may not exist yet), fn-16 (`dotnet-native-aot`, `dotnet-aot-wasm` may not exist yet)
- **Pattern reference:** fn-13 (Uno Platform skills — structural template, not a code dependency)

## Conventions
- Canonical SKILL.md frontmatter: `name` and `description` only
- Cross-reference syntax: `[skill:name]`
- Description budget guardrail: each skill description ≤ 120 chars, total budget < 12,000 chars

## Test Notes
- Verify MAUI current-state assessment is honest (mentions caveats, not just positive spin)
- Verify migration options are presented objectively (not just "use MAUI")
- Verify .NET 11 content documents both the new defaults AND opt-out mechanisms
- Verify AOT skill covers library compatibility gaps realistically
- Verify agent triggers on MAUI-related keywords and delegates correctly
- Verify agent preloads `dotnet-version-detection` and `dotnet-project-analysis` for context detection
- Run `./scripts/validate-skills.sh` to confirm all frontmatter and cross-refs pass

## References
- .NET MAUI Docs: https://learn.microsoft.com/en-us/dotnet/maui/
- .NET 11 Preview 1: https://devblogs.microsoft.com/dotnet/dotnet-11-preview-1/
- MAUI Native AOT: https://learn.microsoft.com/en-us/dotnet/maui/deployment/nativeaot
- CommunityToolkit.Mvvm: https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/
- MAUI Shell: https://learn.microsoft.com/en-us/dotnet/maui/fundamentals/shell/
