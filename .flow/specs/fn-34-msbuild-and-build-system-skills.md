# MSBuild and Build System Skills

## Overview
Create a new skill category for MSBuild/project system authoring and build optimization. Covers custom targets, props files, items, tasks (managed and inline), UsingTask, and crucially — diagnosing and fixing incremental build failures.

## Scope
- **MSBuild Authoring skill** — Custom targets, props/targets import order, items and item metadata, conditions, property functions, well-known metadata
- **MSBuild Custom Tasks** — ITask, IIncrementalTask (from dotnet/msbuild), inline tasks, managed tasks, UsingTask registration, task input/output parameters
- **Build Optimization skill** — Incremental build diagnostics (when MSBuild warns "not all outputs are up to date", files modified mid-build), `/bl` binary log analysis, MSBuild Structured Log Viewer, `/graph` mode, `/p:BuildInParallel`, NoWarn/TreatWarningsAsErrors
- **Directory.Build.props/targets patterns** — Import ordering, condition guards, property inheritance, preventing double-imports

**Package version policy**: Always reference latest stable MSBuild SDK versions.

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] MSBuild authoring skill covering targets, props, items, conditions, property functions
- [ ] Custom task skill covering ITask, IIncrementalTask, inline tasks, UsingTask
- [ ] Build optimization skill covering incremental build diagnosis, binary log analysis, parallel builds
- [ ] Directory.Build.props/targets patterns documented
- [ ] Incremental build failure diagnosis workflow (warning → binary log → root cause → fix)
- [ ] No fn-N spec references
- [ ] Budget constraint respected
- [ ] All validation commands pass

## References
- `skills/project-structure/dotnet-project-structure/SKILL.md` — existing project structure skill (covers Directory.Build.props basics)
- dotnet/msbuild repo — IIncrementalTask interface
- MSBuild Structured Log Viewer — binary log analysis tool
