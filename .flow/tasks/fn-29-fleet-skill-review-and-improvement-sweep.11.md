# fn-29-fleet-skill-review-and-improvement-sweep.11 Implement improvements: Batches E+F

## Description

Apply all Critical and High-value improvements from consolidated findings to skills in Batches E (ui-frameworks, agent-meta-skills) and F (documentation, packaging, localization). Improvements will be listed in consolidated-findings.md with skill name, category, issue description, and proposed fix. Implement changes by editing SKILL.md or details.md files directly, following the pattern established in batch-a-findings.md "Recommended Changes" section (Critical must-fix, High should-fix, Low nice-to-have). Commit per-category with conventional commit messages.

**File ownership:** This task modifies only `SKILL.md` and `details.md` files within its assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Description changes:** Do not modify descriptions without verifying aggregate budget impact against the projection in consolidated findings. Proposed descriptions in consolidated findings are pre-calculated to fit within the 12K warn threshold.

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
