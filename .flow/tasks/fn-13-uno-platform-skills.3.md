# fn-13-uno-platform-skills.3 Add reverse cross-refs and validate integrations

## Description
Add cross-reference integrations between the new Uno skills and existing skills. Update `dotnet-uno-testing` with reverse cross-refs to the new Uno skills. Validate all hard cross-references resolve. Ensure no duplicate skill IDs in advisor catalog.

### Deliverables
- Updated `skills/testing/dotnet-uno-testing/SKILL.md` with reverse cross-refs: `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`
- Validation that all hard cross-references resolve (grep check)
- Validation that no duplicate skill IDs exist in `dotnet-advisor` catalog
- Soft cross-refs (`dotnet-aot-wasm`, `dotnet-ui-chooser`) validated only if target files exist

### Files modified
- `skills/testing/dotnet-uno-testing/SKILL.md` (add reverse cross-refs)

### Files validated (read-only)
- `.claude-plugin/plugin.json` (verify registrations from fn-13.1 and fn-13.2)
- `skills/foundation/dotnet-advisor/SKILL.md` (verify catalog entries, no duplicates)

## Acceptance
- [ ] `dotnet-uno-testing` SKILL.md contains `[skill:dotnet-uno-platform]` and `[skill:dotnet-uno-targets]` cross-refs
- [ ] All hard cross-references from fn-13.1 and fn-13.2 resolve (grep finds target files)
- [ ] Soft cross-refs (`dotnet-aot-wasm`, `dotnet-ui-chooser`) are present in skill files but not validated for resolution
- [ ] No duplicate skill IDs in `dotnet-advisor` catalog (`grep | sort | uniq -d` returns empty)
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
