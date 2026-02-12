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
Created `dotnet-realtime-communication` and `dotnet-service-communication` skills, registered all 4 serialization skills in plugin.json.

- `dotnet-realtime-communication`: Compares SignalR, SSE (.NET 10 built-in), JSON-RPC 2.0, gRPC streaming with decision guidance, code examples, and transport patterns
- `dotnet-service-communication`: Decision matrix mapping requirements to gRPC, SignalR, SSE, JSON-RPC, REST with routing to deeper skills. Decision flowchart and architecture patterns.
- All 4 skills registered in plugin.json grouped under `skills/serialization/*`, alphabetical
- All grep validations pass: `[skill:dotnet-native-aot]` + `TODO(fn-16)` in all 4, `[skill:dotnet-integration-testing]` + `TODO(fn-7)` in all 4, out-of-scope boundaries present, fn-12 boundary in realtime skill, cross-refs validated, name uniqueness confirmed
- `validate-skills.sh` passes (0 errors)
## Evidence
- Commits:
- Tests: ./scripts/validate-skills.sh: PASSED (0 errors), grep [skill:dotnet-native-aot]: 4/4 skills, grep TODO(fn-16): 4/4 skills, grep TODO(fn-7): 4/4 skills, grep [skill:dotnet-integration-testing]: 4/4 skills, name uniqueness: no duplicates, fn-12 boundary in realtime skill: present, out-of-scope in all 4 skills: confirmed, plugin.json: 4 serialization skills registered alphabetically
- PRs: