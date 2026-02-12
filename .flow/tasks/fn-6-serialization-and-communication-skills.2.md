# fn-6-serialization-and-communication-skills.2 Real-time and service communication routing skills + integration

## Description
Create two skills: `dotnet-realtime-communication` (SignalR, JSON-RPC 2.0, Server-Sent Events, gRPC streaming — when to use what) and `dotnet-service-communication` (higher-level routing skill with decision matrix mapping requirements to gRPC, SignalR, SSE, JSON-RPC, and REST). Then integrate all 4 serialization/communication skills into `plugin.json`, run validation, and audit cross-references.

## Acceptance
- [ ] `skills/serialization/dotnet-realtime-communication/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `skills/serialization/dotnet-service-communication/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-realtime-communication` compares SignalR, SSE (.NET 10 built-in), JSON-RPC 2.0, gRPC streaming with decision guidance
- [ ] `dotnet-realtime-communication` cross-references `[skill:dotnet-grpc]` for gRPC streaming details
- [ ] `dotnet-realtime-communication` contains out-of-scope boundary statement for fn-12 (Blazor-specific SignalR usage)
- [ ] `dotnet-service-communication` contains decision matrix mapping requirements to all 5 protocols: gRPC, SignalR, SSE, JSON-RPC, REST
- [ ] `dotnet-service-communication` cross-references `[skill:dotnet-grpc]`, `[skill:dotnet-realtime-communication]`, `[skill:dotnet-http-client]` (fn-5)
- [ ] Both skills contain explicit out-of-scope boundary statements for: fn-5 (HTTP client/resilience) and fn-16 (AOT). fn-12 boundary required in `dotnet-realtime-communication` only (per applicability matrix).
- [ ] Both skills contain deferred fn-7 testing placeholders using standardized format: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` marker (this satisfies fn-7 boundary requirement per epic applicability matrix)
- [ ] Both skills include `[skill:dotnet-native-aot]` with `TODO(fn-16)` marker — required in both
- [ ] All 4 fn-6 skill paths registered in `.claude-plugin/plugin.json`, grouped under `skills/serialization/*`, alphabetical within group
- [ ] `./scripts/validate-skills.sh` passes for all 4 skills
- [ ] Skill `name` frontmatter values are unique repo-wide — hard gate (no duplicates across all `skills/*/*/SKILL.md`)
- [ ] Grep validation: `[skill:dotnet-native-aot]` present in all 4 skills; `TODO(fn-16)` markers present in all 4 skills
- [ ] Grep validation: `[skill:dotnet-integration-testing]` plus `TODO(fn-7)` present in all 4 skill files: `skills/serialization/dotnet-serialization/SKILL.md`, `skills/serialization/dotnet-grpc/SKILL.md`, `skills/serialization/dotnet-realtime-communication/SKILL.md`, `skills/serialization/dotnet-service-communication/SKILL.md`

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
