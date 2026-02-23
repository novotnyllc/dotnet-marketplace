# dotnet-grpc -- Detailed Examples

Extended code examples for gRPC server implementation, client patterns, streaming, authentication, load balancing, health checks, interceptors, error handling, deadlines, and gRPC-Web.

---

## ASP.NET Core gRPC Server

### Service Implementation

Implement the generated abstract base class:

```csharp
using Grpc.Core;
using MyApp.Grpc;

public sealed class OrderGrpcService(
    OrderRepository repository,
    ILogger<OrderGrpcService> logger) : OrderService.OrderServiceBase
{
    // Unary
    public override async Task<OrderResponse> GetOrder(
        GetOrderRequest request,
        ServerCallContext context)
    {
        var order = await repository.GetByIdAsync(request.Id, context.CancellationToken);
        if (order is null)
        {
            throw new RpcException(new Status(StatusCode.NotFound,
                $"Order {request.Id} not found"));
        }

        return MapToResponse(order);
    }

    // Server streaming
    public override async Task ListOrders(
        ListOrdersRequest request,
        IServerStreamWriter<OrderResponse> responseStream,
        ServerCallContext context)
    {
        await foreach (var order in repository.ListByCustomerAsync(
            request.CustomerId, context.CancellationToken))
        {
            await responseStream.WriteAsync(MapToResponse(order),
                context.CancellationToken);
        }
    }

    // Client streaming
    public override async Task<UploadOrdersResponse> UploadOrders(
        IAsyncStreamReader<CreateOrderRequest> requestStream,
        ServerCallContext context)
    {
        var count = 0;
        await foreach (var request in requestStream.ReadAllAsync(
            context.CancellationToken))
        {
            await repository.CreateAsync(MapFromRequest(request),
                context.CancellationToken);
            count++;
        }

        return new UploadOrdersResponse { OrdersCreated = count };
    }

    // Bidirectional streaming
    public override async Task ProcessOrders(
        IAsyncStreamReader<CreateOrderRequest> requestStream,
        IServerStreamWriter<OrderResponse> responseStream,
        ServerCallContext context)
    {
        await foreach (var request in requestStream.ReadAllAsync(
            context.CancellationToken))
        {
            var order = await repository.CreateAsync(MapFromRequest(request),
                context.CancellationToken);
            await responseStream.WriteAsync(MapToResponse(order),
                context.CancellationToken);
        }
    }

    private static OrderResponse MapToResponse(Order order) =>
        new()
        {
            Id = order.Id,
            CustomerId = order.CustomerId,
            CreatedAt = Google.Protobuf.WellKnownTypes.Timestamp.FromDateTimeOffset(
                order.CreatedAt)
        };

    private static Order MapFromRequest(CreateOrderRequest request) =>
        new()
        {
            CustomerId = request.CustomerId,
            Items = request.Items.Select(i => new OrderItem
            {
                ProductId = i.ProductId,
                Quantity = i.Quantity,
                UnitPrice = (decimal)i.UnitPrice
            }).ToList()
        };
}
```

### Endpoint Hosting

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddGrpc(options =>
{
    options.MaxReceiveMessageSize = 4 * 1024 * 1024; // 4 MB
    options.MaxSendMessageSize = 4 * 1024 * 1024;
    options.EnableDetailedErrors = builder.Environment.IsDevelopment();
});

var app = builder.Build();
app.MapGrpcService<OrderGrpcService>();
app.Run();
```

### gRPC Reflection (Development)

```csharp
builder.Services.AddGrpc();
builder.Services.AddGrpcReflection();

var app = builder.Build();
app.MapGrpcService<OrderGrpcService>();

if (app.Environment.IsDevelopment())
{
    app.MapGrpcReflectionService();
}
```

---

## Client Patterns

### Basic Client

```csharp
using Grpc.Net.Client;
using MyApp.Grpc;

using var channel = GrpcChannel.ForAddress("https://localhost:5001");
var client = new OrderService.OrderServiceClient(channel);

var response = await client.GetOrderAsync(
    new GetOrderRequest { Id = 42 });
```

### DI-Registered Client with IHttpClientFactory

```csharp
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(options =>
    {
        options.Address = new Uri("https://order-service:5001");
    })
    .ConfigureChannel(options =>
    {
        options.MaxReceiveMessageSize = 4 * 1024 * 1024;
    });
```

Apply resilience via [skill:dotnet-resilience]:

```csharp
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(options =>
    {
        options.Address = new Uri("https://order-service:5001");
    })
    .AddStandardResilienceHandler();
```

### Reading Server Streams

```csharp
using var call = client.ListOrders(
    new ListOrdersRequest { CustomerId = "cust-123" });

await foreach (var order in call.ResponseStream.ReadAllAsync())
{
    Console.WriteLine($"Order {order.Id}: {order.CustomerId}");
}
```

### Client Streaming

```csharp
using var call = client.UploadOrders();

foreach (var order in ordersToCreate)
{
    await call.RequestStream.WriteAsync(new CreateOrderRequest
    {
        CustomerId = order.CustomerId
    });
}

await call.RequestStream.CompleteAsync();
var response = await call;
Console.WriteLine($"Created {response.OrdersCreated} orders");
```

### Bidirectional Streaming

```csharp
using var call = client.ProcessOrders();

var readTask = Task.Run(async () =>
{
    await foreach (var response in call.ResponseStream.ReadAllAsync())
    {
        Console.WriteLine($"Processed order {response.Id}");
    }
});

foreach (var order in ordersToProcess)
{
    await call.RequestStream.WriteAsync(new CreateOrderRequest
    {
        CustomerId = order.CustomerId
    });
}

await call.RequestStream.CompleteAsync();
await readTask;
```

---

## Authentication

### Bearer Token (JWT)

Server-side:

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = "https://identity.example.com";
        options.TokenValidationParameters.ValidAudience = "order-api";
    });

builder.Services.AddAuthorization();
builder.Services.AddGrpc();

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
app.MapGrpcService<OrderGrpcService>().RequireAuthorization();
```

Client-side token propagation:

```csharp
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(options =>
    {
        options.Address = new Uri("https://order-service:5001");
    })
    .AddCallCredentials(async (context, metadata, serviceProvider) =>
    {
        var tokenProvider = serviceProvider.GetRequiredService<ITokenProvider>();
        var token = await tokenProvider.GetTokenAsync(context.CancellationToken);
        metadata.Add("Authorization", $"Bearer {token}");
    });
```

### Certificate Authentication (mTLS)

```csharp
// Server: require client certificates
builder.WebHost.ConfigureKestrel(kestrel =>
{
    kestrel.ConfigureHttpsDefaults(https =>
    {
        https.ClientCertificateMode = ClientCertificateMode.RequireCertificate;
    });
});

builder.Services.AddAuthentication(CertificateAuthenticationDefaults.AuthenticationScheme)
    .AddCertificate(options =>
    {
        options.AllowedCertificateTypes = CertificateTypes.Chained;
        options.RevocationMode = X509RevocationMode.NoCheck;
    });
```

```csharp
// Client: provide client certificate
var handler = new HttpClientHandler();
handler.ClientCertificates.Add(
    new X509Certificate2("client.pfx", "password"));

using var channel = GrpcChannel.ForAddress("https://order-service:5001",
    new GrpcChannelOptions
    {
        HttpHandler = handler
    });
```

---

## Load Balancing

### Client-Side Load Balancing

```csharp
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(options =>
    {
        options.Address = new Uri("dns:///order-service:5001");
    })
    .ConfigureChannel(options =>
    {
        options.Credentials = ChannelCredentials.Insecure;
        options.ServiceConfig = new ServiceConfig
        {
            LoadBalancingConfigs = { new RoundRobinConfig() }
        };
    });
```

### Proxy-Based Load Balancing

```csharp
builder.Services
    .AddGrpcClient<OrderService.OrderServiceClient>(options =>
    {
        options.Address = new Uri("https://order-service-lb:5001");
    })
    .ConfigurePrimaryHttpMessageHandler(() => new SocketsHttpHandler
    {
        EnableMultipleHttp2Connections = true
    });
```

---

## Health Checks

### gRPC Health Check Protocol

```csharp
builder.Services.AddGrpc();
builder.Services.AddGrpcHealthChecks()
    .AddCheck("database", () =>
    {
        return HealthCheckResult.Healthy();
    });

var app = builder.Build();
app.MapGrpcService<OrderGrpcService>();
app.MapGrpcHealthChecksService();
```

### Integration with ASP.NET Core Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddNpgSql(
        builder.Configuration.GetConnectionString("OrderDb")!,
        name: "order-db",
        tags: ["ready"]);

builder.Services.AddGrpc();
builder.Services.AddGrpcHealthChecks()
    .AddAsyncCheck("order-db", async (sp, ct) =>
    {
        var healthCheckService = sp.GetRequiredService<HealthCheckService>();
        var report = await healthCheckService.CheckHealthAsync(
            r => r.Tags.Contains("ready"), ct);
        return report.Status == HealthStatus.Healthy
            ? HealthCheckResult.Healthy()
            : HealthCheckResult.Unhealthy();
    });
```

### Kubernetes Probes for gRPC

```yaml
livenessProbe:
  grpc:
    port: 5001
  initialDelaySeconds: 10
  periodSeconds: 15

readinessProbe:
  grpc:
    port: 5001
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

## Interceptors

### Server Interceptor

```csharp
public sealed class LoggingInterceptor(ILogger<LoggingInterceptor> logger)
    : Interceptor
{
    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(
        TRequest request,
        ServerCallContext context,
        UnaryServerMethod<TRequest, TResponse> continuation)
    {
        var stopwatch = Stopwatch.StartNew();
        try
        {
            var response = await continuation(request, context);
            logger.LogInformation(
                "gRPC {Method} completed in {ElapsedMs}ms",
                context.Method, stopwatch.ElapsedMilliseconds);
            return response;
        }
        catch (RpcException ex)
        {
            logger.LogError(ex,
                "gRPC {Method} failed with {StatusCode}",
                context.Method, ex.StatusCode);
            throw;
        }
    }
}

// Register
builder.Services.AddGrpc(options =>
{
    options.Interceptors.Add<LoggingInterceptor>();
});
```

### Client Interceptor

```csharp
public sealed class AuthInterceptor(ITokenProvider tokenProvider) : Interceptor
{
    public override AsyncUnaryCall<TResponse> AsyncUnaryCall<TRequest, TResponse>(
        TRequest request,
        ClientInterceptorContext<TRequest, TResponse> context,
        AsyncUnaryCallContinuation<TRequest, TResponse> continuation)
    {
        var token = tokenProvider.GetCachedToken();
        var headers = context.Options.Headers ?? new Metadata();
        headers.Add("Authorization", $"Bearer {token}");

        var newContext = new ClientInterceptorContext<TRequest, TResponse>(
            context.Method, context.Host,
            context.Options.WithHeaders(headers));

        return continuation(request, newContext);
    }
}
```

---

## Error Handling

### Rich Error Details

```csharp
// Server: throw with metadata
var status = new Status(StatusCode.InvalidArgument, "Validation failed");
var metadata = new Metadata
{
    { "field", "customer_id" },
    { "reason", "Customer ID is required" }
};
throw new RpcException(status, metadata);

// Client: read error metadata
try
{
    var response = await client.GetOrderAsync(request);
}
catch (RpcException ex) when (ex.StatusCode == StatusCode.InvalidArgument)
{
    var field = ex.Trailers.GetValue("field");
    var reason = ex.Trailers.GetValue("reason");
    logger.LogWarning("Validation error on {Field}: {Reason}", field, reason);
}
```

---

## Deadlines and Cancellation

```csharp
// Client: set a deadline
var deadline = DateTime.UtcNow.AddSeconds(10);
var response = await client.GetOrderAsync(
    new GetOrderRequest { Id = 42 },
    deadline: deadline);

// Server: check deadline and propagate cancellation
public override async Task<OrderResponse> GetOrder(
    GetOrderRequest request,
    ServerCallContext context)
{
    var order = await repository.GetByIdAsync(request.Id, context.CancellationToken);
    // ...
}
```

---

## gRPC-Web for Browser Clients

### Server Configuration

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddGrpc();
builder.Services.AddCors(options =>
{
    options.AddPolicy("GrpcWeb", policy =>
    {
        policy.WithOrigins("https://app.example.com")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .WithExposedHeaders("Grpc-Status", "Grpc-Message", "Grpc-Encoding");
    });
});

var app = builder.Build();

app.UseRouting();
app.UseCors();
app.UseGrpcWeb();

app.MapGrpcService<OrderGrpcService>()
    .EnableGrpcWeb()
    .RequireCors("GrpcWeb");
```

### JavaScript Client (grpc-web)

```javascript
import { OrderServiceClient } from './generated/order_grpc_web_pb';
import { GetOrderRequest } from './generated/order_pb';

const client = new OrderServiceClient('https://api.example.com');

const request = new GetOrderRequest();
request.setId(42);

client.getOrder(request, {}, (err, response) => {
    if (err) {
        console.error('gRPC error:', err.message);
        return;
    }
    console.log('Order:', response.toObject());
});
```

### Envoy Proxy Alternative

```yaml
http_filters:
  - name: envoy.filters.http.grpc_web
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_web.v3.GrpcWeb
  - name: envoy.filters.http.cors
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.cors.v3.Cors
  - name: envoy.filters.http.router
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```
