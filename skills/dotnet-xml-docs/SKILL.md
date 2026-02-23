---
name: dotnet-xml-docs
description: Writes XML doc comments. Tags, inheritdoc, GenerateDocumentationFile, warning suppression.
license: MIT
user-invocable: false
---

# dotnet-xml-docs

XML documentation comments for .NET: all standard tags (`<summary>`, `<param>`, `<returns>`, `<exception>`, `<remarks>`, `<example>`, `<value>`, `<typeparam>`, `<typeparamref>`, `<paramref>`), advanced tags (`<inheritdoc>` for interface and base class inheritance, `<see cref="..."/>`, `<seealso>`, `<c>` and `<code>`), enabling XML doc generation with `<GenerateDocumentationFile>` MSBuild property, warning suppression strategies for internal APIs (`CS1591`, `<NoWarn>`, `InternalsVisibleTo`), XML doc conventions for public NuGet libraries, auto-generation tooling (IDE quick-fix `///` trigger, GhostDoc-style patterns), and IntelliSense integration showing XML docs in IDE tooltips and autocomplete.

**Version assumptions:** .NET 8.0+ baseline. XML documentation comments are a C# language feature available in all .NET versions. `<GenerateDocumentationFile>` MSBuild property works with .NET SDK 6+. `<inheritdoc>` fully supported since C# 9.0 / .NET 5+.

## Scope

- Standard XML doc tags (summary, param, returns, exception, remarks, example)
- Advanced tags (inheritdoc, see cref, seealso, c, code)
- GenerateDocumentationFile MSBuild configuration
- Warning suppression strategies for internal APIs (CS1591)
- Conventions for public NuGet library documentation

## Out of scope

- API documentation site generation (DocFX, Starlight) -- see [skill:dotnet-api-docs]
- General C# coding conventions and naming standards -- see [skill:dotnet-csharp-coding-standards]
- CI/CD deployment of documentation sites -- see [skill:dotnet-gha-deploy]

Cross-references: [skill:dotnet-api-docs] for downstream API documentation generation from XML comments, [skill:dotnet-csharp-coding-standards] for general C# coding conventions, [skill:dotnet-gha-deploy] for doc site deployment.

---

## Enabling XML Documentation Generation

### MSBuild Configuration

Enable XML documentation file generation in the project or `Directory.Build.props`:

```xml
<!-- In .csproj or Directory.Build.props -->
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>
```

This generates a `.xml` file alongside the assembly during build (e.g., `MyLibrary.xml` next to `MyLibrary.dll`). NuGet pack automatically includes this XML file in the package, enabling IntelliSense for package consumers.

### Warning Suppression for Internal APIs

When `GenerateDocumentationFile` is enabled, the compiler emits CS1591 warnings for all public members missing XML doc comments. Suppress warnings selectively for internal-facing code:

**Option 1: Suppress globally for the entire project (not recommended for public libraries):**

```xml
<PropertyGroup>
  <NoWarn>$(NoWarn);CS1591</NoWarn>
</PropertyGroup>
```

**Option 2: Suppress per-file with pragma directives (recommended for mixed-visibility assemblies):**

```csharp
#pragma warning disable CS1591 // Missing XML comment for publicly visible type or member
public class InternalServiceHelper
{
    // This type is internal-facing despite being public
    // (e.g., exposed for testing via InternalsVisibleTo)
}
#pragma warning restore CS1591
```

**Option 3: Use `InternalsVisibleTo` and keep internal types truly internal:**

```csharp
// In AssemblyInfo.cs or a Properties file
[assembly: InternalsVisibleTo("MyLibrary.Tests")]
```

```csharp
// Mark internal-facing types as internal instead of public
internal class ServiceHelper
{
    // No CS1591 warning -- internal types are not documented
}
```

**Option 4: Treat missing docs as errors for public libraries (strictest):**

```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <!-- Treat missing XML docs as build errors -->
  <WarningsAsErrors>$(WarningsAsErrors);CS1591</WarningsAsErrors>
</PropertyGroup>
```

This forces documentation for every public member. Use this for NuGet packages where consumers depend on IntelliSense documentation.

---


For complete tag examples (summary, param, returns, exception, remarks, example, inheritdoc, see/seealso, comprehensive class example, library conventions), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Always enable `<GenerateDocumentationFile>` for public libraries** -- without it, NuGet consumers get no IntelliSense documentation. Add it to `Directory.Build.props` to apply across all projects in a solution.

2. **Use `<inheritdoc />` for interface implementations and overrides** -- do not duplicate documentation text between an interface and its implementation. Duplication causes maintenance drift.

3. **Do not suppress CS1591 globally for public NuGet packages** -- global suppression via `<NoWarn>CS1591</NoWarn>` hides all missing documentation warnings. Use per-file `#pragma` suppression for intentionally undocumented types, or make internal types truly `internal`.

4. **Use `<see cref="..."/>` for all type references, not bare type names** -- `<see cref="Widget"/>` enables IDE navigation and is validated at build time. Bare text "Widget" is not linked and can become stale if the type is renamed.

5. **Use `<see langword="null"/>` instead of bare `null` in documentation text** -- this renders with proper formatting in IntelliSense and API doc sites. Same applies to `true`, `false`, and other C# keywords.

6. **`<inheritdoc>` resolves at build time, not design time** -- some older IDE versions may show "Documentation not found" for `<inheritdoc>` in tooltips. The documentation is correctly resolved in the generated XML file and in API doc sites.

7. **XML doc comments must use `&lt;` and `&gt;` for generic type syntax in prose** -- but `<see cref="..."/>` handles generics automatically. Use `<see cref="List{T}"/>` (curly braces), not `<see cref="List&lt;T&gt;"/>`.

8. **In `<code>` blocks, use `&lt;` and `&gt;` for angle brackets** -- XML doc comments are XML, so `<` and `>` in code examples must be escaped. Alternatively, use `<![CDATA[...]]>` to avoid escaping.

9. **Do not generate API documentation sites from XML comments** -- API doc site generation (DocFX, OpenAPI-as-docs) belongs to [skill:dotnet-api-docs]. This skill covers the XML comment authoring side only.

10. **Document cancellation tokens with a single standard line** -- use "A token to cancel the asynchronous operation." for all `CancellationToken` parameters. Do not over-document the cancellation pattern.
