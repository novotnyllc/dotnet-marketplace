# fn-60.3 Fix activation and confusion routing issues

## Description

Based on the analysis from task .2, fix skill descriptions (frontmatter) to improve activation routing accuracy and reduce confusion between overlapping skills.

**Depends on:** fn-60.2
**Size:** L
**Files:**
- `skills/*/SKILL.md` -- frontmatter description updates for skills identified in .2

**Execution order**: Run this task BEFORE task .4 (even though deps allow parallelism) to isolate attribution of improvements and avoid file conflicts.

## Approach

### Activation Fixes
- Skills that were never activated in L3: make descriptions more specific and action-oriented
- Skills with low activation rates: add key differentiating terms to descriptions
- Follow the routing style guide: Action + Domain + Differentiator formula (docs/skill-routing-style-guide.md)
- Keep descriptions under 120 characters

### Confusion Fixes
- For flagged cross-activation pairs (>20% rate): differentiate the two skills' descriptions
- For low-discrimination skills: add unique qualifying terms
- Focus on the 7 domain groups: testing, security, data, performance, api, cicd, blazor
- Ensure each skill in a group has a clearly distinct "action" or "domain" keyword

### Validation
- Run `./scripts/validate-skills.sh` after each batch of changes
- Quick-verify with `python3 tests/evals/run_activation.py --dry-run` (index char count should stay reasonable)
- Spot-check individual skills with `python3 tests/evals/run_activation.py --skill <name>`

## Acceptance
- [ ] All skills identified in .2 analysis have updated descriptions
- [ ] Descriptions still under 120 characters each
- [ ] Total description budget is budget-neutral or reduced (no increase from pre-fix baseline; target staying under 12,000 chars)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] Changes follow routing style guide conventions
