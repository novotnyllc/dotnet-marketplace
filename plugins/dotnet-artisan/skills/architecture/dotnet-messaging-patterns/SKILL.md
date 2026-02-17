---
name: dotnet-messaging-patterns
description: "Building event-driven systems. Pub/sub, competing consumers, DLQ, sagas, delivery guarantees."
---

# dotnet-messaging-patterns

Durable messaging patterns for .NET event-driven architectures. Covers publish/subscribe, competing consumers, dead-letter queues, saga/process manager orchestration, and delivery guarantee strategies using Azure Service Bus, RabbitMQ, and MassTransit.

**Out of scope:** Background service lifecycle and `IHostedService` registration -- see [skill:dotnet-background-services]. Resilience pipelines and retry policies -- see [skill:dotnet-resilience]. JSON/binary serialization configuration -- see [skill:dotnet-serialization]. In-process producer/consumer queues with `Channel<T>` -- see [skill:dotnet-channels].

Cross-references: [skill:dotnet-background-services] for hosting message consumers, [skill:dotnet-resilience] for fault tolerance around message handlers, [skill:dotnet-serialization] for message envelope serialization, [skill:dotnet-channels] for in-process queuing patterns.

---

## Messaging Fundamentals

### Message Types

| Type | Purpose | Example |
|------|---------|---------|
| **Command** | Request an action (one recipient) | `PlaceOrder`, `ShipPackage` |
| **Event** | Notify something happened (many recipients) | `OrderPlaced`, `PaymentReceived` |
| **Document** | Transfer data between systems | `CustomerProfile`, `ProductCatalog` |

Commands are sent to a specific queue; events are published to a topic/exchange and delivered to all subscribers. This distinction drives the choice between point-to-point and pub/sub topologies.

### Delivery Guarantees

| Guarantee | Behavior | Implementation |
|-----------|----------|----------------|
| **At-most-once** | Fire and forget; message may be lost | No ack, no retry |
| **At-least-once** | Message retried until acknowledged; duplicates possible | Ack after processing + retry on failure |
| **Exactly-once** | Each message processed exactly once | At-least-once + idempotent consumer |

**At-least-once with idempotent consumers** is the standard approach for durable messaging. True exactly-once requires distributed transactions (which most brokers do not support) or consumer-side deduplication.

---

## Publish/Subscribe

### Azure Service Bus Topics

```csharp
// Publisher -- send event to a topic
await using var client = new ServiceBusClient(connectionString);
await using var sender = client.CreateSender("order-events");

var message = new ServiceBusMessage(
    JsonSerializer.SerializeToUtf8Bytes(new OrderPlaced(orderId, total)))
{
    Subject = nameof(OrderPlaced),
    ContentType = "application/json",
    MessageId = Guid.NewGuid().ToString()
};

await sender.SendMessageAsync(message, cancellationToken);
```

```csharp
// Subscriber -- process events from a subscription
await using var processor = client.CreateProcessor(
    topicName: "order-events",
    subscriptionName: "billing-service",
    new ServiceBusProcessorOptions
    {
        MaxConcurrentCalls = 10,
        AutoCompleteMessages = false
    });

processor.ProcessMessageAsync += async args =>
{
    var body = args.Message.Body.ToObjectFromJson<OrderPlaced>();
    await HandleOrderPlacedAsync(body);
    await args.CompleteMessageAsync(args.Message);
};

processor.ProcessErrorAsync += args =>
{
    logger.LogError(args.Exception, "Error processing message");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync(cancellationToken);
```

**Key packages:**

```xml
<PackageReference Include="Azure.Messaging.ServiceBus" Version="7.*" />
```

### RabbitMQ Fanout Exchange

```csharp
// Publisher -- declare exchange and publish
var factory = new ConnectionFactory { HostName = "localhost" };
await using var connection = await factory.CreateConnectionAsync();
await using var channel = await connection.CreateChannelAsync();

await channel.ExchangeDeclareAsync(
    exchange: "order-events",
    type: ExchangeType.Fanout,
    durable: true);

var body = JsonSerializer.SerializeToUtf8Bytes(
    new OrderPlaced(orderId, total));

await channel.BasicPublishAsync(
    exchange: "order-events",
    routingKey: string.Empty,
    body: body);
```

**Key packages:**

```xml
<PackageReference Include="RabbitMQ.Client" Version="7.*" />
```

### MassTransit Publish

MassTransit abstracts the broker, providing a unified API for Azure Service Bus, RabbitMQ, Amazon SQS, and in-memory transport.

```csharp
// Registration
builder.Services.AddMassTransit(x =>
{
    x.AddConsumer<OrderPlacedConsumer>();

    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });
        cfg.ConfigureEndpoints(context);
    });
});

// Publisher
public sealed class OrderService(IPublishEndpoint publishEndpoint)
{
    public async Task PlaceOrderAsync(
        Guid orderId, decimal total, CancellationToken ct)
    {
        // Process order...
        await publishEndpoint.Publish(
            new OrderPlaced(orderId, total), ct);
    }
}

// Consumer
public sealed class OrderPlacedConsumer(
    ILogger<OrderPlacedConsumer> logger)
    : IConsumer<OrderPlaced>
{
    public async Task Consume(ConsumeContext<OrderPlaced> context)
    {
        logger.LogInformation(
            "Processing order {OrderId}", context.Message.OrderId);
        await ProcessAsync(context.Message);
    }
}

// Message contract (use records in a shared contracts assembly)
public record OrderPlaced(Guid OrderId, decimal Total);
```

**Key packages:**

```xml
<PackageReference Include="MassTransit" Version="8.*" />
<!-- Pick ONE transport: -->
<PackageReference Include="MassTransit.RabbitMQ" Version="8.*" />
<!-- OR -->
<PackageReference Include="MassTransit.Azure.ServiceBus.Core" Version="8.*" />
```

---

## Competing Consumers

Multiple consumer instances process messages from the same queue in parallel. The broker delivers each message to exactly one consumer, distributing load across instances.

### Pattern

```
Queue: order-processing
  ├── Consumer Instance A  (picks message 1)
  ├── Consumer Instance B  (picks message 2)
  └── Consumer Instance C  (picks message 3)
```

### Azure Service Bus -- Scaling Consumers

```csharp
// Multiple instances reading from the same queue automatically compete.
// MaxConcurrentCalls controls per-instance parallelism.
var processor = client.CreateProcessor("order-processing",
    new ServiceBusProcessorOptions
    {
        MaxConcurrentCalls = 20,
        PrefetchCount = 50,
        AutoCompleteMessages = false
    });
```

### MassTransit -- Concurrency Limits

```csharp
x.AddConsumer<OrderProcessor>(cfg =>
{
    cfg.UseConcurrentMessageLimit(10);
});
```

### Ordering Considerations

Competing consumers sacrifice strict ordering for throughput. When order matters:
- **Azure Service Bus**: Use sessions (`RequiresSession = true`) to guarantee FIFO within a session ID (e.g., per customer)
- **RabbitMQ**: Use a single consumer per queue, or consistent-hash exchange to partition by key
- **MassTransit**: Configure `UseMessagePartitioner` for key-based ordering

---

## Dead-Letter Queues

Dead-letter queues (DLQs) capture messages that cannot be processed after exhausting retries. They prevent poison messages from blocking the main queue.

### Why Messages Are Dead-Lettered

| Reason | Trigger |
|--------|---------|
| Max delivery attempts exceeded | Message failed processing N times |
| TTL expired | Message sat in queue past its time-to-live |
| Consumer rejection | Consumer explicitly dead-letters the message |
| Queue length exceeded | Queue overflow policy routes to DLQ |

### Azure Service Bus DLQ

```csharp
// Dead-letter a message with reason
await args.DeadLetterMessageAsync(
    args.Message,
    deadLetterReason: "ValidationFailed",
    deadLetterErrorDescription: "Missing required field: CustomerId");

// Read from the dead-letter sub-queue
await using var dlqReceiver = client.CreateReceiver(
    "order-processing",
    new ServiceBusReceiverOptions
    {
        SubQueue = SubQueue.DeadLetter
    });

while (true)
{
    var message = await dlqReceiver.ReceiveMessageAsync(
        TimeSpan.FromSeconds(5), cancellationToken);
    if (message is null) break;

    logger.LogWarning(
        "DLQ message: {Reason} - {Description}",
        message.DeadLetterReason,
        message.DeadLetterErrorDescription);

    // Inspect, fix, and re-submit or discard
    await dlqReceiver.CompleteMessageAsync(message);
}
```

### MassTransit Error/Fault Queues

MassTransit automatically creates `_error` and `_skipped` queues. Failed messages after retry exhaustion move to the error queue with fault metadata.

```csharp
// Configure retry before dead-lettering
x.AddConsumer<OrderProcessor>(cfg =>
{
    cfg.UseMessageRetry(r => r.Intervals(
        TimeSpan.FromSeconds(1),
        TimeSpan.FromSeconds(5),
        TimeSpan.FromSeconds(15)));
});
```

### DLQ Monitoring

Always monitor DLQ depth with alerts. Unmonitored DLQs accumulate silently until data is lost or stale.

---

## Saga / Process Manager

Sagas coordinate multi-step business processes across services. Each step publishes events that trigger the next step, with compensation logic for failures.

### Choreography vs Orchestration

| Style | How it works | Use when |
|-------|-------------|----------|
| **Choreography** | Services react to events independently; no central coordinator | Simple flows, few steps, loosely coupled |
| **Orchestration** | A saga/process manager directs each step | Complex flows, compensation needed, visibility required |

### MassTransit State Machine Saga

```csharp
// Saga state
public class OrderState : SagaStateMachineInstance
{
    public Guid CorrelationId { get; set; }
    public string CurrentState { get; set; } = default!;
    public Guid OrderId { get; set; }
    public decimal Total { get; set; }
    public DateTime? PaymentReceivedAt { get; set; }
}

// State machine definition
public sealed class OrderStateMachine : MassTransitStateMachine<OrderState>
{
    public State Submitted { get; private set; } = default!;
    public State PaymentPending { get; private set; } = default!;
    public State Completed { get; private set; } = default!;
    public State Faulted { get; private set; } = default!;

    public Event<OrderSubmitted> OrderSubmitted { get; private set; } = default!;
    public Event<PaymentReceived> PaymentReceived { get; private set; } = default!;
    public Event<PaymentFailed> PaymentFailed { get; private set; } = default!;

    public OrderStateMachine()
    {
        InstanceState(x => x.CurrentState);

        Event(() => OrderSubmitted,
            x => x.CorrelateById(ctx => ctx.Message.OrderId));
        Event(() => PaymentReceived,
            x => x.CorrelateById(ctx => ctx.Message.OrderId));
        Event(() => PaymentFailed,
            x => x.CorrelateById(ctx => ctx.Message.OrderId));

        Initially(
            When(OrderSubmitted)
                .Then(ctx =>
                {
                    ctx.Saga.OrderId = ctx.Message.OrderId;
                    ctx.Saga.Total = ctx.Message.Total;
                })
                .Publish(ctx => new RequestPayment(
                    ctx.Saga.OrderId, ctx.Saga.Total))
                .TransitionTo(PaymentPending));

        During(PaymentPending,
            When(PaymentReceived)
                .Then(ctx =>
                    ctx.Saga.PaymentReceivedAt = DateTime.UtcNow)
                .Publish(ctx => new FulfillOrder(ctx.Saga.OrderId))
                .TransitionTo(Completed),
            When(PaymentFailed)
                .Publish(ctx => new CancelOrder(ctx.Saga.OrderId))
                .TransitionTo(Faulted));
    }
}

// Registration -- requires MassTransit.EntityFrameworkCore package for EF persistence
// NuGet: MassTransit.EntityFrameworkCore Version="8.*"
builder.Services.AddMassTransit(x =>
{
    x.AddSagaStateMachine<OrderStateMachine, OrderState>()
        .EntityFrameworkRepository(r =>
        {
            r.ExistingDbContext<SagaDbContext>();
            r.UsePostgres();
        });

    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.ConfigureEndpoints(context);
    });
});
```

### Saga Persistence

| Store | Package | Use when |
|-------|---------|----------|
| Entity Framework Core | `MassTransit.EntityFrameworkCore` | Already using EF Core; need transactions |
| MongoDB | `MassTransit.MongoDb` | Document-oriented state; high throughput |
| Redis | `MassTransit.Redis` | Ephemeral sagas; low latency |
| In-Memory | Built-in | Testing only -- state lost on restart |

### Compensation Pattern

When a saga step fails, publish compensating commands to undo prior steps:

```
OrderSubmitted -> RequestPayment -> PaymentReceived -> ReserveInventory
                                                          |
                                                     InventoryFailed
                                                          |
                                                    RefundPayment (compensation)
                                                          |
                                                    CancelOrder (compensation)
```

---

## Idempotent Consumers

At-least-once delivery means consumers may receive the same message multiple times. Idempotent consumers ensure repeated processing produces the same result.

### Database-Based Deduplication

```csharp
public sealed class IdempotentOrderConsumer(
    AppDbContext db,
    ILogger<IdempotentOrderConsumer> logger)
    : IConsumer<OrderPlaced>
{
    public async Task Consume(ConsumeContext<OrderPlaced> context)
    {
        var messageId = context.MessageId
            ?? throw new InvalidOperationException("Missing MessageId");

        // Check if already processed
        var exists = await db.ProcessedMessages
            .AnyAsync(m => m.MessageId == messageId);

        if (exists)
        {
            logger.LogInformation(
                "Duplicate message {MessageId}, skipping", messageId);
            return;
        }

        // Process the message
        await ProcessOrderAsync(context.Message);

        // Record as processed
        db.ProcessedMessages.Add(new ProcessedMessage
        {
            MessageId = messageId,
            ProcessedAt = DateTime.UtcNow,
            ConsumerType = nameof(IdempotentOrderConsumer)
        });

        await db.SaveChangesAsync();
    }
}
```

### Natural Idempotency

Prefer operations that are naturally idempotent:
- **Upserts** (`INSERT ... ON CONFLICT UPDATE`) instead of blind inserts
- **Conditional updates** (`UPDATE ... WHERE Status = 'Pending'`) instead of unconditional
- **Deterministic IDs** derived from message content instead of auto-generated

---

## Message Envelope Pattern

Wrap message payloads in a standard envelope with metadata for tracing, versioning, and routing.

```csharp
public sealed record MessageEnvelope<T>(
    string MessageId,
    string MessageType,
    DateTimeOffset Timestamp,
    string CorrelationId,
    string Source,
    int Version, // Schema version for backward-compatible deserialization
    T Payload);
```

MassTransit provides this automatically via `ConsumeContext` (MessageId, CorrelationId, Headers). When using raw broker clients, implement envelopes explicitly.

---

## Agent Gotchas

1. **Do not use auto-complete with Azure Service Bus** -- set `AutoCompleteMessages = false` and call `CompleteMessageAsync` after successful processing. Auto-complete acknowledges before processing finishes, risking data loss on failure.
2. **Do not forget to handle poison messages** -- always configure max delivery count and DLQ monitoring. Without these, a single bad message blocks the entire queue indefinitely.
3. **Do not use in-memory saga persistence in production** -- saga state is lost on restart, leaving business processes in unknown states. Use Entity Framework, MongoDB, or Redis persistence.
4. **Do not assume message ordering across partitions** -- competing consumers and topic subscriptions deliver messages out of order by default. Use sessions or partitioning when order matters.
5. **Do not skip idempotency for at-least-once consumers** -- brokers may redeliver on timeout, network glitch, or consumer restart. Every consumer must handle duplicate messages safely.
6. **Do not hardcode connection strings** -- use environment variables or Azure Key Vault references. For local development, use user secrets or `.env` files excluded from source control.

---

## References

- [Azure Service Bus documentation](https://learn.microsoft.com/en-us/azure/service-bus-messaging/)
- [Azure Service Bus client library for .NET](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/messaging.servicebus-readme)
- [RabbitMQ .NET client documentation](https://www.rabbitmq.com/client-libraries/dotnet-api-guide)
- [MassTransit documentation](https://masstransit.io/documentation/concepts)
- [MassTransit sagas](https://masstransit.io/documentation/patterns/saga)
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
