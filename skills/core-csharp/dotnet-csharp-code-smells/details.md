# dotnet-csharp-code-smells -- Detailed Examples

Code examples for each anti-pattern category. Each section shows the bad pattern followed by the correct fix.

---

## 1. Resource Management (IDisposable)

### Missing `using` on Disposable Local (CA2000)

```csharp
// BAD: StreamReader is never disposed if an exception occurs
public string ReadFile(string path)
{
    var reader = new StreamReader(path);
    return reader.ReadToEnd();  // reader leaked on exception or normal exit
}

// FIX: using declaration ensures disposal
public string ReadFile(string path)
{
    using var reader = new StreamReader(path);
    return reader.ReadToEnd();
}
```

### Undisposed IDisposable Fields (CA2213)

```csharp
// BAD: _timer is never disposed
public class PollingService
{
    private readonly Timer _timer = new(Callback, null, TimeSpan.Zero, TimeSpan.FromSeconds(30));

    private static void Callback(object? state) { /* ... */ }
}

// FIX: implement IDisposable and dispose the field
public sealed class PollingService : IDisposable
{
    private readonly Timer _timer = new(Callback, null, TimeSpan.Zero, TimeSpan.FromSeconds(30));

    private static void Callback(object? state) { /* ... */ }

    public void Dispose() => _timer.Dispose();
}
```

### Canonical Dispose Pattern (for unsealed classes)

```csharp
public class ResourceHolder : IDisposable
{
    private SafeHandle? _handle;
    private bool _disposed;

    public void Dispose()
    {
        Dispose(disposing: true);
        GC.SuppressFinalize(this);  // CA1816
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed) return;

        if (disposing)
        {
            _handle?.Dispose();
        }

        _disposed = true;
    }
}
```

---

## 2. Warning Suppression Hacks

### CS0067: Event Never Used -- Suppression via Null Invoke (Motivating Example)

This is a real-world anti-pattern where a developer invokes an event with `null` arguments solely to suppress compiler warning CS0067 ("The event is never used").

```csharp
// BAD: invoking event with null to suppress CS0067
// Creates misleading runtime behavior -- subscribers receive null args
public class SuppressWarnings
{
    public event EventHandler<EventArgs> MyEvent;

    public SuppressWarnings()
    {
        // This "works" to suppress the warning but:
        // 1. Fires the event with null sender during construction
        // 2. Subscribers (if any) receive unexpected null args
        // 3. Masks the real issue: the event may be genuinely unused
        MyEvent?.Invoke(null, EventArgs.Empty);
    }
}
```

**Correct alternatives:**

```csharp
// FIX Option 1: #pragma warning disable (preferred when event is needed for interface compliance)
public class SuppressWarnings
{
#pragma warning disable CS0067 // Event is required by INotifyPropertyChanged but raised via helper
    public event EventHandler<EventArgs> MyEvent;
#pragma warning restore CS0067
}

// FIX Option 2: Explicit event accessors (preferred when event is a no-op by design)
public class SuppressWarnings
{
    public event EventHandler<EventArgs> MyEvent { add { } remove { } }
}

// FIX Option 3: If the event is truly unused, remove it entirely
```

---

## 3. LINQ Anti-Patterns

### Premature `.ToList()` Mid-Chain

```csharp
// BAD: materializes full list before filtering
var result = orders
    .ToList()           // forces full materialization
    .Where(o => o.IsActive)
    .Select(o => o.Id)
    .ToList();

// FIX: keep chain lazy, materialize only at the end
var result = orders
    .Where(o => o.IsActive)
    .Select(o => o.Id)
    .ToList();
```

### Multiple Enumeration of IEnumerable (CA1851)

```csharp
// BAD: enumerates the sequence twice
public void Process(IEnumerable<Order> orders)
{
    Console.WriteLine($"Count: {orders.Count()}");  // first enumeration
    foreach (var order in orders)                     // second enumeration
    {
        Handle(order);
    }
}

// FIX: materialize once
public void Process(IEnumerable<Order> orders)
{
    var orderList = orders.ToList();
    Console.WriteLine($"Count: {orderList.Count}");
    foreach (var order in orderList)
    {
        Handle(order);
    }
}
```

### Client-Side Evaluation in EF Core

```csharp
// BAD: CustomFormat() cannot be translated to SQL; entire table loaded into memory
var names = dbContext.Customers
    .Where(c => CustomFormat(c.Name).StartsWith("VIP"))
    .ToListAsync();

// FIX: use translatable expressions or filter after explicit load
var names = await dbContext.Customers
    .Where(c => c.Name.StartsWith("VIP"))  // translatable to SQL
    .ToListAsync();
```

---

## 4. Event Handling Leaks

### Not Unsubscribing from Events

```csharp
// BAD: subscriber never unsubscribes; publisher holds reference forever
public class Dashboard
{
    public Dashboard(OrderService service)
    {
        service.OrderCreated += OnOrderCreated;
        // If Dashboard is disposed but OrderService lives on,
        // Dashboard is never garbage collected
    }

    private void OnOrderCreated(object? sender, OrderEventArgs e) { /* ... */ }
}

// FIX: implement IDisposable and unsubscribe
public sealed class Dashboard : IDisposable
{
    private readonly OrderService _service;

    public Dashboard(OrderService service)
    {
        _service = service;
        _service.OrderCreated += OnOrderCreated;
    }

    private void OnOrderCreated(object? sender, OrderEventArgs e) { /* ... */ }

    public void Dispose()
    {
        _service.OrderCreated -= OnOrderCreated;
    }
}
```

### Async Void Event Handler Exception Handling

```csharp
// BAD: async void with no exception handling; crashes the process
private async void OnButtonClick(object? sender, EventArgs e)
{
    await ProcessOrderAsync();  // unhandled exception terminates app
}

// FIX: wrap in try/catch since async void exceptions are unobservable
private async void OnButtonClick(object? sender, EventArgs e)
{
    try
    {
        await ProcessOrderAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to process order on button click");
        // Show user-facing error or handle gracefully
    }
}
```

---

## 5. Async Exception Routing (Motivating Example)

### TryEnqueue with Async Lambda -- Exceptions Lost

This is a real-world anti-pattern where exceptions inside an async lambda are silently lost because they are not routed through a `TaskCompletionSource`.

```csharp
// BAD: exception inside async lambda is never observed
public Task<int> ComputeOnUiThreadAsync()
{
    var tcs = new TaskCompletionSource<int>();

    dispatcherQueue.TryEnqueue(async () =>
    {
        // If DoWorkAsync() throws, the exception is swallowed.
        // The tcs never completes -- caller hangs forever.
        var result = await DoWorkAsync();
        tcs.SetResult(result);
    });

    return tcs.Task;
}

// FIX: route exceptions through the TaskCompletionSource
public Task<int> ComputeOnUiThreadAsync()
{
    var tcs = new TaskCompletionSource<int>();

    dispatcherQueue.TryEnqueue(async () =>
    {
        try
        {
            var result = await DoWorkAsync();
            tcs.SetResult(result);
        }
        catch (OperationCanceledException)
        {
            tcs.TrySetCanceled();
        }
        catch (Exception ex)
        {
            tcs.TrySetException(ex);
        }
    });

    return tcs.Task;
}
```

Cross-reference: See [skill:dotnet-csharp-async-patterns] for broader async exception handling patterns.

---

## 6. Exception Handling Gaps

### Empty Catch Block

```csharp
// BAD: silently swallows all errors
try
{
    await SaveOrderAsync(order);
}
catch (Exception)
{
    // nothing -- caller thinks save succeeded
}

// FIX: at minimum log; preferably re-throw or return error
try
{
    await SaveOrderAsync(order);
}
catch (DbUpdateException ex)
{
    _logger.LogError(ex, "Failed to save order {OrderId}", order.Id);
    throw;  // let caller handle the failure
}
```

### `throw ex;` Resets Stack Trace (CA2200)

```csharp
// BAD: resets stack trace
catch (Exception ex)
{
    _logger.LogError(ex, "Operation failed");
    throw ex;  // CA2200: stack trace lost
}

// FIX: bare throw preserves stack trace
catch (Exception ex)
{
    _logger.LogError(ex, "Operation failed");
    throw;  // preserves original stack trace
}
```

### Throwing in Finally

```csharp
// BAD: exception in finally masks the original exception
try
{
    await ProcessAsync();
}
finally
{
    CleanupThatMayThrow();  // if this throws, original exception is lost
}

// FIX: guard the finally block
try
{
    await ProcessAsync();
}
finally
{
    try
    {
        CleanupThatMayThrow();
    }
    catch (Exception ex)
    {
        _logger.LogWarning(ex, "Cleanup failed; original exception preserved");
    }
}
```

---

## 7. Design Smells

### Long Parameter List -- Introduce Parameter Object

```csharp
// BAD: 7 parameters -- hard to call correctly, easy to swap arguments
public Order CreateOrder(
    string customerId, string productId, int quantity,
    decimal price, string currency, string shippingAddress,
    DateTime requestedDelivery)
{ /* ... */ }

// FIX: introduce a parameter object
public sealed record CreateOrderRequest(
    string CustomerId,
    string ProductId,
    int Quantity,
    decimal Price,
    string Currency,
    string ShippingAddress,
    DateTime RequestedDelivery);

public Order CreateOrder(CreateOrderRequest request) { /* ... */ }
```

### Deep Nesting -- Use Guard Clauses

```csharp
// BAD: deeply nested logic
public decimal CalculateDiscount(Order order)
{
    if (order != null)
    {
        if (order.Customer != null)
        {
            if (order.Customer.IsPremium)
            {
                if (order.Total > 100)
                {
                    return order.Total * 0.1m;
                }
            }
        }
    }
    return 0;
}

// FIX: guard clauses for early return
public decimal CalculateDiscount(Order order)
{
    if (order?.Customer is not { IsPremium: true })
    {
        return 0;
    }

    if (order.Total <= 100)
    {
        return 0;
    }

    return order.Total * 0.1m;
}
```
