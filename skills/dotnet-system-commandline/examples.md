# dotnet-system-commandline -- Detailed Examples

Extended code examples for custom type parsing, validation, configuration, tab completion, DI integration, testing, response files, and migration from beta4.

---

## Custom Type Parsing

### CustomParser Property

For types without built-in parsers, use the `CustomParser` property on `Option<T>` or `Argument<T>`.

```csharp
public record ConnectionInfo(string Host, int Port);

var connectionOption = new Option<ConnectionInfo?>("--connection")
{
    Description = "Connection as host:port",
    CustomParser = result =>
    {
        var raw = result.Tokens.SingleOrDefault()?.Value;
        if (raw is null)
        {
            result.AddError("--connection requires a value");
            return null;
        }

        var parts = raw.Split(':');
        if (parts.Length != 2 || !int.TryParse(parts[1], out var port))
        {
            result.AddError("Expected format: host:port");
            return null;
        }

        return new ConnectionInfo(parts[0], port);
    }
};
```

### DefaultValueFactory

```csharp
var portOption = new Option<int>("--port")
{
    Description = "Server port",
    DefaultValueFactory = _ => 8080  // type-safe default
};
```

### Combining CustomParser with Validation

```csharp
var uriOption = new Option<Uri?>("--uri")
{
    Description = "Target URI",
    CustomParser = result =>
    {
        var raw = result.Tokens.SingleOrDefault()?.Value;
        if (raw is null) return null;

        if (!Uri.TryCreate(raw, UriKind.Absolute, out var uri))
        {
            result.AddError("Invalid URI format");
            return null;
        }

        if (uri.Scheme != "https")
        {
            result.AddError("Only HTTPS URIs are accepted");
            return null;
        }

        return uri;
    }
};
```

---

## Validation

### Option and Argument Validators

```csharp
// Validators use Validators.Add (not AddValidator in 2.0)
var portOption = new Option<int>("--port") { Description = "Port number" };
portOption.Validators.Add(result =>
{
    var value = result.GetValue(portOption);
    if (value < 1 || value > 65535)
    {
        result.AddError("Port must be between 1 and 65535");
    }
});

// Arity constraints
var tagsOption = new Option<string[]>("--tag")
{
    Arity = new ArgumentArity(1, 5),  // 1 to 5 tags
    AllowMultipleArgumentsPerToken = true
};
```

### Built-In Validators

```csharp
// Accept only existing files/directories
var inputOption = new Option<FileInfo>("--input");
inputOption.AcceptExistingOnly();

// Accept only legal file names
var nameArg = new Argument<string>("name");
nameArg.AcceptLegalFileNamesOnly();

// Accept only from a set of values (moved from FromAmong)
var envOption = new Option<string>("--env");
envOption.AcceptOnlyFromAmong("dev", "staging", "prod");
```

---

## Configuration

In 2.0.0 GA, `CommandLineBuilder` is removed. Configuration uses `ParserConfiguration` (for parsing) and `InvocationConfiguration` (for invocation).

### Parser Configuration

```csharp
using System.CommandLine;

var config = new ParserConfiguration
{
    EnablePosixBundling = true,  // -abc == -a -b -c (default: true)
};

// Response files enabled by default; disable with:
// config.ResponseFileTokenReplacer = null;

ParseResult parseResult = rootCommand.Parse(args, config);
```

### Invocation Configuration

```csharp
var invocationConfig = new InvocationConfiguration
{
    // Redirect output for testing or customization
    Output = Console.Out,
    Error = Console.Error,

    // Process termination handling (default: 2 seconds)
    ProcessTerminationTimeout = TimeSpan.FromSeconds(5),

    // Disable default exception handler for custom try/catch
    EnableDefaultExceptionHandler = false
};

int exitCode = parseResult.Invoke(invocationConfig);
```

---

## Tab Completion

### Enabling Completion

Tab completion is built into RootCommand via the SuggestDirective (included by default).

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

### Custom Completions

```csharp
// Static completions
var envOption = new Option<string>("--environment");
envOption.CompletionSources.Add("development", "staging", "production");

// Dynamic completions
var branchOption = new Option<string>("--branch");
branchOption.CompletionSources.Add(ctx =>
[
    new CompletionItem("main"),
    new CompletionItem("develop"),
    // Dynamically fetch branches
    .. GetGitBranches().Select(b => new CompletionItem(b))
]);
```

---

## Automatic --version and --help

### Version

`--version` is automatically available on RootCommand via `VersionOption`. It reads from:
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

### Help

Help is automatically provided via `HelpOption` on RootCommand. Descriptions from constructors and `Description` properties flow into help text.

---

## Directives

Directives replace some beta-era `CommandLineBuilder` extensions. RootCommand exposes a `Directives` collection.

```csharp
// Built-in directives (included by default on RootCommand):
// [suggest] -- tab completion suggestions
// Other available directives:
rootCommand.Directives.Add(new DiagramDirective());           // [diagram] -- shows parse tree
rootCommand.Directives.Add(new EnvironmentVariablesDirective()); // [env:VAR=value]
```

### Parse Error Handling

```csharp
// Customize parse error behavior
ParseResult result = rootCommand.Parse(args);
if (result.Action is ParseErrorAction parseError)
{
    parseError.ShowTypoCorrections = true;
    parseError.ShowHelp = false;
}
int exitCode = result.Invoke();
```

---

## Dependency Injection Pattern

The `System.CommandLine.Hosting` package is discontinued in 2.0.0 GA. For DI integration, use `Microsoft.Extensions.Hosting` directly and compose services before parsing.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.CommandLine;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices(services =>
    {
        services.AddSingleton<ISyncService, SyncService>();
        services.AddSingleton<IFileSystem, PhysicalFileSystem>();
    })
    .Build();

var serviceProvider = host.Services;

var sourceOption = new Option<string>("--source") { Description = "Source endpoint" };
var syncCommand = new Command("sync", "Synchronize data");
syncCommand.Options.Add(sourceOption);

syncCommand.SetAction(async (ParseResult parseResult, CancellationToken ct) =>
{
    var syncService = serviceProvider.GetRequiredService<ISyncService>();
    var source = parseResult.GetValue(sourceOption);
    await syncService.SyncAsync(source!, ct);
    return 0;
});

var rootCommand = new RootCommand("My CLI tool");
rootCommand.Subcommands.Add(syncCommand);

return await rootCommand.Parse(args).InvokeAsync();
```

---

## Testing

### Testing with InvocationConfiguration (TextWriter Capture)

`IConsole` is removed in 2.0.0 GA. For testing, redirect output via `InvocationConfiguration`.

```csharp
[Fact]
public void ListCommand_WritesItems_ToOutput()
{
    // Arrange
    var outputWriter = new StringWriter();
    var errorWriter = new StringWriter();
    var config = new InvocationConfiguration
    {
        Output = outputWriter,
        Error = errorWriter
    };

    var rootCommand = BuildRootCommand();

    // Act
    ParseResult parseResult = rootCommand.Parse("list --format json");
    int exitCode = parseResult.Invoke(config);

    // Assert
    Assert.Equal(0, exitCode);
    Assert.Contains("json", outputWriter.ToString());
    Assert.Empty(errorWriter.ToString());
}
```

### Testing Parsed Values Without Invocation

```csharp
[Fact]
public void ParseResult_ExtractsOptionValues()
{
    var portOption = new Option<int>("--port") { DefaultValueFactory = _ => 8080 };
    var rootCommand = new RootCommand { portOption };

    ParseResult result = rootCommand.Parse("--port 3000");

    Assert.Equal(3000, result.GetValue(portOption));
    Assert.Empty(result.Errors);
}

