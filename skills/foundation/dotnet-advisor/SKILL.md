---
name: dotnet-advisor
description: "WHEN user works with .NET, C#, ASP.NET Core, Blazor, MAUI, Uno Platform, EF Core, NuGet, or MSBuild projects. Routes to specialist skills. WHEN NOT non-.NET languages (Python, JavaScript, Go, Rust, Java)."
---

# dotnet-advisor

Router and index skill for **dotnet-artisan**. Always loaded. Routes .NET development queries to the appropriate specialist skills based on context.

## First Step: Detect Project Version

Before any .NET guidance, determine the project's target framework:

> Load [skill:dotnet-version-detection] to read TFMs from `.csproj`, `Directory.Build.props`, and `global.json`. Adapt all guidance to the detected .NET version (net8.0, net9.0, net10.0, net11.0).

---

## Skill Catalog

<!-- Budget: PROJECTED_SKILLS_COUNT=95, MAX_DESC_CHARS=120 -->
<!-- Projected max: 95 x 120 = 11,400 chars (under 12,000 WARN threshold) -->

### 1. Foundation & Plugin Infrastructure `implemented`
- [skill:dotnet-advisor] -- this skill (router/index)
- [skill:dotnet-version-detection] -- TFM/SDK detection, preview features
- [skill:dotnet-project-analysis] -- solution structure, project refs, CPM
- [skill:plugin-self-publish] -- plugin versioning, changelog, CI/CD

### 2. Core C# & Language Patterns `planned`
- dotnet-csharp-modern-patterns -- C# 14/15 features, records, pattern matching
- dotnet-csharp-coding-standards -- naming, conventions, file organization
- dotnet-csharp-async-patterns -- async/await best practices, common mistakes
- dotnet-csharp-nullable-reference-types -- NRT patterns, annotations, migration
- dotnet-csharp-dependency-injection -- MS DI, keyed services, decoration
- dotnet-csharp-configuration -- options pattern, feature flags, secrets
- dotnet-csharp-source-generators -- IIncrementalGenerator, emit patterns

### 3. Project Structure & Scaffolding `planned`
- dotnet-project-structure -- .slnx, Directory.Build.props, CPM, analyzers
- dotnet-scaffolding-base -- project scaffolding with best practices
- dotnet-add-analyzers -- Roslyn analyzers, nullable, trimming, AOT compat
- dotnet-add-ci -- add CI/CD to existing project
- dotnet-add-testing -- add test infrastructure
- dotnet-modernize -- analyze code for modernization opportunities

### 4. Architecture Patterns `planned`
- dotnet-architecture-patterns -- minimal API org, vertical slices, error handling
- dotnet-background-services -- BackgroundService, Channels, producer/consumer
- dotnet-resilience -- Polly v8 + MS.Extensions.Resilience (NOT Http.Polly)
- dotnet-http-client -- IHttpClientFactory, typed/named clients, resilience
- dotnet-observability -- OpenTelemetry, structured logging, health checks
- dotnet-efcore-patterns -- DbContext lifecycle, migrations, interceptors
- dotnet-efcore-architecture -- read/write models, avoiding N+1
- dotnet-data-access-strategy -- EF Core vs Dapper vs ADO.NET decision
- dotnet-containers -- multi-stage Dockerfiles, rootless, health checks
- dotnet-container-deployment -- Kubernetes, Docker Compose, registries

### 5. Serialization & Communication `planned`
- dotnet-serialization -- AOT source-gen: STJ, Protobuf, MessagePack
- dotnet-grpc -- service definition, streaming, auth, health checks
- dotnet-realtime-communication -- SignalR, JSON-RPC, SSE, gRPC streaming
- dotnet-service-communication -- routes to gRPC, real-time, or REST

### 6. API Development `planned`
- dotnet-minimal-apis -- route groups, filters, validation, OpenAPI 3.1
- dotnet-api-versioning -- URL versioning, MS.AspNetCore.Mvc.Versioning
- dotnet-openapi -- OpenAPI: MS.AspNetCore.OpenApi (built-in .NET 10+)
- dotnet-api-security -- Identity, OAuth/OIDC, JWT, passkeys, CORS

### 7. Security `planned`
- dotnet-security-owasp -- OWASP top 10 for .NET
- dotnet-secrets-management -- user secrets, secure config patterns
- dotnet-cryptography -- modern crypto incl. post-quantum (.NET 10)

### 8. Testing `planned`
- dotnet-testing-strategy -- unit vs integration vs E2E, organization
- dotnet-xunit -- xUnit v3, theories, fixtures, parallelism
- dotnet-integration-testing -- WebApplicationFactory, Testcontainers
- dotnet-ui-testing-core -- core UI testing patterns
- dotnet-blazor-testing -- bUnit for Blazor components
- dotnet-maui-testing -- Appium, XHarness for MAUI
- dotnet-uno-testing -- Playwright for Uno WASM
- dotnet-playwright -- browser automation, E2E testing
- dotnet-snapshot-testing -- Verify for snapshot testing
- dotnet-test-quality -- coverage, CRAP analysis, mutation testing

### 9. Performance & Benchmarking `planned`
- dotnet-benchmarkdotnet -- BenchmarkDotNet setup, configs, CI
- dotnet-performance-patterns -- Span, pooling, zero-alloc, sealed
- dotnet-profiling -- dotnet-counters, trace, dump, memory
- dotnet-ci-benchmarking -- continuous benchmarking, regression detection

### 10. Native AOT & Trimming `planned`
- dotnet-native-aot -- trimming, RD.xml, reflection-free, size opt
- dotnet-aot-architecture -- architect for AOT from start
- dotnet-trimming -- trim-safe annotations, linker config, testing
- dotnet-aot-wasm -- WASM AOT for Blazor and Uno

### 11. CLI Tool Development `planned`
- dotnet-system-commandline -- System.CommandLine, middleware, hosting
- dotnet-cli-architecture -- layered CLI design, testability
- dotnet-cli-aot-distribution -- Native AOT + cross-platform distribution
- dotnet-cli-homebrew -- Homebrew formula authoring
- dotnet-cli-apt -- apt/dpkg packaging for Linux
- dotnet-cli-winget -- winget manifest for Windows
- dotnet-cli-unified-pipeline -- unified multi-platform CI/CD

### 12. UI Frameworks `planned`
- dotnet-blazor-patterns -- Server, WASM, Hybrid, auto/streaming
- dotnet-blazor-components -- component architecture, JS interop
- dotnet-blazor-auth -- auth across hosting models
- dotnet-uno-platform -- Extensions, MVUX, Toolkit, themes
- dotnet-uno-targets -- Web/WASM, Mobile, Desktop, Embedded
- dotnet-uno-mcp -- Uno MCP server for live docs
- dotnet-maui-development -- MAUI patterns, current state
- dotnet-maui-aot -- MAUI Native AOT on iOS/Mac Catalyst
- dotnet-winui -- WinUI 3 development patterns
- dotnet-wpf-modern -- WPF on .NET Core, MVVM Toolkit
- dotnet-wpf-migration -- migration to WinUI or Uno
- dotnet-winforms-basics -- WinForms on .NET Core
- dotnet-ui-chooser -- decision tree for UI framework selection

### 13. Multi-Targeting & Polyfills `planned`
- dotnet-multi-targeting -- PolySharp, Polyfill, conditional compilation
- dotnet-version-upgrade -- .NET 8 -> 10 -> 11 upgrade guidance

### 14. Localization & Internationalization `planned`
- dotnet-localization -- i18n: .resx, IStringLocalizer, RTL, pluralization

### 15. Packaging & Publishing `planned`
- dotnet-nuget-modern -- CPM, source generators, SourceLink, CI publish
- dotnet-msix -- MSIX creation, signing, distribution, auto-update
- dotnet-github-releases -- GitHub Releases with release notes

### 16. Release Management `planned`
- dotnet-release-management -- NBGV, changelogs, SemVer strategy

### 17. CI/CD `planned`
- dotnet-gha-patterns -- reusable workflows, composite actions, matrix
- dotnet-gha-build-test -- .NET build + test workflows
- dotnet-gha-publish -- NuGet/container publishing workflows
- dotnet-gha-deploy -- deployment patterns (Pages, registries)
- dotnet-ado-patterns -- ADO YAML pipelines, Environments, Gates
- dotnet-ado-build-test -- ADO build + test pipelines
- dotnet-ado-publish -- ADO publishing pipelines
- dotnet-ado-unique -- ADO-specific: classic pipelines, service connections

### 18. Documentation `planned`
- dotnet-documentation-strategy -- Starlight, Docusaurus, DocFX
- dotnet-mermaid-diagrams -- architecture/sequence/class diagrams
- dotnet-github-docs -- README, CONTRIBUTING, issue templates
- dotnet-xml-docs -- XML documentation comments
- dotnet-api-docs -- API doc generation, OpenAPI specs

### 19. Agent Meta-Skills `planned`
- dotnet-agent-gotchas -- common agent mistakes with .NET
- dotnet-build-analysis -- understand build output, MSBuild errors
- dotnet-csproj-reading -- read/modify .csproj, MSBuild properties
- dotnet-solution-navigation -- navigate solutions, find entry points

---

## Routing Logic

Use this decision tree to load the right skills for the current task.

### Starting a New Project
1. [skill:dotnet-version-detection] -- detect or choose target framework
2. [skill:dotnet-project-analysis] -- understand existing solution (if any)
3. Load project-structure skills for scaffolding
4. Load architecture skills for design decisions

### Writing or Modifying C# Code
- Modern C# patterns, coding standards, NRT, DI, configuration -> Core C# skills
- Async/await, concurrency -> csharp-async-patterns
- Source generators -> csharp-source-generators

### Building APIs
- Minimal APIs (default for new) -> dotnet-minimal-apis
- API versioning -> dotnet-api-versioning
- OpenAPI/Swagger -> dotnet-openapi
- Auth -> dotnet-api-security
- Resilience/HTTP clients -> dotnet-resilience, dotnet-http-client

### Working with Data
- EF Core usage -> dotnet-efcore-patterns, dotnet-efcore-architecture
- Choosing data access approach -> dotnet-data-access-strategy
- Serialization (JSON, Protobuf) -> dotnet-serialization

### Building UI
- Choosing a framework -> dotnet-ui-chooser
- Blazor -> dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth
- Uno Platform -> dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp
- MAUI -> dotnet-maui-development, dotnet-maui-aot
- WPF -> dotnet-wpf-modern (migration: dotnet-wpf-migration)
- WinUI -> dotnet-winui
- WinForms -> dotnet-winforms-basics

### Testing
- Strategy/what to test -> dotnet-testing-strategy
- xUnit v3 -> dotnet-xunit
- Integration tests -> dotnet-integration-testing
- UI testing -> dotnet-ui-testing-core + framework-specific skill
- Snapshot testing -> dotnet-snapshot-testing
- Coverage/quality -> dotnet-test-quality

### Performance Work
- Benchmarking -> dotnet-benchmarkdotnet
- Optimization patterns -> dotnet-performance-patterns
- Profiling -> dotnet-profiling
- CI benchmarks -> dotnet-ci-benchmarking

### Native AOT / Trimming
- AOT compilation -> dotnet-native-aot
- Architecting for AOT -> dotnet-aot-architecture
- Trimming -> dotnet-trimming
- WASM AOT -> dotnet-aot-wasm

### CLI Tools
- System.CommandLine -> dotnet-system-commandline
- CLI design -> dotnet-cli-architecture
- Distribution -> dotnet-cli-aot-distribution + platform-specific skills

### Containers & Deployment
- Dockerfiles -> dotnet-containers
- Kubernetes/Compose -> dotnet-container-deployment

### Security
- OWASP compliance -> dotnet-security-owasp
- Secrets management -> dotnet-secrets-management
- Cryptography -> dotnet-cryptography

### Communication Patterns
- gRPC -> dotnet-grpc
- Real-time (SignalR, SSE) -> dotnet-realtime-communication
- Choosing protocol -> dotnet-service-communication

### CI/CD Setup
- GitHub Actions -> dotnet-gha-patterns + specific workflow skills
- Azure DevOps -> dotnet-ado-patterns + specific pipeline skills

### Packaging & Releases
- NuGet publishing -> dotnet-nuget-modern
- MSIX -> dotnet-msix
- GitHub Releases -> dotnet-github-releases
- Versioning -> dotnet-release-management

### Multi-Targeting
- Multi-TFM builds -> dotnet-multi-targeting
- Version upgrades -> dotnet-version-upgrade

### Localization
- i18n/l10n -> dotnet-localization

### Documentation
- Doc strategy -> dotnet-documentation-strategy
- Diagrams -> dotnet-mermaid-diagrams
- GitHub docs -> dotnet-github-docs
- XML docs -> dotnet-xml-docs
- API docs -> dotnet-api-docs

### Agent Assistance
- Agent making .NET mistakes -> dotnet-agent-gotchas
- Build errors -> dotnet-build-analysis
- Reading .csproj -> dotnet-csproj-reading
- Navigating solutions -> dotnet-solution-navigation

### Background Work
- Background services, queues -> dotnet-background-services
- Observability/logging -> dotnet-observability
