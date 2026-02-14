# fn-15: Desktop Frameworks Skills

## Overview
Delivers skills for Windows desktop frameworks (WinUI 3, WPF, WinForms) covering modern .NET Core patterns, migration guidance from .NET Framework, and a comprehensive UI framework decision tree. Enables agents to guide framework selection and desktop app modernization. Does NOT include a dedicated agent — routing goes through `dotnet-advisor`.

## Scope

**Skills (5 total, directory: `skills/ui-frameworks/<name>/SKILL.md`):**

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-winui` | `skills/ui-frameworks/dotnet-winui/` | WinUI 3 / Windows App SDK: project setup, XAML patterns, MSIX packaging, unpackaged deployment, UWP migration |
| `dotnet-wpf-modern` | `skills/ui-frameworks/dotnet-wpf-modern/` | WPF on .NET 8+: Host builder / DI, MVVM Toolkit, performance gains, modern C# patterns, what changed from .NET Framework |
| `dotnet-wpf-migration` | `skills/ui-frameworks/dotnet-wpf-migration/` | Context-dependent migration: WPF .NET Framework → .NET 8+, WPF → WinUI (Windows-only), WPF → Uno (cross-platform) |
| `dotnet-winforms-basics` | `skills/ui-frameworks/dotnet-winforms-basics/` | WinForms on .NET 8+: high-DPI, dark mode (experimental), modern DI patterns, migration tips from .NET Framework |
| `dotnet-ui-chooser` | `skills/ui-frameworks/dotnet-ui-chooser/` | Framework selection decision tree: Web (Blazor), cross-platform (MAUI, Uno, Avalonia), Windows-only (WinUI, WPF, WinForms) |

Skill IDs use `dotnet-*` naming. Each SKILL.md uses canonical frontmatter (`name`, `description`) per fn-2 conventions. Cross-references use `[skill:name]` syntax.

**Agents:** None. Desktop frameworks are niche enough that `dotnet-advisor` routing suffices. The advisor catalog already has entries for all 5 skills.

## WinUI Content Coverage

The `dotnet-winui` skill must cover these topics:

| Topic | Key Concepts |
|-------|-------------|
| Project Setup | Windows App SDK, `<UseWinUI>true</UseWinUI>`, TFM `net8.0-windows10.0.19041.0` |
| XAML Patterns | WinUI XAML (not UWP XAML), compiled bindings (`x:Bind`), `x:Load` for deferred loading |
| MVVM | CommunityToolkit.Mvvm integration, same patterns as MAUI |
| Packaging | MSIX packaging vs unpackaged deployment, `<WindowsPackageType>None</WindowsPackageType>` |
| Windows Integration | App lifecycle, notifications, widgets (Windows 11), taskbar integration |
| UWP Migration | API mapping, namespace changes (`Windows.UI.*` → `Microsoft.UI.*`), UWP .NET 9 preview path |
| Agent Gotchas | UWP vs WinUI namespace confusion, packaged vs unpackaged differences, Windows version requirements |

## WPF Modern Content Coverage

The `dotnet-wpf-modern` skill must cover these topics:

| Topic | Key Concepts |
|-------|-------------|
| .NET 8+ Differences | Host builder pattern, DI, new project template, nullable reference types, implicit usings |
| MVVM Toolkit | CommunityToolkit.Mvvm integration with WPF, source generators, ObservableProperty |
| Performance | Hardware-accelerated rendering improvements, startup time, trimming readiness |
| Modern C# | Records for ViewModels, pattern matching in converters, primary constructors in services |
| Theming | Fluent theme (WPF .NET 9+), custom themes, system theme detection |
| Agent Gotchas | Don't mix .NET Framework and .NET 8+ WPF patterns, don't use obsolete APIs (BitmapEffect, etc.) |

## WinForms Basics Content Coverage

The `dotnet-winforms-basics` skill must cover these topics:

| Topic | Key Concepts |
|-------|-------------|
| .NET 8+ Differences | New project template, DI via Host builder, nullable reference types |
| High-DPI | `ApplicationHighDpiMode.PerMonitorV2`, DPI-unaware designer mode (.NET 9+), scaling gotchas |
| Dark Mode | `Application.SetColorMode(SystemColorMode.Dark)` (experimental in .NET 9, targeting finalization in .NET 11) |
| When to Use | Rapid prototyping, internal tools, simple CRUD forms, Windows-only utilities |
| Modernization Tips | Add DI, use async patterns, convert to .NET 8+ for support |
| Agent Gotchas | Don't recommend WinForms for new customer-facing apps, don't use deprecated APIs |

## UI Chooser Content Coverage

The `dotnet-ui-chooser` skill must cover these decision factors:

| Factor | Frameworks Compared |
|--------|-------------------|
| Target Platforms | Web: Blazor; Mobile+Desktop: MAUI, Uno; Windows-only: WinUI, WPF, WinForms; All: Uno |
| Team Expertise | .NET-only: all; WinUI XAML: WinUI, Uno; WPF XAML: WPF; Web: Blazor; Mobile: MAUI |
| UI Complexity | Rich native: WinUI, WPF; Web-style: Blazor; Simple forms: WinForms |
| Performance Needs | Native rendering: WinUI, WPF; AOT: MAUI (iOS), Uno (WASM); GPU: WPF |
| Migration Path | UWP → WinUI; Xamarin → MAUI; WPF → WinUI or Uno; Web → Blazor |

Decision tree format: structured "if target X, consider Y" guidance, not a recommendation engine. The skill must be objective and present trade-offs for each framework.

## WPF Migration Content Coverage

The `dotnet-wpf-migration` skill must cover these migration paths:

| Migration Path | Key Concepts |
|---------------|-------------|
| WPF .NET Framework → .NET 8+ | `dotnet-upgrade-assistant`, API compatibility, NuGet package updates, breaking changes |
| WPF → WinUI 3 | When to migrate (Windows-only, need modern UI), API mapping, XAML differences |
| WPF → Uno Platform | When to migrate (cross-platform needed), API compatibility via WinUI surface, Uno Extensions |
| WinForms → .NET 8+ | `dotnet-upgrade-assistant`, designer compatibility, NuGet updates |
| UWP → WinUI 3 | Namespace changes, app model differences, Windows App SDK migration |
| UWP → Uno Platform | When cross-platform is needed from UWP, cross-ref `[skill:dotnet-uno-platform]` |
| Decision Matrix | Context-dependent: Windows-only → WinUI; cross-platform → Uno; staying Windows → WPF .NET 8+ |

## Scope Boundaries

| Concern | fn-15 owns | Other epic owns | Enforcement |
|---|---|---|---|
| WinUI-specific patterns | Full WinUI 3 skill coverage | N/A | Self-contained |
| WPF modern patterns | WPF on .NET 8+ patterns | N/A | Self-contained |
| WPF legacy (.NET Framework) | Migration guidance only | Out of scope (legacy) | Migration skill handles boundary |
| WinForms patterns | Basics and modernization tips | N/A | Self-contained |
| UI framework selection | Decision tree across all frameworks | Individual framework skills own depth | Cross-refs to all framework skills |
| MAUI patterns | Cross-reference only | fn-14: `dotnet-maui-development` | Cross-ref `[skill:dotnet-maui-development]` (hard) |
| Uno patterns | Cross-reference only | fn-13: `dotnet-uno-platform` | Cross-ref `[skill:dotnet-uno-platform]` (hard) |
| Blazor patterns | Cross-reference only | fn-12: `dotnet-blazor-patterns` | Cross-ref `[skill:dotnet-blazor-patterns]` (hard) |
| Desktop testing | Brief mention with cross-ref only | fn-7: testing skills | Cross-ref `[skill:dotnet-ui-testing-core]` (hard) |
| AOT / trimming | Brief mention per-framework | fn-16: `dotnet-native-aot` | Cross-ref `[skill:dotnet-native-aot]` (soft dep, may not exist yet) |

## .NET Version Policy

- **Baseline:** .NET 8.0+ (current LTS)
- **WinUI 3:** Windows App SDK 1.6+ (current stable), TFM `net8.0-windows10.0.19041.0`
- **WPF/WinForms:** TFM `net8.0-windows` (no Windows SDK version needed)
- **.NET 9 features:** WPF Fluent theme, WinForms dark mode (experimental), UWP .NET 9 preview
- **.NET 11 targets:** WinForms visual styles finalization
- Cross-reference `[skill:dotnet-version-detection]` for TFM detection

## Key Context
- WinUI 3 is the modern Windows-native framework (replacement for UWP)
- WPF is mature, Windows-only, but modernized on .NET Core with DI, Host builder
- WinForms is simplest, Windows-only, suitable for internal tools and rapid prototyping
- `dotnet-ui-chooser` is the cross-cutting decision tree skill referenced by MAUI, Uno, Blazor skills as a soft dep
- Migration guidance must be context-dependent (not "always migrate to X")
- No agent needed — `dotnet-advisor` routes desktop queries via catalog entries
- Existing advisor catalog entries: `[skill:dotnet-winui]`, `[skill:dotnet-wpf-modern]`, `[skill:dotnet-wpf-migration]`, `[skill:dotnet-winforms-basics]`, `[skill:dotnet-ui-chooser]`
- Cross-platform frameworks (MAUI, Uno, Blazor) already have skills — fn-15 only cross-references them

## Task Decomposition

Tasks must execute serially (1 → 2 → 3) because task 2 depends on skills created in task 1, and task 3 validates the outputs of tasks 1 and 2.

### fn-15.1: Create desktop framework skills (WinUI, WPF, WinForms)
**Delivers:** `dotnet-winui`, `dotnet-wpf-modern`, `dotnet-winforms-basics`
- `skills/ui-frameworks/dotnet-winui/SKILL.md`
- `skills/ui-frameworks/dotnet-wpf-modern/SKILL.md`
- `skills/ui-frameworks/dotnet-winforms-basics/SKILL.md`
- Cross-references: `[skill:dotnet-ui-testing-core]` (hard); `[skill:dotnet-native-aot]` (soft)
- Each skill includes Agent Gotchas section
- Does NOT modify `plugin.json` or `dotnet-advisor` — task 3 owns all registration
- **Modifies:** `skills/ui-frameworks/` (3 new dirs with SKILL.md files only)

### fn-15.2: Create dotnet-ui-chooser decision tree skill
**Delivers:** `dotnet-ui-chooser`
- `skills/ui-frameworks/dotnet-ui-chooser/SKILL.md`
- Covers all framework categories: Web (Blazor), cross-platform (MAUI, Uno, Avalonia), Windows-only (WinUI, WPF, WinForms)
- Decision tree format with structured guidance, trade-off tables
- Cross-references: `[skill:dotnet-blazor-patterns]`, `[skill:dotnet-maui-development]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-winui]`, `[skill:dotnet-wpf-modern]`, `[skill:dotnet-winforms-basics]` (all hard)
- Does NOT modify `plugin.json` or `dotnet-advisor` — task 3 owns all registration
- **Modifies:** `skills/ui-frameworks/` (1 new dir with SKILL.md file only)

### fn-15.3: Register skills, create migration guidance, and validate integrations
**Delivers:** `dotnet-wpf-migration` skill + all plugin.json registrations + cross-reference validation
- `skills/ui-frameworks/dotnet-wpf-migration/SKILL.md`
- Registers ALL 5 fn-15 skills in `plugin.json` (sole owner of plugin.json changes for this epic)
- Verifies/deduplicates ALL 5 `dotnet-advisor` catalog entries (sole owner of advisor changes for this epic)
- Migration paths: WPF .NET Framework → .NET 8+, WPF → WinUI, WPF → Uno, WinForms → .NET 8+, UWP → WinUI, UWP → Uno (cross-ref), Decision Matrix
- Cross-references: `[skill:dotnet-winui]`, `[skill:dotnet-wpf-modern]`, `[skill:dotnet-uno-platform]`, `[skill:dotnet-winforms-basics]`, `[skill:dotnet-ui-chooser]` (all hard)
- Validates all hard cross-references across fn-15 skills resolve (grep check)
- Validates no duplicate skill IDs in advisor catalog
- Updates existing framework skills to strengthen `[skill:dotnet-ui-chooser]` reference (replace soft-dep placeholder with hard ref where applicable)
- **Modifies:** `skills/ui-frameworks/` (1 new dir), `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`
- **Updates (cross-refs only):** `skills/ui-frameworks/dotnet-maui-development/SKILL.md`, `skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md`, `skills/ui-frameworks/dotnet-uno-platform/SKILL.md`
- **Validates (read-only):** all fn-15 skills, `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`

## Quick Commands
```bash
# Smoke test: verify all 5 skills exist
for s in dotnet-winui dotnet-wpf-modern dotnet-wpf-migration dotnet-winforms-basics dotnet-ui-chooser; do
  test -f "skills/ui-frameworks/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Verify WinUI content coverage
grep -ci "WinUI\|Windows App SDK\|MSIX\|UseWinUI\|x:Bind" skills/ui-frameworks/dotnet-winui/SKILL.md

# Verify WPF modern content coverage
grep -ci "Host builder\|MVVM Toolkit\|ObservableProperty\|Fluent theme\|net8.0-windows" skills/ui-frameworks/dotnet-wpf-modern/SKILL.md

# Verify WinForms content coverage
grep -ci "High.DPI\|dark mode\|SetColorMode\|PerMonitorV2" skills/ui-frameworks/dotnet-winforms-basics/SKILL.md

# Verify UI chooser covers all frameworks
for f in Blazor MAUI "Uno Platform" WinUI WPF WinForms; do
  grep -qi "$f" skills/ui-frameworks/dotnet-ui-chooser/SKILL.md && echo "OK: $f" || echo "MISSING: $f"
done

# Verify migration paths documented
grep -ci "upgrade.assistant\|WinUI.*migration\|Uno.*migration\|namespace.*Microsoft.UI" skills/ui-frameworks/dotnet-wpf-migration/SKILL.md

# Verify cross-references (hard) in ui-chooser
for s in dotnet-blazor-patterns dotnet-maui-development dotnet-uno-platform dotnet-winui dotnet-wpf-modern dotnet-winforms-basics; do
  grep -q "skill:$s" skills/ui-frameworks/dotnet-ui-chooser/SKILL.md && echo "OK: $s" || echo "MISSING: $s"
done

# Verify cross-references (soft)
grep "skill:dotnet-native-aot" skills/ui-frameworks/dotnet-winui/SKILL.md

# Verify each skill registered in plugin.json
for s in dotnet-winui dotnet-wpf-modern dotnet-wpf-migration dotnet-winforms-basics dotnet-ui-chooser; do
  grep -q "skills/ui-frameworks/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify no duplicate skill IDs in advisor catalog
grep -oP 'skill:[a-z-]+' skills/foundation/dotnet-advisor/SKILL.md | sort | uniq -d  # expect empty

# Verify reverse cross-refs added to existing skills
grep "skill:dotnet-ui-chooser" skills/ui-frameworks/dotnet-maui-development/SKILL.md
grep "skill:dotnet-ui-chooser" skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md
grep "skill:dotnet-ui-chooser" skills/ui-frameworks/dotnet-uno-platform/SKILL.md

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 5 skills created at `skills/ui-frameworks/<name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-winui` covers all 7 topics from the WinUI Content Coverage table
3. `dotnet-winui` documents both MSIX and unpackaged deployment modes
4. `dotnet-wpf-modern` covers all 6 topics from the WPF Modern Content Coverage table
5. `dotnet-wpf-modern` documents Host builder / DI pattern for modern WPF
6. `dotnet-winforms-basics` covers all 6 topics from the WinForms Content Coverage table
7. `dotnet-winforms-basics` documents experimental dark mode with caveats
8. `dotnet-ui-chooser` covers all 5 decision factors from the UI Chooser Content Coverage table
9. `dotnet-ui-chooser` presents trade-offs objectively (not recommending one framework)
10. `dotnet-wpf-migration` covers all 7 migration paths from the WPF Migration Content Coverage table
11. `dotnet-wpf-migration` provides context-dependent guidance (not "always use X")
12. Scope boundaries enforced: MAUI, Uno, Blazor cross-refs are hard; AOT cross-ref is soft
13. All 5 skills registered in `plugin.json` `skills` array (verified per-skill, not by count)
14. All 5 skills present in `dotnet-advisor` catalog; no duplicate skill IDs
15. Hard cross-references present and resolvable
16. Soft cross-references: `[skill:dotnet-native-aot]` (validated only if file present)
17. Reverse cross-refs: existing framework skills' `[skill:dotnet-ui-chooser]` soft-dep placeholder is now a hard ref
18. `./scripts/validate-skills.sh` passes
19. Combined skill description budget remains under 12,000 chars (5 new skills × ~120 chars ≈ 600 chars added)

## Dependencies
- **Hard:** fn-3 (core C# patterns — `dotnet-csharp-dependency-injection` for DI patterns)
- **Soft:** fn-14 (`dotnet-maui-development` for ui-chooser cross-ref), fn-13 (`dotnet-uno-platform` for ui-chooser cross-ref), fn-12 (`dotnet-blazor-patterns` for ui-chooser cross-ref)
- **Soft:** fn-16 (`dotnet-native-aot` may not exist yet)
- **Pattern reference:** fn-14 (MAUI skills — structural template, not a code dependency)

## Conventions
- Canonical SKILL.md frontmatter: `name` and `description` only
- Cross-reference syntax: `[skill:name]`
- Description budget guardrail: each skill description ≤ 120 chars, total budget < 12,000 chars
- No agent for this epic — `dotnet-advisor` handles routing
- Migration guidance must be context-dependent, never absolute

## Test Notes
- Verify WinUI skill distinguishes WinUI 3 from UWP (common agent confusion point)
- Verify WPF skill covers .NET 8+ patterns, not .NET Framework patterns
- Verify WinForms dark mode is documented as experimental with platform caveats
- Verify ui-chooser is objective and covers trade-offs, not just recommendations
- Verify migration paths include `dotnet-upgrade-assistant` where applicable
- Verify all skills have Agent Gotchas sections
- Run `./scripts/validate-skills.sh` to confirm all frontmatter and cross-refs pass

## References
- WinUI 3: https://learn.microsoft.com/en-us/windows/apps/winui/winui3/
- Windows App SDK: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/
- WPF on .NET: https://learn.microsoft.com/en-us/dotnet/desktop/wpf/
- WinForms on .NET: https://learn.microsoft.com/en-us/dotnet/desktop/winforms/
- dotnet-upgrade-assistant: https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-overview
- UWP to WinUI migration: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/migrate-to-windows-app-sdk/
