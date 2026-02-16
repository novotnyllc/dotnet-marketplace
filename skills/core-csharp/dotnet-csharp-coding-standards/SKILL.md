---
name: dotnet-csharp-coding-standards
description: "WHEN writing or reviewing C# for naming, style, or file organization. Framework Design Guidelines and conventions."
---

# dotnet-csharp-coding-standards

Modern .NET coding standards based on Microsoft Framework Design Guidelines and C# Coding Conventions. This skill covers naming, file organization, and code style rules that agents should follow when generating or reviewing C# code.

Cross-references: [skill:dotnet-csharp-modern-patterns] for language feature usage, [skill:dotnet-csharp-async-patterns] for async naming conventions, [skill:dotnet-solid-principles] for SOLID, DRY, and SRP design principles at the class and interface level.

---

## Naming Conventions

### General Rules

| Element | Convention | Example |
|---------|-----------|---------|
| Namespaces | PascalCase, dot-separated | `MyCompany.MyProduct.Core` |
| Classes, Records, Structs | PascalCase | `OrderService`, `OrderSummary` |
| Interfaces | `I` + PascalCase | `IOrderRepository` |
| Methods | PascalCase | `GetOrderAsync` |
| Properties | PascalCase | `OrderDate` |
| Events | PascalCase | `OrderCompleted` |
| Public constants | PascalCase | `MaxRetryCount` |
| Private fields | `_camelCase` | `_orderRepository` |
| Parameters, locals | camelCase | `orderId`, `totalAmount` |
| Type parameters | `T` or `T` + PascalCase | `T`, `TKey`, `TValue` |
| Enum members | PascalCase | `OrderStatus.Pending` |

### Async Method Naming

Suffix async methods with `Async`:

```csharp
// Correct
public Task<Order> GetOrderAsync(int id);
public ValueTask SaveChangesAsync(CancellationToken ct);

// Wrong
public Task<Order> GetOrder(int id);      // missing Async suffix
public Task<Order> GetOrderTask(int id);  // wrong suffix
```

Exception: Event handlers and interface implementations where the framework does not use the `Async` suffix (e.g., ASP.NET Core middleware `InvokeAsync` is already named by the framework).

### Boolean Naming

Prefix booleans with `is`, `has`, `can`, `should`, or similar:

```csharp
public bool IsActive { get; set; }
public bool HasOrders { get; }
public bool CanDelete(Order order);
```

### Collection Naming

Use plural nouns for collections:

```csharp
public IReadOnlyList<Order> Orders { get; }    // not OrderList
public Dictionary<string, int> CountsByName { get; } // descriptive
```

---

## File Organization

### One Type Per File

Each top-level type (class, record, struct, interface, enum) should be in its own file, named exactly as the type. Nested types stay in the containing type's file.

```
OrderService.cs        -> public class OrderService
IOrderRepository.cs    -> public interface IOrderRepository
OrderStatus.cs         -> public enum OrderStatus
OrderSummary.cs        -> public record OrderSummary
```

### File-Scoped Namespaces

