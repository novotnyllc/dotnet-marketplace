# fn-34-msbuild-and-build-system-skills.2 Create MSBuild custom tasks skill (ITask, IIncrementalTask, inline)

## Description
Create skills/build-system/dotnet-msbuild-tasks/SKILL.md covering custom MSBuild task authoring: ITask interface, IIncrementalTask, inline tasks (CodeTaskFactory), UsingTask registration, task parameters, and debugging.

**Size:** M
**Files:** skills/build-system/dotnet-msbuild-tasks/SKILL.md, .claude-plugin/plugin.json

## Approach
- ITask and ToolTask base classes
- IIncrementalTask: when to use, implementation pattern (from dotnet/msbuild repo)
- Task parameters: [Required], [Output], ITaskItem, ITaskItem[]
- Inline tasks with CodeTaskFactory (for simple cases)
- UsingTask registration in .targets files
- Task debugging: MSBUILDDEBUGONSTART, attaching debugger
- Task NuGet packaging: buildTransitive, build folders
- Cross-ref to [skill:dotnet-msbuild-authoring]
## Acceptance
- [ ] ITask and IIncrementalTask covered
- [ ] Inline tasks documented
- [ ] UsingTask and packaging patterns
- [ ] Debugging guidance
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
