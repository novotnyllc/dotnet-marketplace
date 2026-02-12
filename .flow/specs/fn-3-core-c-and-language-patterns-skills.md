# fn-3: Core C# & Language Patterns Skills

## Overview
Delivers essential C# language skills covering modern patterns, async/await, nullable reference types, dependency injection, configuration, and source generators. Includes a specialized concurrency agent.

## Scope

**Skills** (7 total, directory: `skills/core-csharp/<name>/SKILL.md`):

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-csharp-modern-patterns` | `skills/core-csharp/dotnet-csharp-modern-patterns/` | C# 14/15 features, pattern matching, records, primary constructors, collection expressions |
| `dotnet-csharp-coding-standards` | `skills/core-csharp/dotnet-csharp-coding-standards/` | Modern .NET coding standards, naming conventions, file organization (Framework Design Guidelines) |
| `dotnet-csharp-async-patterns` | `skills/core-csharp/dotnet-csharp-async-patterns/` | Async/await best practices, common agent mistakes (blocking on tasks, async void, missing ConfigureAwait) |
| `dotnet-csharp-nullable-reference-types` | `skills/core-csharp/dotnet-csharp-nullable-reference-types/` | NRT patterns, annotation strategies, migration guidance |
| `dotnet-csharp-dependency-injection` | `skills/core-csharp/dotnet-csharp-dependency-injection/` | MS DI advanced patterns: keyed services, decoration, factory patterns, scopes, hosted service registration |
| `dotnet-csharp-configuration` | `skills/core-csharp/dotnet-csharp-configuration/` | Options pattern, user secrets, environment-based config, Microsoft.FeatureManagement for feature flags |
| `dotnet-csharp-source-generators` | `skills/core-csharp/dotnet-csharp-source-generators/` | Creating AND using source generators: IIncrementalGenerator, syntax/semantic analysis, emit patterns, testing |

Skill IDs match the `[skill:dotnet-csharp-*]` cross-references already used in `dotnet-advisor` catalog (category 2). Each SKILL.md uses canonical frontmatter (`name`, `description`) per fn-2 conventions. Cross-references use `[skill:name]` syntax.

**Agents** (1 total, file: `agents/dotnet-csharp-concurrency-specialist.md`):

| Agent ID | File | Summary |
|----------|------|---------|
| `dotnet-csharp-concurrency-specialist` | `agents/dotnet-csharp-concurrency-specialist.md` | Deep expertise in Task/async patterns, thread safety, synchronization, race condition analysis |

Agent registration: added to `plugin.json` `agents` array as `"agents/dotnet-csharp-concurrency-specialist.md"`.

Trigger phrases: "race condition", "deadlock", "thread safety", "concurrent access", "lock contention", "async race", "parallel execution", "synchronization issue".

Preloaded skills: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-modern-patterns]`.

## Key Context
- All skills must reference Microsoft .NET Framework Design Guidelines (https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- C# Coding Conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- Async guidance from David Fowler: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- Source Generator Cookbook: https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md
- Skills must adapt to detected TFM (net8.0, net9.0, net10.0, net11.0) and use polyfills where applicable
- .NET 11 preview awareness: Runtime async, collection expression `with()` arguments

## Quick Commands
```bash
# Smoke test: verify skill descriptions are agent-discoverable
ls skills/core-csharp/*/SKILL.md | xargs grep -l "description:"

# Validate skill frontmatter
./scripts/validate-skills.sh

# Test cross-references between skills
grep -r "\[skill:" skills/core-csharp/
```

## Acceptance Criteria
1. All 7 skills created at `skills/core-csharp/<name>/SKILL.md` with canonical frontmatter (`name`, `description`) and progressive disclosure body
2. Skill IDs match `dotnet-csharp-*` names used in `dotnet-advisor` catalog category 2
3. Concurrency specialist agent at `agents/dotnet-csharp-concurrency-specialist.md` with frontmatter (name, description, model, tools), trigger phrases, and preloaded skills
4. Agent registered in `plugin.json` `agents` array
5. Skills cross-reference each other using `[skill:name]` syntax (e.g., async-patterns references DI for IHostedService)
6. Modern C# features documented with TFM-specific guidance (C# 14 for net10.0, C# 15 preview for net11.0)
7. Source generator skill covers both creating and consuming generators
8. All skills reference authoritative Microsoft documentation links
9. Agent gotcha patterns documented (blocking async, wrong DI lifetimes, NRT annotation mistakes)
10. `./scripts/validate-skills.sh` passes with all new skills
11. Combined skill description budget remains under 12,000 chars (7 new skills × ~120 chars ≈ 840 chars added)

## Test Notes
- Test skill auto-discovery by searching for C# patterns in agent context
- Validate that concurrency specialist agent triggers on threading-related keywords
- Validate `[skill:dotnet-csharp-*]` cross-references resolve correctly
- Check that .NET 11 preview features only suggested when `net11.0` TFM detected
- Run `./scripts/validate-skills.sh` to confirm all frontmatter and cross-refs pass

## References
- Microsoft Framework Design Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/
- C# Coding Conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- Source Generator Cookbook: https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md
- dotnet-skills reference: https://github.com/Aaronontheweb/dotnet-skills
