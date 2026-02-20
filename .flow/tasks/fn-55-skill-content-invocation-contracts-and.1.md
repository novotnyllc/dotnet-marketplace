# fn-55-skill-content-invocation-contracts-and.1 Define invocation contract spec and update style guide

## Description
Define a purely structural, machine-checkable invocation contract spec for SKILL.md. Document validation split. Include rollout playbook. Fix PRD: epic reference + agent update deferral.

**Size:** M
**Files:** `docs/skill-routing-style-guide.md`, `CONTRIBUTING-SKILLS.md`, `.flow/specs/prd-routing-reliability-and-skill-invocation.md`

## Approach

- Add "Invocation Contract" section to style guide with 3 structural rules:
  1. Scope contains ≥1 `- ` bullet within section boundaries
  2. OOS contains ≥1 `- ` bullet within section boundaries
  3. At least one OOS bullet contains `[skill:<id>]` string (presence only)
- Unordered (`- `) only. Numbered lists do NOT count. Explicit statement.
- Validation split: STRICT_INVOCATION (presence) vs STRICT_REFS (resolution) — documented as independent.
- No "Use when:" phrasing requirement.
- Positive/negative examples using cases.json skills
- "Rollout Playbook" paragraph: WARN-only → STRICT_INVOCATION=1 after 130 skills compliant
- CONTRIBUTING-SKILLS.md section 8 checklist item
- PRD fixes:
  - Line 10: `fn-57` → `fn-55`
  - Workstream B.2: add note that agent updates (agents/*.md) are deferred — agents don't use Scope/OOS format, separate convention needed
  - Acceptance Criteria #6 (if applicable): add deferral note

## Key context

- Style guide already covers description formula, scope format, cross-ref syntax
- Agent files (agents/*.md) use a different structure than skills — invocation contract applies to SKILL.md only
- PRD originally scoped "skill and agent updates" but agents need a different convention first

## Acceptance
- [ ] `grep "Invocation Contract" docs/skill-routing-style-guide.md` finds section
- [ ] 3 structural rules, unordered bullets only, numbered lists excluded
- [ ] STRICT_INVOCATION vs STRICT_REFS split documented
- [ ] NO "Use when:" requirement stated
- [ ] Examples included
- [ ] Rollout playbook paragraph
- [ ] CONTRIBUTING-SKILLS.md checklist item
- [ ] PRD: fn-57 → fn-55 corrected
- [ ] PRD: Workstream B.2 agent deferral note added
