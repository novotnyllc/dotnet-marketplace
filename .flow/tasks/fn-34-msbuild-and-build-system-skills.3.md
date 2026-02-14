# fn-34-msbuild-and-build-system-skills.3 Create build optimization and diagnostics skill

## Description
Create skills/build-system/dotnet-build-optimization/SKILL.md covering build optimization and diagnostics. Key focus: diagnosing incremental build failures, binary log analysis, parallel builds, and common build performance pitfalls.

**Size:** M
**Files:** skills/build-system/dotnet-build-optimization/SKILL.md, .claude-plugin/plugin.json

## Approach
- Incremental build diagnostics: warning -> /bl binary log -> Structured Log Viewer -> root cause -> fix
- Common failures: targets without Inputs/Outputs, file copy timestamps, generators writing mid-build
- Binary log analysis: dotnet build /bl, MSBuild Structured Log Viewer, msbuild -pp
- Parallel build: /m, /graph mode, BuildInParallel property
- NoWarn/TreatWarningsAsErrors strategy
- Build caching: NuGet restore optimization, .NET SDK artifact caching
- Cross-ref to [skill:dotnet-msbuild-authoring] and [skill:dotnet-msbuild-tasks]
## Acceptance
- [ ] Incremental build failure diagnosis workflow
- [ ] Binary log analysis
- [ ] Parallel build configuration
- [ ] Common pitfalls listed
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
