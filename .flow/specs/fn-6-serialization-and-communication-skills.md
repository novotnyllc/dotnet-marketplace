# fn-6: Serialization & Communication Skills

## Overview
Delivers AOT-friendly serialization and service communication skills including System.Text.Json source generators, gRPC, real-time communication patterns, and service communication routing. These are **communication-focused** skills covering data formats and transport protocols. Core language patterns live in fn-3; architecture patterns in fn-5; Native AOT depth in fn-16.

## Scope
**Skills (4 total, directory: `skills/serialization/<name>/SKILL.md`):**

| Skill ID | Directory | Summary |
|----------|-----------|---------|
| `dotnet-serialization` | `skills/serialization/dotnet-serialization/` | AOT-friendly source-gen serialization: System.Text.Json source gen, Protobuf, MessagePack. Performance tradeoffs. |
| `dotnet-grpc` | `skills/serialization/dotnet-grpc/` | Full gRPC skill: service definition, code-gen, streaming, auth, load balancing, health checks |
| `dotnet-realtime-communication` | `skills/serialization/dotnet-realtime-communication/` | Service communication patterns: SignalR, JSON-RPC 2.0, Server-Sent Events, gRPC streaming. When to use what. |
| `dotnet-service-communication` | `skills/serialization/dotnet-service-communication/` | Higher-level routing skill with decision matrix mapping requirements to gRPC, SignalR, SSE, JSON-RPC, REST |

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills.

## Scope Boundaries

| Concern | fn-6 owns (serialization & communication) | Other epic owns (depth) | Enforcement |
|---|---|---|---|
| Source generators | Cross-references `[skill:dotnet-csharp-source-generators]`; mandatory in serialization, conditional in gRPC | fn-3: owns source generator authoring patterns | Grep validates cross-ref in serialization skill |
| AOT compatibility | Notes AOT-safe serialization choices; `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker | fn-16: owns AOT architecture, trimming strategies | Grep validates `[skill:dotnet-native-aot]` + `TODO(fn-16)` in all 4 skills |
| HTTP client / REST | `dotnet-service-communication` routes REST questions to `[skill:dotnet-http-client]` | fn-5: owns IHttpClientFactory patterns | Cross-ref validates routing |
| Resilience | Cross-references `[skill:dotnet-resilience]` for retry/circuit-breaker on gRPC channels | fn-5: owns Polly v8 resilience patterns | Cross-ref in gRPC skill |
| Testing | Deferred cross-refs to fn-7 skills with `TODO(fn-7)` marker — added when fn-7 lands | fn-7: owns testing strategies and frameworks | Grep validates `TODO(fn-7)` markers; fn-7 reconciliation replaces |
| Blazor SignalR | fn-6 covers SignalR transport patterns; Blazor-specific usage deferred to fn-12 | fn-12: owns Blazor skills | Out-of-scope boundary statement in realtime skill |

## Deferred Cross-Reference Format
All deferred cross-references follow a standardized format:
- Literal cross-ref ID: `[skill:dotnet-native-aot]`, `[skill:dotnet-integration-testing]`
- TODO marker: `TODO(fn-16)`, `TODO(fn-7)`
- Example: `<!-- TODO(fn-16): Replace with canonical cross-ref when fn-16 lands --> See [skill:dotnet-native-aot] for AOT architecture depth.`

## Boundary Applicability Matrix
Not all boundary epics require explicit out-of-scope statements in all skills. The fn-7 (testing) boundary is satisfied by the deferred placeholder format above — skills include literal fn-7 skill IDs with `TODO(fn-7)` markers rather than separate out-of-scope prose.

| Epic boundary | fn-6.1 skills | fn-6.2 skills | Enforcement mechanism |
|---|---|---|---|
| fn-3 (source generators) | Out-of-scope statement | N/A | Grep for boundary text |
| fn-5 (resilience/HTTP) | Out-of-scope statement | Out-of-scope statement | Grep for boundary text |
| fn-7 (testing) | Deferred placeholder format | Deferred placeholder format | Grep for `TODO(fn-7)` + literal skill ID |
| fn-12 (Blazor) | N/A | Out-of-scope statement in realtime | Grep for boundary text |
| fn-16 (AOT) | Out-of-scope statement | Out-of-scope statement | Grep for boundary text + `TODO(fn-16)` |

## Task Decomposition

### fn-6.1: Serialization and gRPC skills (parallelizable content, fn-6.2 owns integration)
**Delivers:** `dotnet-serialization`, `dotnet-grpc`
- `skills/serialization/dotnet-serialization/SKILL.md`
- `skills/serialization/dotnet-grpc/SKILL.md`
- Both require `name` and `description` frontmatter
- `dotnet-serialization` covers STJ source generators, Protobuf, MessagePack with performance tradeoffs
- `dotnet-serialization` warns against reflection-based serialization (Newtonsoft.Json) for AOT
- `dotnet-serialization` mandatory cross-ref: `[skill:dotnet-csharp-source-generators]`
- `dotnet-grpc` covers .proto definition, code-gen, ASP.NET Core gRPC server implementation + endpoint hosting, Grpc.Net.Client for client patterns, all 4 streaming patterns (unary, server streaming, client streaming, bidirectional streaming — each named explicitly), auth, load balancing, health checks
- `dotnet-grpc` conditional cross-ref: `[skill:dotnet-csharp-source-generators]` only if discussing generator-adjacent scenarios
- `dotnet-grpc` cross-references `[skill:dotnet-resilience]` for retry/circuit-breaker on gRPC channels
- Both include `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker
- Both include deferred fn-7 testing placeholders using standardized format: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` marker
- Both include explicit out-of-scope boundary statements for fn-3, fn-5, fn-16
- Skill name uniqueness: advisory pre-check in fn-6.1 (hard gate in fn-6.2)
- Does NOT touch `plugin.json` (handled by fn-6.2)

### fn-6.2: Real-time and service communication routing skills + integration (depends on fn-6.1 for cross-ref targets)
**Delivers:** `dotnet-realtime-communication`, `dotnet-service-communication`, plus plugin registration for all 4 skills
- `skills/serialization/dotnet-realtime-communication/SKILL.md`
- `skills/serialization/dotnet-service-communication/SKILL.md`
- `dotnet-realtime-communication` compares SignalR, SSE (.NET 10 built-in), JSON-RPC 2.0, gRPC streaming
- `dotnet-realtime-communication` includes out-of-scope boundary for fn-12 (Blazor-specific SignalR)
- `dotnet-service-communication` contains decision matrix mapping requirements to all 5 protocols: gRPC, SignalR, SSE, JSON-RPC, REST — with cross-refs to deeper skills
- Both include `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker — required in both (not conditional)
- Both include deferred fn-7 testing placeholders using standardized format: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` marker
- `dotnet-realtime-communication` includes out-of-scope boundary for fn-12 (Blazor-specific SignalR); `dotnet-service-communication` does not require fn-12 boundary (not SignalR-focused)
- Both include explicit out-of-scope boundary statements for fn-5 and fn-16 (fn-7 boundary satisfied by deferred placeholder format per applicability matrix)
- Registers all 4 skill paths in `.claude-plugin/plugin.json`, grouped under `skills/serialization/*`, alphabetical within group
- Runs `./scripts/validate-skills.sh` and repo-wide name uniqueness check (hard gate)
- Grep validates: `[skill:dotnet-native-aot]` in all 4 skills, `TODO(fn-16)` markers in all 4, `TODO(fn-7)` markers with literal fn-7 skill IDs
- Single owner of `plugin.json` changes — eliminates merge conflicts

**fn-7 Reconciliation:** When fn-7 lands, a follow-up task must replace `TODO(fn-7)` markers and deferred placeholder comments with canonical `[skill:...]` cross-references. This reconciliation is tracked as a dependency note in fn-7's spec.

## Key Context
- System.Text.Json source generators are AOT-friendly and required for Native AOT
- Reflection-based serialization (Newtonsoft.Json) is incompatible with trimming/AOT
- .NET 10 brings built-in Server-Sent Events support to ASP.NET Core
- gRPC is the recommended approach for service-to-service communication in .NET
- Protobuf is the default gRPC wire format; MessagePack is an alternative for specific scenarios
- SignalR supports multiple transports: WebSockets, Server-Sent Events, Long Polling
- JSON-RPC 2.0 is used by Language Server Protocol and some .NET tooling

## Quick Commands
```bash
# Validate all 4 skills exist with frontmatter
for s in dotnet-serialization dotnet-grpc dotnet-realtime-communication dotnet-service-communication; do
  test -f "skills/serialization/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate frontmatter has required fields (name AND description)
for s in skills/serialization/*/SKILL.md; do
  grep -q "^name:" "$s" && grep -q "^description:" "$s" && echo "OK: $s" || echo "MISSING FRONTMATTER: $s"
