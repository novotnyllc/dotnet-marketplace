# dotnet-artisan: Comprehensive .NET Coding Agent Skills Plugin

## Problem
Coding agents (Claude Code, GitHub Copilot, OpenAI Codex) lack comprehensive, opinionated, modern .NET development guidance. Existing skills (e.g., dotnet-skills) have significant gaps in UI frameworks, security, CI/CD, CLI tools, documentation, and cross-agent compatibility. Agents frequently make .NET-specific mistakes (async/await misuse, wrong packages, deprecated APIs, bad project structure).

## Key Decisions
- **Plugin name:** dotnet-artisan
- **Single plugin** with grouped skill directories and auto-generated router/index
- **Agent-first** audience, opinionated style
- **Active .NET version detection** from project files (TFM, global.json, Directory.Build.props)
- **Preview features** detected and used when project allows them
- **.NET 10 (C# 14)** as current stable, **.NET 11 Preview 1 (C# 15)** awareness
- **Polyfill-forward** using PolySharp and SimonCropp/Polyfill
- **AOT-friendly** source-gen over reflection throughout
- **No data layer** (separate plugin later) except serialization (STJ, Protobuf source gen)
- **No Akka** (too domain-specific)
- **Aspire awareness** but not deep coverage (point out when relevant)
- **Minimal APIs** as recommended API style for new projects
- **Polly v8 + Microsoft.Extensions.Resilience** as resilience stack (Http.Polly deprecated)
- **MS DI only** with advanced patterns (no third-party containers)
- **Built-in .NET patterns** for background work (BackgroundService + Channels, no Hangfire/Quartz)
- **Cross-agent build pipeline**: dotnet tool (inner loop) + GitHub Action (publishing)
- **Progressive MCP**: start with existing servers (Uno, MS Learn), add custom as needed
- **Smart hooks** with configurable defaults, file-type-specific firing
- **Open but curated** community model
- **Start fresh**, selectively reference dotnet-skills quality content

## Edge Cases
- Projects targeting multiple TFMs need consistent guidance across all targets
- Preview SDK installed alongside stable: skills must not break when both present
- WinForms/WPF projects on .NET Core may have hybrid old/new patterns
- MAUI has VS 2026 integration bugs that skills should warn about
- Some NuGet libraries don't support AOT yet - skills need fallback guidance
- Copilot and Codex have different capability levels for hooks/agents
- Projects without global.json need SDK detection from dotnet --version

## Open Questions
- Exact Mermaid diagram standards for architecture documentation
- Whether custom MCP servers are needed beyond existing ones
- Optimal skill description length for cross-agent auto-discovery
- How to handle Copilot Workspace vs Codex worktree parallelism differences

## Acceptance
- [ ] Plugin installs and works in Claude Code with all skills discoverable
- [ ] Agent can detect .NET version from project files and adapt guidance
- [ ] Cross-agent build generates valid Copilot instructions and Codex AGENTS.md
- [ ] All skills follow Agent Skills open standard (SKILL.md format)
- [ ] Hooks fire correctly for .cs, .csproj, .xaml file edits
- [ ] Router/advisor skill correctly identifies and loads relevant skills
- [ ] No deprecated .NET patterns suggested in any skill
- [ ] README includes comprehensive skill catalog with Mermaid architecture diagrams
- [ ] CI validates skill format, frontmatter, cross-references on every push
- [ ] Full spec document at docs/dotnet-artisan-spec.md is authoritative reference
