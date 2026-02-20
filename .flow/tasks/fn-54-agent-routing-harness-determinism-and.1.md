# fn-54-agent-routing-harness-determinism-and.1 Add run ID telemetry, lifecycle progress, and failure categories

## Description
Add batch and unit UUID run IDs, structured lifecycle progress output, and failure categories to the routing test runner so every prompt-agent unit is trackable from queue to completion.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`

## Approach

- Generate `batch_run_id` (UUID v4) once per `RunAsync()` invocation; generate `unit_run_id` (UUID v4) per work item in `ExecuteWorkAsync()` (L206-257)
- Add `batch_run_id` to `ResultEnvelope` (L1464) and `unit_run_id` to `AgentResult` (L1524)
- Emit lifecycle transitions to stderr via `LogProgress()`: `[batch:{batch_run_id}] [unit:{unit_run_id}] {agent}:{case_id} -> {state}` where state is queued/running/completed/failed/timeout
- Add `failure_category` field to `AgentResult`: `timeout` (TimedOut==true), `transport` (process failed to start / missing CLI / nonzero exit with no parseable output), `assertion` (evidence gating failed), or null (pass). Orthogonal to routing mismatch `failure_kind`.
- Preserve existing `--no-progress` flag behavior (suppress stderr lifecycle output)

## Key context

- `LogProgress()` already uses `lock (_consoleLock)` for thread-safe stderr writes — reuse this
- `results[item.Index]` pre-allocated array ensures deterministic output ordering — do not change
- Run IDs must appear in both stderr progress AND JSON output for correlation
- Artifact directory creation and ARTIFACT_DIR emission are T4's responsibility, not T1's
- `parse` failure category deferred — current runner does substring matching, not structured JSON parsing

## Acceptance
- [ ] ResultEnvelope includes `batch_run_id` (UUID) — verifiable: `jq '.batch_run_id' <output> | grep -E '^[0-9a-f-]{36}$'`
- [ ] Every AgentResult includes `unit_run_id` (UUID) — verifiable: `jq '.results[].unit_run_id' <output>`
- [ ] unit_run_ids are unique across all results in a single execution
- [ ] Stderr shows lifecycle transitions: queued -> running -> completed/failed/timeout per unit
- [ ] AgentResult includes `failure_category` (timeout|transport|assertion|null)
- [ ] `--no-progress` suppresses lifecycle output
- [ ] Existing test cases continue to pass with no behavioral change
