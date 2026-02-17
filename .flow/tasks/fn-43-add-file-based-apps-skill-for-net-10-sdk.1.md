# fn-43-add-file-based-apps-skill-for-net-10-sdk.1 Author dotnet-file-based-apps SKILL.md

## Description
Author `skills/foundation/dotnet-file-based-apps/SKILL.md` covering .NET 10 SDK file-based apps (`dotnet run app.cs` without a project file).

**Visibility:** Implicit (agent-loaded, not user-invocable)
**Size:** M
**Files:** `skills/foundation/dotnet-file-based-apps/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/core-csharp/dotnet-file-io/SKILL.md` for structure
- Cover all four directive types: `#:package`, `#:sdk`, `#:property`, `#:project`
- Include migration path from file-based to project-based apps
- Note .NET 10+ SDK requirement
- Description must explicitly differentiate from `dotnet-file-io` — avoid "file I/O"
- Target description ~90 chars to stay within budget (132 skills projected)
- Reference: https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps

## Key context

- `#:` directives are SDK-level, not C# syntax — must appear before any C# code
- `dotnet build` and `dotnet test` do not apply in traditional sense for file-based apps
- `dotnet-file-io` (FileStream/RandomAccess) is a DIFFERENT skill — naming overlap risk, avoid confusion
## Approach

- Follow existing skill pattern at `skills/core-csharp/dotnet-file-io/SKILL.md` for structure
- Cover all four directive types: `#:package`, `#:sdk`, `#:property`, `#:project`
- Include migration path from file-based to project-based apps
- Note .NET 10+ SDK requirement
- Reference: https://learn.microsoft.com/en-us/dotnet/core/sdk/file-based-apps

## Key context

- `#:` directives are SDK-level, not C# syntax — must appear before any C# code
- `dotnet build` and `dotnet test` do not apply in traditional sense for file-based apps
- `dotnet-file-io` (FileStream/RandomAccess) is a DIFFERENT skill — naming overlap risk
## Acceptance
- [ ] SKILL.md exists at `skills/foundation/dotnet-file-based-apps/`
- [ ] Valid frontmatter with `name` and `description` (under 120 chars, ~90 target)
- [ ] Description explicitly differentiates from dotnet-file-io
- [ ] Covers `#:package`, `#:sdk`, `#:property`, `#:project` directives
- [ ] Covers migration from file-based to project-based
- [ ] Notes .NET 10+ SDK requirement
- [ ] Cross-reference syntax used for related skills
## Done summary
Authored dotnet-file-based-apps SKILL.md covering .NET 10 SDK file-based apps with all four #: directives (package, sdk, property, project), CLI commands, shell execution, launch profiles, user secrets, build caching, migration path, and 8 Agent Gotchas. Description at 90 chars explicitly differentiates from dotnet-file-io.
## Evidence
- Commits: b09fe9d, 0235153
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: