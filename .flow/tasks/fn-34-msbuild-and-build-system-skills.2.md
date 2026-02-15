# fn-34-msbuild-and-build-system-skills.2 Create MSBuild custom tasks skill (ITask, IIncrementalTask, inline)

## Description
Create `skills/build-system/dotnet-msbuild-tasks/SKILL.md` covering custom MSBuild task authoring: ITask interface, ToolTask base class, IIncrementalTask (MSBuild 17.8+, VS 2022 17.8+, .NET 8 SDK), inline tasks (CodeTaskFactory), UsingTask registration, task parameters, debugging, and NuGet packaging.

**Size:** M
**Files:** `skills/build-system/dotnet-msbuild-tasks/SKILL.md`
**Does NOT touch:** `.claude-plugin/plugin.json` (owned by task .3)

## Approach
- ITask interface and ToolTask base class patterns
- IIncrementalTask: `Microsoft.Build.Framework.IIncrementalTask` — requires MSBuild 17.8+ (VS 2022 17.8+, .NET 8 SDK). Document version gate explicitly.
- Task parameters: [Required], [Output], ITaskItem, ITaskItem[]
- Inline tasks with CodeTaskFactory (for simple cases)
- UsingTask registration in .targets files
- Task debugging: MSBUILDDEBUGONSTART=1 or =2, attaching debugger
- Task NuGet packaging: buildTransitive and build folders, props/targets files
- Cross-ref to `[skill:dotnet-msbuild-authoring]` (soft — same epic)
- Each section uses explicit `##` headers
- Include Agent Gotchas section (task authoring pitfalls)
- Include References section with Microsoft Learn links

## Acceptance
- [ ] ITask interface and ToolTask base class covered
- [ ] IIncrementalTask documented with MSBuild 17.8+ version gate
- [ ] Inline tasks (CodeTaskFactory) documented with example
- [ ] UsingTask registration pattern documented
- [ ] Task parameters ([Required], [Output], ITaskItem) covered
- [ ] Task debugging (MSBUILDDEBUGONSTART) documented
- [ ] Task NuGet packaging (buildTransitive/build folders) documented
- [ ] Cross-ref to `[skill:dotnet-msbuild-authoring]` present
- [ ] Agent Gotchas section with task authoring pitfalls
- [ ] References section with Microsoft Learn links
- [ ] All cross-references use `[skill:name]` syntax
- [ ] SKILL.md frontmatter has `name` and `description` only
- [ ] Description under 120 characters

## Validation
```bash
# Verify skill file exists and has required frontmatter
grep -q '^name: dotnet-msbuild-tasks' skills/build-system/dotnet-msbuild-tasks/SKILL.md
grep -q '^description:' skills/build-system/dotnet-msbuild-tasks/SKILL.md

# Verify IIncrementalTask version gate is documented
grep -q 'MSBuild 17.8' skills/build-system/dotnet-msbuild-tasks/SKILL.md

# Verify cross-references use [skill:] syntax
grep -c '\[skill:dotnet-msbuild-authoring\]' skills/build-system/dotnet-msbuild-tasks/SKILL.md

# Verify Agent Gotchas section exists
grep -q '## .*Gotcha' skills/build-system/dotnet-msbuild-tasks/SKILL.md

# Verify References section exists
grep -q '## References' skills/build-system/dotnet-msbuild-tasks/SKILL.md

# Run full validation
./scripts/validate-skills.sh
```

## Done summary
Created MSBuild custom tasks skill (dotnet-msbuild-tasks) covering ITask interface, ToolTask base class, IIncrementalTask with MSBuild 17.8+ version gate, inline tasks via CodeTaskFactory, UsingTask registration, task parameters with ITaskItem metadata access, MSBUILDDEBUGONSTART debugging, and NuGet task packaging with build/buildTransitive folders.
## Evidence
- Commits: 07e6ff29a3a5d75a8f7cd68e30a9b8c4b08f8e57, e77cee3afb4063ebd5d6ccacf0123fecf3d28795
- Tests: ./scripts/validate-skills.sh
- PRs: