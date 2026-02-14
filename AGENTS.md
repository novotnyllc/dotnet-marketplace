# dotnet-artisan -- Agent Guide

**dotnet-artisan** provides .NET development skills for Claude Code. This file contains the skill routing index and agent delegation patterns for human readers and agents consuming AGENTS.md. For the full internal routing logic, see the `dotnet-advisor` skill.

## Skill Routing Index

The plugin organizes 97 skills into 18 categories. Use this index to identify which category covers your domain.

| Category | Count | When to Use |
|---|---|---|
| **Foundation** | 4 | Project analysis, version detection, skill routing, plugin publishing |
| **Core C#** | 7 | Modern C# patterns, async/await, DI, configuration, NRTs, source generators |
| **Project Structure** | 6 | Solution layout, scaffolding, analyzers, CI setup, testing setup, modernization |
| **Architecture** | 10 | Architecture patterns, EF Core, background services, resilience, HTTP clients, containers |
| **Serialization** | 4 | gRPC, SignalR/real-time, JSON/Protobuf serialization, service communication |
| **Testing** | 10 | Test strategy, xUnit v3, integration testing, UI testing, Playwright, snapshot testing |
| **API Development** | 5 | Minimal APIs, versioning, OpenAPI, API security, input validation |
| **Security** | 3 | OWASP compliance, secrets management, cryptography |
| **UI Frameworks** | 13 | Blazor, Uno Platform, MAUI, WinUI, WPF, WinForms, UI framework selection |
| **Native AOT** | 4 | Native AOT compilation, trimming, AOT architecture, WASM AOT |
| **CLI Tools** | 5 | System.CommandLine, CLI architecture, distribution, packaging, release pipelines |
| **Agent Meta-Skills** | 4 | Agent gotchas, build analysis, csproj reading, solution navigation |
| **Performance** | 4 | BenchmarkDotNet, performance patterns, profiling, CI benchmarking |
| **CI/CD** | 8 | GitHub Actions (patterns, build, publish, deploy), Azure DevOps (patterns, build, publish, unique) |
| **Packaging** | 3 | NuGet authoring, MSIX, GitHub Releases |
| **Release Management** | 1 | NBGV versioning, changelogs, SemVer strategy |
| **Documentation** | 5 | Doc strategy, Mermaid diagrams, GitHub docs, XML docs, API docs |
| **Localization** | 1 | i18n with .resx, IStringLocalizer, RTL, pluralization |

For the complete skill-level catalog with routing decision trees, see the `dotnet-advisor` skill at `skills/foundation/dotnet-advisor/SKILL.md`.

## Agent Delegation Patterns

The plugin includes 9 specialist agents. The central router (`dotnet-architect`) analyzes project context and delegates to the appropriate specialist.

| Agent | Domain | Preloaded Skills | When to Delegate |
|---|---|---|---|
| **dotnet-architect** | Architecture & routing | dotnet-advisor, dotnet-version-detection, dotnet-project-analysis | Framework selection, architecture review, project structure decisions |
| **dotnet-csharp-concurrency-specialist** | Concurrency & threading | dotnet-csharp-async-patterns, dotnet-csharp-modern-patterns | Race conditions, deadlocks, thread safety, synchronization bugs |
| **dotnet-security-reviewer** | Security review | dotnet-advisor, dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography | OWASP compliance, secrets exposure, cryptographic misuse, security audit |
| **dotnet-blazor-specialist** | Blazor development | dotnet-version-detection, dotnet-project-analysis, dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth | Render modes, component design, Blazor auth, state management |
| **dotnet-uno-specialist** | Uno Platform | dotnet-version-detection, dotnet-project-analysis, dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp | Cross-platform Uno apps, Extensions ecosystem, MVUX, MCP integration |
| **dotnet-maui-specialist** | .NET MAUI | dotnet-version-detection, dotnet-project-analysis, dotnet-maui-development, dotnet-maui-aot | MAUI apps, platform-specific code, Xamarin migration, iOS AOT |
| **dotnet-performance-analyst** | Performance analysis | dotnet-profiling, dotnet-benchmarkdotnet, dotnet-observability | Profiling data interpretation, benchmark regressions, GC analysis |
| **dotnet-benchmark-designer** | Benchmark design | dotnet-benchmarkdotnet, dotnet-performance-patterns | BenchmarkDotNet setup, measurement methodology, diagnoser selection |
| **dotnet-docs-generator** | Documentation | dotnet-documentation-strategy, dotnet-mermaid-diagrams, dotnet-xml-docs | README generation, architecture diagrams, XML doc skeletons, doc tooling |

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
- **Performance agents** (analyst vs designer) split on interpretation vs methodology
- **Security reviewer** is read-only -- produces findings, does not modify code
- **Docs generator** is the only agent with write tools (Edit, Write) -- all others are read-only analysis

## Cross-References

- [README.md](README.md) -- Full skill catalog with counts, architecture diagrams, installation, and usage examples
- [CONTRIBUTING.md](CONTRIBUTING.md) -- Skill authoring guide, PR process, validation requirements, directory conventions

---

<!-- BEGIN FLOW-NEXT -->
## Flow-Next

This project uses Flow-Next for task tracking. Use `.flow/bin/flowctl` instead of markdown TODOs or TodoWrite.

**Quick commands:**
```bash
.flow/bin/flowctl list                # List all epics + tasks
.flow/bin/flowctl epics               # List all epics
.flow/bin/flowctl tasks --epic fn-N   # List tasks for epic
.flow/bin/flowctl ready --epic fn-N   # What's ready
.flow/bin/flowctl show fn-N.M         # View task
.flow/bin/flowctl start fn-N.M        # Claim task
.flow/bin/flowctl done fn-N.M --summary-file s.md --evidence-json e.json
```

**Rules:**
- Use `.flow/bin/flowctl` for ALL task tracking
- Do NOT create markdown TODOs or use TodoWrite
- Re-anchor (re-read spec + status) before every task

**More info:** `.flow/bin/flowctl --help` or read `.flow/usage.md`
<!-- END FLOW-NEXT -->
