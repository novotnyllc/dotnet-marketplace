# fn-27-roslyn-analyzer-authoring-skills.1 Create dotnet-roslyn-analyzers skill

## Description
Create the `dotnet-roslyn-analyzers` skill covering custom Roslyn analyzer authoring: DiagnosticAnalyzer, CodeFixProvider, DiagnosticSuppressor, testing, and NuGet packaging.

**Size:** M
**Files:**
- `skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md` (new)

## Approach
- Follow existing skill patterns at `skills/core-csharp/dotnet-csharp-source-generators/SKILL.md` for structure and frontmatter conventions
- Use `[skill:...]` cross-reference syntax per fn-2 conventions
- Reference `skills/project-structure/dotnet-add-analyzers/SKILL.md` for scope boundary (that skill covers *consuming*; this covers *authoring*)
- Reference `skills/core-csharp/dotnet-csharp-source-generators/SKILL.md` lines 466-491 for shared Roslyn packaging concepts (cross-ref, don't duplicate)

## Key context
- Skill MUST be comprehensive: DiagnosticAnalyzer (syntax/symbol/operation analysis), CodeFixProvider (code actions, document editing), DiagnosticSuppressor (conditional suppression)
- DiagnosticDescriptor conventions: fn-27 is canonical owner — ID prefix patterns (e.g., `MYLIB001`), category naming, severity selection rationale, helpLinkUri patterns
- Testing: use Microsoft.CodeAnalysis.Testing high-level API (`CSharpAnalyzerVerifier<T>`, `CSharpCodeFixVerifier<T,TFix>`) as primary, not raw CSharpCompilation
- Performance: critical section — analyzers run in real-time. Document allocation-free patterns for RegisterSyntaxNodeAction callbacks
- NuGet packaging: `analyzers/dotnet/cs/` layout, `IncludeBuildOutput=false`, separate analyzer and code fix assemblies
- Meta-diagnostics: RS1001 (missing DiagnosticAnalyzer attribute), RS1004 (recommended API), RS1025 (concurrent dictionary)
- Always target netstandard2.0 — explain WHY (compiler runtime compatibility across VS, MSBuild, CLI)
- Pitfall from memory: source generator hint names must include namespace to avoid collisions (analogous for analyzer diagnostic IDs)
- Pitfall from memory: skill code examples must list third-party NuGet packages explicitly
## Acceptance
- [ ] Skill file exists at `skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md`
- [ ] Frontmatter has `name: dotnet-roslyn-analyzers` and `description` (under 120 chars)
- [ ] Covers DiagnosticAnalyzer: project setup (netstandard2.0), RegisterSyntaxNodeAction, RegisterSymbolAction, RegisterOperationAction, DiagnosticDescriptor
- [ ] Covers CodeFixProvider: RegisterCodeFixesAsync, CodeAction creation, document/solution modification, equivalence keys
- [ ] Covers DiagnosticSuppressor: SuppressionDescriptor, ReportSuppression, when to use vs. EditorConfig
- [ ] Covers DiagnosticDescriptor conventions: ID prefix patterns, categories, severity selection, helpLinkUri
- [ ] Covers testing: CSharpAnalyzerVerifier, CSharpCodeFixVerifier, diagnostic markup syntax, multi-file scenarios
- [ ] Covers NuGet packaging: analyzers/dotnet/cs/ layout, IncludeBuildOutput=false, separate assemblies
- [ ] Covers performance: allocation-free callbacks, symbol-based filtering, ImmutableArray for SupportedDiagnostics
- [ ] Documents RS1001, RS1004, RS1025 meta-diagnostics
- [ ] Cross-references `[skill:dotnet-csharp-source-generators]`, `[skill:dotnet-add-analyzers]`, `[skill:dotnet-testing-strategy]`, `[skill:dotnet-csharp-coding-standards]`
- [ ] Explicit scope boundary statement: authoring vs. consuming vs. source generators
- [ ] Does NOT touch plugin.json (handled by fn-27.2)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
