# fn-64.6 Consolidate dotnet-tooling (32 source skills)
<!-- Updated by plan-sync: fn-64.1 mapped 32 source skills to dotnet-tooling, not ~34. agent-gotchas -> dotnet-api, slopwatch -> dotnet-testing, add-ci -> dotnet-devops, add-testing -> dotnet-testing -->

## Description
Create consolidated `dotnet-tooling` skill directory. Merge 32 build, performance, AOT, CLI, project setup, docs generation, and version management skills into one skill with companion files. This is the largest consolidation group. Delete source skill directories. Do NOT edit `plugin.json` (deferred to task .9).

**Size:** M
**Files:** `skills/dotnet-tooling/SKILL.md` + `references/*.md` (new), 32 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: developer tooling overview, routing table with rich keyword hints, scope/out-of-scope, ToC (~4-5KB given breadth)
- Create `references/` dir with one companion file per source skill (32 files total, per consolidation map from .1):
  - `references/project-structure.md` — .slnx, Directory.Build.props, CPM, analyzers
  - `references/scaffold-project.md` — dotnet new with CPM, analyzers, editorconfig, SourceLink
  - `references/csproj-reading.md` — SDK-style .csproj, PropertyGroup, ItemGroup, CPM
  - `references/msbuild-authoring.md` — targets, props, conditions, Directory.Build patterns
  - `references/msbuild-tasks.md` — ITask, ToolTask, inline tasks (merge existing examples.md)
  - `references/build-analysis.md` — MSBuild output, NuGet errors, analyzer warnings
  - `references/build-optimization.md` — slow builds, binary logs, parallel, restore
  - `references/artifacts-output.md` — UseArtifactsOutput, ArtifactsPath, CI/Docker impact
  - `references/multi-targeting.md` — multiple TFMs, PolySharp, conditional compilation
  - `references/performance-patterns.md` — Span, ArrayPool, ref struct, sealed, stackalloc
  - `references/profiling.md` — dotnet-counters, dotnet-trace, dotnet-dump, flame graphs
  - `references/native-aot.md` — PublishAot, ILLink, P/Invoke, size optimization
  - `references/aot-architecture.md` — source gen over reflection, AOT-safe DI, factories
  - `references/trimming.md` — annotations, ILLink, IL2xxx warnings, IsTrimmable
  - `references/gc-memory.md` — GC modes, LOH/POH, Gen0/1/2, Span/Memory, ArrayPool
  - `references/cli-architecture.md` — command/handler/service, clig.dev, exit codes
  - `references/system-commandline.md` — System.CommandLine 2.0, RootCommand, Option<T> (merge existing examples.md)
  - `references/spectre-console.md` — tables, trees, progress, prompts, live displays
  - `references/terminal-gui.md` — Terminal.Gui v2, views, layout, menus, dialogs (merge existing examples.md)
  - `references/cli-distribution.md` — AOT vs framework-dependent, RID matrix, single-file
  - `references/cli-packaging.md` — Homebrew, apt/deb, winget, Scoop, Chocolatey
  - `references/cli-release-pipeline.md` — GHA build matrix, artifact staging, checksums
  - `references/documentation-strategy.md` — Starlight, Docusaurus, DocFX decision tree
  - `references/xml-docs.md` — XML doc comments, inheritdoc, warning suppression (merge existing examples.md)
  - `references/tool-management.md` — global/local tools, manifests, restore, pinning
  - `references/version-detection.md` — TFM/SDK from .csproj, global.json, Directory.Build
  - `references/version-upgrade.md` — LTS-to-LTS, staged through STS, preview paths
  - `references/solution-navigation.md` — entry points, .sln/.slnx, dependency graphs
  - `references/project-analysis.md` — solution layout, build config, .csproj analysis
  - `references/modernize.md` — outdated TFMs, deprecated packages, superseded patterns
  - `references/add-analyzers.md` — nullable, trimming, AOT compat analyzers, severity
  - `references/mermaid-diagrams.md` — architecture, sequence, class, deployment, ER diagrams (merge existing examples.md)
  - Note: `scripts/scan-dotnet-targets.py` preserved from dotnet-version-detection as `scripts/scan-dotnet-targets.py`
- Delete old skill directories after content is migrated
- **Do NOT edit plugin.json** — manifest update deferred to task .9

## Key context

- This is the broadest consolidation (32 source skills) — intentionally a grab-bag per epic decision #9
- The SKILL.md routing table must have strong keyword differentiation since sub-topics are diverse
- Several absorbed source skills were user-invocable (scaffold-project, add-analyzers, modernize, version-upgrade). Task .1 decided: dotnet-tooling is user-invocable: true. Note: add-ci went to dotnet-devops, add-testing and slopwatch went to dotnet-testing
- `dotnet-version-detection` and `dotnet-project-analysis` are shared foundations used by 5 agents — companion file must be prominent in ToC
- If post-implementation this feels too broad, splitting into build/performance/cli is a single-task change (epic decision #9)

## Acceptance
- [ ] `skills/dotnet-tooling/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-tooling/references/` contains 32 companion files (one per source skill) plus `scripts/scan-dotnet-targets.py`
- [ ] All 32 source tooling skill directories deleted
- [ ] `plugin.json` NOT edited (deferred to task .9)
- [ ] Valid frontmatter
- [ ] No content lost from source skills
- [ ] User-invocable set to `true` (per task .1: absorbs scaffold-project, add-analyzers, modernize, version-upgrade)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
