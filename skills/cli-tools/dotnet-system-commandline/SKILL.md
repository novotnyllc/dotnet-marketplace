---
name: dotnet-system-commandline
description: "WHEN building CLI apps. System.CommandLine 2.0: RootCommand, Option<T>, middleware, hosting, tab completion, IConsole."
---

# dotnet-system-commandline

System.CommandLine 2.0 API for building .NET CLI applications: RootCommand, Command, Option<T>, Argument<T>, the middleware pipeline, hosting integration with `UseCommandHandler`, tab completion, automatic `--version`/`--help` generation, dependency injection via `Microsoft.Extensions.Hosting`, and the `IConsole` abstraction for testable output.

**Version assumptions:** .NET 8.0+ baseline. System.CommandLine 2.0.0-beta4 (pre-release NuGet package). Despite the beta version number, the API surface is stable and battle-tested -- it powers the `dotnet` CLI itself, the .NET Interactive kernel, and many Microsoft-internal tools. The package has been in active use since 2020 with a stable API contract.

**Out of scope:** CLI application architecture patterns (layered command/handler/service design, configuration precedence, exit codes, stdin/stdout/stderr) -- see [skill:dotnet-cli-architecture]. Native AOT compilation and publish pipeline -- see [skill:dotnet-native-aot] (fn-16). CLI distribution strategy and packaging -- see [skill:dotnet-cli-distribution] (fn-17). General CI/CD patterns -- see [skill:dotnet-gha-patterns] and [skill:dotnet-ado-patterns]. DI container mechanics -- see [skill:dotnet-csharp-dependency-injection] (fn-3).

Cross-references: [skill:dotnet-cli-architecture] for CLI design patterns and testing, [skill:dotnet-native-aot] for AOT publishing CLI tools, [skill:dotnet-csharp-dependency-injection] for DI fundamentals, [skill:dotnet-csharp-configuration] for configuration integration.

---

## Production Readiness Assessment

System.CommandLine 2.0 is distributed as a pre-release NuGet package (`2.0.0-beta4`). This section explains what that means in practice.

**Why it is production-ready despite beta versioning:**
- Powers the `dotnet` CLI (millions of daily invocations)
- Used by .NET Interactive, MAUI workloads, and NuGet client
- Core API surface (Command, Option, Argument, middleware) has been stable since 2021
- Breaking changes between betas are rare and well-documented

**What the beta status means:**
- The NuGet package version includes a pre-release suffix
- Projects using `<TreatWarningsAsErrors>` may need `<NoWarn>` for the pre-release dependency
- API could theoretically change before the 1.0/2.0 stable release
- Some advanced APIs (custom parsing, response files) may see minor changes

```xml
<ItemGroup>
  <PackageReference Include="System.CommandLine" Version="2.0.0-beta4.24324.3" />
  <!-- Hosting integration for DI + UseCommandHandler -->
  <PackageReference Include="System.CommandLine.Hosting" Version="0.4.0-alpha.24324.3" />
  <!-- Required for UseCommandHandler property binding by name -->
  <PackageReference Include="System.CommandLine.NamingConventionBinder" Version="2.0.0-beta4.24324.3" />
</ItemGroup>
```

---

## RootCommand and Command Hierarchy

### Basic Command Structure

```csharp
using System.CommandLine;

// Root command -- the entry point
var rootCommand = new RootCommand("My CLI tool description");

// Add a subcommand
var listCommand = new Command("list", "List all items");
rootCommand.AddCommand(listCommand);

// Nested subcommands: mycli migrate up
var migrateCommand = new Command("migrate", "Database migrations");
var upCommand = new Command("up", "Apply pending migrations");
var downCommand = new Command("down", "Revert last migration");
migrateCommand.AddCommand(upCommand);
migrateCommand.AddCommand(downCommand);
rootCommand.AddCommand(migrateCommand);
```

### Options and Arguments

```csharp
// Option<T> -- named parameter (--output, -o)
var outputOption = new Option<FileInfo>(
    name: "--output",
    description: "Output file path")
{
    IsRequired = true
};
outputOption.AddAlias("-o");

// Argument<T> -- positional parameter
var fileArgument = new Argument<FileInfo>(
    name: "file",
    description: "Input file to process");

// Option with default value
var verbosityOption = new Option<int>(
    name: "--verbosity",
    getDefaultValue: () => 1,
    description: "Verbosity level (0-3)");

// Option with constrained values
var formatOption = new Option<string>(
    name: "--format",
    description: "Output format")
    .FromAmong("json", "csv", "table");

rootCommand.AddOption(outputOption);
rootCommand.AddArgument(fileArgument);
```

### Setting Handlers

```csharp
// Handler receives parsed values via binding
listCommand.SetHandler(
    (FileInfo output, int verbosity) =>
    {
        Console.WriteLine($"Output: {output.FullName}, Verbosity: {verbosity}");
    },
    outputOption, verbosityOption);

// Async handler with cancellation (use InvocationContext for CancellationToken)
listCommand.SetHandler(
    async (InvocationContext context) =>
    {
        var output = context.ParseResult.GetValueForOption(outputOption)!;
        var verbosity = context.ParseResult.GetValueForOption(verbosityOption);
        await ProcessAsync(output, verbosity, context.GetCancellationToken());
    });
```

### Invoking the Command

```csharp
// Program.cs entry point
return await rootCommand.InvokeAsync(args);
```

The return value is the exit code. `InvokeAsync` returns 0 on success, non-zero on failure.

---

## Middleware Pipeline

System.CommandLine has a middleware pipeline that intercepts command invocations, similar to ASP.NET Core middleware.

### Built-In Middleware

The default pipeline includes (in order):
1. **Exception handling** -- catches unhandled exceptions and returns exit code 1
2. **Parse error reporting** -- shows validation errors for invalid input
3. **Help** -- `--help` / `-h` / `-?` triggers help text and short-circuits
4. **Version** -- `--version` triggers version display and short-circuits
5. **Parse directive** -- `[parse]` shows how input was parsed (debugging aid)
6. **Suggest directive** -- `[suggest]` provides tab completion suggestions
7. **User handler** -- the `SetHandler` delegate

### Custom Middleware

```csharp
var builder = new CommandLineBuilder(rootCommand)
    .UseDefaults()  // Adds all built-in middleware
    .AddMiddleware(async (context, next) =>
    {
        // Before: runs before the command handler
        var sw = Stopwatch.StartNew();

        await next(context);

        // After: runs after the command handler
        sw.Stop();
        if (context.ParseResult.GetValueForOption(verboseOption))
        {
            Console.Error.WriteLine($"Elapsed: {sw.ElapsedMilliseconds}ms");
        }
    })
    .Build();

return await builder.InvokeAsync(args);
```

### Middleware Order Matters

Middleware registered with `AddMiddleware` runs in registration order. Place error-handling middleware early and telemetry/logging middleware late.

---

## Hosting Integration

`System.CommandLine.Hosting` integrates with `Microsoft.Extensions.Hosting` to provide DI, configuration, and logging -- the same infrastructure used by ASP.NET Core and worker services.

### Setup

```csharp
using System.CommandLine;
using System.CommandLine.Builder;
using System.CommandLine.Hosting;
using System.CommandLine.NamingConventionBinder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var rootCommand = new RootCommand("My CLI tool");
var syncCommand = new Command("sync", "Synchronize data");
syncCommand.AddOption(new Option<string>("--source", "Source endpoint"));
rootCommand.AddCommand(syncCommand);

var builder = new CommandLineBuilder(rootCommand)
    .UseHost(_ => Host.CreateDefaultBuilder(args), host =>
    {
        host.ConfigureServices(services =>
        {
            services.AddSingleton<ISyncService, SyncService>();
            services.AddSingleton<IFileSystem, PhysicalFileSystem>();
        });

        host.UseCommandHandler<SyncCommand, SyncCommand.Handler>();
    })
    .UseDefaults()
    .Build();

return await builder.InvokeAsync(args);
```

### Command Handler Class Pattern

```csharp
public class SyncCommand
{
    public class Handler : ICommandHandler
    {
        private readonly ISyncService _syncService;

        // Constructor injection -- resolved from DI
        public Handler(ISyncService syncService)
        {
            _syncService = syncService;
        }

        // Bound from command-line options (by naming convention)
        public string Source { get; set; } = "";

        public int Invoke(InvocationContext context) =>
            InvokeAsync(context).GetAwaiter().GetResult();

        public async Task<int> InvokeAsync(InvocationContext context)
        {
            await _syncService.SyncAsync(Source, context.GetCancellationToken());
            return 0;  // exit code
        }
    }
}
```

`UseCommandHandler<TCommand, THandler>` binds option/argument values to public properties on the handler by name. The handler is resolved from DI, so constructor injection works.

---

## Tab Completion

System.CommandLine provides shell-native tab completion for Bash, Zsh, Fish, and PowerShell.

### Enabling Completion

```csharp
var builder = new CommandLineBuilder(rootCommand)
    .UseDefaults()  // Includes suggest directive
    .Build();
```

Users register completions for their shell:

```bash
# Bash -- add to ~/.bashrc
source <(mycli [suggest:bash])

# Zsh -- add to ~/.zshrc
source <(mycli [suggest:zsh])

# PowerShell -- add to $PROFILE
mycli [suggest:powershell] | Out-String | Invoke-Expression

# Fish
mycli [suggest:fish] | source
```

### Custom Completion

```csharp
var envOption = new Option<string>("--environment");
envOption.AddCompletions("development", "staging", "production");

// Dynamic completions
var branchOption = new Option<string>("--branch");
branchOption.AddCompletions(ctx =>
{
    // Return completions based on context
    return GetGitBranches();
});
```

---

## Automatic --version and --help

### Version

`--version` is automatically added to the RootCommand. It reads from:
1. `AssemblyInformationalVersionAttribute` (preferred -- includes SemVer metadata)
2. `AssemblyVersionAttribute` (fallback)

```xml
<!-- Set in .csproj for automatic --version output -->
<PropertyGroup>
  <Version>1.2.3</Version>
  <!-- Or use source link / CI-generated version -->
  <InformationalVersion>1.2.3+abc123</InformationalVersion>
</PropertyGroup>
```

### Help Customization

```csharp
var rootCommand = new RootCommand("Tool description shown in help");

// Help is automatic for all commands, options, and arguments
// Descriptions come from constructor parameters

// Customize help layout
var builder = new CommandLineBuilder(rootCommand)
    .UseHelp(ctx =>
    {
        ctx.HelpBuilder.CustomizeLayout(_ =>
            HelpBuilder.Default.GetLayout()
                .Append(_ => _.Output.WriteLine("Examples:"))
                .Append(_ => _.Output.WriteLine("  mycli sync --source https://api.example.com")));
    })
    .UseDefaults()
    .Build();
```

---

## IConsole Abstraction

`IConsole` provides a testable abstraction over `Console`. Use it in command handlers to enable unit testing without capturing stdout/stderr globally.

### Using IConsole in Handlers

```csharp
public class ListHandler : ICommandHandler
{
    private readonly IItemRepository _repository;

    public ListHandler(IItemRepository repository)
    {
        _repository = repository;
    }

    public async Task<int> InvokeAsync(InvocationContext context)
    {
        var items = await _repository.GetAllAsync();
        var console = context.Console;

        foreach (var item in items)
        {
            console.Out.Write($"{item.Id}: {item.Name}\n");
        }

        if (!items.Any())
        {
            console.Error.Write("No items found.\n");
            return 1;
        }

        return 0;
    }

    public int Invoke(InvocationContext context) =>
        InvokeAsync(context).GetAwaiter().GetResult();
}
```

### Testing with TestConsole

```csharp
[Fact]
public async Task ListHandler_WritesItems_ToStdout()
{
    var repository = new FakeItemRepository(
    [
        new Item(1, "Widget"),
        new Item(2, "Gadget")
    ]);

    var handler = new ListHandler(repository);
    var console = new TestConsole();
    var context = new InvocationContext(
        new Parser(new RootCommand()).Parse(""), console);

    var exitCode = await handler.InvokeAsync(context);

    Assert.Equal(0, exitCode);
    Assert.Contains("Widget", console.Out.ToString());
}
```

---

## Validation

### Option Validators

```csharp
var portOption = new Option<int>("--port", "Port number");
portOption.AddValidator(result =>
{
    var value = result.GetValueForOption(portOption);
    if (value < 1 || value > 65535)
    {
        result.ErrorMessage = "Port must be between 1 and 65535";
    }
});

// Arity constraints
var tagsOption = new Option<string[]>("--tag")
{
    Arity = new ArgumentArity(1, 5),  // 1 to 5 tags
    AllowMultipleArgumentsPerToken = true
};
```

### Global Options

```csharp
// Global options are inherited by all subcommands
var verboseOption = new Option<bool>("--verbose", "Enable verbose output");
verboseOption.AddAlias("-v");
rootCommand.AddGlobalOption(verboseOption);

// Available in any subcommand handler
syncCommand.SetHandler((bool verbose) =>
{
    if (verbose) Console.Error.WriteLine("Verbose mode enabled");
}, verboseOption);
```

---

## Response Files

System.CommandLine supports response files (`@filename`) for passing large sets of arguments:

```bash
# args.rsp
--source https://api.example.com
--output /tmp/results.json
--verbose

# Invoke with response file
mycli sync @args.rsp
```

Response file support is included in `UseDefaults()`.

---

## Agent Gotchas

1. **Do not use `System.CommandLine` 1.x patterns.** Version 2.0 has a completely different API surface. There is no `CommandHandler.Create()` in 2.0 -- use `SetHandler` or `UseCommandHandler` with hosting.
2. **Do not confuse `Option<T>` with `Argument<T>`.** Options are named (`--output file.txt`), arguments are positional (`mycli file.txt`). Using the wrong type produces confusing parse errors.
3. **Do not forget `UseDefaults()` on `CommandLineBuilder`.** Without it, help, version, error reporting, and completion all fail silently. `UseDefaults()` registers all standard middleware.
4. **Do not use `SetHandler` with more than 8 parameters.** The generic overloads max out at 8. For complex commands, use the hosting pattern with `UseCommandHandler<TCommand, THandler>` and property binding.
5. **Do not ignore the pre-release package version.** Projects with `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` will fail to build unless the pre-release dependency is acknowledged via `<NoWarn>NU5104</NoWarn>` or explicit version pinning.
6. **Do not write to `Console.Out` directly in hosted command handlers.** Use the `IConsole` abstraction from `InvocationContext.Console` for testability. Direct console writes bypass the test harness.

---

## References

- [System.CommandLine overview](https://learn.microsoft.com/en-us/dotnet/standard/commandline/)
- [System.CommandLine API reference](https://learn.microsoft.com/en-us/dotnet/api/system.commandline)
- [Tab completion](https://learn.microsoft.com/en-us/dotnet/standard/commandline/tab-completion)
- [Hosting integration](https://learn.microsoft.com/en-us/dotnet/standard/commandline/hosting)
- [System.CommandLine GitHub](https://github.com/dotnet/command-line-api)
