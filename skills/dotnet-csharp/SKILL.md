---
name: dotnet-csharp
description: Guides C# language patterns, coding standards, and .NET runtime features. Covers async/await, dependency injection, configuration, source generators, nullable reference types, serialization, channels, LINQ optimization, domain modeling, SOLID principles, concurrency, analyzers, editorconfig, file I/O, native interop, validation, modern C# syntax (records, pattern matching, primary constructors), and API design.
license: MIT
user-invocable: false
---

# dotnet-csharp

## Overview

C# language patterns, coding standards, and .NET runtime features for idiomatic, performant code. This consolidated skill covers 22 topic areas. Load the appropriate companion file from `references/` based on the routing table below.

Baseline dependency: `references/coding-standards.md` defines naming, file layout, and style rules that apply to all C# code generation and review tasks. Load it by default whenever C# code will be produced.

Most-shared companion: `references/async-patterns.md` is referenced by 4 agents and covers async/await patterns critical to nearly all .NET development.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Coding standards | naming, file layout, style rules | references/coding-standards.md |
| Async/await | async, Task, ConfigureAwait, cancellation | references/async-patterns.md |
| Dependency injection | DI, services, scopes, keyed, lifetimes | references/dependency-injection.md |
| Configuration | Options pattern, user secrets, feature flags | references/configuration.md |
| Source generators | IIncrementalGenerator, GeneratedRegex, LoggerMessage | references/source-generators.md |
| Nullable reference types | annotations, migration, agent mistakes | references/nullable-reference-types.md |
| Serialization | System.Text.Json, Protobuf, MessagePack, AOT | references/serialization.md |
| Channels | Channel\<T\>, bounded/unbounded, backpressure | references/channels.md |
| LINQ optimization | IQueryable vs IEnumerable, compiled queries | references/linq-optimization.md |
| Domain modeling | aggregates, value objects, domain events | references/domain-modeling.md |
| SOLID principles | SRP, DRY, anti-patterns, compliance checks | references/solid-principles.md |
| Concurrency | lock, SemaphoreSlim, Interlocked, concurrent collections | references/concurrency-patterns.md |
| Roslyn analyzers | DiagnosticAnalyzer, CodeFixProvider, multi-version | references/roslyn-analyzers.md |
| Editorconfig | IDE/CA severity, AnalysisLevel, globalconfig | references/editorconfig.md |
| File I/O | FileStream, RandomAccess, FileSystemWatcher, paths | references/file-io.md |
| Native interop | P/Invoke, LibraryImport, marshalling | references/native-interop.md |
| Input validation | .NET 10 AddValidation, FluentValidation | references/input-validation.md |
| Validation patterns | DataAnnotations, IValidatableObject, IValidateOptions | references/validation-patterns.md |
| Modern patterns | records, pattern matching, primary constructors | references/modern-patterns.md |
| API design | naming, parameter ordering, return types, extensions | references/api-design.md |
| Type design/perf | struct vs class, sealed, Span/Memory, collections | references/type-design-performance.md |
| Code smells | anti-patterns, async misuse, DI mistakes, fixes | references/code-smells.md |

## Scope

- C# language features (C# 8-15)
- .NET runtime patterns (async, DI, config, serialization, channels, LINQ)
- Code quality (analyzers, editorconfig, code smells, SOLID)
- Type design and domain modeling
- File I/O and native interop
- Input validation (model and options validation)

## Out of scope

- ASP.NET Core / web API patterns -> [skill:dotnet-api]
- UI framework patterns -> [skill:dotnet-ui]
- Testing patterns -> [skill:dotnet-testing]
- Build/MSBuild/project setup -> [skill:dotnet-tooling]
- Performance profiling tools -> [skill:dotnet-tooling]

## Companion Files

- `references/coding-standards.md` -- Baseline C# conventions (naming, layout, style rules)
- `references/async-patterns.md` -- async/await, Task patterns, ConfigureAwait, cancellation
- `references/dependency-injection.md` -- MS DI, keyed services, scopes, decoration, lifetimes
- `references/configuration.md` -- Options pattern, user secrets, feature flags, IOptions\<T\>
- `references/source-generators.md` -- IIncrementalGenerator, GeneratedRegex, LoggerMessage, STJ
- `references/nullable-reference-types.md` -- Annotation strategies, migration, agent mistakes
- `references/serialization.md` -- System.Text.Json source generators, Protobuf, MessagePack
- `references/channels.md` -- Channel\<T\>, bounded/unbounded, backpressure, drain
- `references/linq-optimization.md` -- IQueryable vs IEnumerable, compiled queries, allocations
- `references/domain-modeling.md` -- Aggregates, value objects, domain events, repositories
- `references/solid-principles.md` -- SOLID and DRY principles, C# anti-patterns, fixes
- `references/concurrency-patterns.md` -- lock, SemaphoreSlim, Interlocked, concurrent collections
- `references/roslyn-analyzers.md` -- DiagnosticAnalyzer, CodeFixProvider, CodeRefactoring
- `references/editorconfig.md` -- IDE/CA severity, AnalysisLevel, globalconfig, enforcement
- `references/file-io.md` -- FileStream, RandomAccess, FileSystemWatcher, MemoryMappedFile
- `references/native-interop.md` -- P/Invoke, LibraryImport, marshalling, cross-platform
- `references/input-validation.md` -- .NET 10 AddValidation, FluentValidation, ProblemDetails
- `references/validation-patterns.md` -- DataAnnotations, IValidatableObject, IValidateOptions\<T\>
- `references/modern-patterns.md` -- Records, pattern matching, primary constructors, C# 12-15
- `references/api-design.md` -- Naming, parameter ordering, return types, error patterns
- `references/type-design-performance.md` -- struct vs class, sealed, Span/Memory, collections
- `references/code-smells.md` -- Anti-patterns, async misuse, DI mistakes, fixes
