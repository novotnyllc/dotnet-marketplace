# fn-3: Core C# & Language Patterns Skills

## Overview
Delivers essential C# language skills covering modern patterns, async/await, nullable reference types, dependency injection, configuration, and source generators. Includes a specialized concurrency agent.

## Scope
**Skills:**
- `csharp-modern-patterns` - C# 14/15 features, pattern matching, records, primary constructors, collection expressions
- `csharp-coding-standards` - Modern .NET coding standards, naming conventions, file organization (Framework Design Guidelines)
- `csharp-async-patterns` - Async/await best practices, common agent mistakes (blocking on tasks, async void, missing ConfigureAwait)
- `csharp-nullable-reference-types` - NRT patterns, annotation strategies, migration guidance
- `csharp-dependency-injection` - MS DI advanced patterns: keyed services, decoration, factory patterns, scopes, hosted service registration
- `csharp-configuration` - Options pattern, user secrets, environment-based config, Microsoft.FeatureManagement for feature flags
- `csharp-source-generators` - Creating AND using source generators: IIncrementalGenerator, syntax/semantic analysis, emit patterns, testing

**Agents:**
- `csharp-concurrency-specialist` - Deep expertise in Task/async patterns, thread safety, synchronization, race condition analysis

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
fd -e md . skills/core-csharp/ | xargs grep -l "description:"

# Validate skill frontmatter
.flow/bin/flowctl validate-skills skills/core-csharp/

# Test cross-references between skills
grep -r "See also:" skills/core-csharp/
```

## Acceptance Criteria
1. All 7 skills written with SKILL.md frontmatter and progressive disclosure descriptions
2. Concurrency specialist agent configured with preloaded async/threading skills
3. Skills cross-reference each other (e.g., async-patterns references DI for IHostedService)
4. Modern C# features documented with TFM-specific guidance (C# 14 for net10.0, C# 15 preview for net11.0)
5. Source generator skill covers both creating and consuming generators
6. All skills reference authoritative Microsoft documentation links
7. Agent gotcha patterns documented (blocking async, wrong DI lifetimes, NRT annotation mistakes)

## Test Notes
- Test skill auto-discovery by searching for C# patterns in agent context
- Validate that concurrency specialist agent triggers on threading-related keywords
- Check that .NET 11 preview features only suggested when `net11.0` TFM detected

## References
- Microsoft Framework Design Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/
- C# Coding Conventions: https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- Source Generator Cookbook: https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md
- dotnet-skills reference: https://github.com/Aaronontheweb/dotnet-skills
