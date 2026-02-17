# fn-45 Add .NET Tools Consumer Skill

## Overview

Add a new `dotnet-tool-management` skill covering the consumer/user perspective of .NET tools: installing, managing, and configuring global tools, local tool manifests (`.config/dotnet-tools.json`), RID-specific tools, and AOT-published tool binaries. Complements the existing producer-focused `dotnet-cli-packaging` skill.

## Scope

**In:** SKILL.md for `dotnet-tool-management` under `skills/cli-tools/`, plugin.json registration, advisor routing, cross-references.

**Out:** Tool authoring/packaging (covered by `dotnet-cli-packaging`). Tool distribution pipeline (covered by `dotnet-cli-distribution`).

**Scope boundary with `dotnet-cli-packaging`**: Packaging skill covers `PackAsTool`, NuGet packaging, RID-specific tool manifests from the PRODUCER side. This skill covers `dotnet tool install`, `dotnet tool restore`, manifest management from the CONSUMER side.

**Scope boundary with `dotnet-cli-distribution`**: Distribution covers publishing native binaries. This skill covers consuming pre-built tools regardless of how they were distributed.

## Key Context

- RID-specific tools: https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools
- `dotnet-tools.json` manifest for reproducible tool versions in team/CI environments
- `dotnet tool restore` in CI pipelines — should run before build
- AOT-published tools distributed as native binaries (not via `dotnet tool install`)
- Tool manifest does not support RID constraints — RID-specific tools use `ToolPackageRuntimeIdentifiers` on the packaging side

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/cli-tools/dotnet-tool-management/SKILL.md` exists with valid frontmatter
- [ ] Covers global vs local tool installation
- [ ] Covers `.config/dotnet-tools.json` manifest creation and management
- [ ] Covers `dotnet tool restore` in CI scenarios
- [ ] Covers RID-specific tool consumption
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-cli-packaging`, `dotnet-cli-distribution`
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/core/tools/rid-specific-tools
- https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools
- https://learn.microsoft.com/en-us/dotnet/core/tools/local-tools
- `skills/cli-tools/dotnet-cli-packaging/SKILL.md:381-451` (producer perspective)
- `skills/cli-tools/dotnet-cli-distribution/SKILL.md` (distribution perspective)
- `skills/foundation/dotnet-project-analysis/SKILL.md:244-251` (tool manifest detection)
