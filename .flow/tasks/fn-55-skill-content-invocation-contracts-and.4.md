# fn-55-skill-content-invocation-contracts-and.4 Add positive and negative control regression test cases

## Description
Add positive/negative control test cases exercising fn-54's schema. Update provider baseline. Prove integration via runner mismatch classifications in output.

**Size:** M
**Files:** `tests/agent-routing/cases.json`, `tests/agent-routing/provider-baseline.json`, `tests/trigger-corpus.json` (if new categories)

## Approach

- **HARD PREREQUISITE:** fn-54 runner support (optional_skills, disallowed_skills, provider-baseline.json) must be on branch before merge.
- Add ≥3 positive control cases targeting skills from T3, diverse prompt styles
- Add ≥2 negative control cases using `disallowed_skills` — prompts that should NOT invoke specific skills
- Add ≥1 case with `optional_skills` for diagnostic output
- **Baseline updates:** Run matrix (or `--agents claude,codex,copilot`) to generate baseline entries for all new case IDs. Add entries to `provider-baseline.json` with intended per-provider statuses (claude likely pass, copilot may be fail/infra_error).
- **Prove integration is active (not hypothetical counterfactual):**
  - At least one disallowed case must produce `disallowed_hit` mismatch classification in runner JSON output when the disallowed skill IS invoked
  - At least one optional case must produce `optional_hits[]` entries in runner JSON output
  - Verification: `jq '.results[] | select(.failure_kind == "disallowed_hit")' <output>` returns non-empty
- Each case has specific evidence tokens (not copy-pasted defaults)
- If adding new category, update `tests/trigger-corpus.json`

## Key context

- Current corpus: 14 cases. fn-54 adds optional_skills, disallowed_skills, disallowed_min_tier.
- fn-54 also adds provider-baseline.json — new cases MUST have entries or CI will hard-fail
- All existing cases share generic `required_any_evidence` — new cases use targeted evidence
- Memory: "Trigger corpus completeness" — new category → trigger-corpus.json entry

## Acceptance
- [ ] ≥3 new positive control cases in cases.json
- [ ] ≥2 new negative control cases using `disallowed_skills`
- [ ] ≥1 case uses `optional_skills`
- [ ] `provider-baseline.json` updated with entries for ALL new case IDs per provider
- [ ] Runner JSON output includes `disallowed_hit` classification for at least one case — verifiable: `jq` query
- [ ] Runner JSON output includes `optional_hits` for at least one case — verifiable: `jq` query
- [ ] New cases have case-specific evidence tokens
- [ ] All new cases pass with `--agents claude` locally (with fn-54 on branch)
- [ ] `tests/trigger-corpus.json` updated if new categories added
