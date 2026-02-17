# fn-46 Add Artifact Output Layout Skill

## Overview

Add a new `dotnet-artifacts-output` skill covering the .NET SDK artifacts output layout (`UseArtifactsOutput`). Present as a recommended option for new projects with clear tradeoffs (path changes affect CI, Docker, tooling).

**Visibility:** Implicit — auto-loaded by agents via advisor routing when build output layout or UseArtifactsOutput context is detected. Not user-invocable.

## Scope

**In:** SKILL.md for `dotnet-artifacts-output` under `skills/project-structure/`, plugin.json registration, advisor routing, cross-references to affected skills (containers, CI, project structure).

**Out:** Modifying existing skills to change their `bin/` path references (tracked separately if/when artifacts output becomes the SDK default).

**Scope boundary with `dotnet-project-structure`**: Project structure covers source organization (`.sln`, `.csproj`, `src/`, `tests/`). Artifacts output covers BUILD output organization (`artifacts/bin/`, `artifacts/obj/`, `artifacts/publish/`). Source tree vs output tree.

## Key Context

- https://learn.microsoft.com/en-us/dotnet/core/sdk/artifacts-output
- Available since .NET 8, opt-in via `<UseArtifactsOutput>true</UseArtifactsOutput>` in `Directory.Build.props`
- Changes output paths: `bin/Debug/net10.0/` → `artifacts/bin/MyProject/debug/`
- Affects: `.gitignore`, Dockerfiles (`COPY --from=build`), CI artifact upload paths
- `ArtifactsPath` property allows customizing the root artifacts directory
- NOT the .NET 10 default (remains opt-in) — present as recommended option with tradeoffs
- Budget: target description ~90 chars. Total projected: 132 skills after batch.

## Quick commands

```bash
./scripts/validate-skills.sh
```

## Acceptance

- [ ] `skills/project-structure/dotnet-artifacts-output/SKILL.md` exists with valid frontmatter
- [ ] Covers enabling UseArtifactsOutput in Directory.Build.props
- [ ] Covers new path structure (bin, obj, publish, package subdirectories)
- [ ] Covers impact on Dockerfiles, CI pipelines, .gitignore
- [ ] Covers ArtifactsPath customization
- [ ] Presents as recommended option with tradeoffs, not universal default
- [ ] Description under 120 characters
- [ ] Registered in plugin.json
- [ ] `dotnet-advisor` routing updated
- [ ] Cross-references to/from `dotnet-project-structure`, `dotnet-containers`, `dotnet-gha-build-test`
- [ ] Integration task notes file contention with plugin.json/advisor shared files
- [ ] All validation scripts pass

## References

- https://learn.microsoft.com/en-us/dotnet/core/sdk/artifacts-output
- `skills/project-structure/dotnet-project-structure/SKILL.md` (scope boundary)
- `skills/architecture/dotnet-containers/SKILL.md` (Dockerfile path impact)
- `skills/ci-cd/dotnet-gha-build-test/SKILL.md` (CI artifact paths)
