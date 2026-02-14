---
name: dotnet-roslyn-analyzers
description: "WHEN authoring custom Roslyn analyzers. DiagnosticAnalyzer, CodeFixProvider, DiagnosticSuppressor, testing, packaging."
---

# dotnet-roslyn-analyzers

Guidance for **authoring** custom Roslyn analyzers, code fix providers, and diagnostic suppressors. Covers project setup, DiagnosticDescriptor conventions, analysis context registration, code fix actions, testing with Microsoft.CodeAnalysis.Testing, NuGet packaging, and performance best practices.

**Scope boundary:** This skill covers *writing* analyzers. For *consuming and configuring* existing analyzers (CA rules, EditorConfig severity, third-party packages), see [skill:dotnet-add-analyzers]. For *authoring source generators* (IIncrementalGenerator, syntax providers, code emission), see [skill:dotnet-csharp-source-generators]. Analyzers and source generators share the same NuGet packaging layout (`analyzers/dotnet/cs/`) and `Microsoft.CodeAnalysis.CSharp` dependency, but serve different purposes: analyzers report diagnostics, generators emit code.

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
    <!-- NuGet: Microsoft.CodeAnalysis.CSharp -->
    <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.12.0" PrivateAssets="all" />
    <!-- NuGet: Microsoft.CodeAnalysis.Analyzers (meta-diagnostics for analyzer authors) -->
    <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.3.4" PrivateAssets="all" />
  </ItemGroup>
</Project>
```

- `EnforceExtendedAnalyzerRules` enables RS-series meta-diagnostics that catch common analyzer authoring mistakes (see Meta-Diagnostics section below).
- `IsRoslynComponent` enables IDE tooling support for the project.
- `LangVersion>latest` lets you write modern C# in the analyzer itself while still targeting `netstandard2.0`.
- All Roslyn SDK packages must use `PrivateAssets="all"` to avoid shipping them as transitive dependencies.

---

## DiagnosticAnalyzer

Every analyzer inherits from `DiagnosticAnalyzer` and must be decorated with `[DiagnosticAnalyzer(LanguageNames.CSharp)]`.

```csharp
using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Diagnostics;

[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class NoPublicFieldsAnalyzer : DiagnosticAnalyzer
{
    // Diagnostic ID uses project prefix + sequential number
    public const string DiagnosticId = "MYLIB001";

    private static readonly DiagnosticDescriptor Rule = new(
        id: DiagnosticId,
        title: "Public fields should be properties",
        messageFormat: "Field '{0}' is public; use a property instead",
        category: "Design",
        defaultSeverity: DiagnosticSeverity.Warning,
        isEnabledByDefault: true,
        helpLinkUri: $"https://example.com/docs/rules/{DiagnosticId}");

    // Return an ImmutableArray -- allocating a new array per call is RS1030-adjacent waste
    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics { get; }
        = ImmutableArray.Create(Rule);

    public override void Initialize(AnalysisContext context)
    {
        // Required: enable concurrent execution and generated code analysis config
        context.EnableConcurrentExecution();
        context.ConfigureGeneratedCodeAnalysis(
            GeneratedCodeAnalysisFlags.None);

        context.RegisterSymbolAction(AnalyzeField, SymbolKind.Field);
    }

    private static void AnalyzeField(SymbolAnalysisContext context)
    {
        var field = (IFieldSymbol)context.Symbol;

        if (field.DeclaredAccessibility == Accessibility.Public
            && !field.IsConst
            && !field.IsReadOnly)
        {
            var diagnostic = Diagnostic.Create(
                Rule,
                field.Locations[0],
                field.Name);

            context.ReportDiagnostic(diagnostic);
        }
    }
}
```

### Analysis Context Registration

Choose the most appropriate registration method for your analysis:

| Method | Granularity | Use When |
|--------|-------------|----------|
| `RegisterSyntaxNodeAction` | Individual syntax nodes | Pattern matching on specific syntax (e.g., `if` statements, method declarations) |
| `RegisterSymbolAction` | Declared symbols | Checking symbol-level properties (accessibility, type, attributes) |
| `RegisterOperationAction` | IL-level operations | Analyzing semantic operations (assignments, invocations) independent of syntax |
| `RegisterSyntaxTreeAction` | Entire syntax tree | File-level checks (e.g., missing headers, encoding) |
| `RegisterCompilationStartAction` | Compilation start | When you need to accumulate state across the compilation, then report at end |
| `RegisterCompilationAction` | Full compilation | One-shot analysis after all files are compiled |

```csharp
// RegisterSyntaxNodeAction -- analyze specific syntax nodes
context.RegisterSyntaxNodeAction(
    AnalyzeInvocation,
    SyntaxKind.InvocationExpression);

// RegisterOperationAction -- analyze semantic operations
context.RegisterOperationAction(
    AnalyzeAssignment,
    OperationKind.SimpleAssignment);

// RegisterCompilationStartAction -- accumulate state, then report at compilation end
context.RegisterCompilationStartAction(compilationContext =>
{
    // Resolve types once at compilation start
    var disposableType = compilationContext.Compilation
        .GetTypeByMetadataName("System.IDisposable");

    if (disposableType is null)
        return;

    compilationContext.RegisterSymbolAction(
        ctx => AnalyzeTypeDisposal(ctx, disposableType),
        SymbolKind.NamedType);
});
```

---

## DiagnosticDescriptor Conventions

fn-27 is the canonical owner of DiagnosticDescriptor guidance. Follow these conventions for all custom analyzers:

### ID Prefix Patterns

Use a short, unique prefix derived from your project or library name, followed by a sequential number:

| Pattern | Example | When |
|---------|---------|------|
| `PROJ###` | `MYLIB001` | Single-project analyzers |
| `AREA####` | `PERF0001` | Category-scoped analyzers (performance, security) |
| `XX####` | `MA0042` | Short-prefix convention (e.g., Meziantou.Analyzer) |

Avoid prefixes reserved by the .NET platform: `CA` (code analysis), `CS` (compiler), `RS` (Roslyn SDK), `IDE` (code style), `IL` (linker), `SYSLIB` (runtime). Include the namespace in the ID constant to prevent collisions when multiple analyzer packages are installed.

### Category Naming

Use standard .NET analysis categories where applicable:

`Design`, `Globalization`, `Interoperability`, `Maintainability`, `Naming`, `Performance`, `Reliability`, `Security`, `Style`, `Usage`

For domain-specific categories, use a clear, titlecase name (e.g., `EntityFramework`, `AspNetCore`).

### Severity Selection

| Severity | Use When |
|----------|----------|
| `Error` | Code will not work correctly at runtime (null deref, SQL injection, resource leak) |
| `Warning` | Code works but violates best practices or has performance issues |
| `Info` | Suggestion for improvement, not a defect |
| `Hidden` | IDE-only refactoring suggestion, not shown in build output |

Default to `Warning` for most rules. Use `Error` sparingly -- users cannot suppress errors via EditorConfig without disabling the rule entirely.

### helpLinkUri

Always provide a non-null `helpLinkUri` (RS1015 enforces this). Point to stable documentation:

```csharp
helpLinkUri: $"https://github.com/myorg/mylib/blob/main/docs/rules/{DiagnosticId}.md"
```

---

## CodeFixProvider

Code fix providers offer automated corrections for diagnostics. They inherit from `CodeFixProvider` and register fixes for specific diagnostic IDs.

```csharp
using System.Collections.Immutable;
using System.Composition;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CodeActions;
using Microsoft.CodeAnalysis.CodeFixes;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

[ExportCodeFixProvider(LanguageNames.CSharp, Name = nameof(NoPublicFieldsCodeFixProvider))]
[Shared]
public sealed class NoPublicFieldsCodeFixProvider : CodeFixProvider
{
    public override ImmutableArray<string> FixableDiagnosticIds { get; }
        = ImmutableArray.Create(NoPublicFieldsAnalyzer.DiagnosticId);

    // Enable FixAll support -- RS1016 flags missing FixAllProvider
    public override FixAllProvider GetFixAllProvider()
        => WellKnownFixAllProviders.BatchFixer;

    public override async Task RegisterCodeFixesAsync(CodeFixContext context)
    {
        var root = await context.Document
            .GetSyntaxRootAsync(context.CancellationToken)
            .ConfigureAwait(false);

        var diagnostic = context.Diagnostics[0];
        var diagnosticSpan = diagnostic.Location.SourceSpan;

        var fieldDeclaration = root?.FindToken(diagnosticSpan.Start)
            .Parent?
            .AncestorsAndSelf()
            .OfType<FieldDeclarationSyntax>()
            .FirstOrDefault();

        if (fieldDeclaration is null)
            return;

        // EquivalenceKey enables FixAll grouping -- RS1010/RS1011 require unique keys
        context.RegisterCodeFix(
            CodeAction.Create(
                title: "Convert to property",
                createChangedDocument: ct =>
                    ConvertToPropertyAsync(context.Document, fieldDeclaration, ct),
                equivalenceKey: "ConvertToProperty"),
            diagnostic);
    }

    private static async Task<Document> ConvertToPropertyAsync(
        Document document,
        FieldDeclarationSyntax fieldDeclaration,
        CancellationToken cancellationToken)
    {
        var root = await document
            .GetSyntaxRootAsync(cancellationToken)
            .ConfigureAwait(false);

        var variable = fieldDeclaration.Declaration.Variables[0];
        var propertyName = variable.Identifier.Text;

        // Build auto-property with same type and accessibility
        var property = SyntaxFactory.PropertyDeclaration(
                fieldDeclaration.Declaration.Type,
                propertyName)
            .WithModifiers(fieldDeclaration.Modifiers)
            .WithAccessorList(
                SyntaxFactory.AccessorList(
                    SyntaxFactory.List(new[]
                    {
                        SyntaxFactory.AccessorDeclaration(SyntaxKind.GetAccessorDeclaration)
                            .WithSemicolonToken(SyntaxFactory.Token(SyntaxKind.SemicolonToken)),
                        SyntaxFactory.AccessorDeclaration(SyntaxKind.SetAccessorDeclaration)
                            .WithSemicolonToken(SyntaxFactory.Token(SyntaxKind.SemicolonToken))
                    })))
            .WithLeadingTrivia(fieldDeclaration.GetLeadingTrivia())
            .WithTrailingTrivia(fieldDeclaration.GetTrailingTrivia());

        var newRoot = root!.ReplaceNode(fieldDeclaration, property);
        return document.WithSyntaxRoot(newRoot);
    }
}
```

### Key CodeFixProvider Patterns

- **EquivalenceKey:** Every `CodeAction` must have a unique `equivalenceKey` for FixAll support (RS1010, RS1011). Use the fix description or diagnostic ID as the key.
- **Document vs. Solution modification:** Use `createChangedDocument` when the fix modifies a single file. Use `createChangedSolution` when the fix must rename symbols across files or add new files.
- **Trivia preservation:** Always transfer leading/trailing trivia from replaced nodes to maintain formatting and comments.
- **FixAllProvider:** Return `WellKnownFixAllProviders.BatchFixer` for batch-applicable fixes. Omit only for fixes that require user interaction or have cross-fix dependencies.

---

## DiagnosticSuppressor

A `DiagnosticSuppressor` conditionally suppresses diagnostics from other analyzers. Use this when your codebase has a pattern that a third-party analyzer flags incorrectly, and EditorConfig cannot express the suppression condition.

```csharp
using System.Collections.Immutable;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Diagnostics;

[DiagnosticAnalyzer(LanguageNames.CSharp)]
public sealed class CustomNullCheckSuppressor : DiagnosticSuppressor
{
    private static readonly SuppressionDescriptor SuppressCA1062 = new(
        id: "MYLIB_SUP001",
        suppressedDiagnosticId: "CA1062",
        justification: "Parameter is validated by custom Guard.NotNull helper");

    public override ImmutableArray<SuppressionDescriptor> SupportedSuppressions { get; }
        = ImmutableArray.Create(SuppressCA1062);

    public override void ReportSuppressions(SuppressionAnalysisContext context)
    {
        foreach (var diagnostic in context.ReportedDiagnostics)
        {
            var tree = diagnostic.Location.SourceTree;
            if (tree is null)
                continue;

            var root = tree.GetRoot(context.CancellationToken);
            var node = root.FindNode(diagnostic.Location.SourceSpan);

            // Walk up to the containing method and check for Guard.NotNull call
            var method = node.FirstAncestorOrSelf<Microsoft.CodeAnalysis.CSharp.Syntax.MethodDeclarationSyntax>();
            if (method is null)
                continue;

            var methodText = method.ToFullString();

            // Simplified check -- production code should use semantic analysis
            if (methodText.Contains("Guard.NotNull"))
            {
                context.ReportSuppression(
                    Suppression.Create(SuppressCA1062, diagnostic));
            }
        }
    }
}
```

### When to Use DiagnosticSuppressor vs. EditorConfig

| Approach | Use When |
|----------|----------|
| EditorConfig severity override | Suppression applies unconditionally to all instances of a rule |
| `[SuppressMessage]` attribute | Suppression applies to a specific code location with a justification |
| `DiagnosticSuppressor` | Suppression depends on code structure or patterns (e.g., custom validation, code generation markers) |

Suppressors cannot report new diagnostics -- they can only suppress existing ones. They participate in the same analyzer pipeline and follow the same `netstandard2.0` targeting requirements.

---

## Testing Analyzers

Use the `Microsoft.CodeAnalysis.Testing` infrastructure for ergonomic, high-level analyzer testing. This is preferred over raw `CSharpCompilation` testing.

### Required NuGet Packages

```xml
<ItemGroup>
  <!-- NuGet: Microsoft.CodeAnalysis.CSharp.Analyzer.Testing -->
  <PackageReference Include="Microsoft.CodeAnalysis.CSharp.Analyzer.Testing" Version="1.1.2" />
  <!-- NuGet: Microsoft.CodeAnalysis.CSharp.CodeFix.Testing -->
  <PackageReference Include="Microsoft.CodeAnalysis.CSharp.CodeFix.Testing" Version="1.1.2" />
  <!-- NuGet: Microsoft.CodeAnalysis.CSharp.Workspaces (dependency) -->
  <PackageReference Include="Microsoft.CodeAnalysis.CSharp.Workspaces" Version="4.12.0" />
  <!-- NuGet: xunit (test framework) -->
  <PackageReference Include="xunit" Version="2.9.3" />
</ItemGroup>
```

### Analyzer-Only Testing

Use `CSharpAnalyzerVerifier<T>` to test that diagnostics are reported (or not reported) correctly:

```csharp
using Microsoft.CodeAnalysis.Testing;
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

    [Fact]
    public async Task PrivateField_NoDiagnostic()
    {
        var test = """
            public class MyClass
            {
                private int _value;
            }
            """;

        await Verify.VerifyAnalyzerAsync(test);
    }

    [Fact]
    public async Task PublicConstField_NoDiagnostic()
    {
        var test = """
            public class MyClass
            {
                public const int MaxRetries = 3;
            }
            """;

        await Verify.VerifyAnalyzerAsync(test);
    }
}
```

### Diagnostic Markup Syntax

The testing framework uses markup to indicate expected diagnostic locations:

| Markup | Meaning |
|--------|---------|
| `[|text|]` | Diagnostic expected on `text` (use when analyzer has exactly one `DiagnosticDescriptor`) |
| `{|DIAG_ID:text|}` | Diagnostic with specific ID expected on `text` |
| `{|DIAG_ID:text{|OTHER_ID:nested|}more|}` | Multiple overlapping diagnostics |

### Analyzer + CodeFix Testing

Use `CSharpCodeFixVerifier<TAnalyzer, TCodeFix>` to test the full analyzer-to-fix pipeline:

```csharp
using Verify = Microsoft.CodeAnalysis.CSharp.Testing.CSharpCodeFixVerifier<
    NoPublicFieldsAnalyzer,
    NoPublicFieldsCodeFixProvider,
    Microsoft.CodeAnalysis.Testing.DefaultVerifier>;

public class NoPublicFieldsCodeFixTests
{
    [Fact]
    public async Task PublicField_FixConvertsToProperty()
    {
        var test = """
            public class MyClass
            {
                public int {|MYLIB001:Value|};
            }
            """;

        var fixedCode = """
            public class MyClass
            {
                public int Value { get; set; }
            }
            """;

        await Verify.VerifyCodeFixAsync(test, fixedCode);
    }
}
```

### Multi-File Test Scenarios

```csharp
[Fact]
public async Task MultiFile_DiagnosticInSecondFile()
{
    var test = new Verify.Test
    {
        TestState =
        {
            Sources =
            {
                ("Helpers.cs", """
                    public static class Helpers
                    {
                        public static void DoWork() { }
                    }
                    """),
                ("Models.cs", """
                    public class Order
                    {
                        public decimal {|MYLIB001:Total|};
                    }
                    """)
            }
        }
    };

    await test.RunAsync();
}
```

---

## NuGet Packaging

Analyzers are shipped as NuGet packages with a specific directory layout. The assemblies go under `analyzers/dotnet/cs/`, not `lib/`.

### Package Layout

```
MyAnalyzers.nupkg
  analyzers/
    dotnet/
      cs/
        MyAnalyzers.dll           # Analyzer assembly
        MyAnalyzers.CodeFixes.dll # Code fix assembly (optional, separate)
  lib/
    netstandard2.0/
      _._                        # Empty placeholder (no runtime dependency)
```

### Project Configuration

```xml
<!-- Analyzer .csproj -->
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

### Separate Analyzer and Code Fix Assemblies

For multi-analyzer NuGet packages, separating analyzers from code fixes improves IDE load time. The IDE loads code fix assemblies lazily (only when the user requests a fix), while analyzer assemblies load immediately:

```
MyAnalyzers.nupkg
  analyzers/dotnet/cs/
    MyAnalyzers.dll               # Analyzers only -- loaded immediately
    MyAnalyzers.CodeFixes.dll     # Code fixes -- loaded on demand
```

Create two projects: `MyAnalyzers` (analyzers) and `MyAnalyzers.CodeFixes` (fixes that reference the analyzer project). Pack both into the same NuGet package:

```xml
<!-- In the analyzer .csproj -->
<ItemGroup>
  <None Include="$(OutputPath)\$(AssemblyName).dll"
        Pack="true" PackagePath="analyzers/dotnet/cs" />
  <None Include="$(OutputPath)\MyAnalyzers.CodeFixes.dll"
        Pack="true" PackagePath="analyzers/dotnet/cs" />
</ItemGroup>
```

### Pack Verification

After packing, verify the layout:

```bash
dotnet pack -c Release
# Inspect package contents (nupkg is a zip file)
unzip -l ./bin/Release/MyAnalyzers.1.0.0.nupkg | grep analyzers/
# Or use NuGet Package Explorer (GUI) for interactive inspection
```

See [skill:dotnet-csharp-source-generators] for additional shared packaging concepts (the `analyzers/dotnet/cs/` layout is identical for both analyzers and source generators).

---

## Performance Best Practices

Analyzers run in real-time during editing. Poor performance degrades the IDE experience for every user of the analyzer.

### Allocation-Free Callbacks

Avoid allocations in hot-path callbacks. Every `RegisterSyntaxNodeAction` callback runs per-node, potentially thousands of times per keystroke:

```csharp
// BAD: resolves type on every symbol callback (per-symbol overhead)
context.RegisterSymbolAction(symbolCtx =>
{
    // GetTypeByMetadataName is called for EVERY symbol in the compilation
    var disposableType = symbolCtx.Compilation
        .GetTypeByMetadataName("System.IDisposable");
    if (disposableType is null) return;

    Analyze(symbolCtx, disposableType);
}, SymbolKind.NamedType);

// GOOD: resolve state once per compilation, closure allocated once
context.RegisterCompilationStartAction(compilationCtx =>
{
    var importantType = compilationCtx.Compilation
        .GetTypeByMetadataName("System.IDisposable");
    if (importantType is null) return;

    // One closure per compilation -- acceptable cost
    compilationCtx.RegisterSymbolAction(
        symbolCtx => Analyze(symbolCtx, importantType),
        SymbolKind.NamedType);
});
```

> **Note:** A single closure allocated once per compilation inside `RegisterCompilationStartAction` is acceptable. The anti-pattern is resolving types or allocating closures inside per-node or per-symbol callbacks, where the cost multiplies across thousands of invocations.

### Symbol-Based Filtering

Prefer symbol-based analysis over syntax-based analysis when both are viable. Symbol analysis operates on the compiler's resolved model and avoids re-parsing:

```csharp
// Prefer: RegisterSymbolAction for declared-symbol checks
context.RegisterSymbolAction(ctx =>
{
    var method = (IMethodSymbol)ctx.Symbol;
    if (method.ReturnsVoid && method.Parameters.Length == 0) { /* ... */ }
}, SymbolKind.Method);

// Avoid: RegisterSyntaxNodeAction when symbol analysis suffices
// Syntax analysis requires manually resolving types and handling aliases
```

### ImmutableArray for SupportedDiagnostics

Cache `SupportedDiagnostics` as an `ImmutableArray<DiagnosticDescriptor>` field. The runtime calls this property frequently:

```csharp
// GOOD: single allocation, cached
public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics { get; }
    = ImmutableArray.Create(Rule1, Rule2, Rule3);

// BAD: allocates a new array on every access
public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics
    => ImmutableArray.Create(Rule1, Rule2, Rule3);
```

### Additional Performance Guidelines

- **Enable concurrent execution:** Always call `context.EnableConcurrentExecution()` unless your analyzer has shared mutable state (which it should not).
- **Avoid per-compilation state in fields:** Do not store per-compilation data in analyzer instance fields (RS1008). Use `RegisterCompilationStartAction` to scope state to a single compilation.
- **Filter early in syntax predicates:** When using `RegisterSyntaxNodeAction`, register for the most specific `SyntaxKind` possible to minimize callback frequency.
- **Avoid `Compilation.GetSemanticModel()`:** Use the `SemanticModel` provided by the analysis context instead (RS1030).

---

## Common Meta-Diagnostics (RS-Series)

The `Microsoft.CodeAnalysis.Analyzers` package reports RS-series diagnostics on your analyzer code itself. These are invaluable for catching authoring mistakes at compile time. Enable them via `EnforceExtendedAnalyzerRules` in your project file.

### Frequently Encountered RS Diagnostics

| ID | Title | What It Catches |
|----|-------|-----------------|
| RS1001 | Missing `DiagnosticAnalyzerAttribute` | Analyzer class missing `[DiagnosticAnalyzer(LanguageNames.CSharp)]` |
| RS1004 | Recommend adding language support | Analyzer supports C# but not VB (informational) |
| RS1007 | Provide localizable arguments | DiagnosticDescriptor strings should use `LocalizableResourceString` |
| RS1008 | Avoid storing per-compilation data | Instance fields holding compilation-specific data break concurrent execution |
| RS1010 | Create code actions with unique `EquivalenceKey` | CodeAction missing equivalence key for FixAll support |
| RS1015 | Provide non-null `helpLinkUri` | DiagnosticDescriptor has null or empty help link |
| RS1016 | Code fix providers should provide FixAll support | Missing `GetFixAllProvider()` override |
| RS1017 | DiagnosticId must be non-null constant | Diagnostic ID is not a compile-time constant |
| RS1022 | Do not use Workspaces assembly types | Analyzer references `Microsoft.CodeAnalysis.Workspaces` (not available in all hosts) |
| RS1024 | Symbols should be compared for equality | Using `==` instead of `SymbolEqualityComparer` for symbol comparison |
| RS1026 | Enable concurrent execution | Missing `context.EnableConcurrentExecution()` call |
| RS1029 | Do not use reserved diagnostic IDs | Using `CA`, `CS`, `IDE`, or other platform-reserved prefixes |
| RS1030 | Do not invoke `Compilation.GetSemanticModel()` | Use the `SemanticModel` from the analysis context instead |
| RS1035 | Do not use APIs banned for analyzers | Using APIs not available in all analyzer host environments |
| RS1041 | Compiler extensions should target `netstandard2.0` | Project targets a framework other than `netstandard2.0` |

### Release Tracking (RS2000-Series)

For mature analyzers, enable release tracking to manage diagnostic ID lifecycle:

| ID | Title | What It Catches |
|----|-------|-----------------|
| RS2000 | Add analyzer diagnostic IDs to analyzer release | New diagnostic ID not tracked in release file |
| RS2001 | Ensure up-to-date entry for analyzer diagnostic IDs | Release tracking file is out of sync |
| RS2008 | Enable analyzer release tracking | Project should opt into release tracking |

Release tracking uses `AnalyzerReleases.Shipped.md` and `AnalyzerReleases.Unshipped.md` files to track which diagnostic IDs have been published.

---

## References

- [Tutorial: Write your first analyzer and code fix](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix)
- [Roslyn SDK overview](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/)
- [Microsoft.CodeAnalysis.Testing](https://github.com/dotnet/roslyn-sdk/tree/main/src/Microsoft.CodeAnalysis.Testing)
- [Analyzer NuGet packaging conventions](https://learn.microsoft.com/en-us/nuget/guides/analyzers-conventions)
- [dotnet/roslyn-analyzers (RS diagnostic source)](https://github.com/dotnet/roslyn-analyzers)
- [Meziantou.Analyzer (exemplar project)](https://github.com/meziantou/Meziantou.Analyzer)
