# fn-4: Project Structure & Scaffolding Skills

## Overview
Delivers skills for modern .NET project structure, scaffolding, and modernization including solution layout, analyzers, CI/CD setup, and testing infrastructure.

## Scope
**Skills:**
- `dotnet-project-structure` - Modern solution layout: .slnx, Directory.Build.props, central package management, editorconfig, analyzers
- `dotnet-scaffolding-base` - Base project scaffolding with all best practices applied
- `dotnet-add-analyzers` - Add/configure .NET analyzers, Roslyn analyzers, nullable, trimming warnings, AOT compat analyzers
- `dotnet-add-ci` - Add CI/CD to existing project (composable, detects platform)
- `dotnet-add-testing` - Add test infrastructure to existing project
- `dotnet-modernize` - Analyze existing code for modernization opportunities, suggest upgrades

## Key Context
- .slnx is the modern solution format (XML-based, human-readable)
- Directory.Build.props and Directory.Packages.props for centralized configuration
- Central Package Management (CPM) is the recommended approach
- Code analyzers enforceable via EditorConfig: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- Library design guidance: https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/

## Quick Commands
```bash
# Smoke test: validate project structure skill
fd -e md dotnet-project-structure skills/

# Test scaffolding output
dotnet new console -o /tmp/test-scaffold && ls -la /tmp/test-scaffold

# Verify analyzer recommendations
grep -r "Microsoft.CodeAnalysis.NetAnalyzers" skills/project-structure/
```

## Acceptance Criteria
1. All 6 skills written with standard depth and frontmatter
2. Project structure skill documents .slnx, Directory.Build.props, CPM patterns
3. Scaffolding skill provides complete new-project template with all best practices
4. Add-analyzers skill covers CA rules, nullable context, trimming, AOT analyzers
5. Add-CI skill detects GitHub Actions vs Azure DevOps and provides platform-specific guidance
6. Modernize skill analyzes projects for upgrade opportunities (old TFMs, deprecated packages, outdated patterns)
7. Skills cross-reference dotnet-version-detection for TFM-aware guidance

## Test Notes
- Test scaffolding skill by generating a new project and validating structure
- Verify analyzer skill recommends appropriate analyzers for detected TFM
- Check modernize skill detects superseded patterns (e.g., Microsoft.Extensions.Http.Polly → Microsoft.Extensions.Http.Resilience)

## References
- .NET Library Design Guidance: https://learn.microsoft.com/en-us/dotnet/standard/library-guidance/
- Code Analysis Overview: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview
- Central Package Management: https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
- dotnet-skills project-structure reference: https://github.com/Aaronontheweb/dotnet-skills
