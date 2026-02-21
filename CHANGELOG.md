# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **GitHub Copilot CLI compatibility** -- Flat `skills/<skill-name>/` layout enables Copilot's one-level-deep skill scanning. All 131 SKILL.md files include `license: MIT` and unquoted descriptions for Copilot CLI compatibility.
- **32-skill routing strategy** -- Documented Copilot CLI display limit behavior and `dotnet-advisor` meta-routing strategy in CONTRIBUTING-SKILLS.md.

### Changed

- **Flat skill directory layout** -- Migrated from `skills/<category>/<skill-name>/` to `skills/<skill-name>/` to support cross-provider discovery (Claude Code, Copilot CLI, Codex).
- **Frontmatter migration** -- Removed quoted descriptions and added `license: MIT` across all 131 skills for Copilot CLI compatibility.
- **Similarity scoring** -- Removed same-category boost from similarity detection (no longer applicable with flat layout).
- **Updated documentation** -- AGENTS.md, CONTRIBUTING.md, CONTRIBUTING-SKILLS.md, README.md, and docs updated for flat layout, Copilot compatibility, and canonical skill count of 131.

## [0.2.0] - 2026-02-20

### Added

- **Invocation contract enforcement** -- Added MCP invocation-contract and routing-language compliance checks (including canonical IDs and compliance reporting), so invalid skill invocation definitions are caught before execution.
- **Routing quality tooling** -- Added routing language quality checks such as semantic overlap detection plus baseline and ownership audits to reduce ambiguous or conflicting guidance between skills.
- **Agent-routing CI validation** -- Added provider-matrix CI flows and agent skill-usage checks in the test runner to catch routing regressions with stronger regression guardrails.

### Changed

- **Routing execution and telemetry** -- Updated routing execution to use provider-matrix workflows with run-ID isolation, concurrency bounds, progress logging, and lifecycle telemetry for clearer, more reliable evaluations.
- **Routing schema and gating** -- Extended routing case schemas with optional, disallowed, and provider-alias fields and introduced tier-based evidence gating with ComputeTier, producing more predictable routing outcomes.

### Fixed

- **Routing decision consistency** -- Fixed path normalization, optional/disallowed token handling, provider aliasing, and merge behavior so routing candidates are evaluated consistently across runs.
- **Failure handling accuracy** -- Fixed CLI/transport failure detection and preserved script exit codes so diagnostics are reliable, with reduced noisy or misleading failure reporting.
- **Validation accuracy** -- Fixed validator and frontmatter parsing issues plus metadata/spec drift, ensuring reported thresholds and guidance stay aligned with actual runtime behavior.

### Changed

- **Standardized routing language** across all 130 skills and 14 agents for reliable skill discovery. Descriptions follow Action + Domain + Differentiator formula, all cross-references use `[skill:name]` syntax, and every skill has explicit Scope and Out-of-scope sections.
- **Added semantic similarity detection** to prevent description overlap between skills. CI gates on baseline regression with suppression list for known-acceptable pairs.
- **Tightened CI quality gates** -- agent bare-reference counts gated at zero, per-key baseline regression check, similarity baseline regression enabled.
- **Updated contributor documentation** -- CONTRIBUTING-SKILLS.md, CONTRIBUTING.md, and AGENTS.md updated with canonical routing-language conventions and similarity avoidance guidance.

## [0.1.1] - 2026-02-17

### Added

- **dotnet-file-io** skill (Core C#) -- FileStream async patterns, RandomAccess API, FileSystemWatcher debouncing, MemoryMappedFile, path traversal prevention, secure temp files, cross-platform considerations
- `.agents/openai.yaml` at repo root for Codex skill discovery
- **Version bump automation** -- `scripts/bump.sh` propagates version to plugin.json, marketplace.json (plugin entry + metadata), README badge, and CHANGELOG footer links
- **Root marketplace validation** -- `scripts/validate-root-marketplace.sh` as shared validation (used by both `validate-marketplace.sh` and CI workflows directly)
- **Plugin.json enrichment fields** -- `author`, `homepage`, `repository`, `license`, `keywords` validated by `validate-marketplace.sh`

### Changed

- **Marketplace restructure** -- Converted repo to flat marketplace layout with root `.claude-plugin/marketplace.json` discovery file listing dotnet-artisan as the available plugin (`"source": "./"`)
- **Removed dist pipeline** -- Deleted `scripts/generate_dist.py`, `scripts/validate_cross_agent.py`, and all `dist/` generation. Source files ARE the plugin; no build step needed
- **Per-plugin versioning** -- Release workflow now uses `dotnet-artisan/v*` tag format instead of `v*`
- **CI updated** -- `validate.yml` no longer runs dist generation or cross-agent conformance; added root marketplace.json validation and 3-way version consistency check. `release.yml` removed Pages deployment, now extracts release notes from CHANGELOG.md dynamically
- **Marketplace metadata** -- Root marketplace.json restructured to official Anthropic schema (`$schema`, `name`, `owner`, `metadata`, per-plugin `category`/`homepage`/`keywords`). Plugin.json enriched with `author`, `homepage`, `repository`, `license`, `keywords`
- **Validation deduplication** -- `validate-marketplace.sh` root marketplace section now delegates to `scripts/validate-root-marketplace.sh` instead of duplicating checks
- **Release documentation** -- CONTRIBUTING.md expanded with version management, bump script usage, tag convention (`dotnet-artisan/vX.Y.Z`), and release workflow documentation
- **Agent count corrected** -- README now lists all 14 specialist agents (was 9)
- **Description budget trimmed** from 13,481 to 11,948 chars (84 descriptions trimmed, removed filler words and redundant phrases) -- now below the 12,000-char WARN threshold
- Updated `--projected-skills` parameter in `validate-skills.sh` from 100 to 121 to match actual registered skill count
- Quality-checked 12 new skills from fn-30 through fn-36 for description formula compliance and cross-reference syntax

### Removed

- Root-level `plugin.json` (replaced by marketplace.json + per-plugin plugin.json)
- Cross-agent dist generation pipeline (`generate_dist.py`, `validate_cross_agent.py`) -- source files are the plugin, no transformation needed
- GitHub Pages deployment from release workflow
- Stale files: `docs/fleet-review-rubric.md`, `docs/review-reports/`, `scripts/ralph/runs/`, dist pipeline scripts
- Archived fleet review rubric and consolidated findings as historical snapshots (fn-29 audit, fn-37 cleanup, fn-40 resolution)

## [0.1.0] - 2026-02-14

### Added

- Plugin skeleton and infrastructure with `plugin.json`, `marketplace.json`, and validation scripts
- **Foundation skills** (4) -- Advisor routing, version detection, project analysis, self-publish
- **Core C# skills** (7) -- Modern patterns, coding standards, async/await, nullable reference types, dependency injection, configuration, source generators
- **Project structure skills** (6) -- Project structure, scaffolding, analyzers, CI setup, testing setup, modernization
- **Architecture skills** (10) -- Architecture patterns, background services, resilience, HTTP client, observability, EF Core patterns, EF Core architecture, data access strategy, containers, container deployment
- **Serialization and communication skills** (4) -- gRPC, real-time communication (SignalR/WebSockets), serialization, service communication
- **Testing skills** (10) -- Testing strategy, xUnit, integration testing, UI testing core, Blazor testing, MAUI testing, Uno testing, Playwright, snapshot testing, test quality
- **API development skills** (5) -- Minimal APIs, API versioning, OpenAPI, API security, input validation
- **Security skills** (3) -- OWASP compliance, secrets management, cryptography
- **UI framework skills** (13) -- Blazor patterns, Blazor components, Blazor auth, Uno Platform, Uno targets, Uno MCP, MAUI development, MAUI AOT, WinUI, WPF modern, WPF migration, WinForms basics, UI chooser
- **Native AOT skills** (4) -- Native AOT, AOT architecture, trimming, AOT WASM
- **CLI tools skills** (5) -- System.CommandLine, CLI architecture, CLI distribution, CLI packaging, CLI release pipeline
- **Agent meta-skills** (4) -- Agent gotchas, build analysis, csproj reading, solution navigation
- **Performance skills** (4) -- BenchmarkDotNet, performance patterns, profiling, CI benchmarking
- **CI/CD skills** (8) -- GitHub Actions patterns, build/test, publish, deploy; Azure DevOps patterns, build/test, publish, unique features
- **Packaging and publishing skills** (3) -- NuGet authoring, MSIX, GitHub Releases
- **Release management skill** (1) -- Release management
- **Documentation skills** (5) -- Documentation strategy, Mermaid diagrams, GitHub docs, XML docs, API docs
- **Localization skill** (1) -- Localization
- 9 specialist agents: dotnet-architect, concurrency specialist, security reviewer, Blazor specialist, Uno specialist, MAUI specialist, performance analyst, benchmark designer, docs generator
- Session hooks for start context and post-edit validation
- MCP server integrations for Context7, Uno Platform, and Microsoft Learn
- Cross-agent build pipeline generating dist outputs for Claude Code, GitHub Copilot, and OpenAI Codex
- Validation scripts for skills, marketplace, distribution generation, and cross-agent conformance
- README with skill catalog, Mermaid architecture diagrams, and cross-agent documentation
- CONTRIBUTING guide with skill authoring conventions and PR process

[unreleased]: https://github.com/novotnyllc/dotnet-artisan/compare/dotnet-artisan/v0.2.0...HEAD
[0.2.0]: https://github.com/novotnyllc/dotnet-artisan/compare/dotnet-artisan/v0.1.1...dotnet-artisan/v0.2.0
[0.1.1]: https://github.com/novotnyllc/dotnet-artisan/releases/tag/dotnet-artisan/v0.1.1
[0.1.0]: https://github.com/novotnyllc/dotnet-artisan/commits/main  <!-- no release tag for 0.1.0; links to main branch history -->
