# dotnet-marketplace

This repository is a .NET development skills marketplace. It contains one plugin, **dotnet-artisan**, with 130 skills across 22 categories and 14 specialist agents.

For skill routing, quality gates, and agent delegation, see [plugins/dotnet-artisan/AGENTS.md](plugins/dotnet-artisan/AGENTS.md).

## Skill Locations

All skills follow the Agent Skills standard. Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (`name`, `description`).

**Path pattern:** `plugins/dotnet-artisan/skills/<category>/<skill-name>/SKILL.md`

### Categories

| Category | Path | Count |
|---|---|---|
| Foundation | `plugins/dotnet-artisan/skills/foundation/` | 4 |
| Core C# | `plugins/dotnet-artisan/skills/core-csharp/` | 18 |
| Project Structure | `plugins/dotnet-artisan/skills/project-structure/` | 7 |
| Architecture | `plugins/dotnet-artisan/skills/architecture/` | 15 |
| Serialization | `plugins/dotnet-artisan/skills/serialization/` | 4 |
| Testing | `plugins/dotnet-artisan/skills/testing/` | 10 |
| API Development | `plugins/dotnet-artisan/skills/api-development/` | 9 |
| Security | `plugins/dotnet-artisan/skills/security/` | 3 |
| Multi-Targeting | `plugins/dotnet-artisan/skills/multi-targeting/` | 2 |
| UI Frameworks | `plugins/dotnet-artisan/skills/ui-frameworks/` | 14 |
| Native AOT | `plugins/dotnet-artisan/skills/native-aot/` | 4 |
| CLI Tools | `plugins/dotnet-artisan/skills/cli-tools/` | 6 |
| TUI | `plugins/dotnet-artisan/skills/tui/` | 2 |
| Agent Meta-Skills | `plugins/dotnet-artisan/skills/agent-meta-skills/` | 5 |
| AI | `plugins/dotnet-artisan/skills/ai/` | 1 |
| Performance | `plugins/dotnet-artisan/skills/performance/` | 5 |
| CI/CD | `plugins/dotnet-artisan/skills/cicd/` | 8 |
| Packaging | `plugins/dotnet-artisan/skills/packaging/` | 3 |
| Release Management | `plugins/dotnet-artisan/skills/release-management/` | 1 |
| Documentation | `plugins/dotnet-artisan/skills/documentation/` | 5 |
| Localization | `plugins/dotnet-artisan/skills/localization/` | 1 |
| Build System | `plugins/dotnet-artisan/skills/build-system/` | 3 |

## Agents

14 specialist agents are defined in `plugins/dotnet-artisan/agents/`. The central router is `dotnet-architect`, which delegates to domain specialists (Blazor, MAUI, Uno, security, performance, testing, cloud, etc.).

## Plugin Manifest

The plugin manifest is at `plugins/dotnet-artisan/.claude-plugin/plugin.json`.

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
