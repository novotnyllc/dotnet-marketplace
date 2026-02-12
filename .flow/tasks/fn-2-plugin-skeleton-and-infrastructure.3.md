## Description
Create the `dotnet-version-detection` skill that reads project files to determine the .NET version, C# language version, and preview feature state. This is a cross-cutting skill referenced by virtually all other skills. The skill focuses on detection/reporting; version-specific feature knowledge is stored as a dated reference data section.

**Size:** M
**Files:**
- `skills/foundation/dotnet-version-detection/SKILL.md`

## Approach

1. Use `/plugin-dev:skill-development` for frontmatter
2. Skill instructs agent to read and parse using this **precedence algorithm**:
   1. Direct `<TargetFramework>` value in .csproj (highest priority)
   2. `<TargetFrameworks>` (semicolon-delimited) -- report all, guide on highest
   3. `Directory.Build.props` shared TFM (if no per-project override)
   4. MSBuild property expressions (e.g., `$(SomeTfm)`) -- emit "unresolved property: $(SomeTfm)" warning, fall back to global.json SDK version
   5. `dotnet --version` as last resort
3. Additional detection:
   - `global.json` -> `sdk.version`
   - `<LangVersion>preview</LangVersion>` -> C# 15 features
   - `<EnablePreviewFeatures>true</EnablePreviewFeatures>` -> .NET 11 features
   - `<Features>$(Features);runtime-async=on</Features>` -> runtime-async
4. Output structured version info: TFM(s), C# version, preview state, SDK version, any warnings
5. Multi-targeting handling: report all TFMs, guide on highest, note polyfill needs for lower
6. **Version-to-feature reference data section** (separate from detection logic):
   - .NET version matrix (net8.0 through net11.0) with C# versions and support dates
   - .NET 11 Preview 1 feature awareness
   - Tagged with `Last updated: YYYY-MM-DD` for staleness tracking
7. Edge cases:
   - No csproj: suggest creating project
   - MSBuild property indirection: warn "unresolved property", use SDK version fallback
   - Inconsistent files: warn, prefer csproj TFM over global.json
   - `dotnet --version` fallback when no project files exist

## Key context

- Reference: `docs/dotnet-artisan-spec.md` -> "Current .NET Landscape" and ".NET 11 Preview 1 Features"
- Detection runs on first .NET file encounter, caches per-project
- Must never suggest deprecated patterns for detected version
- Separation of concerns: detection logic vs feature catalog (feature catalog is a dated data section, not inline code)
- Use `[skill:name]` cross-reference syntax for any references to other skills
- Required frontmatter: `name`, `description` (canonical set from epic spec)

## Acceptance
- [ ] Skill reads TargetFramework from .csproj correctly (direct values)
- [ ] Skill handles multi-targeting (TargetFrameworks with semicolons)
- [ ] Skill reads global.json SDK version
- [ ] Skill reads Directory.Build.props for shared settings
- [ ] Skill detects preview features (LangVersion, EnablePreviewFeatures)
- [ ] Skill emits "unresolved property" warning for MSBuild property expressions
- [ ] Precedence algorithm documented and followed (csproj > Directory.Build.props > global.json > dotnet --version)
- [ ] Version-to-feature reference data section is separate from detection logic
- [ ] Reference data tagged with `Last updated: YYYY-MM-DD`
- [ ] Version matrix covers net8.0 through net11.0 with C# versions
- [ ] Edge cases handled: missing files, MSBuild indirection, inconsistent versions, no SDK

## Done summary
Created dotnet-version-detection skill with strict TFM precedence algorithm (csproj > Directory.Build.props > global.json > dotnet --version), multi-targeting support, preview feature detection (LangVersion, EnablePreviewFeatures, runtime-async), MSBuild property expression warnings, edge case handling, and a separate version-to-feature reference data section covering net8.0 through net11.0.
## Evidence
- Commits: d31130345d, 7b737165e1, 46208d07af
- Tests: jq empty .claude-plugin/plugin.json
- PRs: