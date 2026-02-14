# fn-36-library-api-compatibility-skills.2 Create API surface validation skill (PublicApiAnalyzers, Verify, ApiCompat)

## Description
Create skills/api/dotnet-api-surface-validation/SKILL.md covering tools for validating public API surface area: PublicApiAnalyzers, Verify snapshot testing, and ApiCompat tool.

**Size:** M
**Files:** skills/api/dotnet-api-surface-validation/SKILL.md, .claude-plugin/plugin.json

## Approach
- PublicApiAnalyzers: PublicAPI.Shipped.txt/PublicAPI.Unshipped.txt, RS0016/RS0017, shipped/unshipped lifecycle
- Verify for API surface snapshots: detect unintended public API changes
- ApiCompat tool (Microsoft.DotNet.ApiCompat): comparing assemblies for breaking changes
- CI integration: enforcing API surface checks in build/PR pipeline
- Cross-ref to [skill:dotnet-library-api-compat], [skill:dotnet-snapshot-testing], [skill:dotnet-roslyn-analyzers]
## Acceptance
- [ ] PublicApiAnalyzers workflow documented
- [ ] Verify for API surface snapshots
- [ ] ApiCompat tool usage
- [ ] CI integration patterns
- [ ] Cross-refs correct
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
