# fn-4: Project Structure & Scaffolding Skills

## Overview
Delivers skills for modern .NET project structure, scaffolding, and modernization. These are **setup-oriented** skills that help users bootstrap or improve a repo's foundational layout. Deep platform-specific CI/CD, testing, and version-migration guidance live in fn-19, fn-7, and fn-10 respectively.

## Scope
**Skills (6 total):**
- `dotnet-project-structure` — Modern solution layout: .slnx (with .sln fallback for older tooling/CI), Directory.Build.props, Directory.Build.targets, Directory.Packages.props (CPM), .editorconfig, analyzers
- `dotnet-scaffold-project` — Scaffold a new project with all best practices applied (structure, CPM, analyzers, editorconfig, SourceLink, deterministic builds)
- `dotnet-add-analyzers` — Add/configure .NET analyzers: Roslyn CA rules, nullable context, trimming warnings, AOT compat analyzers
- `dotnet-add-ci` — Add starter CI/CD to an existing project (detects GHA vs ADO, composable template); advanced patterns live in fn-19
- `dotnet-add-testing` — Add test infrastructure scaffolding to an existing project (xunit ref, test project, coverlet); deep testing patterns live in fn-7
- `dotnet-modernize` — Analyze existing code for modernization opportunities (outdated TFMs, deprecated packages, superseded patterns); version upgrade migration paths live in fn-10

**Naming convention:** All skills use `dotnet-` prefix. Verb-noun style for additive skills (`add-*`, `scaffold-*`, `modernize`); noun style for reference skills (`project-structure`).

## Scope Boundaries

| Concern | fn-4 owns (scaffolding) | Other epic owns (depth) |
|---|---|---|
| CI/CD | Starter workflow template, platform detection | fn-19: composable workflows, matrix builds, deploy pipelines |
| Testing | Test project scaffolding, package refs, coverlet config | fn-7: xUnit v3, strategies, integration, UI, snapshot, quality |
| Version upgrades | Detecting outdated TFMs/packages, flagging opportunities | fn-10: migration paths, polyfill strategies, multi-targeting |
| Version detection | Cross-references `[skill:dotnet-version-detection]` (foundation, fn-2) | fn-2: owns the skill; fn-10: version upgrade + multi-targeting |

## Key Context
- .slnx is the modern solution format (.NET 9+, XML-based, human-readable); .sln remains the fallback for older tooling and CI agents
- Directory.Build.props and Directory.Packages.props for centralized configuration
- Directory.Build.targets for build customization (imported after project)
- Central Package Management (CPM) is the recommended approach for multi-project repos
- NuGet audit is enabled by default in .NET 9+ (`NuGetAudit` property)
- Lock files (`RestorePackagesWithLockFile`) for deterministic restores
- SourceLink and deterministic builds should be default for libraries
- Code analyzers enforceable via EditorConfig: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- Library design guidance: https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/

## Task Decomposition

### fn-4.1: Project structure and scaffolding base skills
**Delivers:** `dotnet-project-structure`, `dotnet-scaffold-project`
- `skills/project-structure/dotnet-project-structure/SKILL.md`
- `skills/project-structure/dotnet-scaffold-project/SKILL.md`
- Both require `name` and `description` frontmatter
- `dotnet-project-structure` must cross-reference `[skill:dotnet-version-detection]`

### fn-4.2: Analyzer and CI/CD integration skills
**Delivers:** `dotnet-add-analyzers`, `dotnet-add-ci`
- `skills/project-structure/dotnet-add-analyzers/SKILL.md`
- `skills/project-structure/dotnet-add-ci/SKILL.md`
- `dotnet-add-ci` must document boundary with fn-19 (starter only)
- `dotnet-add-analyzers` must cover CA rules, nullable, trimming, AOT analyzers

### fn-4.3: Testing infrastructure and modernization skills
**Delivers:** `dotnet-add-testing`, `dotnet-modernize`
- `skills/project-structure/dotnet-add-testing/SKILL.md`
- `skills/project-structure/dotnet-modernize/SKILL.md`
- `dotnet-add-testing` must document boundary with fn-7 (scaffolding only)
- `dotnet-modernize` must document boundary with fn-10 (flagging only, not migration paths)

## Quick Commands
```bash
# Validate all 6 skills exist with frontmatter
for s in dotnet-project-structure dotnet-scaffold-project dotnet-add-analyzers dotnet-add-ci dotnet-add-testing dotnet-modernize; do
  test -f "skills/project-structure/$s/SKILL.md" && echo "OK: $s" || echo "MISSING: $s"
done

# Validate frontmatter has required fields
grep -l "^name:" skills/project-structure/*/SKILL.md | wc -l  # expect 6

# Verify cross-references
grep -r "\[skill:dotnet-version-detection\]" skills/project-structure/
```

## Acceptance Criteria
1. All 6 skills exist at `skills/project-structure/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-project-structure` documents .slnx (with .sln fallback), Directory.Build.props, Directory.Build.targets, CPM, .editorconfig
3. `dotnet-scaffold-project` provides complete new-project template with CPM, analyzers, editorconfig, SourceLink, deterministic builds, NuGet audit
4. `dotnet-add-analyzers` covers CA rules, nullable context, trimming warnings, AOT compatibility analyzers
5. `dotnet-add-ci` detects GitHub Actions vs Azure DevOps and provides starter workflow; documents that advanced patterns live in fn-19
6. `dotnet-add-testing` scaffolds test project with xUnit ref, coverlet, directory structure; documents that deep patterns live in fn-7
7. `dotnet-modernize` flags outdated TFMs, deprecated packages, superseded patterns; documents that migration paths live in fn-10
8. Skills cross-reference `[skill:dotnet-version-detection]` for TFM-aware guidance
9. All skills registered in `plugin.json`
10. `./scripts/validate-skills.sh` passes for all 6 skills

## Test Notes
- Test scaffolding skill by generating a new project and validating structure matches documented layout
- Verify analyzer skill recommends appropriate analyzers for detected TFM
- Check modernize skill detects superseded patterns (e.g., `Microsoft.Extensions.Http.Polly` → `Microsoft.Extensions.Http.Resilience`)
- Verify `dotnet-add-ci` produces valid GHA YAML and ADO YAML starter templates
- Confirm boundary cross-references are present in `dotnet-add-ci`, `dotnet-add-testing`, `dotnet-modernize`

## References
- .NET Library Design Guidance: https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/
- Code Analysis Overview: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- Central Package Management: https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
- .slnx Format: https://learn.microsoft.com/en-us/visualstudio/ide/reference/solution-file?view=vs-2022
- dotnet-skills project-structure reference: https://github.com/Aaronontheweb/dotnet-skills
