# fn-43-add-file-based-apps-skill-for-net-10-sdk.2 Integrate dotnet-file-based-apps into plugin registry and routing

## Description
Register `dotnet-file-based-apps` in plugin.json, add routing entry in `dotnet-advisor`, and add cross-references to/from `dotnet-version-detection` and `dotnet-project-analysis`.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `skills/foundation/dotnet-advisor/SKILL.md`, `skills/foundation/dotnet-version-detection/SKILL.md`, `skills/foundation/dotnet-project-analysis/SKILL.md`, `scripts/validate-skills.sh`

## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry in `dotnet-advisor` (Routing Logic section)
- Add `[skill:dotnet-file-based-apps]` cross-references in version-detection and project-analysis
- Update `--projected-skills` in `scripts/validate-skills.sh` (increment by 1 for this skill)

## File contention warning

**plugin.json and dotnet-advisor SKILL.md are shared files** modified by all 5 integration tasks (fn-43.2 through fn-47.2). These tasks must NOT run in parallel — run them sequentially to avoid merge conflicts. The authoring tasks (.1) are fully parallel since they create new files in disjoint directories.
## Approach

- Add skill path to plugin.json `skills` array
- Add routing entry at `skills/foundation/dotnet-advisor/SKILL.md:176-304`
- Add `[skill:dotnet-file-based-apps]` cross-references in version-detection and project-analysis
- Update `--projected-skills` count in `scripts/validate-skills.sh`
## Acceptance
- [ ] plugin.json includes `skills/foundation/dotnet-file-based-apps`
- [ ] `dotnet-advisor` has routing entry for file-based apps
- [ ] Cross-references added in `dotnet-version-detection` and `dotnet-project-analysis`
- [ ] `--projected-skills` incremented in validate-skills.sh
- [ ] All four validation scripts pass
## Done summary
Integrated dotnet-file-based-apps into plugin registry: added to plugin.json skills array, added catalog entry and routing rule in dotnet-advisor, added cross-references in dotnet-version-detection and dotnet-project-analysis, incremented projected-skills to 123. Both validate-skills.sh and validate-marketplace.sh pass.
## Evidence
- Commits:
- Tests:
- PRs: