# MSBuild and Build System Skills

## Overview
Create a new `build-system` skill category covering MSBuild project system authoring, custom task development, and build optimization/diagnostics. Fills the gap between `dotnet-project-structure` (solution layout and shared config) and `dotnet-build-analysis` (interpreting build output) — this epic covers **authoring** and **optimizing** the build system itself.

## Scope
**Skills (3 total, new category `skills/build-system/`):**
- `dotnet-msbuild-authoring` — Custom targets (BeforeTargets/AfterTargets/DependsOnTargets), Inputs/Outputs for incrementality, props/targets import ordering, items and item metadata (Include/Exclude/Update/Remove), conditions, property functions, well-known metadata, Directory.Build.props/targets advanced patterns (import chain, condition guards, double-import prevention)
- `dotnet-msbuild-tasks` — ITask and ToolTask base classes, IIncrementalTask (MSBuild 17.8+, `Microsoft.Build.Framework.IIncrementalTask`), inline tasks (CodeTaskFactory), UsingTask registration, task parameters ([Required], [Output], ITaskItem), task debugging (MSBUILDDEBUGONSTART), task NuGet packaging (buildTransitive/build folders)
- `dotnet-build-optimization` — Incremental build diagnostics (warning → `/bl` binary log → MSBuild Structured Log Viewer → root cause → fix), common incremental failures (missing Inputs/Outputs, file copy timestamps, generators writing mid-build), binary log analysis (`dotnet build /bl`, `-pp` preprocessed project), parallel builds (`/m`, `/graph` mode, `BuildInParallel`), build caching and restore optimization

## Scope Boundaries

| Concern | fn-34 owns (build system authoring) | Other skill owns | Enforcement |
|---|---|---|---|
| Directory.Build.props/targets basics | N/A — cross-references `[skill:dotnet-project-structure]` | `dotnet-project-structure`: solution layout, basic shared props, nested import pattern | fn-34 skills state "basic layout → [skill:dotnet-project-structure]"; grep validates |
| Directory.Build.props/targets advanced | Import ordering rules, condition guards, double-import prevention, custom targets in .targets files | N/A | Content in `dotnet-msbuild-authoring` only |
| MSBuild error interpretation | N/A — cross-references `[skill:dotnet-build-analysis]` | `dotnet-build-analysis`: error code prefixes (CS/MSB/NU/IDE/CA), NuGet restore failures, CI drift | fn-34 skills state "interpreting errors → [skill:dotnet-build-analysis]"; grep validates |
| NoWarn/TreatWarningsAsErrors | Build-level configuration strategy (when to use, how to set per-project vs per-solution) | `dotnet-build-analysis`: Slopwatch anti-patterns (detecting inappropriate suppression) | fn-34 covers "how to configure"; build-analysis covers "how to detect misuse" |
| Build caching/restore | SDK artifact caching, `/p:RestorePackagesWithLockFile`, build output caching | `dotnet-project-structure`: lock files, CPM, nuget.config | fn-34 covers build-time optimization; project-structure covers restore-time configuration |

## Dependencies
- **Hard:** None (new category, no prerequisite epics)
- **Soft:** fn-4 (project-structure) and fn-9 (agent-meta-skills) should be complete for cross-reference targets to exist — both are complete

## .NET Version Policy
- MSBuild SDK version: reference latest stable (.NET 10 SDK era patterns)
- IIncrementalTask: requires MSBuild 17.8+ (VS 2022 17.8+, .NET 8 SDK)
- Version-gate any API that requires a specific MSBuild/SDK version with explicit callouts

## Cross-Reference Classification
- **Hard cross-refs** (must exist, validated by grep):
  - `[skill:dotnet-project-structure]` — solution layout, Directory.Build.props basics
  - `[skill:dotnet-build-analysis]` — MSBuild error interpretation, CI drift diagnosis
- **Soft cross-refs** (internal to this epic, validated with `--allow-planned-refs`):
  - `[skill:dotnet-msbuild-authoring]` — referenced by tasks .2 and .3
  - `[skill:dotnet-msbuild-tasks]` — referenced by task .3

## Task Decomposition

### fn-34.1: MSBuild authoring skill (parallelizable with .2 and .3)
**Delivers:** `dotnet-msbuild-authoring`
- `skills/build-system/dotnet-msbuild-authoring/SKILL.md`
- Covers: custom targets, import ordering, items/metadata, conditions, property functions, Directory.Build advanced patterns
- Cross-refs `[skill:dotnet-project-structure]` for basic layout
- Does NOT touch `plugin.json` (handled by fn-34.3)

### fn-34.2: MSBuild custom tasks skill (parallelizable with .1 and .3)
**Delivers:** `dotnet-msbuild-tasks`
- `skills/build-system/dotnet-msbuild-tasks/SKILL.md`
- Covers: ITask, IIncrementalTask (MSBuild 17.8+), inline tasks, UsingTask, task packaging, debugging
- Cross-refs `[skill:dotnet-msbuild-authoring]` (soft — same epic)
- Does NOT touch `plugin.json` (handled by fn-34.3)

### fn-34.3: Build optimization skill + integration (depends on .1 and .2)
**Delivers:** `dotnet-build-optimization` + plugin registration for all 3 skills
- `skills/build-system/dotnet-build-optimization/SKILL.md`
- `.claude-plugin/plugin.json` — **sole owner**: registers all 3 skill paths
- Cross-refs `[skill:dotnet-msbuild-authoring]` and `[skill:dotnet-msbuild-tasks]` (soft — same epic)
- Cross-refs `[skill:dotnet-build-analysis]` for error interpretation (hard)
- Runs all four validation commands
- Updates README.md skill catalog (category count: 20, skill count: 104) and CLAUDE.md counts

## Conventions
- All skills use `dotnet-` prefix with noun style
- SKILL.md frontmatter: `name` and `description` only
- Cross-references use `[skill:name]` syntax throughout
- Each skill includes: Overview, Prerequisites, content sections with `##` headers, Agent Gotchas, References
- Description budget: 3 skills × ~120 chars = ~360 chars additional

## Quick commands
```bash
./scripts/validate-skills.sh && \
./scripts/validate-marketplace.sh && \
python3 scripts/generate_dist.py --strict && \
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] `dotnet-msbuild-authoring` skill covering custom targets (BeforeTargets/AfterTargets/DependsOnTargets), Inputs/Outputs, import ordering
- [ ] Items and item metadata (Include/Exclude/Update/Remove, well-known metadata) documented
- [ ] Conditions and property functions documented
- [ ] Directory.Build.props/targets advanced patterns (import chain, condition guards, double-import prevention)
- [ ] `dotnet-msbuild-tasks` skill covering ITask, ToolTask, IIncrementalTask (MSBuild 17.8+)
- [ ] Inline tasks (CodeTaskFactory) and UsingTask registration documented
- [ ] Task parameters ([Required], [Output], ITaskItem) and debugging (MSBUILDDEBUGONSTART) covered
- [ ] Task NuGet packaging (buildTransitive/build folders) documented
- [ ] `dotnet-build-optimization` skill covering incremental build diagnosis workflow (warning → `/bl` → root cause → fix)
- [ ] Binary log analysis (`dotnet build /bl`, MSBuild Structured Log Viewer) documented
- [ ] Parallel builds (`/m`, `/graph`, BuildInParallel) documented
- [ ] Common incremental build failure patterns listed with fixes
- [ ] Scope boundary enforced: basic Directory.Build → `[skill:dotnet-project-structure]`, error interpretation → `[skill:dotnet-build-analysis]`
- [ ] Each skill has Agent Gotchas section with MSBuild-specific pitfalls
- [ ] Each skill has References section with official Microsoft Learn links
- [ ] All cross-references use `[skill:name]` syntax (grep validated)
- [ ] All 3 skills registered in `plugin.json` (by task .3)
- [ ] README.md and CLAUDE.md updated with new category and skill counts
- [ ] Skill descriptions under 120 characters each
- [ ] No fn-N spec references in skill content
- [ ] Budget constraint respected (all four validation commands pass)

## References
- `skills/project-structure/dotnet-project-structure/SKILL.md` — existing project structure skill (covers Directory.Build.props basics)
- `skills/agent-meta-skills/dotnet-build-analysis/SKILL.md` — existing build analysis skill (covers MSBuild error interpretation)
- [MSBuild Reference](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-reference)
- [MSBuild Task Reference](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-task-reference)
- [MSBuild Structured Log Viewer](https://msbuildlog.com/)
- dotnet/msbuild repo — IIncrementalTask interface (MSBuild 17.8+)
