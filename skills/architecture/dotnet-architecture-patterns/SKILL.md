---
name: dotnet-architecture-patterns
description: "WHEN organizing APIs at scale. Vertical slices, request pipelines, validation, caching, error handling, idempotency."
---

# dotnet-architecture-patterns

Modern architecture patterns for .NET applications. Covers practical approaches to organizing minimal APIs at scale, vertical slice architecture, request pipeline composition, validation strategies, caching, error handling, and idempotency/outbox patterns.

**Out of scope:** DI container mechanics and async/await patterns are owned by fn-3 -- see [skill:dotnet-csharp-dependency-injection] and [skill:dotnet-csharp-async-patterns]. Project scaffolding and file layout are owned by fn-4 -- see [skill:dotnet-scaffold-project]. Testing strategies are owned by fn-7 -- <!-- TODO: fn-7 reconciliation -- replace with canonical [skill:...] IDs when fn-7 lands -->.

Cross-references: [skill:dotnet-csharp-dependency-injection] for service registration and lifetimes, [skill:dotnet-csharp-async-patterns] for async pipeline patterns, [skill:dotnet-csharp-configuration] for Options pattern in configuration.

---

## Vertical Slice Architecture

Organize code by feature (vertical slice) rather than by technical layer (controllers, services, repositories). Each slice owns its endpoint, handler, validation, and data access.

### Directory Structure

```
Features/
  Orders/
    CreateOrder/
      CreateOrderEndpoint.cs
      CreateOrderHandler.cs
      CreateOrderRequest.cs
      CreateOrderValidator.cs
    GetOrder/
      GetOrderEndpoint.cs
      GetOrderHandler.cs
    ListOrders/
      ListOrdersEndpoint.cs
      ListOrdersHandler.cs
  Products/
    GetProduct/
      ...
```

### Why Vertical Slices

- **Low coupling**: changing one feature does not ripple through shared layers
- **Easy navigation**: everything for a feature is in one place
- **Independent testability**: each slice has a clear input/output contract
- **Team scalability**: different developers can work on different features without merge conflicts

### Slice Anatomy

Each slice typically contains:

1. **Request/Response DTOs** -- the contract
2. **Validator** -- input validation rules
3. **Handler** -- business logic
4. **Endpoint** -- HTTP mapping (route, method, status codes)

```csharp
// Features/Orders/CreateOrder/CreateOrderRequest.cs
public sealed record CreateOrderRequest(
    string CustomerId,
    List<OrderLineRequest> Lines);

public sealed record OrderLineRequest(
    string ProductId,
    int Quantity);

// Features/Orders/CreateOrder/CreateOrderResponse.cs
public sealed record CreateOrderResponse(
    string OrderId,
    decimal Total,
    DateTimeOffset CreatedAt);
```

---

## Minimal API Organization at Scale

### Route Group Pattern

Use `MapGroup` to organize related endpoints and apply shared filters:

```csharp
// Program.cs
var app = builder.Build();

app.MapGroup("/api/orders")
   .WithTags("Orders")
   .MapOrderEndpoints();

app.MapGroup("/api/products")
   .WithTags("Products")
   .MapProductEndpoints();

app.Run();
```

```csharp
// Features/Orders/OrderEndpoints.cs
public static class OrderEndpoints
{
    public static RouteGroupBuilder MapOrderEndpoints(this RouteGroupBuilder group)
    {
        group.MapPost("/", CreateOrderEndpoint.Handle)
             .WithName("CreateOrder")
             .Produces<CreateOrderResponse>(StatusCodes.Status201Created)
             .ProducesValidationProblem();

        group.MapGet("/{id}", GetOrderEndpoint.Handle)
             .WithName("GetOrder")
             .Produces<OrderResponse>()
             .ProducesProblem(StatusCodes.Status404NotFound);

        group.MapGet("/", ListOrdersEndpoint.Handle)
             .WithName("ListOrders")
             .Produces<PagedResult<OrderSummary>>();

        return group;
    }
}
```

### Endpoint Classes

Keep each endpoint in its own static class with a single `Handle` method:

```csharp
public static class CreateOrderEndpoint
{
    public static async Task<IResult> Handle(
        CreateOrderRequest request,
        IValidator<CreateOrderRequest> validator,
        IOrderService orderService,
        CancellationToken ct)
    {
        var validation = await validator.ValidateAsync(request, ct);
        if (!validation.IsValid)
        {
            return Results.ValidationProblem(validation.ToDictionary());
        }

        var order = await orderService.CreateAsync(request, ct);

        return Results.Created($"/api/orders/{order.OrderId}", order);
    }
}
```

---

## Request Pipeline Composition

### Endpoint Filters (Middleware for Endpoints)

Use endpoint filters for cross-cutting concerns scoped to specific routes:

```csharp
// Validation filter applied to a route group
public sealed class ValidationFilter<TRequest> : IEndpointFilter
    where TRequest : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var request = context.Arguments.OfType<TRequest>().FirstOrDefault();
        if (request is null)
        {
            return Results.BadRequest();
        }

        var validator = context.HttpContext.RequestServices
            .GetService<IValidator<TRequest>>();

        if (validator is not null)
        {
            var result = await validator.ValidateAsync(request);
            if (!result.IsValid)
            {
                return Results.ValidationProblem(result.ToDictionary());
            }
        }

        return await next(context);
    }
}

// Usage
group.MapPost("/", CreateOrderEndpoint.Handle)
     .AddEndpointFilter<ValidationFilter<CreateOrderRequest>>();
```

### Pipeline Order

The standard middleware pipeline order matters:

```csharp
app.UseExceptionHandler();       // 1. Global error handling
app.UseStatusCodePages();        // 2. Status code formatting
app.UseRateLimiter();            // 3. Rate limiting
app.UseAuthentication();         // 4. Authentication
app.UseAuthorization();          // 5. Authorization
// Endpoint routing happens here
```

---

## Error Handling

### Problem Details (RFC 9457)

Use the built-in Problem Details support for consistent error responses:

```csharp
// Program.cs
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] =
            context.HttpContext.TraceIdentifier;
    };
});

app.UseExceptionHandler();
app.UseStatusCodePages();
```

### Result Pattern for Business Logic

Return a result type from handlers instead of throwing exceptions for expected business failures:

```csharp
public abstract record Result<T>
{
    public sealed record Success(T Value) : Result<T>;
    public sealed record NotFound(string Message) : Result<T>;
    public sealed record ValidationFailed(IDictionary<string, string[]> Errors) : Result<T>;
    public sealed record Conflict(string Message) : Result<T>;
}

// In the handler
public async Task<Result<Order>> CreateAsync(
    CreateOrderRequest request,
    CancellationToken ct)
{
    var customer = await _db.Customers.FindAsync([request.CustomerId], ct);
    if (customer is null)
    {
        return new Result<Order>.NotFound($"Customer {request.CustomerId} not found");
    }

    // ... create order
    return new Result<Order>.Success(order);
}

// In the endpoint -- map result to HTTP response
return result switch
{
    Result<Order>.Success s => Results.Created($"/api/orders/{s.Value.Id}", s.Value),
    Result<Order>.NotFound n => Results.Problem(n.Message, statusCode: 404),
    Result<Order>.ValidationFailed v => Results.ValidationProblem(v.Errors),
    Result<Order>.Conflict c => Results.Problem(c.Message, statusCode: 409),
    _ => Results.Problem("Unexpected error", statusCode: 500)
};
```

---

## Validation Strategy

### FluentValidation Integration

```csharp
// Register validators by assembly scanning
builder.Services.AddValidatorsFromAssemblyContaining<Program>(ServiceLifetime.Scoped);

// Validator implementation
public sealed class CreateOrderValidator : AbstractValidator<CreateOrderRequest>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .MaximumLength(50);

        RuleFor(x => x.Lines)
            .NotEmpty()
            .WithMessage("Order must have at least one line item");

        RuleForEach(x => x.Lines)
            .ChildRules(line =>
            {
                line.RuleFor(l => l.ProductId).NotEmpty();
                line.RuleFor(l => l.Quantity).GreaterThan(0);
            });
    }
}
```

### Data Annotations + MiniValidation (Lighter Alternative)

For simpler scenarios, use data annotations with `MiniValidation`:

```csharp
public sealed record CreateProductRequest(
    [Required, MaxLength(200)] string Name,
    [Range(0.01, double.MaxValue)] decimal Price);

// In endpoint
if (!MiniValidator.TryValidate(request, out var errors))
{
    return Results.ValidationProblem(errors);
}
```

---

## Caching Strategy

### Output Caching (HTTP Response Caching)

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(p => p.NoCache());

    options.AddPolicy("ProductList", p =>
        p.Expire(TimeSpan.FromMinutes(5))
         .Tag("products"));

    options.AddPolicy("ProductDetail", p =>
        p.Expire(TimeSpan.FromMinutes(10))
         .SetVaryByRouteValue("id")
         .Tag("products"));
});

app.UseOutputCache();

// Apply to endpoints
group.MapGet("/", ListProductsEndpoint.Handle)
     .CacheOutput("ProductList");

group.MapGet("/{id}", GetProductEndpoint.Handle)
     .CacheOutput("ProductDetail");

// Invalidate by tag
app.MapPost("/api/products", async (
    IOutputCacheStore cache,
    /* ... */) =>
{
    // ... create product
    await cache.EvictByTagAsync("products", ct);
    return Results.Created(/* ... */);
});
```

### Distributed Caching (Application-Level)

```csharp
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration
        .GetConnectionString("Redis");
});

// Usage with IDistributedCache
public sealed class ProductService(
    IDistributedCache cache,
    AppDbContext db)
{
    public async Task<Product?> GetByIdAsync(
        string id, CancellationToken ct = default)
    {
        var cacheKey = $"product:{id}";
        var cached = await cache.GetStringAsync(cacheKey, ct);

        if (cached is not null)
        {
            return JsonSerializer.Deserialize<Product>(cached);
        }

        var product = await db.Products.FindAsync([id], ct);
        if (product is not null)
        {
            await cache.SetStringAsync(
                cacheKey,
                JsonSerializer.Serialize(product),
                new DistributedCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
                },
                ct);
        }

        return product;
    }
}
```

### HybridCache (.NET 9+)

`HybridCache` combines L1 (in-memory) and L2 (distributed) caching with stampede protection:

```csharp
builder.Services.AddHybridCache(options =>
{
    options.DefaultEntryOptions = new HybridCacheEntryOptions
    {
        Expiration = TimeSpan.FromMinutes(10),
        LocalCacheExpiration = TimeSpan.FromMinutes(2)
    };
});

// Usage -- stampede-safe, two-tier
public sealed class ProductService(HybridCache cache, AppDbContext db)
{
    public async Task<Product?> GetByIdAsync(
        string id, CancellationToken ct = default)
    {
        return await cache.GetOrCreateAsync(
            $"product:{id}",
            async cancel => await db.Products.FindAsync([id], cancel),
            cancellationToken: ct);
    }
}
```

---

## Idempotency and Outbox Pattern

### Idempotency Keys

Prevent duplicate processing of retried requests. A robust idempotency implementation must:

1. **Scope keys** by route + user/tenant to prevent cross-endpoint collisions
2. **Atomically claim** the key before executing, so concurrent duplicates are rejected
3. **Store a concrete response envelope** (not an `IResult` reference) for safe replay

#### Database-Backed Idempotency (Recommended)

Use a database row with a unique constraint for atomic claim-then-execute:

```csharp
// Idempotency record stored alongside domain data
public sealed class IdempotencyRecord
{
    public required string Key { get; init; }         // Scoped key
    public required string RequestRoute { get; init; }
    public required string? UserId { get; init; }
    public int StatusCode { get; set; }
    public string? ResponseBody { get; set; }         // Serialized JSON
    public string? ContentType { get; set; }
    public DateTimeOffset CreatedAt { get; init; } = DateTimeOffset.UtcNow;
    public bool IsCompleted { get; set; }
}

public sealed class IdempotencyFilter(AppDbContext db) : IEndpointFilter
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var httpContext = context.HttpContext;
        if (!httpContext.Request.Headers.TryGetValue(
            "Idempotency-Key", out var keyValues))
        {
            return await next(context);
        }

        var clientKey = keyValues.ToString();
        if (string.IsNullOrWhiteSpace(clientKey) || clientKey.Length > 256)
        {
            return Results.Problem("Invalid Idempotency-Key", statusCode: 400);
        }

        // Scope key by route + user to prevent cross-endpoint/cross-tenant collisions
        var route = $"{httpContext.Request.Method}:{httpContext.Request.Path}";
        var userId = httpContext.User.FindFirst("sub")?.Value ?? "anonymous";
        var scopedKey = $"{route}:{userId}:{clientKey}";

        // Check for existing record (completed = replay, in-progress = reject)
        var existing = await db.IdempotencyRecords
            .FirstOrDefaultAsync(r => r.Key == scopedKey);

        if (existing is { IsCompleted: true })
        {
            return Results.Text(
                existing.ResponseBody ?? "",
                existing.ContentType ?? "application/json",
                statusCode: existing.StatusCode);
        }

        if (existing is { IsCompleted: false })
        {
            // Another request claimed this key but hasn't completed yet.
            // Reject to prevent duplicate execution.
            return Results.Problem(
                "Duplicate request in progress", statusCode: 409);
        }

        // Atomic claim: insert with unique constraint -- concurrent duplicate
        // requests will throw DbUpdateException and get a 409 Conflict
        {
            var record = new IdempotencyRecord
            {
                Key = scopedKey,
                RequestRoute = route,
                UserId = userId,
                IsCompleted = false
            };
            db.IdempotencyRecords.Add(record);

            try
            {
                await db.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                return Results.Problem(
                    "Duplicate request in progress", statusCode: 409);
            }

            existing = record;
        }

        // Execute the actual handler
        var result = await next(context);

        // Capture concrete response envelope for replay
        if (result is IStatusCodeHttpResult statusResult
            && result is IValueHttpResult valueResult)
        {
            existing.StatusCode = statusResult.StatusCode ?? 200;
            existing.ResponseBody = JsonSerializer.Serialize(valueResult.Value);
            existing.ContentType = "application/json";
            existing.IsCompleted = true;
            await db.SaveChangesAsync();
        }

        return result;
    }
}
```

**Key design choices:**
- **Three states**: no record (claim it), in-progress (reject 409), completed (replay cached response)
- Unique constraint on `Key` column provides atomic claim without distributed locks
- Scoped key (`route:userId:clientKey`) prevents cross-endpoint and cross-tenant collisions
- Response envelope stores serialized body + status code + content type (not `IResult` references)
- In-progress records (claimed but not completed) return 409 to concurrent duplicates
- Consider adding a stale-record cleanup job to handle abandoned in-progress records (e.g., process crashed mid-execution)

### Transactional Outbox Pattern

Guarantee at-least-once delivery of domain events alongside database writes:

```csharp
// 1. Store outbox messages in the same transaction as the domain write
public sealed class OutboxMessage
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public required string EventType { get; init; }
    public required string Payload { get; init; }
    public DateTimeOffset CreatedAt { get; init; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? ProcessedAt { get; set; }
}

// 2. In the handler -- same DbContext transaction
public async Task<Order> CreateOrderAsync(
    CreateOrderRequest request,
    CancellationToken ct)
{
    await using var transaction = await _db.Database
        .BeginTransactionAsync(ct);

    var order = new Order { /* ... */ };
    _db.Orders.Add(order);

    _db.OutboxMessages.Add(new OutboxMessage
    {
        EventType = "OrderCreated",
        Payload = JsonSerializer.Serialize(
            new OrderCreatedEvent(order.Id, order.Total))
    });

    await _db.SaveChangesAsync(ct);
    await transaction.CommitAsync(ct);

    return order;
}

// 3. Background processor publishes outbox messages
// See [skill:dotnet-background-services] for the Channels-based
// processor that polls and publishes these messages.
```

The outbox pattern ensures that if the database write succeeds, the event is guaranteed to be published (eventually), even if the message broker is temporarily unavailable.

---

## Key Principles

- **Prefer composition over inheritance** -- use endpoint filters, middleware, and pipeline composition rather than base classes
- **Keep slices independent** -- avoid shared abstractions that couple features together
- **Validate early, fail fast** -- validate at the boundary (endpoint filters) before entering business logic
- **Use Problem Details everywhere** -- consistent error format across all endpoints
- **Cache at the right level** -- output cache for HTTP responses, distributed cache for shared state, HybridCache for both
- **Make writes idempotent** -- use idempotency keys for any non-idempotent operation clients may retry

---

## References

- [ASP.NET Core Best Practices](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0)
- [Minimal APIs overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/overview)
- [Output caching middleware](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output)
- [HybridCache library](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid)
- [Problem Details (RFC 9457)](https://www.rfc-editor.org/rfc/rfc9457)
- [Endpoint filters in minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/min-api-filters)
