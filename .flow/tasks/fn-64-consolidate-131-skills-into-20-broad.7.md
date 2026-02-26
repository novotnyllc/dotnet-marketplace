# fn-64-consolidate-131-skills-into-20-broad.7 Consolidate build and performance skills: dotnet-performance, dotnet-aot, dotnet-build, dotnet-cli-apps

## Description
Create consolidated skill directories for build and performance skills: `dotnet-performance`, `dotnet-aot`, `dotnet-build`, and `dotnet-cli-apps`.

**Size:** M
**Files:** `skills/dotnet-performance/SKILL.md` + `references/*.md` (new), `skills/dotnet-aot/SKILL.md` + `references/*.md` (new), `skills/dotnet-build/SKILL.md` + `references/*.md` (new), `skills/dotnet-cli-apps/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~20 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- `dotnet-performance` merges: benchmarkdotnet, performance-patterns, profiling, ci-benchmarking, gc-memory, linq-optimization
- `dotnet-aot` merges: native-aot, aot-architecture, trimming, aot-wasm
- `dotnet-build` merges: msbuild-authoring, msbuild-tasks, build-optimization, build-analysis, csproj-reading
- `dotnet-cli-apps` merges: system-commandline, cli-architecture, cli-distribution, cli-packaging, cli-release-pipeline, tool-management, terminal-gui, spectre-console
## Acceptance
- [ ] 4 consolidated skill directories created with SKILL.md + references/
- [ ] All source skill directories for this batch deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter on all SKILL.md files
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
