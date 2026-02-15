# fn-29-fleet-skill-review-and-improvement-sweep.9 Implement improvements: Batches A+B

## Description

Apply all Critical and High-value improvements from consolidated findings to skills in Batches A (foundation, core-csharp, project-structure, release-management) and B (architecture, serialization, security, multi-targeting). Improvements will be listed in consolidated-findings.md with skill name, category, issue description, and proposed fix. Implement changes by editing SKILL.md or details.md files directly, following the pattern established in batch-a-findings.md "Recommended Changes" section (Critical must-fix, High should-fix, Low nice-to-have). Commit per-category with conventional commit messages.

**File ownership:** This task modifies only `SKILL.md` and `details.md` files within its assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Description changes:** Do not modify descriptions without verifying aggregate budget impact against the projection in consolidated findings. Proposed descriptions in consolidated findings are pre-calculated to fit within the 12K warn threshold.

### Files

- **Input:** `docs/review-reports/consolidated-findings.md`
- **Modified:** `skills/foundation/*/SKILL.md`, `skills/core-csharp/*/SKILL.md`, `skills/project-structure/*/SKILL.md`, `skills/release-management/*/SKILL.md`, `skills/architecture/*/SKILL.md`, `skills/serialization/*/SKILL.md`, `skills/security/*/SKILL.md`, `skills/multi-targeting/*/SKILL.md`

## Acceptance
- [ ] All Critical improvements for Batches A+B implemented
- [ ] All High-value improvements for Batches A+B implemented
- [ ] Per-category commits with conventional commit messages (e.g., `fix(core-csharp): ...`)
- [ ] `./scripts/validate-skills.sh` passes after all changes
- [ ] No modifications to plugin.json, AGENTS.md, or README.md

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
