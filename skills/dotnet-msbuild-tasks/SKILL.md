---
name: dotnet-msbuild-tasks
description: Writes custom MSBuild tasks. ITask, ToolTask, IIncrementalTask, inline tasks, UsingTask.
license: MIT
user-invocable: false
---

# dotnet-msbuild-tasks

Guidance for authoring custom MSBuild tasks: implementing the `ITask` interface, extending `ToolTask` for CLI wrappers, using `IIncrementalTask` (MSBuild 17.8+) for incremental execution, defining inline tasks with `CodeTaskFactory`, registering tasks via `UsingTask`, declaring task parameters, debugging tasks, and packaging tasks as NuGet packages.

**Version assumptions:** .NET 8.0+ SDK (MSBuild 17.8+). `IIncrementalTask` requires MSBuild 17.8+ (VS 2022 17.8+, .NET 8 SDK). All examples use SDK-style projects. All C# examples assume `using Microsoft.Build.Framework;` and `using Microsoft.Build.Utilities;` are in scope unless shown explicitly.

## Scope

- ITask interface and Task base class implementation
- ToolTask for wrapping external CLI tools
- IIncrementalTask for engine-filtered incremental execution
- Inline tasks with CodeTaskFactory
- UsingTask registration and task parameters
- Task debugging and NuGet packaging

## Out of scope

- MSBuild project system authoring (targets, props, items, conditions) -- see [skill:dotnet-msbuild-authoring]

Cross-references: [skill:dotnet-msbuild-authoring] for custom targets, import ordering, items, conditions, and property functions.

---

## ITask Interface

All MSBuild tasks implement `Microsoft.Build.Framework.ITask`. The simplest approach is to inherit from `Microsoft.Build.Utilities.Task`, which provides default implementations for `BuildEngine` and `HostObject`.

### Minimal Custom Task

```csharp
using Microsoft.Build.Framework;
using Microsoft.Build.Utilities;

public class GenerateFileHash : Task
{
    [Required]
    public string InputFile { get; set; } = string.Empty;

    [Output]
    public string Hash { get; set; } = string.Empty;

    public override bool Execute()
    {
        if (!File.Exists(InputFile))
        {
            Log.LogError("Input file not found: {0}", InputFile);
            return false;
        }

        using var stream = File.OpenRead(InputFile);
        var bytes = System.Security.Cryptography.SHA256.HashData(stream);
        Hash = Convert.ToHexString(bytes).ToLowerInvariant();

        Log.LogMessage(MessageImportance.Normal,
            "SHA-256 hash for {0}: {1}", InputFile, Hash);
        return true;
    }
}
```

### ITask Contract

| Member | Purpose |
|---|---|
| `BuildEngine` | Provides logging, error reporting, and build context |
| `HostObject` | Host-specific data (rarely used) |
| `Execute()` | Runs the task. Return `true` for success, `false` for failure |

The `Task` base class exposes a `Log` property (`TaskLoggingHelper`) with convenience methods:

| Method | When to use |
|---|---|
| `Log.LogMessage(importance, msg)` | Informational output (Normal, High, Low) |
| `Log.LogWarning(msg)` | Non-fatal issues |
| `Log.LogError(msg)` | Fatal errors (causes build failure) |
| `Log.LogWarningFromException(ex)` | Warning from caught exception |
| `Log.LogErrorFromException(ex)` | Error from caught exception |

---


For detailed code examples (ToolTask, IIncrementalTask, task parameters, inline tasks, UsingTask, debugging, NuGet packaging), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Returning `false` without logging an error.** If `Execute()` returns `false` but `Log.LogError` was never called, MSBuild reports a generic "task failed" with no actionable message. Always log an error before returning `false`.

2. **Using `Console.WriteLine` instead of `Log.LogMessage`.** Console output bypasses MSBuild's logging infrastructure and may not appear in build logs, binary logs, or IDE error lists. Always use `Log.LogMessage`, `Log.LogWarning`, or `Log.LogError`.

3. **Referencing `IIncrementalTask` without version-gating.** This interface requires MSBuild 17.8+ (.NET 8 SDK). Tasks referencing it will fail to load on older MSBuild versions with a `TypeLoadException`. If supporting older SDKs, use target-level `Inputs`/`Outputs` instead. If the task must support both old and new MSBuild, ship separate task assemblies per MSBuild version range or use `#if` conditional compilation with a version constant.

4. **Placing task DLLs in the NuGet `lib/` folder.** This adds the assembly as a compile reference to consuming projects, polluting their type namespace. Set `IncludeBuildOutput=false` and pack into `tools/` instead.

5. **Forgetting `PrivateAssets="all"` on MSBuild framework package references.** Without it, `Microsoft.Build.Framework` and `Microsoft.Build.Utilities.Core` become transitive dependencies of consuming projects, causing version conflicts.

6. **Using `AssemblyFile` with a path relative to the project.** In NuGet packages, the `.targets` file is in a different location than the consuming project. Use `$(MSBuildThisFileDirectory)` to build paths relative to the `.targets` file itself.

7. **Leaving `Debugger.Launch()` in release builds.** Shipping a task with unconditional `Debugger.Launch()` halts builds on CI/CD servers. Guard with `#if DEBUG` or remove before packaging.

8. **Inline tasks with complex dependencies.** `CodeTaskFactory` compiles code at build time with limited assembly references. For tasks that need NuGet packages or complex type hierarchies, compile a standalone task assembly instead.

---

## References

- [MSBuild Task Writing](https://learn.microsoft.com/en-us/visualstudio/msbuild/task-writing)
- [MSBuild Task Reference](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-task-reference)
- [ToolTask Class](https://learn.microsoft.com/en-us/dotnet/api/microsoft.build.utilities.tooltask)
- [MSBuild Inline Tasks](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-inline-tasks)
- [UsingTask Element](https://learn.microsoft.com/en-us/visualstudio/msbuild/usingtask-element-msbuild)
- [MSBuild Task Parameters](https://learn.microsoft.com/en-us/visualstudio/msbuild/task-writing#task-parameters)
- [Creating a NuGet Package with MSBuild Tasks](https://learn.microsoft.com/en-us/nuget/create-packages/creating-a-package-msbuild)
- [Debugging MSBuild Tasks](https://learn.microsoft.com/en-us/visualstudio/msbuild/how-to-debug-msbuild-custom-task)
