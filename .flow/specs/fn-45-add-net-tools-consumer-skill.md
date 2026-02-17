# fn-45 Add .NET Tools Consumer Skill

## Overview

Add a new `dotnet-tool-management` skill covering the consumer/user perspective of .NET tools: installing, managing, and configuring global tools, local tool manifests (`.config/dotnet-tools.json`), and CI restore workflows. Complements the existing producer-focused `dotnet-cli-packaging` skill.

**Visibility:** Implicit — auto-loaded by agents via advisor routing when tool management context is detected. Not user-invocable.

## Scope

**In:** SKILL.md for `dotnet-tool-management` under `skills/cli-tools/`, plugin.json registration, advisor routing, cross-references.

**Out:** Tool authoring/packaging (covered by `dotnet-cli-packaging`). Tool distribution pipeline (covered by `dotnet-cli-distribution`).

**Scope boundary with `dotnet-cli-packaging`**: Packaging covers `PackAsTool`, NuGet packaging, RID-specific tool manifests from the PRODUCER side. This skill covers `dotnet tool install`, `dotnet tool restore`, manifest management from the CONSUMER side.

## Key Context

- https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools
- `.config/dotnet-tools.json` manifest for reproducible tool versions in team/CI environments
- `dotnet tool restore` in CI pipelines — should run before build
- RID-specific tools: from consumer perspective, `dotnet tool install` handles RID selection automatically. Brief note only, cross-ref to `dotnet-cli-packaging` for authoring.
- Budget: target description ~90 chars. Total projected: 132 skills after batch.

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/cli-tools/dotnet-tool-management/SKILL.md` exists with valid frontmatter
- [ ] Covers global vs local tool installation
- [ ] Covers `.config/dotnet-tools.json` manifest creation and management
- [ ] Covers `dotnet tool restore` in CI scenarios
- [ ] RID-specific section is brief note (consumer perspective: "it just works"), cross-refs packaging skill
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-cli-packaging`, `dotnet-cli-distribution`
- [ ] Integration task notes file contention with plugin.json/advisor shared files
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools
- https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools
- https://learn.microsoft.com/en-us/dotnet/core/tools/local-tools
- `skills/cli-tools/dotnet-cli-packaging/SKILL.md` (producer perspective)
- `skills/cli-tools/dotnet-cli-distribution/SKILL.md` (distribution perspective)
