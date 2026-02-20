# fn-55-skill-content-invocation-contracts-and.5 Establish cross-provider change policy and update contributor docs

## Description
Establish cross-provider change policy with an operator-grade checklist in contributor documentation. Policy must be actionable, not ceremonial.

**Size:** S
**Files:** `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`

## Approach

- Add "Cross-Provider Change Policy" subsection to CONTRIBUTING.md near release checklist (lines 234-245)
- Policy must include 3 concrete operator-grade bullets:
  1. "PR description must state: targeted provider (if any) + expected behavior deltas across providers."
  2. "Attach CI artifact links or paste per-provider summary lines for claude/codex/copilot from CI matrix output."
  3. "If behavior intentionally diverges between providers, update provider-baseline.json (from fn-54) in same PR with justification comment."
- Add checkbox to release checklist: `- [ ] Cross-provider verification: changes verified against claude/codex/copilot matrix`
- Add pointer in CONTRIBUTING-SKILLS.md section 5 ("Testing Your Skill") to CI provider matrix output for verifying cross-agent behavior
- Preserve all existing checklist items unchanged

## Key context

- CONTRIBUTING.md release checklist (lines 234-245) uses `- [ ]` checkbox format with backtick-wrapped identifiers
- CONTRIBUTING-SKILLS.md has "Testing Your Skill" section (section 5)
- Memory: "grep-verifiable ACs" — new items must be greppable
- Policy should reference fn-54's provider-baseline.json for intentional divergence

## Acceptance
- [ ] `grep "Cross-Provider" CONTRIBUTING.md` finds the new policy section
- [ ] Policy includes 3 concrete bullets (targeted provider, CI artifacts, baseline updates)
- [ ] Release checklist includes cross-provider verification checkbox item
- [ ] Policy specifies that provider-targeted changes require explicit non-target verification
- [ ] CONTRIBUTING-SKILLS.md references CI provider matrix for testing verification
- [ ] Existing checklist items preserved unchanged
