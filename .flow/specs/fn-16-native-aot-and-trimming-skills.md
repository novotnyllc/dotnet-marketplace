# fn-16: Native AOT and Trimming Skills

## Overview
Delivers Native AOT compilation, trimming, and AOT-friendly architecture skills for general .NET applications. These skills teach patterns and best practices for building AOT-compatible applications from the ground up. MAUI-specific iOS/Mac Catalyst AOT is already owned by fn-14 (`dotnet-maui-aot`) and is out of scope here.

## Scope
**Skills (4 total):**
- `dotnet-native-aot` — Full Native AOT compilation pipeline: PublishAot configuration, ILLink descriptors (NOT legacy RD.xml), reflection-free patterns, P/Invoke considerations, size optimization, self-contained deployment with `runtime-deps` base images, `EnableAotAnalyzer`/`EnableTrimAnalyzer` diagnostics
- `dotnet-aot-architecture` — AOT-first application design: source generators over reflection, AOT-safe DI patterns (explicit registration vs assembly scanning), serialization choices (STJ source gen, Protobuf, MessagePack), library compatibility assessment, factory patterns replacing `Activator.CreateInstance`
- `dotnet-trimming` — Trim-safe development: trimming annotations (`[RequiresUnreferencedCode]`, `[DynamicallyAccessedMembers]`, `[DynamicDependency]`), ILLink descriptor XML, `TrimmerSingleWarn`, testing trimmed output, fixing IL2xxx/IL3xxx warnings, library authoring with `IsTrimmable`
- `dotnet-aot-wasm` — WebAssembly AOT for Blazor WASM and Uno WASM: compilation pipeline, download size vs runtime speed tradeoffs, trimming interplay (reduces size, AOT increases artifact but improves speed), lazy loading, Brotli pre-compression

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills.

## Dependencies

**Hard epic dependencies:**
- fn-5 (Architecture Patterns Skills): `[skill:dotnet-containers]` must exist for `runtime-deps` base image cross-ref
- fn-3 (Core C# Skills): `[skill:dotnet-csharp-source-generators]` and `[skill:dotnet-csharp-dependency-injection]` must exist for cross-refs

**Soft epic dependencies:**
- fn-12 (Blazor Skills): `[skill:dotnet-blazor-patterns]` for Blazor WASM AOT context — fn-16 does not block on fn-12
- fn-13 (Uno Platform Skills): `[skill:dotnet-uno-platform]` for Uno WASM AOT context — fn-16 does not block on fn-13
- fn-6 (Serialization Skills): `[skill:dotnet-serialization]` for AOT-safe serialization cross-refs — already shipped
- fn-14 (MAUI Skills): `[skill:dotnet-maui-aot]` for MAUI AOT scope boundary — already shipped

## .NET Version Policy

**Baseline:** .NET 8.0+ (first version with full Native AOT for ASP.NET Core and console apps)

| .NET Version | AOT Capability |
|---|---|
| .NET 7 | Native AOT introduced for console apps only |
| .NET 8 | ASP.NET Core Minimal API AOT, MAUI iOS AOT, console apps |
| .NET 9 | Improved trimming warnings, broader library compat |
| .NET 10 | Enhanced request delegate generator, expanded Minimal API AOT, reduced linker warning surface |

**Version-gating guidance:** Skills should use `.NET 8.0+` as the minimum baseline. .NET 10-specific improvements go in a dedicated section (fn-16.2). Skills must not assume .NET 10 features are available universally — gate with version notes.

## Conventions

- **Frontmatter:** Required fields are `name` and `description` only
- **Cross-reference syntax:** `[skill:skill-name]` for all skill references
- **Description budget:** Target < 120 characters per skill description
- **Out-of-scope format:** "**Out of scope:**" paragraph with epic ownership attribution
- **Code examples:** Use `.NET 8.0+` TFM unless demonstrating version-specific features

## Scope Boundaries

| Concern | fn-16 owns | Other epic owns | Enforcement |
|---|---|---|---|
| MAUI iOS/Catalyst AOT | Cross-references `[skill:dotnet-maui-aot]` | fn-14: owns MAUI-specific AOT pipeline, publish profiles, library compat matrix | Scope boundary statement in `dotnet-native-aot`; grep validates |
| Serialization | AOT compatibility guidance only | fn-6: owns serialization depth (`[skill:dotnet-serialization]`) | Cross-ref to fn-6; no re-teaching serializer setup |
| Source generators | References source gen as AOT enabler | fn-3: owns source generator authoring (`[skill:dotnet-csharp-source-generators]`) | Cross-ref to fn-3 skill |
| Container deployment | AOT + `runtime-deps` base image | fn-5: owns container patterns (`[skill:dotnet-containers]`) | Cross-ref in container section |
| CLI tools | AOT for CLI tool distribution | fn-17: owns CLI tool development depth | Cross-ref placeholder |
| Performance benchmarking | N/A | fn-18: owns performance depth | N/A |
| DI patterns | AOT-safe DI only | fn-3: owns DI depth (`[skill:dotnet-csharp-dependency-injection]`) | Cross-ref; no re-teaching DI |
| Blazor/Uno framework patterns | AOT compilation only | fn-11 (Blazor), fn-13 (Uno) | Cross-refs to framework skills |

## Cross-Reference Classification

| Target Skill | Type | Notes |
|---|---|---|
| `[skill:dotnet-serialization]` | Hard | STJ source gen, Protobuf, MessagePack AOT compat |
| `[skill:dotnet-csharp-source-generators]` | Hard | Source gen as AOT enabler |
| `[skill:dotnet-csharp-dependency-injection]` | Hard | AOT-safe DI patterns |
| `[skill:dotnet-maui-aot]` | Hard | Scope boundary (fn-14 owns MAUI AOT) |
| `[skill:dotnet-containers]` | Hard | `runtime-deps` base image for AOT |
| `[skill:dotnet-blazor-patterns]` | Soft | Blazor WASM AOT context |
| `[skill:dotnet-uno-platform]` | Soft | Uno WASM AOT context |
| `[skill:dotnet-multi-targeting]` | Soft | TFM considerations for AOT |

## Task Decomposition

### fn-16.1: Create core AOT and trimming skills (no dependencies)
**Delivers:** `dotnet-native-aot`, `dotnet-aot-architecture`, `dotnet-trimming`, `dotnet-aot-wasm`
- `skills/native-aot/dotnet-native-aot/SKILL.md`
- `skills/native-aot/dotnet-aot-architecture/SKILL.md`
- `skills/native-aot/dotnet-trimming/SKILL.md`
- `skills/native-aot/dotnet-aot-wasm/SKILL.md`
- All require `name` and `description` frontmatter
- `dotnet-native-aot` covers: PublishAot, ILLink descriptors, reflection-free patterns, P/Invoke, size optimization, EnableAotAnalyzer/EnableTrimAnalyzer, self-contained with runtime-deps
- `dotnet-aot-architecture` covers: source gen over reflection, AOT-safe DI, serialization choices, library compat assessment, factory patterns
- `dotnet-trimming` covers: annotations, ILLink descriptors, TrimmerSingleWarn, testing trimmed output, fixing warnings, library authoring with IsTrimmable vs app PublishTrimmed
- `dotnet-aot-wasm` covers: Blazor WASM AOT, Uno WASM AOT, download size vs runtime speed, lazy loading, Brotli pre-compression
- Each skill must contain out-of-scope boundary statements
- MSBuild properties must differentiate app vs library usage per pitfall: apps use PublishTrimmed/PublishAot + EnableTrimAnalyzer/EnableAotAnalyzer; libraries use IsTrimmable/IsAotCompatible
- ILLink descriptors must be used (NOT legacy RD.xml which is .NET Native/UWP format)
- WASM section must not conflate trimming size reduction with AOT size increase
- Does NOT modify `plugin.json` (handled by fn-16.3)

### fn-16.2: Add .NET 10 ASP.NET Core AOT section to dotnet-native-aot (depends on fn-16.1)
**Delivers:** .NET 10-specific AOT content in `dotnet-native-aot`
- Documents .NET 10 ASP.NET Core AOT improvements (improved request delegate generator, Minimal API AOT support, Blazor Server AOT compat)
- Integrates into `dotnet-native-aot` skill as a dedicated section
- **Depends on fn-16.1** (needs the base skill file to exist)
- Does NOT modify `plugin.json` (handled by fn-16.3)

### fn-16.3: Integration — plugin registration, validation, and cross-reference audit (depends on fn-16.1, fn-16.2)
**Delivers:** Plugin registration and validation for all 4 skills
- Registers all 4 skill paths in `.claude-plugin/plugin.json`
- Runs repo-wide uniqueness check on skill `name` frontmatter
- Runs `./scripts/validate-skills.sh`
- Validates cross-references use canonical skill IDs
- Validates scope boundary statements present in each skill
- Updates existing skill TODO placeholders that reference fn-16 (e.g., `dotnet-serialization` has `<!-- TODO(fn-16) -->`)
- Single owner of `plugin.json` modifications
- Validates soft cross-refs are excluded from hard validation commands

## Key Context
- Native AOT uses ILLink descriptors and `[DynamicDependency]` attributes — NOT legacy RD.xml (which is .NET Native/UWP format, silently ignored by modern .NET AOT)
- MSBuild properties differ by project type: apps use `PublishTrimmed`/`PublishAot` + `EnableTrimAnalyzer`/`EnableAotAnalyzer`; libraries use `IsTrimmable`/`IsAotCompatible` (which auto-enable analyzers)
- WASM AOT and trimming have opposite size effects: trimming reduces download size, AOT increases artifact size (but improves runtime speed) — do not conflate
- `dotnet publish --no-actual-publish` is not valid; use `dotnet build /p:EnableTrimAnalyzer=true /p:EnableAotAnalyzer=true` for analysis without publishing
- Source generators are the primary AOT enabler (replacing reflection-based patterns)
- .NET 10 brings significant ASP.NET Core AOT improvements (request delegate generator, Minimal APIs)
- `dotnet-maui-aot` already covers MAUI iOS/Mac Catalyst AOT — fn-16 focuses on general .NET AOT

## Quick Commands
```bash
# Validate all 4 skills exist with frontmatter
for s in dotnet-native-aot dotnet-aot-architecture dotnet-trimming dotnet-aot-wasm; do
  test -f "skills/native-aot/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate frontmatter has required fields (name AND description)
for s in skills/native-aot/*/SKILL.md; do
  grep -q "^name:" "$s" && grep -q "^description:" "$s" && echo "OK: $s" || echo "MISSING FRONTMATTER: $s"
done

# Repo-wide skill name uniqueness check
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Canonical frontmatter validation
./scripts/validate-skills.sh

# Verify ILLink descriptors used (NOT RD.xml)
grep -ri "rd\.xml" skills/native-aot/ && echo "FAIL: legacy RD.xml reference found" || echo "OK: no RD.xml"

# Verify cross-references use canonical skill IDs
grep -r "\[skill:dotnet-serialization\]" skills/native-aot/
grep -r "\[skill:dotnet-csharp-source-generators\]" skills/native-aot/
grep -r "\[skill:dotnet-csharp-dependency-injection\]" skills/native-aot/
grep -r "\[skill:dotnet-maui-aot\]" skills/native-aot/
grep -r "\[skill:dotnet-containers\]" skills/native-aot/

# Verify scope boundary statements
grep -l "Out of scope\|out of scope\|Scope boundary" skills/native-aot/*/SKILL.md | wc -l  # expect 4

# Verify MSBuild property differentiation (app vs library)
grep -l "IsTrimmable\|IsAotCompatible" skills/native-aot/dotnet-trimming/SKILL.md  # expect match
grep -l "PublishAot\|PublishTrimmed" skills/native-aot/dotnet-native-aot/SKILL.md  # expect match

# Verify EnableAotAnalyzer/EnableTrimAnalyzer coverage
grep -l "EnableAotAnalyzer\|EnableTrimAnalyzer" skills/native-aot/dotnet-native-aot/SKILL.md  # expect match

# Verify factory pattern coverage in aot-architecture
grep -l "Activator.CreateInstance\|factory pattern" skills/native-aot/dotnet-aot-architecture/SKILL.md  # expect match

# Verify WASM lazy loading and Brotli coverage
grep -l "lazy load" skills/native-aot/dotnet-aot-wasm/SKILL.md  # expect match
grep -l "Brotli\|brotli" skills/native-aot/dotnet-aot-wasm/SKILL.md  # expect match

# Verify runtime-deps base image reference
grep -l "runtime-deps" skills/native-aot/dotnet-native-aot/SKILL.md  # expect match

# Verify TODO(fn-16) placeholders are resolved after fn-16.3
grep -r "TODO(fn-16)" skills/  # expect empty after fn-16.3

# Verify plugin.json contains all 4 native-aot skills (after fn-16.3)
for s in dotnet-native-aot dotnet-aot-architecture dotnet-trimming dotnet-aot-wasm; do
  grep -q "skills/native-aot/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done
```

## Acceptance Criteria
1. All 4 skills exist at `skills/native-aot/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-native-aot` covers full AOT pipeline: PublishAot, ILLink descriptors, reflection-free patterns, P/Invoke, size optimization, self-contained deployment with `runtime-deps` base image
3. `dotnet-native-aot` documents `EnableAotAnalyzer`/`EnableTrimAnalyzer` diagnostic enablement and `dotnet build /p:EnableTrimAnalyzer=true` for analysis without publishing
4. `dotnet-native-aot` includes .NET 10 ASP.NET Core AOT improvements section
5. `dotnet-aot-architecture` covers AOT-first design: source gen over reflection, AOT-safe DI patterns (explicit registration), serialization choices, library compat assessment, factory patterns replacing `Activator.CreateInstance`
6. `dotnet-trimming` covers trim-safe development: annotations, ILLink descriptors, TrimmerSingleWarn, testing trimmed output, fixing IL2xxx/IL3xxx warnings
7. `dotnet-trimming` differentiates MSBuild properties for apps (`PublishTrimmed` + `EnableTrimAnalyzer`) vs libraries (`IsTrimmable`/`IsAotCompatible`)
8. `dotnet-aot-wasm` covers WebAssembly AOT for Blazor WASM and Uno WASM with correct size/speed tradeoff documentation
9. `dotnet-aot-wasm` covers lazy loading assemblies and Brotli pre-compression for WASM download optimization
10. `dotnet-aot-wasm` does not conflate trimming (reduces size) with AOT (increases artifact size, improves runtime speed)
11. No skill references legacy RD.xml — all trimming preservation uses ILLink descriptors and `[DynamicDependency]`
12. Skills cross-reference fn-6 serialization, fn-3 source generators, fn-3 DI using canonical skill IDs — not re-teach
13. Each skill contains explicit out-of-scope boundary statement for related epics (fn-14 MAUI AOT, fn-3 DI/source gen, fn-6 serialization)
14. `dotnet-native-aot` cross-references `[skill:dotnet-maui-aot]` with scope boundary (fn-14 owns MAUI-specific AOT)
15. All 4 skills registered in `.claude-plugin/plugin.json` (fn-16.3)
16. `./scripts/validate-skills.sh` passes for all 4 skills
17. Skill `name` frontmatter values are unique repo-wide
18. Existing `<!-- TODO(fn-16) -->` placeholders in other skills are resolved with canonical cross-refs (fn-16.3)
19. fn-16.2 depends on fn-16.1 (needs base skill file); fn-16.3 depends on fn-16.1 and fn-16.2 — serial execution: fn-16.1 → fn-16.2 → fn-16.3

## Test Notes
- Verify no skill uses "RD.xml" — all preservation uses ILLink descriptors
- Verify `dotnet-aot-wasm` correctly describes trimming reducing size while AOT increases artifact size
- Verify `dotnet-aot-wasm` covers lazy loading assemblies and Brotli pre-compression
- Verify `dotnet-trimming` shows both `PublishTrimmed` (app) and `IsTrimmable` (library) with clear differentiation
- Verify `dotnet-native-aot` mentions `runtime-deps` base image for self-contained AOT deployment
- Verify `dotnet-native-aot` documents `EnableAotAnalyzer`/`EnableTrimAnalyzer` and analysis-without-publish command
- Verify `dotnet-aot-architecture` covers factory patterns replacing `Activator.CreateInstance`
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names
- Verify existing fn-16 TODO placeholders in serialization skill are resolved
- Verify soft cross-refs (Blazor, Uno, multi-targeting) are noted but not enforced in validation commands

## References
- Native AOT deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- Trim self-contained applications: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options
- Prepare libraries for trimming: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming
- ILLink descriptor format: https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/trimming-options#descriptor-format
- ASP.NET Core Native AOT: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot
- System.Text.Json source generation: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation
