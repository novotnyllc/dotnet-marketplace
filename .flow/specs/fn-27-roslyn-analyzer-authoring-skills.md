# fn-27: Roslyn Analyzer Authoring Skills

## Overview
Delivers a skill for writing custom Roslyn analyzers, code fix providers, and diagnostic suppressors. This is an **authoring** skill teaching how to build Roslyn compiler extensions — distinct from fn-4's `dotnet-add-analyzers` (configuring/consuming existing analyzers) and fn-3's `dotnet-csharp-source-generators` (authoring source generators).

## Scope
**Skills (1 total):**
- `dotnet-roslyn-analyzers` — Writing custom DiagnosticAnalyzers, CodeFixProviders, and DiagnosticSuppressors: project setup (netstandard2.0), DiagnosticDescriptor conventions (IDs, categories, severity, helpLinkUri), analysis context registration, code fix actions, testing with Microsoft.CodeAnalysis.Testing, NuGet packaging under `analyzers/dotnet/cs/` layout, performance best practices

## Scope Boundaries

| Concern | fn-27 owns (authoring) | Other epic owns | Enforcement |
|---|---|---|---|
| Analyzer configuration | N/A — cross-references `[skill:dotnet-add-analyzers]` | fn-4: configuring CA rules, EditorConfig severity, third-party analyzers | Grep validates cross-ref presence |
| Source generators | N/A — cross-references `[skill:dotnet-csharp-source-generators]` | fn-3: IIncrementalGenerator, syntax/semantic analysis for generation | Grep validates cross-ref presence |
| NuGet packaging | Analyzer-specific NuGet layout (`analyzers/dotnet/cs/`, `IncludeBuildOutput=false`) | fn-20: general NuGet publishing | Cross-ref to fn-20 when it lands |
| Testing | Analyzer-specific testing (CSharpAnalyzerVerifier, CSharpCodeFixVerifier) | fn-7: general testing strategy and frameworks | Cross-ref to `[skill:dotnet-testing-strategy]` |
| Code smells | N/A | fn-26: which patterns to detect during review | Cross-ref to `[skill:dotnet-csharp-code-smells]` when it lands |
| DiagnosticDescriptor conventions | **Canonical owner** — ID naming (prefix conventions), categories, severity selection, helpLinkUri patterns | fn-3 source generators may emit diagnostics; should cross-ref fn-27 for conventions (aspirational — fn-3 is closed, add if reopened) | N/A |

## Key Context
- Analyzers MUST target `netstandard2.0` — the compiler loads analyzers on various runtimes (Mono, .NET Framework, .NET Core); targeting net8.0+ breaks VS/MSBuild compatibility
- Analyzers and source generators share the same NuGet packaging layout (`analyzers/dotnet/cs/`) and `Microsoft.CodeAnalysis.CSharp` dependency, but serve different purposes: analyzers report diagnostics, generators emit code
- `Microsoft.CodeAnalysis.Testing` provides high-level test infrastructure (`CSharpAnalyzerVerifier<T>`, `CSharpCodeFixVerifier<T,TFix>`) that is more ergonomic than raw `CSharpCompilation` testing
- Performance is critical: analyzers run in real-time during editing. Avoid allocations in `RegisterSyntaxNodeAction`, prefer `SymbolKind`-based filtering, use `ImmutableArray` for supported diagnostics
- DiagnosticSuppressor is an advanced feature for conditionally suppressing diagnostics from other analyzers (e.g., suppressing CA1062 when a custom null-check pattern is used)
- Multi-analyzer NuGet packages should separate analyzer and code fix assemblies for faster IDE load when fixes aren't needed
- Common Roslyn SDK meta-diagnostics (e.g., RS-series rules) flag issues in analyzer code itself — the skill should document these with verified ID-to-meaning mappings from official Roslyn SDK documentation

## Cross-Reference Matrix
| Skill | Required Outbound Refs |
|---|---|
| `dotnet-roslyn-analyzers` | `[skill:dotnet-csharp-source-generators]`, `[skill:dotnet-add-analyzers]`, `[skill:dotnet-testing-strategy]`, `[skill:dotnet-csharp-coding-standards]` |

## Quick Commands
```bash
# Validate skill exists with frontmatter
test -f "skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md" && echo "OK" || echo "MISSING"

# Validate frontmatter has required fields
grep -q "^name:" "skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md" && \
grep -q "^description:" "skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md" && \
echo "OK" || echo "MISSING FRONTMATTER"

# Verify netstandard2.0 targeting documented
grep -i "netstandard2.0" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

# Verify DiagnosticAnalyzer coverage
grep -i "DiagnosticAnalyzer" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

# Verify CodeFixProvider coverage
grep -i "CodeFixProvider" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

# Verify testing coverage
grep -i "CSharpAnalyzerVerifier\|CSharpCodeFixVerifier" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

# Verify cross-references per matrix
grep "skill:dotnet-csharp-source-generators" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md
grep "skill:dotnet-add-analyzers" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md
grep "skill:dotnet-testing-strategy" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md
grep "skill:dotnet-csharp-coding-standards" skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md

# Verify skill registered in plugin.json
grep "skills/core-csharp/dotnet-roslyn-analyzers" .claude-plugin/plugin.json

# Verify advisor catalog entry
grep "skill:dotnet-roslyn-analyzers" skills/foundation/dotnet-advisor/SKILL.md

# Run validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. Skill exists at `skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md` with `name` and `description` frontmatter
2. Covers DiagnosticAnalyzer authoring: project setup (netstandard2.0, Microsoft.CodeAnalysis.CSharp), analysis context registration (RegisterSyntaxNodeAction, RegisterSymbolAction, RegisterOperationAction), DiagnosticDescriptor conventions
3. Covers CodeFixProvider authoring: code fix registration, CodeAction creation, document/solution modification, equivalence key patterns
4. Covers DiagnosticSuppressor: when to use (suppress third-party diagnostics conditionally), SuppressionDescriptor, ReportSuppression
5. Covers testing with Microsoft.CodeAnalysis.Testing: CSharpAnalyzerVerifier, CSharpCodeFixVerifier, diagnostic location markup syntax (`[|...|]`, `{|ID:...|}`), multi-file test scenarios
6. Covers NuGet packaging: `analyzers/dotnet/cs/` layout, `IncludeBuildOutput=false`, separating analyzer and code fix assemblies, pack verification
7. Covers performance best practices: avoid allocations in hot paths, prefer symbol-based over syntax-based analysis where possible, incremental analysis patterns
8. Documents common Roslyn SDK meta-diagnostics with verified ID-to-meaning mappings from official documentation
9. Explicit scope boundary with `[skill:dotnet-csharp-source-generators]` (generators) and `[skill:dotnet-add-analyzers]` (consuming)
10. Cross-references validated per matrix using grep (including `[skill:dotnet-csharp-coding-standards]`)
11. Skill registered in `.claude-plugin/plugin.json` skills array
12. Skill added to `dotnet-advisor` catalog (category 2) and routing logic
13. `./scripts/validate-skills.sh` passes

## Test Notes
- Verify skill distinguishes analyzer authoring from source generator authoring
- Test that netstandard2.0 targeting is emphasized with explanation of why
- Validate testing section shows both analyzer-only and analyzer+codefix test patterns
- Confirm NuGet packaging section shows correct directory layout
- Verify performance section warns about RegisterSyntaxNodeAction allocation patterns
- Verify DiagnosticDescriptor conventions include ID prefix guidance, category naming, severity selection rationale
- Verify RS-series meta-diagnostic IDs are accurate against official Roslyn SDK documentation

## References
- Tutorial: Write your first analyzer and code fix: https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/tutorials/how-to-write-csharp-analyzer-code-fix
- Roslyn SDK: https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/
- Microsoft.CodeAnalysis.Testing: https://github.com/dotnet/roslyn-sdk/tree/main/src/Microsoft.CodeAnalysis.Testing
- Analyzer NuGet packaging: https://learn.microsoft.com/en-us/nuget/guides/analyzers-conventions
- dotnet/roslyn-analyzers: https://github.com/dotnet/roslyn-analyzers
- Meziantou.Analyzer (exemplar): https://github.com/meziantou/Meziantou.Analyzer
