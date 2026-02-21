---
name: dotnet-grpc
description: Builds gRPC services. Proto definition, code-gen, ASP.NET Core host, streaming, auth.
license: MIT
user-invocable: false
---

# dotnet-grpc

Full gRPC lifecycle for .NET applications. Covers `.proto` service definition, code generation, ASP.NET Core gRPC server implementation and endpoint hosting, `Grpc.Net.Client` client patterns, all four streaming patterns (unary, server streaming, client streaming, bidirectional streaming), authentication, load balancing, and health checks.

For detailed code examples (server implementation, client patterns, streaming, auth, interceptors, gRPC-Web), see `examples.md` in this skill directory.

## Scope

- Proto service definition and code generation
- ASP.NET Core gRPC server implementation
- Grpc.Net.Client client patterns
- All four streaming patterns (unary, server, client, bidirectional)
- Authentication, load balancing, and health checks

## Out of scope

- Source generator authoring patterns -- see [skill:dotnet-csharp-source-generators]
- HTTP client factory and resilience pipelines -- see [skill:dotnet-http-client] and [skill:dotnet-resilience]
- Native AOT architecture and trimming -- see [skill:dotnet-native-aot] and [skill:dotnet-trimming]

Cross-references: [skill:dotnet-resilience] for retry/circuit-breaker on gRPC channels, [skill:dotnet-serialization] for Protobuf wire format details. See [skill:dotnet-integration-testing] for testing gRPC services.

---

## Proto Definition and Code Generation

### Project Setup

gRPC uses Protocol Buffers as its interface definition language. The `Grpc.Tools` package generates C# code from `.proto` files at build time.

**Server project:**

```xml
<ItemGroup>
  <PackageReference Include="Grpc.AspNetCore" Version="2.*" />
</ItemGroup>

<ItemGroup>
  <Protobuf Include="Protos\*.proto" GrpcServices="Server" />
</ItemGroup>
```

**Client project:**

```xml
<ItemGroup>
  <PackageReference Include="Google.Protobuf" Version="3.*" />
  <PackageReference Include="Grpc.Net.Client" Version="2.*" />
  <PackageReference Include="Grpc.Tools" Version="2.*" PrivateAssets="All" />
</ItemGroup>

<ItemGroup>
  <Protobuf Include="Protos\*.proto" GrpcServices="Client" />
</ItemGroup>
```

**Shared contracts project (recommended for larger services):**

```xml
<ItemGroup>
  <PackageReference Include="Google.Protobuf" Version="3.*" />
  <PackageReference Include="Grpc.Tools" Version="2.*" PrivateAssets="All" />
</ItemGroup>

<ItemGroup>
  <Protobuf Include="Protos\*.proto" GrpcServices="Both" />
</ItemGroup>
```

### Proto File Definition

```protobuf
syntax = "proto3";

option csharp_namespace = "MyApp.Grpc";

package myapp;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Service definition with all 4 streaming patterns
service OrderService {
  rpc GetOrder (GetOrderRequest) returns (OrderResponse);
  rpc ListOrders (ListOrdersRequest) returns (stream OrderResponse);
  rpc UploadOrders (stream CreateOrderRequest) returns (UploadOrdersResponse);
  rpc ProcessOrders (stream CreateOrderRequest) returns (stream OrderResponse);
}

message GetOrderRequest {
  int32 id = 1;
}

message ListOrdersRequest {
  string customer_id = 1;
  int32 page_size = 2;
  string page_token = 3;
}

message CreateOrderRequest {
  string customer_id = 1;
  repeated OrderItemMessage items = 2;
}

message OrderResponse {
  int32 id = 1;
  string customer_id = 2;
  repeated OrderItemMessage items = 3;
  google.protobuf.Timestamp created_at = 4;
}

message OrderItemMessage {
  string product_id = 1;
  int32 quantity = 2;
  double unit_price = 3;
}

message UploadOrdersResponse {
  int32 orders_created = 1;
}
```

### Code-Gen Workflow

The `Grpc.Tools` package runs the Protobuf compiler (`protoc`) and C# gRPC plugin at build time. Generated files appear in `obj/` and are included automatically:

1. Add `.proto` files to the project via `<Protobuf>` items
2. Set `GrpcServices` to `Server`, `Client`, or `Both`
3. Build the project -- generated C# types and service stubs appear in `obj/Debug/net10.0/Protos/`
4. Implement the generated abstract base class (server) or use the generated client class

The gRPC code-gen toolchain uses source generation to produce the C# stubs from `.proto` definitions. This is conceptually similar to [skill:dotnet-csharp-source-generators] but uses `protoc` rather than Roslyn incremental generators.

---

## Streaming Patterns Summary

gRPC supports four communication patterns:

| Pattern | Request | Response | Use Case |
|---------|---------|----------|----------|
| **Unary** | Single message | Single message | Standard request-response (CRUD, queries) |
| **Server streaming** | Single message | Stream of messages | Real-time feeds, large result sets, push notifications |
| **Client streaming** | Stream of messages | Single message | Bulk uploads, aggregation, telemetry ingestion |
| **Bidirectional streaming** | Stream of messages | Stream of messages | Chat, real-time collaboration, event processing |

---

## Status Codes

Map domain errors to gRPC status codes:

| gRPC Status | HTTP Equivalent | Use When |
|-------------|----------------|----------|
| `OK` | 200 | Success |
| `NotFound` | 404 | Resource does not exist |
| `InvalidArgument` | 400 | Client sent bad data |
| `PermissionDenied` | 403 | Caller lacks permission |
| `Unauthenticated` | 401 | No valid credentials |
| `AlreadyExists` | 409 | Duplicate creation attempt |
| `ResourceExhausted` | 429 | Rate limited |
| `Internal` | 500 | Unhandled server error |
| `Unavailable` | 503 | Transient failure -- safe to retry |
| `DeadlineExceeded` | 504 | Operation timed out |

---

## gRPC-Web Limitations

- **Unary and server streaming only** -- client streaming and bidirectional streaming are not supported by gRPC-Web
- **No HTTP/2 trailers** -- status and trailing metadata are encoded in the response body
- **CORS required** -- cross-origin requests need explicit CORS configuration on the server
- **Consider SignalR for full-duplex browser communication** -- see [skill:dotnet-realtime-communication] for alternatives when bidirectional streaming is required

---

## Key Principles

- **Use `.proto` files as the contract** -- they are the single source of truth for the API shape, shared between client and server
- **Set `GrpcServices` on `<Protobuf>` items** -- `Server` for service projects, `Client` for consumer projects, `Both` for shared contracts
- **Reuse channels** -- `GrpcChannel` manages HTTP/2 connections; creating a new channel per call wastes resources
- **Register gRPC clients via DI** -- `AddGrpcClient` integrates with `IHttpClientFactory` for connection pooling and resilience
- **Always set deadlines** -- calls without deadlines can hang indefinitely if the server is slow or unreachable
- **Use L7 load balancers** -- L4 load balancers pin all traffic to one backend because HTTP/2 multiplexes on a single TCP connection
- **Implement the gRPC health check protocol** -- enables Kubernetes probes and load balancers to monitor service health
- **Use gRPC-Web for browser clients** -- native gRPC requires HTTP/2 trailers which browsers do not support; gRPC-Web bridges this gap

See [skill:dotnet-native-aot] for Native AOT compilation pipeline and [skill:dotnet-aot-architecture] for AOT-compatible patterns when building gRPC services with ahead-of-time compilation.

---

## Agent Gotchas

1. **Do not create a new `GrpcChannel` per request** -- channels are expensive to create and manage HTTP/2 connections. Reuse them or use DI-registered clients.
2. **Do not omit `GrpcServices` on `<Protobuf>` items** -- the default is `Both`, which generates server and client stubs. This bloats client projects with unused server code and vice versa.
3. **Do not use L4 load balancers for gRPC without enabling `EnableMultipleHttp2Connections`** -- HTTP/2 multiplexing means a single connection handles all RPCs, defeating load distribution.
4. **Do not throw generic `Exception` from gRPC services** -- throw `RpcException` with appropriate `StatusCode` and descriptive messages. Unhandled exceptions become `StatusCode.Internal` with no useful detail.
5. **Do not forget to call `CompleteAsync()` on client streams** -- the server waits for stream completion before sending its response. Forgetting this causes the call to hang.
6. **Do not use `grpc.health.v1.Health` without registering health checks** -- an empty health service always reports `Serving`, which defeats the purpose of health monitoring.
7. **Do not enable gRPC-Web globally without CORS** -- `UseGrpcWeb()` without a CORS policy allows any origin to call your gRPC services. Always pair with explicit `RequireCors()`.
8. **Do not attempt client streaming or bidirectional streaming with gRPC-Web** -- the gRPC-Web protocol only supports unary and server streaming. Use SignalR or native gRPC for full-duplex browser communication.

---

## Attribution

Adapted from [Aaronontheweb/dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) (MIT license).

---

## References

- [gRPC for .NET overview](https://learn.microsoft.com/en-us/aspnet/core/grpc/?view=aspnetcore-10.0)
- [Create a gRPC client and server](https://learn.microsoft.com/en-us/aspnet/core/tutorials/grpc/grpc-start?view=aspnetcore-10.0)
- [gRPC client factory integration](https://learn.microsoft.com/en-us/aspnet/core/grpc/clientfactory?view=aspnetcore-10.0)
- [gRPC services with ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/grpc/aspnetcore?view=aspnetcore-10.0)
- [gRPC health checks](https://learn.microsoft.com/en-us/aspnet/core/grpc/health-checks?view=aspnetcore-10.0)
- [gRPC load balancing](https://learn.microsoft.com/en-us/aspnet/core/grpc/loadbalancing?view=aspnetcore-10.0)
- [gRPC authentication](https://learn.microsoft.com/en-us/aspnet/core/grpc/authn-and-authz?view=aspnetcore-10.0)
- [gRPC interceptors](https://learn.microsoft.com/en-us/aspnet/core/grpc/interceptors?view=aspnetcore-10.0)
- [gRPC-Web for .NET](https://learn.microsoft.com/en-us/aspnet/core/grpc/grpcweb?view=aspnetcore-10.0)
- [Protocol Buffers language guide](https://protobuf.dev/programming-guides/proto3/)
