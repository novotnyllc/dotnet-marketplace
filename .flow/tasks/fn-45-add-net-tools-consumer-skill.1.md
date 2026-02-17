# fn-45-add-net-tools-consumer-skill.1 Author dotnet-tool-management SKILL.md

## Description
Author `skills/cli-tools/dotnet-tool-management/SKILL.md` covering the consumer perspective of .NET tools: installing, managing manifests, restoring in CI, and consuming RID-specific tools.

**Size:** M
**Files:** `skills/cli-tools/dotnet-tool-management/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/cli-tools/dotnet-cli-packaging/SKILL.md` for style
- Cover: `dotnet tool install -g`, `dotnet tool install` (local), `dotnet tool restore`
- Cover `.config/dotnet-tools.json` manifest creation, version pinning, team workflows
- Cover RID-specific tool consumption per https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools
- Cover CI integration: tool restore before build
- Reference: https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools

## Key context

- `dotnet-cli-packaging` (lines 381-451) covers the PRODUCER side — this skill covers CONSUMER
- `dotnet-project-analysis` (lines 244-251) already detects `.config/dotnet-tools.json` but does not guide creation
- Dotnet tools are framework-dependent by default; RID-specific tools use `ToolPackageRuntimeIdentifiers` on packaging side
## Acceptance
- [ ] SKILL.md exists at `skills/cli-tools/dotnet-tool-management/`
- [ ] Valid frontmatter with `name` and `description` (under 120 chars)
- [ ] Covers global vs local tool installation
- [ ] Covers `.config/dotnet-tools.json` manifest management
- [ ] Covers `dotnet tool restore` in CI
- [ ] Covers RID-specific tool consumption
- [ ] Cross-reference syntax used for related skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
