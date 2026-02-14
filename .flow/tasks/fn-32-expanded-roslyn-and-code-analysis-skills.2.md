# fn-32-expanded-roslyn-and-code-analysis-skills.2 Create dedicated EditorConfig skill

## Description
Create skills/core-csharp/dotnet-editorconfig/SKILL.md as a dedicated EditorConfig skill covering .NET code style rules (IDE*), code quality rules (CA*), severity configuration, AnalysisLevel, EnforceCodeStyleInBuild, and global AnalyzerConfig files.

**Size:** M
**Files:** skills/core-csharp/dotnet-editorconfig/SKILL.md, .claude-plugin/plugin.json

## Approach
- .editorconfig structure and precedence (directory hierarchy)
- .NET code style rules: IDE0001-IDE0090+ (naming, formatting, expression-level preferences)
- Code quality rules: CA1000+ (design, globalization, performance, reliability)
- Severity levels: none, silent, suggestion, warning, error
- AnalysisLevel property (latest, preview, 5.0, 6.0, etc.)
- EnforceCodeStyleInBuild for CI enforcement
- Global AnalyzerConfig files (.globalconfig)
- Cross-ref to [skill:dotnet-roslyn-analyzers] and [skill:dotnet-project-structure]
## Acceptance
- [ ] IDE* and CA* rule categories documented
- [ ] Severity and AnalysisLevel covered
- [ ] Global AnalyzerConfig documented
- [ ] Cross-refs to related skills
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
