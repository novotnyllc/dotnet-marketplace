# fn-54-agent-routing-harness-determinism-and.4 Isolate all artifacts per batch, set concurrency, optimize log scanning

## Description
Isolate ALL per-run artifacts (results.json AND tool-use-proof.log) into batch-run-ID directories. Add `--artifacts-root`, emit `ARTIFACT_DIR`, set MAX_CONCURRENCY, optimize log snapshot to per-agent-per-batch.

**Size:** M
**Files:** `tests/agent-routing/check-skills.cs`, `test.sh`

## Approach

- T4 is sole owner of all artifact functionality:
  - Create `<artifacts-root>/<batch_run_id>/` at start of `RunAsync()`
  - Per-unit artifacts under `<batch_run_id>/<agent>-<case_id>/`
  - `results.json` at `<batch_run_id>/results.json`
  - `tool-use-proof.log` at `<batch_run_id>/tool-use-proof.log` (no separate `--proof-log` needed — default resolves under batch dir)
  - Emit `ARTIFACT_DIR=<fullpath>` on stderr after directory creation
- Add `--artifacts-root <path>` to `RunnerOptions.Parse()` (default: `tests/agent-routing/artifacts`)
- Remove hardcoded `PROOF_LOG` from test.sh (L8). test.sh no longer needs to manage proof log path — runner handles it.
- MAX_CONCURRENCY: default 4, `MAX_CONCURRENCY` env fallback, `--max-parallel` flag precedence
- Log snapshot: `CaptureLogSnapshot()` once per agent per batch (before scheduling), stored in `Dictionary<string, LogSnapshot>`
- `--enable-log-scan` flag: off when max_parallel > 1, on when serial. Aligns with T2's log_fallback policy.
- Update test.sh `--help` for all new options

## Key context

- Current `PROOF_LOG` in test.sh (L8) is single shared path — collision point. Removing it and defaulting under batch dir fixes this.
- `trap cleanup EXIT` in test.sh (L196) cleans `apps/` — do not change
- Memory: "Sole owner for parallel file creation" — runner creates batch dir, not test.sh
- Memory: "GHA script | tee exit code loss" — preserve exit codes

## Acceptance
- [ ] results.json at `<artifacts-root>/<batch_run_id>/results.json` — verifiable: `ls artifacts/*/results.json`
- [ ] tool-use-proof.log at `<artifacts-root>/<batch_run_id>/tool-use-proof.log` — verifiable: `ls artifacts/*/tool-use-proof.log`
- [ ] Per-unit artifacts at `<batch_run_id>/<agent>-<case_id>/`
- [ ] `ARTIFACT_DIR=<fullpath>` on stderr — verifiable: `./test.sh 2>&1 | grep ARTIFACT_DIR`
- [ ] `--artifacts-root` overrides base — verifiable: `--artifacts-root /tmp/test-arts` writes there
- [ ] test.sh has NO hardcoded `PROOF_LOG` path — verifiable: `grep -c PROOF_LOG test.sh` returns 0
- [ ] No collision: two sequential runs → different batch directories
- [ ] MAX_CONCURRENCY: default 4, env override, flag precedence
- [ ] `CaptureLogSnapshot()` once per agent per batch, not per unit
- [ ] `--enable-log-scan`: off when parallel, on when serial
- [ ] test.sh `--help` documents all new options
