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
- **All skills must align with official Microsoft .NET design guidelines** (see spec for full reference table)
- **Key design guideline references**: Framework Design Guidelines, C# Coding Conventions, ASP.NET Core Best Practices, Microsoft REST API Guidelines, System.CommandLine Design Guidance, Library Design Guidance, Native AOT Deployment, Secure Coding Guidelines, David Fowler's Async Guidance
- **Enforcement**: Skills should recommend EditorConfig + .NET Code Analyzers (CAxxxx rules) + third-party analyzers (StyleCop, Roslynator) where applicable

## Planning-Stage Instructions

**CRITICAL:** When `/flow-next:plan` runs to break this into sub-epics and tasks, it MUST use the following plugin-dev skills to inform and validate the plan:

### Required Skills During Planning

1. **`/plugin-dev:plugin-structure`** - Use FIRST to validate the overall plugin architecture (plugin.json manifest, directory layout, skill/agent/hook/MCP organization). The plan must conform to Claude Code plugin conventions.

2. **`/plugin-dev:skill-development`** - Use when planning each skill to ensure:
   - SKILL.md frontmatter follows correct format (name, description, allowed-tools, context, agent, etc.)
   - Skill descriptions are optimized for auto-discovery triggering
   - Skills are organized for progressive disclosure (descriptions loaded first, full content on invoke)
   - Cross-references between skills are properly structured

3. **`/plugin-dev:agent-development`** - Use when planning each subagent to ensure:
   - Agent frontmatter is correct (name, description, tools, disallowedTools, model, permissionMode, maxTurns)
   - Agent descriptions accurately describe when delegation should happen
   - Skills can be preloaded into subagents where appropriate

4. **`/plugin-dev:hook-development`** - Use when planning the hooks system to ensure:
   - Hook matchers are correctly scoped (PreToolUse, PostToolUse, etc.)
   - Hook types (command, prompt, agent) are chosen appropriately
   - Hooks.json structure is valid

5. **`/plugin-dev:mcp-integration`** - Use when planning MCP server integration to ensure:
   - .mcp.json configuration follows correct format
   - ${CLAUDE_PLUGIN_ROOT} paths are used for bundled servers
   - MCP servers integrate cleanly with the plugin lifecycle

6. **`/plugin-dev:command-development`** - Use if any slash commands beyond skills are needed

7. **`/plugin-dev:plugin-settings`** - Use when planning configurable options (hook aggressiveness, MCP toggles, etc.)

### Planning Validation

After planning each sub-epic, use:
- **`/plugin-dev:skill-reviewer`** - Review skill descriptions for triggering effectiveness and quality
- **`/plugin-dev:plugin-validator`** - Validate the overall plugin structure as it's planned

### Implementation-Stage Skills

During implementation, use these additional skills:

**Plugin Development:** `/plugin-dev:create-plugin`, `/plugin-dev:agent-creator`
**Code Quality:** `/pr-review-toolkit:code-reviewer`, `/pr-review-toolkit:silent-failure-hunter`, `/pr-review-toolkit:code-simplifier`, `/pr-review-toolkit:comment-analyzer`, `/pr-review-toolkit:type-design-analyzer`, `/pr-review-toolkit:pr-test-analyzer`
**Documentation:** `/doc-coauthoring`, `/claude-md-management:claude-md-improver`, `/claude-md-management:revise-claude-md`
**Commit & PR:** `/commit-commands:commit`, `/commit-commands:commit-push-pr`
**QA Reference:** `/dotnet-skills:slopwatch` (LLM reward hacking detection), `/dotnet-skills:marketplace-publishing` (reference), `/dotnet-skills:skills-index-snippets` (index generation reference)

### Existing dotnet-skills Reference

Use [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) as reference material (not to copy directly). Key skills to reference: `csharp-coding-standards`, `csharp-type-design-performance`, `csharp-api-design`, `project-structure`, `serialization`, `snapshot-testing`, `playwright-blazor`, `testcontainers`, `crap-analysis`, `package-management`, `microsoft-extensions-dependency-injection`, `microsoft-extensions-configuration`.

### Planning Workflow

For each sub-epic being planned:
1. Reference `docs/dotnet-artisan-spec.md` for the authoritative requirements
2. Use the relevant plugin-dev skills above to validate the planned structure
3. Ensure cross-agent compatibility is addressed (build pipeline generates Copilot/Codex formats)
4. Skills should cross-reference related skills in their descriptions
5. Plan the router/advisor skill early (it needs to know the full catalog)
6. Reference the Microsoft .NET Design Guidelines reference table in the spec for authoritative standards
7. Use existing dotnet-skills reference material as starting points where applicable

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
