# fn-64-consolidate-131-skills-into-20-broad.8 Consolidate cross-cutting skills: dotnet-security, dotnet-observability, dotnet-docs, remaining

## Description
Create consolidated skill directories for cross-cutting skills and handle all remaining unmapped skills: `dotnet-security`, `dotnet-observability`, `dotnet-docs`, and a catch-all for remaining skills per the mapping from task .1.

**Size:** M
**Files:** `skills/dotnet-security/SKILL.md` + `references/*.md` (new), `skills/dotnet-observability/SKILL.md` + `references/*.md` (new), `skills/dotnet-docs/SKILL.md` + `references/*.md` (new), additional skills per mapping, `.claude-plugin/plugin.json`, remaining source dirs (delete)

## Approach

- Follow consolidation map from task .1
- `dotnet-security` merges: security-owasp, secrets-management, cryptography
- `dotnet-observability` merges: observability, structured-logging, io-pipelines
- `dotnet-docs` merges: documentation-strategy, mermaid-diagrams, github-docs, xml-docs, api-docs
- Handle remaining unmapped skills per task .1 output: dotnet-aspire-patterns, dotnet-semantic-kernel, dotnet-localization, dotnet-messaging-patterns, dotnet-domain-modeling, dotnet-background-services, dotnet-native-interop, dotnet-solid-principles, dotnet-serialization, dotnet-channels, dotnet-validation-patterns, dotnet-grpc, dotnet-realtime-communication, dotnet-service-communication, dotnet-http-client, dotnet-resilience, dotnet-multi-targeting, dotnet-version-upgrade, dotnet-version-detection, dotnet-file-based-apps, dotnet-agent-gotchas, dotnet-slopwatch, dotnet-solution-navigation

## Key context

- Many "remaining" skills may fold into existing groups per task .1 mapping (e.g., dotnet-resilience → dotnet-api, dotnet-channels → dotnet-csharp)
- Some may warrant their own consolidated skill (e.g., dotnet-aspire if big enough)
- Agent meta-skills (agent-gotchas, slopwatch, solution-navigation) may fold into dotnet-project-setup or dotnet-advisor
## Acceptance
- [ ] `skills/dotnet-security/SKILL.md` + `references/` created
- [ ] `skills/dotnet-observability/SKILL.md` + `references/` created
- [ ] `skills/dotnet-docs/SKILL.md` + `references/` created
- [ ] All remaining unmapped skills placed per task .1 mapping
- [ ] Zero old skill directories remain (all 131 original dirs removed or replaced)
- [ ] `plugin.json` contains only consolidated skill paths
- [ ] Valid frontmatter on all SKILL.md files
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
