# fn-53-skill-routing-language-hardening.11 Content-Preservation Verification

## Description
Mandatory verification that all intended content remains represented after normalization across T5-T10. Produce a content migration map with source-section to destination-section mapping. Run automated checks for dropped sections, broken references, and self/cyclic cross-links.

**Size:** M
**Files:**
- `docs/skill-content-migration-map.md` (new)
- Read-only: all `skills/**/SKILL.md`, `agents/*.md`, sweep reports from T6-T9

## Approach

- Diff each SKILL.md against its pre-normalization state (git diff against the branch point)
- Build migration map: for each modified skill, list sections before/after with content status (unchanged/reworded/moved/removed)
- Run the T3 validator to check all cross-references resolve
- Check for self-referential cross-links (skill referencing itself)
- Verify no section was dropped without being moved elsewhere
- Verify total description budget is within WARN threshold

## Key context

- Memory pitfall: "Stale not-yet-landed references must be treated consistently" -- check for `planned` status markers that should now be `implemented`
- The `dotnet-advisor` catalog sections marked `planned`/`implemented` must be verified current
- This is the quality gate before docs/CI updates in T12
## Acceptance
- [ ] `docs/skill-content-migration-map.md` covers all 130 skills with section-level before/after mapping
- [ ] Zero dropped sections without documented migration target
- [ ] Zero broken cross-references across skills and agents
- [ ] Zero self-referential cross-links
- [ ] `dotnet-advisor` catalog status markers are current
- [ ] Total description budget ≤12,000 chars (within WARN threshold)
- [ ] `./scripts/validate-skills.sh` passes with zero errors and zero new warnings vs baseline
- [ ] `./scripts/validate-marketplace.sh` passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
