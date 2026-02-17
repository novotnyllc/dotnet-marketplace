# fn-43-add-file-based-apps-skill-for-net-10-sdk.2 Integrate dotnet-file-based-apps into plugin registry and routing

## Description
Register `dotnet-file-based-apps` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references to/from `dotnet-version-detection` and `dotnet-project-analysis`.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/foundation/dotnet-version-detection/SKILL.md`, `skills/foundation/dotnet-project-analysis/SKILL.md`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry at `skills/foundation/dotnet-advisor/SKILL.md:176-304`
- Add `[skill:dotnet-file-based-apps]` cross-references in version-detection and project-analysis
- Update `--projected-skills` count in `scripts/validate-skills.sh`
## Acceptance
- [ ] plugin.json includes `skills/foundation/dotnet-file-based-apps`
- [ ] `dotnet-advisor` has routing entry for file-based apps
- [ ] Cross-references added in `dotnet-version-detection` and `dotnet-project-analysis`
- [ ] All four validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
