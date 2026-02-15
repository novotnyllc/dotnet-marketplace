# fn-28-skill-authoring-how-to-manual-from.2 Update cross-references to skills guide

## Description

Add a prominent cross-reference to `CONTRIBUTING-SKILLS.md` in `CONTRIBUTING.md` so contributors can discover the skills-specific guide. Also verify and update references in `CLAUDE.md` and `AGENTS.md`:

- **CONTRIBUTING.md**: Add a section or callout near the top of the "Skill Authoring Guide" section directing readers to `CONTRIBUTING-SKILLS.md` for the comprehensive how-to manual. The existing skill authoring content in CONTRIBUTING.md should remain (it serves as a quick reference), but should note that the full guide is in CONTRIBUTING-SKILLS.md.
- **CLAUDE.md**: Update the References section to mention `CONTRIBUTING-SKILLS.md` alongside `CONTRIBUTING.md`.
- **AGENTS.md**: Verify the existing reference to "Skill authoring guide" in CONTRIBUTING.md is still accurate; update if needed to also mention CONTRIBUTING-SKILLS.md.

## Acceptance

- [ ] CONTRIBUTING.md contains a visible cross-reference to CONTRIBUTING-SKILLS.md
- [ ] CLAUDE.md References section mentions CONTRIBUTING-SKILLS.md
- [ ] AGENTS.md references verified and updated if needed
- [ ] All four validation commands still pass
- [ ] Cross-references use correct relative paths (no broken links)

## Files

- `CONTRIBUTING.md` (edit)
- `CLAUDE.md` (edit, if needed)
- `AGENTS.md` (edit, if needed)

## Done summary
Added cross-references to CONTRIBUTING-SKILLS.md in CONTRIBUTING.md (blockquote callout in Skill Authoring Guide section), CLAUDE.md (References section), and AGENTS.md (Cross-References section) so contributors can discover the comprehensive skill authoring how-to manual.
## Evidence
- Commits: f348651c089355ae528525e371fe0250ac924151
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: