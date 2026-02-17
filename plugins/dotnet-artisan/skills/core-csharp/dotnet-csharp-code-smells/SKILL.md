---
name: dotnet-csharp-code-smells
description: "Reviewing C# for logic issues. Anti-patterns, common pitfalls, async misuse, DI mistakes."
---

# dotnet-csharp-code-smells

Proactive code-smell and anti-pattern detection for C# code. This skill triggers during all workflow modes -- planning, implementation, and review. Each entry identifies the smell, explains why it is harmful, provides the correct fix, and references the relevant CA rule or cross-reference.

Cross-references: [skill:dotnet-csharp-async-patterns] for async gotchas, [skill:dotnet-csharp-coding-standards] for naming and style, [skill:dotnet-csharp-dependency-injection] for DI lifetime misuse, [skill:dotnet-csharp-nullable-reference-types] for NRT annotation mistakes.

**Out of Scope:** LLM-specific generation mistakes (wrong NuGet packages, bad project structure, MSBuild errors) are covered by [skill:dotnet-agent-gotchas]. This skill covers general .NET code smells that any developer -- human or AI -- should avoid.

---

## 1. Resource Management (IDisposable Misuse)

| Smell | Why Harmful | Fix | Rule |
|-------|-------------|-----|------|
| Missing `using` on disposable locals | Leaks unmanaged handles (sockets, files, DB connections) | Wrap in `using` declaration or `using` block | CA2000 |
| Undisposed `IDisposable` fields | Class holds disposable resource but never disposes it | Implement `IDisposable`; dispose fields in `Dispose()` | CA2213 |
| Wrong Dispose pattern (no finalizer guard) | Double-dispose or missed cleanup on GC finalization | Follow canonical `Dispose(bool)` pattern; call `GC.SuppressFinalize(this)` | CA1816 |
| Disposable created in one method, stored in field | Ownership unclear; easy to forget disposal | Document ownership; make the containing class `IDisposable` | CA2000 |
| `using` on non-owned resource | Premature disposal of shared resource (e.g., injected `HttpClient`) | Only dispose resources you create; let DI manage injected services | -- |

See `details.md` for code examples of each pattern.

---

## 2. Warning Suppression Hacks

| Smell | Why Harmful | Fix | Rule |
|-------|-------------|-----|------|
| Invoking event with `null` to suppress CS0067 | Creates misleading runtime behavior; masks real bugs | Use `#pragma warning disable CS0067` or explicit event accessors `{ add {} remove {} }` | CS0067 |
| Dummy variable assignments to suppress CS0219 | Dead code that confuses readers | Use `_ = expression;` discard or `#pragma warning disable` | CS0219 |
| Blanket `#pragma warning disable` without restore | Suppresses ALL warnings for rest of file | Always pair with `#pragma warning restore`; suppress specific codes only | -- |
| `[SuppressMessage]` without justification | Future maintainers cannot evaluate if suppression is still valid | Always include `Justification = "reason"` | CA1303 |

See `details.md` for the CS0067 motivating example (bad pattern to correct fix).

---

## 3. LINQ Anti-Patterns

| Smell | Why Harmful | Fix | Rule |
|-------|-------------|-----|------|
| Premature `.ToList()` mid-chain | Forces full materialization; wastes memory | Keep chain lazy; materialize only at the end | CA1851 |
| Multiple enumeration of `IEnumerable<T>` | Re-executes query or DB call on each enumeration | Materialize once with `.ToList()` then reuse | CA1851 |
| Client-side evaluation in EF Core | Loads entire table into memory; silent perf bomb | Rewrite query as translatable LINQ or use `AsAsyncEnumerable()` with explicit intent | -- |
| `.Count() > 0` instead of `.Any()` | Enumerates entire collection instead of short-circuiting | Use `.Any()` for existence checks | CA1827 |
| Nested `foreach` instead of `.Join()` or `.GroupJoin()` | O(n*m) when O(n+m) is possible | Use LINQ join operations or `Dictionary` lookup | -- |
| `.Where().First()` instead of `.First(predicate)` | Creates unnecessary intermediate iterator | Pass predicate directly to `.First()` or `.FirstOrDefault()` | CA1826 |

---

## 4. Event Handling Leaks

| Smell | Why Harmful | Fix | Rule |
|-------|-------------|-----|------|
| Not unsubscribing from events | Memory leak: publisher holds reference to subscriber | Unsubscribe in `Dispose()` or use weak event pattern | -- |
| Raising events in constructor | Subscribers may not be attached yet; derived class not fully constructed | Raise events only from fully initialized instances | CA2214 |
| `async void` event handler (misused) | `async void` is the only valid signature for event handlers, but exceptions are unobservable | Wrap body in try/catch; log and handle exceptions explicitly | -- |
| Event handler not checking for null | `NullReferenceException` when no subscribers | Use `event?.Invoke()` null-conditional pattern | -- |
| Static event without cleanup | Rooted references prevent GC for application lifetime | Prefer instance events or use `WeakEventManager` | -- |

Cross-reference: [skill:dotnet-csharp-async-patterns] covers `async void` fire-and-forget patterns in depth.

---

## 5. Design Smells

| Smell | Threshold | Why Harmful | Fix |
|-------|-----------|-------------|-----|
| God class | >500 lines | Too many responsibilities; hard to test and maintain | Extract cohesive classes using SRP |
| Long method | >30 lines | Hard to understand, test, and review | Extract helper methods with descriptive names |
| Long parameter list | >5 parameters | Indicates missing abstraction | Introduce parameter object or builder |
| Feature envy | Method uses another class's data more than its own | Misplaced responsibility; tight coupling | Move method to the class it envies |
| Primitive obsession | Domain concepts represented as raw `string`/`int` | No type safety; validation scattered | Introduce value objects or strongly-typed IDs |
| Deep nesting | >3 levels of indentation | Hard to follow control flow | Use guard clauses (early return) and extract methods |

---

## 6. Exception Handling Gaps

| Smell | Why Harmful | Fix | Rule |
|-------|-------------|-----|------|
| Empty catch block | Silently swallows errors; masks bugs | At minimum, log the exception; prefer letting it propagate | CA1031 |
| Catching base `Exception` | Catches `OutOfMemoryException`, `StackOverflowException`, etc. | Catch specific exception types | CA1031 |
| Log-and-swallow (`catch { log; }`) | Caller never learns operation failed | Re-throw after logging, or return error result | -- |
| Throwing in `finally` | Masks original exception with the new one | Use try/catch inside finally; never throw from finally | -- |
| `throw ex;` instead of `throw;` | Resets stack trace; hides original failure location | Use bare `throw;` to preserve stack trace | CA2200 |
| Not including inner exception | Loses causal chain when wrapping exceptions | Pass original as `innerException` parameter | -- |

Cross-reference: [skill:dotnet-csharp-async-patterns] covers exception handling in fire-and-forget and async void scenarios.

---

## Quick Reference: CA Rules

| Rule | Description |
|------|-------------|
| CA1031 | Do not catch general exception types |
| CA1816 | Call `GC.SuppressFinalize` correctly |
| CA1826 | Do not use `Enumerable` methods on indexable collections |
| CA1827 | Do not use `Count()`/`LongCount()` when `Any()` can be used |
| CA1851 | Possible multiple enumerations of `IEnumerable` collection |
| CA2000 | Dispose objects before losing scope |
| CA2200 | Rethrow to preserve stack details |
| CA2213 | Disposable fields should be disposed |
| CA2214 | Do not call overridable methods in constructors |

Enable these via `<AnalysisLevel>latest-all</AnalysisLevel>` in your project. See [skill:dotnet-csharp-coding-standards] for analyzer configuration.

---

## References

- [Microsoft Code Quality Rules](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/)
- [Framework Design Guidelines](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- [David Fowler Async Guidance](https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md)
