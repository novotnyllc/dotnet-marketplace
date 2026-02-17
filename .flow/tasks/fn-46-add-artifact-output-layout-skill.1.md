# fn-46-add-artifact-output-layout-skill.1 Author dotnet-artifacts-output SKILL.md

## Description
Author `skills/project-structure/dotnet-artifacts-output/SKILL.md` covering the .NET SDK artifacts output layout (`UseArtifactsOutput`). Recommend as default for new projects.

**Size:** M
**Files:** `skills/project-structure/dotnet-artifacts-output/SKILL.md`

## Approach

- Follow existing skill pattern at `skills/project-structure/dotnet-project-structure/SKILL.md`
- Cover enabling via `<UseArtifactsOutput>true</UseArtifactsOutput>` in `Directory.Build.props`
- Cover new path structure: `artifacts/bin/`, `artifacts/obj/`, `artifacts/publish/`, `artifacts/package/`
- Cover impact: `.gitignore`, Dockerfiles, CI artifact upload paths
- Cover `ArtifactsPath` customization
- Reference: https://learn.microsoft.com/en-us/dotnet/core/sdk/artifacts-output

## Key context

- Available since .NET 8, opt-in (not default)
- Output paths change: `bin/Debug/net10.0/` → `artifacts/bin/MyProject/debug/`
- Skills referencing `bin/` paths (containers, CI) are NOT updated in this task — cross-references only
- Scope boundary: `dotnet-project-structure` = source tree organization; this skill = build output organization
## Acceptance
- [ ] SKILL.md exists at `skills/project-structure/dotnet-artifacts-output/`
- [ ] Valid frontmatter with `name` and `description` (under 120 chars)
- [ ] Covers enabling UseArtifactsOutput in Directory.Build.props
- [ ] Covers new path structure with all subdirectories
- [ ] Covers impact on Dockerfiles, CI, .gitignore
- [ ] Covers ArtifactsPath customization
- [ ] Cross-reference syntax used for related skills
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
