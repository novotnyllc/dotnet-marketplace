# dotnet-roslyn-analyzers -- Detailed Examples

Extended code examples for CodeRefactoringProvider authoring, multi-Roslyn-version targeting, and multi-version test matrix configuration.

---

## CodeRefactoringProvider: Full Extract Interface Example

A complete `CodeRefactoringProvider` that extracts an interface from a class. The provider is offered when the cursor is on a class identifier and the class has at least one public method.

```csharp
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Composition;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CodeActions;
using Microsoft.CodeAnalysis.CodeRefactorings;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

[ExportCodeRefactoringProvider(LanguageNames.CSharp, Name = nameof(ExtractInterfaceRefactoring))]
[Shared]
public sealed class ExtractInterfaceRefactoring : CodeRefactoringProvider
{
    public override async Task ComputeRefactoringsAsync(CodeRefactoringContext context)
    {
        var root = await context.Document
            .GetSyntaxRootAsync(context.CancellationToken)
            .ConfigureAwait(false);

        var node = root?.FindNode(context.Span);
        var classDecl = node?.FirstAncestorOrSelf<ClassDeclarationSyntax>();

        if (classDecl is null)
            return;

        // Only offer when cursor is on the class identifier
        if (!classDecl.Identifier.Span.IntersectsWith(context.Span))
            return;

        var publicMethods = classDecl.Members
            .OfType<MethodDeclarationSyntax>()
            .Where(m => m.Modifiers.Any(SyntaxKind.PublicKeyword))
            .ToList();

        if (publicMethods.Count == 0)
            return;

        context.RegisterRefactoring(
            CodeAction.Create(
                title: $"Extract interface I{classDecl.Identifier.Text}",
                createChangedSolution: ct =>
                    ExtractInterfaceAsync(context.Document, classDecl, publicMethods, ct),
                equivalenceKey: "ExtractInterface"));
    }

    private static async Task<Solution> ExtractInterfaceAsync(
        Document document,
        ClassDeclarationSyntax classDecl,
        List<MethodDeclarationSyntax> methods,
        CancellationToken cancellationToken)
    {
        // Build interface members from public method signatures
        var interfaceMembers = methods.Select(m =>
            SyntaxFactory.MethodDeclaration(m.ReturnType, m.Identifier)
                .WithParameterList(m.ParameterList)
                .WithSemicolonToken(SyntaxFactory.Token(SyntaxKind.SemicolonToken))
                .WithLeadingTrivia(SyntaxFactory.ElasticCarriageReturnLineFeed)
            ).Cast<MemberDeclarationSyntax>();

        var interfaceName = $"I{classDecl.Identifier.Text}";
        var interfaceDecl = SyntaxFactory.InterfaceDeclaration(interfaceName)
            .WithModifiers(SyntaxFactory.TokenList(
                SyntaxFactory.Token(SyntaxKind.PublicKeyword)))
            .WithMembers(SyntaxFactory.List(interfaceMembers));

        // Add interface to the same document after the class
        var root = await document.GetSyntaxRootAsync(cancellationToken)
            .ConfigureAwait(false);
        var newRoot = root!.InsertNodesAfter(classDecl, new[] { interfaceDecl });

        // Add base type to the class
        var updatedClass = newRoot.DescendantNodes()
            .OfType<ClassDeclarationSyntax>()
            .First(c => c.Identifier.Text == classDecl.Identifier.Text);

        var baseList = updatedClass.BaseList ?? SyntaxFactory.BaseList();
        var newBaseList = baseList.AddTypes(
            SyntaxFactory.SimpleBaseType(SyntaxFactory.ParseTypeName(interfaceName)));

        newRoot = newRoot.ReplaceNode(updatedClass,
            updatedClass.WithBaseList(newBaseList));

        return document.WithSyntaxRoot(newRoot).Project.Solution;
    }
}
```

---

## CodeRefactoringProvider Testing

Use `CSharpCodeRefactoringVerifier<T>` to test refactoring providers. Use the framework-agnostic package with `DefaultVerifier` (the framework-specific `.XUnit` suffix packages are obsolete):

```xml
<PropertyGroup>
  <!-- Enable Microsoft.Testing.Platform v2 runner -->
  <UseMicrosoftTestingPlatformRunner>true</UseMicrosoftTestingPlatformRunner>
</PropertyGroup>

<ItemGroup>
  <!-- NuGet: Microsoft.CodeAnalysis.CSharp.CodeRefactoring.Testing (framework-agnostic) -->
  <PackageReference Include="Microsoft.CodeAnalysis.CSharp.CodeRefactoring.Testing" Version="1.1.3" />
  <!-- NuGet: xunit.v3 (xUnit v3 test framework) -->
  <PackageReference Include="xunit.v3" Version="3.2.2" />
</ItemGroup>
```

```csharp
using Microsoft.CodeAnalysis.Testing;
using Verify = Microsoft.CodeAnalysis.CSharp.Testing.CSharpCodeRefactoringVerifier<
    ExtractInterfaceRefactoring,
    Microsoft.CodeAnalysis.Testing.DefaultVerifier>;

public class ExtractInterfaceRefactoringTests
{
    [Fact]
    public async Task ClassWithPublicMethods_OffersRefactoring()
    {
        var test = new Verify.Test
        {
            TestCode = """
                public class [|MyService|]
                {
                    public void DoWork() { }
                    public int Calculate(int x) => x * 2;
                    private void InternalHelper() { }
                }
                """,
            FixedCode = """
                public class MyService : IMyService
                {
                    public void DoWork() { }
                    public int Calculate(int x) => x * 2;
                    private void InternalHelper() { }
                }
                public interface IMyService
                {
                    void DoWork();
                    int Calculate(int x);
                }
                """
        };

        await test.RunAsync();
    }

    [Fact]
    public async Task ClassWithNoPublicMethods_NoRefactoring()
    {
        var test = """
            public class [|MyService|]
            {
                private void InternalHelper() { }
            }
            """;

        // Verify no refactoring is offered (no expected FixedCode)
        var verifyTest = new Verify.Test
        {
            TestCode = test,
            FixedCode = test
        };

        await verifyTest.RunAsync();
    }
}
```

The markup `[|text|]` indicates where the cursor/selection triggers the refactoring. The verifier checks that the refactoring is offered and produces the expected `FixedCode`.

---

## Multi-Roslyn-Version Project Structure

A complete multi-version analyzer solution structure following the Meziantou.Analyzer pattern:

```
MyAnalyzers/
  Directory.Build.props          # Shared properties
  Directory.Build.targets        # Conditional compilation constants
  src/
    MyAnalyzers/
      MyAnalyzers.csproj         # Analyzer project
      MyAnalyzer.cs
    MyAnalyzers.CodeFixes/
      MyAnalyzers.CodeFixes.csproj
      MyCodeFix.cs
  test/
    MyAnalyzers.Tests/
      MyAnalyzers.Tests.csproj   # Test project
      MyAnalyzerTests.cs
  pack/
    MyAnalyzers.Package/
      MyAnalyzers.Package.csproj # Packaging project
```

### Directory.Build.props

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    <EnforceExtendedAnalyzerRules>true</EnforceExtendedAnalyzerRules>
    <IsRoslynComponent>true</IsRoslynComponent>
    <RoslynVersion Condition="'$(RoslynVersion)' == ''">3.8</RoslynVersion>
  </PropertyGroup>
</Project>
```

### Directory.Build.targets

```xml
<Project>
  <!-- Roslyn version conditional compilation constants -->
  <PropertyGroup Condition="'$(RoslynVersion)' >= '3.8'">
    <DefineConstants>$(DefineConstants);ROSLYN_3_8;ROSLYN_3_8_OR_GREATER</DefineConstants>
  </PropertyGroup>
  <PropertyGroup Condition="'$(RoslynVersion)' >= '4.2'">
    <DefineConstants>$(DefineConstants);ROSLYN_4_2;ROSLYN_4_2_OR_GREATER</DefineConstants>
  </PropertyGroup>
  <PropertyGroup Condition="'$(RoslynVersion)' >= '4.4'">
    <DefineConstants>$(DefineConstants);ROSLYN_4_4;ROSLYN_4_4_OR_GREATER</DefineConstants>
  </PropertyGroup>
  <PropertyGroup Condition="'$(RoslynVersion)' >= '4.6'">
    <DefineConstants>$(DefineConstants);ROSLYN_4_6;ROSLYN_4_6_OR_GREATER</DefineConstants>
  </PropertyGroup>
  <PropertyGroup Condition="'$(RoslynVersion)' >= '4.8'">
    <DefineConstants>$(DefineConstants);ROSLYN_4_8;ROSLYN_4_8_OR_GREATER</DefineConstants>
  </PropertyGroup>
  <PropertyGroup Condition="'$(RoslynVersion)' >= '4.14'">
    <DefineConstants>$(DefineConstants);ROSLYN_4_14;ROSLYN_4_14_OR_GREATER</DefineConstants>
  </PropertyGroup>
</Project>
```

### CI Multi-Version Test Matrix (GitHub Actions)

Uses xUnit v3 with Microsoft.Testing.Platform v2 (MTP2). Set `UseMicrosoftTestingPlatformRunner` in the test project (see CodeRefactoringProvider Testing above) and parameterize `$(RoslynVersion)`:

```yaml
jobs:
  test:
    strategy:
      matrix:
        roslyn-version: ['3.8', '4.2', '4.4', '4.6', '4.8']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'
      - name: Test with Roslyn ${{ matrix.roslyn-version }}
        run: >
          dotnet test
          -p:RoslynVersion=${{ matrix.roslyn-version }}
          --logger "trx;LogFileName=results-${{ matrix.roslyn-version }}.trx"
```

### Packaging Project (.csproj)

The packaging project references each version-specific build output and places them in the correct NuGet paths:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <IncludeBuildOutput>false</IncludeBuildOutput>
    <DevelopmentDependency>true</DevelopmentDependency>
    <SuppressDependenciesWhenPacking>true</SuppressDependenciesWhenPacking>
    <PackageId>MyAnalyzers</PackageId>
  </PropertyGroup>

  <ItemGroup>
    <!-- Fallback: lowest supported Roslyn version -->
    <None Include="..\build\roslyn3.8\MyAnalyzers.dll"
          Pack="true" PackagePath="analyzers/dotnet/cs" />
    <!-- Version-specific overrides -->
    <None Include="..\build\roslyn3.8\MyAnalyzers.dll"
          Pack="true" PackagePath="analyzers/dotnet/roslyn3.8/cs" />
    <None Include="..\build\roslyn4.2\MyAnalyzers.dll"
          Pack="true" PackagePath="analyzers/dotnet/roslyn4.2/cs" />
    <None Include="..\build\roslyn4.4\MyAnalyzers.dll"
          Pack="true" PackagePath="analyzers/dotnet/roslyn4.4/cs" />
  </ItemGroup>

  <ItemGroup>
    <None Include="_._" Pack="true" PackagePath="lib/netstandard2.0" />
  </ItemGroup>
</Project>
```

### Version-Gated API Usage

```csharp
public sealed class MyAdvancedAnalyzer : DiagnosticAnalyzer
{
    public override void Initialize(AnalysisContext context)
    {
        context.EnableConcurrentExecution();
        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);

        // Base registration works on all versions
        context.RegisterSymbolAction(AnalyzeSymbol, SymbolKind.Method);

#if ROSLYN_3_8_OR_GREATER
        // DiagnosticSuppressor support (Roslyn 3.8+)
        // Register compilation-level suppression analysis
        context.RegisterCompilationStartAction(compilationCtx =>
        {
            compilationCtx.RegisterSymbolAction(
                AnalyzeForSuppression, SymbolKind.NamedType);
        });
#endif

#if ROSLYN_4_8_OR_GREATER
        // CollectionExpression operation kind available in Roslyn 4.8+
        context.RegisterOperationAction(AnalyzeCollectionExpression,
            OperationKind.CollectionExpression);
#endif
    }

    // ... analysis methods
}
```

### Pack Verification for Multi-Version Packages

```bash
dotnet pack -c Release
# Verify version-specific paths exist
unzip -l ./bin/Release/MyAnalyzers.1.0.0.nupkg | grep 'analyzers/'
# Expected output:
#   analyzers/dotnet/cs/MyAnalyzers.dll
#   analyzers/dotnet/roslyn3.8/cs/MyAnalyzers.dll
#   analyzers/dotnet/roslyn4.2/cs/MyAnalyzers.dll
#   analyzers/dotnet/roslyn4.4/cs/MyAnalyzers.dll
```
