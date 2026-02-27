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
- Deep implementation content -- see each domain skill ([skill:dotnet-csharp], [skill:dotnet-api], [skill:dotnet-ui], [skill:dotnet-testing], [skill:dotnet-devops], [skill:dotnet-tooling], [skill:dotnet-debugging]) and their companion files

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

## Skill Catalog

| Skill | Summary | Differentiator |
|-------|---------|----------------|
| [skill:dotnet-csharp] | C# language patterns, coding standards, async/await, DI, LINQ, domain modeling | Language-level guidance, always loaded as baseline |
| [skill:dotnet-api] | ASP.NET Core, EF Core, gRPC, SignalR, resilience, security, Aspire | Backend services and data access |
| [skill:dotnet-ui] | Blazor, MAUI, Uno Platform, WPF, WinUI, WinForms, accessibility | All UI frameworks and cross-platform targets |
| [skill:dotnet-testing] | xUnit v3, integration/E2E, Playwright, snapshots, benchmarks | Test strategy, frameworks, and quality gates |
| [skill:dotnet-devops] | GitHub Actions, Azure DevOps, containers, NuGet, observability | CI/CD pipelines, packaging, and operations |
| [skill:dotnet-tooling] | Project setup, MSBuild, Native AOT, profiling, CLI apps, version detection | Build system, performance, and developer tools |
| [skill:dotnet-debugging] | WinDbg MCP, crash dumps, hang analysis, memory diagnostics | Live and post-mortem dump analysis |
| dotnet-advisor | This skill -- routes to domain skills above | Entry point, always loaded first |

---

## Cross-Domain Playbooks

Multi-skill routing recipes for common scenarios. Each domain skill's own Routing Table handles topic-to-file mapping; these playbooks identify which skills to combine.

- **New API service:** [skill:dotnet-tooling] (scaffold) + [skill:dotnet-api] (architecture) + [skill:dotnet-devops] (CI/CD) + [skill:dotnet-testing] (test strategy)
- **Starting a new project:** [skill:dotnet-tooling] (version detection, project structure) + [skill:dotnet-csharp] (coding standards)
- **UI application:** [skill:dotnet-ui] (framework choice, components) + [skill:dotnet-csharp] (patterns) + [skill:dotnet-testing] (UI testing)
- **Performance optimization:** [skill:dotnet-tooling] (profiling, AOT, GC) + [skill:dotnet-testing] (benchmarks) + [skill:dotnet-csharp] (patterns)
- **CLI tool end-to-end:** [skill:dotnet-tooling] (System.CommandLine, CLI design) + [skill:dotnet-devops] (packaging, distribution, releases)
- **Cloud-native service:** [skill:dotnet-api] (Aspire, architecture) + [skill:dotnet-devops] (containers, observability) + [skill:dotnet-testing] (integration tests)
- **Security audit:** [skill:dotnet-api] (OWASP, secrets, crypto) + [skill:dotnet-csharp] (input validation)
- **Documentation sprint:** [skill:dotnet-tooling] (doc strategy, Mermaid, XML docs) + [skill:dotnet-devops] (GitHub docs)
- **Agent troubleshooting:** [skill:dotnet-api] (agent gotchas) + [skill:dotnet-tooling] (build analysis, solution navigation)

---

## Specialist Agent Routing

For complex analysis that benefits from domain expertise, delegate to specialist agents:

- Architecture review, framework selection, design patterns -> [skill:dotnet-architect]
- ASP.NET Core middleware, request pipeline, DI lifetimes, diagnostic scenarios -> [skill:dotnet-aspnetcore-specialist]
- Async/await performance, ValueTask, ConfigureAwait, IO.Pipelines -> [skill:dotnet-async-performance-specialist]
- Benchmark design, measurement methodology, diagnoser selection -> [skill:dotnet-benchmark-designer]
- Blazor components, render modes, hosting models, auth -> [skill:dotnet-blazor-specialist]
- Cloud deployment, .NET Aspire, AKS, CI/CD pipelines, distributed tracing -> [skill:dotnet-cloud-specialist]
- General code review (correctness, performance, security, architecture) -> [skill:dotnet-code-review-agent]
- Race conditions, deadlocks, thread safety, synchronization -> [skill:dotnet-csharp-concurrency-specialist]
- Documentation generation, XML docs, Mermaid diagrams, README scaffolding -> [skill:dotnet-docs-generator]
- .NET MAUI development, platform targets, Xamarin migration, MAUI AOT -> [skill:dotnet-maui-specialist]
- Performance profiling, flame graphs, heap dumps, benchmark regression -> [skill:dotnet-performance-analyst]
- Security vulnerabilities, OWASP compliance, secrets exposure, crypto review -> [skill:dotnet-security-reviewer]
- Test architecture, test type selection, test data management, microservice testing -> [skill:dotnet-testing-specialist]
- Uno Platform, Extensions ecosystem, MVUX, multi-target deployment -> [skill:dotnet-uno-specialist]