Always use file-scoped namespaces (C# 10+):

```csharp
// Correct
namespace MyApp.Services;

public class OrderService { }

// Avoid: block-scoped namespace adds unnecessary indentation
namespace MyApp.Services
{
    public class OrderService { }
}
```

### Using Directives

Place `using` directives at the top of the file, outside the namespace. With `<ImplicitUsings>enable</ImplicitUsings>` (default in modern .NET), common namespaces are already imported. Only add explicit `using` statements for namespaces not covered by implicit usings.

Order of `using` directives:
1. `System.*` namespaces
2. Third-party namespaces
3. Project namespaces

### Directory Structure

Organize by feature or layer, matching namespace hierarchy:

```
src/MyApp/
  Features/
    Orders/
      OrderService.cs
      IOrderRepository.cs
      OrderEndpoints.cs
    Users/
      UserService.cs
  Infrastructure/
    Persistence/
      OrderRepository.cs
```

---

## Code Style

### Braces

Always use braces for control flow, even for single-line bodies:

```csharp
// Correct
if (order.IsValid)
{
    Process(order);
}

// Avoid
if (order.IsValid)
    Process(order);
```

### Expression-Bodied Members

Use expression bodies for single-expression members:

```csharp
// Properties
public string FullName => $"{FirstName} {LastName}";

// Methods (single expression only)
public override string ToString() => $"Order #{Id}";

// Avoid for multi-statement methods -- use block body instead
```

### `var` Usage

Use `var` when the type is obvious from the right-hand side:

```csharp
// Type is obvious: use var
var orders = new List<Order>();
var customer = GetCustomerById(id);
var name = "Alice";

// Type is not obvious: use explicit type
IOrderRepository repo = serviceProvider.GetRequiredService<IOrderRepository>();
decimal total = CalculateTotal(items);
```

### Null Handling

Prefer pattern matching over null checks:

```csharp
// Preferred
if (order is not null) { }
if (order is { Status: OrderStatus.Active }) { }

// Acceptable
if (order != null) { }

// Avoid
if (order is object) { }
if (!(order is null)) { }
```

Use null-conditional and null-coalescing operators:

```csharp
var name = customer?.Name ?? "Unknown";
var orders = customer?.Orders ?? [];
items ??= [];
```

### String Handling

Prefer string interpolation over concatenation or `string.Format`:

```csharp
// Preferred
var message = $"Order {orderId} totals {total:C2}";

// For complex interpolations, use raw string literals (C# 11+)
var json = $$"""
    {
        "id": {{orderId}},
        "name": "{{name}}"
    }
    """;

// Avoid
var message = string.Format("Order {0} totals {1:C2}", orderId, total);
var message = "Order " + orderId + " totals " + total.ToString("C2");
```

---

## Access Modifiers

Always specify access modifiers explicitly. Do not rely on defaults:

```csharp
// Correct
public class OrderService
{
    private readonly IOrderRepository _repo;
    internal void ProcessBatch() { }
}

// Avoid: implicit internal class, implicit private field
class OrderService
{
    readonly IOrderRepository _repo;
}
```

### Modifier Order

Follow the standard order:

```
access (public/private/protected/internal) -> static -> extern -> new ->
virtual/abstract/override/sealed -> readonly -> volatile -> async -> partial
```

```csharp
public static readonly int MaxSize = 100;
protected virtual async Task<Order> LoadAsync() => await repo.GetDefaultAsync();
public sealed override string ToString() => Name;
```

---

## Type Design

These conventions implement SOLID and DRY principles at the code level. For comprehensive coverage with anti-patterns and fixes, see [skill:dotnet-solid-principles].

### Seal Classes by Default

Seal classes that are not designed for inheritance. This improves performance (devirtualization) and communicates intent:

```csharp
public sealed class OrderService(IOrderRepository repo)
{
    // Not designed for inheritance
}
```

Only leave classes unsealed when you explicitly design them as base classes.

### Prefer Composition Over Inheritance

```csharp
// Preferred: composition
public sealed class OrderProcessor(IValidator validator, INotifier notifier)
{
    public async Task ProcessAsync(Order order)
    {
        await validator.ValidateAsync(order);
        await notifier.NotifyAsync(order);
    }
}

// Avoid: deep inheritance hierarchies
public class BaseProcessor { }
public class ValidatingProcessor : BaseProcessor { }
public class NotifyingValidatingProcessor : ValidatingProcessor { }
```

### Interface Segregation

Keep interfaces focused. Prefer multiple small interfaces over one large one:

```csharp
// Preferred
public interface IOrderReader
{
    Task<Order?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<Order>> GetAllAsync(CancellationToken ct = default);
}

public interface IOrderWriter
{
    Task<Order> CreateAsync(Order order, CancellationToken ct = default);
    Task UpdateAsync(Order order, CancellationToken ct = default);
}

// Avoid: one large interface with unrelated responsibilities
public interface IOrderRepository : IOrderReader, IOrderWriter { }
```

---

## CancellationToken Conventions

Accept `CancellationToken` as the last parameter in async methods. Use `default` as the default value for optional tokens:

```csharp
public async Task<Order> GetOrderAsync(int id, CancellationToken ct = default)
{
    return await _repo.GetByIdAsync(id, ct);
}
```

Always forward the token to downstream async calls. Never ignore a received `CancellationToken`.

---

## XML Documentation

Add XML docs to public API surfaces. Keep them concise:

```csharp
/// <summary>
/// Retrieves an order by its unique identifier.
/// </summary>
/// <param name="id">The order identifier.</param>
/// <param name="ct">Cancellation token.</param>
/// <returns>The order, or <see langword="null"/> if not found.</returns>
public Task<Order?> GetByIdAsync(int id, CancellationToken ct = default);
```

Do not add XML docs to:
- Private or internal members (unless it's a library's `InternalsVisibleTo` API)
- Self-evident members (e.g., `public string Name { get; }`)
- Test methods

---

## Analyzer Enforcement

Configure these analyzers in `Directory.Build.props` or `.editorconfig` to enforce standards automatically:

```xml
<PropertyGroup>
  <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  <AnalysisLevel>latest-all</AnalysisLevel>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

Key `.editorconfig` rules for C# style:
```ini
[*.cs]
csharp_style_namespace_declarations = file_scoped:warning
csharp_prefer_braces = true:warning
csharp_style_var_for_built_in_types = true:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
dotnet_style_require_accessibility_modifiers = always:warning
csharp_style_prefer_pattern_matching = true:suggestion
```

See [skill:dotnet-add-analyzers] for full analyzer configuration.

---

## References

- [Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- [C# Coding Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C# Identifier Naming Rules](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names)
- [.editorconfig for .NET](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/code-style-rule-options)
