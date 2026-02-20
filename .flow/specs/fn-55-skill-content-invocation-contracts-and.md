# Skill Content Invocation Contracts and Validation

## Overview

Strengthen SKILL.md content so invocation signals are explicit, testable, and validated in CI. Define the invocation contract spec, update high-traffic skills, extend the validator with contract compliance checks, add content regression test cases, and establish cross-provider change policy.

**PRD:** `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
**PRD amendment:** Agent updates (agents/*.md) deferred to a follow-up epic. Agents don't use `## Scope`/`## Out of scope` format — a separate invocation-signal convention for agents is needed before updating them. PRD Workstream B.2 and Acceptance Criteria #6 to be updated with deferral note.

## Scope

- Define invocation contract as purely structural, machine-checkable rules for SKILL.md
- Update skill-routing-style-guide.md with invocation contract section
- Update the 14 skills in cases.json corpus with stronger signals (NO agents/*.md)
- Extend _validate_skills.py with structural invocation-contract checks
- Add positive/negative control test cases (requires fn-54 runner + baseline)
- Establish cross-provider change policy with operator-grade checklist
- Fix PRD: epic reference (fn-57 → fn-55) + agent update deferral note across all locations

## Design decisions

- **Invocation contract — 3 structural rules (unordered bullets only):**
  1. `## Scope` contains ≥1 unordered bullet (`- `) within section boundaries
  2. `## Out of scope` contains ≥1 unordered bullet (`- `) within section boundaries
  3. At least one OOS bullet contains a `[skill:<id>]` reference string (presence; resolution governed by STRICT_REFS)
  - Unordered (`- `) only. Numbered lists do NOT count.
  - No "Use when:" phrasing requirement.
- **Rule #3 is a NEW dedicated check:** Separate from STRICT_REFS resolution. Rule #3 checks `[skill:` string presence inside OOS bullets; STRICT_REFS checks that referenced skill IDs actually exist. Both can be enabled/disabled independently.
- **Validation split:** STRICT_INVOCATION (presence) vs STRICT_REFS (resolution) — independent controls. Documented in BOTH `docs/skill-routing-style-guide.md` (new Invocation Contract section) AND `scripts/validate-skills.sh` (header comments).
- **STRICT_INVOCATION mechanism:** `_validate_skills.py` reads `STRICT_INVOCATION` env var directly (same pattern as Python-level env reads). When set to `1`, contract warnings become errors.
- **Stable output format:** Contract warnings use `INVOCATION_CONTRACT:` prefix in the warning message. Exact format matches existing validator convention:
  ```
  WARN:  skills/<cat>/<name>/SKILL.md -- INVOCATION_CONTRACT: <description>
  ```
  Summary key `INVOCATION_CONTRACT_WARN_COUNT=<N>` emitted by `_validate_skills.py` (Python), propagated through `validate-skills.sh` output.
- **Warning duplication during rollout:** A skill missing `## Scope` entirely will produce both the existing `missing '## Scope' section` warning AND the new `INVOCATION_CONTRACT: Scope section has 0 unordered bullets` warning. This is expected and correct during rollout — both warnings serve distinct purposes (structural presence vs contract compliance). Consolidation deferred until STRICT_INVOCATION is enabled by default.
- **WARN→ERROR rollout:** Default WARN. CI flip after compliance. Rollout playbook in style guide.
- **Skill scope:** 14 cases.json skills + dotnet-advisor routing catalog. NO agents/*.md — deferred (see PRD amendment).
- **Test case dependency:** Hard fn-54 prerequisite. Baseline updates required. Integration proved via runner mismatch classifications in JSON output.
- **T4 case design for observability:** At least one disallowed case must use a prompt crafted to likely trigger the disallowed skill, so `failure_kind == "disallowed_hit"` is actually observable. At least one optional case must use a prompt likely to trigger the optional skill, so `optional_hits[]` is populated. Note: disallowed cases that produce `disallowed_hit` are expected failures — acceptance criteria must distinguish positive cases (expected pass) from control cases (expected outcomes per baseline).
- **Cross-provider policy:** 3 concrete operator-grade bullets.
- **Budget check:** `BUDGET_STATUS != FAIL` (i.e., `CURRENT_DESC_CHARS < 15600`) — aligned with validator semantics.

## Task ordering

```
T1 (contract spec + style guide + PRD fixes) → T2 (validator checks)
                                               → T3 (skill content updates)
T3 → T4 (test cases + baseline) [after fn-54 merged + T3 ready]
T1 → T5 (cross-provider policy)
```

**Shared file note:** T1 and T5 both edit `CONTRIBUTING-SKILLS.md` (T1: section 8 checklist; T5: section 5 testing pointer). They are disjoint sections but same file. T5 already depends on T1, ensuring sequential access. Implementers should be aware of this overlap.

## Quick commands

```bash
./scripts/validate-skills.sh
./test.sh --agents claude --category foundation,testing
./scripts/validate-skills.sh 2>&1 | grep BUDGET
```

## Acceptance

- [ ] Invocation contract in style guide: 3 structural rules, unordered bullets only
- [ ] Contract separates presence (STRICT_INVOCATION) from resolution (STRICT_REFS)
- [ ] STRICT split documented in both style guide AND validate-skills.sh header comments
- [ ] Rule #3 (OOS `[skill:]` presence) implemented as dedicated check, independent of STRICT_REFS
- [ ] All 14 cases.json skills have ≥1 Scope `- ` bullet and ≥1 OOS `- ` bullet with `[skill:name]`
- [ ] No agents/*.md modified (deferred)
- [ ] Validator: section-bounded, unordered only, fence-aware, WARN default
- [ ] Contract warnings use exact format: `WARN:  <path> -- INVOCATION_CONTRACT: <description>`
- [ ] `INVOCATION_CONTRACT_WARN_COUNT` emitted by Python, propagated through shell wrapper
- [ ] `STRICT_INVOCATION=1` promotes to ERROR — toggle proved via exit code AC
- [ ] ≥3 positive cases (expected pass), ≥2 disallowed control cases, ≥1 optional control case; baseline updated
- [ ] New positive cases pass with `--agents claude` locally
- [ ] At least one disallowed case yields `failure_kind == disallowed_hit` consistent with `provider-baseline.json`
- [ ] At least one optional case populates `optional_hits[]` in runner output
- [ ] CONTRIBUTING.md cross-provider policy with 3 operator-grade bullets
- [ ] PRD: fn-57 → fn-55 + agent update deferral note (Document Control, Workstream B.2, AC #6)
- [ ] `BUDGET_STATUS != FAIL` (CURRENT_DESC_CHARS < 15600)
- [ ] All existing validation and tests pass

## References

- PRD: `.flow/specs/prd-routing-reliability-and-skill-invocation.md`
- Predecessor: fn-53; Depends on: fn-54
- Key files: `docs/skill-routing-style-guide.md`, `scripts/_validate_skills.py`, `tests/agent-routing/cases.json`, `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`
