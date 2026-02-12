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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
