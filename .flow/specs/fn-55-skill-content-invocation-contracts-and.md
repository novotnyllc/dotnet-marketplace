# Skill Content Invocation Contracts and Validation

## Overview

Strengthen SKILL.md content so invocation signals are explicit, testable, and validated in CI. Define the invocation contract spec, update high-traffic skills, extend the validator with contract compliance checks, add content regression test cases, and establish cross-provider change policy.

**PRD:** `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
**PRD amendment:** Agent updates (agents/*.md) deferred to a follow-up epic. Agents don't use `## Scope`/`## Out of scope` format — a separate invocation-signal convention for agents is needed before updating them. PRD Workstream B.2 and Acceptance Criteria #6 to be updated with deferral note.

## Scope

- Define invocation contract as purely structural, machine-checkable rules for SKILL.md
- Update skill-routing-style-guide.md with invocation contract section
- Update the 14 skills in cases.json corpus with stronger signals
- Extend _validate_skills.py with structural invocation-contract checks
- Add positive/negative control test cases (requires fn-54 runner + baseline)
- Establish cross-provider change policy with operator-grade checklist
- Fix PRD: epic reference (fn-57 → fn-55) + agent update deferral note

## Design decisions

- **Invocation contract — 3 structural rules (unordered bullets only):**
  1. `## Scope` contains ≥1 unordered bullet (`- `) within section boundaries
  2. `## Out of scope` contains ≥1 unordered bullet (`- `) within section boundaries
  3. At least one OOS bullet contains a `[skill:<id>]` reference string (presence; resolution governed by STRICT_REFS)
  - Unordered (`- `) only. Numbered lists do NOT count.
  - No "Use when:" phrasing requirement.
- **Validation split:** STRICT_INVOCATION (presence) vs STRICT_REFS (resolution) — independent controls.
- **STRICT_INVOCATION mechanism:** `_validate_skills.py` reads `STRICT_INVOCATION` env var directly (same pattern as Python-level env reads). When set to `1`, contract warnings become errors. AC proves toggle via exit code difference.
- **WARN→ERROR rollout:** Default WARN. CI flip after compliance. Rollout playbook in style guide.
- **Skill scope:** 14 cases.json skills + dotnet-advisor routing catalog. No agents/*.md — deferred (see PRD amendment).
- **Test case dependency:** Hard fn-54 prerequisite. Baseline updates required. Integration proved via runner mismatch classifications in JSON output.
- **Cross-provider policy:** 3 concrete operator-grade bullets.
- **Budget check:** `BUDGET_STATUS != FAIL` (i.e., `CURRENT_DESC_CHARS < 15600`) — aligned with validator semantics.

## Task ordering

```
T1 (contract spec + style guide + PRD fixes) → T2 (validator checks)
                                               → T3 (skill content updates)
T3 → T4 (test cases + baseline) [after fn-54 merged + T3 ready]
T1 → T5 (cross-provider policy)
```

## Quick commands

```bash
./scripts/validate-skills.sh
./test.sh --agents claude --category foundation,testing
./scripts/validate-skills.sh 2>&1 | grep BUDGET
```

## Acceptance

- [ ] Invocation contract in style guide: 3 structural rules, unordered bullets only
- [ ] Contract separates presence (STRICT_INVOCATION) from resolution (STRICT_REFS)
- [ ] All 14 cases.json skills have ≥1 Scope `- ` bullet and ≥1 OOS `- ` bullet with `[skill:name]`
- [ ] Validator: section-bounded, unordered only, WARN default
- [ ] `STRICT_INVOCATION=1` promotes to ERROR — toggle proved via exit code AC
- [ ] `INVOCATION_CONTRACT_WARN_COUNT` in validator output
- [ ] ≥3 positive, ≥2 disallowed, ≥1 optional cases; baseline updated; integration proved via jq
- [ ] CONTRIBUTING.md cross-provider policy with 3 operator-grade bullets
- [ ] PRD: fn-57 → fn-55 + agent update deferral note
- [ ] `BUDGET_STATUS != FAIL` (CURRENT_DESC_CHARS < 15600)
- [ ] All existing validation and tests pass

## References

- PRD: `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
- Predecessor: fn-53; Depends on: fn-54
- Key files: `docs/skill-routing-style-guide.md`, `scripts/_validate_skills.py`, `tests/agent-routing/cases.json`, `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`
