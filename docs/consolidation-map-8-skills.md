# 8-Skill Consolidation Map

> Definitive mapping of 131 source skills to 8 target skills.
> Produced for epic fn-64-consolidate-131-skills-into-8-broad, task .1.

## Table of Contents

1. [Consolidation Summary](#consolidation-summary)
2. [Target Skill 1: dotnet-csharp](#target-skill-1-dotnet-csharp)
3. [Target Skill 2: dotnet-api](#target-skill-2-dotnet-api)
4. [Target Skill 3: dotnet-ui](#target-skill-3-dotnet-ui)
5. [Target Skill 4: dotnet-testing](#target-skill-4-dotnet-testing)
6. [Target Skill 5: dotnet-devops](#target-skill-5-dotnet-devops)
7. [Target Skill 6: dotnet-tooling](#target-skill-6-dotnet-tooling)
8. [Target Skill 7: dotnet-debugging](#target-skill-7-dotnet-debugging)
9. [Target Skill 8: dotnet-advisor](#target-skill-8-dotnet-advisor)
10. [Edge Cases](#edge-cases)
11. [Companion File Naming Convention](#companion-file-naming-convention)
12. [Existing Companion File Migration](#existing-companion-file-migration)
13. [User-Invocable Assignments](#user-invocable-assignments)
14. [Verification](#verification)

---

## Consolidation Summary

| # | Target Skill | Source Count | User-Invocable |
|---|-------------|:-----------:|:--------------:|
| 1 | **dotnet-csharp** | 22 | false |
| 2 | **dotnet-api** | 27 | false |
| 3 | **dotnet-ui** | 18 | true |
| 4 | **dotnet-testing** | 12 | false |
| 5 | **dotnet-devops** | 18 | false |
| 6 | **dotnet-tooling** | 32 | true |
| 7 | **dotnet-debugging** | 1 | true |
| 8 | **dotnet-advisor** | 1 | true |
| | **TOTAL** | **131** | |

Note: dotnet-advisor is an identity mapping (source skill = target skill). dotnet-debugging is a single-source rename from `dotnet-windbg-debugging`. Every one of the 131 source skills has exactly one assignment.

---

## Target Skill 1: dotnet-csharp

### Routing Description (~380 chars)

Guides C# language patterns, coding standards, and .NET runtime features. Covers async/await, dependency injection, configuration, source generators, nullable reference types, serialization, channels, LINQ optimization, domain modeling, SOLID principles, concurrency, analyzers, editorconfig, file I/O, native interop, validation, modern C# syntax (records, pattern matching, primary constructors), and API design.

### Source Skills (22)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-csharp-coding-standards` | `references/coding-standards.md` | Foundation -- loaded first by advisor |
| 2 | `dotnet-csharp-async-patterns` | `references/async-patterns.md` | |
| 3 | `dotnet-csharp-dependency-injection` | `references/dependency-injection.md` | |
| 4 | `dotnet-csharp-configuration` | `references/configuration.md` | |
| 5 | `dotnet-csharp-source-generators` | `references/source-generators.md` | |
| 6 | `dotnet-csharp-nullable-reference-types` | `references/nullable-reference-types.md` | |
| 7 | `dotnet-serialization` | `references/serialization.md` | |
| 8 | `dotnet-channels` | `references/channels.md` | |
| 9 | `dotnet-linq-optimization` | `references/linq-optimization.md` | |
| 10 | `dotnet-domain-modeling` | `references/domain-modeling.md` | |
| 11 | `dotnet-solid-principles` | `references/solid-principles.md` | |
| 12 | `dotnet-csharp-concurrency-patterns` | `references/concurrency-patterns.md` | |
| 13 | `dotnet-roslyn-analyzers` | `references/roslyn-analyzers.md` | Has existing `details.md` |
| 14 | `dotnet-editorconfig` | `references/editorconfig.md` | |
| 15 | `dotnet-file-io` | `references/file-io.md` | |
| 16 | `dotnet-native-interop` | `references/native-interop.md` | |
| 17 | `dotnet-input-validation` | `references/input-validation.md` | |
| 18 | `dotnet-validation-patterns` | `references/validation-patterns.md` | |
| 19 | `dotnet-csharp-modern-patterns` | `references/modern-patterns.md` | |
| 20 | `dotnet-csharp-api-design` | `references/api-design.md` | |
| 21 | `dotnet-csharp-type-design-performance` | `references/type-design-performance.md` | |
| 22 | `dotnet-csharp-code-smells` | `references/code-smells.md` | Has existing `details.md` |

### SKILL.md Content Outline

```
---
name: dotnet-csharp
description: <routing description above, ~380 chars>
license: MIT
user-invocable: false
---

# dotnet-csharp

## Overview
C# language patterns, coding standards, and .NET runtime features for idiomatic,
performant code.

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
| Channels | Channel<T>, bounded/unbounded, backpressure | references/channels.md |
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
- `references/configuration.md` -- Options pattern, user secrets, feature flags, IOptions<T>
- `references/source-generators.md` -- IIncrementalGenerator, GeneratedRegex, LoggerMessage, STJ
- `references/nullable-reference-types.md` -- Annotation strategies, migration, agent mistakes
- `references/serialization.md` -- System.Text.Json source generators, Protobuf, MessagePack
- `references/channels.md` -- Channel<T>, bounded/unbounded, backpressure, drain
- `references/linq-optimization.md` -- IQueryable vs IEnumerable, compiled queries, allocations
- `references/domain-modeling.md` -- Aggregates, value objects, domain events, repositories
- `references/solid-principles.md` -- SOLID and DRY principles, C# anti-patterns, fixes
- `references/concurrency-patterns.md` -- lock, SemaphoreSlim, Interlocked, concurrent collections
- `references/roslyn-analyzers.md` -- DiagnosticAnalyzer, CodeFixProvider, CodeRefactoring
- `references/editorconfig.md` -- IDE/CA severity, AnalysisLevel, globalconfig, enforcement
- `references/file-io.md` -- FileStream, RandomAccess, FileSystemWatcher, MemoryMappedFile
- `references/native-interop.md` -- P/Invoke, LibraryImport, marshalling, cross-platform
- `references/input-validation.md` -- .NET 10 AddValidation, FluentValidation, ProblemDetails
- `references/validation-patterns.md` -- DataAnnotations, IValidatableObject, IValidateOptions<T>
- `references/modern-patterns.md` -- Records, pattern matching, primary constructors, C# 12-15
- `references/api-design.md` -- Naming, parameter ordering, return types, error patterns
- `references/type-design-performance.md` -- struct vs class, sealed, Span/Memory, collections
- `references/code-smells.md` -- Anti-patterns, async misuse, DI mistakes, fixes
```

---

## Target Skill 2: dotnet-api

### Routing Description (~390 chars)

Builds ASP.NET Core APIs, data access, and backend services. Covers minimal APIs, middleware, EF Core (patterns and architecture), gRPC, SignalR/SSE, resilience (Polly), HTTP client, API versioning, OpenAPI, security (OWASP, secrets, crypto), background services, Aspire orchestration, Semantic Kernel AI integration, architecture patterns, messaging, service communication, data access strategy, API surface validation, and API documentation.

### Source Skills (27)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-minimal-apis` | `references/minimal-apis.md` | |
| 2 | `dotnet-middleware-patterns` | `references/middleware-patterns.md` | |
| 3 | `dotnet-efcore-patterns` | `references/efcore-patterns.md` | |
| 4 | `dotnet-efcore-architecture` | `references/efcore-architecture.md` | |
| 5 | `dotnet-data-access-strategy` | `references/data-access-strategy.md` | Was user-invocable |
| 6 | `dotnet-grpc` | `references/grpc.md` | Has existing `examples.md` |
| 7 | `dotnet-realtime-communication` | `references/realtime-communication.md` | SignalR, SSE, gRPC streaming |
| 8 | `dotnet-resilience` | `references/resilience.md` | Polly v8 |
| 9 | `dotnet-http-client` | `references/http-client.md` | |
| 10 | `dotnet-api-versioning` | `references/api-versioning.md` | |
| 11 | `dotnet-openapi` | `references/openapi.md` | |
| 12 | `dotnet-api-security` | `references/api-security.md` | Auth, JWT, CORS |
| 13 | `dotnet-security-owasp` | `references/security-owasp.md` | |
| 14 | `dotnet-secrets-management` | `references/secrets-management.md` | |
| 15 | `dotnet-cryptography` | `references/cryptography.md` | |
| 16 | `dotnet-background-services` | `references/background-services.md` | |
| 17 | `dotnet-aspire-patterns` | `references/aspire-patterns.md` | |
| 18 | `dotnet-semantic-kernel` | `references/semantic-kernel.md` | |
| 19 | `dotnet-architecture-patterns` | `references/architecture-patterns.md` | Has existing `examples.md` |
| 20 | `dotnet-messaging-patterns` | `references/messaging-patterns.md` | |
| 21 | `dotnet-service-communication` | `references/service-communication.md` | |
| 22 | `dotnet-api-surface-validation` | `references/api-surface-validation.md` | |
| 23 | `dotnet-library-api-compat` | `references/library-api-compat.md` | |
| 24 | `dotnet-io-pipelines` | `references/io-pipelines.md` | PipeReader/PipeWriter |
| 25 | `dotnet-agent-gotchas` | `references/agent-gotchas.md` | Cross-cutting but API-heavy |
| 26 | `dotnet-file-based-apps` | `references/file-based-apps.md` | .NET 10 feature |
| 27 | `dotnet-api-docs` | `references/api-docs.md` | DocFX, OpenAPI-as-docs |

### Edge Case Rationale

- **dotnet-agent-gotchas** -> dotnet-api: Most agent gotchas are API/backend concerns (async misuse, NuGet errors, DI). The content is cross-cutting but best routed with API patterns since that is where agents make the most mistakes.
- **dotnet-file-based-apps** -> dotnet-api: .NET 10 file-based apps are a new app model closely aligned with Minimal APIs.
- **dotnet-api-docs** -> dotnet-api: DocFX and OpenAPI docs are API documentation concerns.
- **dotnet-io-pipelines** -> dotnet-api: High-perf network I/O (Kestrel integration) is backend/API territory.
- **dotnet-library-api-compat** -> dotnet-api: API compatibility rules serve library-as-API-contract scenarios.

### SKILL.md Content Outline

```
---
name: dotnet-api
description: <routing description above, ~390 chars>
license: MIT
user-invocable: false
---

# dotnet-api

## Overview
ASP.NET Core APIs, data access, backend services, security, and cloud-native patterns.

## Routing Table
| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Minimal APIs | endpoint, route group, filter, TypedResults | references/minimal-apis.md |
| EF Core patterns | DbContext, migrations, AsNoTracking | references/efcore-patterns.md |
| EF Core architecture | read/write split, aggregate boundaries, N+1 | references/efcore-architecture.md |
| Data access strategy | EF Core vs Dapper vs ADO.NET decision | references/data-access-strategy.md |
| Middleware | pipeline ordering, short-circuit, exception | references/middleware-patterns.md |
| gRPC | proto, code-gen, streaming, auth | references/grpc.md |
| Real-time | SignalR, SSE, JSON-RPC, gRPC streaming | references/realtime-communication.md |
| Resilience | Polly v8, retry, circuit breaker, timeout | references/resilience.md |
| HTTP client | IHttpClientFactory, typed/named, DelegatingHandler | references/http-client.md |
| API versioning | Asp.Versioning, URL/header/query, sunset | references/api-versioning.md |
| OpenAPI | MS.AspNetCore.OpenApi, Swashbuckle, NSwag | references/openapi.md |
| API security | Identity, OAuth/OIDC, JWT, CORS, rate limiting | references/api-security.md |
| OWASP | injection, auth, XSS, deprecated APIs | references/security-owasp.md |
| Secrets | user secrets, env vars, rotation | references/secrets-management.md |
| Cryptography | AES-GCM, RSA, ECDSA, hashing, key derivation | references/cryptography.md |
| Background services | BackgroundService, IHostedService, lifecycle | references/background-services.md |
| Aspire | AppHost, service discovery, dashboard | references/aspire-patterns.md |
| Semantic Kernel | AI/LLM plugins, prompts, memory, agents | references/semantic-kernel.md |
| Architecture | vertical slices, layered, pipelines, caching | references/architecture-patterns.md |
| Messaging | MassTransit, Azure Service Bus, pub/sub, sagas | references/messaging-patterns.md |
| Service communication | REST vs gRPC vs SignalR decision matrix | references/service-communication.md |
| API surface validation | PublicApiAnalyzers, Verify, ApiCompat | references/api-surface-validation.md |
| Library API compat | binary/source compat, type forwarders | references/library-api-compat.md |
| I/O pipelines | PipeReader/PipeWriter, backpressure, Kestrel | references/io-pipelines.md |
| Agent gotchas | async misuse, NuGet errors, DI mistakes | references/agent-gotchas.md |
| File-based apps | .NET 10, directives, csproj migration | references/file-based-apps.md |
| API docs | DocFX, OpenAPI-as-docs, versioned docs | references/api-docs.md |

## Scope
- ASP.NET Core web APIs (minimal and controller-based)
- Data access (EF Core, Dapper, ADO.NET)
- Service communication (gRPC, SignalR, SSE, messaging)
- Security (auth, OWASP, secrets, crypto)
- Cloud-native (Aspire, resilience, background services)
- AI integration (Semantic Kernel)
- Architecture patterns

## Out of scope
- C# language features -> [skill:dotnet-csharp]
- UI rendering -> [skill:dotnet-ui]
- Test authoring -> [skill:dotnet-testing]
- CI/CD pipelines -> [skill:dotnet-devops]
- Build tooling -> [skill:dotnet-tooling]

## Companion Files
- `references/minimal-apis.md` -- Minimal API route groups, filters, TypedResults, OpenAPI
- `references/middleware-patterns.md` -- Pipeline ordering, short-circuit, exception handling
- `references/efcore-patterns.md` -- DbContext, AsNoTracking, query splitting
- `references/efcore-architecture.md` -- Read/write split, aggregate boundaries, N+1
- `references/data-access-strategy.md` -- EF Core vs Dapper vs ADO.NET decision matrix
- `references/grpc.md` -- Proto definition, code-gen, ASP.NET Core host, streaming
- `references/realtime-communication.md` -- SignalR hubs, SSE, JSON-RPC 2.0, scaling
- `references/resilience.md` -- Polly v8 retry, circuit breaker, timeout, rate limiter
- `references/http-client.md` -- IHttpClientFactory, typed/named clients, DelegatingHandlers
- `references/api-versioning.md` -- Asp.Versioning.Http/Mvc, URL/header/query, sunset
- `references/openapi.md` -- MS.AspNetCore.OpenApi, Swashbuckle migration, NSwag
- `references/api-security.md` -- Identity, OAuth/OIDC, JWT bearer, CORS, rate limiting
- `references/security-owasp.md` -- OWASP Top 10 hardening for .NET
- `references/secrets-management.md` -- User secrets, environment variables, rotation
- `references/cryptography.md` -- AES-GCM, RSA, ECDSA, hashing, PQC key derivation
- `references/background-services.md` -- BackgroundService, IHostedService, lifecycle
- `references/aspire-patterns.md` -- AppHost, service discovery, components, dashboard
- `references/semantic-kernel.md` -- AI/LLM plugins, prompt templates, memory, agents
- `references/architecture-patterns.md` -- Vertical slices, layered, pipelines, caching
- `references/messaging-patterns.md` -- MassTransit, Azure Service Bus, pub/sub, sagas
- `references/service-communication.md` -- REST vs gRPC vs SignalR decision matrix
- `references/api-surface-validation.md` -- PublicApiAnalyzers, Verify snapshots, ApiCompat
- `references/library-api-compat.md` -- Binary/source compat, type forwarders, SemVer
- `references/io-pipelines.md` -- PipeReader/PipeWriter, backpressure, Kestrel
- `references/agent-gotchas.md` -- Common agent mistakes in .NET code
- `references/file-based-apps.md` -- .NET 10 file-based C# apps
- `references/api-docs.md` -- DocFX, OpenAPI-as-docs, versioned documentation
```

---

## Target Skill 3: dotnet-ui

### Routing Description (~370 chars)

Builds .NET UI applications across all frameworks. Covers Blazor (patterns, components, auth, testing), MAUI (development, AOT, testing), Uno Platform (core, targets, MCP, testing), WPF (modern and migration), WinUI 3, WinForms, accessibility, localization, and UI framework selection. Includes XAML, MVVM, render modes, and platform-specific deployment.

### Source Skills (18)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-blazor-patterns` | `references/blazor-patterns.md` | |
| 2 | `dotnet-blazor-components` | `references/blazor-components.md` | |
| 3 | `dotnet-blazor-auth` | `references/blazor-auth.md` | Blazor auth flows (per epic spec grouping) |
| 4 | `dotnet-blazor-testing` | `references/blazor-testing.md` | |
| 5 | `dotnet-maui-development` | `references/maui-development.md` | Has existing `examples.md` |
| 6 | `dotnet-maui-aot` | `references/maui-aot.md` | |
| 7 | `dotnet-maui-testing` | `references/maui-testing.md` | |
| 8 | `dotnet-uno-platform` | `references/uno-platform.md` | |
| 9 | `dotnet-uno-targets` | `references/uno-targets.md` | |
| 10 | `dotnet-uno-mcp` | `references/uno-mcp.md` | |
| 11 | `dotnet-uno-testing` | `references/uno-testing.md` | |
| 12 | `dotnet-wpf-modern` | `references/wpf-modern.md` | |
| 13 | `dotnet-wpf-migration` | `references/wpf-migration.md` | |
| 14 | `dotnet-winui` | `references/winui.md` | |
| 15 | `dotnet-winforms-basics` | `references/winforms-basics.md` | |
| 16 | `dotnet-accessibility` | `references/accessibility.md` | |
| 17 | `dotnet-localization` | `references/localization.md` | |
| 18 | `dotnet-ui-chooser` | `references/ui-chooser.md` | Was user-invocable |

### Edge Case Rationale

- **dotnet-blazor-auth** here (per epic spec): The epic groups Blazor auth under dotnet-ui ("Blazor: patterns, components, auth, testing"). Auth UI patterns (AuthorizeView, login/logout flows) are Blazor-specific; server-side auth middleware config is cross-referenced from [skill:dotnet-api].
- **dotnet-blazor-testing**, **dotnet-maui-testing**, **dotnet-uno-testing** here (not dotnet-testing): Framework-specific test setup belongs with the framework. dotnet-testing covers strategy and framework-agnostic patterns.
- **dotnet-ui-testing-core** NOT here (-> dotnet-testing): Per epic spec, "UI testing core" is listed under dotnet-testing. Cross-framework test patterns (page objects, selectors, async waits) are testing methodology.
- **dotnet-localization** here: Resource files and IStringLocalizer are primarily UI-facing.

### SKILL.md Content Outline

```
---
name: dotnet-ui
description: <routing description above, ~370 chars>
license: MIT
user-invocable: true
---

# dotnet-ui

## Overview
.NET UI development across Blazor, MAUI, Uno, WPF, WinUI, and WinForms.

## Routing Table
| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Blazor patterns | hosting model, render mode, routing | references/blazor-patterns.md |
| Blazor components | lifecycle, state, JS interop, EditForm | references/blazor-components.md |
| Blazor auth | AuthorizeView, Identity UI, OIDC flows | references/blazor-auth.md |
| Blazor testing | bUnit, rendering, events, JS mocking | references/blazor-testing.md |
| MAUI development | project structure, XAML, MVVM, platform | references/maui-development.md |
| MAUI AOT | iOS/Catalyst, Native AOT, trimming | references/maui-aot.md |
| MAUI testing | Appium, XHarness, platform validation | references/maui-testing.md |
| Uno Platform | Extensions, MVUX, Toolkit, Hot Reload | references/uno-platform.md |
| Uno targets | WASM, iOS, Android, macOS, Windows, Linux | references/uno-targets.md |
| Uno MCP | tool detection, search-then-fetch, init | references/uno-mcp.md |
| Uno testing | Playwright WASM, platform patterns | references/uno-testing.md |
| WPF modern | Host builder, MVVM Toolkit, Fluent theme | references/wpf-modern.md |
| WPF migration | WPF/WinForms to .NET 8+, UWP to WinUI | references/wpf-migration.md |
| WinUI | Windows App SDK, XAML, MSIX/unpackaged | references/winui.md |
| WinForms | high-DPI, dark mode, DI, modernization | references/winforms-basics.md |
| Accessibility | SemanticProperties, ARIA, AutomationPeer | references/accessibility.md |
| Localization | .resx, IStringLocalizer, pluralization, RTL | references/localization.md |
| UI chooser | framework selection decision tree | references/ui-chooser.md |

## Scope
- Blazor (Server, WASM, Hybrid, Auto)
- MAUI mobile/desktop
- Uno Platform cross-platform
- WPF, WinUI 3, WinForms
- Accessibility and localization
- UI testing (bUnit, Appium, Playwright WASM)

## Out of scope
- Server-side auth middleware config -> [skill:dotnet-api]
- Non-UI testing (unit, integration) -> [skill:dotnet-testing]
- Backend patterns -> [skill:dotnet-api]

## Companion Files
- `references/blazor-patterns.md` -- Hosting models, render modes, routing, streaming, prerender
- `references/blazor-components.md` -- Lifecycle, state management, JS interop, EditForm, QuickGrid
- `references/blazor-auth.md` -- Login/logout, AuthorizeView, Identity UI, OIDC
- `references/blazor-testing.md` -- bUnit rendering, events, cascading params, JS interop mocking
- `references/maui-development.md` -- Project structure, XAML/MVVM, platform services
- `references/maui-aot.md` -- iOS/Catalyst Native AOT, size/startup gains, library gaps
- `references/maui-testing.md` -- Appium device automation, XHarness, platform validation
- `references/uno-platform.md` -- Extensions, MVUX, Toolkit controls, Hot Reload
- `references/uno-targets.md` -- Per-target guidance for WASM, iOS, Android, macOS, Windows, Linux
- `references/uno-mcp.md` -- Tool detection, search-then-fetch workflow, init rules
- `references/uno-testing.md` -- Playwright for WASM, platform-specific patterns
- `references/wpf-modern.md` -- Host builder, MVVM Toolkit, Fluent theme, performance
- `references/wpf-migration.md` -- WPF/WinForms to .NET 8+, WPF to WinUI or Uno
- `references/winui.md` -- Windows App SDK, XAML patterns, MSIX/unpackaged, UWP migration
- `references/winforms-basics.md` -- High-DPI, dark mode, DI patterns, modernization
- `references/accessibility.md` -- SemanticProperties, ARIA, AutomationPeer, testing per platform
- `references/localization.md` -- .resx resources, IStringLocalizer, source generators, pluralization
- `references/ui-chooser.md` -- Decision tree across Blazor, MAUI, Uno, WinUI, WPF, WinForms
```

### User-Invocable Rationale

`dotnet-ui` is user-invocable because it absorbs `dotnet-ui-chooser` (user-invocable: true), which users invoke to select a UI framework.

---

## Target Skill 4: dotnet-testing

### Routing Description (~360 chars)

Defines .NET testing strategy and practices. Covers test architecture (unit vs integration vs E2E decision tree), xUnit v3 authoring, integration testing (WebApplicationFactory, Testcontainers, Aspire), snapshot testing (Verify), Playwright browser automation, BenchmarkDotNet microbenchmarks, CI benchmark gating, test quality metrics (Coverlet, Stryker.NET), UI testing core patterns, and test doubles patterns.

### Source Skills (12)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-testing-strategy` | `references/testing-strategy.md` | |
| 2 | `dotnet-xunit` | `references/xunit.md` | |
| 3 | `dotnet-integration-testing` | `references/integration-testing.md` | |
| 4 | `dotnet-snapshot-testing` | `references/snapshot-testing.md` | |
| 5 | `dotnet-playwright` | `references/playwright.md` | |
| 6 | `dotnet-benchmarkdotnet` | `references/benchmarkdotnet.md` | |
| 7 | `dotnet-ci-benchmarking` | `references/ci-benchmarking.md` | |
| 8 | `dotnet-test-quality` | `references/test-quality.md` | |
| 9 | `dotnet-add-testing` | `references/add-testing.md` | Was user-invocable (scaffold) |
| 10 | `dotnet-slopwatch` | `references/slopwatch.md` | Was user-invocable |
| 11 | `dotnet-aot-wasm` | `references/aot-wasm.md` | WASM AOT testing context |
| 12 | `dotnet-ui-testing-core` | `references/ui-testing-core.md` | Per epic spec: UI testing core in testing |

### Edge Case Rationale

- **dotnet-blazor-testing** NOT here (-> dotnet-ui): Blazor component testing (bUnit) is framework-specific, belongs with UI.
- **dotnet-maui-testing**, **dotnet-uno-testing** NOT here (-> dotnet-ui): Same reasoning as above.
- **dotnet-ui-testing-core** here (per epic spec): The epic explicitly lists "UI testing core" under dotnet-testing. Cross-framework test patterns (page objects, selectors, async waits) are testing methodology, not UI-framework-specific.
- **dotnet-add-testing** here: Scaffolding test infrastructure is a testing concern.
- **dotnet-slopwatch** here: Quality analysis tool, natural fit with test quality.
- **dotnet-aot-wasm** here (not dotnet-tooling): While AOT is tooling-adjacent, WASM AOT compilation is specifically about testing Blazor/Uno WASM size and startup, closely tied to test/benchmark context. However, this is a borderline call -- see Edge Cases section.

### SKILL.md Content Outline

```
---
name: dotnet-testing
description: <routing description above, ~360 chars>
license: MIT
user-invocable: false
---

# dotnet-testing

## Overview
Testing strategy, frameworks, and quality tooling for .NET applications.

## Routing Table
| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Strategy | unit vs integration vs E2E, test doubles | references/testing-strategy.md |
| xUnit | Facts, Theories, fixtures, parallelism | references/xunit.md |
| Integration | WebApplicationFactory, Testcontainers, Aspire | references/integration-testing.md |
| Snapshot | Verify, scrubbing, API responses | references/snapshot-testing.md |
| Playwright | E2E browser, CI caching, trace viewer | references/playwright.md |
| BenchmarkDotNet | microbenchmarks, memory diagnosers | references/benchmarkdotnet.md |
| CI benchmarking | threshold alerts, baseline tracking | references/ci-benchmarking.md |
| Test quality | Coverlet, Stryker.NET, flaky tests | references/test-quality.md |
| Add testing | scaffold xUnit project, coverlet, layout | references/add-testing.md |
| Slopwatch | LLM reward hacking detection | references/slopwatch.md |
| AOT WASM | Blazor/Uno WASM AOT, size, lazy loading | references/aot-wasm.md |
| UI testing core | page objects, selectors, async waits | references/ui-testing-core.md |

## Scope
- Test strategy and architecture
- xUnit v3 test authoring
- Integration testing (WebApplicationFactory, Testcontainers)
- E2E browser testing (Playwright)
- Snapshot testing (Verify)
- Benchmarking (BenchmarkDotNet, CI gating)
- Quality (coverage, mutation testing)
- Cross-framework UI testing patterns
- Test scaffolding

## Out of scope
- UI framework-specific testing (bUnit, Appium) -> [skill:dotnet-ui]
- CI/CD pipeline configuration -> [skill:dotnet-devops]
- Performance profiling -> [skill:dotnet-tooling]

## Companion Files
- `references/testing-strategy.md` -- Unit vs integration vs E2E decision tree, test doubles
- `references/xunit.md` -- xUnit v3 Facts, Theories, fixtures, parallelism, IAsyncLifetime
- `references/integration-testing.md` -- WebApplicationFactory, Testcontainers, Aspire, fixtures
- `references/snapshot-testing.md` -- Verify complex outputs, scrubbing non-deterministic values
- `references/playwright.md` -- Playwright E2E, CI browser caching, trace viewer, codegen
- `references/benchmarkdotnet.md` -- Setup, memory diagnosers, baselines, result analysis
- `references/ci-benchmarking.md` -- Automated threshold alerts, baseline tracking, trend reports
- `references/test-quality.md` -- Coverlet code coverage, Stryker.NET mutation testing, flaky tests
- `references/add-testing.md` -- Scaffold xUnit project, coverlet, test layout
- `references/slopwatch.md` -- Slopwatch CLI for LLM reward hacking detection
- `references/aot-wasm.md` -- Blazor/Uno WASM AOT compilation, size vs speed, lazy loading
- `references/ui-testing-core.md` -- Page objects, test selectors, async waits, accessibility
```

---

## Target Skill 5: dotnet-devops

### Routing Description (~380 chars)

Configures CI/CD pipelines, packaging, and operational tooling for .NET. Covers GitHub Actions (build/test, deploy, publish, patterns), Azure DevOps (build/test, publish, patterns, environments), containers (Dockerfiles, deployment), NuGet authoring, MSIX packaging, GitHub Releases, release management (NBGV, SemVer), observability (OpenTelemetry), and structured logging pipelines.

### Source Skills (18)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-gha-build-test` | `references/gha-build-test.md` | |
| 2 | `dotnet-gha-deploy` | `references/gha-deploy.md` | |
| 3 | `dotnet-gha-publish` | `references/gha-publish.md` | |
| 4 | `dotnet-gha-patterns` | `references/gha-patterns.md` | |
| 5 | `dotnet-ado-build-test` | `references/ado-build-test.md` | |
| 6 | `dotnet-ado-publish` | `references/ado-publish.md` | |
| 7 | `dotnet-ado-patterns` | `references/ado-patterns.md` | Has existing `examples.md` |
| 8 | `dotnet-ado-unique` | `references/ado-unique.md` | |
| 9 | `dotnet-containers` | `references/containers.md` | |
| 10 | `dotnet-container-deployment` | `references/container-deployment.md` | |
| 11 | `dotnet-nuget-authoring` | `references/nuget-authoring.md` | |
| 12 | `dotnet-msix` | `references/msix.md` | |
| 13 | `dotnet-github-releases` | `references/github-releases.md` | |
| 14 | `dotnet-release-management` | `references/release-management.md` | |
| 15 | `dotnet-observability` | `references/observability.md` | Has existing `examples.md` |
| 16 | `dotnet-structured-logging` | `references/structured-logging.md` | |
| 17 | `dotnet-add-ci` | `references/add-ci.md` | Was user-invocable |
| 18 | `dotnet-github-docs` | `references/github-docs.md` | README, CONTRIBUTING, templates |

### Edge Case Rationale

- **dotnet-observability** here (not dotnet-api): While observability is configured in API code, the concern is operational (OTel, health checks, metrics export) and aligns with DevOps.
- **dotnet-structured-logging** here (not dotnet-api): Log pipeline design (aggregation, sampling, PII) is operational.
- **dotnet-github-docs** here: GitHub-native docs (README, CONTRIBUTING, templates) are repo DevOps concerns.
- **dotnet-nuget-authoring** here (not dotnet-tooling): NuGet publishing is a packaging/release concern.
- **dotnet-add-ci** here: CI scaffolding is a DevOps concern.

### SKILL.md Content Outline

```
---
name: dotnet-devops
description: <routing description above, ~380 chars>
license: MIT
user-invocable: false
---

# dotnet-devops

## Overview
CI/CD, packaging, release management, and operational tooling for .NET.

## Routing Table
| Topic | Keywords | Companion File |
|-------|----------|----------------|
| GHA build/test | setup-dotnet, NuGet cache, reporting | references/gha-build-test.md |
| GHA deploy | Azure Web Apps, GitHub Pages, containers | references/gha-deploy.md |
| GHA publish | NuGet push, container images, signing, SBOM | references/gha-publish.md |
| GHA patterns | reusable workflows, composite, matrix, cache | references/gha-patterns.md |
| ADO build/test | DotNetCoreCLI, Artifacts, test results | references/ado-build-test.md |
| ADO publish | NuGet push, containers to ACR | references/ado-publish.md |
| ADO patterns | templates, variable groups, multi-stage | references/ado-patterns.md |
| ADO unique | environments, approvals, service connections | references/ado-unique.md |
| Containers | multi-stage Dockerfiles, SDK publish, rootless | references/containers.md |
| Container deployment | Compose, health probes, CI/CD pipelines | references/container-deployment.md |
| NuGet authoring | SDK-style, source generators, multi-TFM | references/nuget-authoring.md |
| MSIX | creation, signing, Store, sideload, auto-update | references/msix.md |
| GitHub Releases | creation, assets, notes, pre-release | references/github-releases.md |
| Release management | NBGV, SemVer, changelogs, branching | references/release-management.md |
| Observability | OpenTelemetry, health checks, custom metrics | references/observability.md |
| Structured logging | aggregation, sampling, PII, correlation | references/structured-logging.md |
| Add CI | CI/CD scaffold, GHA vs ADO detection | references/add-ci.md |
| GitHub docs | README badges, CONTRIBUTING, templates | references/github-docs.md |

## Scope
- GitHub Actions workflows
- Azure DevOps pipelines
- Container builds and deployment
- NuGet/MSIX packaging
- Release management (NBGV, SemVer, changelogs)
- Observability (OpenTelemetry, health checks)
- Structured logging
- GitHub repository documentation

## Out of scope
- API/backend code patterns -> [skill:dotnet-api]
- Build system authoring -> [skill:dotnet-tooling]
- Test authoring -> [skill:dotnet-testing]

## Companion Files
- `references/gha-build-test.md` -- GitHub Actions .NET build/test, setup-dotnet, NuGet cache
- `references/gha-deploy.md` -- Deploy from GHA to Azure, GitHub Pages, container registries
- `references/gha-publish.md` -- NuGet push, container images, signing, SBOM from GHA
- `references/gha-patterns.md` -- Reusable workflows, composite actions, matrix, caching
- `references/ado-build-test.md` -- Azure DevOps .NET build/test, DotNetCoreCLI task
- `references/ado-publish.md` -- NuGet push, containers to ACR from ADO
- `references/ado-patterns.md` -- YAML pipelines, templates, variable groups, multi-stage
- `references/ado-unique.md` -- Environments, approvals, service connections, pipelines
- `references/containers.md` -- Multi-stage Dockerfiles, SDK container publish, rootless
- `references/container-deployment.md` -- Compose, health probes, CI/CD image pipelines
- `references/nuget-authoring.md` -- SDK-style csproj, source generators, multi-TFM, symbols
- `references/msix.md` -- MSIX creation, signing, Store submission, sideload, auto-update
- `references/github-releases.md` -- Release creation, assets, notes, pre-release management
- `references/release-management.md` -- NBGV versioning, SemVer, changelogs, branching
- `references/observability.md` -- OpenTelemetry traces/metrics/logs, health checks
- `references/structured-logging.md` -- Aggregation, queries, sampling, PII scrubbing, correlation
- `references/add-ci.md` -- CI/CD scaffold, GitHub Actions vs Azure DevOps detection
- `references/github-docs.md` -- README badges, CONTRIBUTING, issue/PR templates
```

---

## Target Skill 6: dotnet-tooling

### Routing Description (~400 chars)

Manages .NET project setup, build systems, and developer tooling. Covers solution structure, MSBuild (authoring, tasks, Directory.Build), build optimization, performance patterns, profiling (dotnet-counters/trace/dump), Native AOT publishing, trimming, GC/memory tuning, CLI app architecture (System.CommandLine, Spectre.Console, Terminal.Gui), docs generation, tool management, version detection/upgrade, and solution navigation.

### Source Skills (32)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-project-structure` | `references/project-structure.md` | |
| 2 | `dotnet-scaffold-project` | `references/scaffold-project.md` | Was user-invocable |
| 3 | `dotnet-csproj-reading` | `references/csproj-reading.md` | |
| 4 | `dotnet-msbuild-authoring` | `references/msbuild-authoring.md` | |
| 5 | `dotnet-msbuild-tasks` | `references/msbuild-tasks.md` | Has existing `examples.md` |
| 6 | `dotnet-build-analysis` | `references/build-analysis.md` | context: fork, model: haiku (drop in consolidation) |
| 7 | `dotnet-build-optimization` | `references/build-optimization.md` | |
| 8 | `dotnet-artifacts-output` | `references/artifacts-output.md` | |
| 9 | `dotnet-multi-targeting` | `references/multi-targeting.md` | |
| 10 | `dotnet-performance-patterns` | `references/performance-patterns.md` | |
| 11 | `dotnet-profiling` | `references/profiling.md` | |
| 12 | `dotnet-native-aot` | `references/native-aot.md` | |
| 13 | `dotnet-aot-architecture` | `references/aot-architecture.md` | |
| 14 | `dotnet-trimming` | `references/trimming.md` | |
| 15 | `dotnet-gc-memory` | `references/gc-memory.md` | |
| 16 | `dotnet-cli-architecture` | `references/cli-architecture.md` | |
| 17 | `dotnet-system-commandline` | `references/system-commandline.md` | Has existing `examples.md` |
| 18 | `dotnet-spectre-console` | `references/spectre-console.md` | |
| 19 | `dotnet-terminal-gui` | `references/terminal-gui.md` | Has existing `examples.md` |
| 20 | `dotnet-cli-distribution` | `references/cli-distribution.md` | |
| 21 | `dotnet-cli-packaging` | `references/cli-packaging.md` | |
| 22 | `dotnet-cli-release-pipeline` | `references/cli-release-pipeline.md` | |
| 23 | `dotnet-documentation-strategy` | `references/documentation-strategy.md` | |
| 24 | `dotnet-xml-docs` | `references/xml-docs.md` | Has existing `examples.md` |
| 25 | `dotnet-tool-management` | `references/tool-management.md` | |
| 26 | `dotnet-version-detection` | `references/version-detection.md` | context: fork, model: haiku (drop in consolidation); has scripts/ |
| 27 | `dotnet-version-upgrade` | `references/version-upgrade.md` | Was user-invocable |
| 28 | `dotnet-solution-navigation` | `references/solution-navigation.md` | context: fork, model: haiku (drop in consolidation) |
| 29 | `dotnet-project-analysis` | `references/project-analysis.md` | context: fork, model: haiku (drop in consolidation) |
| 30 | `dotnet-modernize` | `references/modernize.md` | Was user-invocable |
| 31 | `dotnet-add-analyzers` | `references/add-analyzers.md` | Was user-invocable |
| 32 | `dotnet-mermaid-diagrams` | `references/mermaid-diagrams.md` | Has existing `examples.md` |

### SKILL.md Content Outline

```
---
name: dotnet-tooling
description: <routing description above, ~400 chars>
license: MIT
user-invocable: true
---

# dotnet-tooling

## Overview
.NET project setup, build systems, performance, CLI apps, and developer tooling.

## Routing Table
| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Project structure | solution, .slnx, CPM, analyzers | references/project-structure.md |
| Scaffold project | dotnet new, CPM, SourceLink, editorconfig | references/scaffold-project.md |
| Csproj reading | PropertyGroup, ItemGroup, CPM, props | references/csproj-reading.md |
| MSBuild authoring | targets, props, conditions, Directory.Build | references/msbuild-authoring.md |
| MSBuild tasks | ITask, ToolTask, inline tasks, UsingTask | references/msbuild-tasks.md |
| Build analysis | MSBuild output, NuGet errors, analyzer warnings | references/build-analysis.md |
| Build optimization | slow builds, binary logs, parallel, restore | references/build-optimization.md |
| Artifacts output | UseArtifactsOutput, ArtifactsPath, CI/Docker | references/artifacts-output.md |
| Multi-targeting | multiple TFMs, polyfills, conditional compilation | references/multi-targeting.md |
| Performance patterns | Span, ArrayPool, ref struct, sealed, stackalloc | references/performance-patterns.md |
| Profiling | dotnet-counters, dotnet-trace, flame graphs | references/profiling.md |
| Native AOT | PublishAot, ILLink, P/Invoke, size optimization | references/native-aot.md |
| AOT architecture | source gen, AOT-safe DI, serialization | references/aot-architecture.md |
| Trimming | annotations, ILLink, IL2xxx warnings, IsTrimmable | references/trimming.md |
| GC/memory | GC modes, LOH/POH, Span/Memory, ArrayPool | references/gc-memory.md |
| CLI architecture | command/handler/service, clig.dev, exit codes | references/cli-architecture.md |
| System.CommandLine | RootCommand, Option<T>, SetAction, parsing | references/system-commandline.md |
| Spectre.Console | tables, trees, progress, prompts, live displays | references/spectre-console.md |
| Terminal.Gui | views, layout, menus, dialogs, bindings, themes | references/terminal-gui.md |
| CLI distribution | AOT vs framework-dependent, RID matrix | references/cli-distribution.md |
| CLI packaging | Homebrew, apt/deb, winget, Scoop, Chocolatey | references/cli-packaging.md |
| CLI release pipeline | GHA build matrix, artifact staging, checksums | references/cli-release-pipeline.md |
| Documentation strategy | Starlight, Docusaurus, DocFX decision tree | references/documentation-strategy.md |
| XML docs | tags, inheritdoc, GenerateDocumentationFile | references/xml-docs.md |
| Tool management | global, local, manifests, restore, pinning | references/tool-management.md |
| Version detection | TFM/SDK from .csproj, global.json | references/version-detection.md |
| Version upgrade | LTS-to-LTS, staged, preview, upgrade paths | references/version-upgrade.md |
| Solution navigation | entry points, .sln/.slnx, dependency graphs | references/solution-navigation.md |
| Project analysis | solution layout, build config analysis | references/project-analysis.md |
| Modernize | outdated TFMs, deprecated packages, patterns | references/modernize.md |
| Add analyzers | nullable, trimming, AOT compat, severity config | references/add-analyzers.md |
| Mermaid diagrams | architecture, sequence, class, ER, flowcharts | references/mermaid-diagrams.md |

## Scope
- Solution structure and project scaffolding
- MSBuild authoring and build optimization
- Performance patterns and profiling
- Native AOT, trimming, GC tuning
- CLI app development (System.CommandLine, Spectre.Console, Terminal.Gui)
- Documentation generation (DocFX, XML docs)
- Tool management and version detection/upgrade
- Solution navigation and project analysis
- Code modernization

## Out of scope
- Web API patterns -> [skill:dotnet-api]
- Test authoring -> [skill:dotnet-testing]
- CI/CD pipelines -> [skill:dotnet-devops]

## Companion Files
- `references/project-structure.md` -- .slnx, Directory.Build.props, CPM, analyzers
- `references/scaffold-project.md` -- dotnet new with CPM, analyzers, editorconfig, SourceLink
- `references/csproj-reading.md` -- SDK-style .csproj, PropertyGroup, ItemGroup, CPM
- `references/msbuild-authoring.md` -- Targets, props, conditions, Directory.Build patterns
- `references/msbuild-tasks.md` -- ITask, ToolTask, IIncrementalTask, inline tasks
- `references/build-analysis.md` -- MSBuild output, NuGet errors, analyzer warnings
- `references/build-optimization.md` -- Slow builds, binary logs, parallel, restore
- `references/artifacts-output.md` -- UseArtifactsOutput, ArtifactsPath, CI/Docker impact
- `references/multi-targeting.md` -- Multiple TFMs, PolySharp, conditional compilation
- `references/performance-patterns.md` -- Span, ArrayPool, ref struct, sealed, stackalloc
- `references/profiling.md` -- dotnet-counters, dotnet-trace, dotnet-dump, flame graphs
- `references/native-aot.md` -- PublishAot, ILLink descriptors, P/Invoke, size optimization
- `references/aot-architecture.md` -- Source gen over reflection, AOT-safe DI, factories
- `references/trimming.md` -- Annotations, ILLink, IL2xxx warnings, IsTrimmable
- `references/gc-memory.md` -- GC modes, LOH/POH, Gen0/1/2, Span/Memory, ArrayPool
- `references/cli-architecture.md` -- Command/handler/service, clig.dev, exit codes
- `references/system-commandline.md` -- System.CommandLine 2.0, RootCommand, Option<T>
- `references/spectre-console.md` -- Tables, trees, progress, prompts, live displays
- `references/terminal-gui.md` -- Terminal.Gui v2, views, layout, menus, dialogs
- `references/cli-distribution.md` -- AOT vs framework-dependent, RID matrix, single-file
- `references/cli-packaging.md` -- Homebrew, apt/deb, winget, Scoop, Chocolatey
- `references/cli-release-pipeline.md` -- GHA build matrix, artifact staging, checksums
- `references/documentation-strategy.md` -- Starlight, Docusaurus, DocFX decision tree
- `references/xml-docs.md` -- XML doc comments, inheritdoc, warning suppression
- `references/tool-management.md` -- Global/local tools, manifests, restore, pinning
- `references/version-detection.md` -- TFM/SDK from .csproj, global.json, Directory.Build
- `references/version-upgrade.md` -- LTS-to-LTS, staged through STS, preview paths
- `references/solution-navigation.md` -- Entry points, .sln/.slnx, dependency graphs
- `references/project-analysis.md` -- Solution layout, build config, .csproj analysis
- `references/modernize.md` -- Outdated TFMs, deprecated packages, superseded patterns
- `references/add-analyzers.md` -- Nullable, trimming, AOT compat analyzers, severity
- `references/mermaid-diagrams.md` -- Architecture, sequence, class, deployment, ER diagrams
```

### User-Invocable Rationale

`dotnet-tooling` is user-invocable because it absorbs `dotnet-scaffold-project` (user-invocable: true), `dotnet-version-upgrade` (true), `dotnet-modernize` (true), and `dotnet-add-analyzers` (true).

---

## Target Skill 7: dotnet-debugging

### Routing Description (~350 chars)

Debugs Windows applications using WinDbg and crash dump analysis. Covers MCP server integration, live process attach, dump file triage, crash analysis, hang detection, high-CPU diagnosis, memory leak investigation, kernel debugging, symbol configuration, scenario command packs, diagnostic report generation, and SOS extension workflows for .NET runtime inspection.

### Source Skills (1)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-windbg-debugging` | (identity -- stays as-is with rename) | Existing `reference/` dir (16 files) -> rename to `references/` |

### Existing Companion Files (migrate reference/ -> references/)

The existing `reference/` directory contains 16 files that must be renamed to `references/`:

| Current Path | New Path |
|-------------|----------|
| `reference/access-mcp.md` | `references/access-mcp.md` |
| `reference/capture-playbooks.md` | `references/capture-playbooks.md` |
| `reference/common-patterns.md` | `references/common-patterns.md` |
| `reference/dump-workflow.md` | `references/dump-workflow.md` |
| `reference/live-attach.md` | `references/live-attach.md` |
| `reference/mcp-setup.md` | `references/mcp-setup.md` |
| `reference/report-template.md` | `references/report-template.md` |
| `reference/sanity-check.md` | `references/sanity-check.md` |
| `reference/scenario-command-packs.md` | `references/scenario-command-packs.md` |
| `reference/symbols.md` | `references/symbols.md` |
| `reference/task-crash.md` | `references/task-crash.md` |
| `reference/task-hang.md` | `references/task-hang.md` |
| `reference/task-high-cpu.md` | `references/task-high-cpu.md` |
| `reference/task-kernel.md` | `references/task-kernel.md` |
| `reference/task-memory.md` | `references/task-memory.md` |
| `reference/task-unknown.md` | `references/task-unknown.md` |

### SKILL.md Content Outline

```
---
name: dotnet-debugging
description: <routing description above, ~350 chars>
license: MIT
user-invocable: true
---

# dotnet-debugging

(Mostly identical to current dotnet-windbg-debugging SKILL.md,
 with reference/ paths updated to references/)
```

---

## Target Skill 8: dotnet-advisor

### Routing Description (~300 chars)

Routes .NET and C# work to the correct domain skill. Analyzes the task, loads dotnet-csharp (coding standards) for code paths, then dispatches to the appropriate skill among dotnet-csharp, dotnet-api, dotnet-ui, dotnet-testing, dotnet-devops, dotnet-tooling, or dotnet-debugging based on task domain.

### Source Skills (1)

| # | Source Skill | References/ Topic | Notes |
|---|-------------|-------------------|-------|
| 1 | `dotnet-advisor` | (identity -- rewrite routing catalog) | Hooks inject as mandatory first action |

### SKILL.md Content Outline

```
---
name: dotnet-advisor
description: <routing description above, ~300 chars>
license: MIT
user-invocable: true
---

# dotnet-advisor

## Immediate Routing Actions (Do First)
1. Invoke [skill:dotnet-csharp] (read references/coding-standards.md) for any code path
2. Route to domain skill based on task analysis

## Routing Catalog

| Domain | Skill | When to Route |
|--------|-------|---------------|
| C# language | [skill:dotnet-csharp] | Language patterns, coding standards, DI, config, async |
| Backend/API | [skill:dotnet-api] | ASP.NET Core, EF Core, security, Aspire, architecture |
| UI | [skill:dotnet-ui] | Blazor, MAUI, Uno, WPF, WinUI, WinForms |
| Testing | [skill:dotnet-testing] | xUnit, integration tests, benchmarks, quality |
| DevOps | [skill:dotnet-devops] | CI/CD, containers, NuGet, releases, observability |
| Tooling | [skill:dotnet-tooling] | Build, MSBuild, perf, AOT, CLI apps, version mgmt |
| Debugging | [skill:dotnet-debugging] | WinDbg, crash dumps, live attach |

## Default Quality Rule
Always invoke [skill:dotnet-csharp] for code paths to ensure coding standards compliance.

## Scope
- Task analysis and skill routing
- Coding standards enforcement

## Out of scope
- Direct implementation (delegates to domain skills)
```

---

## Edge Cases

### 1. Cross-Cutting Skills

| Skill | Could fit in | Assigned to | Rationale |
|-------|-------------|-------------|-----------|
| `dotnet-agent-gotchas` | csharp, api, tooling | **dotnet-api** | Most gotchas are API/backend (async, DI, NuGet). C# is language-only. |
| `dotnet-blazor-auth` | api, ui | **dotnet-ui** | Epic spec groups under "Blazor (patterns, components, auth, testing)". Auth UI patterns are Blazor-specific. |
| `dotnet-ui-testing-core` | ui, testing | **dotnet-testing** | Epic spec lists "UI testing core" under dotnet-testing. Cross-framework test methodology. |
| `dotnet-aot-wasm` | testing, tooling, ui | **dotnet-testing** | WASM AOT is about size/startup benchmarking. UI has maui-aot separately. |
| `dotnet-file-based-apps` | api, tooling, csharp | **dotnet-api** | .NET 10 app model, closely aligned with Minimal APIs. |
| `dotnet-io-pipelines` | api, csharp | **dotnet-api** | High-perf Kestrel I/O is server/API territory. |
| `dotnet-localization` | ui, csharp | **dotnet-ui** | IStringLocalizer is primarily UI-facing. |
| `dotnet-observability` | api, devops | **dotnet-devops** | Operational concern (OTel export, health checks). |
| `dotnet-structured-logging` | api, devops | **dotnet-devops** | Log pipeline design is operational. |
| `dotnet-api-docs` | api, tooling | **dotnet-api** | DocFX, OpenAPI-as-docs are API documentation. |
| `dotnet-documentation-strategy` | tooling, devops | **dotnet-tooling** | Tooling for choosing doc generators. |
| `dotnet-mermaid-diagrams` | tooling, any | **dotnet-tooling** | Diagram generation is a developer tool. |
| `dotnet-github-docs` | devops, tooling | **dotnet-devops** | README/CONTRIBUTING/templates are repo-ops. |
| `dotnet-slopwatch` | testing, tooling | **dotnet-testing** | Quality analysis tool alongside coverage/mutation. |
| `dotnet-library-api-compat` | api, tooling | **dotnet-api** | API compatibility is an API contract concern. |
| `dotnet-api-surface-validation` | api, testing | **dotnet-api** | API surface detection is API design concern. |

### 2. User-Invocable Assignments

11 source skills are currently user-invocable. Their target skill assignments:

| Source Skill (user-invocable) | Target Skill | Target Gets user-invocable? |
|------------------------------|-------------|---------------------------|
| `dotnet-advisor` | dotnet-advisor | **Yes** (identity) |
| `dotnet-windbg-debugging` | dotnet-debugging | **Yes** (identity) |
| `dotnet-ui-chooser` | dotnet-ui | **Yes** |
| `dotnet-scaffold-project` | dotnet-tooling | **Yes** |
| `dotnet-version-upgrade` | dotnet-tooling | (already Yes via scaffold-project) |
| `dotnet-modernize` | dotnet-tooling | (already Yes) |
| `dotnet-add-analyzers` | dotnet-tooling | (already Yes) |
| `dotnet-data-access-strategy` | dotnet-api | No -- data access strategy is a design decision, not user-initiated action |
| `dotnet-add-ci` | dotnet-devops | No -- CI scaffolding is model-initiated |
| `dotnet-add-testing` | dotnet-testing | No -- test scaffolding is model-initiated |
| `dotnet-slopwatch` | dotnet-testing | No -- Slopwatch is model-initiated quality check |

**Result**: 4 of 8 target skills are user-invocable: dotnet-advisor, dotnet-debugging, dotnet-ui, dotnet-tooling.

**Rationale for non-user-invocable targets**:
- **dotnet-csharp**: Language guidance is model-loaded, not user-invoked.
- **dotnet-api**: Backend patterns are model-loaded.
- **dotnet-testing**: Test patterns are model-loaded (add-testing was scaffolding, but the broader skill is guidance).
- **dotnet-devops**: CI/CD guidance is model-loaded.

### 3. Skills with context: fork and model: haiku

4 source skills have special frontmatter that affects execution context:

| Source Skill | Frontmatter | Target Skill | Migration Note |
|-------------|-------------|-------------|----------------|
| `dotnet-build-analysis` | context: fork, model: haiku | dotnet-tooling | Drop context/model -- consolidated skill loads normally |
| `dotnet-project-analysis` | context: fork, model: haiku | dotnet-tooling | Drop context/model |
| `dotnet-solution-navigation` | context: fork, model: haiku | dotnet-tooling | Drop context/model |
| `dotnet-version-detection` | context: fork, model: haiku | dotnet-tooling | Drop context/model; migrate scripts/ to references/ or keep as scripts/ |

**Decision**: The `context: fork` and `model: haiku` attributes were designed for lightweight auto-detection skills that run in isolation. In the consolidated model, these become companion reference files read on demand. The fork/haiku semantics do not transfer to the parent skill.

**Special case: dotnet-version-detection/scripts/scan-dotnet-targets.py** -- this is an executable script, not documentation. It should be preserved as `scripts/scan-dotnet-targets.py` within the dotnet-tooling skill directory (not in references/).

---

## Companion File Naming Convention

- **Directory**: `references/` (plural, not `reference/`)
- **File naming**: `<topic>.md` where topic is the distinctive part of the source skill name
  - `dotnet-csharp-async-patterns` -> `references/async-patterns.md`
  - `dotnet-efcore-patterns` -> `references/efcore-patterns.md`
  - `dotnet-blazor-components` -> `references/blazor-components.md`
- **Existing companion files** (details.md, examples.md): Content merged into the topic reference file
  - `dotnet-roslyn-analyzers/details.md` -> merged into `dotnet-csharp/references/roslyn-analyzers.md`
  - `dotnet-grpc/examples.md` -> merged into `dotnet-api/references/grpc.md`
- **Existing scripts/**: Preserved as `scripts/` (not references/)
  - `dotnet-version-detection/scripts/scan-dotnet-targets.py` -> `dotnet-tooling/scripts/scan-dotnet-targets.py`

---

## Existing Companion File Migration

| Source Skill | Existing File | Target Skill | Migration Target |
|-------------|--------------|-------------|-----------------|
| `dotnet-ado-patterns` | `examples.md` (15K) | dotnet-devops | Merge into `references/ado-patterns.md` |
| `dotnet-architecture-patterns` | `examples.md` (19K) | dotnet-api | Merge into `references/architecture-patterns.md` |
| `dotnet-csharp-code-smells` | `details.md` (10K) | dotnet-csharp | Merge into `references/code-smells.md` |
| `dotnet-grpc` | `examples.md` (14K) | dotnet-api | Merge into `references/grpc.md` |
| `dotnet-maui-development` | `examples.md` (19K) | dotnet-ui | Merge into `references/maui-development.md` |
| `dotnet-mermaid-diagrams` | `examples.md` (19K) | dotnet-tooling | Merge into `references/mermaid-diagrams.md` |
| `dotnet-msbuild-tasks` | `examples.md` (19K) | dotnet-tooling | Merge into `references/msbuild-tasks.md` |
| `dotnet-observability` | `examples.md` (20K) | dotnet-devops | Merge into `references/observability.md` |
| `dotnet-roslyn-analyzers` | `details.md` (12K) | dotnet-csharp | Merge into `references/roslyn-analyzers.md` |
| `dotnet-system-commandline` | `examples.md` (12K) | dotnet-tooling | Merge into `references/system-commandline.md` |
| `dotnet-terminal-gui` | `examples.md` (7.8K) | dotnet-tooling | Merge into `references/terminal-gui.md` |
| `dotnet-version-detection` | `scripts/scan-dotnet-targets.py` | dotnet-tooling | Keep as `scripts/scan-dotnet-targets.py` |
| `dotnet-windbg-debugging` | `reference/` (16 files) | dotnet-debugging | Rename dir to `references/` |
| `dotnet-xml-docs` | `examples.md` (18K) | dotnet-tooling | Merge into `references/xml-docs.md` |

---

## Verification

### Assignment completeness check

Total source skills: 131
- dotnet-csharp: 22
- dotnet-api: 28
- dotnet-ui: 18
- dotnet-testing: 11
- dotnet-devops: 18
- dotnet-tooling: 32
- dotnet-debugging: 1 (identity)
- dotnet-advisor: 1 (identity)
- **Total: 131** (verified -- no skill left unassigned)

### Full assignment roster (alphabetical by source skill)

| Source Skill | Target Skill |
|-------------|-------------|
| dotnet-accessibility | dotnet-ui |
| dotnet-add-analyzers | dotnet-tooling |
| dotnet-add-ci | dotnet-devops |
| dotnet-add-testing | dotnet-testing |
| dotnet-ado-build-test | dotnet-devops |
| dotnet-ado-patterns | dotnet-devops |
| dotnet-ado-publish | dotnet-devops |
| dotnet-ado-unique | dotnet-devops |
| dotnet-advisor | dotnet-advisor |
| dotnet-agent-gotchas | dotnet-api |
| dotnet-aot-architecture | dotnet-tooling |
| dotnet-aot-wasm | dotnet-testing |
| dotnet-api-docs | dotnet-api |
| dotnet-api-security | dotnet-api |
| dotnet-api-surface-validation | dotnet-api |
| dotnet-api-versioning | dotnet-api |
| dotnet-architecture-patterns | dotnet-api |
| dotnet-artifacts-output | dotnet-tooling |
| dotnet-aspire-patterns | dotnet-api |
| dotnet-background-services | dotnet-api |
| dotnet-benchmarkdotnet | dotnet-testing |
| dotnet-blazor-auth | dotnet-ui |
| dotnet-blazor-components | dotnet-ui |
| dotnet-blazor-patterns | dotnet-ui |
| dotnet-blazor-testing | dotnet-ui |
| dotnet-build-analysis | dotnet-tooling |
| dotnet-build-optimization | dotnet-tooling |
| dotnet-channels | dotnet-csharp |
| dotnet-ci-benchmarking | dotnet-testing |
| dotnet-cli-architecture | dotnet-tooling |
| dotnet-cli-distribution | dotnet-tooling |
| dotnet-cli-packaging | dotnet-tooling |
| dotnet-cli-release-pipeline | dotnet-tooling |
| dotnet-container-deployment | dotnet-devops |
| dotnet-containers | dotnet-devops |
| dotnet-cryptography | dotnet-api |
| dotnet-csharp-api-design | dotnet-csharp |
| dotnet-csharp-async-patterns | dotnet-csharp |
| dotnet-csharp-code-smells | dotnet-csharp |
| dotnet-csharp-coding-standards | dotnet-csharp |
| dotnet-csharp-concurrency-patterns | dotnet-csharp |
| dotnet-csharp-configuration | dotnet-csharp |
| dotnet-csharp-dependency-injection | dotnet-csharp |
| dotnet-csharp-modern-patterns | dotnet-csharp |
| dotnet-csharp-nullable-reference-types | dotnet-csharp |
| dotnet-csharp-source-generators | dotnet-csharp |
| dotnet-csharp-type-design-performance | dotnet-csharp |
| dotnet-csproj-reading | dotnet-tooling |
| dotnet-data-access-strategy | dotnet-api |
| dotnet-documentation-strategy | dotnet-tooling |
| dotnet-domain-modeling | dotnet-csharp |
| dotnet-editorconfig | dotnet-csharp |
| dotnet-efcore-architecture | dotnet-api |
| dotnet-efcore-patterns | dotnet-api |
| dotnet-file-based-apps | dotnet-api |
| dotnet-file-io | dotnet-csharp |
| dotnet-gc-memory | dotnet-tooling |
| dotnet-gha-build-test | dotnet-devops |
| dotnet-gha-deploy | dotnet-devops |
| dotnet-gha-patterns | dotnet-devops |
| dotnet-gha-publish | dotnet-devops |
| dotnet-github-docs | dotnet-devops |
| dotnet-github-releases | dotnet-devops |
| dotnet-grpc | dotnet-api |
| dotnet-http-client | dotnet-api |
| dotnet-input-validation | dotnet-csharp |
| dotnet-integration-testing | dotnet-testing |
| dotnet-io-pipelines | dotnet-api |
| dotnet-library-api-compat | dotnet-api |
| dotnet-linq-optimization | dotnet-csharp |
| dotnet-localization | dotnet-ui |
| dotnet-maui-aot | dotnet-ui |
| dotnet-maui-development | dotnet-ui |
| dotnet-maui-testing | dotnet-ui |
| dotnet-mermaid-diagrams | dotnet-tooling |
| dotnet-messaging-patterns | dotnet-api |
| dotnet-middleware-patterns | dotnet-api |
| dotnet-minimal-apis | dotnet-api |
| dotnet-modernize | dotnet-tooling |
| dotnet-msbuild-authoring | dotnet-tooling |
| dotnet-msbuild-tasks | dotnet-tooling |
| dotnet-msix | dotnet-devops |
| dotnet-multi-targeting | dotnet-tooling |
| dotnet-native-aot | dotnet-tooling |
| dotnet-native-interop | dotnet-csharp |
| dotnet-nuget-authoring | dotnet-devops |
| dotnet-observability | dotnet-devops |
| dotnet-openapi | dotnet-api |
| dotnet-performance-patterns | dotnet-tooling |
| dotnet-playwright | dotnet-testing |
| dotnet-profiling | dotnet-tooling |
| dotnet-project-analysis | dotnet-tooling |
| dotnet-project-structure | dotnet-tooling |
| dotnet-realtime-communication | dotnet-api |
| dotnet-release-management | dotnet-devops |
| dotnet-resilience | dotnet-api |
| dotnet-roslyn-analyzers | dotnet-csharp |
| dotnet-scaffold-project | dotnet-tooling |
| dotnet-secrets-management | dotnet-api |
| dotnet-security-owasp | dotnet-api |
| dotnet-semantic-kernel | dotnet-api |
| dotnet-serialization | dotnet-csharp |
| dotnet-service-communication | dotnet-api |
| dotnet-slopwatch | dotnet-testing |
| dotnet-snapshot-testing | dotnet-testing |
| dotnet-solid-principles | dotnet-csharp |
| dotnet-solution-navigation | dotnet-tooling |
| dotnet-spectre-console | dotnet-tooling |
| dotnet-structured-logging | dotnet-devops |
| dotnet-system-commandline | dotnet-tooling |
| dotnet-terminal-gui | dotnet-tooling |
| dotnet-test-quality | dotnet-testing |
| dotnet-testing-strategy | dotnet-testing |
| dotnet-tool-management | dotnet-tooling |
| dotnet-trimming | dotnet-tooling |
| dotnet-ui-chooser | dotnet-ui |
| dotnet-ui-testing-core | dotnet-testing |
| dotnet-uno-mcp | dotnet-ui |
| dotnet-uno-platform | dotnet-ui |
| dotnet-uno-targets | dotnet-ui |
| dotnet-uno-testing | dotnet-ui |
| dotnet-validation-patterns | dotnet-csharp |
| dotnet-version-detection | dotnet-tooling |
| dotnet-version-upgrade | dotnet-tooling |
| dotnet-windbg-debugging | dotnet-debugging |
| dotnet-winforms-basics | dotnet-ui |
| dotnet-winui | dotnet-ui |
| dotnet-wpf-migration | dotnet-ui |
| dotnet-wpf-modern | dotnet-ui |
| dotnet-xml-docs | dotnet-tooling |
| dotnet-xunit | dotnet-testing |

### Count verification per target

```
dotnet-csharp:    22 (coding-standards, async-patterns, dependency-injection, configuration, source-generators, nullable-reference-types, serialization, channels, linq-optimization, domain-modeling, solid-principles, concurrency-patterns, roslyn-analyzers, editorconfig, file-io, native-interop, input-validation, validation-patterns, modern-patterns, api-design, type-design-performance, code-smells)
dotnet-api:       27 (minimal-apis, middleware-patterns, efcore-patterns, efcore-architecture, data-access-strategy, grpc, realtime-communication, resilience, http-client, api-versioning, openapi, api-security, security-owasp, secrets-management, cryptography, background-services, aspire-patterns, semantic-kernel, architecture-patterns, messaging-patterns, service-communication, api-surface-validation, library-api-compat, io-pipelines, agent-gotchas, file-based-apps, api-docs)
dotnet-ui:        18 (blazor-patterns, blazor-components, blazor-auth, blazor-testing, maui-development, maui-aot, maui-testing, uno-platform, uno-targets, uno-mcp, uno-testing, wpf-modern, wpf-migration, winui, winforms-basics, accessibility, localization, ui-chooser)
dotnet-testing:   12 (testing-strategy, xunit, integration-testing, snapshot-testing, playwright, benchmarkdotnet, ci-benchmarking, test-quality, add-testing, slopwatch, aot-wasm, ui-testing-core)
dotnet-devops:    18 (gha-build-test, gha-deploy, gha-publish, gha-patterns, ado-build-test, ado-publish, ado-patterns, ado-unique, containers, container-deployment, nuget-authoring, msix, github-releases, release-management, observability, structured-logging, add-ci, github-docs)
dotnet-tooling:   32 (project-structure, scaffold-project, csproj-reading, msbuild-authoring, msbuild-tasks, build-analysis, build-optimization, artifacts-output, multi-targeting, performance-patterns, profiling, native-aot, aot-architecture, trimming, gc-memory, cli-architecture, system-commandline, spectre-console, terminal-gui, cli-distribution, cli-packaging, cli-release-pipeline, documentation-strategy, xml-docs, tool-management, version-detection, version-upgrade, solution-navigation, project-analysis, modernize, add-analyzers, mermaid-diagrams)
dotnet-debugging: 1  (windbg-debugging)
dotnet-advisor:   1  (advisor)
TOTAL:           131 (22 + 27 + 18 + 12 + 18 + 32 + 1 + 1)
```

All 131 source skills have exactly one assignment. No duplicates, no gaps.
