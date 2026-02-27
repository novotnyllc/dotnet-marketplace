---
name: dotnet-api
description: Builds ASP.NET Core APIs, data access, and backend services. Covers minimal APIs, middleware, EF Core (patterns and architecture), gRPC, SignalR/SSE, resilience (Polly), HTTP client, API versioning, OpenAPI, security (OWASP, secrets, crypto), background services, Aspire orchestration, Semantic Kernel AI integration, architecture patterns, messaging, service communication, data access strategy, API surface validation, and API documentation.
license: MIT
user-invocable: false
---

# dotnet-api

## Overview

ASP.NET Core APIs, data access, backend services, security, and cloud-native patterns. This consolidated skill spans 27 topic areas. Load the appropriate companion file from `references/` based on the routing table below.

Baseline dependency: `references/minimal-apis.md` defines the core ASP.NET Core Minimal API patterns (route groups, endpoint filters, TypedResults, parameter binding) that apply to most API development tasks. Load it by default when building HTTP endpoints.

Most-shared companion: `references/architecture-patterns.md` covers vertical slices, request pipelines, error handling, caching, and idempotency patterns used across nearly all ASP.NET Core projects.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Minimal APIs | endpoint, route group, filter, TypedResults | references/minimal-apis.md |
| Middleware | pipeline ordering, short-circuit, exception | references/middleware-patterns.md |
| EF Core patterns | DbContext, migrations, AsNoTracking | references/efcore-patterns.md |
| EF Core architecture | read/write split, aggregate boundaries, N+1 | references/efcore-architecture.md |
| Data access strategy | EF Core vs Dapper vs ADO.NET decision | references/data-access-strategy.md |
| gRPC | proto, code-gen, streaming, auth | references/grpc.md |
| Real-time | SignalR, SSE, JSON-RPC, gRPC streaming | references/realtime-communication.md |
| Resilience | Polly v8, retry, circuit breaker, timeout | references/resilience.md |
| HTTP client | IHttpClientFactory, typed/named, DelegatingHandler | references/http-client.md |
| API versioning | Asp.Versioning, URL/header/query, sunset | references/api-versioning.md |
| OpenAPI | MS.AspNetCore.OpenApi, Swashbuckle, NSwag | references/openapi.md |
| API security | Identity, OAuth/OIDC, JWT, CORS, rate limiting | references/api-security.md |
| OWASP | injection, auth, XSS, deprecated APIs | references/security-owasp.md |
| Secrets | user secrets, env vars, rotation | references/secrets-management.md |
| Cryptography | AES-GCM, RSA, ECDSA, hashing, key derivation | references/cryptography.md |
| Background services | BackgroundService, IHostedService, lifecycle | references/background-services.md |
| Aspire | AppHost, service discovery, dashboard | references/aspire-patterns.md |
| Semantic Kernel | AI/LLM plugins, prompts, memory, agents | references/semantic-kernel.md |
| Architecture | vertical slices, layered, pipelines, caching | references/architecture-patterns.md |
| Messaging | MassTransit, Azure Service Bus, pub/sub, sagas | references/messaging-patterns.md |
| Service communication | REST vs gRPC vs SignalR decision matrix | references/service-communication.md |
| API surface validation | PublicApiAnalyzers, Verify, ApiCompat | references/api-surface-validation.md |
| Library API compat | binary/source compat, type forwarders | references/library-api-compat.md |
| I/O pipelines | PipeReader/PipeWriter, backpressure, Kestrel | references/io-pipelines.md |
| Agent gotchas | async misuse, NuGet errors, DI mistakes | references/agent-gotchas.md |
| File-based apps | .NET 10, directives, csproj migration | references/file-based-apps.md |
| API docs | DocFX, OpenAPI-as-docs, versioned docs | references/api-docs.md |

## Scope

- ASP.NET Core web APIs (minimal and controller-based)
- Data access (EF Core, Dapper, ADO.NET)
- Service communication (gRPC, SignalR, SSE, messaging)
- Security (auth, OWASP, secrets, crypto)
- Cloud-native (Aspire, resilience, background services)
- AI integration (Semantic Kernel)
- Architecture patterns

## Out of scope

- C# language features -> [skill:dotnet-csharp]
- UI rendering -> [skill:dotnet-ui]
- Test authoring -> [skill:dotnet-testing]
- CI/CD pipelines -> [skill:dotnet-devops]
- Build tooling -> [skill:dotnet-tooling]

## Companion Files

- `references/minimal-apis.md` -- Minimal API route groups, filters, TypedResults, OpenAPI
- `references/middleware-patterns.md` -- Pipeline ordering, short-circuit, exception handling
- `references/efcore-patterns.md` -- DbContext, AsNoTracking, query splitting, migrations
- `references/efcore-architecture.md` -- Read/write split, aggregate boundaries, N+1
- `references/data-access-strategy.md` -- EF Core vs Dapper vs ADO.NET decision matrix
- `references/grpc.md` -- Proto definition, code-gen, ASP.NET Core host, streaming
- `references/realtime-communication.md` -- SignalR hubs, SSE, JSON-RPC 2.0, scaling
- `references/resilience.md` -- Polly v8 retry, circuit breaker, timeout, rate limiter
- `references/http-client.md` -- IHttpClientFactory, typed/named clients, DelegatingHandlers
- `references/api-versioning.md` -- Asp.Versioning.Http/Mvc, URL/header/query, sunset
- `references/openapi.md` -- MS.AspNetCore.OpenApi, Swashbuckle migration, NSwag
- `references/api-security.md` -- Identity, OAuth/OIDC, JWT bearer, CORS, rate limiting
- `references/security-owasp.md` -- OWASP Top 10 hardening for .NET
- `references/secrets-management.md` -- User secrets, environment variables, rotation
- `references/cryptography.md` -- AES-GCM, RSA, ECDSA, hashing, PQC key derivation
- `references/background-services.md` -- BackgroundService, IHostedService, lifecycle
- `references/aspire-patterns.md` -- AppHost, service discovery, components, dashboard
- `references/semantic-kernel.md` -- AI/LLM plugins, prompt templates, memory, agents
- `references/architecture-patterns.md` -- Vertical slices, layered, pipelines, caching
- `references/messaging-patterns.md` -- MassTransit, Azure Service Bus, pub/sub, sagas
- `references/service-communication.md` -- REST vs gRPC vs SignalR decision matrix
- `references/api-surface-validation.md` -- PublicApiAnalyzers, Verify snapshots, ApiCompat
- `references/library-api-compat.md` -- Binary/source compat, type forwarders, SemVer
- `references/io-pipelines.md` -- PipeReader/PipeWriter, backpressure, Kestrel
- `references/agent-gotchas.md` -- Common agent mistakes in .NET code
- `references/file-based-apps.md` -- .NET 10 file-based C# apps
- `references/api-docs.md` -- DocFX, OpenAPI-as-docs, versioned documentation
