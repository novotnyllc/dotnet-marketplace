---
name: dotnet-roslyn-analyzers
description: Authors Roslyn analyzers. DiagnosticAnalyzer, CodeFixProvider, CodeRefactoring, multi-version.
license: MIT
user-invocable: false
---

# dotnet-roslyn-analyzers

Guidance for **authoring** custom Roslyn analyzers, code fix providers, code refactoring providers, and diagnostic suppressors. Covers project setup, DiagnosticDescriptor conventions, analysis context registration, code fix actions, code refactoring actions, multi-Roslyn-version targeting (3.8 through 4.14), testing with Microsoft.CodeAnalysis.Testing, NuGet packaging, and performance best practices.

For extended code examples (CodeRefactoringProvider implementation, multi-version project structure, test matrix configuration), see `details.md` in this skill directory.

## Scope

- DiagnosticAnalyzer authoring and analysis context registration
- CodeFixProvider and CodeRefactoringProvider implementation
- Multi-Roslyn-version targeting (3.8 through 4.14)
- Testing with Microsoft.CodeAnalysis.Testing
- NuGet packaging for analyzer assemblies

## Out of scope

- Consuming and configuring existing analyzers (CA rules, severity) -- see [skill:dotnet-add-analyzers]
- Authoring source generators (IIncrementalGenerator) -- see [skill:dotnet-csharp-source-generators]
- Naming conventions -- see [skill:dotnet-csharp-coding-standards]

Cross-references: [skill:dotnet-csharp-source-generators] for shared Roslyn packaging concepts and IIncrementalGenerator patterns, [skill:dotnet-add-analyzers] for consuming and configuring analyzers, [skill:dotnet-testing-strategy] for general test organization and framework selection, [skill:dotnet-csharp-coding-standards] for naming conventions applied to analyzer code.

---

## Project Setup

Analyzer projects **must** target `netstandard2.0`. The compiler loads analyzers into various host processes (Visual Studio on .NET Framework/Mono, MSBuild on .NET Core, `dotnet build` CLI) -- targeting `net8.0+` breaks compatibility with hosts that do not run on that runtime.

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <EnforceExtendedAnalyzerRules>true</EnforceExtendedAnalyzerRules>
    <IsRoslynComponent>true</IsRoslynComponent>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.12.0" PrivateAssets="all" />
    <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.11.0" PrivateAssets="all" />
  </ItemGroup>
</Project>
```

- `EnforceExtendedAnalyzerRules` enables RS-series meta-diagnostics that catch common analyzer authoring mistakes.
- `IsRoslynComponent` enables IDE tooling support for the project.
- `LangVersion>latest` lets you write modern C# in the analyzer itself while still targeting `netstandard2.0`.
- All Roslyn SDK packages must use `PrivateAssets="all"` to avoid shipping them as transitive dependencies.

---

## DiagnosticAnalyzer

Every analyzer inherits from `DiagnosticAnalyzer` and must be decorated with `[DiagnosticAnalyzer(LanguageNames.CSharp)]`.

```csharp
[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class NoPublicFieldsAnalyzer : DiagnosticAnalyzer
{
    public const string DiagnosticId = "MYLIB001";

    private static readonly DiagnosticDescriptor Rule = new(
        id: DiagnosticId,
        title: "Public fields should be properties",
        messageFormat: "Field '{0}' is public; use a property instead",
        category: "Design",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        helpLinkUri: $"https://example.com/docs/rules/{DiagnosticId}");

    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics { get; }
        = ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        context.EnableConcurrentExecution();
        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
        context.RegisterSymbolAction(AnalyzeField, SymbolKind.Field);
    }

    private static void AnalyzeField(SymbolAnalysisContext context)
    {
        var field = (IFieldSymbol)context.Symbol;
        if (field.DeclaredAccessibility == Accessibility.Public
            && !field.IsConst && !field.IsReadOnly)
        {
            context.ReportDiagnostic(Diagnostic.Create(Rule, field.Locations[0], field.Name));
        }
    }
}
```

### Analysis Context Registration

| Method | Granularity | Use When |
|--------|-------------|----------|
| `RegisterSyntaxNodeAction` | Individual syntax nodes | Pattern matching on specific syntax |
| `RegisterSymbolAction` | Declared symbols | Checking symbol-level properties |
| `RegisterOperationAction` | IL-level operations | Analyzing semantic operations |
| `RegisterSyntaxTreeAction` | Entire syntax tree | File-level checks |
| `RegisterCompilationStartAction` | Compilation start | Accumulate state across compilation |
| `RegisterCompilationAction` | Full compilation | One-shot analysis after all files |

---

## DiagnosticDescriptor Conventions

### ID Prefix Patterns

| Pattern | Example | When |
|---------|---------|------|
| `PROJ###` | `MYLIB001` | Single-project analyzers |
| `AREA####` | `PERF0001` | Category-scoped analyzers |
| `XX####` | `MA0042` | Short-prefix convention |

Avoid prefixes reserved by the .NET platform: `CA`, `CS`, `RS`, `IDE`, `IL`, `SYSLIB`.

### Severity Selection

| Severity | Use When |
|----------|----------|
| `Error` | Code will not work correctly at runtime |
| `Warning` | Code works but violates best practices |
| `Info` | Suggestion for improvement |
| `Hidden` | IDE-only refactoring suggestion |

Default to `Warning` for most rules. Always provide a non-null `helpLinkUri` (RS1015 enforces this).

---

## CodeFixProvider

