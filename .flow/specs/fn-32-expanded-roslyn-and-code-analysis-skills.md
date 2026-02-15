# Expanded Roslyn and Code Analysis Skills

## Overview
Extend the existing `dotnet-roslyn-analyzers` skill and add new skills to cover the full Roslyn authoring surface: multi-version targeting (Roslyn 3.8, 4.2, 4.4+), CodeRefactoringProvider, DiagnosticSuppressor patterns (noting DiagnosticSuppressor requires Roslyn 3.8+), and a dedicated EditorConfig skill covering .NET CA/IDE rules, severity configuration, and AnalysisLevel settings.

## Scope
- **Roslyn version targeting** — Extend `dotnet-roslyn-analyzers` to cover multi-TFM analyzer packaging (Meziantou.Analyzer pattern: `analyzers/dotnet/roslyn{version}/cs/` path structure with version boundaries 3.8, 4.2, 4.4, 4.6, 4.8, 4.14; `$(RoslynVersion)` property and `ROSLYN_X_Y` conditional compilation constants)
- **CodeRefactoringProvider** — New or extended coverage for code refactoring authoring (currently missing entirely)
- **EditorConfig skill** — Dedicated `dotnet-editorconfig` skill covering: .NET code style rules (IDE*), code quality rules (CA*), severity levels, AnalysisLevel, EnforceCodeStyleInBuild, global AnalyzerConfig
- **Analyzer testing** — Ensure coverage of CSharpAnalyzerVerifier, CSharpCodeFixVerifier for multi-Roslyn-version test matrices

**Testing default**: All test guidance uses xUnit v3 with Microsoft.Testing.Platform v2 (MTP2).

## Quick commands
```bash
./scripts/validate-skills.sh
python3 scripts/generate_dist.py --strict
```

## Acceptance
- [ ] Roslyn version targeting documented (3.8, 4.2, 4.4+ packaging paths and conditional compilation)
- [ ] CodeRefactoringProvider authoring covered
- [ ] Dedicated EditorConfig skill created with CA/IDE rules, severity, AnalysisLevel
- [ ] Multi-version analyzer test patterns included
- [ ] Testing examples use xUnit v3 + MTP2
- [ ] No fn-N spec references
- [ ] Budget constraint respected (< 15,000 chars total)
- [ ] All validation commands pass

## References
- `skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md` — existing analyzer skill (692 lines)
- Meziantou.Analyzer — multi-Roslyn-version packaging pattern
- Microsoft Roslyn SDK docs — CodeRefactoringProvider, DiagnosticSuppressor
