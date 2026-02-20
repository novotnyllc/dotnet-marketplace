# fn-54-agent-routing-harness-determinism-and.3 Extend case schema with optional, disallowed, and provider alias fields

## Description
Extend the `CaseDefinition` schema with `optional_skills`, `disallowed_skills`, and `provider_aliases` fields. Integrate with T2's tier-aware evaluation for granular mismatch classification with tier-gated disallowed detection.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`, `tests/agent-routing/cases.json`

## Approach

- Add fields to `CaseDefinition` (L1332): `optional_skills: string[]`, `disallowed_skills: string[]`, `provider_aliases: Dictionary<string, Dictionary<string, string>>`, `disallowed_min_tier: int` (default 2)
- `disallowed_skills` check: after evidence evaluation, if any disallowed skill token appears in `TokenHits` at or above `disallowed_min_tier`, classify as `disallowed_hit`. Tier 3 disallowed matches reported in diagnostics only (not failure-causing) to avoid false positives from weak mentions.
- `optional_skills`: track matches in `TokenHits` diagnostics. Output as `optional_hits[]` in AgentResult. Excluded from pass/fail gating.
- `provider_aliases`: resolve agent-specific skill names to canonical names before evidence matching. Integrates with `AddSkillVariants()` which already handles colon-separated prefixes.
- Granular mismatch reasons in `ClassifyFailure()`: `missing_required` (required token missing or below min tier), `disallowed_hit` (disallowed token found at >= min tier), `optional_only` (only optional skills matched, no required), `mixed` (multiple failure reasons)
- New fields default to empty — all 14 existing cases pass unchanged

## Key context

- T2 must be completed first: disallowed/optional matching uses `TokenHits` and `ComputeTier`
- `disallowed_min_tier` default 2 prevents Tier 3 weak mentions from triggering false disallowed failures — mirrors the same "weak evidence" problem from the original false-positive vector
- `AddSkillVariants()` already handles colon-separated prefixes — provider_aliases extends this
- All 14 existing cases use `required_all_evidence` and `required_any_evidence` only

## Acceptance
- [ ] CaseDefinition supports `optional_skills`, `disallowed_skills`, `provider_aliases`, `disallowed_min_tier` fields
- [ ] New fields default to empty/2 (all 14 existing cases pass unchanged)
- [ ] Disallowed skill at >= Tier 2 produces `disallowed_hit` failure
- [ ] Disallowed skill at Tier 3 only appears in diagnostics, not failure classification
- [ ] `disallowed_min_tier` per-case override works — verifiable: case with `disallowed_min_tier: 1` fails on Tier 1 hit
- [ ] Optional skill matches in `optional_hits[]` in AgentResult JSON, no pass/fail impact
- [ ] Provider aliases resolved before evidence matching
- [ ] ClassifyFailure returns: missing_required, disallowed_hit, optional_only, mixed
