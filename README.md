# dotnet-artisan

> Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications

[![CI](https://github.com/novotnyllc/dotnet-artisan/actions/workflows/validate.yml/badge.svg)](https://github.com/novotnyllc/dotnet-artisan/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](.claude-plugin/plugin.json)

## Overview

**dotnet-artisan** is a Claude Code plugin that provides 131 skills and 14 specialist agents for .NET development. It is compatible with Claude Code, GitHub Copilot CLI, and OpenAI Codex. It follows the [Agent Skills](https://github.com/anthropics/agent-skills) open standard for skill authoring and discovery.

The plugin covers the full breadth of the .NET ecosystem:
- Modern C# patterns, async/await, dependency injection, and source generators
- ASP.NET Core APIs, Blazor, MAUI, Uno Platform, WinUI, and WPF
- Entity Framework Core, data access strategies, and serialization
- Testing with xUnit, integration testing, Playwright, and snapshot testing
- CI/CD for GitHub Actions and Azure DevOps
- Native AOT, trimming, performance profiling, and benchmarking
- Security, packaging, documentation, and release management

## Installation

### Claude Code

From within Claude Code, run:

```
/plugin marketplace add novotnyllc/dotnet-artisan
```

Once installed, Claude Code automatically loads relevant skills based on your questions about .NET development.

### GitHub Copilot CLI

Install the plugin as a Copilot skill:

```bash
copilot skill install novotnyllc/dotnet-artisan@dotnet-artisan
```

The flat `skills/<skill-name>/` layout is compatible with Copilot's one-level-deep skill scanning.

### OpenAI Codex

Codex discovers skills via the `.agents/openai.yaml` manifest at the repository root. Install with the Codex skill installer or sync skill directories into `~/.codex/skills/`.

## Skill Catalog

The plugin organizes 131 skills in a flat directory layout (`skills/<skill-name>/SKILL.md`). Each skill follows the Agent Skills open standard with a `SKILL.md` file containing structured frontmatter (`name`, `description`) and rich guidance content.

| Category | Count | Example Skills |
|---|---|---|
| **Foundation** | 4 | dotnet-advisor, dotnet-version-detection, dotnet-project-analysis, dotnet-file-based-apps |
| **Core C#** | 18 | dotnet-csharp-modern-patterns, dotnet-csharp-async-patterns, dotnet-csharp-concurrency-patterns, dotnet-csharp-type-design-performance, dotnet-native-interop, dotnet-file-io, dotnet-io-pipelines, dotnet-linq-optimization |
| **Project Structure** | 7 | dotnet-project-structure, dotnet-scaffold-project, dotnet-artifacts-output, dotnet-modernize |
| **Architecture** | 15 | dotnet-architecture-patterns, dotnet-efcore-patterns, dotnet-messaging-patterns, dotnet-aspire-patterns |
| **Serialization** | 4 | dotnet-grpc, dotnet-realtime-communication, dotnet-serialization |
| **Testing** | 10 | dotnet-testing-strategy, dotnet-xunit, dotnet-integration-testing |
| **API Development** | 9 | dotnet-minimal-apis, dotnet-api-versioning, dotnet-openapi, dotnet-csharp-api-design |
| **Security** | 3 | dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography |
| **Multi-Targeting** | 2 | dotnet-multi-targeting, dotnet-version-upgrade |
| **UI Frameworks** | 14 | dotnet-blazor-patterns, dotnet-maui-development, dotnet-uno-platform, dotnet-accessibility |
| **Native AOT** | 4 | dotnet-native-aot, dotnet-trimming, dotnet-aot-wasm |
| **CLI Tools** | 6 | dotnet-system-commandline, dotnet-cli-architecture, dotnet-cli-distribution, dotnet-tool-management |
| **TUI** | 2 | dotnet-terminal-gui, dotnet-spectre-console |
| **Agent Meta-Skills** | 5 | dotnet-agent-gotchas, dotnet-build-analysis, dotnet-csproj-reading, dotnet-slopwatch |
| **Performance** | 5 | dotnet-benchmarkdotnet, dotnet-performance-patterns, dotnet-gc-memory |
| **CI/CD** | 8 | dotnet-gha-patterns, dotnet-gha-build-test, dotnet-ado-patterns |
| **Packaging** | 3 | dotnet-nuget-authoring, dotnet-msix, dotnet-github-releases |
| **Release Management** | 1 | dotnet-release-management |
| **Documentation** | 5 | dotnet-documentation-strategy, dotnet-mermaid-diagrams, dotnet-github-docs |
| **Localization** | 1 | dotnet-localization |
| **Build System** | 3 | dotnet-msbuild-authoring, dotnet-msbuild-tasks, dotnet-build-optimization |
| **AI** | 1 | dotnet-semantic-kernel |

## Agents

The plugin includes 14 specialist agents that provide focused expertise in specific domains. The central routing agent, `dotnet-architect`, analyzes your query context and delegates to the appropriate specialist.

| Agent | Description |
|---|---|
| **dotnet-architect** | Analyzes project context, requirements, and constraints to recommend architecture approaches, framework choices, and design patterns |
| **dotnet-csharp-concurrency-specialist** | Debugs race conditions, deadlocks, thread safety issues, and synchronization problems in .NET code |
| **dotnet-security-reviewer** | Reviews .NET code for security vulnerabilities, OWASP compliance, secrets exposure, and cryptographic misuse |
| **dotnet-blazor-specialist** | Guides Blazor development across all hosting models (Server, WASM, Hybrid, Auto) including components, state, and auth |
| **dotnet-uno-specialist** | Builds cross-platform Uno Platform apps with Extensions ecosystem, MVUX patterns, Toolkit controls, and MCP integration |
| **dotnet-maui-specialist** | Builds .NET MAUI apps with platform-specific development, Xamarin migration, and Native AOT on iOS/Catalyst |
| **dotnet-performance-analyst** | Analyzes profiling data, benchmark results, GC behavior, and diagnoses performance bottlenecks |
| **dotnet-benchmark-designer** | Designs BenchmarkDotNet benchmarks, prevents measurement bias, and validates benchmark methodology |
| **dotnet-docs-generator** | Generates documentation including Mermaid diagrams, XML doc skeletons, and GitHub-native docs |
| **dotnet-async-performance-specialist** | Analyzes ValueTask correctness, ConfigureAwait decisions, async overhead, ThreadPool tuning |
| **dotnet-aspnetcore-specialist** | Guides middleware authoring, DI patterns, minimal API design, and request pipeline optimization |
| **dotnet-testing-specialist** | Designs test pyramids, unit vs integration vs E2E boundaries, test data management |
| **dotnet-cloud-specialist** | Guides .NET Aspire orchestration, AKS deployment, distributed tracing, infrastructure-as-code |
| **dotnet-code-review-agent** | Performs multi-dimensional code review across correctness, performance, security, and architecture |

## Architecture

### Plugin Structure

```mermaid
graph TB
    subgraph Plugin["dotnet-artisan Plugin"]
        direction TB
        PJ[plugin.json]

        subgraph Agents["14 Specialist Agents"]
            DA[dotnet-architect<br/>Central Router]
            CSC[concurrency-specialist]
            SR[security-reviewer]
            BSA[blazor-specialist]
            US[uno-specialist]
            MS[maui-specialist]
            PA[performance-analyst]
            BD[benchmark-designer]
            DG[docs-generator]
            ASP[async-performance-specialist]
            ASN[aspnetcore-specialist]
            TS[testing-specialist]
            CS[cloud-specialist]
            CR[code-review-agent]
        end

        subgraph Skills["131 Skills"]
            F[Foundation<br/>4 skills]
            CC[Core C#<br/>18 skills]
            PS[Project Structure<br/>7 skills]
            AR[Architecture<br/>15 skills]
            SE[Serialization<br/>4 skills]
            TE[Testing<br/>10 skills]
            AD[API Development<br/>9 skills]
            SC[Security<br/>3 skills]
            MT[Multi-Targeting<br/>2 skills]
            UI[UI Frameworks<br/>14 skills]
            NA[Native AOT<br/>4 skills]
            CL[CLI Tools<br/>6 skills]
            TU[TUI<br/>2 skills]
            AM[Agent Meta-Skills<br/>5 skills]
            PE[Performance<br/>5 skills]
            CI[CI/CD<br/>8 skills]
            PK[Packaging<br/>3 skills]
            RM[Release Mgmt<br/>1 skill]
            DO[Documentation<br/>5 skills]
            LO[Localization<br/>1 skill]
            BSys[Build System<br/>3 skills]
            AI[AI<br/>1 skill]
        end

        subgraph Infra["Infrastructure"]
            HK[hooks/hooks.json]
            MCP[.mcp.json]
        end
    end

    DA --> BSA
    DA --> US
    DA --> MS
    DA --> CSC
    DA --> SR
    DA --> PA
    DA --> BD
    DA --> DG
    DA --> ASP
    DA --> ASN
    DA --> TS
    DA --> CS
    DA --> CR

    BSA --> UI
    US --> UI
    MS --> UI
    CSC --> CC
    SR --> SC
    PA --> PE
    BD --> PE
    DG --> DO
    DA --> AR
    DA --> F
```

### Agent Delegation Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude as Claude Code
    participant Router as dotnet-architect<br/>(Routing Agent)
    participant Specialist as Specialist Agent
    participant Skills as Skill Files

    User->>Claude: "How do I set up Blazor auth?"
    Claude->>Router: Route query
    Router->>Router: Load dotnet-advisor catalog<br/>+ analyze query context
    Router->>Specialist: Delegate to blazor-specialist
    Specialist->>Skills: Load dotnet-blazor-auth<br/>+ dotnet-blazor-patterns
    Skills-->>Specialist: Skill content
    Specialist-->>Claude: Structured guidance
    Claude-->>User: Blazor auth recommendation<br/>with code examples
```

## Usage Examples

**Ask about project architecture:**
> "I have a new .NET 9 web API project. What architecture pattern should I use for a medium-sized e-commerce backend?"

Claude Code loads `dotnet-architecture-patterns` and `dotnet-project-structure` to recommend a clean architecture approach with specific project layout, middleware pipeline, and dependency injection configuration.

**Debug a concurrency issue:**
> "I'm getting intermittent failures in my background service that processes messages from a queue. Sometimes messages are processed twice."

The `dotnet-csharp-concurrency-specialist` agent activates, loading `dotnet-csharp-async-patterns` and `dotnet-background-services` to diagnose the race condition and recommend idempotency patterns.

**Set up CI/CD:**
> "Help me create a GitHub Actions workflow that builds, tests, and publishes my NuGet package."

Claude Code loads `dotnet-gha-build-test` and `dotnet-gha-publish` to generate a complete workflow with proper versioning, test matrix, and NuGet push configuration.

## Agent Skill Routing Checks

This repo includes a CI-ready routing checker to verify that agents discover and use expected skills.

- Live full-corpus checks (manual/scheduled):
  - `./test.sh`

See `docs/agent-routing-tests.md` for details, workflow inputs, and environment variables.

## Contributing

See [CONTRIBUTING-SKILLS.md](CONTRIBUTING-SKILLS.md) for the skill authoring guide, or [CONTRIBUTING.md](CONTRIBUTING.md) for the general contribution workflow.

## Acknowledgements

- The [Claude Code plugin system](https://docs.anthropic.com/en/docs/claude-code/plugins) and [Agent Skills](https://github.com/anthropics/agent-skills) open standard for enabling structured, discoverable development skills
- The [.NET community and ecosystem](https://dotnet.microsoft.com/) for the frameworks, libraries, and patterns documented in these skills
- All [contributors](https://github.com/novotnyllc/dotnet-artisan/graphs/contributors) who help improve and expand the plugin

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
