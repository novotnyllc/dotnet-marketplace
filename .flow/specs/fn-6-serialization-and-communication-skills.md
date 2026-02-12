# fn-6: Serialization & Communication Skills

## Overview
Delivers AOT-friendly serialization and service communication skills including System.Text.Json source generators, gRPC, real-time communication patterns, and service communication routing.

## Scope
**Skills:**
- `dotnet-serialization` - AOT-friendly source-gen serialization: System.Text.Json source gen, Protobuf, MessagePack. Performance tradeoffs.
- `dotnet-grpc` - Full gRPC skill: service definition, code-gen, streaming, auth, load balancing, health checks
- `dotnet-realtime-communication` - Service communication patterns: SignalR, JSON-RPC 2.0, Server-Sent Events, gRPC streaming. When to use what.
- `dotnet-service-communication` - Higher-level skill that routes to gRPC, real-time, or REST based on requirements

## Key Context
- System.Text.Json source generators are AOT-friendly and required for Native AOT
- Reflection-based serialization is incompatible with trimming/AOT
- .NET 10 brings built-in Server-Sent Events support to ASP.NET Core
- gRPC is the recommended approach for service-to-service communication
- Skills must reference performance tradeoffs (STJ vs Protobuf vs MessagePack)

## Quick Commands
```bash
# Smoke test: verify serialization skill covers source generators
grep -i "source generator" skills/serialization/dotnet-serialization.md

# Validate gRPC streaming patterns
grep -i "streaming" skills/serialization/dotnet-grpc.md

# Test service communication routing logic
grep -r "when to use" skills/serialization/dotnet-service-communication.md
```

## Acceptance Criteria
1. All 4 skills written with standard depth and frontmatter
2. Serialization skill emphasizes STJ source generators for AOT compatibility
3. gRPC skill covers full lifecycle: .proto definition, code-gen, client/server patterns, streaming (unary, server, client, bidirectional)
4. Real-time communication skill compares SignalR, SSE, JSON-RPC, gRPC streaming with decision guidance
5. Service communication skill acts as router, loading other skills based on requirements
6. Skills cross-reference dotnet-native-aot for AOT-specific considerations
7. Performance tradeoffs documented with benchmark references

## Test Notes
- Verify serialization skill detects non-AOT-friendly patterns (reflection-based serialization)
- Test that service-communication skill routes to appropriate specialized skills
- Validate gRPC skill covers both ASP.NET Core gRPC and Grpc.Net.Client

## References
- System.Text.Json Source Generators: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation
- gRPC for .NET: https://learn.microsoft.com/en-us/aspnet/core/grpc/?view=aspnetcore-10.0
- Native AOT Deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- dotnet-skills serialization reference: https://github.com/Aaronontheweb/dotnet-skills
