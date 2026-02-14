# fn-20-packaging-and-publishing-skills.3 Integration — plugin registration, advisor catalog, validation, cross-reference reconciliation

## Description
Register all 4 fn-20 skills in `plugin.json`, update the advisor catalog, reconcile cross-references, and run validation. This task depends on fn-20.1 and fn-20.2 completing first. Single owner of `plugin.json` changes — eliminates merge conflicts.

**Plugin registration:**
- Add 4 skill paths to `.claude-plugin/plugin.json` `skills` array:
  - `skills/packaging/dotnet-nuget-authoring`
  - `skills/packaging/dotnet-msix`
  - `skills/packaging/dotnet-github-releases`
  - `skills/release-management/dotnet-release-management`

**Advisor catalog updates in `skills/foundation/dotnet-advisor/SKILL.md`:**
- Section 15 ("Packaging & Publishing"): change `planned` to `implemented`
- Section 16 ("Release Management"): change `planned` to `implemented`
- Update `[skill:dotnet-nuget-modern]` reference to `[skill:dotnet-nuget-authoring]` (name change from original plan)
- Add `[skill:dotnet-github-releases]` routing entry under "Packaging & Releases" section
- Verify all skill names in advisor match their SKILL.md `name` frontmatter values exactly

**Cross-reference reconciliation:**
- Search for `<!-- TODO(fn-20) -->` placeholders in all skills — resolve with canonical cross-refs
- Search for bare "fn-20" mentions in other skills — update to canonical `[skill:dotnet-*]` cross-refs where appropriate
- fn-27 (Roslyn Analyzer Authoring) spec mentions "cross-ref to fn-20 when it lands" for NuGet layout — verify if fn-27 skills exist yet and add cross-ref if so

**Validation:**
- Run repo-wide skill name uniqueness check
- Run `./scripts/validate-skills.sh`
- Validate cross-references present in all 4 skills
- Verify advisor section updates

**Files modified:**
- `.claude-plugin/plugin.json`
- `skills/foundation/dotnet-advisor/SKILL.md`
- Any skills with `<!-- TODO(fn-20) -->` placeholders (if any)

## Acceptance
- [ ] All 4 skill paths registered in `plugin.json` `skills` array
- [ ] Advisor section 15 updated from `planned` to `implemented`
- [ ] Advisor section 16 updated from `planned` to `implemented`
- [ ] Advisor `[skill:dotnet-nuget-modern]` reference updated to `[skill:dotnet-nuget-authoring]`
- [ ] Advisor skill names match SKILL.md `name` frontmatter values exactly
- [ ] `grep -r 'TODO(fn-20)' skills/` returns empty
- [ ] `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty (no duplicate names)
- [ ] `./scripts/validate-skills.sh` passes
- [ ] Cross-references validated in all 4 skills

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