Code fix providers offer automated corrections for diagnostics. Key patterns:

- **EquivalenceKey:** Every `CodeAction` must have a unique `equivalenceKey` for FixAll support (RS1010, RS1011)
- **Document vs. Solution modification:** Use `createChangedDocument` for single-file fixes, `createChangedSolution` for cross-file renames
- **Trivia preservation:** Always transfer leading/trailing trivia from replaced nodes
- **FixAllProvider:** Return `WellKnownFixAllProviders.BatchFixer` for batch-applicable fixes

See `details.md` for the complete CodeFixProvider implementation with property conversion.

---

## DiagnosticSuppressor

Conditionally suppresses diagnostics from other analyzers when EditorConfig cannot express the suppression condition. Requires Roslyn 3.8+.

| Approach | Use When |
|----------|----------|
| EditorConfig severity override | Suppression applies unconditionally |
| `[SuppressMessage]` attribute | Suppression applies to a specific location |
| `DiagnosticSuppressor` | Suppression depends on code structure or patterns |

---

## Multi-Roslyn-Version Targeting

### Version Boundaries

| Roslyn Version | Ships With | Key APIs Added |
|---------------|------------|----------------|
| 3.8 | VS 16.8 / .NET 5 SDK | `DiagnosticSuppressor` |
| 4.2 | VS 17.2 / .NET 6 SDK | Improved incremental analysis |
| 4.4 | VS 17.4 / .NET 7 SDK | `ForAttributeWithMetadataName` |
| 4.8 | VS 17.8 / .NET 8 U1 | `CollectionExpression` support |
| 4.14 | VS 17.14 / .NET 10 SDK | Latest API surface |

Use conditional compilation constants (`ROSLYN_X_Y_OR_GREATER`) and version-specific NuGet paths (`analyzers/dotnet/roslyn{version}/cs/`). See `details.md` for the complete multi-version project structure.

---

## Testing Analyzers

Use `Microsoft.CodeAnalysis.Testing` for ergonomic analyzer testing:

```csharp
using Verify = Microsoft.CodeAnalysis.CSharp.Testing.CSharpAnalyzerVerifier<
    NoPublicFieldsAnalyzer,
    Microsoft.CodeAnalysis.Testing.DefaultVerifier>;

public class NoPublicFieldsAnalyzerTests
{
    [Fact]
    public async Task PublicField_ReportsDiagnostic()
    {
        var test = """
            public class MyClass
            {
                public int {|MYLIB001:Value|};
            }
            """;
        await Verify.VerifyAnalyzerAsync(test);
    }
}
```

### Diagnostic Markup Syntax

| Markup | Meaning |
|--------|---------|
| `[|text|]` | Diagnostic expected on `text` (single descriptor) |
| `{|DIAG_ID:text|}` | Diagnostic with specific ID expected |

---

## NuGet Packaging

Analyzers ship as NuGet packages with assemblies in `analyzers/dotnet/cs/`, not `lib/`.

```xml
<PropertyGroup>
  <IncludeBuildOutput>false</IncludeBuildOutput>
  <DevelopmentDependency>true</DevelopmentDependency>
  <SuppressDependenciesWhenPacking>true</SuppressDependenciesWhenPacking>
</PropertyGroup>

<ItemGroup>
  <None Include="$(OutputPath)\$(AssemblyName).dll"
        Pack="true"
        PackagePath="analyzers/dotnet/cs" />
</ItemGroup>
```

---

## Performance Best Practices

- **Resolve types once per compilation** inside `RegisterCompilationStartAction`, not per-node/symbol callbacks
- **Cache `SupportedDiagnostics`** as `ImmutableArray` field, not expression-bodied property
- **Enable concurrent execution** -- always call `context.EnableConcurrentExecution()`
- **Filter early** -- register for the most specific `SyntaxKind` possible
- **Avoid `Compilation.GetSemanticModel()`** -- use the `SemanticModel` from the analysis context (RS1030)

---

## Common Meta-Diagnostics (RS-Series)

| ID | Title | What It Catches |
|----|-------|-----------------|
| RS1001 | Missing `DiagnosticAnalyzerAttribute` | Analyzer class missing attribute |
| RS1008 | Avoid storing per-compilation data | Instance fields with compilation data |
| RS1010 | Create code actions with unique `EquivalenceKey` | Missing equivalence key |
| RS1015 | Provide non-null `helpLinkUri` | Empty help link |
| RS1016 | Code fix providers should provide FixAll support | Missing `GetFixAllProvider()` |
| RS1024 | Symbols should be compared for equality | Using `==` instead of `SymbolEqualityComparer` |
| RS1026 | Enable concurrent execution | Missing `EnableConcurrentExecution()` |
| RS1030 | Do not invoke `Compilation.GetSemanticModel()` | Using wrong semantic model source |
| RS1041 | Compiler extensions should target `netstandard2.0` | Wrong target framework |

---

## References

- [Tutorial: Write your first analyzer and code fix](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix)
- [Roslyn SDK overview](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/)
- [Microsoft.CodeAnalysis.Testing](https://github.com/dotnet/roslyn-sdk/tree/main/src/Microsoft.CodeAnalysis.Testing)
- [Analyzer NuGet packaging conventions](https://learn.microsoft.com/en-us/nuget/guides/analyzers-conventions)
- [dotnet/roslyn-analyzers (RS diagnostic source)](https://github.com/dotnet/roslyn-analyzers)
- [Meziantou.Analyzer (exemplar project)](https://github.com/meziantou/Meziantou.Analyzer)
