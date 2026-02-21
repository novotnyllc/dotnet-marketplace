# dotnet-observability -- Detailed Examples

Extended code examples for distributed tracing, custom metrics, structured logging, health checks, and production configuration.

---

## Distributed Tracing

### How .NET Tracing Works

.NET uses `System.Diagnostics.Activity` as its native tracing primitive. OpenTelemetry maps these to spans:

| .NET Concept | OpenTelemetry Concept |
|---|---|
| `ActivitySource` | Tracer |
| `Activity` | Span |
| `Activity.SetTag` | Span attribute |
| `Activity.AddEvent` | Span event |
| `Activity.SetStatus` | Span status |

### Custom Traces

```csharp
public sealed class OrderService
{
    // One ActivitySource per logical component, named after the namespace
    private static readonly ActivitySource s_activitySource = new("MyApp.Orders");

    public async Task<Order> CreateOrderAsync(
        CreateOrderRequest request,
        CancellationToken ct)
    {
        using var activity = s_activitySource.StartActivity(
            "CreateOrder",
            ActivityKind.Internal);

        activity?.SetTag("order.customer_id", request.CustomerId);
        activity?.SetTag("order.line_count", request.Lines.Count);

        var order = new Order { /* ... */ };

        activity?.AddEvent(new ActivityEvent("OrderValidated"));

        await _db.Orders.AddAsync(order, ct);
        await _db.SaveChangesAsync(ct);

        activity?.SetTag("order.id", order.Id);
        activity?.SetStatus(ActivityStatusCode.Ok);

        return order;
    }
}
```

### Trace Context Propagation

W3C Trace Context is the default propagation format in .NET. It works automatically across HTTP boundaries with `HttpClient`:

```csharp
// Trace context is automatically propagated via traceparent/tracestate headers
// when using HttpClient with OpenTelemetry.Instrumentation.Http.
// No manual propagation needed for HTTP-based communication.
```

For message-based communication (queues, event buses), propagate context explicitly:

```csharp
// Producer: inject context into message headers
var propagator = Propagators.DefaultTextMapPropagator;
var carrier = new Dictionary<string, string>();
var currentActivity = Activity.Current;
if (currentActivity is not null)
{
    propagator.Inject(
        new PropagationContext(currentActivity.Context, Baggage.Current),
        carrier,
        (dict, key, value) => dict[key] = value);
}
// Attach carrier as message headers

// Consumer: extract context from message headers
var parentContext = propagator.Extract(
    default,
    messageHeaders,
    (headers, key) => headers.TryGetValue(key, out var value)
        ? [value] : []);

using var activity = s_activitySource.StartActivity(
    "ProcessMessage",
    ActivityKind.Consumer,
    parentContext.ActivityContext);
```

---

## Metrics

### Built-in Metrics

ASP.NET Core and HttpClient emit metrics automatically when OpenTelemetry instrumentation is configured:

| Meter | Key Metrics |
|-------|-------------|
| `Microsoft.AspNetCore.Hosting` | `http.server.request.duration`, `http.server.active_requests` |
| `Microsoft.AspNetCore.Routing` | `aspnetcore.routing.match_attempts` |
| `System.Net.Http` | `http.client.request.duration`, `http.client.active_requests` |
| `System.Runtime` | `process.runtime.dotnet.gc.collections.count`, `process.runtime.dotnet.threadpool.threads.count` |

### Custom Metrics

Use `System.Diagnostics.Metrics` for application-specific metrics:

```csharp
public sealed class OrderMetrics
{
    // One Meter per logical component
    private readonly Counter<long> _ordersCreated;
    private readonly Histogram<double> _orderProcessingDuration;
    private readonly UpDownCounter<long> _activeOrders;

    public OrderMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("MyApp.Orders");

        _ordersCreated = meter.CreateCounter<long>(
            "myapp.orders.created",
            unit: "{order}",
            description: "Number of orders created");

        _orderProcessingDuration = meter.CreateHistogram<double>(
            "myapp.orders.processing_duration",
            unit: "s",
            description: "Time to process an order");

        _activeOrders = meter.CreateUpDownCounter<long>(
            "myapp.orders.active",
            unit: "{order}",
            description: "Number of orders currently being processed");
    }

    public void RecordOrderCreated(string region)
    {
        _ordersCreated.Add(1, new KeyValuePair<string, object?>("region", region));
    }

    public void RecordProcessingDuration(double seconds)
    {
        _orderProcessingDuration.Record(seconds);
    }

    public void IncrementActiveOrders() => _activeOrders.Add(1);
    public void DecrementActiveOrders() => _activeOrders.Add(-1);
}
```

Register the metrics class in DI:

```csharp
builder.Services.AddSingleton<OrderMetrics>();
```

### Metric Naming Conventions

Follow the OpenTelemetry semantic conventions:

- Use lowercase with dots as separators: `myapp.orders.created`
- Use standard units from the spec: `s` (seconds), `ms` (milliseconds), `By` (bytes), `{request}` (dimensionless)
- Prefix with your application/service name: `myapp.*`
- Use consistent tag names across metrics: `region`, `status`, `order.type`

---

## Structured Logging

### Microsoft.Extensions.Logging (Built-in)

The built-in logging framework supports structured logging natively. Use compile-time source generators for high-performance logging:

```csharp
public static partial class Log
{
    [LoggerMessage(
        Level = LogLevel.Information,
        Message = "Order {OrderId} created for customer {CustomerId} with {LineCount} items, total {Total:C}")]
    public static partial void OrderCreated(
        this ILogger logger,
        string orderId,
        string customerId,
        int lineCount,
        decimal total);

    [LoggerMessage(
        Level = LogLevel.Warning,
        Message = "Order {OrderId} processing exceeded threshold: {Duration}ms")]
    public static partial void OrderProcessingSlow(
        this ILogger logger,
        string orderId,
        double duration);

    [LoggerMessage(
        Level = LogLevel.Error,
        Message = "Failed to process order {OrderId}")]
    public static partial void OrderProcessingFailed(
        this ILogger logger,
        Exception exception,
        string orderId);
}

// Usage
logger.OrderCreated(order.Id, order.CustomerId, order.Lines.Count, order.Total);
```

### Why Source-Generated Logging

- **Zero allocation** for disabled log levels (checked at call site)
- **Compile-time validation** of message templates and parameters
- **Structured by default** -- parameters become named properties in the log event

### LoggerMessage.Define (Legacy / Pre-.NET 6)

Before source generators (.NET 5 and earlier), use `LoggerMessage.Define` to achieve the same zero-allocation benefits. This approach still works in modern .NET and is useful in non-partial classes or when targeting older frameworks:

```csharp
public static class LogMessages
{
    private static readonly Action<ILogger, string, int, Exception?> s_orderCreated =
        LoggerMessage.Define<string, int>(
            LogLevel.Information,
            new EventId(1, nameof(OrderCreated)),
            "Order {OrderId} created with {LineCount} items");

    public static void OrderCreated(
        ILogger logger, string orderId, int lineCount)
        => s_orderCreated(logger, orderId, lineCount, null);

    private static readonly Action<ILogger, string, Exception?> s_orderFailed =
        LoggerMessage.Define<string>(
            LogLevel.Error,
            new EventId(2, nameof(OrderFailed)),
            "Failed to process order {OrderId}");

    public static void OrderFailed(
        ILogger logger, string orderId, Exception exception)
        => s_orderFailed(logger, orderId, exception);
}
```

Prefer `[LoggerMessage]` source generators for new code targeting .NET 6+. Use `LoggerMessage.Define` only when source generators are unavailable.

### Message Templates: Do and Do Not

Message templates use named placeholders that become structured properties. This is fundamental to structured logging -- violations prevent log indexing and search.

```csharp
// CORRECT: structured message template with named placeholders
logger.LogInformation("Order {OrderId} shipped to {City}", orderId, city);

// WRONG: string interpolation -- bypasses structured logging entirely
logger.LogInformation($"Order {orderId} shipped to {city}");

// WRONG: string concatenation -- same problem
logger.LogInformation("Order " + orderId + " shipped to " + city);

// WRONG: ToString() in template -- loses type information
logger.LogInformation("Order {OrderId} shipped at {Time}",
    orderId, DateTime.UtcNow.ToString("o")); // pass DateTime directly

// CORRECT: pass objects directly, let the formatter handle rendering
logger.LogInformation("Order {OrderId} shipped at {ShippedAt}",
    orderId, DateTime.UtcNow);
```

### Log Level Best Practices

| Level | When to Use | Example |
|-------|-------------|---------|
| `Trace` | Detailed diagnostic info (method entry/exit, variable values) | `Entering ProcessOrder with {OrderId}` |
| `Debug` | Internal app state useful during development | `Cache hit for product {ProductId}` |
| `Information` | Normal application flow, business events | `Order {OrderId} created successfully` |
| `Warning` | Unexpected situations that do not prevent operation | `Retry {Attempt} for external API call` |
| `Error` | Failures that affect the current operation | `Failed to save order {OrderId}` |
| `Critical` | Application-wide failures requiring immediate action | `Database connection pool exhausted` |

### Log Filtering (Microsoft.Extensions.Logging)

Configure log level filtering in `appsettings.json` to suppress noisy framework logs while keeping application logs at the desired level:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.AspNetCore.HttpLogging": "Information",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning",
      "System.Net.Http.HttpClient": "Warning",
      "MyApp": "Debug"
    },
    "Console": {
      "LogLevel": {
        "Default": "Warning"
      }
    }
  }
}
```

Key filtering rules:
- **Most-specific category wins** -- `MyApp.Orders` matches `MyApp` if no more specific override exists
- **Provider-level overrides** -- the `Console` section above overrides the default for the console provider only
- **Environment overrides** -- use `appsettings.Development.json` to enable `Debug`/`Trace` locally without affecting production

### Log Scopes for Correlation

```csharp
public async Task<Order> ProcessOrderAsync(
    string orderId,
    CancellationToken ct)
{
    using var scope = _logger.BeginScope(
        new Dictionary<string, object>
        {
            ["OrderId"] = orderId,
            ["CorrelationId"] = Activity.Current?.TraceId.ToString() ?? ""
        });

    // All log messages within this scope include OrderId and CorrelationId
    _logger.LogInformation("Starting order processing");
    // ...
}
```

### Serilog Integration

For advanced sinks (Elasticsearch, Seq, Datadog), Serilog is the standard structured logging library.

| Package | Purpose |
|---------|---------|
| `Serilog.AspNetCore` | `UseSerilog()` host integration + `UseSerilogRequestLogging()` |
| `Serilog.Settings.Configuration` | `ReadFrom.Configuration()` for appsettings.json binding |
| `Serilog.Sinks.OpenTelemetry` | `WriteTo.OpenTelemetry()` OTLP sink |
| `Serilog.Formatting.Compact` | `RenderedCompactJsonFormatter` for structured console output |
| `Serilog.Enrichers.Environment` | `Enrich.WithMachineName()` and `Enrich.WithEnvironmentName()` |

```csharp
// Program.cs
builder.Host.UseSerilog((context, loggerConfiguration) =>
{
    loggerConfiguration
        .ReadFrom.Configuration(context.Configuration)
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithEnvironmentName()
        .WriteTo.Console(new RenderedCompactJsonFormatter())
        .WriteTo.OpenTelemetry(options =>
        {
            options.Endpoint = context.Configuration["OTEL_EXPORTER_OTLP_ENDPOINT"]
                ?? "http://localhost:4317";
            options.Protocol = OtlpProtocol.Grpc;
        });
});

// Use Serilog request logging instead of the built-in one
app.UseSerilogRequestLogging(options =>
{
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
        diagnosticContext.Set("UserAgent", httpContext.Request.Headers.UserAgent.ToString());
    };
});
```

Configure via `appsettings.json`:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore.Database.Command": "Warning",
        "System.Net.Http.HttpClient": "Warning"
      }
    }
  }
}
```

### Choosing Between MS.Extensions.Logging and Serilog

| Scenario | Recommendation |
|----------|---------------|
| Console + OTLP export only | `Microsoft.Extensions.Logging` + OpenTelemetry exporter |
| Need Elasticsearch, Seq, or Datadog sinks | Serilog |
| .NET Aspire application | Use the built-in logging (Aspire configures OTLP automatically) |
| High-throughput, minimal allocation | Source-generated `LoggerMessage` (works with both) |

---

## Health Checks

Health checks enable orchestrators (Kubernetes, Docker, load balancers) to determine whether your application is ready to serve traffic.

### Health Check Packages

The built-in `Microsoft.Extensions.Diagnostics.HealthChecks` package provides the core framework. Community packages from `Xabaril/AspNetCore.Diagnostics.HealthChecks` add provider-specific checks:

| Package | Extension Method |
|---------|-----------------|
| `AspNetCore.HealthChecks.Npgsql` | `.AddNpgSql()` |
| `AspNetCore.HealthChecks.Redis` | `.AddRedis()` |
| `AspNetCore.HealthChecks.Uris` | `.AddUrlGroup()` |
| `AspNetCore.HealthChecks.UI.Client` | `UIResponseWriter.WriteHealthCheckUIResponse` |

### Basic Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy(), tags: ["live"])
    .AddNpgSql(
        builder.Configuration.GetConnectionString("DefaultConnection")!,
        name: "database",
        tags: ["ready"])
    .AddRedis(
        builder.Configuration.GetConnectionString("Redis")!,
        name: "redis",
        tags: ["ready"])
    .AddUrlGroup(
        new Uri("https://api.external.com/health"),
        name: "external-api",
        tags: ["ready"]);

var app = builder.Build();

// Liveness: is the process running? (don't check dependencies)
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live")
});

// Readiness: can the process serve traffic? (check dependencies)
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready"),
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
```

### Custom Health Checks

```csharp
public sealed class DiskSpaceHealthCheck(
    IOptions<DiskSpaceOptions> options) : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken ct = default)
    {
        var drive = new DriveInfo(options.Value.DrivePath);
        var freeSpaceMb = drive.AvailableFreeSpace / (1024 * 1024);

        var data = new Dictionary<string, object>
        {
            ["FreeSpaceMB"] = freeSpaceMb,
            ["DrivePath"] = options.Value.DrivePath
        };

        if (freeSpaceMb < options.Value.MinimumFreeSpaceMb)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy(
                $"Low disk space: {freeSpaceMb}MB remaining", data: data));
        }

        return Task.FromResult(HealthCheckResult.Healthy(
            $"Disk space OK: {freeSpaceMb}MB free", data: data));
    }
}

// Registration
builder.Services.AddHealthChecks()
    .AddCheck<DiskSpaceHealthCheck>("disk-space", tags: ["ready"]);
```

### Liveness vs Readiness

| Check | Purpose | Failure Action | Example |
|-------|---------|---------------|---------|
| **Liveness** (`/health/live`) | Is the process healthy? | Restart container | Self-check, deadlock detection |
| **Readiness** (`/health/ready`) | Can the process serve traffic? | Remove from load balancer | Database, Redis, external APIs |

**Important:** Liveness checks should NOT include dependency checks. If a database is down, restarting your app will not fix the database. Liveness checks that fail on dependency issues cause cascading restarts.

### Health Check Publishing

`HealthCheckPublisherOptions` controls the periodic evaluation schedule. To push results to monitoring systems, register an `IHealthCheckPublisher` implementation:

```csharp
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy());

// Configure periodic evaluation schedule
builder.Services.Configure<HealthCheckPublisherOptions>(options =>
{
    options.Delay = TimeSpan.FromSeconds(5);   // Initial delay before first run
    options.Period = TimeSpan.FromSeconds(30);  // Interval between evaluations
});

// Register a publisher to push results (e.g., to logs, metrics, or external systems)
builder.Services.AddSingleton<IHealthCheckPublisher, LoggingHealthCheckPublisher>();
```

A minimal publisher that logs health status:

```csharp
public sealed class LoggingHealthCheckPublisher(
    ILogger<LoggingHealthCheckPublisher> logger) : IHealthCheckPublisher
{
    public Task PublishAsync(
        HealthReport report, CancellationToken ct)
    {
        logger.LogInformation(
            "Health check: {Status} ({TotalDuration}ms)",
            report.Status,
            report.TotalDuration.TotalMilliseconds);
        return Task.CompletedTask;
    }
}
```

---

## Putting It Together: Production Configuration

A complete observability setup for a production .NET API:

```csharp
var builder = WebApplication.CreateBuilder(args);

// 1. OpenTelemetry -- traces, metrics, logs
builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService(builder.Environment.ApplicationName))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddSource("MyApp.*")
        .AddOtlpExporter())
    .WithMetrics(metrics => metrics
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddRuntimeInstrumentation()
        .AddMeter("MyApp.*")
        .AddOtlpExporter());

// 2. Structured logging with OpenTelemetry export
builder.Logging.AddOpenTelemetry(logging =>
{
    logging.IncludeScopes = true;
    logging.IncludeFormattedMessage = true;
    logging.AddOtlpExporter();
});

// 3. Health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => HealthCheckResult.Healthy(), tags: ["live"])
    .AddNpgSql(
        builder.Configuration.GetConnectionString("DefaultConnection")!,
        name: "database",
        tags: ["ready"]);

// 4. Custom application metrics
builder.Services.AddSingleton<OrderMetrics>();

var app = builder.Build();

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live")
});
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.Run();
```

---