done

# Repo-wide skill name uniqueness check
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty (no duplicates)

# Canonical frontmatter validation
./scripts/validate-skills.sh

# Verify serialization skill covers source generators (mandatory cross-ref)
grep "\[skill:dotnet-csharp-source-generators\]" skills/serialization/dotnet-serialization/SKILL.md

# Verify gRPC covers all 4 streaming patterns explicitly (separate checks for deterministic evidence)
grep -qi "unary" skills/serialization/dotnet-grpc/SKILL.md && echo "OK: unary" || echo "MISSING: unary"
grep -qi "server streaming" skills/serialization/dotnet-grpc/SKILL.md && echo "OK: server streaming" || echo "MISSING: server streaming"
grep -qi "client streaming" skills/serialization/dotnet-grpc/SKILL.md && echo "OK: client streaming" || echo "MISSING: client streaming"
grep -qi "bidirectional" skills/serialization/dotnet-grpc/SKILL.md && echo "OK: bidirectional" || echo "MISSING: bidirectional"

# Verify gRPC covers server-side patterns (ASP.NET Core gRPC)
grep -qi "service implementation\|endpoint hosting\|MapGrpcService\|GrpcService" skills/serialization/dotnet-grpc/SKILL.md && echo "OK: server patterns" || echo "MISSING: server patterns"

# Verify AOT deferred placeholders (standardized format)
grep -r "\[skill:dotnet-native-aot\]" skills/serialization/  # expect 4 matches
grep -r "TODO(fn-16)" skills/serialization/  # expect 4 matches

# Verify fn-7 deferred testing placeholders in all 4 skills (literal skill ID + TODO marker)
for s in dotnet-serialization dotnet-grpc dotnet-realtime-communication dotnet-service-communication; do
  grep -q "TODO(fn-7)" "skills/serialization/$s/SKILL.md" && echo "OK: $s TODO(fn-7)" || echo "MISSING: $s TODO(fn-7)"
  grep -q "\[skill:dotnet-integration-testing\]" "skills/serialization/$s/SKILL.md" && echo "OK: $s fn-7 skill ID" || echo "MISSING: $s fn-7 skill ID"
done

# Verify cross-references
grep -r "\[skill:dotnet-resilience\]" skills/serialization/dotnet-grpc/SKILL.md
grep -r "\[skill:dotnet-http-client\]" skills/serialization/dotnet-service-communication/SKILL.md

# Verify service-communication decision matrix covers all 5 protocols (separate checks for deterministic evidence)
grep -qi "gRPC" skills/serialization/dotnet-service-communication/SKILL.md && echo "OK: gRPC" || echo "MISSING: gRPC"
grep -qi "SignalR" skills/serialization/dotnet-service-communication/SKILL.md && echo "OK: SignalR" || echo "MISSING: SignalR"
grep -qi "SSE\|Server-Sent Events" skills/serialization/dotnet-service-communication/SKILL.md && echo "OK: SSE" || echo "MISSING: SSE"
grep -qi "JSON-RPC" skills/serialization/dotnet-service-communication/SKILL.md && echo "OK: JSON-RPC" || echo "MISSING: JSON-RPC"
grep -qi "REST" skills/serialization/dotnet-service-communication/SKILL.md && echo "OK: REST" || echo "MISSING: REST"

# Verify out-of-scope boundary statements
grep -l "fn-12\|Blazor" skills/serialization/dotnet-realtime-communication/SKILL.md  # expect 1
grep -l "out-of-scope\|boundary" skills/serialization/*/SKILL.md | wc -l  # expect 4

# Verify plugin.json ordering (serialization skills grouped and alphabetical)
grep "skills/serialization" .claude-plugin/plugin.json
```

## Acceptance Criteria
1. All 4 skills exist at `skills/serialization/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. Serialization skill covers STJ source generators, Protobuf, MessagePack with AOT compatibility notes
3. Serialization skill includes performance tradeoff guidance (STJ vs Protobuf vs MessagePack)
4. Serialization skill warns against reflection-based serialization (Newtonsoft.Json) for AOT scenarios
5. gRPC skill covers full lifecycle: .proto definition, code-gen, client/server patterns, all 4 streaming patterns named explicitly (unary, server streaming, client streaming, bidirectional streaming)
6. gRPC skill covers authentication, load balancing, health checks, and Grpc.Net.Client usage
6a. gRPC skill cross-references `[skill:dotnet-resilience]` for retry/circuit-breaker on gRPC channels
7. Real-time communication skill compares SignalR, SSE (.NET 10 built-in), JSON-RPC 2.0, gRPC streaming with decision guidance
8. Service communication skill contains decision matrix mapping requirements to all 5 protocols: gRPC, SignalR, SSE, JSON-RPC, REST — with cross-refs to deeper skills
9. Serialization skill mandatory cross-ref: `[skill:dotnet-csharp-source-generators]`; gRPC skill conditional cross-ref only if discussing generator-adjacent scenarios
10. All 4 skills include `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker (standardized deferred placeholder format)
11. Each skill contains explicit out-of-scope boundary statements per the applicability matrix: fn-3 (fn-6.1 only), fn-5, fn-12 (realtime skill only), fn-16 — grep-validated. fn-7 boundary is satisfied by deferred placeholder format (criterion #12), not separate prose.
12. All 4 skills contain deferred fn-7 testing placeholders using standardized format: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` marker
13. All 4 skills registered in `.claude-plugin/plugin.json`, grouped under `skills/serialization/*`, alphabetical within group
14. `./scripts/validate-skills.sh` passes for all 4 skills
15. Skill `name` frontmatter values are unique repo-wide (hard gate in fn-6.2; advisory in fn-6.1)
16. fn-6.1 content is parallelizable with fn-6.2 content work; fn-6.2 owns plugin.json integration (file-disjoint for skill content)

## Test Notes
- Verify serialization skill detects non-AOT-friendly patterns (reflection-based serialization)
- Test that service-communication skill routes to appropriate specialized skills via decision matrix
- Validate gRPC skill covers both ASP.NET Core gRPC and Grpc.Net.Client
- Validate gRPC skill names all 4 streaming patterns explicitly (not just "streaming")
- Verify SSE coverage notes .NET 10 built-in support
- Verify SignalR coverage includes transport negotiation and fallback
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide
- Verify `[skill:dotnet-native-aot]` and `TODO(fn-16)` present in all 4 skills
- Verify `TODO(fn-7)` deferred testing placeholders present
- Verify boundary cross-references use canonical skill IDs (not shorthand)
- Verify out-of-scope boundary statements are present where applicable
- Verify `plugin.json` contains all 4 serialization skill paths after fn-6.2, grouped and alphabetical

## References
- System.Text.Json Source Generators: https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/source-generation
- gRPC for .NET: https://learn.microsoft.com/en-us/aspnet/core/grpc/?view=aspnetcore-10.0
- Native AOT Deployment: https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/
- SignalR: https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction?view=aspnetcore-10.0
- Server-Sent Events (.NET 10): https://learn.microsoft.com/en-us/aspnet/core/fundamentals/server-sent-events?view=aspnetcore-10.0
- dotnet-skills serialization reference: https://github.com/Aaronontheweb/dotnet-skills
