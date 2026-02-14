# fn-36-library-api-compatibility-skills.1 Create library API compatibility skill (binary/source compat, type forwarders)

## Description
Create skills/api/dotnet-library-api-compat/SKILL.md covering binary and source compatibility rules for .NET library authors, type forwarders, and versioning strategy for NuGet packages.

**Size:** M
**Files:** skills/api/dotnet-library-api-compat/SKILL.md, .claude-plugin/plugin.json

## Approach
- Binary compatibility: field layout, virtual dispatch, default interface members, new overloads
- Source compatibility: overload resolution, extension method conflicts, namespace additions
- Type forwarders: [TypeForwardedTo]/[TypeForwardedFrom] for migrating types between assemblies
- SemVer for NuGet: major (breaking), minor (additive), patch (bug fix)
- Multi-TFM packaging: targeting multiple frameworks, TFM-specific APIs
- Cross-ref to [skill:dotnet-api-versioning] and [skill:dotnet-csharp-api-design]
## Acceptance
- [ ] Binary compatibility rules with examples
- [ ] Source compatibility rules with examples
- [ ] Type forwarder patterns documented
- [ ] SemVer for NuGet guidance
- [ ] Cross-refs correct
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
