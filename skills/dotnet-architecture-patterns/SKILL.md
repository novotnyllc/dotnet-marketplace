---
name: dotnet-architecture-patterns
description: Designs ASP.NET Core architecture -- vertical slices, pipelines, caching, errors.
license: MIT
user-invocable: false
---

# dotnet-architecture-patterns

Modern architecture patterns for .NET applications. Covers practical approaches to organizing minimal APIs at scale, vertical slice architecture, request pipeline composition, validation strategies, caching, error handling, and idempotency/outbox patterns.

## Scope

- Vertical slice architecture and feature-folder organization
- Request pipeline composition and MediatR patterns
- Caching strategies (memory, distributed, output caching, HybridCache)
- Error handling and problem details (RFC 9457)
- Idempotency and outbox patterns
- Result pattern for business logic error flow

## Out of scope

- DI container mechanics and async/await patterns -- see [skill:dotnet-csharp-dependency-injection] and [skill:dotnet-csharp-async-patterns]
- Project scaffolding and file layout -- see [skill:dotnet-scaffold-project]
- Testing strategies -- see [skill:dotnet-testing-strategy] and [skill:dotnet-integration-testing]
- SOLID principles and design pattern foundations -- see [skill:dotnet-solid-principles]

Cross-references: [skill:dotnet-csharp-dependency-injection] for service registration and lifetimes, [skill:dotnet-csharp-async-patterns] for async pipeline patterns, [skill:dotnet-csharp-configuration] for Options pattern in configuration, [skill:dotnet-solid-principles] for SOLID/DRY design principles governing class and interface design.

---


For detailed code examples (vertical slices, minimal API organization, pipeline composition, error handling, caching, idempotency, outbox), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Idempotency must handle three states** -- An idempotency implementation must distinguish no-record (claim it), in-progress (reject duplicate), and completed (replay cached response). Check-then-act without guarding the in-progress state allows concurrent duplicate execution.
2. **Always finalize idempotency records unconditionally** -- Do NOT gate completion on specific `IResult` subtypes (e.g., `IValueHttpResult`). Non-value results like `Results.NoContent()` or `Results.Accepted()` would be left permanently stuck in the in-progress state.
3. **Cache invalidation must be explicit** -- When using output caching or distributed caching, ALWAYS invalidate (evict by tag or key) after write operations. Forgetting invalidation causes stale reads that are hard to debug.
4. **HybridCache stampede protection only works with `GetOrCreateAsync`** -- Do NOT use separate get-then-set patterns with `HybridCache`; use the factory overload so the library serializes concurrent requests for the same key.
5. **Outbox messages must be written in the same transaction as domain data** -- If you write the outbox message outside the domain transaction, a crash between the two writes loses the event. ALWAYS use `BeginTransactionAsync` to wrap both writes atomically.
6. **Endpoint filter order matters** -- Filters added first run outermost. A validation filter must run before an idempotency filter, otherwise invalid requests get cached as idempotent responses.
7. **Do NOT share `DbContext` across concurrent requests** -- `DbContext` is not thread-safe. Each request must resolve its own scoped instance from DI. Using a singleton or static `DbContext` causes data corruption under concurrency.

---

## Knowledge Sources

Architecture patterns in this skill are grounded in publicly available content from:

- **Jimmy Bogard's Vertical Slice Architecture** -- Organizing code by feature instead of by technical layer. Bogard advocates that each vertical slice owns its own request, handler, validation, and data access, reducing cross-feature coupling. He originated the popular MediatR library for request/handler dispatch in .NET, though MediatR is now commercial for commercial use. When applying vertical slice guidance, prefer the built-in IEndpointFilter and handler pattern shown above rather than introducing a third-party mediator dependency for simple scenarios. Source: https://www.jimmybogard.com/vertical-slice-architecture/
- **Jimmy Bogard's Domain-Driven Design Patterns** -- Rich domain model guidance including entity design, value objects, domain events, and aggregate boundaries. Key insight: domain events should be dispatched after the aggregate state change is persisted (not before), to avoid inconsistency if persistence fails. Source: https://www.jimmybogard.com/
- **Nick Chapsas' Modern .NET Patterns** -- Practical patterns for modern .NET including result types for error handling, structured validation pipelines, and modern C# feature adoption in production codebases. Source: https://www.youtube.com/@nickchapsas

> **Note:** This skill applies publicly documented guidance. It does not represent or speak for the named sources. MediatR is a commercial product for commercial use; the patterns here are demonstrated with built-in .NET mechanisms.

## References

- [ASP.NET Core Best Practices](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/best-practices?view=aspnetcore-10.0)
- [Minimal APIs overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/overview)
- [Output caching middleware](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output)
- [HybridCache library](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid)
- [Problem Details (RFC 9457)](https://www.rfc-editor.org/rfc/rfc9457)
- [Endpoint filters in minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/min-api-filters)
- [Vertical Slice Architecture (Jimmy Bogard)](https://www.jimmybogard.com/vertical-slice-architecture/)
