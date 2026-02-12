# fn-3-core-c-and-language-patterns-skills.3 Configuration and source generator skills

## Description
Create two skills under `skills/core-csharp/`:

**`dotnet-csharp-configuration`**: Options pattern (`IOptions<T>`, `IOptionsMonitor<T>`, `IOptionsSnapshot<T>`), `IValidateOptions<T>`, user secrets, environment-based configuration, `Microsoft.FeatureManagement` for feature flags. Cross-references `[skill:dotnet-csharp-dependency-injection]` for registration patterns.

**`dotnet-csharp-source-generators`**: Covers BOTH creating and consuming source generators. Creating: `IIncrementalGenerator`, syntax providers, semantic analysis, emit patterns, diagnostic reporting, testing with `CSharpGeneratorDriver`. Consuming: `[GeneratedRegex]`, `[LoggerMessage]`, STJ source-gen, `[JsonSerializable]`. Cross-references `[skill:dotnet-csharp-modern-patterns]` for related C# features.

Both skills must use canonical frontmatter, `[skill:name]` cross-references, description under 120 chars, and reference authoritative docs (Source Generator Cookbook for source-generators).

## Acceptance
- [ ] `skills/core-csharp/dotnet-csharp-configuration/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-source-generators/SKILL.md` exists with valid frontmatter
- [ ] All descriptions under 120 chars
- [ ] Configuration skill covers Options pattern variants and FeatureManagement
- [ ] Source generator skill covers both creating AND consuming generators
- [ ] Source Generator Cookbook referenced
- [ ] Cross-references use `[skill:name]` syntax
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Added dotnet-csharp-configuration skill (Options pattern with IOptions<T>/IOptionsMonitor<T>/IOptionsSnapshot<T>, IValidateOptions<T>, user secrets, environment-based config, Microsoft.FeatureManagement) and dotnet-csharp-source-generators skill (creating generators with IIncrementalGenerator and consuming GeneratedRegex, LoggerMessage, STJ source-gen). Both use canonical frontmatter, [skill:name] cross-references, and descriptions under 120 chars.
## Evidence
- Commits: 00b442862e5a7c8cf8a4948a39634e9c004fa5ec
- Tests: ./scripts/validate-skills.sh
- PRs: