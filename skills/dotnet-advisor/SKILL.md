---
name: dotnet-advisor
description: Routes .NET/C# work to domain skills. Loads coding-standards for code paths.
user-invocable: true
license: MIT
---

# dotnet-advisor

Router and index skill for **dotnet-artisan**. Always loaded. Routes .NET development queries to the appropriate consolidated skill based on context.

## Scope

- Routing .NET/C# requests to the correct domain skill or specialist agent
- Loading [skill:dotnet-csharp] (read `references/coding-standards.md`) as baseline for all code paths
- Maintaining the skill catalog and routing precedence
- Delegating complex analysis to specialist agents
- Decision-tree navigation for ambiguous requests spanning multiple domains

## Out of scope

- Domain-specific implementation guidance -- see [skill:dotnet-csharp], [skill:dotnet-api], [skill:dotnet-ui], [skill:dotnet-testing], [skill:dotnet-devops], [skill:dotnet-tooling], [skill:dotnet-debugging]
- Deep content lives in each skill's `references/` companion files -- the advisor routes, skills implement

## Immediate Routing Actions (Do First)

For every .NET/C# request, execute this sequence before detailed planning:
1. Invoke [skill:dotnet-csharp] (read `references/coding-standards.md`).
2. Invoke the primary domain skill for the request (API, testing, UI, devops, tooling, debugging).
3. Continue with any additional routed skills.

For generic "build me an app" requests, do not skip step 1 even when project scaffolding is the next action.

## Default Quality Rule

For any task that may produce, change, or review C#/.NET code:
1. Load [skill:dotnet-csharp] (read `references/coding-standards.md`) as a baseline dependency.
2. Then load domain-specific skills (API, testing, UI, etc.).
3. Apply standards from coding-standards throughout planning and implementation, not only in final cleanup.

## First Step: Detect Project Version

Before any .NET guidance, determine the project's target framework:

> Load [skill:dotnet-tooling] (read `references/version-detection.md`) to read TFMs from `.csproj`, `Directory.Build.props`, and `global.json`. Adapt all guidance to the detected .NET version (net8.0, net9.0, net10.0, net11.0).

---

## Skill Catalog (8 Skills)

### 1. dotnet-csharp -- C# Language & Runtime Patterns
[skill:dotnet-csharp] -- C# language patterns, coding standards, async/await, DI, config, source generators, nullable types, serialization, channels, LINQ, domain modeling, SOLID, concurrency, analyzers, editorconfig, file I/O, native interop, validation, modern syntax, API design.

Key companion files: `references/coding-standards.md`, `references/async-patterns.md`, `references/dependency-injection.md`, `references/modern-patterns.md`, `references/concurrency-patterns.md`, `references/domain-modeling.md`, `references/solid-principles.md`

### 2. dotnet-api -- ASP.NET Core, Data Access & Backend Services
[skill:dotnet-api] -- Minimal APIs, middleware, EF Core, gRPC, SignalR/SSE, resilience (Polly), HTTP client, API versioning, OpenAPI, security (OWASP, secrets, crypto), background services, Aspire, Semantic Kernel, architecture patterns, messaging, service communication.

Key companion files: `references/minimal-apis.md`, `references/efcore-patterns.md`, `references/architecture-patterns.md`, `references/api-security.md`, `references/resilience.md`, `references/aspire-patterns.md`, `references/security-owasp.md`

### 3. dotnet-ui -- UI Frameworks (Blazor, MAUI, Uno, WPF, WinUI, WinForms)
[skill:dotnet-ui] -- Blazor (patterns, components, auth, testing), MAUI (development, AOT, testing), Uno Platform (core, targets, MCP, testing), WPF (modern, migration), WinUI 3, WinForms, accessibility, localization, UI framework selection.

Key companion files: `references/blazor-patterns.md`, `references/blazor-components.md`, `references/maui-development.md`, `references/uno-platform.md`, `references/ui-chooser.md`, `references/wpf-modern.md`

### 4. dotnet-testing -- Test Strategy, Frameworks & Quality
[skill:dotnet-testing] -- Test strategy, xUnit v3, integration/E2E, snapshots (Verify), Playwright, benchmarks (BenchmarkDotNet), quality gates, CI benchmarking.

Key companion files: `references/testing-strategy.md`, `references/xunit.md`, `references/integration-testing.md`, `references/playwright.md`, `references/benchmarkdotnet.md`

### 5. dotnet-devops -- CI/CD, Packaging & Operations
[skill:dotnet-devops] -- GitHub Actions, Azure DevOps, containers (Dockerfiles, deployment), NuGet, MSIX, GitHub Releases, release management (NBGV, SemVer), observability (OpenTelemetry), structured logging.

Key companion files: `references/gha-patterns.md`, `references/ado-patterns.md`, `references/containers.md`, `references/nuget-authoring.md`, `references/observability.md`, `references/release-management.md`

### 6. dotnet-tooling -- Project Setup, Build & Developer Tools
[skill:dotnet-tooling] -- Solution structure, MSBuild, build optimization, performance patterns, profiling, Native AOT, trimming, GC/memory, CLI apps (System.CommandLine, Spectre.Console, Terminal.Gui), docs generation, tool management, version detection/upgrade, solution navigation.

Key companion files: `references/version-detection.md`, `references/project-structure.md`, `references/native-aot.md`, `references/profiling.md`, `references/performance-patterns.md`, `references/system-commandline.md`, `references/scaffold-project.md`

### 7. dotnet-debugging -- WinDbg & Crash Dump Analysis
[skill:dotnet-debugging] -- WinDbg MCP, live process attach, dump triage, crash/hang/CPU/memory analysis, symbol config, SOS extension, diagnostic reports.

Key companion files: `references/dump-workflow.md`, `references/task-crash.md`, `references/task-hang.md`, `references/task-memory.md`, `references/mcp-setup.md`

### 8. dotnet-advisor -- This Skill (Router/Index)
Routes all .NET queries to the appropriate domain skill above.

---

## Routing Logic

Use this decision tree to load the right skills for the current task.

### Starting a New Project
1. [skill:dotnet-tooling] (read `references/version-detection.md`) -- detect or choose target framework
2. [skill:dotnet-tooling] (read `references/project-analysis.md`) -- understand existing solution (if any)
3. [skill:dotnet-tooling] (read `references/project-structure.md`, `references/scaffold-project.md`) -- scaffold project
4. [skill:dotnet-api] (read `references/architecture-patterns.md`) -- design decisions
- File-based app (no .csproj, .NET 10+) -> [skill:dotnet-api] (read `references/file-based-apps.md`)
- Build output layout -> [skill:dotnet-tooling] (read `references/artifacts-output.md`)

### Writing or Modifying C# Code
- Always load first -> [skill:dotnet-csharp] (read `references/coding-standards.md`)
- Modern C# patterns -> [skill:dotnet-csharp] (read `references/modern-patterns.md`)
- NRT -> [skill:dotnet-csharp] (read `references/nullable-reference-types.md`)
- DI -> [skill:dotnet-csharp] (read `references/dependency-injection.md`)
- Configuration -> [skill:dotnet-csharp] (read `references/configuration.md`)
- Async/await, concurrency -> [skill:dotnet-csharp] (read `references/async-patterns.md`, `references/concurrency-patterns.md`)
- Source generators -> [skill:dotnet-csharp] (read `references/source-generators.md`)
- Code review, code quality -> [skill:dotnet-csharp] (read `references/code-smells.md`)
- Custom analyzers/code fixes -> [skill:dotnet-csharp] (read `references/roslyn-analyzers.md`)
- File I/O -> [skill:dotnet-csharp] (read `references/file-io.md`)
- LINQ optimization -> [skill:dotnet-csharp] (read `references/linq-optimization.md`)
- P/Invoke, native interop -> [skill:dotnet-csharp] (read `references/native-interop.md`)
- Domain modeling, DDD -> [skill:dotnet-csharp] (read `references/domain-modeling.md`)
- SOLID principles -> [skill:dotnet-csharp] (read `references/solid-principles.md`)
- Serialization -> [skill:dotnet-csharp] (read `references/serialization.md`)
- Channels -> [skill:dotnet-csharp] (read `references/channels.md`)
- Input validation -> [skill:dotnet-csharp] (read `references/input-validation.md`)

### Building APIs
- Minimal APIs -> [skill:dotnet-api] (read `references/minimal-apis.md`)
- API versioning -> [skill:dotnet-api] (read `references/api-versioning.md`)
- OpenAPI/Swagger -> [skill:dotnet-api] (read `references/openapi.md`)
- Auth, CORS, rate limiting -> [skill:dotnet-api] (read `references/api-security.md`)
- Middleware -> [skill:dotnet-api] (read `references/middleware-patterns.md`)
- API surface tracking -> [skill:dotnet-api] (read `references/api-surface-validation.md`)
- Resilience/HTTP clients -> [skill:dotnet-api] (read `references/resilience.md`, `references/http-client.md`)
- EF Core -> [skill:dotnet-api] (read `references/efcore-patterns.md`, `references/efcore-architecture.md`)
- Data access strategy -> [skill:dotnet-api] (read `references/data-access-strategy.md`)
- Background services -> [skill:dotnet-api] (read `references/background-services.md`)
- gRPC -> [skill:dotnet-api] (read `references/grpc.md`)
- Real-time (SignalR, SSE) -> [skill:dotnet-api] (read `references/realtime-communication.md`)
- Messaging, event-driven -> [skill:dotnet-api] (read `references/messaging-patterns.md`)
- .NET Aspire -> [skill:dotnet-api] (read `references/aspire-patterns.md`)
- Semantic Kernel, AI -> [skill:dotnet-api] (read `references/semantic-kernel.md`)
- IO.Pipelines -> [skill:dotnet-api] (read `references/io-pipelines.md`)

### Security
- OWASP compliance -> [skill:dotnet-api] (read `references/security-owasp.md`)
- Secrets management -> [skill:dotnet-api] (read `references/secrets-management.md`)
- Cryptography -> [skill:dotnet-api] (read `references/cryptography.md`)
- Library API compat -> [skill:dotnet-api] (read `references/library-api-compat.md`)

### Building UI
- Choosing a framework -> [skill:dotnet-ui] (read `references/ui-chooser.md`)
- Accessibility -> [skill:dotnet-ui] (read `references/accessibility.md`)
- Blazor -> [skill:dotnet-ui] (read `references/blazor-patterns.md`, `references/blazor-components.md`, `references/blazor-auth.md`)
- Uno Platform -> [skill:dotnet-ui] (read `references/uno-platform.md`, `references/uno-targets.md`, `references/uno-mcp.md`)
- MAUI -> [skill:dotnet-ui] (read `references/maui-development.md`, `references/maui-aot.md`)
- WPF -> [skill:dotnet-ui] (read `references/wpf-modern.md`, `references/wpf-migration.md`)
- WinUI -> [skill:dotnet-ui] (read `references/winui.md`)
- WinForms -> [skill:dotnet-ui] (read `references/winforms-basics.md`)
- Localization -> [skill:dotnet-ui] (read `references/localization.md`)

### Testing
- Strategy -> [skill:dotnet-testing] (read `references/testing-strategy.md`)
- xUnit v3 -> [skill:dotnet-testing] (read `references/xunit.md`)
- Integration tests -> [skill:dotnet-testing] (read `references/integration-testing.md`)
- Playwright E2E -> [skill:dotnet-testing] (read `references/playwright.md`)
- Snapshot testing -> [skill:dotnet-testing] (read `references/snapshot-testing.md`)
- Coverage/quality -> [skill:dotnet-testing] (read `references/test-quality.md`)
- UI testing -> [skill:dotnet-testing] (read `references/ui-testing-core.md`) + [skill:dotnet-ui] for framework-specific
- Benchmarking -> [skill:dotnet-testing] (read `references/benchmarkdotnet.md`, `references/ci-benchmarking.md`)

### Performance Work
- Performance patterns -> [skill:dotnet-tooling] (read `references/performance-patterns.md`)
- Profiling -> [skill:dotnet-tooling] (read `references/profiling.md`)
- GC tuning, memory -> [skill:dotnet-tooling] (read `references/gc-memory.md`)

### Native AOT / Trimming
- AOT compilation -> [skill:dotnet-tooling] (read `references/native-aot.md`)
- AOT architecture -> [skill:dotnet-tooling] (read `references/aot-architecture.md`)
- Trimming -> [skill:dotnet-tooling] (read `references/trimming.md`)
- WASM AOT -> [skill:dotnet-testing] (read `references/aot-wasm.md`)

### CLI Tools
- System.CommandLine -> [skill:dotnet-tooling] (read `references/system-commandline.md`)
- CLI design -> [skill:dotnet-tooling] (read `references/cli-architecture.md`)
- CLI distribution/packaging -> [skill:dotnet-tooling] (read `references/cli-distribution.md`, `references/cli-packaging.md`, `references/cli-release-pipeline.md`)
- Tool management -> [skill:dotnet-tooling] (read `references/tool-management.md`)

### CI/CD Setup
- GitHub Actions -> [skill:dotnet-devops] (read `references/gha-patterns.md`, `references/gha-build-test.md`, `references/gha-publish.md`, `references/gha-deploy.md`)
- Azure DevOps -> [skill:dotnet-devops] (read `references/ado-patterns.md`, `references/ado-build-test.md`, `references/ado-publish.md`, `references/ado-unique.md`)

### Containers & Deployment
- Dockerfiles -> [skill:dotnet-devops] (read `references/containers.md`)
- Kubernetes/Compose -> [skill:dotnet-devops] (read `references/container-deployment.md`)

### Packaging & Releases
- NuGet -> [skill:dotnet-devops] (read `references/nuget-authoring.md`)
- MSIX -> [skill:dotnet-devops] (read `references/msix.md`)
- GitHub Releases -> [skill:dotnet-devops] (read `references/github-releases.md`)
- Versioning -> [skill:dotnet-devops] (read `references/release-management.md`)

### Observability & Logging
- OpenTelemetry -> [skill:dotnet-devops] (read `references/observability.md`)
- Structured logging -> [skill:dotnet-devops] (read `references/structured-logging.md`)

### Multi-Targeting & Upgrades
- Multi-TFM builds -> [skill:dotnet-tooling] (read `references/multi-targeting.md`)
- Version upgrades -> [skill:dotnet-tooling] (read `references/version-upgrade.md`)

### Documentation
- Doc strategy -> [skill:dotnet-tooling] (read `references/documentation-strategy.md`)
- Mermaid diagrams -> [skill:dotnet-tooling] (read `references/mermaid-diagrams.md`)
- GitHub docs -> [skill:dotnet-devops] (read `references/github-docs.md`)
- XML docs -> [skill:dotnet-tooling] (read `references/xml-docs.md`)

### Agent Assistance
- Agent making .NET mistakes -> [skill:dotnet-api] (read `references/agent-gotchas.md`)
- Build errors -> [skill:dotnet-tooling] (read `references/build-analysis.md`)
- Reading .csproj -> [skill:dotnet-tooling] (read `references/csproj-reading.md`)
- Navigating solutions -> [skill:dotnet-tooling] (read `references/solution-navigation.md`)

### Debugging
- Crash dumps, hangs, WinDbg -> [skill:dotnet-debugging]

### Specialist Agent Routing

For complex analysis that benefits from domain expertise, delegate to specialist agents:

- Async/await performance, ValueTask, ConfigureAwait, IO.Pipelines -> [skill:dotnet-async-performance-specialist]
- ASP.NET Core middleware, request pipeline, DI lifetimes, diagnostic scenarios -> [skill:dotnet-aspnetcore-specialist]
- Test architecture, test type selection, test data management, microservice testing -> [skill:dotnet-testing-specialist]
- Cloud deployment, .NET Aspire, AKS, CI/CD pipelines, distributed tracing -> [skill:dotnet-cloud-specialist]
- General code review (correctness, performance, security, architecture) -> [skill:dotnet-code-review-agent]
