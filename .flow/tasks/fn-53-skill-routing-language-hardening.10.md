# fn-53-skill-routing-language-hardening.10 Agent File Normalization

## Description
Normalize all 14 agent files (`agents/*.md`) to use canonical `[skill:]` cross-reference syntax. Baseline bare-ref counts per agent are documented in `docs/skill-routing-audit-baseline.md`. Also normalize agent description conventions per T2 style guide.

**Size:** M
**Files:**
- All 14 `agents/*.md` files (edit)
- Read-only: `docs/skill-routing-style-guide.md`

## Approach

- Convert all bare-text skill/agent references (backtick-wrapped, bold-wrapped) to `[skill:]` syntax
- Use `docs/skill-routing-audit-baseline.md` per-agent bare-ref counts to prioritize work (do not rely on hardcoded counts here)
- All 14 agents have bare refs per the baseline audit; none are pre-clean
- Even "clean" agents must be scanned for edge-case bare refs (e.g., in Trigger Lexicon text, code comments, or reference URLs that happen to contain skill names)
- Normalize agent description fields per style guide: no-WHEN-prefix, third-person declarative style ("Analyzes X for Y" not "WHEN analyzing X")
- Verify all `[skill:]` references in agent files resolve to existing skill directories
- After normalization, run the T3 agent validation (`--scan-agents` mode) to confirm zero bare-text refs remain

## Key context

- T3 adds automated agent file validation to `_validate_skills.py`. Use this to verify T10's work. Note: T3 reports agent bare-ref counts as informational (not errors) until T10 completes. After T10, T12 tightens the CI gate to enforce zero agent bare refs.
- Memory pitfall: "Cross-reference IDs must be canonical" -- verify each ref against actual skill name: fields.
- 5 agent descriptions currently use `WHEN` prefix. T2 style guide resolves: no WHEN prefix, third-person declarative.

## Acceptance
- [ ] All 14 agent files use `[skill:]` syntax for cross-references (zero bare-text refs, including in "clean" agents)
- [ ] Agent descriptions follow style guide conventions (no WHEN prefix, third-person declarative)
- [ ] All `[skill:]` references in agent files resolve to existing skill directories
- [ ] T3 agent validation passes (zero `AGENT_BARE_REF_COUNT`)
- [ ] `./scripts/validate-skills.sh` passes (agents not validated by this, but skills must not regress)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
