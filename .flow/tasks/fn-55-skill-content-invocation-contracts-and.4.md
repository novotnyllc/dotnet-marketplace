# fn-55-skill-content-invocation-contracts-and.4 Add positive and negative control regression test cases

## Description
Add positive/negative control test cases exercising fn-54's schema. Update provider baseline. Prove integration via runner mismatch classifications in output.

**Size:** M
**Files:** `tests/agent-routing/cases.json`, `tests/agent-routing/provider-baseline.json`, `tests/trigger-corpus.json` (if new categories)

## Approach

- **HARD PREREQUISITE:** fn-54 runner support (optional_skills, disallowed_skills, provider-baseline.json) must be on branch before merge.
- Add ≥3 positive control cases targeting skills from T3, diverse prompt styles
- Add ≥2 negative control cases using `disallowed_skills`:
  - **At least one case MUST be designed to likely trigger the disallowed skill.** The prompt must naturally lead toward the disallowed skill's domain while requiring a different skill for the primary task. This ensures `failure_kind == "disallowed_hit"` is actually observable in runner output (not just hypothetical). Set `expected_status` in baseline to reflect the expected outcome per provider.
- Add ≥1 case with `optional_skills`:
  - **Prompt must be designed to likely trigger the optional skill** so `optional_hits[]` is populated in runner output. Choose an optional skill whose domain naturally overlaps with the primary task prompt.
- **Baseline updates:** Run matrix (or `--agents claude,codex,copilot`) to generate baseline entries for all new case IDs. Add entries to `provider-baseline.json` with intended per-provider statuses (claude likely pass, copilot may be fail/infra_error).
- **Prove integration is active (not hypothetical counterfactual):**
  - At least one disallowed case produces `disallowed_hit` mismatch classification in runner JSON output when the disallowed skill IS invoked
  - At least one optional case produces `optional_hits[]` entries in runner JSON output
  - Verification: `jq '.results[] | select(.failure_kind == "disallowed_hit")' <output>` returns non-empty
  - Verification: `jq '.results[] | select(.optional_hits | length > 0)' <output>` returns non-empty
- Each case has specific evidence tokens (not copy-pasted defaults)
- If adding new category, update `tests/trigger-corpus.json`

## Key context

- Current corpus: 14 cases. fn-54 adds optional_skills, disallowed_skills, disallowed_min_tier.
- fn-54 also adds provider-baseline.json — new cases MUST have entries or CI will hard-fail
- All existing cases share generic `required_any_evidence` — new cases use targeted evidence
- Memory: "Trigger corpus completeness" — new category → trigger-corpus.json entry
- The disallowed case design is critical: if the prompt doesn't naturally lead toward the disallowed skill, the model will simply not invoke it, and `disallowed_hit` will never appear — making the test case useless for validation
- **Disallowed cases that produce `disallowed_hit` are expected failures, not bugs.** Their baseline entry should reflect this (e.g., `expected_status: "fail"` for providers where the hit is expected). Do NOT conflate "pass with claude" with "all cases succeed."

## Acceptance
- [ ] ≥3 new positive control cases in cases.json
- [ ] ≥2 new negative control cases using `disallowed_skills`
- [ ] ≥1 disallowed case with prompt crafted to likely trigger the disallowed skill (observable `disallowed_hit`)
- [ ] ≥1 case uses `optional_skills` with prompt crafted to likely trigger the optional skill (observable `optional_hits[]`)
- [ ] `provider-baseline.json` updated with entries for ALL new case IDs per provider
- [ ] New **positive** cases pass with `--agents claude` locally (with fn-54 on branch)
- [ ] At least one **disallowed** control case yields `failure_kind == disallowed_hit` in runner output, consistent with `provider-baseline.json` expected_status — verifiable: `jq` query
- [ ] At least one **optional** control case yields `optional_hits` entries in runner output — verifiable: `jq` query
- [ ] New cases have case-specific evidence tokens
- [ ] `tests/trigger-corpus.json` updated if new categories added

## Evidence
<!-- flowctl:evidence -->

## Done summary
<!-- flowctl:done-summary -->
