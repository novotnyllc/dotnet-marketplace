# fn-4-project-structure-and-scaffolding-skills.2 Analyzer and CI/CD integration skills

## Description
Create `dotnet-add-analyzers` and `dotnet-add-ci` skills in the project-structure skill category. The analyzer skill covers built-in Roslyn CA rules, nullable enforcement, trimming/AOT analyzers, third-party analyzer packages, and EditorConfig severity overrides. The CI skill detects GitHub Actions vs Azure DevOps and provides starter workflow templates for build/test/pack.

## Acceptance
- [x] `skills/project-structure/dotnet-add-analyzers/SKILL.md` exists with `name` and `description` frontmatter
- [x] `skills/project-structure/dotnet-add-ci/SKILL.md` exists with `name` and `description` frontmatter
- [x] `dotnet-add-analyzers` covers CA rules, nullable context, trimming warnings, AOT compatibility analyzers
- [x] `dotnet-add-ci` detects GitHub Actions vs Azure DevOps and provides starter workflows
- [x] `dotnet-add-ci` documents boundary with fn-19 (starter only, advanced patterns in fn-19)
- [x] Both skills cross-reference `[skill:dotnet-version-detection]`
- [x] Both skills registered in `plugin.json`
- [x] `./scripts/validate-skills.sh` passes with 0 errors

## Done summary
Created two skills: `dotnet-add-analyzers` (Roslyn CA rules, AnalysisLevel, EditorConfig severity, nullable, trimming/AOT analyzers, third-party packages like Meziantou and BannedApiAnalyzers) and `dotnet-add-ci` (platform detection, GitHub Actions and Azure DevOps starter workflows, NuGet pack steps, adaptation guidance). Both registered in plugin.json. Validation passes with 0 errors.

## Evidence
- Commits:
- Tests:
- PRs: