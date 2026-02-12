# fn-9: Agent Meta-Skills

## Overview
Delivers meta-skills that teach agents how to work effectively with .NET projects: common gotchas, build output analysis, .csproj reading/modification, and solution navigation.

## Scope
**Skills:**
- `dotnet-agent-gotchas` - Common mistakes agents make with .NET: async/await errors, wrong NuGet packages, deprecated APIs, bad project structure, nullable handling, source gen config, trimming warnings, test organization, DI registration
- `dotnet-build-analysis` - Help agents understand build output, MSBuild errors, NuGet restore issues
- `dotnet-csproj-reading` - Teach agents to read/modify .csproj files, understand MSBuild properties, conditions
- `dotnet-solution-navigation` - Teach agents to navigate .NET solutions: find entry points, understand project dependencies, locate configuration

## Key Context
- These are meta-skills designed to improve agent behavior across all .NET tasks
- Agent gotchas skill should document actual mistakes observed in agent-generated code
- Skills should reference slopwatch patterns from dotnet-skills: https://github.com/Aaronontheweb/dotnet-skills
- MSBuild documentation: https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild

## Quick Commands
```bash
# Smoke test: verify gotchas skill lists common mistakes
grep -i "mistake\|gotcha\|avoid" skills/agent-meta/dotnet-agent-gotchas.md

# Validate MSBuild error patterns
grep -i "MSBuild\|error" skills/agent-meta/dotnet-build-analysis.md

# Test csproj reading patterns
grep -i "csproj\|MSBuild" skills/agent-meta/dotnet-csproj-reading.md
```

## Acceptance Criteria
1. All 4 skills written with standard depth and frontmatter
2. Agent gotchas skill documents common mistakes: blocking async, wrong package versions, deprecated APIs, NRT annotation errors
3. Build analysis skill helps agents parse MSBuild output, NuGet errors, analyzer warnings
4. Csproj reading skill teaches PropertyGroup, ItemGroup, Condition, SDK-style project structure
5. Solution navigation skill documents finding entry points (Program.cs), understanding project references, locating configs
6. Skills reference slopwatch patterns (disabled tests, suppressed warnings, empty catch blocks)
7. Cross-references to other skills where agents commonly make mistakes

## Test Notes
- Test gotchas skill by checking for real-world agent mistake patterns
- Verify build analysis skill covers common MSBuild errors
- Validate csproj reading skill with examples of common modifications

## References
- MSBuild Reference: https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild
- dotnet-skills slopwatch: https://github.com/Aaronontheweb/dotnet-skills
- .NET Project SDK: https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