[Fact]
public void ParseResult_ReportsErrors_ForInvalidInput()
{
    var portOption = new Option<int>("--port");
    var rootCommand = new RootCommand { portOption };

    ParseResult result = rootCommand.Parse("--port not-a-number");

    Assert.NotEmpty(result.Errors);
}
```

### Testing Custom Parsers

```csharp
[Fact]
public void CustomParser_ParsesConnectionInfo()
{
    var connOption = new Option<ConnectionInfo?>("--connection")
    {
        CustomParser = result =>
        {
            var parts = result.Tokens.Single().Value.Split(':');
            return new ConnectionInfo(parts[0], int.Parse(parts[1]));
        }
    };
    var rootCommand = new RootCommand { connOption };

    ParseResult result = rootCommand.Parse("--connection localhost:5432");

    var conn = result.GetValue(connOption);
    Assert.Equal("localhost", conn!.Host);
    Assert.Equal(5432, conn.Port);
}
```

### Testing with DI Services

```csharp
[Fact]
public async Task SyncCommand_CallsService()
{
    var mockService = new Mock<ISyncService>();
    var services = new ServiceCollection()
        .AddSingleton(mockService.Object)
        .BuildServiceProvider();

    var sourceOption = new Option<string>("--source");
    var syncCommand = new Command("sync") { sourceOption };
    syncCommand.SetAction(async (ParseResult pr, CancellationToken ct) =>
    {
        var svc = services.GetRequiredService<ISyncService>();
        await svc.SyncAsync(pr.GetValue(sourceOption)!, ct);
        return 0;
    });

    var root = new RootCommand { syncCommand };
    int exitCode = await root.Parse("sync --source https://api.example.com")
        .InvokeAsync();

    Assert.Equal(0, exitCode);
    mockService.Verify(s => s.SyncAsync("https://api.example.com",
        It.IsAny<CancellationToken>()), Times.Once);
}
```

---

## Response Files

System.CommandLine supports response files (`@filename`) for passing large sets of arguments. Response file support is enabled by default; disable via `ParserConfiguration.ResponseFileTokenReplacer = null`.

```bash
# args.rsp
--source https://api.example.com
--output /tmp/results.json
--verbose

# Invoke with response file
mycli sync @args.rsp
```

---

## Migration from Beta4 to 2.0.0 GA

| Beta4 API | 2.0.0 GA Replacement |
|---|---|
| `command.SetHandler(...)` | `command.SetAction(...)` |
| `command.AddOption(opt)` | `command.Options.Add(opt)` |
| `command.AddCommand(sub)` | `command.Subcommands.Add(sub)` |
| `command.AddArgument(arg)` | `command.Arguments.Add(arg)` |
| `option.AddAlias("-x")` | `option.Aliases.Add("-x")` |
| `option.AddValidator(...)` | `option.Validators.Add(...)` |
| `option.IsRequired = true` | `option.Required = true` |
| `option.IsHidden = true` | `option.Hidden = true` |
| `InvocationContext context` | `ParseResult parseResult` (in SetAction) |
| `context.GetCancellationToken()` | `CancellationToken ct` (second param in async SetAction) |
| `context.Console` | `InvocationConfiguration.Output / .Error` |
| `IConsole` / `TestConsole` | `StringWriter` via `InvocationConfiguration` |
| `new CommandLineBuilder(root).UseDefaults().Build()` | `root.Parse(args)` (middleware built-in) |
| `builder.AddMiddleware(...)` | Removed -- use `ParseResult.Action` inspection or wrap `Invoke` |
| `CommandLineBuilder` | `ParserConfiguration` + `InvocationConfiguration` |
| `UseCommandHandler<T,T>` (Hosting) | Build host directly, resolve services in SetAction |
| `Parser` class | `CommandLineParser` (static class) |
| `FindResultFor(symbol)` | `GetResult(symbol)` |
| `ErrorMessage = "..."` | `result.AddError("...")` |
| `getDefaultValue: () => val` | `DefaultValueFactory = _ => val` |
| `ParseArgument<T>` delegate | `CustomParser` property |

---
