# fn-36-library-api-compatibility-skills.2 Create API surface validation skill (PublicApiAnalyzers, Verify, ApiCompat)

## Description
Create skills/api-development/dotnet-api-surface-validation/SKILL.md covering tools for validating public API surface area: PublicApiAnalyzers (primary new content), Verify API surface snapshot pattern, and ApiCompat CI enforcement workflow.

**Size:** M
**Files:** skills/api-development/dotnet-api-surface-validation/SKILL.md
**Depends on:** fn-36-library-api-compatibility-skills.1

## Approach
- PublicApiAnalyzers: PublicAPI.Shipped.txt/PublicAPI.Unshipped.txt, RS0016/RS0017, shipped/unshipped lifecycle, shipping workflow
- Verify for API surface snapshots: the specific pattern of reflecting over assembly types/members to detect unintended public API changes (cross-ref to [skill:dotnet-snapshot-testing] for Verify fundamentals — setup, scrubbing, converters)
- ApiCompat CI enforcement: how to gate PRs on API surface changes, CI pipeline integration (cross-ref to [skill:dotnet-multi-targeting] and [skill:dotnet-nuget-authoring] for EnablePackageValidation/ApiCompat tool mechanics)
- Cross-ref to [skill:dotnet-library-api-compat] for binary/source compat rules, [skill:dotnet-roslyn-analyzers] for general analyzer configuration
- Include Agent Gotchas, Prerequisites, and References sections

## Acceptance
- [ ] PublicApiAnalyzers workflow documented — `grep -c 'PublicAPI.Shipped\|PublicAPI.Unshipped\|RS0016\|RS0017' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] Verify API surface snapshot pattern — `grep -c 'GetTypes\|GetMembers\|Assembly.*Public' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] ApiCompat CI enforcement — `grep -c 'CI\|pipeline\|gate\|enforce' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] Cross-refs to related skills — `grep -c '\[skill:' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] Agent Gotchas section present — `grep -c 'Agent Gotcha' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] Prerequisites section present — `grep -c 'Prerequisite' skills/api-development/dotnet-api-surface-validation/SKILL.md`
- [ ] No fn-N references in body — `grep -c 'fn-[0-9]' skills/api-development/dotnet-api-surface-validation/SKILL.md` returns 0
- [ ] Description under 120 characters in frontmatter

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
