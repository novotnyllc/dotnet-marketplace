# fn-31-self-contained-skills-port.3 Enhance gRPC and SignalR skills

## Description
Enhance two existing skills with ported content from dotnet-skills: `skills/serialization/dotnet-grpc/SKILL.md` for gRPC patterns and `skills/serialization/dotnet-realtime-communication/SKILL.md` for SignalR real-time communication. Credit original authors.

**Size:** M
**Files:** skills/serialization/dotnet-grpc/SKILL.md, skills/serialization/dotnet-realtime-communication/SKILL.md

## Approach
- Read both existing skills first to understand current coverage and avoid duplication
- gRPC (`skills/serialization/dotnet-grpc/`): enhance with interceptors, streaming patterns (server/client/bidirectional), deadline/cancellation, gRPC-Web for browser clients
- SignalR (`skills/serialization/dotnet-realtime-communication/`): enhance with hub design, strongly-typed hubs, groups, connection lifecycle, scaling with Redis backplane
- Both: use latest stable package versions, credit Aaronontheweb/dotnet-skills via `## Attribution`
- No plugin.json change needed (both skills already registered)

## Acceptance
- [ ] Existing gRPC skill enhanced with interceptors, streaming, gRPC-Web
- [ ] Existing SignalR/real-time skill enhanced with hubs, groups, scaling
- [ ] Latest stable package versions
- [ ] Original authors credited via `## Attribution` section
- [ ] Descriptions under 120 chars
- [ ] Validation passes

## Done summary
Enhanced gRPC skill with gRPC-Web section (server config, JS client, Envoy proxy, limitations) and SignalR/real-time skill with connection lifecycle, groups management, client-to-server streaming, JWT authentication, IUserIdProvider, and Azure SignalR Service scaling. Removed fn-N references and added Attribution sections crediting Aaronontheweb/dotnet-skills.
## Evidence
- Commits: c3d09fcc4369738f8912c7acc41e2adc1ad68b22
- Tests: ./scripts/validate-skills.sh, python3 scripts/generate_dist.py --strict
- PRs: