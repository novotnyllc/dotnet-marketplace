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
7. **No deprecated patterns**: Skills must never suggest deprecated approaches (e.g., Microsoft.Extensions.Http.Polly, Swashbuckle for new projects)
8. **Context-aware loading**: Minimize context bloat by loading skills progressively based on actual task needs

---

## Agent Usage Flow

### Planning Mode (when in planning, flow-next plan/interview, or explicit plan mode)
1. Agent detects .NET project (reads .csproj, TFM, global.json, Directory.Build.props)
2. Advisor/router skill loads, understands full skill catalog
3. Advisor identifies relevant skills for the task at hand
4. Agent loads those skills + follows cross-references to related skills
5. Agent presents plan to user incorporating skill guidance
6. On approval, execution proceeds with skills already loaded

### Implementation Mode (when coding, fixing, implementing)
1. Agent is working on a task
2. As it encounters .NET patterns, skill descriptions auto-match via progressive disclosure
3. Relevant skills load progressively (no upfront context bloat)
4. Skills cross-reference each other: "if you're doing X, also load Y"
5. Hooks fire post-edit: format, validate, suggest tests
6. Agent follows skill guidance automatically without user intervention

### Key Behaviors
- Version detection runs first in both modes
- Skills adapt output based on detected TFM (net8.0 vs net10.0 vs net11.0)
- Preview features are used when project allows them (detected from LangVersion, TFM)
- Agents never suggest deprecated patterns
- Cross-agent routing: equivalent routing instructions generated for Copilot and Codex

---

## Migration from Existing dotnet-skills

**Approach:** Start fresh with our own structure and style. Selectively use high-quality content from [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) as a starting reference where applicable. No Akka content (too domain-specific). Acknowledge in README acknowledgements section.

**What to reference (selectively):**
- Performance patterns and benchmark design
- Testing patterns (Testcontainers, Playwright, snapshot testing)
- C# coding standards foundations
- Project structure conventions

**What to skip entirely:**
- Akka.NET content (5 skills, 1 agent) - too domain-specific
- Aspire-specific content - we'll maintain awareness but not deep coverage
- DocFX specialist agent - we'll cover modern doc tooling instead

**What to rewrite completely:**
- Serialization (needs AOT/source-gen focus)
- Package management (needs modern CPM focus)
- All architecture patterns (needs to be practical, not academic)

---

## Build Pipeline

### Inner Loop (dotnet tool)
- `dotnet tool` for local development that generates per-agent outputs
- Validates skill format, frontmatter, cross-references
- Generates dist/ outputs for testing locally

### Publishing (GitHub Action)
- Runs on push/release
- Generates dist/claude/, dist/copilot/, dist/codex/
- Publishes to Claude Code marketplace
- Creates GitHub Release with all artifacts

---

## Planning-Stage Requirements

When breaking this into sub-epics and tasks, the planning phase MUST use these plugin-dev skills to validate and inform the plan:

### Required Skills During Planning

1. **`/plugin-dev:plugin-structure`** - Use FIRST to validate overall plugin architecture (plugin.json, directory layout, skill/agent/hook/MCP organization)
2. **`/plugin-dev:skill-development`** - Use when planning each skill (SKILL.md frontmatter, description optimization for auto-discovery, progressive disclosure, cross-references)
3. **`/plugin-dev:agent-development`** - Use when planning each subagent (frontmatter, delegation triggers, preloaded skills)
4. **`/plugin-dev:hook-development`** - Use when planning hooks system (matchers, types, hooks.json structure)
5. **`/plugin-dev:mcp-integration`** - Use when planning MCP server integration (.mcp.json, ${CLAUDE_PLUGIN_ROOT} paths)
6. **`/plugin-dev:command-development`** - Use if any slash commands beyond skills are needed
7. **`/plugin-dev:plugin-settings`** - Use when planning configurable options (hook aggressiveness, MCP toggles)

### Planning Validation

After planning each sub-epic, use:
- **`/plugin-dev:skill-reviewer`** - Review skill descriptions for triggering effectiveness and quality
- **`/plugin-dev:plugin-validator`** - Validate the overall plugin structure as planned

### Implementation-Stage Skills

During implementation of each sub-epic/task, use these additional skills:

**Plugin Development:**
- **`/plugin-dev:create-plugin`** - End-to-end plugin creation workflow with validation
- **`/plugin-dev:agent-creator`** - Generate agent configurations

**Code Quality (use proactively after writing code):**
- **`/pr-review-toolkit:code-reviewer`** - Review code for adherence to project guidelines
- **`/pr-review-toolkit:silent-failure-hunter`** - Detect silent failures and inadequate error handling
- **`/pr-review-toolkit:code-simplifier`** - Simplify code for clarity and maintainability
- **`/pr-review-toolkit:comment-analyzer`** - Verify comment accuracy and completeness
- **`/pr-review-toolkit:type-design-analyzer`** - Analyze type design for encapsulation and invariants
- **`/pr-review-toolkit:pr-test-analyzer`** - Review test coverage quality

**Documentation & Project:**
- **`/doc-coauthoring`** - Structured documentation co-authoring workflow (for README, CONTRIBUTING, etc.)
- **`/claude-md-management:claude-md-improver`** - Audit and improve CLAUDE.md files
- **`/claude-md-management:revise-claude-md`** - Update CLAUDE.md with session learnings

**Commit & PR:**
- **`/commit-commands:commit`** - Create git commits
- **`/commit-commands:commit-push-pr`** - Commit, push, and open PRs

**Quality Assurance (from dotnet-skills, use as reference):**
- **`/dotnet-skills:slopwatch`** - Detect LLM reward hacking (disabled tests, suppressed warnings, empty catch blocks)
- **`/dotnet-skills:marketplace-publishing`** - Reference for marketplace publishing workflow
- **`/dotnet-skills:skills-index-snippets`** - Reference for AGENTS.md/CLAUDE.md index generation

### Existing dotnet-skills Reference Material

The existing [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) plugin provides useful reference material. Key skills to reference (not copy directly):

| dotnet-skills Skill | Use As Reference For |
|---------------------|---------------------|
| `csharp-coding-standards` | Foundation for our modernized coding standards skill |
| `csharp-type-design-performance` | Performance-oriented type design patterns |
| `csharp-api-design` | Extend-only API design principles |
| `project-structure` | .slnx, Directory.Build.props patterns |
| `serialization` | Schema-based serialization approach (we'll expand for AOT) |
| `snapshot-testing` | Verify-based snapshot patterns |
| `playwright-blazor` | Blazor-specific Playwright patterns |
| `testcontainers` | Integration test infrastructure patterns |
| `crap-analysis` | Code coverage and risk analysis |
| `package-management` | Central Package Management patterns |
| `microsoft-extensions-dependency-injection` | DI registration patterns |
| `microsoft-extensions-configuration` | Options pattern foundations |

### Planning Workflow Per Sub-Epic

1. Reference this spec (`docs/dotnet-artisan-spec.md`) for authoritative requirements
2. Use relevant plugin-dev skills above to validate planned structure
3. Ensure cross-agent compatibility is addressed (build pipeline generates Copilot/Codex formats)
4. Skills should cross-reference related skills in their descriptions
5. Plan the router/advisor skill early (it needs to know the full catalog)
6. Reference the Microsoft .NET Design Guidelines table (above) for authoritative standards each skill must follow
7. Use existing dotnet-skills reference material (above) as starting points where applicable

---

## Microsoft .NET Design Guidelines Reference

All skills MUST align with official Microsoft .NET design guidelines. These are the authoritative references that skills should follow and cite:

### Core Guidelines

| Guideline | URL | Status |
|-----------|-----|--------|
| **Framework Design Guidelines** | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/ | Based on 2nd Ed; 3rd Ed book exists but Learn not fully updated. Foundational principles still current. |
| **C# Coding Conventions** | https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions | Actively maintained, current for 2026. PascalCase, camelCase, `_field`, `s_static`. |
| **Naming Guidelines** | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/naming-guidelines | Core naming rules: PascalCase types, I-prefix interfaces, verb phrases for methods. |
| **Identifier Names (C#)** | https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names | C#-specific naming rules and analyzer-enforceable conventions. |

### API & Architecture

| Guideline | URL | Status |
|-----------|-----|--------|
| **ASP.NET Core Best Practices** | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0 | Updated for .NET 10. Async-first, HybridCache, no blocking. |
| **Microsoft REST API Guidelines** | https://github.com/microsoft/api-guidelines | General guidelines deprecated in favor of Azure-specific. Active vNext branch. |
| **Azure REST API Guidelines** | https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md | Azure service teams' current reference. |
| **Minimal APIs Route Handlers** | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/route-handlers?view=aspnetcore-10.0 | Route groups, filters, organization patterns for scale. |
| **OpenAPI in ASP.NET Core** | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/openapi/overview?view=aspnetcore-10.0 | Built-in .NET 9+. `WithOpenApi()` deprecated in .NET 10; use transformers. |
| **System.CommandLine Design** | https://learn.microsoft.com/en-us/dotnet/standard/commandline/design-guidance | CLI design like REST design. Naming, verbs/nouns, verbosity, POSIX. |
| **Library Design Guidance** | https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/ | NuGet authoring, SemVer, Source Link, cross-platform, stability. |

### Quality & Analysis

| Guideline | URL | Status |
|-----------|-----|--------|
| **Code Analysis Overview** | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview | Built on Roslyn; enabled by default .NET 5+. |
| **Code Quality Rules (CAxxxx)** | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ | Categories: Design, Globalization, Performance, Security, Usage. |
| **Code-Style Naming Rules** | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/naming-rules | EditorConfig-enforceable naming conventions. |
| **NuGet Package Authoring** | https://learn.microsoft.com/en-us/nuget/create-packages/package-authoring-best-practices | Package ID, SemVer, metadata, Source Link, README. |

### Security

| Guideline | URL | Status |
|-----------|-----|--------|
| **Security in .NET** | https://learn.microsoft.com/en-us/dotnet/standard/security/ | Core security guidance. |
| **Secure Coding Guidelines** | https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines | Avoid CAS, APTCA, .NET Remoting, DCOM, binary formatters. |
| **ASP.NET Core Security** | https://learn.microsoft.com/en-us/aspnet/core/security/?view=aspnetcore-10.0 | Updated for .NET 10. Secret Manager, managed identities. |

### Performance & AOT

| Guideline | URL | Status |
|-----------|-----|--------|
| **Native AOT Deployment** | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/ | net8.0+. No dynamic assembly loading, restricted reflection. |
| **Prepare Libraries for Trimming** | https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming | IsTrimmable, annotations, linker config. |
| **ASP.NET Core Native AOT** | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot?view=aspnetcore-10.0 | Updated for .NET 10 with major AOT improvements. |
| **AOT Warnings** | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/fixing-warnings | Static analysis via build-time warnings. |
| **Optimizing AOT** | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/optimizing | Size optimization, trimming strategies. |

### Async & Threading

| Guideline | URL | Status |
|-----------|-----|--------|
| **David Fowler's Async Guidance** | https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md | Community standard. Prefer async Task, avoid .Wait()/.Result. |
| **Async/Await Best Practices (MSDN)** | https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming | Foundation article (Stephen Cleary). Still highly relevant. |

### Documentation & Source Gen

| Guideline | URL | Status |
|-----------|-----|--------|
| **XML Documentation Tags** | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags | `///` comments, `<summary>`, `<param>`, `cref`. |
| **Source Generators Overview** | https://learn.microsoft.com/en-sg/dotnet/csharp/roslyn-sdk/source-generators-overview | IIncrementalGenerator recommended over ISourceGenerator. |
| **Incremental Generators Cookbook** | https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md | Performance patterns, value type data models, equatability. |
| **Logging Source Gen** | https://learn.microsoft.com/en-us/dotnet/core/extensions/logger-message-generator | Compile-time logging for high-performance structured logging. |
| **Regex Source Generators** | https://learn.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-source-generators | AOT-friendly regex compilation. |

### Enforcement

Most guidelines can be enforced via:
- **EditorConfig** files (`.editorconfig`)
- **.NET Code Analyzers** (`Microsoft.CodeAnalysis.NetAnalyzers 10.0.100`)
- **StyleCop.Analyzers**, **Roslynator**, **SonarAnalyzer** (third-party)
- **Visual Studio / VS Code** integration

Skills should reference these guidelines where applicable and recommend the appropriate analyzers/enforcement mechanisms.

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

#### Runtime
- **Runtime Async** - Async/await moves from compiler state machines to runtime-level execution. Enabled by default in CoreCLR. Produces simpler IL, fully compatible with existing compiler-async code. 23% regression under high load when mixing with non-runtime-async framework libraries (expected to resolve as framework recompiles). Requires `<EnablePreviewFeatures>true</EnablePreviewFeatures>` + `<Features>$(Features);runtime-async=on</Features>` at project level. Native AOT compatible.
- **CoreCLR on WebAssembly** - Foundational work (not ready for general use). WASM-targeting RyuJIT for AOT compilation, browser-host threading/timers/interop. AOT performance within 20% of desktop CoreCLR+JIT. Blazor WASM can now choose between Mono (still default) and CoreCLR. Console apps loading in under a second.
- **CoreCLR for Android** - Now the **default runtime** for Android Release builds in MAUI, replacing Mono. Shorter startup times, better ecosystem compatibility, slightly larger app size. Opt out with `<UseMonoRuntime>true</UseMonoRuntime>`.
- **GC heap hard limit for 32-bit** - `GCHeapHardLimit` now works on 32-bit (previously 64-bit only). Max 1GB heap on 32-bit. Not enabled in 32-bit containers.
- RISC-V and s390x architecture enablement
- CoreCLR interpreter expansion

#### C# 15 Preview
- **Collection expression arguments** - `with()` syntax as first element in collection expressions for constructor parameters:
  ```csharp
  List<int> nums = [with(capacity: 32), 0, ..evens, ..odds];
  HashSet<string> names = [with(comparer: StringComparer.OrdinalIgnoreCase), "Alice", "Bob"];
  Dictionary<string, int> lookup = [with(StringComparer.Ordinal), "one":1, "two":2];
  ```
  Enables capacity pre-allocation, custom comparers, and any constructor parameter. Syntax is "strawman" and may change.

#### Libraries
- **Zstandard compression** - New `System.IO.Compression.Zstandard` assembly with `ZstandardStream`, `ZstandardEncoder`, `ZstandardDecoder`. 2-7x faster compression and 2-14x faster decompression than Brotli/Deflate with comparable ratios. Supports streaming, one-shot, dictionary-based compression, quality levels, checksum. HTTP `AutomaticDecompression` supports `DecompressionMethods.Zstandard`.
- **BFloat16 type** - `System.Numerics.BFloat16` for AI/ML workloads. 8 exponent bits (same range as float) + 7 significand bits (reduced precision). ~2x throughput on supported hardware. Full numeric interfaces (`INumber<BFloat16>`, `IFloatingPoint<BFloat16>`). Vector support (Vector64/128/256/512). BinaryPrimitives read/write support.
- **Happy Eyeballs** (RFC 8305) in `Socket.ConnectAsync` - Parallel IPv4/IPv6 DNS resolution and alternating connection attempts. `Socket.ConnectAsync(SocketType.Stream, ProtocolType.Tcp, e, ConnectAlgorithm.Parallel)`. Faster dual-stack connections with automatic fallback.
- FrozenDictionary supports collection expressions
- Rune support expanded across String, StringBuilder, TextWriter
- MediaTypeMap for MIME type lookups
- HMAC and KMAC verification APIs
- Hard link creation APIs
- DivisionRounding enum

#### ASP.NET Core & Blazor
- `EnvironmentBoundary` component for conditional rendering
- `Label` and `DisplayName` components for forms/accessibility
- QuickGrid `OnRowClick` event
- `RelativeToCurrentUri` for relative navigation
- SignalR `ConfigureConnection` for interactive server components
- `IHostedService` support in Blazor WebAssembly
- OpenAPI schema support for binary file responses
- `IOutputCachePolicyProvider` for output caching customization
- Auto-trust development certificates in WSL

#### MAUI
- **XAML source generation enabled by default** - Replaces XAMLC. Compile-time XAML-to-C# generation, AOT-friendly, eliminates runtime reflection for XAML parsing. Consistent debug/release behavior. Revert with `<MauiXamlInflator>XamlC</MauiXamlInflator>`.
- `dotnet run` interactive target framework and device selection

#### EF Core
- **Complex types and JSON columns on TPT/TPC inheritance** - Previously limited to TPH only. Now works with Table-Per-Type and Table-Per-Concrete-Type strategies.
- Create and apply migrations in single step
- Azure Cosmos DB: transactional batches, bulk execution, session token management

#### SDK & Tooling
- `dotnet run` interactive target framework/device selection
- `dotnet test` positional arguments
- `dotnet watch` hot reload for reference changes with configurable ports
- New code analyzers, terminal logger improvements

#### .NET 11 Themes
- Agentic UI, Distributed Reliability, Green Computing, Performance

### Skill Implications from .NET 11 Preview 1

Skills must be aware of these .NET 11 changes and adapt guidance when `net11.0` TFM is detected:

| Skill Area | .NET 11 Impact |
|-----------|---------------|
| **Version Detection** | Detect `net11.0` TFM, `<LangVersion>preview</LangVersion>`, runtime-async feature flags |
| **WASM/AOT** | CoreCLR vs Mono runtime selection for WebAssembly; WASM AOT via RyuJIT |
| **MAUI** | XAML source gen default, CoreCLR for Android default, `dotnet run` device selection |
| **Modern C#** | Collection expression `with()` arguments for capacity/comparers |
| **Serialization** | BFloat16 serialization for AI/ML data pipelines |
| **Performance** | Zstandard compression (prefer over Brotli/Deflate for speed), runtime-async implications |
| **Networking** | Happy Eyeballs `ConnectAlgorithm.Parallel` for dual-stack apps |
| **EF Core** | Complex types + JSON columns with TPT/TPC (no longer TPH-only) |
| **Architecture** | Runtime-async changes profiling/debugging strategies; CoreCLR unification across platforms |
| **Security** | HMAC/KMAC verification APIs for cryptographic operations |

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
- **24 sub-epics (fn-2 through fn-25)** maximizing parallelism for swarm execution
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
- [skill:dotnet-csharp-code-smells] - Proactive code smell and anti-pattern detection: IDisposable misuse, warning suppression hacks, LINQ anti-patterns, event handling leaks, design smells

**Agents:**
- `csharp-concurrency-specialist` - Deep expertise in Task/async patterns, thread safety, synchronization, race condition analysis

### 3. Project Structure & Scaffolding

**Skills:**
- `dotnet-project-structure` - Modern solution layout: .slnx, Directory.Build.props, central package management, editorconfig, analyzers
- `dotnet-scaffold-project` - Base project scaffolding with all best practices applied
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

### 4b. Data Access & Persistence

**Skills:**
- `dotnet-efcore-patterns` - EF Core best practices: DbContext lifecycle, change tracking (AsNoTracking by default), query splitting, migrations, dedicated migration DbContext, interceptors
- `dotnet-efcore-architecture` - EF Core architecture patterns: separate read/write models, repository vs direct DbContext, avoiding N+1, row limits, application-side sorting/filtering anti-patterns
- `dotnet-data-access-strategy` - Choosing the right data access approach: EF Core vs Dapper vs raw ADO.NET. When to use each, performance tradeoffs, AOT compatibility

### 4c. Containers & Cloud Deployment

**Skills:**
- `dotnet-containers` - Container best practices for .NET: multi-stage Dockerfiles, `dotnet publish` container images (.NET 8+ built-in), rootless containers, health checks, signal handling
- `dotnet-container-deployment` - Deploying .NET containers: Kubernetes basics (manifests, probes, resource limits), Docker Compose for local dev, container registries, CI/CD integration

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
| Epic | Title | Depends On |
|------|-------|------------|
| fn-2 | Plugin Skeleton & Infrastructure | — |

### Wave 1: Core Skills (parallel after fn-2)
| Epic | Title | Depends On |
|------|-------|------------|
| fn-3 | Core C# & Language Patterns | fn-2 |
| fn-4 | Project Structure & Scaffolding | fn-2 |
| fn-5 | Architecture Patterns (incl. Data Access, Containers) | fn-2 |
| fn-6 | Serialization & Communication | fn-2 |
| fn-7 | Testing Foundation | fn-2 |
| fn-8 | Security Skills | fn-2 |
| fn-9 | Agent Meta-Skills | fn-2 |
| fn-10 | Version Detection & Multi-Targeting | fn-2 |
| fn-11 | API Development | fn-2 |
| fn-23 | Hooks & MCP Integration | fn-2 |

### Wave 2: Frameworks & Tools (parallel after relevant Wave 1 items)
| Epic | Title | Depends On |
|------|-------|------------|
| fn-12 | Blazor Skills | fn-3, fn-7 |
| fn-13 | Uno Platform Skills | fn-3, fn-7 |
| fn-14 | MAUI Skills | fn-3, fn-7 |
| fn-15 | Desktop Frameworks (WinUI/WPF/WinForms) | fn-3 |
| fn-16 | Native AOT & Trimming | fn-5 |
| fn-17 | CLI Tool Development | fn-5 |
| fn-18 | Performance & Benchmarking | fn-5 |
| fn-22 | Localization | fn-3 |

### Wave 3: Integration & Polish (parallel after Wave 2)
| Epic | Title | Depends On |
|------|-------|------------|
| fn-19 | CI/CD (GitHub Actions + Azure DevOps) | fn-11, fn-16, fn-17, fn-18 |
| fn-20 | Packaging & Publishing | fn-19 |
| fn-21 | Documentation Skills | fn-19 |
| fn-24 | Cross-Agent Build Pipeline | fn-19, fn-23 |
| fn-25 | Community Setup (README, CONTRIBUTING) | fn-20, fn-21, fn-24 |

---

## Community Model

- **Open but curated**: Accept contributions with high quality bar
- **CONTRIBUTING.md**: Clear skill authoring guide
- **Automated validation**: CI pipeline validates skill format, frontmatter, references, markdown lint
- **Example projects**: Curated examples demonstrating skills in action
- **README**: Comprehensive with skill catalog, installation, usage examples, architecture diagrams (Mermaid), acknowledgements section pointing to external resources

---

## Fact Provenance Policy

Technical claims in this spec and in generated skills must include:
- **Source URL** linking to the authoritative documentation or announcement
- **Last verified date** (YYYY-MM-DD format)
- Claims about deprecated/removed APIs must cite the official deprecation notice or migration guide
- Preview-era feature details (.NET 11 Preview) are marked as volatile and must be re-verified before each release

Skills should use a `<!-- Last verified: YYYY-MM-DD -->` comment in their SKILL.md body for claims that may change.

## Research Findings Referenced

### Resilience Stack (Last verified: 2026-02-11)
- **Polly v8.6.5** is the definitive standard (no alternatives gaining traction)
- **Microsoft.Extensions.Resilience** and **Microsoft.Extensions.Http.Resilience** are the official approach
- **Microsoft.Extensions.Http.Polly** is superseded by Microsoft.Extensions.Http.Resilience ([migration guide](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/resilience/migration-guide)) — do not use for new projects
- Standard HTTP resilience pipeline: Rate limiter -> Total timeout -> Retry -> Circuit breaker -> Attempt timeout
- Hedging strategy now first-class for distributed systems
- Chaos engineering support since Polly v8.3.0

### API Patterns (Last verified: 2026-02-11)
- **Minimal APIs** are Microsoft's official recommendation for new projects
- .NET 10 brings built-in validation, SSE, OpenAPI 3.1 to Minimal APIs
- **FastEndpoints** and **Carter** remain viable alternatives for more structure
- **Vertical slice architecture** is increasingly mainstream
- Swashbuckle: no longer actively maintained; Microsoft.AspNetCore.OpenApi is the built-in replacement for .NET 9+ projects. Existing Swashbuckle-based projects can continue using it but should plan migration.

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
