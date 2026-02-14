# fn-34-msbuild-and-build-system-skills.1 Create MSBuild authoring skill (targets, props, items, conditions)

## Description
Create skills/build-system/dotnet-msbuild-authoring/SKILL.md covering MSBuild project system authoring fundamentals: custom targets, props/targets files, import ordering, items and item metadata, conditions, property functions, well-known metadata, and Directory.Build.props/targets patterns.

**Size:** M
**Files:** skills/build-system/dotnet-msbuild-authoring/SKILL.md, .claude-plugin/plugin.json

## Approach
- Target authoring: BeforeTargets/AfterTargets/DependsOnTargets, Inputs/Outputs for incrementality
- Props vs targets: import ordering (props before project, targets after)
- Items and metadata: Include/Exclude, Update, Remove, well-known metadata
- Conditions: property/item condition syntax, TFM conditions, OS conditions
- Property functions: string manipulation, MSBuild intrinsic functions
- Directory.Build.props/targets: import chain, condition guards, preventing double-imports
- Cross-ref to [skill:dotnet-project-structure]
## Acceptance
- [ ] Custom targets with BeforeTargets/AfterTargets/DependsOnTargets
- [ ] Import ordering documented
- [ ] Items, metadata, conditions covered
- [ ] Property functions documented
- [ ] Directory.Build patterns
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
