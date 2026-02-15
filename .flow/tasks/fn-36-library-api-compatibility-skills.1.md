# fn-36-library-api-compatibility-skills.1 Create library API compatibility skill (binary/source compat, type forwarders)

## Description
Create skills/api-development/dotnet-library-api-compat/SKILL.md covering binary and source compatibility rules for .NET library authors, type forwarders, and how versioning decisions affect compatibility.

**Size:** M
**Files:** skills/api-development/dotnet-library-api-compat/SKILL.md

## Approach
- Binary compatibility: field layout, virtual dispatch, default interface members, new overloads, sealed→unsealed transitions
- Source compatibility: overload resolution, extension method conflicts, namespace additions, optional parameter changes
- Type forwarders: [TypeForwardedTo]/[TypeForwardedFrom] for migrating types between assemblies without breaking consumers
- SemVer impact summary: which changes are major/minor/patch (brief — cross-ref to [skill:dotnet-nuget-authoring] for full SemVer rules)
- Multi-TFM binary compat: how adding/removing TFMs affects compatibility (cross-ref to [skill:dotnet-multi-targeting] for packaging mechanics)
- Cross-ref to [skill:dotnet-api-versioning] and [skill:dotnet-nuget-authoring]
- Include Agent Gotchas, Prerequisites, and References sections

## Acceptance
- [ ] Binary compatibility rules with examples — `grep -c 'binary compatibility\|Binary Compatibility\|field layout\|virtual dispatch' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] Source compatibility rules with examples — `grep -c 'source compatibility\|Source Compatibility\|overload resolution' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] Type forwarder patterns documented — `grep -c 'TypeForwardedTo\|TypeForwardedFrom' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] SemVer impact summary with cross-ref — `grep -c '\[skill:dotnet-nuget-authoring\]' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] Agent Gotchas section present — `grep -c 'Agent Gotcha' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] Prerequisites section present — `grep -c 'Prerequisite' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] Cross-refs use [skill:name] syntax — `grep -c '\[skill:' skills/api-development/dotnet-library-api-compat/SKILL.md`
- [ ] No fn-N references in body — `grep -c 'fn-[0-9]' skills/api-development/dotnet-library-api-compat/SKILL.md` returns 0
- [ ] Description under 120 characters in frontmatter

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
