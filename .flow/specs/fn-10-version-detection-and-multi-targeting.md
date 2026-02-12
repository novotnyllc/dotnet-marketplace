# fn-10: Version Detection & Multi-Targeting

## Overview
Delivers two skills that build on the existing `dotnet-version-detection` foundation skill: multi-targeting strategies with polyfill emphasis, and .NET version upgrade guidance.

**Responsibility boundary:** `dotnet-version-detection` (fn-2/foundation) owns all detection logic (TFM resolution, SDK version, preview feature flags). This epic's skills **consume** detected outputs and provide strategy/guidance only — they never re-implement detection.

## Scope
**Skills (2):**
- `dotnet-multi-targeting` → `skills/multi-targeting/dotnet-multi-targeting/SKILL.md` — Multi-targeting strategies with polyfill-first approach: PolySharp, SimonCropp/Polyfill, conditional compilation for runtime gaps, API compat analyzers
- `dotnet-version-upgrade` → `skills/multi-targeting/dotnet-version-upgrade/SKILL.md` — Modern .NET version upgrades with defined upgrade lanes and polyfill bridge strategies

## Key Context
- `dotnet-version-detection` already handles TFM detection from .csproj, Directory.Build.props, global.json and cross-references both new skills
- New skills consume the structured output from version detection and provide actionable guidance
- PolySharp and SimonCropp/Polyfill enable latest C# language features on older TFMs (compile-time polyfills)
- Conditional compilation (`#if`) remains necessary for runtime/API behavior gaps that polyfills cannot cover
- API compatibility analyzers (`EnablePackageValidation`, `ApiCompat`) validate multi-targeting correctness

### Decision Matrix: Polyfill vs Conditional Compilation
| Gap Type | Strategy | Example |
|----------|----------|---------|
| Language/syntax feature | Polyfill (PolySharp/Polyfill) | `required` modifier, `init` properties, collection expressions on net8.0 |
| BCL API addition | Polyfill if available, else `#if` | `System.Threading.Lock` on net8.0 via Polyfill |
| Runtime behavior difference | Conditional compilation or adapter | Runtime-async (net11.0 only), different GC modes |
| Platform API divergence | Conditional compilation with `[SupportedOSPlatform]` | Windows-only APIs, Android-specific features |

### Upgrade Lanes
| Lane | Path | Use Case |
|------|------|----------|
| Production (default) | net8.0 → net10.0 | LTS-to-LTS, recommended for most apps |
| Staged production | net8.0 → net9.0 → net10.0 | When ecosystem dependencies require incremental migration |
| Experimental | net10.0 → net11.0 (preview) | Non-production only, exploring upcoming features |

**.NET 9 note:** While .NET 9 is STS and approaching end-of-support (May 2026), staging through .NET 9 may be necessary when third-party packages or breaking changes require incremental migration.

## Quick Commands
```bash
# Smoke test: verify polyfill coverage in multi-targeting skill
grep -i "PolySharp\|Polyfill" skills/multi-targeting/dotnet-multi-targeting/SKILL.md

# Verify decision matrix in multi-targeting skill
grep -i "conditional\|#if\|polyfill" skills/multi-targeting/dotnet-multi-targeting/SKILL.md

# Test upgrade guidance lanes
grep -i "upgrade\|migration\|lane" skills/multi-targeting/dotnet-version-upgrade/SKILL.md

# Verify cross-references
grep -i "\[skill:" skills/multi-targeting/*/SKILL.md
```

## Acceptance Criteria
1. Both skills written following the standard pattern (frontmatter with `name`+`description`, overview, detailed sections, gotchas, prerequisites, references, cross-references)
2. Multi-targeting skill includes decision matrix for polyfill vs conditional compilation vs adapter patterns
3. Multi-targeting skill documents PolySharp and SimonCropp/Polyfill with concrete package references, setup examples, and feature coverage
4. Multi-targeting skill documents API compatibility validation workflow: `EnablePackageValidation`, `ApiCompat` baseline, pass/fail criteria
5. Version upgrade skill defines three upgrade lanes (production LTS→LTS, staged through STS, experimental preview) with explicit guardrails
6. Version upgrade skill covers .NET 9 as a staging option (not skipped), with STS end-of-support context
7. Both skills consume output from `dotnet-version-detection` — no re-implementation of TFM detection logic
8. Cross-references: both skills link to `[skill:dotnet-version-detection]`; `dotnet-version-detection` already links back via `[skill:dotnet-multi-targeting]` and `[skill:dotnet-version-upgrade]`
9. Skills placed in `skills/multi-targeting/` directory (both skills share this category)

## File Ownership (Parallelization)
Tasks touch **disjoint** files:
- **fn-10.1**: `skills/multi-targeting/dotnet-multi-targeting/SKILL.md` (creates)
- **fn-10.2**: `skills/multi-targeting/dotnet-version-upgrade/SKILL.md` (creates)

No shared file edits needed — tasks can run fully in parallel.

## Test Notes
- Verify multi-targeting skill provides correct guidance for sample scenarios:
  - Single TFM net8.0 project wanting C# 14 features → PolySharp/Polyfill
  - Multi-TFM `net8.0;net10.0` project → polyfill for language features + `#if` for runtime gaps
  - net11.0 preview with `EnablePreviewFeatures` → experimental lane guidance
  - Mismatched global.json/csproj → consume warning from version-detection, add upgrade guidance
- Verify upgrade skill provides correct lane selection for:
  - net8.0 LTS → net10.0 LTS (direct upgrade)
  - net8.0 with ecosystem constraints → staged through net9.0
  - net10.0 → net11.0 preview (non-production only)
- Validate cross-references resolve correctly (no broken `[skill:...]` links)
- Verify no duplication of detection logic from `dotnet-version-detection`

## References

> **Last verified: 2026-02-12**
- PolySharp: https://github.com/Sergio0694/PolySharp
- SimonCropp Polyfill: https://github.com/SimonCropp/Polyfill
- .NET Multi-Targeting: https://learn.microsoft.com/en-us/dotnet/standard/frameworks
- .NET Upgrade Assistant: https://dotnet.microsoft.com/en-us/platform/upgrade-assistant
- Package Validation: https://learn.microsoft.com/en-us/dotnet/fundamentals/package-validation/overview
- API Compatibility: https://learn.microsoft.com/en-us/dotnet/fundamentals/apicompat/overview
