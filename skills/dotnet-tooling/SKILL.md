---
name: dotnet-tooling
description: Manages .NET project setup, build systems, and developer tooling. Covers solution structure, MSBuild (authoring, tasks, Directory.Build), build optimization, performance patterns, profiling (dotnet-counters/trace/dump), Native AOT publishing, trimming, GC/memory tuning, CLI app architecture (System.CommandLine, Spectre.Console, Terminal.Gui), docs generation, tool management, version detection/upgrade, and solution navigation.
license: MIT
user-invocable: true
---

# dotnet-tooling

## Overview

.NET project setup, build systems, performance, CLI apps, and developer tooling. This consolidated skill spans 32 topic areas. Load the appropriate companion file from `references/` based on the routing table below.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Project structure | solution, .slnx, CPM, analyzers | references/project-structure.md |
| Scaffold project | dotnet new, CPM, SourceLink, editorconfig | references/scaffold-project.md |
| Csproj reading | PropertyGroup, ItemGroup, CPM, props | references/csproj-reading.md |
| MSBuild authoring | targets, props, conditions, Directory.Build | references/msbuild-authoring.md |
| MSBuild tasks | ITask, ToolTask, inline tasks, UsingTask | references/msbuild-tasks.md |
| Build analysis | MSBuild output, NuGet errors, analyzer warnings | references/build-analysis.md |
| Build optimization | slow builds, binary logs, parallel, restore | references/build-optimization.md |
| Artifacts output | UseArtifactsOutput, ArtifactsPath, CI/Docker | references/artifacts-output.md |
| Multi-targeting | multiple TFMs, polyfills, conditional compilation | references/multi-targeting.md |
| Performance patterns | Span, ArrayPool, ref struct, sealed, stackalloc | references/performance-patterns.md |
| Profiling | dotnet-counters, dotnet-trace, flame graphs | references/profiling.md |
| Native AOT | PublishAot, ILLink, P/Invoke, size optimization | references/native-aot.md |
| AOT architecture | source gen, AOT-safe DI, serialization | references/aot-architecture.md |
| Trimming | annotations, ILLink, IL2xxx warnings, IsTrimmable | references/trimming.md |
| GC/memory | GC modes, LOH/POH, Span/Memory, ArrayPool | references/gc-memory.md |
| CLI architecture | command/handler/service, clig.dev, exit codes | references/cli-architecture.md |
| System.CommandLine | RootCommand, Option<T>, SetAction, parsing | references/system-commandline.md |
| Spectre.Console | tables, trees, progress, prompts, live displays | references/spectre-console.md |
| Terminal.Gui | views, layout, menus, dialogs, bindings, themes | references/terminal-gui.md |
| CLI distribution | AOT vs framework-dependent, RID matrix | references/cli-distribution.md |
| CLI packaging | Homebrew, apt/deb, winget, Scoop, Chocolatey | references/cli-packaging.md |
| CLI release pipeline | GHA build matrix, artifact staging, checksums | references/cli-release-pipeline.md |
| Documentation strategy | Starlight, Docusaurus, DocFX decision tree | references/documentation-strategy.md |
| XML docs | tags, inheritdoc, GenerateDocumentationFile | references/xml-docs.md |
| Tool management | global, local, manifests, restore, pinning | references/tool-management.md |
| Version detection | TFM/SDK from .csproj, global.json | references/version-detection.md |
| Version upgrade | LTS-to-LTS, staged, preview, upgrade paths | references/version-upgrade.md |
| Solution navigation | entry points, .sln/.slnx, dependency graphs | references/solution-navigation.md |
| Project analysis | solution layout, build config analysis | references/project-analysis.md |
| Modernize | outdated TFMs, deprecated packages, patterns | references/modernize.md |
| Add analyzers | nullable, trimming, AOT compat, severity config | references/add-analyzers.md |
| Mermaid diagrams | architecture, sequence, class, ER, flowcharts | references/mermaid-diagrams.md |

## Scope

- Solution structure and project scaffolding
- MSBuild authoring and build optimization
- Performance patterns and profiling
- Native AOT, trimming, GC tuning
- CLI app development (System.CommandLine, Spectre.Console, Terminal.Gui)
- Documentation generation (DocFX, XML docs)
- Tool management and version detection/upgrade
- Solution navigation and project analysis
- Code modernization and analyzer configuration
- Mermaid diagram generation

## Out of scope

- Web API patterns -> [skill:dotnet-api]
- Test authoring -> [skill:dotnet-testing]
- CI/CD pipelines -> [skill:dotnet-devops]
- C# language patterns -> [skill:dotnet-csharp]
- UI framework development -> [skill:dotnet-ui]
- WinDbg debugging -> [skill:dotnet-debugging]

## Companion Files

- `references/project-structure.md` -- .slnx, Directory.Build.props, CPM, analyzers
- `references/scaffold-project.md` -- dotnet new with CPM, analyzers, editorconfig, SourceLink
- `references/csproj-reading.md` -- SDK-style .csproj, PropertyGroup, ItemGroup, CPM
- `references/msbuild-authoring.md` -- Targets, props, conditions, Directory.Build patterns
- `references/msbuild-tasks.md` -- ITask, ToolTask, IIncrementalTask, inline tasks
- `references/build-analysis.md` -- MSBuild output, NuGet errors, analyzer warnings
- `references/build-optimization.md` -- Slow builds, binary logs, parallel, restore
- `references/artifacts-output.md` -- UseArtifactsOutput, ArtifactsPath, CI/Docker impact
- `references/multi-targeting.md` -- Multiple TFMs, PolySharp, conditional compilation
- `references/performance-patterns.md` -- Span, ArrayPool, ref struct, sealed, stackalloc
- `references/profiling.md` -- dotnet-counters, dotnet-trace, dotnet-dump, flame graphs
- `references/native-aot.md` -- PublishAot, ILLink descriptors, P/Invoke, size optimization
- `references/aot-architecture.md` -- Source gen over reflection, AOT-safe DI, factories
- `references/trimming.md` -- Annotations, ILLink, IL2xxx warnings, IsTrimmable
- `references/gc-memory.md` -- GC modes, LOH/POH, Gen0/1/2, Span/Memory, ArrayPool
- `references/cli-architecture.md` -- Command/handler/service, clig.dev, exit codes
- `references/system-commandline.md` -- System.CommandLine 2.0, RootCommand, Option<T>
- `references/spectre-console.md` -- Tables, trees, progress, prompts, live displays
- `references/terminal-gui.md` -- Terminal.Gui v2, views, layout, menus, dialogs
- `references/cli-distribution.md` -- AOT vs framework-dependent, RID matrix, single-file
- `references/cli-packaging.md` -- Homebrew, apt/deb, winget, Scoop, Chocolatey
- `references/cli-release-pipeline.md` -- GHA build matrix, artifact staging, checksums
- `references/documentation-strategy.md` -- Starlight, Docusaurus, DocFX decision tree
- `references/xml-docs.md` -- XML doc comments, inheritdoc, warning suppression
- `references/tool-management.md` -- Global/local tools, manifests, restore, pinning
- `references/version-detection.md` -- TFM/SDK from .csproj, global.json, Directory.Build
- `references/version-upgrade.md` -- LTS-to-LTS, staged through STS, preview paths
- `references/solution-navigation.md` -- Entry points, .sln/.slnx, dependency graphs
- `references/project-analysis.md` -- Solution layout, build config, .csproj analysis
- `references/modernize.md` -- Outdated TFMs, deprecated packages, superseded patterns
- `references/add-analyzers.md` -- Nullable, trimming, AOT compat analyzers, severity
- `references/mermaid-diagrams.md` -- Architecture, sequence, class, deployment, ER diagrams

## Scripts

- `scripts/scan-dotnet-targets.py` -- Scan repository for .NET TFM and SDK version signals
