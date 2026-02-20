# fn-54-agent-routing-harness-determinism-and.1 Add run ID telemetry, lifecycle progress, and failure categories

## Description
Add batch and unit UUID run IDs, structured lifecycle progress output, and failure categories to the routing test runner so every prompt-agent unit is trackable from queue to completion.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`

## Approach

- Generate `batch_run_id` (UUID v4) once per `RunAsync()` invocation; generate `unit_run_id` (UUID v4) per work item in `ExecuteWorkAsync()` (L206-257)
- Add `batch_run_id` to `ResultEnvelope` (L1464) and `unit_run_id` to `AgentResult` (L1524)
- Emit lifecycle transitions to stderr via `LogProgress()`: `[batch:{batch_run_id}] [unit:{unit_run_id}] {agent}:{case_id} -> {state}` where state is queued/running/completed/failed/timeout
- Add `failure_category` field to `AgentResult` with deterministic priority-order mapping: `timeout` if `TimedOut==true`; `transport` if process failed to start, CLI missing, or status is `infra_error`; `assertion` if evidence gating failed and not timed out; null if pass. Evaluated in priority order (timeout > transport > assertion). Orthogonal to routing mismatch `failure_kind`.
- Preserve existing `--no-progress` flag behavior (suppress stderr lifecycle transitions only). Protocol output lines (`ARTIFACT_DIR=...`) are never suppressed by `--no-progress` — they are T4's responsibility but T1 must not gate them behind `--no-progress`.

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

## Done summary
Added batch_run_id (UUID) to ResultEnvelope and unit_run_id (UUID) to each AgentResult for cross-correlation. Implemented lifecycle progress output on stderr (queued/running/completed/failed/timeout) with run IDs. Added failure_category field with deterministic priority mapping (timeout > transport > assertion). Detects missing CLI binaries (bash exit 126/127) as transport failures. Updated operator docs with new fields and stderr format.
## Evidence
- Commits: 733c2f599f8962818c9d45d2f05ea30c3df75a76, 08520bb, 686a61e
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, dotnet run --file tests/agent-routing/check-skills.cs -- --help, dotnet run --file tests/agent-routing/check-skills.cs -- --agents nonexistent --no-progress (verified batch_run_id, unit_run_id, failure_category), AGENT_FAKECLI_TEMPLATE='totally_nonexistent_binary_xyz {prompt}' dotnet run ... (verified CLI-missing -> transport)
- PRs: