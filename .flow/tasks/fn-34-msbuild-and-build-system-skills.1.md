# fn-34-msbuild-and-build-system-skills.1 Create MSBuild authoring skill (targets, props, items, conditions)

## Description
Create `skills/build-system/dotnet-msbuild-authoring/SKILL.md` covering MSBuild project system authoring fundamentals: custom targets, props/targets files, import ordering, items and item metadata, conditions, property functions, well-known metadata, and Directory.Build.props/targets advanced patterns.

**Size:** M
**Files:** `skills/build-system/dotnet-msbuild-authoring/SKILL.md`
**Does NOT touch:** `.claude-plugin/plugin.json` (owned by task .3)

## Approach
- Custom targets: BeforeTargets/AfterTargets/DependsOnTargets, Inputs/Outputs for incrementality
- Props vs targets: import ordering (props before project evaluation, targets after)
- Items and metadata: Include/Exclude, Update, Remove, well-known metadata (%(Filename), %(Extension), %(RecursiveDir), etc.)
- Conditions: property/item condition syntax, TFM conditions (`'$(TargetFramework)' == 'net10.0'`), OS conditions
- Property functions: `$([System.String]::...)`, `$([MSBuild]::...)` intrinsic functions, `GetPathOfFileAbove`
- Directory.Build.props/targets advanced: import chain with `GetPathOfFileAbove`, condition guards, preventing double-imports
- Scope boundary: basic Directory.Build layout → cross-ref `[skill:dotnet-project-structure]`
- Each section uses explicit `##` headers
- Include Agent Gotchas section (MSBuild authoring pitfalls agents commonly make)
- Include References section with Microsoft Learn links

## Acceptance
- [ ] Custom targets with BeforeTargets/AfterTargets/DependsOnTargets
- [ ] Inputs/Outputs for incremental build targets
- [ ] Import ordering documented (props before, targets after)
- [ ] Items, metadata, conditions covered with examples
- [ ] Property functions documented with examples
- [ ] Directory.Build advanced patterns (import chain, condition guards, double-import prevention)
- [ ] Scope boundary: basic layout cross-refs `[skill:dotnet-project-structure]`
- [ ] Agent Gotchas section with MSBuild authoring pitfalls
- [ ] References section with Microsoft Learn links
- [ ] All cross-references use `[skill:name]` syntax
- [ ] SKILL.md frontmatter has `name` and `description` only
- [ ] Description under 120 characters

## Validation
```bash
# Verify skill file exists and has required frontmatter
grep -q '^name: dotnet-msbuild-authoring' skills/build-system/dotnet-msbuild-authoring/SKILL.md
grep -q '^description:' skills/build-system/dotnet-msbuild-authoring/SKILL.md

# Verify cross-references use [skill:] syntax
grep -c '\[skill:dotnet-project-structure\]' skills/build-system/dotnet-msbuild-authoring/SKILL.md

# Verify Agent Gotchas section exists
grep -q '## .*Gotcha' skills/build-system/dotnet-msbuild-authoring/SKILL.md

# Verify References section exists
grep -q '## References' skills/build-system/dotnet-msbuild-authoring/SKILL.md

# Run full validation
./scripts/validate-skills.sh
```

## Done summary
Created dotnet-msbuild-authoring skill covering MSBuild authoring fundamentals: custom targets (BeforeTargets/AfterTargets/DependsOnTargets), incremental builds (Inputs/Outputs), import ordering, items and metadata, conditions, property functions, and Directory.Build.props/targets advanced patterns (import chain, condition guards, double-import prevention). Includes 8 Agent Gotchas and References section.
## Evidence
- Commits: ee1b32a, c78ef3d
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: