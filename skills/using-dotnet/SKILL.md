---
name: using-dotnet
description: Detects .NET intent for any C#, ASP.NET Core, EF Core, Blazor, MAUI, Uno Platform, WPF, WinUI, SignalR, gRPC, xUnit, NuGet, or MSBuild request from prompt keywords and repository signals (.sln, .csproj, global.json, .cs files). First skill to invoke for all .NET work — loads version-specific coding standards and routes to domain skills via [skill:dotnet-advisor] before any planning or implementation. Do not use for clearly non-.NET tasks (Python, JavaScript, Go, Rust, Java).
license: MIT
user-invocable: false
---

# using-dotnet

## Scope

- Establishing .NET/C# routing discipline before clarifying questions, planning, command execution, or edits.
- Detecting .NET intent from prompt and repository signals (`.sln`, `.slnx`, `.csproj`, `global.json`, `.cs`).
- Enforcing first-step routing through [skill:dotnet-advisor] and baseline loading order.
- Defining priority and rigidity rules for downstream skill invocation.

## Out of scope

- C# implementation details and coding-standard specifics -> [skill:dotnet-csharp]
- Deep domain implementation patterns -> [skill:dotnet-api], [skill:dotnet-ui], [skill:dotnet-testing], [skill:dotnet-devops], [skill:dotnet-tooling], [skill:dotnet-debugging]
- Specialist deep-review workflows -> [skill:dotnet-security-reviewer], [skill:dotnet-performance-analyst], [skill:dotnet-testing-specialist]

## Why Routing Matters

.NET skills contain version-specific guidance (net8.0 vs net9.0 vs net10.0), coding standards, and framework-specific patterns that the model doesn't have in its training data. Skipping routing means the model confidently produces code using deprecated APIs, misses framework-specific patterns, or gives generic advice that ignores project context.

Routing before action ensures:
- **Version-aware guidance** loads before code generation (avoiding stale API suggestions)
- **Coding standards** apply from the start (not patched in after the fact)
- **Domain expertise** routes to the right specialist (avoiding generic advice for specialized problems)

The cost of routing is a few skill invocations. The cost of skipping is rework, stale advice, or subtle bugs.

## Routing Sequence

When a request likely involves .NET or C#, follow this sequence before any other action:

1. **Detect .NET intent** — Look for prompt keywords (C#, .NET, ASP.NET, EF Core, Blazor, MAUI, NuGet, csproj) or repository signals (`.sln`, `.slnx`, `.csproj`, `global.json`, `.cs` files). If either is present, continue.
2. **In a .NET repository, .NET is the default** — When repo signals are present, ambiguous requests like "build me a web app", "add a dashboard", or "write a script" should use .NET solutions (ASP.NET Core, Blazor, .NET file-based apps) rather than defaulting to JavaScript/Python. The user chose a .NET project for a reason.
3. **Invoke [skill:dotnet-advisor]** — This routes the request to the correct domain skills and loads coding standards.
4. **Follow advisor routing** — Load [skill:dotnet-csharp] baseline, then the domain skill(s) the advisor selects.
5. **Now respond** — Clarify, plan, explore, or implement with the right context loaded.

Routing applies even for "simple" questions and clarification requests. The skill loading is lightweight and ensures consistent quality.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first**: this skill, then [skill:dotnet-advisor].
2. **Baseline skill second**: [skill:dotnet-csharp] for any code path.
3. **Domain skills third**: [skill:dotnet-api], [skill:dotnet-ui], [skill:dotnet-testing], [skill:dotnet-devops], [skill:dotnet-tooling], [skill:dotnet-debugging].
4. **Specialist agents fourth**: use only when deeper analysis is required after routing.

## Skill Types

**Rigid** (must follow exactly): this skill, [skill:dotnet-advisor], and baseline-first ordering.

**Flexible** (adapt to context): Domain skills and their companion references.

User instructions define WHAT to do. This process defines HOW to route and load skills before execution.
