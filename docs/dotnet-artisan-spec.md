# dotnet-artisan: Comprehensive .NET Coding Agent Skills Plugin

## Overview

**Plugin Name:** `dotnet-artisan`
**License:** MIT
**Format:** Single Claude Code plugin (primary) with cross-agent compatibility for GitHub Copilot and OpenAI Codex
**Audience:** Agent-first (optimized for AI agent comprehension)
**Style:** Opinionated (prescribe the modern best practice by default)
**Versioning:** SemVer + CHANGELOG.md + GitHub Releases, with NBGV stamping in generated artifacts

---

## Core Design Principles

1. **Active version detection**: Skills must read TFMs from `.csproj`/`Directory.Build.props` to adapt guidance to the project's actual target framework
2. **Preview-aware**: If a project targets a preview TFM or has preview features enabled (e.g., `<LangVersion>preview</LangVersion>`), skills should leverage preview features
3. **Modern .NET first**: Default to .NET 10 (current LTS, released Nov 2025) and C# 14. Be aware of .NET 11 Preview 1 (released Feb 10, 2026) with C# 15 preview and `net11.0` TFM
4. **Polyfill-forward**: Use PolySharp and SimonCropp/Polyfill to bring latest language features to older target frameworks
5. **AOT-friendly**: Prefer source-generator-based approaches over reflection throughout
6. **Cross-agent**: Use Agent Skills open standard (SKILL.md) as canonical format; generate per-agent outputs via build pipeline for Claude Code plugin, Copilot instructions, and Codex AGENTS.md

---

## Current .NET Landscape (Feb 2026)

### Version Matrix

| Version | Status | C# Version | TFM | Support End |
|---------|--------|-------------|-----|-------------|
| .NET 8 | LTS (active) | C# 12 | net8.0 | Nov 2026 |
| .NET 9 | STS | C# 13 | net9.0 | Nov 2026 |
| .NET 10 | LTS (current) | C# 14 | net10.0 | Nov 2028 |
| .NET 11 | Preview 1 | C# 15 (preview) | net11.0 | ~Nov 2028 (STS) |

### Key .NET 10 Features
- C# 14: field-backed properties, `field` contextual keyword, `nameof` for unbound generics, extension improvements
- Post-quantum cryptography (ML-KEM, ML-DSA, SLH-DSA)
- Microsoft Agent Framework (Semantic Kernel + AutoGen)
- ASP.NET Core: Minimal API validation, Server-Sent Events, OpenAPI 3.1, passkey auth
- Runtime: JIT inlining, devirtualization, AVX10.2, NativeAOT enhancements
- Blazor: WebAssembly preloading, form validation, diagnostics

### Key .NET 11 Preview 1 Features (Feb 10, 2026)
- Zstandard compression, BFloat16 type, Runes
- Async runtime improvements (Task.WhenAll overhead reduced)
- CoreCLR on WebAssembly (no mono shim)
- RISC-V and s390x architecture support
- MAUI: XAML source generation by default, CoreCLR for Android
- EF Core: Complex types with inheritance, simplified migrations
- Themes: Agentic UI, Distributed Reliability, Green Computing, Performance

---

## Interview Decisions Summary

### Plugin Architecture
- **Single plugin** with all skills organized by category
- **Grouped directories with auto-generated index skill** that routes agents to the right category
- **Context-aware loading**: Skills reference each other so the agent knows to pull in related ones
- **Router + specialists**: A lightweight index/advisor skill always loaded with full catalog, delegates to specialists

### Skill Granularity
- Context-aware loading where agents load what they need based on the task
- Skills cross-reference each other so agents discover related skills automatically

### Cross-Agent Compatibility
- **Build pipeline**: Canonical source in `skills/` generates Claude Code plugin, Copilot instructions, Codex AGENTS.md
- Leverage full feature sets of each agent (hooks, swarms, fleets, subagents)
- Agent Skills open standard (SKILL.md) as shared base format

### Epic Structure
- **15-20+ fine-grained epics** maximizing parallelism for swarm execution
- **Foundation + parallel**: One foundation epic (plugin structure, shared patterns) blocks everything, then all others parallelize
- **Ralph loop swarm** will handle dependency resolution and parallel development
- Each epic should be minimal in tasks, fleshed out during implementation via plan syncs

---

## Skill Categories & Coverage

### 1. Foundation & Plugin Infrastructure

**Skills:**
- `dotnet-version-detection` - Read TFMs, SDK versions, `global.json`, detect preview features. Instruct agent on current .NET landscape.
- `dotnet-project-analysis` - Understand solution structure, project references, Directory.Build.props, central package management
- `dotnet-advisor` - Router/index skill: always loaded, understands full catalog, delegates to specialist skills based on context
- `plugin-self-publish` - How THIS plugin is published and maintained (SemVer, changelog, CI/CD)

**Agents:**
- `dotnet-architect` - Analyzes project context, requirements, constraints; recommends approaches (UI framework, API style, architecture pattern)

### 2. Core C# & Language Patterns

**Skills:**
- `csharp-modern-patterns` - C# 14/15 features, pattern matching, records, primary constructors, collection expressions
- `csharp-coding-standards` - Modern .NET coding standards, naming conventions, file organization (reference: .NET API design guidelines)
- `csharp-async-patterns` - Async/await best practices, common agent mistakes (blocking on tasks, async void, missing ConfigureAwait)
- `csharp-nullable-reference-types` - NRT patterns, annotation strategies, migration guidance
- `csharp-dependency-injection` - MS DI advanced patterns: keyed services, decoration, factory patterns, scopes, hosted service registration
- `csharp-configuration` - Options pattern, user secrets, environment-based config, Microsoft.FeatureManagement for feature flags
- `csharp-source-generators` - Creating AND using source generators: IIncrementalGenerator, syntax/semantic analysis, emit patterns, testing, project-specific generators

**Agents:**
- `csharp-concurrency-specialist` - Deep expertise in Task/async patterns, thread safety, synchronization, race condition analysis

### 3. Project Structure & Scaffolding

**Skills:**
- `dotnet-project-structure` - Modern solution layout: .slnx, Directory.Build.props, central package management, editorconfig, analyzers
- `dotnet-scaffolding-base` - Base project scaffolding with all best practices applied
- `dotnet-add-analyzers` - Add/configure .NET analyzers, Roslyn analyzers, nullable, trimming warnings, AOT compat analyzers
- `dotnet-add-ci` - Add CI/CD to existing project (composable, detects platform)
- `dotnet-add-testing` - Add test infrastructure to existing project
- `dotnet-modernize` - Analyze existing code for modernization opportunities, suggest upgrades

### 4. Architecture Patterns

**Skills:**
- `dotnet-architecture-patterns` - Practical, modern patterns: minimal API organization, vertical slices, request pipeline, error handling, validation
- `dotnet-background-services` - BackgroundService, IHostedService, System.Threading.Channels for producer/consumer
- `dotnet-resilience` - Polly v8 + Microsoft.Extensions.Resilience + Microsoft.Extensions.Http.Resilience (the modern stack). NOT Microsoft.Extensions.Http.Polly (deprecated).
- `dotnet-http-client` - IHttpClientFactory + resilience pipelines: typed clients, named clients, DelegatingHandlers, testing
- `dotnet-observability` - OpenTelemetry (traces, metrics, logs), Serilog/MS.Extensions.Logging structured logging, health checks, custom metrics

### 5. Serialization & Communication

**Skills:**
- `dotnet-serialization` - AOT-friendly source-gen serialization: System.Text.Json source gen, Protobuf, MessagePack. Performance tradeoffs.
- `dotnet-grpc` - Full gRPC skill: service definition, code-gen, streaming, auth, load balancing, health checks
- `dotnet-realtime-communication` - Service communication patterns: SignalR, JSON-RPC 2.0, Server-Sent Events, gRPC streaming. When to use what.
- `dotnet-service-communication` - Higher-level skill that routes to gRPC, real-time, or REST based on requirements

### 6. API Development

**Skills:**
- `dotnet-minimal-apis` - Minimal APIs as the modern default: route groups, filters, validation, OpenAPI 3.1, organization patterns for scale
- `dotnet-api-versioning` - API versioning with Microsoft.AspNetCore.Mvc.Versioning, URL versioning preferred
- `dotnet-openapi` - OpenAPI/Swagger: Microsoft.AspNetCore.OpenApi, Swashbuckle, NSwag. Built-in .NET 10 first-class support.
- `dotnet-api-security` - Authentication/authorization: ASP.NET Core Identity, OAuth/OIDC, JWT, passkeys (WebAuthn), CORS, CSP

### 7. Security

**Skills:**
- `dotnet-security-owasp` - OWASP top 10 for .NET: injection prevention, XSS, CSRF, security headers, input validation
- `dotnet-secrets-management` - User secrets, environment variables, secure configuration patterns (cloud-agnostic)
- `dotnet-cryptography` - Modern .NET cryptography including post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA in .NET 10)

**Agents:**
- `dotnet-security-reviewer` - Analyzes code for security vulnerabilities, OWASP compliance

### 8. Testing

**Skills:**
- `dotnet-testing-strategy` - Core testing patterns: unit vs integration vs E2E, when to use what, test organization
- `dotnet-xunit` - Comprehensive xUnit: v3 features, theories, fixtures, parallelism, custom assertions, analyzers
- `dotnet-integration-testing` - WebApplicationFactory, Testcontainers, Aspire testing patterns
- `dotnet-ui-testing-core` - Core UI testing patterns applicable across frameworks
- `dotnet-blazor-testing` - bUnit for Blazor component testing
- `dotnet-maui-testing` - Appium, XHarness for MAUI testing
- `dotnet-uno-testing` - Playwright for Uno WASM, platform-specific testing
- `dotnet-playwright` - Playwright for .NET: browser automation, E2E testing, CI caching
- `dotnet-snapshot-testing` - Verify for snapshot testing: API surfaces, HTTP responses, rendered emails
- `dotnet-test-quality` - Code coverage (coverlet), CRAP analysis, mutation testing (Stryker.NET)

### 9. Performance & Benchmarking

**Skills:**
- `dotnet-benchmarkdotnet` - BenchmarkDotNet: setup, custom configs, memory diagnosers, exporters, baselines, CI integration
- `dotnet-performance-patterns` - Performance architecture: Span<T>, pooling, zero-alloc patterns, struct design, sealed classes
- `dotnet-profiling` - dotnet-counters, dotnet-trace, dotnet-dump, memory profiling, allocation analysis
- `dotnet-ci-benchmarking` - Continuous benchmarking in CI: benchmark comparison, regression detection, alerting

**Agents:**
- `dotnet-performance-analyst` - Analyzes profiling results, benchmark comparisons, identifies bottlenecks
- `dotnet-benchmark-designer` - Designs effective benchmarks, knows when BenchmarkDotNet vs custom benchmarks

### 10. Native AOT & Trimming

**Skills:**
- `dotnet-native-aot` - Full Native AOT pipeline: trimming, RD.xml, reflection-free patterns, p/invoke, COM interop, size optimization
- `dotnet-aot-architecture` - How to architect apps for AOT from the start: source gen over reflection, DI patterns, serialization choices
- `dotnet-trimming` - Making apps trim-safe: annotations, linker config, testing trimmed output, fixing warnings
- `dotnet-aot-wasm` - WebAssembly AOT compilation for Blazor WASM and Uno WASM targets

### 11. CLI Tool Development

**Skills:**
- `dotnet-system-commandline` - Full System.CommandLine: commands, options, arguments, middleware, hosting, tab completion, help generation
- `dotnet-cli-architecture` - CLI app architecture patterns (reference: clig.dev). Layered design so apps don't become "one big bash script". Separation of concerns, testability, composability.
- `dotnet-cli-aot-distribution` - Native AOT for CLI tools + cross-platform distribution pipeline
- `dotnet-cli-homebrew` - Homebrew formula authoring + CI/CD pipeline for macOS distribution
- `dotnet-cli-apt` - apt/dpkg packaging + CI/CD pipeline for Linux distribution
- `dotnet-cli-winget` - winget manifest authoring + CI/CD pipeline for Windows distribution
- `dotnet-cli-unified-pipeline` - Unified CI/CD pipeline producing artifacts for multiple package managers from single build

### 12. UI Frameworks

#### Blazor
**Skills:**
- `dotnet-blazor-patterns` - All hosting models: Server, WASM, Hybrid, Blazor Web App (auto/streaming). No bias toward one model.
- `dotnet-blazor-components` - Component architecture, state management, JS interop, forms, validation
- `dotnet-blazor-auth` - Blazor authentication/authorization across hosting models

#### Uno Platform
**Skills:**
- `dotnet-uno-platform` - Full Uno ecosystem: Extensions (Navigation, DI, Config, Serialization), MVUX, Toolkit, Theme resources
- `dotnet-uno-targets` - Deployment by target: Web/WASM, Mobile, Desktop, Embedded
- `dotnet-uno-mcp` - Leverage Uno MCP server for live doc lookups (detect if installed, work standalone too)

#### MAUI
**Skills:**
- `dotnet-maui-development` - MAUI development patterns. Honest assessment of current state (Feb 2026): production-ready with caveats (VS 2026 integration issues, iOS compatibility gaps, smaller ecosystem). 36% YoY user growth, strong enterprise traction.
- `dotnet-maui-aot` - MAUI Native AOT on iOS/Mac Catalyst: up to 50% size reduction, 50% startup improvement. Note: many libraries don't yet support AOT.

#### WinUI
**Skills:**
- `dotnet-winui` - WinUI 3 development patterns for Windows desktop

#### WPF
**Skills:**
- `dotnet-wpf-modern` - WPF on .NET Core: MVVM Toolkit, modern patterns, modernization
- `dotnet-wpf-migration` - WPF migration guidance: context-dependent (WinUI for Windows-only, Uno for cross-platform)

#### WinForms
**Skills:**
- `dotnet-winforms-basics` - WinForms on .NET Core basics + high-level migration tips (not in-depth migration)

#### Decision Support
**Skills:**
- `dotnet-ui-chooser` - Decision tree skill: analyzes requirements and recommends the right UI framework/hosting model. Works in planning mode to help agents solicit info from users.

**Agents:**
- `dotnet-uno-specialist` - Deep Uno Platform expertise
- `dotnet-maui-specialist` - Deep MAUI expertise including platform-specific issues
- `dotnet-blazor-specialist` - Deep Blazor expertise across all hosting models

### 13. Multi-Targeting & Polyfills

**Skills:**
- `dotnet-multi-targeting` - Multi-targeting strategies with polyfill emphasis: PolySharp, SimonCropp/Polyfill, conditional compilation, API compat analyzers
- `dotnet-version-upgrade` - Modern .NET version upgrades (.NET 8 -> 10 -> 11). Forward-looking polyfill usage for latest features on all targets.

### 14. Localization & Internationalization

**Skills:**
- `dotnet-localization` - Full i18n stack: .resx + modern alternatives (JSON resources, source generators), IStringLocalizer, date/number formatting, RTL, pluralization, UI framework integration. Research-based on current .NET community practices.

### 15. Packaging & Publishing

**Skills:**
- `dotnet-nuget-modern` - Modern NuGet essentials: central package management, source generators, SDK-style projects, SourceLink, CI publish
- `dotnet-msix` - Full MSIX skill: package creation, signing, distribution (Microsoft Store, sideloading, App Installer), CI/CD, auto-update
- `dotnet-github-releases` - Publishing to GitHub Releases with release notes generation

### 16. Release Management

**Skills:**
- `dotnet-release-management` - NBGV + changelogs + release notes + GitHub Releases + semantic versioning strategy. Comprehensive release lifecycle.

### 17. CI/CD

#### GitHub Actions
**Skills:**
- `dotnet-gha-patterns` - Composable GitHub Actions patterns: reusable workflows, composite actions, matrix builds for .NET
- `dotnet-gha-build-test` - .NET build + test workflow patterns
- `dotnet-gha-publish` - NuGet/container/artifact publishing workflows
- `dotnet-gha-deploy` - Deployment workflow patterns (GitHub Pages, container registries)

#### Azure DevOps
**Skills:**
- `dotnet-ado-patterns` - Composable ADO YAML pipeline patterns + ADO-unique features: Environments, Gates, Approvals
- `dotnet-ado-build-test` - .NET build + test pipeline patterns
- `dotnet-ado-publish` - Publishing pipeline patterns
- `dotnet-ado-unique` - ADO-specific capabilities: classic pipelines, release management, service connections, artifacts

### 18. Documentation

**Skills:**
- `dotnet-documentation-strategy` - Documentation tooling recommendation: Starlight (modern), Docusaurus (feature-rich), DocFX (legacy). Agent recommends based on project context. Mermaid preferred.
- `dotnet-mermaid-diagrams` - Dedicated Mermaid reference: architecture diagrams, sequence diagrams, class diagrams, deployment diagrams for .NET projects
- `dotnet-github-docs` - GitHub-native documentation: README structure, CONTRIBUTING.md, issue/PR templates, GitHub Pages setup
- `dotnet-xml-docs` - XML documentation comments: best practices, auto-generation, integration with doc tools
- `dotnet-api-docs` - API documentation generation: OpenAPI specs, doc site generation, keeping docs in sync with code

**Agents:**
- `dotnet-docs-generator` - Generates documentation with Mermaid diagrams for .NET projects

### 19. Agent Meta-Skills

**Skills:**
- `dotnet-agent-gotchas` - Common mistakes agents make with .NET: async/await errors, wrong NuGet packages, deprecated APIs, bad project structure, nullable handling, source gen config, trimming warnings, test organization, DI registration
- `dotnet-build-analysis` - Help agents understand build output, MSBuild errors, NuGet restore issues
- `dotnet-csproj-reading` - Teach agents to read/modify .csproj files, understand MSBuild properties, conditions
- `dotnet-solution-navigation` - Teach agents to navigate .NET solutions: find entry points, understand project dependencies, locate configuration

---

## Agents (Subagents)

### Framework Specialists
- `dotnet-uno-specialist` - Uno Platform deep expertise
- `dotnet-maui-specialist` - MAUI deep expertise + platform-specific issues
- `dotnet-blazor-specialist` - Blazor across all hosting models

### Task-Oriented Agents
- `dotnet-architect` - Architecture advisor, recommends approaches
- `dotnet-code-reviewer` - Reviews .NET code for quality, patterns, security
- `dotnet-migration-assistant` - Helps upgrade .NET versions
- `dotnet-docs-generator` - Documentation generation with diagrams
- `dotnet-project-scaffolder` - Creates new projects with best practices

### Cross-Cutting Specialists
- `dotnet-performance-analyst` - Performance profiling and analysis
- `dotnet-benchmark-designer` - Benchmark design expertise
- `dotnet-security-reviewer` - Security vulnerability analysis
- `dotnet-csharp-concurrency-specialist` - Threading, async, race conditions
- `dotnet-ci-troubleshooter` - CI/CD pipeline debugging

---

## Hooks

### Smart Default Hooks (configurable)

**PostToolUse (on .cs file edits):**
- Run `dotnet format` on modified file
- Check for analyzer warnings

**PostToolUse (on .csproj edits):**
- Run `dotnet restore`
- Validate package versions against central package management

**PostToolUse (on test file edits):**
- Suggest running related tests

**PostToolUse (on .xaml edits):**
- Validate XAML syntax if tooling available

**Event-specific smart filtering:**
- Only fire for relevant file types (.cs, .csproj, .xaml, .json)
- Different hooks for different file types
- Configurable aggressiveness via plugin settings

---

## MCP Server Integration

### Progressive approach: start with existing, add custom where needed

**Existing MCP Servers (configured via .mcp.json):**
- Uno Platform MCP - Live Uno documentation lookups
- Microsoft Learn MCP - .NET documentation access
- Context7 MCP - Library documentation lookup

**Future Custom MCP Servers (as needed):**
- .NET SDK Inspector - SDK version detection, TFM analysis
- NuGet Search - Package discovery and version recommendations
- Build Analyzer - Parse and explain MSBuild output

---

## Cross-Agent Support Matrix

### Claude Code (Primary)
- Full plugin format: skills, agents, hooks, MCP servers, LSP
- Subagent fleet capabilities
- Progressive skill loading via descriptions
- Plugin marketplace distribution

### GitHub Copilot
- Agent Skills (SKILL.md) - shared format, natively compatible
- `.github/copilot-instructions.md` - generated from canonical source
- Copilot Workspace multi-agent support
- Path-specific instructions via `applyTo` frontmatter

### OpenAI Codex
- AGENTS.md - generated from canonical source
- Hierarchical directory-based configuration
- Multi-agent worktree isolation support
- codex-1 / GPT-5.3-Codex model compatibility

### Build Pipeline
```
skills/ (canonical SKILL.md)
  |
  +-- dist/claude/     -> Claude Code plugin (plugin.json, agents/, hooks/)
  +-- dist/copilot/    -> .github/copilot-instructions.md + .github/skills/
  +-- dist/codex/      -> AGENTS.md hierarchy
```

---

## Epic Dependency Structure

### Wave 0: Foundation (blocks all others)
1. **Plugin infrastructure** - plugin.json, directory structure, build pipeline, cross-agent generation, index/router skill

### Wave 1: Core Skills (parallel after Wave 0)
2. **Core C# & Language** - Modern patterns, async, nullable, DI, configuration, source generators
3. **Project Structure & Scaffolding** - Solution layout, scaffolding, modernization
4. **Architecture Patterns** - Minimal APIs, background services, resilience, HTTP client, observability
5. **Serialization & Communication** - STJ, gRPC, real-time, service communication
6. **Testing Foundation** - Strategy, xUnit, integration testing, snapshot testing, quality
7. **Security** - OWASP, secrets, cryptography, API security
8. **Agent Meta-Skills** - Gotchas, build analysis, csproj reading, solution navigation
9. **Version Detection & Upgrade** - TFM detection, .NET 11 preview support, polyfills, multi-targeting

### Wave 2: Frameworks & Tools (parallel after relevant Wave 1 items)
10. **Blazor** - Patterns, components, auth, testing
11. **Uno Platform** - Full ecosystem, targets, MCP integration, testing
12. **MAUI** - Development, AOT, testing
13. **WinUI / WPF / WinForms** - Desktop frameworks, migration
14. **Native AOT & Trimming** - Full AOT pipeline, architecture, WASM AOT
15. **CLI Tool Development** - System.CommandLine, architecture, distribution (Homebrew, apt, winget)
16. **Performance & Benchmarking** - BenchmarkDotNet, profiling, CI benchmarking, performance patterns

### Wave 3: Integration & Polish (parallel after relevant Wave 2 items)
17. **CI/CD** - GitHub Actions + Azure DevOps (platform + scenario skills)
18. **Packaging & Publishing** - NuGet, MSIX, GitHub Releases, release management
19. **Documentation** - Strategy, Mermaid, GitHub docs, XML docs, API docs
20. **Localization** - Full i18n stack
21. **Hooks & MCP** - Plugin hooks, MCP server configs, custom MCP development
22. **Cross-Agent Compatibility** - Build pipeline, Copilot/Codex format generation, testing across agents

---

## Community Model

- **Open but curated**: Accept contributions with high quality bar
- **CONTRIBUTING.md**: Clear skill authoring guide
- **Automated validation**: CI pipeline validates skill format, frontmatter, references, markdown lint
- **Example projects**: Curated examples demonstrating skills in action
- **README**: Comprehensive with skill catalog, installation, usage examples, architecture diagrams (Mermaid), acknowledgements section pointing to external resources

---

## Research Findings Referenced

### Resilience Stack (Feb 2026)
- **Polly v8.6.5** is the definitive standard (no alternatives gaining traction)
- **Microsoft.Extensions.Resilience** and **Microsoft.Extensions.Http.Resilience** are the official approach
- **Microsoft.Extensions.Http.Polly** is DEPRECATED - do not use
- Standard HTTP resilience pipeline: Rate limiter -> Total timeout -> Retry -> Circuit breaker -> Attempt timeout
- Hedging strategy now first-class for distributed systems
- Chaos engineering support since Polly v8.3.0

### API Patterns (Feb 2026)
- **Minimal APIs** are Microsoft's official recommendation for new projects
- .NET 10 brings built-in validation, SSE, OpenAPI 3.1 to Minimal APIs
- **FastEndpoints** and **Carter** remain viable alternatives for more structure
- **Vertical slice architecture** is increasingly mainstream
- Swashbuckle deprecated in favor of built-in Microsoft.AspNetCore.OpenApi

### MAUI State (Feb 2026)
- Production-ready with significant caveats
- VS 2026 has serious Android toolchain bugs
- iOS 26.x compatibility gaps
- 36% YoY user growth, 557% increase in community PRs
- Native AOT on iOS: 50% size reduction, 50% startup improvement
- Uno Platform recommended for web/Linux deployment targets

### Documentation Tooling (Feb 2026)
- DocFX: community-maintained since Microsoft dropped official support (Nov 2022)
- Astro Starlight + MarkdownSnippets: modern choice for .NET docs
- Docusaurus: robust alternative with excellent Mermaid/OpenAPI support
- GitHub Pages + GitHub Actions: industry standard for OSS .NET projects
- All modern tools support Mermaid diagrams

### Coding Agent Platforms (Feb 2026)
- All three converging on Agent Skills open standard (SKILL.md format)
- AGENTS.md adopted by 60k+ open source projects
- Claude Code: most feature-rich plugin system (skills, agents, hooks, MCP, LSP)
- GitHub Copilot: Agent Skills + Copilot Extensions + multi-agent workspace
- OpenAI Codex: AGENTS.md hierarchy + multi-agent worktrees + GPT-5.3-Codex
