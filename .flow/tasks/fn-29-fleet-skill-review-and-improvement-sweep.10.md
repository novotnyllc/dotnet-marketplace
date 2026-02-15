# fn-29-fleet-skill-review-and-improvement-sweep.10 Implement improvements: Batches C+D

## Description

Apply all Critical and High-value improvements from consolidated findings to skills in Batches C (testing, cicd) and D (api-development, cli-tools, performance, native-aot). Commit per-category with conventional commit messages.

**File ownership:** This task modifies only `SKILL.md` and `details.md` files within its assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Description changes:** Do not modify descriptions without verifying aggregate budget impact against the projection in consolidated findings.

### Files

- **Input:** `docs/review-reports/consolidated-findings.md`
- **Modified:** `skills/testing/*/SKILL.md`, `skills/cicd/*/SKILL.md`, `skills/api-development/*/SKILL.md`, `skills/cli-tools/*/SKILL.md`, `skills/performance/*/SKILL.md`, `skills/native-aot/*/SKILL.md`

## Acceptance
- [ ] All Critical improvements for Batches C+D implemented
- [ ] All High-value improvements for Batches C+D implemented
- [ ] Per-category commits with conventional commit messages
- [ ] `./scripts/validate-skills.sh` passes after all changes
- [ ] No modifications to plugin.json, AGENTS.md, or README.md

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
