# Fleet Review Findings Implementation

## Overview

The fleet skill review (fn-29) audited all skills against an 11-dimension rubric and produced a consolidated findings report with 82 issues (20 Critical, 31 High, 31 Low). Most findings have been organically fixed through subsequent epics fn-30 through fn-36. This epic implements the remaining work: trimming the aggregate description budget below the WARN threshold, updating the stale `--projected-skills` parameter, and updating documentation to reflect the current state.

**Depends on:** fn-37 (Skill Cleanup Sweep) which handles fn-N reference removal, .gitkeep cleanup, broken cross-refs, and other mechanical cleanup. fn-37 modifies SKILL.md **body content** (fn-N references, cross-refs); this epic modifies SKILL.md **frontmatter** (descriptions) and documentation files. These are disjoint edits within the same files. fn-37 should complete first to avoid merge conflicts; if running in parallel, rebase after fn-37 merges.

## Current state (post fn-30 through fn-36)

- **Already fixed:** All descriptions under 120 chars individually, broken cross-refs resolved, stale markers removed, Agent Gotchas gaps filled, multi-targeting skills registered, xUnit v3 IAsyncLifetime corrected, grep portability fixed
- **Remaining:** Aggregate description budget at ~12,645 chars (WARN threshold is 12,000). The 14 new skills added by fn-30-fn-36 were never reviewed against the rubric. Documentation counts are stale. The `--projected-skills 100` parameter in `validate-skills.sh` is stale (actual count is 113).

## Budget math

- 113 registered skills x 120 chars max = 13,560 chars theoretical maximum
- Current: ~12,645 chars (WARN). Need to trim ~645+ chars.
- `validate-skills.sh` thresholds: `--warn-threshold 12000 --fail-threshold 15000`
- Target: average ~106 chars/skill to comfortably stay below 12K
- Alternative: if trimming alone cannot reach below 12,000 without degrading triggering quality, raise `--warn-threshold` to at most 13,000 (not the fail threshold) with documented rationale

## Regression risk from concurrent epics

fn-38 (Expert Domain Agents) and fn-39 (Skill Coverage Gap Fill) are open and may add skills concurrently. Each new skill increases the aggregate description budget. Task 1 must start by checking the actual skill count (`jq '.skills | length' .claude-plugin/plugin.json`) and re-derive the budget target if the count exceeds 113. If fn-38/fn-39 land first, the trimming targets may need to be more aggressive or the WARN threshold adjustment becomes more likely.

## Quick commands

```bash
# Check current budget and skill count
./scripts/validate-skills.sh 2>&1 | grep -E 'CURRENT_DESC_CHARS|BUDGET_STATUS|WARN|REGISTERED_SKILLS'
jq '.skills | length' .claude-plugin/plugin.json

# Full validation
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh && python3 scripts/generate_dist.py --strict && python3 scripts/validate_cross_agent.py
```

## Acceptance

- [ ] Aggregate description budget below 12,000 chars OR WARN threshold raised to at most 13,000 with documented rationale
- [ ] All 14 skills from fn-30-fn-36 pass basic quality check (descriptions follow `[What] + [When]` formula, cross-refs use `[skill:]` syntax in both frontmatter and body)
- [ ] `--projected-skills` in `validate-skills.sh` updated to match actual registered skill count
- [ ] README.md, CLAUDE.md, AGENTS.md counts match actual registered skill count
- [ ] CHANGELOG.md entry documents fleet review resolution
- [ ] Fleet review docs (`docs/fleet-review-rubric.md`, `docs/review-reports/consolidated-findings.md`) annotated as historical snapshots
- [ ] All 4 validation commands pass with zero errors and zero warnings (excluding budget WARN if threshold adjusted)

## References

- `docs/fleet-review-rubric.md` -- 11-dimension rubric with batch assignments
- `docs/review-reports/consolidated-findings.md` -- 82 original findings (historical snapshot, many now resolved)
- `scripts/_validate_skills.py` -- canonical budget measurement (L307-L363)
- `scripts/validate-skills.sh` -- budget thresholds and `--projected-skills` parameter
- `CONTRIBUTING-SKILLS.md` -- description formula, budget rules
- `.flow/specs/fn-37-skill-cleanup-sweep.md` -- prerequisite epic covering fn-N removal
