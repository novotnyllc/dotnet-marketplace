# fn-43 Add File-Based Apps Skill for .NET 10 SDK

## Overview

Add a new `dotnet-file-based-apps` skill covering the .NET 10 SDK feature that allows running C# files directly without a project file (`dotnet run app.cs`). Covers `#:package`, `#:sdk`, `#:property`, and `#:project` directives.

## Scope

**In:** SKILL.md for `dotnet-file-based-apps` under `skills/foundation/`, plugin.json registration, advisor routing, cross-references from `dotnet-version-detection` and `dotnet-project-analysis`.

**Out:** Modifying version detection logic itself (separate concern). File I/O (`dotnet-file-io` is a different skill).

**Scope boundary with `dotnet-project-analysis`**: Project analysis detects `.csproj`/`.sln`. File-based apps have NO project file — the `.cs` file IS the project. Add a cross-reference note, not full detection logic.

**Scope boundary with `dotnet-scaffold-project`**: Scaffold stays focused on csproj-based projects. File-based apps need no scaffolding (the whole point is no project file).

## Key Context

- .NET 10 SDK feature: https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps
- Directives: `#:package <name>[@version]`, `#:sdk <name>`, `#:property <name>=<value>`, `#:project <path>`
- No `.csproj` means `dotnet build`/`dotnet test` do not apply in the traditional sense
- Agent must recognize `#:` directives as SDK-level, not C# syntax

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/foundation/dotnet-file-based-apps/SKILL.md` exists with valid frontmatter
- [ ] Covers all four directive types with usage guidance
- [ ] Covers migration path from file-based to project-based
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated with file-based apps entry
- [ ] Cross-references added to/from `dotnet-version-detection` and `dotnet-project-analysis`
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps
- `skills/foundation/dotnet-version-detection/SKILL.md` (version gating: .NET 10+ only)
- `skills/foundation/dotnet-project-analysis/SKILL.md` (scope boundary)
- `skills/foundation/dotnet-advisor/SKILL.md:176-304` (routing table)
