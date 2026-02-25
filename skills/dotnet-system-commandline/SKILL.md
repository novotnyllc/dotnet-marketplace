---
name: dotnet-system-commandline
description: System.CommandLine 2.0 CLI apps. RootCommand, Option<T>, SetAction, parsing, tab completion.
license: MIT
user-invocable: false
---

# dotnet-system-commandline

System.CommandLine 2.0 stable API for building .NET CLI applications. Covers RootCommand, Command, Option\<T\>, Argument\<T\>, SetAction for handler binding, ParseResult-based value access, custom type parsing, validation, tab completion, and testing with TextWriter capture.

**Version assumptions:** .NET 8.0+ baseline. System.CommandLine 2.0.0+ (stable NuGet package, GA since November 2025). All examples target the 2.0.0 GA API surface.

**Breaking change note:** System.CommandLine 2.0.0 GA differs significantly from the pre-release beta4 API. Key changes: `SetHandler` replaced by `SetAction`, `ICommandHandler` removed in favor of `SynchronousCommandLineAction`/`AsynchronousCommandLineAction`, `InvocationContext` removed (ParseResult passed directly), `CommandLineBuilder` and `AddMiddleware` removed, `IConsole` removed in favor of TextWriter properties, and the `System.CommandLine.Hosting`/`System.CommandLine.NamingConventionBinder` packages discontinued. Do not use beta-era patterns.

## Scope

- RootCommand, Command, Option<T>, Argument<T> hierarchy
- SetAction handler binding (sync and async)
- ParseResult-based value access
- Custom type parsing and validation
- Tab completion and directives
- Testing with InvocationConfiguration and TextWriter capture
- Migration from beta4 to 2.0.0 GA
- Dependency injection integration without System.CommandLine.Hosting

## Out of scope

- CLI application architecture patterns (layered design, exit codes, stdin/stdout/stderr) -- see [skill:dotnet-cli-architecture]
- Native AOT compilation -- see [skill:dotnet-native-aot]
- CLI distribution strategy -- see [skill:dotnet-cli-distribution]
- General CI/CD patterns -- see [skill:dotnet-gha-patterns] and [skill:dotnet-ado-patterns]
- DI container mechanics -- see [skill:dotnet-csharp-dependency-injection]
- General coding standards -- see [skill:dotnet-csharp-coding-standards]
- CLI packaging for Homebrew, apt, winget -- see [skill:dotnet-cli-packaging]

Cross-references: [skill:dotnet-cli-architecture] for CLI design patterns, [skill:dotnet-native-aot] for AOT publishing CLI tools, [skill:dotnet-csharp-dependency-injection] for DI fundamentals, [skill:dotnet-csharp-configuration] for configuration integration, [skill:dotnet-csharp-coding-standards] for naming and style conventions.

---

## Package Reference

```xml
<ItemGroup>
  <PackageReference Include="System.CommandLine" Version="2.0.*" />
</ItemGroup>
```

System.CommandLine 2.0 targets .NET 8+ and .NET Standard 2.0. A single package provides all functionality -- the separate `System.CommandLine.Hosting`, `System.CommandLine.NamingConventionBinder`, and `System.CommandLine.Rendering` packages from the beta era are discontinued.

---

## RootCommand and Command Hierarchy

### Basic Command Structure

```csharp
using System.CommandLine;

// Root command -- the entry point
var rootCommand = new RootCommand("My CLI tool description");

// Add a subcommand via mutable collection
var listCommand = new Command("list", "List all items");
rootCommand.Subcommands.Add(listCommand);

// Nested subcommands: mycli migrate up
var migrateCommand = new Command("migrate", "Database migrations");
var upCommand = new Command("up", "Apply pending migrations");
var downCommand = new Command("down", "Revert last migration");
migrateCommand.Subcommands.Add(upCommand);
migrateCommand.Subcommands.Add(downCommand);
rootCommand.Subcommands.Add(migrateCommand);
```

### Collection Initializer Syntax

```csharp
// Fluent collection initializer (commands, options, arguments)
RootCommand rootCommand = new("My CLI tool")
{
    new Option<string>("--output", "-o") { Description = "Output file path" },
    new Argument<FileInfo>("file") { Description = "Input file" },
    new Command("list", "List all items")
    {
        new Option<int>("--limit") { Description = "Max items to return" }
    }
};
```

---

## Options and Arguments

### Option\<T\> -- Named Parameters

```csharp
// Option<T> -- named parameter (--output, -o)
// name is the first parameter; additional params are aliases
var outputOption = new Option<FileInfo>("--output", "-o")
{
    Description = "Output file path",
    Required = true  // was IsRequired in beta4
};

// Option with default value via DefaultValueFactory
var verbosityOption = new Option<int>("--verbosity")
{
    Description = "Verbosity level (0-3)",
    DefaultValueFactory = _ => 1
};
```

### Argument\<T\> -- Positional Parameters

```csharp
// Argument<T> -- positional parameter
// name is mandatory in 2.0 (used for help text)
var fileArgument = new Argument<FileInfo>("file")
{
    Description = "Input file to process"
};

rootCommand.Arguments.Add(fileArgument);
```

### Constrained Values

```csharp
var formatOption = new Option<string>("--format")
{
    Description = "Output format"
};
formatOption.AcceptOnlyFromAmong("json", "csv", "table");

rootCommand.Options.Add(formatOption);
```

### Aliases

```csharp
// Aliases are separate from the name in 2.0
// First constructor param is the name; rest are aliases
var verboseOption = new Option<bool>("--verbose", "-v")
{
    Description = "Enable verbose output"
};

// Or add aliases after construction
verboseOption.Aliases.Add("-V");
```

### Global Options

```csharp
// Global options are inherited by all subcommands
var debugOption = new Option<bool>("--debug")
{
    Description = "Enable debug mode",
    Recursive = true  // makes it global (inherited by subcommands)
};
rootCommand.Options.Add(debugOption);
```

---

## Setting Actions (Command Handlers)

In 2.0.0 GA, `SetHandler` is replaced by `SetAction`. Actions receive a `ParseResult` directly (no `InvocationContext`).

### Synchronous Action

```csharp
var outputOption = new Option<FileInfo>("--output", "-o")
{
    Description = "Output file path",
    Required = true
};
var verbosityOption = new Option<int>("--verbosity")
{
    DefaultValueFactory = _ => 1
};

rootCommand.Options.Add(outputOption);
rootCommand.Options.Add(verbosityOption);

rootCommand.SetAction(parseResult =>
{
    var output = parseResult.GetValue(outputOption)!;
    var verbosity = parseResult.GetValue(verbosityOption);
    Console.WriteLine($"Output: {output.FullName}, Verbosity: {verbosity}");
    return 0; // exit code
});
```

### Asynchronous Action with CancellationToken

```csharp
// Async actions receive ParseResult AND CancellationToken
rootCommand.SetAction(async (ParseResult parseResult, CancellationToken ct) =>
{
    var output = parseResult.GetValue(outputOption)!;
    var verbosity = parseResult.GetValue(verbosityOption);
    await ProcessAsync(output, verbosity, ct);
    return 0;
});
```

### Getting Values by Name

```csharp
// Values can also be retrieved by symbol name (requires type parameter)
rootCommand.SetAction(parseResult =>
{
    int delay = parseResult.GetValue<int>("--delay");
    string? message = parseResult.GetValue<string>("--message");
    Console.WriteLine($"Delay: {delay}, Message: {message}");
});
```

### Parsing and Invoking

```csharp
// Program.cs entry point -- parse then invoke
static int Main(string[] args)
{
    var rootCommand = BuildCommand();
    ParseResult parseResult = rootCommand.Parse(args);
    return parseResult.Invoke();
}

// Async entry point
static async Task<int> Main(string[] args)
{
    var rootCommand = BuildCommand();
    ParseResult parseResult = rootCommand.Parse(args);
    return await parseResult.InvokeAsync();
}
```

### Parse Without Invoking

```csharp
// Parse-only mode: inspect results without running actions
ParseResult parseResult = rootCommand.Parse(args);
if (parseResult.Errors.Count > 0)
{
    foreach (var error in parseResult.Errors)
    {
        Console.Error.WriteLine(error.Message);
    }
    return 1;
}

FileInfo? file = parseResult.GetValue(fileOption);
// Process directly without SetAction
```

---


For detailed examples (custom parsing, validation, configuration, tab completion, DI, testing, migration), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Do not use beta4 API patterns.** The 2.0.0 GA API is fundamentally different. There is no `SetHandler` -- use `SetAction`. There is no `InvocationContext` -- actions receive `ParseResult` directly. There is no `CommandLineBuilder` -- configuration uses `ParserConfiguration`/`InvocationConfiguration`.
2. **Do not reference discontinued packages.** `System.CommandLine.Hosting`, `System.CommandLine.NamingConventionBinder`, and `System.CommandLine.Rendering` are discontinued. Use the single `System.CommandLine` package.
3. **Do not confuse `Option<T>` with `Argument<T>`.** Options are named (`--output file.txt`), arguments are positional (`mycli file.txt`). Using the wrong type produces confusing parse errors.
4. **Do not use `AddOption`/`AddCommand`/`AddAlias` methods.** These were replaced by mutable collection properties: `Options.Add`, `Subcommands.Add`, `Aliases.Add`. The old methods do not exist in 2.0.0.
5. **Do not use `IConsole` or `TestConsole` for testing.** These interfaces were removed. Use `InvocationConfiguration` with `StringWriter` for `Output`/`Error` to capture test output.
6. **Do not ignore the `CancellationToken` in async actions.** In 2.0.0 GA, `CancellationToken` is a mandatory second parameter for async `SetAction` delegates. The compiler warns (CA2016) when it is not propagated.
7. **Do not write `Console.Out` directly in command actions.** Write to `InvocationConfiguration.Output` for testability. If no configuration is provided, output goes to `Console.Out` by default, but direct writes bypass test capture.
8. **Do not set default values via constructors.** Use the `DefaultValueFactory` property instead. The old `getDefaultValue` constructor parameter does not exist in 2.0.0.

---

## References

- [System.CommandLine overview](https://learn.microsoft.com/en-us/dotnet/standard/commandline/)
- [System.CommandLine migration guide (beta5+)](https://learn.microsoft.com/en-us/dotnet/standard/commandline/migration-guide-2.0.0-beta5)
- [How to parse and invoke](https://learn.microsoft.com/en-us/dotnet/standard/commandline/how-to-parse-and-invoke)
- [How to customize parsing and validation](https://learn.microsoft.com/en-us/dotnet/standard/commandline/how-to-customize-parsing-and-validation)
- [System.CommandLine GitHub](https://github.com/dotnet/command-line-api)

---

## Attribution

Adapted from [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) (MIT license).
