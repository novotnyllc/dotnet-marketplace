# fn-45-add-net-tools-consumer-skill.1 Author dotnet-tool-management SKILL.md

## Description
Author `skills/cli-tools/dotnet-tool-management/SKILL.md` covering the consumer perspective of .NET tools.

**Visibility:** Implicit (agent-loaded, not user-invocable)
**Size:** M
**Files:** `skills/cli-tools/dotnet-tool-management/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/cli-tools/dotnet-cli-packaging/SKILL.md` for style
- Cover: `dotnet tool install -g`, `dotnet tool install` (local), `dotnet tool restore`
- Cover `.config/dotnet-tools.json` manifest creation, version pinning, team workflows
- RID-specific: brief consumer note ("RID selection is automatic"), cross-ref to `dotnet-cli-packaging`
- Cover CI integration: tool restore before build
- Target description ~90 chars

## Key context

- `dotnet-cli-packaging` covers the PRODUCER side — this skill covers CONSUMER
- RID-specific tools from consumer perspective: `dotnet tool install` handles RID automatically
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
- [ ] Valid frontmatter with `name` and `description` (under 120 chars, ~90 target)
- [ ] Covers global vs local tool installation
- [ ] Covers `.config/dotnet-tools.json` manifest management
- [ ] Covers `dotnet tool restore` in CI
- [ ] RID-specific is brief note with cross-ref to packaging skill
- [ ] Cross-reference syntax used for related skills
## Done summary
Authored dotnet-tool-management SKILL.md covering consumer-side .NET tool workflows: global/local installation, .config/dotnet-tools.json manifest management, version pinning, CI restore (GitHub Actions and Azure DevOps), RID-specific consumer note with cross-ref to packaging skill, and agent gotchas.
## Evidence
- Commits: a922b7c, 1204e1a
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: