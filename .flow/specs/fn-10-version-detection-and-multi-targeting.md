# fn-10: Version Detection & Multi-Targeting

## Overview
Delivers skills for .NET version detection, multi-targeting strategies with polyfills, and modern .NET version upgrades.

## Scope
**Skills:**
- `dotnet-multi-targeting` - Multi-targeting strategies with polyfill emphasis: PolySharp, SimonCropp/Polyfill, conditional compilation, API compat analyzers
- `dotnet-version-upgrade` - Modern .NET version upgrades (.NET 8 -> 10 -> 11). Forward-looking polyfill usage for latest features on all targets.

## Key Context
- Version detection is foundational for all other skills (reads TFMs from .csproj, Directory.Build.props, global.json)
- Skills must adapt output based on detected TFM (net8.0, net9.0, net10.0, net11.0)
- PolySharp and SimonCropp/Polyfill enable latest language features on older TFMs
- .NET 11 preview detection requires checking LangVersion=preview and EnablePreviewFeatures
- Multi-targeting strategy: prefer polyfills over conditional compilation

## Quick Commands
```bash
# Smoke test: verify version detection logic
grep -i "TFM\|TargetFramework" skills/version/dotnet-multi-targeting.md

# Validate polyfill coverage
grep -i "PolySharp\|Polyfill" skills/version/dotnet-multi-targeting.md

# Test upgrade guidance
grep -i "upgrade\|migration" skills/version/dotnet-version-upgrade.md
```

## Acceptance Criteria
1. Both skills written with standard depth and frontmatter
2. Multi-targeting skill emphasizes PolySharp and SimonCropp/Polyfill for modern features on older TFMs
3. Version upgrade skill provides .NET 8 -> 10 -> 11 migration paths
4. Skills document TFM detection from .csproj, Directory.Build.props, global.json
5. .NET 11 preview feature detection covered (LangVersion=preview, EnablePreviewFeatures)
6. Cross-references to other skills that depend on version detection
7. API compatibility analyzers documented for multi-targeting validation

## Test Notes
- Test multi-targeting skill with polyfill examples (e.g., using C# 12 features on net8.0)
- Verify version upgrade skill detects deprecated packages and patterns
- Validate TFM detection logic with sample .csproj files

## References
- PolySharp: https://github.com/Sergio0694/PolySharp
- SimonCropp Polyfill: https://github.com/SimonCropp/Polyfill
- .NET Multi-Targeting: https://learn.microsoft.com/en-us/dotnet/standard/frameworks
- .NET Upgrade Assistant: https://dotnet.microsoft.com/en-us/platform/upgrade-assistant
