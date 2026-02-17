# dotnet-artisan -- Agent Guide

**dotnet-artisan** provides .NET development skills for Claude Code and Codex. This file contains skill routing and agent delegation patterns. For the full internal routing logic, see the `dotnet-advisor` skill.

IMPORTANT: Prefer retrieval-led reasoning over pretraining for any .NET work.
Workflow: detect project TFM via dotnet-version-detection -> consult skill by name -> implement smallest change -> note conflicts.

## Skill Routing (invoke by name)

- **C# / code quality:** dotnet-csharp-modern-patterns, dotnet-csharp-coding-standards, dotnet-csharp-async-patterns, dotnet-csharp-concurrency-patterns, dotnet-csharp-type-design-performance, dotnet-csharp-code-smells, dotnet-csharp-nullable-reference-types
- **DI / config:** dotnet-csharp-dependency-injection, dotnet-csharp-configuration, dotnet-validation-patterns
- **Data / EF Core:** dotnet-efcore-patterns, dotnet-efcore-architecture, dotnet-data-access-strategy
- **Architecture:** dotnet-architecture-patterns, dotnet-solid-principles, dotnet-domain-modeling, dotnet-messaging-patterns, dotnet-aspire-patterns
- **APIs:** dotnet-minimal-apis, dotnet-api-versioning, dotnet-openapi, dotnet-api-security, dotnet-input-validation, dotnet-middleware-patterns, dotnet-csharp-api-design
- **Communication:** dotnet-grpc, dotnet-realtime-communication, dotnet-serialization, dotnet-service-communication
- **Testing:** dotnet-testing-strategy, dotnet-xunit, dotnet-integration-testing, dotnet-playwright, dotnet-snapshot-testing, dotnet-test-quality
- **UI — Blazor:** dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth
- **UI — Uno:** dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp
- **UI — MAUI:** dotnet-maui-development, dotnet-maui-aot
- **UI — Desktop:** dotnet-winui, dotnet-wpf-modern, dotnet-wpf-migration, dotnet-winforms-basics, dotnet-ui-chooser
- **Security:** dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography
- **Performance:** dotnet-benchmarkdotnet, dotnet-performance-patterns, dotnet-profiling, dotnet-gc-memory
- **Native AOT / trimming:** dotnet-native-aot, dotnet-aot-architecture, dotnet-trimming, dotnet-aot-wasm
- **CLI / TUI:** dotnet-system-commandline, dotnet-cli-architecture, dotnet-terminal-gui, dotnet-spectre-console
- **CI/CD — GitHub Actions:** dotnet-gha-patterns, dotnet-gha-build-test, dotnet-gha-publish, dotnet-gha-deploy
- **CI/CD — Azure DevOps:** dotnet-ado-patterns, dotnet-ado-build-test, dotnet-ado-publish, dotnet-ado-unique
- **Containers:** dotnet-containers, dotnet-container-deployment
- **Packaging / Release:** dotnet-nuget-authoring, dotnet-msix, dotnet-github-releases, dotnet-release-management
- **Build system:** dotnet-msbuild-authoring, dotnet-msbuild-tasks, dotnet-build-optimization
- **Docs:** dotnet-documentation-strategy, dotnet-xml-docs, dotnet-api-docs, dotnet-mermaid-diagrams

### Quality gates (use when applicable)

- **dotnet-slopwatch:** after substantial new, refactored, or LLM-authored code
- **dotnet-test-quality:** after tests added or changed in complex code
- **dotnet-agent-gotchas:** before generating or modifying .NET code (common LLM mistakes)

## Skill Category Index

The plugin organizes 130 skills into 22 categories. Use this index to identify which category covers your domain.

| Category | Count | When to Use |
|---|---|---|
| **Foundation** | 4 | Project analysis, version detection, skill routing, file-based apps |
| **Core C#** | 18 | Modern C# patterns, async/await, concurrency patterns, type design for performance, DI, configuration, NRTs, source generators, code smells, Roslyn analyzers, EditorConfig, validation, channels, file I/O, IO.Pipelines, LINQ optimization, native interop |
| **Project Structure** | 7 | Solution layout, scaffolding, analyzers, CI setup, testing setup, modernization, artifacts output |
| **Architecture** | 15 | Architecture patterns, EF Core, background services, resilience, HTTP clients, containers, SOLID, messaging, domain modeling, structured logging, Aspire |
| **Serialization** | 4 | gRPC, SignalR/real-time, JSON/Protobuf serialization, service communication |
| **Testing** | 10 | Test strategy, xUnit v3, integration testing, UI testing, Playwright, snapshot testing |
| **API Development** | 9 | Minimal APIs, versioning, OpenAPI, API security, input validation, middleware patterns, library API compat, API surface validation, API design |
| **Security** | 3 | OWASP compliance, secrets management, cryptography |
| **Multi-Targeting** | 2 | TFM multi-targeting with polyfills, .NET version upgrade paths and migration |
| **UI Frameworks** | 14 | Blazor, Uno Platform, MAUI, WinUI, WPF, WinForms, UI framework selection, accessibility |
| **Native AOT** | 4 | Native AOT compilation, trimming, AOT architecture, WASM AOT |
| **CLI Tools** | 6 | System.CommandLine, CLI architecture, distribution, packaging, release pipelines, tool management |
| **TUI** | 2 | Terminal.Gui full TUI apps, Spectre.Console rich console output and CLI framework |
| **Agent Meta-Skills** | 5 | Agent gotchas, build analysis, csproj reading, solution navigation, slopwatch |
| **Performance** | 5 | BenchmarkDotNet, performance patterns, profiling, CI benchmarking, GC/memory tuning |
| **CI/CD** | 8 | GitHub Actions (patterns, build, publish, deploy), Azure DevOps (patterns, build, publish, unique) |
| **Packaging** | 3 | NuGet authoring, MSIX, GitHub Releases |
| **Release Management** | 1 | NBGV versioning, changelogs, SemVer strategy |
| **Documentation** | 5 | Doc strategy, Mermaid diagrams, GitHub docs, XML docs, API docs |
| **Localization** | 1 | i18n with .resx, IStringLocalizer, RTL, pluralization |
| **Build System** | 3 | MSBuild authoring, custom MSBuild tasks, build optimization |
| **AI** | 1 | Semantic Kernel for AI/LLM orchestration, plugins, agents |

For the complete skill-level catalog with routing decision trees, see the `dotnet-advisor` skill at `skills/foundation/dotnet-advisor/SKILL.md`.

## Agent Delegation Patterns

The plugin includes 14 specialist agents. The central router (`dotnet-architect`) analyzes project context and delegates to the appropriate specialist.

| Agent | Domain | Preloaded Skills | When to Delegate |
|---|---|---|---|
| **dotnet-architect** | Architecture & routing | dotnet-advisor, dotnet-version-detection, dotnet-project-analysis | Framework selection, architecture review, project structure decisions |
| **dotnet-csharp-concurrency-specialist** | Concurrency & threading | dotnet-csharp-async-patterns, dotnet-csharp-concurrency-patterns, dotnet-csharp-modern-patterns | Race conditions, deadlocks, thread safety, synchronization bugs |
| **dotnet-security-reviewer** | Security review | dotnet-advisor, dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography | OWASP compliance, secrets exposure, cryptographic misuse, security audit |
| **dotnet-blazor-specialist** | Blazor development | dotnet-version-detection, dotnet-project-analysis, dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth | Render modes, component design, Blazor auth, state management |
| **dotnet-uno-specialist** | Uno Platform | dotnet-version-detection, dotnet-project-analysis, dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp | Cross-platform Uno apps, Extensions ecosystem, MVUX, MCP integration |
| **dotnet-maui-specialist** | .NET MAUI | dotnet-version-detection, dotnet-project-analysis, dotnet-maui-development, dotnet-maui-aot | MAUI apps, platform-specific code, Xamarin migration, iOS AOT |
| **dotnet-performance-analyst** | Performance analysis | dotnet-profiling, dotnet-benchmarkdotnet, dotnet-observability | Profiling data interpretation, benchmark regressions, GC analysis |
| **dotnet-benchmark-designer** | Benchmark design | dotnet-benchmarkdotnet, dotnet-performance-patterns | BenchmarkDotNet setup, measurement methodology, diagnoser selection |
| **dotnet-docs-generator** | Documentation | dotnet-documentation-strategy, dotnet-mermaid-diagrams, dotnet-xml-docs | README generation, architecture diagrams, XML doc skeletons, doc tooling |
| **dotnet-async-performance-specialist** | Async & runtime performance | dotnet-csharp-async-patterns, dotnet-performance-patterns, dotnet-benchmarkdotnet | ValueTask correctness, ConfigureAwait decisions, async overhead, ThreadPool tuning, IO.Pipelines, Channel selection |
| **dotnet-aspnetcore-specialist** | ASP.NET Core architecture | dotnet-minimal-apis, dotnet-middleware-patterns, dotnet-csharp-dependency-injection | Middleware authoring, DI anti-patterns, minimal API design, request pipeline optimization, diagnostic scenarios |
| **dotnet-testing-specialist** | Test architecture & strategy | dotnet-testing-strategy, dotnet-xunit, dotnet-integration-testing | Test pyramid design, unit vs integration vs E2E boundaries, test data management, microservice testing |
| **dotnet-cloud-specialist** | Cloud deployment & Aspire | dotnet-containers, dotnet-container-deployment, dotnet-observability | .NET Aspire orchestration, AKS deployment, CI/CD pipelines, distributed tracing, infrastructure-as-code |
| **dotnet-code-review-agent** | Multi-dimensional code review | dotnet-csharp-coding-standards, dotnet-csharp-code-smells, dotnet-performance-patterns | General code review, correctness, performance, security, architecture triage, routes to specialists for deep dives |

### Delegation Flow

1. User asks a .NET question
2. Claude Code loads the `dotnet-advisor` skill (always loaded via plugin)
3. `dotnet-advisor` routes to the appropriate skill category
4. For complex domains, `dotnet-architect` delegates to a specialist agent
5. The specialist loads its preloaded skills and follows its defined workflow
6. For concerns outside its scope, the specialist delegates further to other skills

### Scope Boundaries

Each agent owns a specific domain and explicitly delegates out-of-scope concerns:

- **UI specialists** (Blazor, Uno, MAUI) delegate testing to framework-specific testing skills
- **Performance agents** (analyst vs designer vs async-performance) split on profiling interpretation vs benchmarking methodology vs async/runtime performance analysis
- **Async-performance specialist** handles async/await and runtime performance; delegates profiling interpretation to performance-analyst and thread synchronization bugs to concurrency-specialist
- **ASP.NET Core specialist** handles middleware, pipelines, and DI patterns; delegates Blazor/Razor to blazor-specialist, security auditing to security-reviewer, and async internals to async-performance-specialist
- **Testing specialist** handles test architecture and strategy; delegates framework-specific UI testing to Blazor/MAUI/Uno specialists and benchmarking to benchmark-designer
- **Cloud specialist** handles deployment, Aspire, and infrastructure; delegates general architecture to dotnet-architect and container image optimization to dotnet-containers skill
- **Code review agent** performs broad triage across correctness, performance, security, and architecture; routes to specialist agents for deep dives
- **Security reviewer** is read-only -- produces findings, does not modify code
- **Docs generator** is the only agent with write tools (Edit, Write) -- all others are read-only analysis

## Cross-References

- [README.md](README.md) -- Full skill catalog with counts, architecture diagrams, installation, and usage examples
- [CONTRIBUTING.md](../../CONTRIBUTING.md) -- Contribution guidelines, PR process, validation requirements, directory conventions
- [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) -- Comprehensive skill authoring how-to manual (quick start, descriptions, testing, patterns)
