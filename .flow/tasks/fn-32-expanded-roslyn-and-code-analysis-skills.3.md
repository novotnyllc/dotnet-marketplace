# fn-32-expanded-roslyn-and-code-analysis-skills.3 Update analyzer testing patterns for xUnit v3 and MTP2

## Description
Update analyzer testing examples in dotnet-roslyn-analyzers to use xUnit v3 with Microsoft.Testing.Platform v2 (MTP2). Update CSharpAnalyzerVerifier/CSharpCodeFixVerifier patterns and package references.

**Size:** S
**Files:** skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

## Approach
- Update test examples from xUnit v2 to xUnit v3 patterns
- Use Microsoft.Testing.Platform v2 runner
- Update NuGet package references to latest stable versions
- Ensure multi-Roslyn-version test matrix works with xUnit v3
## Acceptance
- [ ] Test examples use xUnit v3 + MTP2
- [ ] Package references updated to latest stable
- [ ] Multi-version test matrix compatible
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
