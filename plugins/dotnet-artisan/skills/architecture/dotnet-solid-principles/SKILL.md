---
name: dotnet-solid-principles
description: "Designing classes or refactoring. SOLID, DRY, SRP with C# anti-patterns, fixes, compliance."
---

# dotnet-solid-principles

Foundational design principles for .NET applications. Covers each SOLID principle with concrete C# anti-patterns and fixes, plus DRY guidance with nuance on when duplication is acceptable. These principles guide class design, interface contracts, and dependency management across all .NET project types.

**Scope boundary:** This skill owns foundational SOLID/DRY design principles at the class and interface level. Architectural patterns (vertical slices, request pipelines, caching, idempotency) are owned by [skill:dotnet-architecture-patterns]. DI container mechanics (registration, lifetimes, keyed services) are owned by [skill:dotnet-csharp-dependency-injection]. Code smells and anti-pattern detection are owned by [skill:dotnet-csharp-code-smells].

Cross-references: [skill:dotnet-architecture-patterns] for clean architecture and vertical slices, [skill:dotnet-csharp-dependency-injection] for DI registration patterns and lifetime management, [skill:dotnet-csharp-code-smells] for anti-pattern detection, [skill:dotnet-csharp-coding-standards] for naming and style conventions.

---

## Single Responsibility Principle (SRP)

A class should have only one reason to change. Apply the "describe in one sentence" test: if you cannot describe what a class does in one sentence without using "and" or "or", it likely violates SRP.

### Anti-Pattern: God Class

```csharp
// WRONG -- OrderService handles validation, persistence, email, and PDF generation
public class OrderService
{
    private readonly AppDbContext _db;
    private readonly SmtpClient _smtp;

    public OrderService(AppDbContext db, SmtpClient smtp)
    {
        _db = db;
        _smtp = smtp;
    }

    public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
    {
        // Validation logic (reason to change #1)
        if (string.IsNullOrEmpty(request.CustomerId))
            throw new ArgumentException("Customer required");

        // Persistence logic (reason to change #2)
        var order = new Order { CustomerId = request.CustomerId };
        _db.Orders.Add(order);
        await _db.SaveChangesAsync();

        // Email notification (reason to change #3)
        var message = new MailMessage("noreply@shop.com", request.Email,
            "Order Confirmed", $"Order {order.Id} created.");
        await _smtp.SendMailAsync(message);

        // PDF generation (reason to change #4)
        GenerateInvoicePdf(order);

        return order;
    }

    private void GenerateInvoicePdf(Order order) { /* ... */ }
}
```

### Fix: Separate Responsibilities

```csharp
// Each class has one reason to change
public sealed class OrderCreator(
    IOrderValidator validator,
    IOrderRepository repository,
    IOrderNotifier notifier)
{
    public async Task<Order> CreateAsync(
        CreateOrderRequest request, CancellationToken ct)
    {
        validator.Validate(request);

        var order = await repository.AddAsync(request, ct);

        await notifier.OrderCreatedAsync(order, ct);

        return order;
    }
}

public sealed class OrderValidator : IOrderValidator
{
    public void Validate(CreateOrderRequest request)
    {
        ArgumentException.ThrowIfNullOrEmpty(request.CustomerId);
        // ... validation rules
    }
}

public sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public async Task<Order> AddAsync(
        CreateOrderRequest request, CancellationToken ct)
    {
        var order = new Order { CustomerId = request.CustomerId };
        db.Orders.Add(order);
        await db.SaveChangesAsync(ct);
        return order;
    }
}
```

### Anti-Pattern: Fat Controller

```csharp
// WRONG -- controller contains business logic, mapping, and persistence
app.MapPost("/api/orders", async (
    CreateOrderRequest request,
    AppDbContext db,
    ILogger<Program> logger) =>
{
    // Validation in the endpoint
    if (request.Lines.Count == 0)
        return Results.BadRequest("At least one line required");

    // Business logic in the endpoint
    var total = request.Lines.Sum(l => l.Quantity * l.Price);
    if (total > 100_000)
        return Results.BadRequest("Order exceeds credit limit");

    // Mapping in the endpoint
    var order = new Order
    {
        CustomerId = request.CustomerId,
        Total = total,
        Lines = request.Lines.Select(l => new OrderLine
        {
            ProductId = l.ProductId,
            Quantity = l.Quantity,
            Price = l.Price
        }).ToList()
    };

    // Persistence in the endpoint
    db.Orders.Add(order);
    await db.SaveChangesAsync();

    logger.LogInformation("Order {OrderId} created", order.Id);
    return Results.Created($"/api/orders/{order.Id}", order);
});
```

