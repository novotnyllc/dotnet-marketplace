# fn-54-agent-routing-harness-determinism-and.5 Convert CI to provider matrix with ref-based regression guardrails

## Description
Convert CI routing workflow to GHA strategy matrix with per-provider artifacts, ref-based baseline comparison via `baseline_ref` input, and mechanically enforceable regression gate including timeout and missing-artifact handling.

**Size:** M
**Files:** `.github/workflows/agent-live-routing.yml`, `tests/agent-routing/provider-baseline.json` (new)

## Approach

- Matrix: `agent: [claude, codex, copilot]`, `fail-fast: false`
- Each job: run `test.sh --agents ${{ matrix.agent }}`, parse `ARTIFACT_DIR=<path>` from stderr via `grep '^ARTIFACT_DIR=' stderr.log | cut -d= -f2-`, upload `routing-results-${{ matrix.agent }}` with `if: always()`
- `continue-on-error: true` copilot (infra only, not regressions)
- `summarize` job: `needs: [routing-test]`, `if: always()`, downloads via `pattern: routing-results-*` + `merge-multiple: true`
- `provider-baseline.json` schema: `{ "case_id": { "claude": { "expected_status": "pass|fail|infra_error", "allow_timeout": false }, ... } }`
- **Baseline comparison source-of-truth (ref-based, explicit):**
  - Add `baseline_ref` input to `workflow_dispatch` (type: string, default: `main`). For `schedule` runs, hardcode `main` as the baseline ref.
  - Workflow uses `actions/checkout` with `fetch-depth: 0` to ensure all refs are available.
  - Summarize step runs `git fetch origin <baseline_ref>` before baseline extraction.
  - Extract baseline via `git show origin/<baseline_ref>:tests/agent-routing/provider-baseline.json`.
  - Note: current triggers are `workflow_dispatch` + `schedule` only — `GITHUB_BASE_REF` is not available. If a PR trigger is added in the future, `baseline_ref` can default to `$GITHUB_BASE_REF` in that context.
  - Baseline edits in branches are allowed but regression is still detected vs the baseline ref version.
- Comparison rules:
  - `pass -> fail` or `pass -> infra_error` vs baseline → REGRESSION (hard fail)
  - `timed_out=true` AND `allow_timeout=false` → REGRESSION
  - `timed_out=true` AND `allow_timeout=true` → ALLOWED
  - `fail -> pass` → IMPROVEMENT (informational, logged in delta table)
  - Missing provider artifact or results.json → HARD FAIL for that provider
  - **Missing-entry policy (two-file comparison):** Summarize loads TWO baselines: (1) **ref baseline** from `git show origin/<baseline_ref>:...` and (2) **current baseline** from the working tree `tests/agent-routing/provider-baseline.json`.
    - Every `(case_id, provider)` in results MUST exist in the **current baseline** — missing → HARD FAIL: `"ERROR: No baseline entry for case '<case_id>' provider '<provider>'. Update provider-baseline.json."`
    - Regression comparison only for entries present in BOTH ref baseline and results. Entries in results + current baseline but absent from ref baseline → `NEW` coverage (logged in delta table, no regression comparison). This prevents deadlocking new-case addition.
- Delta table in job summary: case_id | claude | codex | copilot | delta (where delta is REGRESSION, IMPROVEMENT, NEW, or OK)

## Key context

- Current workflow (L26) is single job with 20-min timeout — matrix jobs each get own timeout
- upload-artifact v4 requires unique names per matrix dimension
- GHA matrix outputs: only last iteration accessible — must use artifacts
- Memory: "CI validation location must be specified" — regression comparison in summarize job only
- Current triggers are `workflow_dispatch` + `schedule` only — `GITHUB_BASE_REF` is empty in these contexts. Use `baseline_ref` input instead.
- `git show origin/<baseline_ref>:...` requires explicit `git fetch origin <baseline_ref>` and `fetch-depth: 0` to ensure ref availability

## Acceptance
- [ ] `strategy.matrix.agent: [claude, codex, copilot]` with `fail-fast: false` — verifiable: grep in workflow
- [ ] Each job uploads `routing-results-${{ matrix.agent }}`
- [ ] Summarize downloads and merges all provider artifacts
- [ ] Workflow adds `baseline_ref` input (default: `main`) — verifiable: grep `baseline_ref` in workflow
- [ ] Workflow uses `fetch-depth: 0` and explicit `git fetch origin <baseline_ref>` — verifiable: grep in workflow
- [ ] Baseline comparison uses `baseline_ref` input for all trigger types — no dependency on `GITHUB_BASE_REF`
- [ ] `provider-baseline.json` uses `expected_status: pass|fail|infra_error` + `allow_timeout`
- [ ] `pass -> fail` regression → CI fails
- [ ] `timed_out + !allow_timeout` → regression detected
- [ ] Missing artifact → hard fail for that provider
- [ ] Missing current-baseline entry for (case_id, provider) → hard fail with targeted error message
- [ ] New case_id absent from ref baseline but present in current baseline → `NEW` in delta table (no regression gate)
- [ ] Delta table in summary
- [ ] Copilot `continue-on-error` does NOT suppress regression gate
- [ ] Each matrix job uploads artifacts with `if: always()` to ensure summarize has data even on failure

## Done summary

## Evidence
