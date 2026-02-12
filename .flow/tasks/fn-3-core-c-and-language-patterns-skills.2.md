# fn-3-core-c-and-language-patterns-skills.2 Async, nullable, and DI skills

## Description
Create three skills under `skills/core-csharp/`:

**`dotnet-csharp-async-patterns`**: Async/await best practices, agent-specific gotchas (blocking on `.Result`/`.Wait()`, `async void`, missing `ConfigureAwait`, fire-and-forget). References David Fowler async guidance. Cross-references `[skill:dotnet-csharp-dependency-injection]` for `IHostedService` patterns.

**`dotnet-csharp-nullable-reference-types`**: NRT annotation strategies (`#nullable enable`, `[NotNullWhen]`, `[MemberNotNull]`), migration guidance for legacy codebases, common annotation mistakes agents make. TFM notes: NRT defaults differ by project template version.

**`dotnet-csharp-dependency-injection`**: MS.Extensions.DependencyInjection advanced patterns: keyed services (.NET 8+), decoration patterns, factory delegates, scope validation, `IHostedService`/`BackgroundService` registration. Cross-references `[skill:dotnet-csharp-async-patterns]` and `[skill:dotnet-csharp-configuration]`.

All skills must use canonical frontmatter, `[skill:name]` cross-references, description under 120 chars, and reference authoritative docs.

## Acceptance
- [ ] `skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-nullable-reference-types/SKILL.md` exists with valid frontmatter
- [ ] `skills/core-csharp/dotnet-csharp-dependency-injection/SKILL.md` exists with valid frontmatter
- [ ] All descriptions under 120 chars
- [ ] Agent gotcha patterns documented in async and NRT skills
- [ ] Cross-references use `[skill:name]` syntax
- [ ] DI skill covers keyed services (net8.0+)
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created three core C# skills under skills/core-csharp/:

1. **dotnet-csharp-async-patterns** - Async/await best practices covering task patterns, ConfigureAwait, cancellation, ValueTask, IAsyncEnumerable, and BackgroundService. Includes 5 agent gotcha sections: blocking on .Result/.Wait(), async void, missing ConfigureAwait, fire-and-forget without error handling, and forgetting CancellationToken.

2. **dotnet-csharp-nullable-reference-types** - NRT annotation strategies with #nullable enable, all System.Diagnostics.CodeAnalysis attributes ([NotNullWhen], [MemberNotNull], [NotNullIfNotNull], etc.), migration guidance, generic constraints, EF Core integration. Includes 5 agent gotcha sections: null-forgiving operator abuse, ignoring warnings, wrong interface nullability, missing [NotNullWhen], and value/reference type confusion.

3. **dotnet-csharp-dependency-injection** - MS.Extensions.DI advanced patterns: service lifetimes with captive dependency warnings, keyed services (net8.0+), decoration (manual + Scrutor), factory delegates, TryAdd for libraries, BackgroundService/IHostedService registration, scope validation, and registration organization.

All skills registered in plugin.json. Cross-references use [skill:name] syntax. All descriptions under 120 chars. validate-skills.sh passes with 0 errors.
## Evidence
- Commits:
- Tests: validate-skills.sh: PASSED (0 errors)
- PRs: