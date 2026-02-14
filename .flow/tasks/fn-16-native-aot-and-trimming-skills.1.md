# fn-16-native-aot-and-trimming-skills.1 Create AOT and trimming skills (native-aot, architecture, trimming, wasm)

## Description
Create four Native AOT and trimming skills: `dotnet-native-aot` (full AOT pipeline: PublishAot, ILLink descriptors, reflection-free patterns, P/Invoke, size optimization, EnableAotAnalyzer/EnableTrimAnalyzer, self-contained with runtime-deps), `dotnet-aot-architecture` (AOT-first design: source gen over reflection, AOT-safe DI, serialization choices, library compat, factory patterns), `dotnet-trimming` (trim-safe development: annotations, ILLink descriptors, TrimmerSingleWarn, testing trimmed output, IL2xxx/IL3xxx warnings, IsTrimmable vs PublishTrimmed), and `dotnet-aot-wasm` (WebAssembly AOT for Blazor WASM and Uno WASM: compilation pipeline, download size vs runtime speed, lazy loading, Brotli pre-compression).

Key technical requirements:
- Use ILLink descriptors and `[DynamicDependency]` — NOT legacy RD.xml (silently ignored by modern .NET AOT)
- Differentiate MSBuild properties: apps use PublishTrimmed/PublishAot + EnableTrimAnalyzer/EnableAotAnalyzer; libraries use IsTrimmable/IsAotCompatible
- WASM section must correctly document that trimming reduces size while AOT increases artifact size (but improves runtime speed)
- Use `dotnet build /p:EnableTrimAnalyzer=true` for analysis without publishing (not `dotnet publish --no-actual-publish`)
- Cross-reference canonical skill IDs for serialization, source generators, DI, MAUI AOT, containers

## Acceptance
- [ ] `skills/native-aot/dotnet-native-aot/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/native-aot/dotnet-aot-architecture/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/native-aot/dotnet-trimming/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/native-aot/dotnet-aot-wasm/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-native-aot` covers PublishAot, ILLink descriptors, reflection-free patterns, P/Invoke, size optimization, self-contained deployment with `runtime-deps` base image
- [ ] `dotnet-native-aot` documents `EnableAotAnalyzer`/`EnableTrimAnalyzer` diagnostic enablement and `dotnet build /p:EnableTrimAnalyzer=true` for analysis without publishing
- [ ] `dotnet-aot-architecture` covers source gen over reflection, AOT-safe DI patterns, serialization choices, library compat assessment, factory patterns replacing `Activator.CreateInstance`
- [ ] `dotnet-trimming` covers annotations, ILLink descriptors, TrimmerSingleWarn, testing trimmed output, IL2xxx/IL3xxx warnings
- [ ] `dotnet-trimming` differentiates app properties (PublishTrimmed + EnableTrimAnalyzer) vs library properties (IsTrimmable/IsAotCompatible)
- [ ] `dotnet-aot-wasm` covers Blazor WASM and Uno WASM AOT with correct size/speed tradeoff
- [ ] `dotnet-aot-wasm` covers lazy loading assemblies and Brotli pre-compression for WASM download optimization
- [ ] No skill references legacy RD.xml — all preservation uses ILLink descriptors
- [ ] All skills contain out-of-scope boundary statements
- [ ] Hard cross-refs present: `[skill:dotnet-serialization]`, `[skill:dotnet-csharp-source-generators]`, `[skill:dotnet-csharp-dependency-injection]`, `[skill:dotnet-maui-aot]`, `[skill:dotnet-containers]`
- [ ] Skill `name` values are unique repo-wide
- [ ] Does NOT modify `plugin.json` (handled by fn-16.3)

## Done summary
Created 4 Native AOT and trimming skills under skills/native-aot/:

1. **dotnet-native-aot** — Full AOT pipeline: PublishAot, ILLink descriptors (not RD.xml), reflection-free patterns, P/Invoke with LibraryImport, size optimization, runtime-deps containers, EnableAotAnalyzer/EnableTrimAnalyzer, ASP.NET Core Minimal API AOT, .NET 10 improvements section
2. **dotnet-aot-architecture** — AOT-first design: source gen over reflection, explicit DI over scanning, STJ source gen serialization, factory patterns replacing Activator.CreateInstance, library compat assessment
3. **dotnet-trimming** — Trim-safe development: annotations (RequiresUnreferencedCode, DynamicallyAccessedMembers, DynamicDependency), ILLink descriptors, TrimmerSingleWarn, IL2xxx/IL3xxx warnings, app vs library MSBuild properties (PublishTrimmed vs IsTrimmable)
4. **dotnet-aot-wasm** — WASM AOT: Blazor WASM + Uno WASM, correct size/speed tradeoff (trimming reduces size, AOT increases size but improves speed), lazy loading, Brotli pre-compression, selective AOT

All skills have name/description frontmatter, out-of-scope boundary statements, and hard cross-refs to dotnet-serialization, dotnet-csharp-source-generators, dotnet-csharp-dependency-injection, dotnet-maui-aot, dotnet-containers. No RD.xml usage. validate-skills.sh passes with 0 errors.
## Evidence
- Commits:
- Tests: validate-skills.sh: PASSED (0 errors, 60 warnings), 4/4 skills exist with name+description frontmatter, 0 duplicate skill names repo-wide, 5 hard cross-refs present: dotnet-serialization, dotnet-csharp-source-generators, dotnet-csharp-dependency-injection, dotnet-maui-aot, dotnet-containers, 4/4 skills have out-of-scope boundary statements, No actual RD.xml usage (only warnings against it), dotnet-trimming: IsTrimmable + PublishTrimmed differentiation present, dotnet-native-aot: PublishAot + EnableAotAnalyzer/EnableTrimAnalyzer present, dotnet-native-aot: runtime-deps base image documented, dotnet-aot-architecture: Activator.CreateInstance factory pattern documented, dotnet-aot-wasm: lazy loading + Brotli compression documented, Description lengths: 112, 115, 118, 119 chars (all <120)
- PRs: