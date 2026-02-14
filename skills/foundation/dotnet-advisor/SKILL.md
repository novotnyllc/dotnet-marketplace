---
name: dotnet-advisor
description: "WHEN user creates APIs, adds tests, fixes async, scaffolds projects, or works with .NET, C#, ASP.NET Core, Blazor, MAUI, Uno Platform, EF Core, NuGet, or MSBuild. Routes to specialist skills. WHEN NOT non-.NET languages (Python, JavaScript, Go, Rust, Java)."
---

# dotnet-advisor

Router and index skill for **dotnet-artisan**. Always loaded. Routes .NET development queries to the appropriate specialist skills based on context.

## First Step: Detect Project Version

Before any .NET guidance, determine the project's target framework:

> Load [skill:dotnet-version-detection] to read TFMs from `.csproj`, `Directory.Build.props`, and `global.json`. Adapt all guidance to the detected .NET version (net8.0, net9.0, net10.0, net11.0).

---

## Skill Catalog

<!-- Budget: PROJECTED_SKILLS_COUNT=100, MAX_DESC_CHARS=120 -->
<!-- Projected max: 100 x 120 = 12,000 chars (at 12,000 WARN threshold) -->

### 1. Foundation & Plugin Infrastructure `implemented`
- [skill:dotnet-advisor] -- this skill (router/index)
- [skill:dotnet-version-detection] -- TFM/SDK detection, preview features
- [skill:dotnet-project-analysis] -- solution structure, project refs, CPM
- [skill:plugin-self-publish] -- plugin versioning, changelog, CI/CD

### 2. Core C# & Language Patterns `planned`
- [skill:dotnet-csharp-modern-patterns] -- C# 14/15 features, records, pattern matching
- [skill:dotnet-csharp-coding-standards] -- naming, conventions, file organization
- [skill:dotnet-csharp-async-patterns] -- async/await best practices, common mistakes
- [skill:dotnet-csharp-nullable-reference-types] -- NRT patterns, annotations, migration
- [skill:dotnet-csharp-dependency-injection] -- MS DI, keyed services, decoration
- [skill:dotnet-csharp-configuration] -- options pattern, feature flags, secrets
- [skill:dotnet-csharp-source-generators] -- IIncrementalGenerator, emit patterns

### 3. Project Structure & Scaffolding `planned`
- [skill:dotnet-project-structure] -- .slnx, Directory.Build.props, CPM, analyzers
- [skill:dotnet-scaffolding-base] -- project scaffolding with best practices
- [skill:dotnet-add-analyzers] -- Roslyn analyzers, nullable, trimming, AOT compat
- [skill:dotnet-add-ci] -- add CI/CD to existing project
- [skill:dotnet-add-testing] -- add test infrastructure
- [skill:dotnet-modernize] -- analyze code for modernization opportunities

### 4. Architecture Patterns `planned`
- [skill:dotnet-architecture-patterns] -- minimal API org, vertical slices, error handling
- [skill:dotnet-background-services] -- BackgroundService, Channels, producer/consumer
- [skill:dotnet-resilience] -- Polly v8 + MS.Extensions.Resilience (NOT Http.Polly)
- [skill:dotnet-http-client] -- IHttpClientFactory, typed/named clients, resilience
- [skill:dotnet-observability] -- OpenTelemetry, structured logging, health checks
- [skill:dotnet-efcore-patterns] -- DbContext lifecycle, migrations, interceptors
- [skill:dotnet-efcore-architecture] -- read/write models, avoiding N+1
- [skill:dotnet-data-access-strategy] -- EF Core vs Dapper vs ADO.NET decision
- [skill:dotnet-containers] -- multi-stage Dockerfiles, rootless, health checks
- [skill:dotnet-container-deployment] -- Kubernetes, Docker Compose, registries

### 5. Serialization & Communication `planned`
- [skill:dotnet-serialization] -- AOT source-gen: STJ, Protobuf, MessagePack
- [skill:dotnet-grpc] -- service definition, streaming, auth, health checks
- [skill:dotnet-realtime-communication] -- SignalR, JSON-RPC, SSE, gRPC streaming
- [skill:dotnet-service-communication] -- routes to gRPC, real-time, or REST

### 6. API Development `planned`
- [skill:dotnet-minimal-apis] -- route groups, filters, validation, OpenAPI 3.1
- [skill:dotnet-api-versioning] -- URL versioning, Asp.Versioning.Http/Mvc
- [skill:dotnet-openapi] -- OpenAPI: MS.AspNetCore.OpenApi (built-in .NET 9+), Swashbuckle migration, NSwag, transformers
- [skill:dotnet-api-security] -- Identity, OAuth/OIDC, JWT, passkeys (WebAuthn), CORS, CSP, rate limiting
- [skill:dotnet-input-validation] -- .NET 10 AddValidation, FluentValidation, Data Annotations, endpoint filters, ProblemDetails

### 7. Security `planned`
- [skill:dotnet-security-owasp] -- OWASP top 10 for .NET
- [skill:dotnet-secrets-management] -- user secrets, secure config patterns
- [skill:dotnet-cryptography] -- modern crypto incl. post-quantum (.NET 10)

### 8. Testing `planned`
- [skill:dotnet-testing-strategy] -- unit vs integration vs E2E, organization
- [skill:dotnet-xunit] -- xUnit v3, theories, fixtures, parallelism
- [skill:dotnet-integration-testing] -- WebApplicationFactory, Testcontainers
- [skill:dotnet-ui-testing-core] -- core UI testing patterns
- [skill:dotnet-blazor-testing] -- bUnit for Blazor components
- [skill:dotnet-maui-testing] -- Appium, XHarness for MAUI
- [skill:dotnet-uno-testing] -- Playwright for Uno WASM
- [skill:dotnet-playwright] -- browser automation, E2E testing
- [skill:dotnet-snapshot-testing] -- Verify for snapshot testing
- [skill:dotnet-test-quality] -- coverage, CRAP analysis, mutation testing

### 9. Performance & Benchmarking `implemented`
- [skill:dotnet-benchmarkdotnet] -- BenchmarkDotNet setup, configs, CI
- [skill:dotnet-performance-patterns] -- Span, pooling, zero-alloc, sealed
- [skill:dotnet-profiling] -- dotnet-counters, trace, dump, memory
- [skill:dotnet-ci-benchmarking] -- continuous benchmarking, regression detection

### 10. Native AOT & Trimming `planned`
- [skill:dotnet-native-aot] -- trimming, RD.xml, reflection-free, size opt
- [skill:dotnet-aot-architecture] -- architect for AOT from start
- [skill:dotnet-trimming] -- trim-safe annotations, linker config, testing
- [skill:dotnet-aot-wasm] -- WASM AOT for Blazor and Uno

### 11. CLI Tool Development
- [skill:dotnet-system-commandline] -- System.CommandLine, middleware, hosting
- [skill:dotnet-cli-architecture] -- layered CLI design, testability
- [skill:dotnet-cli-distribution] -- Native AOT + cross-platform distribution strategy
- [skill:dotnet-cli-packaging] -- Homebrew, apt/deb, winget, Scoop, Chocolatey, dotnet tool
- [skill:dotnet-cli-release-pipeline] -- unified multi-platform CI/CD release workflow

### 12. UI Frameworks `planned`
- [skill:dotnet-blazor-patterns] -- Server, WASM, Hybrid, auto/streaming
- [skill:dotnet-blazor-components] -- component architecture, JS interop
- [skill:dotnet-blazor-auth] -- auth across hosting models
- [skill:dotnet-uno-platform] -- Extensions, MVUX, Toolkit, themes
- [skill:dotnet-uno-targets] -- Web/WASM, Mobile, Desktop, Embedded
- [skill:dotnet-uno-mcp] -- Uno MCP server for live docs
- [skill:dotnet-maui-development] -- MAUI patterns, current state
- [skill:dotnet-maui-aot] -- MAUI Native AOT on iOS/Mac Catalyst
- [skill:dotnet-winui] -- WinUI 3 / Windows App SDK, XAML, MSIX, UWP migration
- [skill:dotnet-wpf-modern] -- WPF on .NET 8+, Host builder, MVVM Toolkit, Fluent theme
- [skill:dotnet-wpf-migration] -- WPF/WinForms to .NET 8+, WPF to WinUI or Uno, UWP migration
- [skill:dotnet-winforms-basics] -- WinForms on .NET 8+, high-DPI, dark mode, DI
- [skill:dotnet-ui-chooser] -- decision tree for UI framework selection

### 13. Multi-Targeting & Polyfills `planned`
- [skill:dotnet-multi-targeting] -- PolySharp, Polyfill, conditional compilation
- [skill:dotnet-version-upgrade] -- .NET 8 -> 10 -> 11 upgrade guidance

### 14. Localization & Internationalization `planned`
- [skill:dotnet-localization] -- i18n: .resx, IStringLocalizer, RTL, pluralization

### 15. Packaging & Publishing `planned`
- [skill:dotnet-nuget-modern] -- CPM, source generators, SourceLink, CI publish
- [skill:dotnet-msix] -- MSIX creation, signing, distribution, auto-update
- [skill:dotnet-github-releases] -- GitHub Releases with release notes

### 16. Release Management `planned`
- [skill:dotnet-release-management] -- NBGV, changelogs, SemVer strategy

### 17. CI/CD `implemented`
- [skill:dotnet-gha-patterns] -- reusable workflows, composite actions, matrix
- [skill:dotnet-gha-build-test] -- .NET build + test workflows
- [skill:dotnet-gha-publish] -- NuGet/container publishing workflows
- [skill:dotnet-gha-deploy] -- deployment patterns (Pages, registries)
- [skill:dotnet-ado-patterns] -- ADO YAML pipelines, Environments, Gates
- [skill:dotnet-ado-build-test] -- ADO build + test pipelines
- [skill:dotnet-ado-publish] -- ADO publishing pipelines
- [skill:dotnet-ado-unique] -- ADO-specific: classic pipelines, service connections

### 18. Documentation `planned`
- [skill:dotnet-documentation-strategy] -- Starlight, Docusaurus, DocFX
- [skill:dotnet-mermaid-diagrams] -- architecture/sequence/class diagrams
- [skill:dotnet-github-docs] -- README, CONTRIBUTING, issue templates
- [skill:dotnet-xml-docs] -- XML documentation comments
- [skill:dotnet-api-docs] -- API doc generation, OpenAPI specs

### 19. Agent Meta-Skills `planned`
- [skill:dotnet-agent-gotchas] -- common agent mistakes with .NET
- [skill:dotnet-build-analysis] -- understand build output, MSBuild errors
- [skill:dotnet-csproj-reading] -- read/modify .csproj, MSBuild properties
- [skill:dotnet-solution-navigation] -- navigate solutions, find entry points

---

## Routing Logic

Use this decision tree to load the right skills for the current task.

### Starting a New Project
1. [skill:dotnet-version-detection] -- detect or choose target framework
2. [skill:dotnet-project-analysis] -- understand existing solution (if any)
3. [skill:dotnet-project-structure], [skill:dotnet-scaffolding-base] -- scaffold project
4. [skill:dotnet-architecture-patterns] -- design decisions

### Writing or Modifying C# Code
- Modern C# patterns -> [skill:dotnet-csharp-modern-patterns]
- Coding standards -> [skill:dotnet-csharp-coding-standards]
- NRT -> [skill:dotnet-csharp-nullable-reference-types]
- DI -> [skill:dotnet-csharp-dependency-injection]
- Configuration -> [skill:dotnet-csharp-configuration]
- Async/await, concurrency -> [skill:dotnet-csharp-async-patterns]
- Source generators -> [skill:dotnet-csharp-source-generators]

### Building APIs
- Minimal APIs (default for new) -> [skill:dotnet-minimal-apis]
- API versioning -> [skill:dotnet-api-versioning]
- OpenAPI/Swagger, Swashbuckle migration -> [skill:dotnet-openapi]
- Auth, CORS, rate limiting, CSP -> [skill:dotnet-api-security]
- Input validation, FluentValidation, Data Annotations -> [skill:dotnet-input-validation]
- Resilience/HTTP clients -> [skill:dotnet-resilience], [skill:dotnet-http-client]

### Working with Data
- EF Core usage -> [skill:dotnet-efcore-patterns], [skill:dotnet-efcore-architecture]
- Choosing data access approach -> [skill:dotnet-data-access-strategy]
- Serialization (JSON, Protobuf) -> [skill:dotnet-serialization]

### Building UI
- Choosing a framework -> [skill:dotnet-ui-chooser]
- Blazor -> [skill:dotnet-blazor-patterns], [skill:dotnet-blazor-components], [skill:dotnet-blazor-auth]
- Uno Platform -> [skill:dotnet-uno-platform], [skill:dotnet-uno-targets], [skill:dotnet-uno-mcp]
- MAUI -> [skill:dotnet-maui-development], [skill:dotnet-maui-aot]
- WPF -> [skill:dotnet-wpf-modern] (migration: [skill:dotnet-wpf-migration])
- WinUI -> [skill:dotnet-winui]
- WinForms -> [skill:dotnet-winforms-basics]

### Testing
- Strategy/what to test -> [skill:dotnet-testing-strategy]
- xUnit v3 -> [skill:dotnet-xunit]
- Integration tests -> [skill:dotnet-integration-testing]
- UI testing -> [skill:dotnet-ui-testing-core] + framework-specific skill
- Snapshot testing -> [skill:dotnet-snapshot-testing]
- Coverage/quality -> [skill:dotnet-test-quality]

### Performance Work
- Benchmarking -> [skill:dotnet-benchmarkdotnet]
- Optimization patterns -> [skill:dotnet-performance-patterns]
- Profiling -> [skill:dotnet-profiling]
- CI benchmarks -> [skill:dotnet-ci-benchmarking]

### Native AOT / Trimming
- AOT compilation -> [skill:dotnet-native-aot]
- Architecting for AOT -> [skill:dotnet-aot-architecture]
- Trimming -> [skill:dotnet-trimming]
- WASM AOT -> [skill:dotnet-aot-wasm]

### CLI Tools
- System.CommandLine -> [skill:dotnet-system-commandline]
- CLI design -> [skill:dotnet-cli-architecture]
- Distribution -> [skill:dotnet-cli-distribution], [skill:dotnet-cli-packaging], [skill:dotnet-cli-release-pipeline]

### Containers & Deployment
- Dockerfiles -> [skill:dotnet-containers]
- Kubernetes/Compose -> [skill:dotnet-container-deployment]

### Security
- OWASP compliance -> [skill:dotnet-security-owasp]
- Secrets management -> [skill:dotnet-secrets-management]
- Cryptography -> [skill:dotnet-cryptography]

### Communication Patterns
- gRPC -> [skill:dotnet-grpc]
- Real-time (SignalR, SSE) -> [skill:dotnet-realtime-communication]
- Choosing protocol -> [skill:dotnet-service-communication]

### CI/CD Setup
- GitHub Actions -> [skill:dotnet-gha-patterns], [skill:dotnet-gha-build-test], [skill:dotnet-gha-publish], [skill:dotnet-gha-deploy]
- Azure DevOps -> [skill:dotnet-ado-patterns], [skill:dotnet-ado-build-test], [skill:dotnet-ado-publish], [skill:dotnet-ado-unique]

### Packaging & Releases
- NuGet publishing -> [skill:dotnet-nuget-modern]
- MSIX -> [skill:dotnet-msix]
- GitHub Releases -> [skill:dotnet-github-releases]
- Versioning -> [skill:dotnet-release-management]

### Multi-Targeting
- Multi-TFM builds -> [skill:dotnet-multi-targeting]
- Version upgrades -> [skill:dotnet-version-upgrade]

### Localization
- i18n/l10n -> [skill:dotnet-localization]

### Documentation
- Doc strategy -> [skill:dotnet-documentation-strategy]
- Diagrams -> [skill:dotnet-mermaid-diagrams]
- GitHub docs -> [skill:dotnet-github-docs]
- XML docs -> [skill:dotnet-xml-docs]
- API docs -> [skill:dotnet-api-docs]

### Agent Assistance
- Agent making .NET mistakes -> [skill:dotnet-agent-gotchas]
- Build errors -> [skill:dotnet-build-analysis]
- Reading .csproj -> [skill:dotnet-csproj-reading]
- Navigating solutions -> [skill:dotnet-solution-navigation]

### Background Work
- Background services, queues -> [skill:dotnet-background-services]
- Observability/logging -> [skill:dotnet-observability]
