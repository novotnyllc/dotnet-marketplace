# fn-32-expanded-roslyn-and-code-analysis-skills.1 Add Roslyn multi-version targeting and CodeRefactoringProvider coverage

## Description
Extend skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md to add: (1) multi-Roslyn-version targeting (3.8, 4.2, 4.4, 4.6, 4.8, 4.14) with version-specific NuGet packaging paths and conditional compilation constants, and (2) CodeRefactoringProvider authoring (currently missing entirely).

**Size:** M
**Files:** skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

## Approach
- Multi-version targeting: Follow Meziantou.Analyzer pattern with $(RoslynVersion) property and analyzers/dotnet/roslyn{version}/cs/ NuGet packaging paths (version boundaries: 3.8, 4.2, 4.4, 4.6, 4.8, 4.14)
- Conditional compilation constants: ROSLYN_X_Y and ROSLYN_X_Y_OR_GREATER (e.g., #if ROSLYN_4_2_OR_GREATER)
- CodeRefactoringProvider: Register via [ExportCodeRefactoringProvider], implement ComputeRefactoringsAsync, create CodeAction instances
- DiagnosticSuppressor version gate: Note that DiagnosticSuppressor requires Roslyn 3.8+ in the multi-version targeting section
- Add sections after existing DiagnosticSuppressor section
- **Size management:** If skill exceeds ~750 lines after additions, extract extended code examples to a companion details.md file (following the pattern used by dotnet-csharp-code-smells)

## Key context
- Existing skill is 692 lines -- add sections, do not restructure
## Acceptance
- [ ] Multi-Roslyn-version targeting documented (3.8, 4.2, 4.4+ packaging paths and conditional compilation)
- [ ] DiagnosticSuppressor Roslyn 3.8+ version gate documented
- [ ] Skill size managed (details.md if >750 lines)
- [ ] CodeRefactoringProvider authoring covered
- [ ] Multi-version test matrix guidance
- [ ] No fn-N spec references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
