# fn-64.2 Consolidate dotnet-csharp (~22 source skills)

## Description
Create consolidated `dotnet-csharp` skill directory. Merge ~22 C# language skills into one skill with companion files. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-csharp/SKILL.md` + `references/*.md` (new), ~22 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: overview, routing table with keyword hints, scope/out-of-scope, ToC to companion files (~3-5KB)
- Create `references/` dir with one companion file per source skill (22 files total, per consolidation map from .1):
  - `references/coding-standards.md` — naming, file layout, style rules
  - `references/async-patterns.md` — async/await, Task, ConfigureAwait, cancellation
  - `references/dependency-injection.md` — MS DI, keyed services, scopes, lifetimes
  - `references/configuration.md` — Options pattern, user secrets, feature flags
  - `references/source-generators.md` — IIncrementalGenerator, GeneratedRegex, LoggerMessage
  - `references/nullable-reference-types.md` — annotations, migration, agent mistakes
  - `references/serialization.md` — System.Text.Json, Protobuf, MessagePack, AOT
  - `references/channels.md` — Channel<T>, bounded/unbounded, backpressure
  - `references/linq-optimization.md` — IQueryable vs IEnumerable, compiled queries
  - `references/domain-modeling.md` — aggregates, value objects, domain events
  - `references/solid-principles.md` — SRP, DRY, anti-patterns, compliance checks
  - `references/concurrency-patterns.md` — lock, SemaphoreSlim, Interlocked, concurrent collections
  - `references/roslyn-analyzers.md` — DiagnosticAnalyzer, CodeFixProvider (merge existing details.md)
  - `references/editorconfig.md` — IDE/CA severity, AnalysisLevel, globalconfig
  - `references/file-io.md` — FileStream, RandomAccess, FileSystemWatcher, paths
  - `references/native-interop.md` — P/Invoke, LibraryImport, marshalling
  - `references/input-validation.md` — .NET 10 AddValidation, FluentValidation
  - `references/validation-patterns.md` — DataAnnotations, IValidatableObject, IValidateOptions
  - `references/modern-patterns.md` — records, pattern matching, primary constructors, C# 12-15
  - `references/api-design.md` — naming, parameter ordering, return types, extensions
  - `references/type-design-performance.md` — struct vs class, sealed, Span/Memory, collections
  - `references/code-smells.md` — anti-patterns, async misuse, DI mistakes (merge existing details.md)
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- `dotnet-csharp-async-patterns` is referenced by 4 agents (most-shared skill) — companion file must be easily discoverable from ToC
- `dotnet-csharp-coding-standards` is the baseline for all C# code reviews — put prominently in SKILL.md overview
- Several source skills have existing `details.md` or `examples.md` — absorb into appropriate companion files
- All project-setup content (scaffolding, artifacts output, add-analyzers, add-ci, add-testing, modernize) goes in `dotnet-tooling` (task .6), NOT here

## Acceptance
- [ ] `skills/dotnet-csharp/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-csharp/references/` contains companion files from all merged source skills
- [ ] All ~22 source C# skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter (name, description, license, user-invocable)
- [ ] No content lost from source skills

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
