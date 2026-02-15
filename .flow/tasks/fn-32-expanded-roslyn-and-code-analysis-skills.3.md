# fn-32-expanded-roslyn-and-code-analysis-skills.3 Update analyzer testing patterns for xUnit v3 and MTP2

## Description
Update analyzer testing examples in dotnet-roslyn-analyzers to use xUnit v3 with Microsoft.Testing.Platform v2 (MTP2). Update CSharpAnalyzerVerifier/CSharpCodeFixVerifier/CSharpCodeRefactoringVerifier patterns and package references.
<!-- Updated by plan-sync: fn-32.1 added CSharpCodeRefactoringVerifier<T> patterns in details.md -->

**Size:** S
**Files:** skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md, skills/core-csharp/dotnet-roslyn-analyzers/details.md

## Approach
- Update test examples from xUnit v2 to xUnit v3 patterns in both SKILL.md and details.md
- Use Microsoft.Testing.Platform v2 runner
- Update NuGet package references to latest stable versions
- Update CSharpCodeRefactoringVerifier<T> test examples in details.md (added by fn-32.1) alongside CSharpAnalyzerVerifier and CSharpCodeFixVerifier
- Ensure multi-Roslyn-version test matrix works with xUnit v3
## Acceptance
- [ ] Test examples use xUnit v3 + MTP2 in SKILL.md
- [ ] Test examples use xUnit v3 + MTP2 in details.md (CSharpCodeRefactoringVerifier<T> tests)
- [ ] Package references updated to latest stable
- [ ] Multi-version test matrix compatible
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
