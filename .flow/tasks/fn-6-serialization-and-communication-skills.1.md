# fn-6-serialization-and-communication-skills.1 Serialization and gRPC skills

## Description
Create two skills: `dotnet-serialization` (AOT-friendly serialization covering System.Text.Json source generators, Protobuf, MessagePack with performance tradeoffs) and `dotnet-grpc` (full gRPC lifecycle: .proto definition, code-gen, ASP.NET Core server implementation, client patterns, streaming, authentication, load balancing, health checks).

## Acceptance
- [ ] `skills/serialization/dotnet-serialization/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/serialization/dotnet-grpc/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-serialization` covers STJ source generators, Protobuf, MessagePack with AOT compatibility notes
- [ ] `dotnet-serialization` includes performance tradeoff guidance (STJ vs Protobuf vs MessagePack)
- [ ] `dotnet-serialization` warns against reflection-based serialization (Newtonsoft.Json) for AOT
- [ ] `dotnet-grpc` covers .proto definition and code-gen workflow
- [ ] `dotnet-grpc` covers ASP.NET Core gRPC server patterns (service implementation + endpoint hosting)
- [ ] `dotnet-grpc` covers Grpc.Net.Client usage for client patterns
- [ ] `dotnet-grpc` covers all 4 streaming patterns — each named explicitly: unary, server streaming, client streaming, bidirectional streaming
- [ ] `dotnet-grpc` covers authentication, load balancing, and health checks
- [ ] `dotnet-grpc` cross-references `[skill:dotnet-resilience]` for retry/circuit-breaker on gRPC channels
- [ ] `dotnet-serialization` cross-references `[skill:dotnet-csharp-source-generators]` (fn-3) — mandatory
- [ ] `dotnet-grpc` cross-references `[skill:dotnet-csharp-source-generators]` only if discussing generator-adjacent scenarios (optional/conditional)
- [ ] Both skills include `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker (standardized deferred placeholder format)
- [ ] Both skills contain explicit out-of-scope boundary statements for: fn-3 (source generators depth), fn-5 (resilience/HTTP client), fn-16 (AOT architecture depth)
- [ ] Both skills contain deferred fn-7 testing placeholders using standardized format: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` marker (this satisfies fn-7 boundary requirement per epic applicability matrix)
- [ ] Skill `name` values are locally unique within fn-6 skills (advisory pre-check; hard gate in fn-6.2)
- [ ] Does NOT modify `plugin.json` (handled by fn-6.2)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
