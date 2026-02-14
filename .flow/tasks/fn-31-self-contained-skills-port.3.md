# fn-31-self-contained-skills-port.3 Port gRPC and SignalR skills

## Description
Create two skills: skills/communication/dotnet-grpc/SKILL.md for gRPC patterns and skills/communication/dotnet-signalr/SKILL.md for SignalR real-time communication. Port and adapt from dotnet-skills reference material, crediting original authors.

**Size:** M
**Files:** skills/communication/dotnet-grpc/SKILL.md, skills/communication/dotnet-signalr/SKILL.md, .claude-plugin/plugin.json

## Approach
- gRPC: proto definitions, server/client generation, streaming (server, client, bidirectional), interceptors, deadline/cancellation, gRPC-Web for browser clients
- SignalR: hub design, strongly-typed hubs, client integration (JS/.NET), groups, connection lifecycle, scaling with Redis backplane
- Both: use latest stable package versions, credit Aaronontheweb/dotnet-skills
## Acceptance
- [ ] gRPC skill covers service definitions, streaming, interceptors
- [ ] SignalR skill covers hubs, groups, scaling
- [ ] Latest stable package versions
- [ ] Original authors credited
- [ ] Both registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
