---
name: dotnet-xml-docs
description: "Writing XML doc comments. Tags, inheritdoc, GenerateDocumentationFile, warning suppression."
---

# dotnet-xml-docs

XML documentation comments for .NET: all standard tags (`<summary>`, `<param>`, `<returns>`, `<exception>`, `<remarks>`, `<example>`, `<value>`, `<typeparam>`, `<typeparamref>`, `<paramref>`), advanced tags (`<inheritdoc>` for interface and base class inheritance, `<see cref="..."/>`, `<seealso>`, `<c>` and `<code>`), enabling XML doc generation with `<GenerateDocumentationFile>` MSBuild property, warning suppression strategies for internal APIs (`CS1591`, `<NoWarn>`, `InternalsVisibleTo`), XML doc conventions for public NuGet libraries, auto-generation tooling (IDE quick-fix `///` trigger, GhostDoc-style patterns), and IntelliSense integration showing XML docs in IDE tooltips and autocomplete.

**Version assumptions:** .NET 8.0+ baseline. XML documentation comments are a C# language feature available in all .NET versions. `<GenerateDocumentationFile>` MSBuild property works with .NET SDK 6+. `<inheritdoc>` fully supported since C# 9.0 / .NET 5+.

**Scope boundary:** This skill owns XML documentation comment authoring -- the syntax, conventions, and MSBuild configuration for generating XML doc files. API documentation site generation from XML comments (DocFX, Starlight) is owned by [skill:dotnet-api-docs]. General C# coding conventions (naming, formatting) are owned by [skill:dotnet-csharp-coding-standards].

**Out of scope:** API documentation site generation from XML comments (DocFX setup, OpenAPI-as-docs, doc-code sync) -- see [skill:dotnet-api-docs]. General C# coding conventions and naming standards -- see [skill:dotnet-csharp-coding-standards]. CI/CD deployment of documentation sites -- see [skill:dotnet-gha-deploy].

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

## Standard XML Doc Tags

### `<summary>`

Describes the type or member. This is the primary tag that appears in IntelliSense tooltips.

```csharp
/// <summary>
/// Provides methods for managing widgets in the system.
/// Widget operations are thread-safe and support cancellation.
/// </summary>
public class WidgetService
{
}
```

### `<param>`

Documents a method parameter.

```csharp
/// <summary>
/// Creates a new widget with the specified name and optional category.
/// </summary>
/// <param name="name">The display name for the widget. Must not be null or whitespace.</param>
/// <param name="category">
/// The category to assign. When <see langword="null"/>, the default category is used.
/// </param>
/// <param name="cancellationToken">A token to cancel the asynchronous operation.</param>
public async Task<Widget> CreateWidgetAsync(
    string name,
    string? category = null,
    CancellationToken cancellationToken = default)
{
}
```

### `<returns>`

Documents the return value.

```csharp
/// <summary>
/// Finds a widget by its unique identifier.
/// </summary>
/// <param name="id">The unique identifier of the widget.</param>
/// <returns>
/// The widget if found; otherwise, <see langword="null"/>.
/// </returns>
public async Task<Widget?> FindByIdAsync(Guid id)
{
}
```

### `<exception>`

Documents exceptions that may be thrown.

```csharp
/// <summary>
/// Updates the widget's name.
/// </summary>
/// <param name="id">The widget identifier.</param>
/// <param name="newName">The new name to assign.</param>
/// <exception cref="ArgumentException">
/// Thrown when <paramref name="newName"/> is null or whitespace.
/// </exception>
/// <exception cref="KeyNotFoundException">
/// Thrown when no widget with the specified <paramref name="id"/> exists.
/// </exception>
/// <exception cref="InvalidOperationException">
/// Thrown when the widget is in a read-only state and cannot be modified.
/// </exception>
public async Task UpdateNameAsync(Guid id, string newName)
{
}
```

### `<remarks>`

Provides additional context beyond the summary. Use for implementation notes, usage guidance, and caveats.

```csharp
/// <summary>
/// Computes the hash of the widget's content for change detection.
/// </summary>
/// <remarks>
/// <para>
/// The hash is computed using SHA-256 over the UTF-8 encoded content.
/// Results are deterministic across platforms and .NET versions.
/// </para>
/// <para>
/// This method is thread-safe. The returned hash is a lowercase hex string
/// without any prefix (e.g., "a1b2c3..." not "0xa1b2c3...").
/// </para>
/// </remarks>
/// <returns>A 64-character lowercase hexadecimal hash string.</returns>
public string ComputeContentHash()
{
}
```

### `<example>`

Provides a code example demonstrating usage. Essential for public library APIs.

```csharp
/// <summary>
/// Creates a new widget and persists it to the repository.
/// </summary>
/// <example>
/// <code>
/// var service = new WidgetService(repository, logger);
///
/// var widget = await service.CreateWidgetAsync(
///     "Dashboard Widget",
///     category: "Analytics",
///     cancellationToken: ct);
///
/// Console.WriteLine($"Created widget: {widget.Id}");
/// </code>
/// </example>
public async Task<Widget> CreateWidgetAsync(
    string name,
    string? category = null,
    CancellationToken cancellationToken = default)
{
}
```

### `<value>`

Documents a property's value. Similar to `<returns>` but for properties.

```csharp
/// <summary>
/// Gets the current status of the widget.
/// </summary>
/// <value>
/// The widget status. Defaults to <see cref="WidgetStatus.Draft"/> for new widgets.
/// </value>
public WidgetStatus Status { get; private set; }
```

### `<typeparam>`

Documents a generic type parameter.

```csharp
/// <summary>
/// A repository that provides CRUD operations for entities.
/// </summary>
/// <typeparam name="TEntity">
/// The entity type. Must implement <see cref="IEntity"/> and have a parameterless constructor.
/// </typeparam>
/// <typeparam name="TKey">
/// The type of the entity's primary key. Typically <see cref="Guid"/> or <see cref="int"/>.
/// </typeparam>
public interface IRepository<TEntity, TKey>
    where TEntity : class, IEntity
    where TKey : struct
{
}
```

---

## Advanced Tags

### `<inheritdoc>`

Inherits documentation from a base class or interface. Eliminates duplication when implementing interfaces or overriding virtual members.

**Interface implementation:**

```csharp
public interface IWidgetService
{
    /// <summary>
    /// Creates a new widget with the specified name.
    /// </summary>
    /// <param name="name">The display name for the widget.</param>
    /// <returns>The created widget.</returns>
    Task<Widget> CreateWidgetAsync(string name);
}

public class WidgetService : IWidgetService
{
    /// <inheritdoc />
    public async Task<Widget> CreateWidgetAsync(string name)
    {
        // Implementation inherits all documentation from the interface
    }
}
```

**Base class override:**

```csharp
public abstract class RepositoryBase<T>
{
    /// <summary>
    /// Retrieves an entity by its unique identifier.
    /// </summary>
    /// <param name="id">The entity identifier.</param>
    /// <returns>The entity if found; otherwise, <see langword="null"/>.</returns>
    public abstract Task<T?> GetByIdAsync(Guid id);
}

public class OrderRepository : RepositoryBase<Order>
{
    /// <inheritdoc />
    public override async Task<Order?> GetByIdAsync(Guid id)
    {
        // Inherits summary, param, and returns docs from base class
    }
}
```

**Selective inheritance with `cref`:**

```csharp
/// <inheritdoc cref="IWidgetService.CreateWidgetAsync(string)"/>
/// <remarks>
/// This implementation validates the name and assigns a default category
/// before persisting to the database.
/// </remarks>
public async Task<Widget> CreateWidgetAsync(string name)
{
}
```

**Inheritance with path filter:**

```csharp
/// <inheritdoc cref="IWidgetService.CreateWidgetAsync(string)" path="/summary"/>
/// <param name="name">Custom param doc that overrides the interface.</param>
public async Task<Widget> CreateWidgetAsync(string name)
{
}
```

### `<see>` and `<seealso>`

Create inline references and "See Also" links.

```csharp
/// <summary>
/// Validates the widget against the rules defined in <see cref="WidgetValidator"/>.
/// Use <see cref="WidgetService.CreateWidgetAsync(string)"/> to create validated widgets.
/// </summary>
/// <seealso cref="WidgetValidator"/>
/// <seealso cref="IValidationResult"/>
/// <seealso href="https://docs.mylib.dev/validation">Validation Guide</seealso>
public ValidationResult Validate(Widget widget)
{
}
```

**`<see>` variants:**

```csharp
/// <summary>
/// Returns <see langword="true"/> if the widget is active,
/// <see langword="false"/> otherwise.
/// Use <see cref="Activate"/> to change the state.
/// The value is stored as a <see cref="bool"/>.
/// </summary>
public bool IsActive { get; }
```

### `<c>` and `<code>`

Format inline code and code blocks within documentation.

```csharp
/// <summary>
/// Parses a widget name from the format <c>"category:name"</c>.
/// </summary>
/// <remarks>
/// The expected input format:
/// <code>
/// "analytics:page-views"    // category = "analytics", name = "page-views"
/// "default:my-widget"       // category = "default", name = "my-widget"
/// "my-widget"               // category = null, name = "my-widget" (no colon)
/// </code>
/// </remarks>
public (string? Category, string Name) ParseWidgetName(string input)
{
}
```

### `<paramref>` and `<typeparamref>`

Reference parameters and type parameters within documentation text.

```csharp
/// <summary>
/// Converts <paramref name="entity"/> to a DTO of type <typeparamref name="TDto"/>.
/// If <paramref name="entity"/> is <see langword="null"/>, returns the default value
/// of <typeparamref name="TDto"/>.
/// </summary>
/// <typeparam name="TDto">The target DTO type.</typeparam>
/// <param name="entity">The source entity to convert.</param>
public TDto? ToDto<TDto>(object? entity)
{
}
```

### `<list>`

Create bulleted, numbered, or table lists within documentation.

```csharp
/// <summary>
/// Applies the specified transformation to the widget.
/// </summary>
/// <remarks>
/// Supported transformations:
/// <list type="bullet">
/// <item><description>Resize -- changes the widget dimensions</description></item>
/// <item><description>Recolor -- applies a new color scheme</description></item>
/// <item><description>Reposition -- moves the widget to new coordinates</description></item>
/// </list>
/// </remarks>
public void ApplyTransformation(Widget widget, Transformation transform)
{
}
```

---

## Comprehensive XML Doc Example

A complete class demonstrating all tag types working together:

```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace MyLibrary;

/// <summary>
/// Manages the lifecycle of widgets including creation, retrieval, update, and deletion.
/// All operations are thread-safe and support cancellation via <see cref="CancellationToken"/>.
/// </summary>
/// <remarks>
/// <para>
/// <see cref="WidgetService"/> requires a registered <see cref="IWidgetRepository"/>
/// and <see cref="ILogger{TCategoryName}"/> via dependency injection.
/// </para>
/// <para>
/// Widget names must be unique within a category. Attempting to create a widget with a
/// duplicate name in the same category throws <see cref="InvalidOperationException"/>.
/// </para>
/// </remarks>
/// <example>
/// Register and use the service:
/// <code>
/// // Registration
/// builder.Services.AddScoped&lt;IWidgetService, WidgetService&gt;();
///
/// // Usage
/// var widget = await widgetService.CreateWidgetAsync(
///     "My Widget",
///     category: "Dashboard");
/// </code>
/// </example>
/// <seealso cref="IWidgetRepository"/>
/// <seealso cref="Widget"/>
public class WidgetService : IWidgetService
{
    private readonly IWidgetRepository _repository;
    private readonly ILogger<WidgetService> _logger;

    /// <summary>
    /// Initializes a new instance of <see cref="WidgetService"/>.
    /// </summary>
    /// <param name="repository">The widget data repository.</param>
    /// <param name="logger">The logger for diagnostic output.</param>
    /// <exception cref="ArgumentNullException">
    /// Thrown when <paramref name="repository"/> or <paramref name="logger"/> is
    /// <see langword="null"/>.
    /// </exception>
    public WidgetService(IWidgetRepository repository, ILogger<WidgetService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }

    /// <summary>
    /// Gets the total number of widgets in the system.
    /// </summary>
    /// <value>A non-negative integer representing the total widget count.</value>
    public int TotalCount => _repository.Count;

    /// <inheritdoc />
    public async Task<Widget> CreateWidgetAsync(
        string name,
        string? category = null,
        CancellationToken cancellationToken = default)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(name);

        _logger.LogInformation("Creating widget {Name} in category {Category}", name, category);

        var widget = new Widget
        {
            Id = Guid.NewGuid(),
            Name = name,
            Category = category ?? "default",
            CreatedAt = DateTimeOffset.UtcNow,
            Status = WidgetStatus.Draft
        };

        await _repository.AddAsync(widget, cancellationToken);
        return widget;
    }

    /// <summary>
    /// Retrieves all widgets matching the specified filter criteria.
    /// </summary>
    /// <param name="filter">
    /// The filter to apply. Use <see cref="WidgetFilter.None"/> for unfiltered results.
    /// </param>
    /// <param name="cancellationToken">A token to cancel the operation.</param>
    /// <returns>
    /// A read-only list of widgets matching the filter. Returns an empty list if no
    /// widgets match the criteria.
    /// </returns>
    /// <exception cref="ArgumentNullException">
    /// Thrown when <paramref name="filter"/> is <see langword="null"/>.
    /// </exception>
    public async Task<IReadOnlyList<Widget>> ListAsync(
        WidgetFilter filter,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(filter);
        return await _repository.FindAsync(filter, cancellationToken);
    }
}
```

---

## XML Doc Conventions for Public Libraries

### Documentation Requirements

For NuGet packages consumed by other developers, follow these conventions:

1. **Every public type must have a `<summary>`** -- this is the minimum for IntelliSense to display useful information
2. **Every public method parameter must have a `<param>`** -- describe what the parameter controls, valid ranges, and null behavior
3. **Every method that can throw must document exceptions with `<exception>`** -- callers need to know what to catch
4. **Return values must have `<returns>`** -- describe the return value semantics, especially for nullable returns
5. **Properties should have `<value>`** -- describe what the property represents and its default value
6. **Generic type parameters must have `<typeparam>`** -- describe constraints and expected usage
7. **Complex APIs should include `<example>`** -- show real usage, not trivial one-liners
8. **Use `<remarks>` for caveats and threading behavior** -- important context that does not belong in the summary

### Writing Style

- Use third person declarative: "Gets the widget name" not "Get the widget name" or "This gets the widget name"
- Start `<summary>` with a verb: "Creates...", "Retrieves...", "Validates...", "Computes..."
- Avoid restating the obvious: do not write "Gets the Name property" for a property called `Name`
- Document behavior, not implementation: "Returns the cached value if available" not "Checks the dictionary and returns the value"
- Use `<see cref="..."/>` for all type and member references -- enables IDE navigation and refactoring support
- Use `<see langword="null"/>`, `<see langword="true"/>`, `<see langword="false"/>` instead of bare `null`, `true`, `false`

### CancellationToken Convention

Standardize documentation for `CancellationToken` parameters:

```csharp
/// <param name="cancellationToken">A token to cancel the asynchronous operation.</param>
```

This one-line description is sufficient for the standard `CancellationToken cancellationToken = default` pattern. Do not over-document what cancellation means -- callers understand the pattern.

---

## Auto-Generation Tooling

### IDE Quick-Fix Generation

All major .NET IDEs generate XML doc skeletons when you type `///` above a member:

**Visual Studio / VS Code (C# Dev Kit):**
- Type `///` above a method, class, or property
- The IDE generates a `<summary>` skeleton with `<param>`, `<returns>`, `<typeparam>` tags pre-filled based on the member's signature

**JetBrains Rider:**
- Type `///` to trigger the same skeleton generation
- Rider additionally warns about missing XML docs and offers quick-fixes to add them

### GhostDoc-Style Patterns

GhostDoc and similar tools generate documentation text from member names using naming convention heuristics:

- `GetWidgetById` generates "Gets the widget by identifier"
- `IsActive` generates "Gets a value indicating whether this instance is active"
- `CreateWidgetAsync` generates "Creates the widget asynchronously"

These auto-generated descriptions are a starting point. Always review and improve generated text to add domain-specific context, parameter constraints, exception conditions, and examples.

### EditorConfig Integration

Enforce XML documentation requirements through `.editorconfig`:

```ini
# .editorconfig
[*.cs]
# Require XML documentation for public members
dotnet_diagnostic.CS1591.severity = warning

# For public libraries, treat as error:
# dotnet_diagnostic.CS1591.severity = error
```

---

## IntelliSense Integration

### How XML Docs Surface in IDEs

XML documentation comments are the primary source of IntelliSense tooltips:

- **Hover tooltips:** Display `<summary>` text when hovering over a type or member
- **Parameter hints:** Display `<param>` text in the parameter info popup during method calls
- **Completion list:** Display `<summary>` in the autocomplete dropdown
- **Quick Info:** Display `<returns>`, `<exception>`, and `<remarks>` in expanded documentation panels
- **Signature help:** Display parameter names and types with `<param>` descriptions

### NuGet Package IntelliSense

When `<GenerateDocumentationFile>` is enabled and the package is published to NuGet, the XML file is included in the package. Consumers get full IntelliSense support without needing source access:

```xml
<!-- The XML doc file is automatically included in the NuGet package -->
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <!-- The XML file appears in the package's lib/net8.0/ directory -->
</PropertyGroup>
```

No additional NuGet packaging configuration is needed -- `dotnet pack` includes the XML doc file automatically when `GenerateDocumentationFile` is `true`.

### Source Link Integration

Combine XML docs with Source Link for the best developer experience:

```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
  <!-- Source Link enables "Go to Definition" into package source -->
  <PublishRepositoryUrl>true</PublishRepositoryUrl>
  <EmbedUntrackedSources>true</EmbedUntrackedSources>
  <IncludeSymbols>true</IncludeSymbols>
  <SymbolPackageFormat>snupkg</SymbolPackageFormat>
</PropertyGroup>
```

With both XML docs and Source Link enabled, consumers can hover for documentation and navigate to the original source code.

---

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
