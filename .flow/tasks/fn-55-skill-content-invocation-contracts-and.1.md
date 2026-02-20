# fn-55-skill-content-invocation-contracts-and.1 Define invocation contract spec and update style guide

## Description
Define a purely structural, machine-checkable invocation contract spec for SKILL.md. Document validation split. Include rollout playbook. Fix PRD: epic reference + agent update deferral across all locations.

**Size:** M
**Files:** `docs/skill-routing-style-guide.md`, `CONTRIBUTING-SKILLS.md`, `.flow/specs/prd-routing-reliability-and-skill-invocation.md`

## Approach

- Add "Invocation Contract" section to style guide with 3 structural rules:
  1. Scope contains ≥1 `- ` bullet within section boundaries
  2. OOS contains ≥1 `- ` bullet within section boundaries
  3. At least one OOS bullet contains `[skill:<id>]` string (presence only — independent of STRICT_REFS resolution)
- Unordered (`- `) only. Numbered lists do NOT count. Explicit statement.
- Validation split documentation (include in BOTH locations):
  - Style guide: `STRICT_INVOCATION=1` → contract warnings become errors (exit 1)
  - Style guide: `STRICT_REFS=1` → unresolved `[skill:]` becomes errors (exit 1)
  - Explicit statement: these are independent toggles
- No "Use when:" phrasing requirement.
- Positive/negative examples using cases.json skills
- "Rollout Playbook" paragraph: WARN-only → STRICT_INVOCATION=1 after 130 skills compliant
- CONTRIBUTING-SKILLS.md section 8 checklist item
- PRD fixes (ALL agent-mentioning locations must be addressed):
  - Document Control (line 10): `fn-57` → `fn-55`
  - Workstream B.2: add note that agent updates (agents/*.md) are deferred — agents don't use Scope/OOS format, separate convention needed
  - Acceptance Criteria #6: add deferral note so AC doesn't contradict epic scope
  - Any other locations referencing agent updates: add consistent deferral language

## Key context

- Style guide already covers description formula, scope format, cross-ref syntax
- Agent files (agents/*.md) use a different structure than skills — invocation contract applies to SKILL.md only
- PRD originally scoped "skill and agent updates" but agents need a different convention first

## Acceptance
- [ ] `grep "Invocation Contract" docs/skill-routing-style-guide.md` finds section
- [ ] 3 structural rules, unordered bullets only, numbered lists excluded
- [ ] Rule #3 documented as presence check independent of STRICT_REFS resolution
- [ ] STRICT_INVOCATION vs STRICT_REFS split documented with explicit independence statement
- [ ] NO "Use when:" requirement stated
- [ ] Examples included
- [ ] Rollout playbook paragraph
- [ ] CONTRIBUTING-SKILLS.md checklist item
- [ ] PRD: fn-57 → fn-55 corrected (Document Control)
- [ ] PRD: Workstream B.2 agent deferral note added
- [ ] PRD: AC #6 agent deferral note added

## Done summary
Defined the invocation contract spec (3 structural rules for SKILL.md) in the style guide section 6, documented STRICT_INVOCATION vs STRICT_REFS as independent toggles in both the style guide and validate-skills.sh header, added invocation contract checklist item to CONTRIBUTING-SKILLS.md section 8, and fixed the PRD (fn-57 -> fn-55, agent deferral notes in Workstream B.2, AC #6, and Rollout Phase 3).
## Evidence
- Commits: 8456661d2f1211646b67f2c09eb8f7399b51644f
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: