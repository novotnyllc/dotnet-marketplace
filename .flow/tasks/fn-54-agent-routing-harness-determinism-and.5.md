# fn-54-agent-routing-harness-determinism-and.5 Convert CI to provider matrix with merge-base regression guardrails

## Description
Convert CI routing workflow to GHA strategy matrix with per-provider artifacts, merge-base baseline comparison, and mechanically enforceable regression gate including timeout and missing-artifact handling.

**Size:** M
**Files:** `.github/workflows/agent-live-routing.yml`, `tests/agent-routing/provider-baseline.json` (new)

## Approach

- Matrix: `agent: [claude, codex, copilot]`, `fail-fast: false`
- Each job: run `test.sh --agents ${{ matrix.agent }}`, parse `ARTIFACT_DIR=<path>` from stderr, upload `routing-results-${{ matrix.agent }}`
- `continue-on-error: true` copilot (infra only, not regressions)
- `summarize` job: `needs: [routing-test]`, `if: always()`, downloads via `pattern: routing-results-*` + `merge-multiple: true`
- `provider-baseline.json` schema: `{ "case_id": { "claude": { "expected_status": "pass|fail|infra_error", "allow_timeout": false }, ... } }`
- **Baseline comparison source-of-truth (explicit):**
  - For PRs: compare against `git show origin/${GITHUB_BASE_REF}:tests/agent-routing/provider-baseline.json` (merge-base version). Baseline edits in the PR branch are allowed but regression is still detected vs base-branch version, making the diff visible in the PR.
  - For pushes to main: compare against the checked-in file (self-referential is fine for non-PR context).
  - Summarize step checks out merge-base baseline as first operation.
- Comparison rules:
  - `pass -> fail` or `pass -> infra_error` vs baseline → REGRESSION (hard fail)
  - `timed_out=true` AND `allow_timeout=false` → REGRESSION
  - `timed_out=true` AND `allow_timeout=true` → ALLOWED
  - `fail -> pass` → IMPROVEMENT (informational, logged in delta table)
  - Missing provider artifact or results.json → HARD FAIL for that provider
- Delta table in job summary: case_id | claude | codex | copilot | delta

## Key context

- Current workflow (L26) is single job with 20-min timeout — matrix jobs each get own timeout
- upload-artifact v4 requires unique names per matrix dimension
- GHA matrix outputs: only last iteration accessible — must use artifacts
- Memory: "CI validation location must be specified" — regression comparison in summarize job only
- `git show origin/${GITHUB_BASE_REF}:...` is the standard GHA pattern for accessing base-branch files in PRs

## Acceptance
- [ ] `strategy.matrix.agent: [claude, codex, copilot]` with `fail-fast: false` — verifiable: grep in workflow
- [ ] Each job uploads `routing-results-${{ matrix.agent }}`
- [ ] Summarize downloads and merges all provider artifacts
- [ ] Baseline comparison uses merge-base for PRs — verifiable: `grep "GITHUB_BASE_REF" agent-live-routing.yml`
- [ ] `provider-baseline.json` uses `expected_status: pass|fail|infra_error` + `allow_timeout`
- [ ] `pass -> fail` regression → CI fails
- [ ] `timed_out + !allow_timeout` → regression detected
- [ ] Missing artifact → hard fail for that provider
- [ ] Delta table in summary
- [ ] Copilot `continue-on-error` does NOT suppress regression gate