Move business logic to a handler; keep the endpoint thin:

```csharp
app.MapPost("/api/orders", async (
    CreateOrderRequest request,
    IOrderHandler handler,
    CancellationToken ct) =>
{
    var result = await handler.CreateAsync(request, ct);
    return result switch
    {
        { IsSuccess: true } => Results.Created(
            $"/api/orders/{result.Value.Id}", result.Value),
        _ => Results.ValidationProblem(result.Errors)
    };
});
```

---

## Open/Closed Principle (OCP)

Classes should be open for extension but closed for modification. Add new behavior by implementing new types, not by editing existing switch/if chains.

### Anti-Pattern: Switch on Type

```csharp
// WRONG -- adding a new discount type requires modifying this method
public decimal CalculateDiscount(Order order)
{
    switch (order.DiscountType)
    {
        case "Percentage":
            return order.Total * order.DiscountValue / 100;
        case "FixedAmount":
            return order.DiscountValue;
        case "BuyOneGetOneFree":
            return order.Lines
                .Where(l => l.Quantity >= 2)
                .Sum(l => l.Price);
        default:
            return 0;
    }
}
```

### Fix: Strategy Pattern

```csharp
public interface IDiscountStrategy
{
    decimal Calculate(Order order);
}

public sealed class PercentageDiscount(decimal percentage) : IDiscountStrategy
{
    public decimal Calculate(Order order) =>
        order.Total * percentage / 100;
}

public sealed class FixedAmountDiscount(decimal amount) : IDiscountStrategy
{
    public decimal Calculate(Order order) =>
        Math.Min(amount, order.Total);
}

// New discount type -- no existing code modified
public sealed class BuyOneGetOneFreeDiscount : IDiscountStrategy
{
    public decimal Calculate(Order order) =>
        order.Lines
            .Where(l => l.Quantity >= 2)
            .Sum(l => l.Price);
}

// Usage -- resolved via DI or factory
public sealed class OrderPricing(
    IEnumerable<IDiscountStrategy> strategies)
{
    public decimal ApplyBestDiscount(Order order) =>
        strategies.Max(s => s.Calculate(order));
}
```

### Extension via Abstract Classes

When strategies share significant behavior, use an abstract base class:

```csharp
public abstract class NotificationSender
{
    public async Task SendAsync(Notification notification, CancellationToken ct)
    {
        // Shared behavior: validation and logging
        ArgumentNullException.ThrowIfNull(notification);
        await SendCoreAsync(notification, ct);
    }

    protected abstract Task SendCoreAsync(
        Notification notification, CancellationToken ct);
}

public sealed class EmailNotificationSender(IEmailClient client)
    : NotificationSender
{
    protected override async Task SendCoreAsync(
        Notification notification, CancellationToken ct)
    {
        await client.SendEmailAsync(
            notification.Recipient, notification.Subject,
            notification.Body, ct);
    }
}
```

---

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types without altering program correctness. A subclass must honor the behavioral contract of its parent -- preconditions cannot be strengthened, postconditions cannot be weakened.

### Anti-Pattern: Throwing in Override

```csharp
public class FileStorage : IStorage
{
    public virtual Stream OpenRead(string path) =>
        File.OpenRead(path);
}

// WRONG -- ReadOnlyFileStorage violates the base contract by
// throwing on a method the base type supports
public class ReadOnlyFileStorage : FileStorage
{
    public override Stream OpenRead(string path)
    {
        if (!File.Exists(path))
            throw new InvalidOperationException(
                "Cannot open files in read-only mode");
        return base.OpenRead(path);
    }

    // Surprise: callers expecting FileStorage behavior get exceptions
}
```

### Anti-Pattern: Collection Covariance Pitfall

```csharp
// WRONG -- List<T> is not covariant; this compiles but causes runtime issues
IList<Animal> animals = new List<Dog>(); // Compile error (correctly)

// However, arrays ARE covariant in C# -- this compiles but throws at runtime:
Animal[] animals = new Dog[10];
animals[0] = new Cat(); // ArrayTypeMismatchException at runtime!
```

### Fix: Use Covariant Interfaces

```csharp
// IEnumerable<out T> and IReadOnlyList<out T> are covariant
IEnumerable<Animal> animals = new List<Dog>(); // Safe -- read-only
IReadOnlyList<Animal> readOnlyAnimals = new List<Dog>(); // Safe

// When you need mutability, keep the concrete type
List<Dog> dogs = [new Dog("Rex"), new Dog("Buddy")];
ProcessAnimals(dogs); // Pass to covariant parameter

void ProcessAnimals(IReadOnlyList<Animal> animals)
{
    foreach (var animal in animals)
        animal.Speak();
}
```

### LSP Compliance Checklist

- Derived classes do not throw new exception types that the base does not declare
- Overrides do not add preconditions (e.g., null checks the base does not require)
- Overrides do not weaken postconditions (e.g., returning null when base guarantees non-null)
- Behavioral contracts are preserved: if `ICollection.Add` succeeds on the base, it must succeed on the derived type

---

## Interface Segregation Principle (ISP)

Clients should not be forced to depend on methods they do not use. Prefer narrow, role-specific interfaces over wide "header" interfaces.

### Anti-Pattern: Header Interface

```csharp
// WRONG -- IWorker forces all implementations to support every capability
public interface IWorker
{
    Task DoWorkAsync(CancellationToken ct);
    void ClockIn();
    void ClockOut();
    Task<decimal> CalculatePayAsync();
    void RequestTimeOff(DateRange range);
    Task SubmitExpenseAsync(Expense expense);
}

// ContractWorker does not clock in/out or request time off
public class ContractWorker : IWorker
{
    public Task DoWorkAsync(CancellationToken ct) => /* ... */;
    public void ClockIn() => throw new NotSupportedException(); // ISP violation
    public void ClockOut() => throw new NotSupportedException(); // ISP violation
    public Task<decimal> CalculatePayAsync() => /* ... */;
    public void RequestTimeOff(DateRange range) =>
        throw new NotSupportedException(); // ISP violation
    public Task SubmitExpenseAsync(Expense expense) =>
        throw new NotSupportedException(); // ISP violation
}
```

### Fix: Role Interfaces

```csharp
public interface IWorkPerformer
{
    Task DoWorkAsync(CancellationToken ct);
}

public interface ITimeTrackable
{
    void ClockIn();
    void ClockOut();
}

public interface IPayable
{
    Task<decimal> CalculatePayAsync();
}

public interface ITimeOffEligible
{
    void RequestTimeOff(DateRange range);
}

// FullTimeEmployee implements all applicable interfaces
public sealed class FullTimeEmployee :
    IWorkPerformer, ITimeTrackable, IPayable, ITimeOffEligible
{
    public Task DoWorkAsync(CancellationToken ct) => /* ... */;
    public void ClockIn() { /* ... */ }
    public void ClockOut() { /* ... */ }
    public Task<decimal> CalculatePayAsync() => /* ... */;
    public void RequestTimeOff(DateRange range) { /* ... */ }
}

// ContractWorker only implements what it needs
public sealed class ContractWorker : IWorkPerformer, IPayable
{
    public Task DoWorkAsync(CancellationToken ct) => /* ... */;
    public Task<decimal> CalculatePayAsync() => /* ... */;
}
```

### Practical .NET ISP

The .NET BCL demonstrates ISP well:

| Wide Interface | Segregated Alternatives |
|---|---|
| `IList<T>` (read + write) | `IReadOnlyList<T>` (read only) |
| `ICollection<T>` | `IReadOnlyCollection<T>` |
| `IDictionary<K,V>` | `IReadOnlyDictionary<K,V>` |

Accept the narrowest interface your method actually needs:

```csharp
// WRONG -- requires IList<T> but only reads
public decimal CalculateTotal(IList<OrderLine> lines) =>
    lines.Sum(l => l.Price * l.Quantity);

// RIGHT -- accepts IReadOnlyList<T> since it only reads
public decimal CalculateTotal(IReadOnlyList<OrderLine> lines) =>
    lines.Sum(l => l.Price * l.Quantity);

// BEST for iteration only -- accepts IEnumerable<T>
public decimal CalculateTotal(IEnumerable<OrderLine> lines) =>
    lines.Sum(l => l.Price * l.Quantity);
```

---

## Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details.

### Anti-Pattern: Direct Dependency

```csharp
// WRONG -- high-level OrderProcessor depends directly on low-level SqlOrderRepository
public sealed class OrderProcessor
{
    private readonly SqlOrderRepository _repository = new();
    private readonly SmtpEmailSender _emailSender = new();

    public async Task ProcessAsync(Order order)
    {
        await _repository.SaveAsync(order);      // Tight coupling to SQL
        await _emailSender.SendAsync(order.Email, // Tight coupling to SMTP
            "Order processed", $"Order {order.Id}");
    }
}
```

### Fix: Depend on Abstractions

```csharp
public interface IOrderRepository
{
    Task SaveAsync(Order order, CancellationToken ct = default);
    Task<Order?> GetByIdAsync(string id, CancellationToken ct = default);
}

public interface INotificationService
{
    Task NotifyAsync(string recipient, string subject,
        string body, CancellationToken ct = default);
}

// High-level module depends on abstractions
public sealed class OrderProcessor(
    IOrderRepository repository,
    INotificationService notifier)
{
    public async Task ProcessAsync(Order order, CancellationToken ct)
    {
        await repository.SaveAsync(order, ct);
        await notifier.NotifyAsync(order.Email,
            "Order processed", $"Order {order.Id}", ct);
    }
}

// Low-level modules implement abstractions
public sealed class SqlOrderRepository(AppDbContext db) : IOrderRepository
{
    public async Task SaveAsync(Order order, CancellationToken ct) =>
        /* EF Core persistence */;
    public async Task<Order?> GetByIdAsync(string id, CancellationToken ct) =>
        await db.Orders.FindAsync([id], ct);
}
```

### DI Registration

Register abstractions with Microsoft.Extensions.DependencyInjection. See [skill:dotnet-csharp-dependency-injection] for lifetime management, keyed services, and decoration patterns.

```csharp
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddScoped<INotificationService, SmtpNotificationService>();
builder.Services.AddScoped<OrderProcessor>();
```

### DIP Boundaries

Apply DIP at module boundaries, not everywhere:

- **DO** abstract infrastructure (database, email, file system, HTTP clients)
- **DO** abstract cross-cutting concerns (logging is already abstracted via `ILogger<T>`)
- **DO NOT** abstract simple value objects, DTOs, or internal implementation details
- **DO NOT** create `IFoo`/`Foo` pairs for every class -- only abstract where substitution adds value (testing, multiple implementations, or anticipated change)

---

## DRY (Don't Repeat Yourself)

Every piece of knowledge should have a single, authoritative representation. But DRY is about knowledge duplication, not code duplication.

### When to Apply DRY

Apply DRY when two pieces of code represent the **same concept** and must change together:

```csharp
// WRONG -- tax rate duplicated across two services
public sealed class InvoiceService
{
    public decimal CalculateTax(decimal amount) => amount * 0.08m;
}

public sealed class QuoteService
{
    public decimal EstimateTax(decimal amount) => amount * 0.08m;
}

// RIGHT -- single source of truth
public static class TaxRates
{
    public const decimal StandardRate = 0.08m;
}
```

### Rule of Three

Do not abstract prematurely. Wait until you see the same pattern three times before extracting a shared abstraction:

1. **First occurrence** -- write it inline
2. **Second occurrence** -- note the duplication but keep it (the two usages may diverge)
3. **Third occurrence** -- extract a shared method, class, or utility

### When Duplication Is Acceptable

Not all code similarity represents knowledge duplication:

```csharp
// These look similar but represent DIFFERENT business concepts
// They will evolve independently -- DO NOT merge them

public sealed class CustomerValidator
{
    public bool IsValid(Customer customer) =>
        !string.IsNullOrEmpty(customer.Name) &&
        !string.IsNullOrEmpty(customer.Email);
}

public sealed class SupplierValidator
{
    public bool IsValid(Supplier supplier) =>
        !string.IsNullOrEmpty(supplier.Name) &&
        !string.IsNullOrEmpty(supplier.ContactEmail);
}
```

**Acceptable duplication scenarios:**
- Test setup code that looks similar across test classes (coupling tests to shared helpers makes them fragile)
- DTOs for different API versions (V1 and V2 may share fields now but diverge later)
- Configuration for different environments (dev and prod configs that happen to be similar today)
- Mapping code between layers (coupling layers to share mappers defeats the purpose of separate layers)

### Abstracting Shared Behavior

When you do extract, prefer composition over inheritance:

```csharp
// Prefer: composition via a shared utility
public static class StringValidation
{
    public static bool IsNonEmpty(string? value) =>
        !string.IsNullOrWhiteSpace(value);
}

// Over: inheritance via a base class
// (couples validators to a shared base, harder to test independently)
```

---

## Applying the Principles Together

### Decision Guide

| Symptom | Likely Violation | Fix |
|---|---|---|
| Class described with "and" | SRP | Split into focused classes |
| Modifying existing code to add features | OCP | Use strategy/plugin pattern |
| `NotSupportedException` in overrides | LSP | Redesign hierarchy or use composition |
| Empty/throwing interface methods | ISP | Split into role interfaces |
| `new` keyword for dependencies | DIP | Inject via constructor |
| Magic numbers/strings in multiple files | DRY | Extract constants or config |
| Copy-pasted code blocks (3+) | DRY | Extract shared method |

### SRP Compliance Test

For each class, answer these questions:

1. **One-sentence test:** Can you describe the class's purpose in one sentence without "and" or "or"?
2. **Change-reason test:** List all reasons this class might need to change. If more than one, consider splitting.
3. **Dependency count test:** Does the constructor take more than 3-4 dependencies? High parameter counts often signal multiple responsibilities.

---

## Agent Gotchas

1. **Do not create `IFoo`/`Foo` pairs for every class.** DIP calls for abstractions at module boundaries (infrastructure, external services), not for every internal class. Unnecessary interfaces add indirection without value and clutter the codebase.
2. **Do not merge similar-looking code from different bounded contexts.** Two validators or DTOs that look alike but serve different business concepts should remain separate. Premature DRY creates coupling between concepts that evolve independently.
3. **Do not use inheritance to share behavior between unrelated types.** Prefer composition (injecting a shared service or using extension methods) over inheriting from a common base class. Inheritance creates tight coupling and makes LSP violations more likely.
4. **Fat controllers and god classes are SRP violations.** When generating endpoint handlers, keep them thin -- delegate to dedicated services for validation, business logic, and persistence. Apply the "one sentence" test to each class.
5. **Switch statements on type discriminators violate OCP.** Replace them with polymorphism (strategy pattern, interface dispatch) so new types can be added without modifying existing code.
6. **Array covariance in C# is unsafe.** `Animal[] animals = new Dog[10]` compiles but throws `ArrayTypeMismatchException` at runtime when adding non-Dog elements. Use `IReadOnlyList<T>` or `IEnumerable<T>` for covariant read-only access.
7. **Accept the narrowest interface type your method needs.** Use `IEnumerable<T>` for iteration, `IReadOnlyList<T>` for indexed read access, and `IList<T>` only when mutation is required. This follows ISP and makes methods more reusable.

---

## Knowledge Sources

SOLID and DRY guidance in this skill is grounded in publicly available content from:

- **Steve Smith (Ardalis) SOLID Principles** -- Practical SOLID application in .NET with guard clause patterns, specification pattern for OCP compliance, and clean architecture layering that enforces DIP at project boundaries. Source: https://ardalis.com/
- **Jimmy Bogard's Domain-Driven Design Patterns** -- Rich domain model guidance that applies SRP to aggregate design (one aggregate root per bounded context) and OCP to domain event handling (new handlers without modifying existing ones). Note: MediatR is commercial for commercial use; apply the patterns with built-in mechanisms where possible. Source: https://www.jimmybogard.com/

> **Note:** This skill applies publicly documented guidance. It does not represent or speak for the named sources.

## References

- [SOLID Principles in C#](https://learn.microsoft.com/en-us/archive/msdn-magazine/2014/may/csharp-best-practices-dangers-of-violating-solid-principles-in-csharp)
- [Dependency Injection in .NET](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [Covariance and Contravariance in Generics](https://learn.microsoft.com/en-us/dotnet/standard/generics/covariance-and-contravariance)
- [Clean Architecture (Ardalis)](https://github.com/ardalis/CleanArchitecture)

## Attribution

Adapted from [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) (MIT license).
