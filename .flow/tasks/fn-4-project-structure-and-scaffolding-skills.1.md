# fn-4-project-structure-and-scaffolding-skills.1 Project structure and scaffolding base skills

## Description
Create the two base skills for fn-4: `dotnet-project-structure` (reference guide for modern .NET solution layout) and `dotnet-scaffold-project` (step-by-step scaffolding of new projects with all best practices).

## Acceptance
- [x] `skills/project-structure/dotnet-project-structure/SKILL.md` exists with `name` and `description` frontmatter
- [x] `skills/project-structure/dotnet-scaffold-project/SKILL.md` exists with `name` and `description` frontmatter
- [x] `dotnet-project-structure` covers .slnx (with .sln fallback), Directory.Build.props, Directory.Build.targets, CPM, .editorconfig
- [x] `dotnet-scaffold-project` provides complete new-project template with CPM, analyzers, editorconfig, SourceLink, deterministic builds, NuGet audit
- [x] Both skills cross-reference `[skill:dotnet-version-detection]`
- [x] Both skills registered in plugin.json
- [x] `./scripts/validate-skills.sh` passes

## Done summary
Created two project-structure base skills:

1. **dotnet-project-structure** — Reference guide for modern .NET solution layout covering .slnx (with .sln fallback), Directory.Build.props, Directory.Build.targets, Central Package Management, .editorconfig, global.json, nuget.config (with packageSourceMapping), NuGet audit, lock files, and SourceLink/deterministic builds.

2. **dotnet-scaffold-project** — Step-by-step guide for scaffolding a new .NET project from scratch with all best practices applied: CPM, analyzers, editorconfig, SourceLink, deterministic builds, NuGet audit, and lock files. Includes project template selection, cleanup of generated code, and verification steps.

Both skills cross-reference `[skill:dotnet-version-detection]` and are registered in plugin.json. Validation passes with 0 errors.
## Evidence
- Commits:
- Tests:
- PRs: