# fn-32-expanded-roslyn-and-code-analysis-skills.1 Add Roslyn multi-version targeting and CodeRefactoringProvider coverage

## Description
Extend skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md to add: (1) multi-Roslyn-version targeting (3.7, 3.8, 4.x) with version-specific packaging paths, and (2) CodeRefactoringProvider authoring (currently missing entirely).

**Size:** M
**Files:** skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

## Approach
- Multi-version targeting: Follow Meziantou.Analyzer pattern with $(RoslynVersion) property and analyzers/dotnet/roslyn3.8/cs/ NuGet packaging paths
- CodeRefactoringProvider: Register via [ExportCodeRefactoringProvider], implement ComputeRefactoringsAsync, create CodeAction instances
- Version-specific conditional compilation: #if ROSLYN3_8 patterns
- Add section after existing DiagnosticAnalyzer/CodeFixProvider sections

## Key context
- Existing skill is 692 lines -- add sections, do not restructure
## Acceptance
- [ ] Multi-Roslyn-version targeting documented (3.7, 3.8, 4.x packaging paths)
- [ ] CodeRefactoringProvider authoring covered
- [ ] Multi-version test matrix guidance
- [ ] No fn-N spec references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
