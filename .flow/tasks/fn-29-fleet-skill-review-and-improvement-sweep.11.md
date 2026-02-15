# fn-29-fleet-skill-review-and-improvement-sweep.11 Implement improvements: Batches E+F

## Description

Apply all Critical and High-value improvements from consolidated findings to skills in Batches E (ui-frameworks, agent-meta-skills) and F (documentation, packaging, localization). Commit per-category with conventional commit messages.

**File ownership:** This task modifies only `SKILL.md` and `details.md` files within its assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Description changes:** Do not modify descriptions without verifying aggregate budget impact against the projection in consolidated findings.

### Files

- **Input:** `docs/review-reports/consolidated-findings.md`
- **Modified:** `skills/ui-frameworks/*/SKILL.md`, `skills/agent-meta-skills/*/SKILL.md`, `skills/documentation/*/SKILL.md`, `skills/packaging/*/SKILL.md`, `skills/localization/*/SKILL.md`

## Acceptance
- [ ] All Critical improvements for Batches E+F implemented
- [ ] All High-value improvements for Batches E+F implemented
- [ ] Per-category commits with conventional commit messages
- [ ] `./scripts/validate-skills.sh` passes after all changes
- [ ] No modifications to plugin.json, AGENTS.md, or README.md

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
