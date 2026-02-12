---
name: dotnet-background-services
description: "WHEN implementing background work. BackgroundService, IHostedService, Channels producer/consumer, graceful shutdown."
---

# dotnet-background-services

Patterns for long-running background work in .NET applications. Covers `BackgroundService`, `IHostedService`, `System.Threading.Channels` for producer/consumer queues, and graceful shutdown handling.

**Out of scope:** DI registration mechanics and service lifetimes are owned by fn-3 -- see [skill:dotnet-csharp-dependency-injection]. Async/await patterns and cancellation token propagation are owned by fn-3 -- see [skill:dotnet-csharp-async-patterns]. Project scaffolding is owned by fn-4 -- see [skill:dotnet-scaffold-project]. Testing strategies for background services are owned by fn-7 -- <!-- TODO: fn-7 reconciliation -- replace with canonical [skill:...] IDs when fn-7 lands -->.

Cross-references: [skill:dotnet-csharp-async-patterns] for async patterns in background workers, [skill:dotnet-csharp-dependency-injection] for hosted service registration and scope management.

---

## BackgroundService vs IHostedService

| Feature | `BackgroundService` | `IHostedService` |
|---------|-------------------|-----------------|
| Purpose | Long-running loop or continuous work | Startup/shutdown hooks |
| Methods | Override `ExecuteAsync` | Implement `StartAsync` + `StopAsync` |
| Lifetime | Runs until cancellation or host shutdown | `StartAsync` runs at startup, `StopAsync` at shutdown |
| Use when | Polling queues, processing streams, periodic jobs | Database migrations, cache warming, resource cleanup |

---

## BackgroundService Patterns

### Basic Polling Worker

```csharp
public sealed class OrderProcessorWorker(
    IServiceScopeFactory scopeFactory,
    ILogger<OrderProcessorWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("Order processor started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                using var scope = scopeFactory.CreateScope();
                var processor = scope.ServiceProvider
                    .GetRequiredService<IOrderProcessor>();

                var processed = await processor.ProcessPendingAsync(stoppingToken);

                if (processed == 0)
                {
                    // No work available -- back off to avoid tight polling
                    await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);
                }
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                // Expected during shutdown -- do not log as error
                break;
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error processing orders");
                // Back off on error to prevent tight failure loops
                await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
            }
        }

        logger.LogInformation("Order processor stopped");
    }
}

// Registration
builder.Services.AddHostedService<OrderProcessorWorker>();
```

### Critical Rules for BackgroundService

1. **Always create scopes** -- `BackgroundService` is registered as a singleton. Inject `IServiceScopeFactory`, not scoped services directly.
2. **Always handle exceptions** -- unhandled exceptions in `ExecuteAsync` stop the host (net8.0+). Wrap the loop body in try/catch.
3. **Always respect the stopping token** -- check `stoppingToken.IsCancellationRequested` and pass the token to all async calls.
4. **Back off on empty/error** -- avoid tight polling loops that waste CPU. Use `Task.Delay` with the stopping token.

---

## IHostedService Patterns

### Startup Hook (Cache Warming, Migrations)

```csharp
public sealed class CacheWarmupService(
    IServiceScopeFactory scopeFactory,
    ILogger<CacheWarmupService> logger) : IHostedService
{
    public async Task StartAsync(CancellationToken cancellationToken)
    {
        logger.LogInformation("Warming caches");

        using var scope = scopeFactory.CreateScope();
        var cache = scope.ServiceProvider.GetRequiredService<IProductCache>();
        await cache.WarmAsync(cancellationToken);

        logger.LogInformation("Cache warmup complete");
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}
```

### Startup + Shutdown (Resource Lifecycle)

```csharp
public sealed class MessageBusService(
    ILogger<MessageBusService> logger) : IHostedService
{
    private IConnection? _connection;

    public async Task StartAsync(CancellationToken cancellationToken)
    {
        logger.LogInformation("Connecting to message bus");
        _connection = await CreateConnectionAsync(cancellationToken);
    }

    public async Task StopAsync(CancellationToken cancellationToken)
    {
        logger.LogInformation("Disconnecting from message bus");
        if (_connection is not null)
        {
            await _connection.CloseAsync(cancellationToken);
            _connection = null;
        }
    }

    private static Task<IConnection> CreateConnectionAsync(
        CancellationToken ct)
    {
        // Connection setup logic
        throw new NotImplementedException();
    }
}
```

---

## Hosted Service Lifecycle

Understanding the startup and shutdown sequence is critical for correct behavior.

### Startup Sequence

1. `IHostedService.StartAsync` is called for each registered service **in registration order**
2. `BackgroundService.ExecuteAsync` is called after `StartAsync` completes (it runs concurrently -- the host does not wait for it to finish)
3. The host is ready to serve requests after all `StartAsync` calls complete

**Important:** `ExecuteAsync` must not block before yielding to the caller. The first `await` in `ExecuteAsync` is where control returns to the host. If you have synchronous setup before the first `await`, keep it short or move it to `StartAsync` via an override.

```csharp
public sealed class MyWorker : BackgroundService
{
    // StartAsync runs to completion before the host is ready.
    // Override only if you need guaranteed pre-ready initialization.
    public override async Task StartAsync(CancellationToken cancellationToken)
    {
        // Initialization that MUST complete before host accepts requests
        await InitializeAsync(cancellationToken);
        await base.StartAsync(cancellationToken);
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        // This runs concurrently with the host
        while (!stoppingToken.IsCancellationRequested)
        {
            await DoWorkAsync(stoppingToken);
        }
    }

    private Task InitializeAsync(CancellationToken ct) => Task.CompletedTask;
    private Task DoWorkAsync(CancellationToken ct) => Task.CompletedTask;
}
```

### Shutdown Sequence

1. `IHostApplicationLifetime.ApplicationStopping` is triggered
2. The host calls `StopAsync` on each hosted service **in reverse registration order**
3. For `BackgroundService`, the stopping token is cancelled, then `StopAsync` waits for `ExecuteAsync` to complete
4. `IHostApplicationLifetime.ApplicationStopped` is triggered

---

## Channels-Based Producer/Consumer

`System.Threading.Channels` provides a high-performance, thread-safe producer/consumer queue that is ideal for decoupling work submission from processing.

### Background Work Queue

```csharp
// The queue abstraction
public interface IBackgroundTaskQueue
{
    ValueTask EnqueueAsync(
        Func<IServiceProvider, CancellationToken, Task> workItem,
        CancellationToken ct = default);

    ValueTask<Func<IServiceProvider, CancellationToken, Task>> DequeueAsync(
        CancellationToken ct);
}

// Channel-backed implementation
public sealed class BackgroundTaskQueue : IBackgroundTaskQueue
{
    private readonly Channel<Func<IServiceProvider, CancellationToken, Task>> _queue;

    public BackgroundTaskQueue(int capacity = 100)
    {
        var options = new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait,  // Back-pressure
            SingleReader = false,
            SingleWriter = false
        };

        _queue = Channel.CreateBounded<Func<IServiceProvider, CancellationToken, Task>>(options);
    }

    public ValueTask EnqueueAsync(
        Func<IServiceProvider, CancellationToken, Task> workItem,
        CancellationToken ct = default)
    {
        ArgumentNullException.ThrowIfNull(workItem);
        return _queue.Writer.WriteAsync(workItem, ct);
    }

    public ValueTask<Func<IServiceProvider, CancellationToken, Task>> DequeueAsync(
        CancellationToken ct)
    {
        return _queue.Reader.ReadAsync(ct);
    }
}
```

### Channel Consumer Worker

```csharp
public sealed class QueueProcessorWorker(
    IBackgroundTaskQueue taskQueue,
    IServiceScopeFactory scopeFactory,
    ILogger<QueueProcessorWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("Queue processor started, waiting for work items");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var workItem = await taskQueue.DequeueAsync(stoppingToken);

                using var scope = scopeFactory.CreateScope();
                await workItem(scope.ServiceProvider, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error executing queued work item");
            }
        }

        logger.LogInformation("Queue processor stopped");
    }
}
```

### Producer (Enqueueing Work)

```csharp
// In an endpoint -- offload slow work to background
app.MapPost("/api/orders/{id}/notify", async (
    string id,
    IBackgroundTaskQueue queue,
    CancellationToken ct) =>
{
    await queue.EnqueueAsync(async (sp, token) =>
    {
        var notifier = sp.GetRequiredService<IOrderNotifier>();
        await notifier.SendNotificationsAsync(id, token);
    }, ct);

    return Results.Accepted();
});
```

### Registration

```csharp
builder.Services.AddSingleton<IBackgroundTaskQueue>(
    new BackgroundTaskQueue(capacity: 100));
builder.Services.AddHostedService<QueueProcessorWorker>();
```

### Channel Options

| Option | Bounded | Unbounded |
|--------|---------|-----------|
| Back-pressure | Yes (`FullMode` controls behavior) | No (unbounded growth risk) |
| Memory safety | Capped at `capacity` items | Can exhaust memory |
| Use when | Production workloads | Prototyping or guaranteed-low-volume |

```csharp
// Bounded -- preferred for production
Channel.CreateBounded<T>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait,     // Block producer until space
    // Alternatives:
    // FullMode = BoundedChannelFullMode.DropOldest  // Drop oldest item
    // FullMode = BoundedChannelFullMode.DropNewest  // Drop the item being written
    // FullMode = BoundedChannelFullMode.DropWrite   // Drop and return false
});

// Unbounded -- use only when you control the producer rate
Channel.CreateUnbounded<T>(new UnboundedChannelOptions
{
    SingleReader = true,   // Optimization when only one consumer
    SingleWriter = false
});
```

---

## Multiple Consumers (Fan-Out)

Scale processing by running multiple consumer instances:

```csharp
public sealed class ScaledQueueProcessor(
    IBackgroundTaskQueue taskQueue,
    IServiceScopeFactory scopeFactory,
    ILogger<ScaledQueueProcessor> logger) : BackgroundService
{
    private const int WorkerCount = 3;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation(
            "Starting {WorkerCount} queue consumers", WorkerCount);

        var workers = Enumerable.Range(0, WorkerCount)
            .Select(i => ProcessQueueAsync(i, stoppingToken));

        await Task.WhenAll(workers);
    }

    private async Task ProcessQueueAsync(
        int workerId, CancellationToken ct)
    {
        logger.LogDebug("Consumer {WorkerId} started", workerId);

        while (!ct.IsCancellationRequested)
        {
            try
            {
                var workItem = await taskQueue.DequeueAsync(ct);
                using var scope = scopeFactory.CreateScope();
                await workItem(scope.ServiceProvider, ct);
            }
            catch (OperationCanceledException) when (ct.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                logger.LogError(ex,
                    "Consumer {WorkerId}: error processing work item", workerId);
            }
        }

        logger.LogDebug("Consumer {WorkerId} stopped", workerId);
    }
}
```

---

## Graceful Shutdown

### Host Shutdown Timeout

By default, the host waits 30 seconds for services to stop. Configure this for long-running operations:

```csharp
builder.Services.Configure<HostOptions>(options =>
{
    options.ShutdownTimeout = TimeSpan.FromSeconds(60);
});
```

### Drain Pattern for Channels

Complete the writer to signal no more items, then drain remaining items before stopping:

```csharp
public sealed class GracefulQueueProcessor(
    IBackgroundTaskQueue taskQueue,
    IServiceScopeFactory scopeFactory,
    ILogger<GracefulQueueProcessor> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("Queue processor started");

        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                var workItem = await taskQueue.DequeueAsync(stoppingToken);
                using var scope = scopeFactory.CreateScope();
                await workItem(scope.ServiceProvider, stoppingToken);
            }
        }
        catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
        {
            // Shutdown requested -- fall through to drain
        }

        // Drain: process remaining items with a deadline
        logger.LogInformation("Draining remaining work items");
        using var drainCts = new CancellationTokenSource(TimeSpan.FromSeconds(25));

        while (taskQueue.TryDequeue(out var remaining))
        {
            try
            {
                using var scope = scopeFactory.CreateScope();
                await remaining(scope.ServiceProvider, drainCts.Token);
            }
            catch (Exception ex)
            {
                logger.LogWarning(ex, "Error during drain");
            }
        }

        logger.LogInformation("Queue processor stopped, drain complete");
    }
}
```

### Responding to Application Lifetime Events

```csharp
public sealed class LifecycleLogger(
    IHostApplicationLifetime lifetime,
    ILogger<LifecycleLogger> logger) : IHostedService
{
    public Task StartAsync(CancellationToken cancellationToken)
    {
        lifetime.ApplicationStarted.Register(() =>
            logger.LogInformation("Application started"));

        lifetime.ApplicationStopping.Register(() =>
            logger.LogInformation("Application stopping -- begin cleanup"));

        lifetime.ApplicationStopped.Register(() =>
            logger.LogInformation("Application stopped -- cleanup complete"));

        return Task.CompletedTask;
    }

    public Task StopAsync(CancellationToken cancellationToken) => Task.CompletedTask;
}
```

---

## Periodic Work with PeriodicTimer

Use `PeriodicTimer` instead of `Task.Delay` for more accurate periodic execution:

```csharp
public sealed class HealthCheckReporter(
    IServiceScopeFactory scopeFactory,
    ILogger<HealthCheckReporter> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(TimeSpan.FromMinutes(1));

        while (await timer.WaitForNextTickAsync(stoppingToken))
        {
            try
            {
                using var scope = scopeFactory.CreateScope();
                var reporter = scope.ServiceProvider
                    .GetRequiredService<IHealthReporter>();
                await reporter.ReportAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Health check report failed");
            }
        }
    }
}
```

---

## Agent Gotchas

1. **Do not inject scoped services into BackgroundService constructors** -- they are singletons. Always use `IServiceScopeFactory`.
2. **Do not use `Task.Run` for background work** -- use `BackgroundService` for proper lifecycle management and graceful shutdown.
3. **Do not swallow `OperationCanceledException`** -- let it propagate or re-check the stopping token. Swallowing it prevents graceful shutdown.
4. **Do not use `Thread.Sleep`** -- use `await Task.Delay(duration, stoppingToken)` or `PeriodicTimer`.
5. **Do not forget to register** -- `AddHostedService<T>()` is required; merely implementing the interface does nothing.

---

## References

- [Background tasks with hosted services](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/host/hosted-services)
- [System.Threading.Channels](https://learn.microsoft.com/en-us/dotnet/core/extensions/channels)
- [BackgroundService](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.backgroundservice)
- [IHostedService interface](https://learn.microsoft.com/en-us/dotnet/api/microsoft.extensions.hosting.ihostedservice)
- [Generic host shutdown](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host#host-shutdown)
- [PeriodicTimer](https://learn.microsoft.com/en-us/dotnet/api/system.threading.periodictimer)
