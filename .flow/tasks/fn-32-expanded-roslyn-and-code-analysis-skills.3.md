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
Updated analyzer testing patterns from xUnit v2 to xUnit v3 (3.2.2) with Microsoft.Testing.Platform v2 (MTP2) runner in both SKILL.md and details.md. Updated Roslyn testing packages to 1.1.3 (framework-agnostic with DefaultVerifier), Microsoft.CodeAnalysis.Analyzers to 3.11.0, and CI matrix to .NET 10 SDK.
## Evidence
- Commits: 6e90efa1afd49ad783214ac5192a806c1d1671b2
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: