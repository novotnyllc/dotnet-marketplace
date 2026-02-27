# Eval Framework Fail-Fast and Error Classification

## Overview

The eval framework (`tests/evals/`) shells out to the `claude` CLI for 73-300+ cases per run. When CLI calls fail deterministically (auth errors, bad flags, probe failures), every single case hits the same error because there is no fail-fast mechanism. Ralph ran fn-60.1 twelve times over 13 hours before the underlying code bugs were fixed.

Three failure modes observed:
1. **Auth error** (03:05) -- CLI surfaced API auth failure, all 73 cases failed identically
2. **Probe failure → arg mode fallback** (06:57-07:58) -- stdin/file_stdin probes failed, fell back to arg mode, prompt too large (15.7k > 4k limit). All 73 cases failed identically.
3. **Bad CLI flag** (10:03-10:13) -- `--max-tokens` flag not supported by CLI. All 73 cases failed identically.

Root cause: no error classification, no consecutive-failure detection, no early abort. The budget check (cost/call cap) is the *only* abort path, and it doesn't trigger on zero-cost failures.

## Scope

**In scope:**
- Error classification in `_common.py`: distinguish permanent errors (auth, bad flags, CLI not found) from transient errors (timeout, rate limit, overloaded)
- New `CLIPermanentError` exception type (non-retryable, like existing `CLIConfigError`)
- Consecutive-failure tracker: abort after N consecutive same-fingerprint failures
- Reduce probe timeout from 120s to 15s
- Runner-level fail-fast integration in all 4 runners
- `FAIL_FAST=1` output key on runner stdout contract
- `run_suite.sh` failure propagation (parse FAIL_FAST, handle skipped runners)
- Config keys for fail-fast thresholds with backward-compatible defaults
- Partial results on abort (already works; add `fail_fast_reason` to meta)

**Out of scope:**
- Adaptive timeouts (too complex for this fix; fixed tiers are sufficient)
- Third-party libraries (no circuitbreaker/tenacity -- custom 30-line tracker)
- Changes to eval datasets, rubrics, or skill content
- Changes to the Claude CLI itself

## Approach

### Error Classification

Add stderr pattern matching in `_execute_cli()` to classify non-zero-exit errors before raising:

**Retryable (raise RuntimeError, `retry_with_backoff` retries normally):**
- `overloaded_error`, `529`, `rate_limit`, `429`, `api_error`, `500`
- `ECONNREFUSED`, `ENOTFOUND`, `ETIMEDOUT`, `timeout`

**Permanent (raise new `CLIPermanentError`, `retry_with_backoff` skips retries):**
- `authentication_error`, `401`, `permission_error`, `403`
- `invalid_request_error`, `400`, `not_found_error`, `404`, `request_too_large`, `413`
- `unknown option`, `invalid flag`, `unrecognized argument`

**Unknown exit errors: default to RuntimeError (retryable)** -- conservative, avoids false abort on unexpected errors.

`CLIPermanentError` extends `CLIConfigError` so `retry_with_backoff` already handles it (line 688-691 re-raises `CLIConfigError` and subclasses immediately).

### Consecutive-Failure Tracker

A `ConsecutiveFailureTracker` class in `_common.py`:
- Tracks consecutive case-level failures (after retries are exhausted) with same error fingerprint
- Fingerprint = first 200 chars of error message (normalized)
- Threshold configurable via `config.yaml` (default: 3)
- `record_failure(exc) -> bool` returns True when threshold breached
- `record_success()` resets counter
- Counter resets at the start of each `--runs` iteration

Unit of failure = **case-level** (not individual CLI call). After `retry_with_backoff` exhausts retries for a case, that counts as one failure.

### Runner Integration

Each runner's main loop gets:
```
tracker = ConsecutiveFailureTracker(threshold=cfg["fail_fast"]["threshold"])
# ... in the loop:
except Exception as exc:
    if tracker.record_failure(exc):
        fail_fast = True; break
# ... on success:
tracker.record_success()
```

Multi-call-per-case runners (effectiveness: 2 gen + 1 judge; size_impact: 3-4 gen + N judge): any unrecoverable error within a case counts as one case-level failure.

### Output Contract Extension

Runners emit `FAIL_FAST=1` or `FAIL_FAST=0` on stdout. When `FAIL_FAST=1`:
- `ABORTED=1` is also set (superset)
- `FAIL_FAST_REASON=<error fingerprint>` added for diagnostics
- Results JSON `meta` gets `fail_fast_reason` field

### Suite-Level Propagation

`run_suite.sh` changes:
- Parse `FAIL_FAST` key from runner stdout
- If `FAIL_FAST=1` with a permanent-error reason (auth, CLI not found), skip remaining runners
- If `FAIL_FAST=1` with a transient reason (rate limit), continue to next runner
- Initialize all cost/call variables to `"0"` before running (prevent `float("")` crash on skipped runners)
- Suite summary JSON gets `fail_fast_runners` array listing which runners triggered fail-fast

### Probe Timeout

Reduce `_detect_cli_caps()` probe timeout from 120s to 15s. Both `stdin` and `file_stdin` modes. Production call timeout stays at 120s (appropriate for actual LLM calls).

## Quick commands

```bash
# Run activation with fail-fast (default behavior after changes)
python3 tests/evals/run_activation.py --dry-run

# Run a single skill to test CLI connectivity
python3 tests/evals/run_activation.py --skill dotnet-xunit

# Run full suite
./tests/evals/run_suite.sh

# Validate skills (no eval changes should break this)
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] Deterministic CLI errors (auth, bad flags) abort a runner within 3 cases, not 73
- [ ] Transient errors (timeout, rate limit) still retry normally
- [ ] `FAIL_FAST=1` emitted on stdout when consecutive-failure threshold breached
- [ ] `run_suite.sh` skips remaining runners on permanent fail-fast, continues on transient
- [ ] Partial results always written on abort (existing behavior preserved)
- [ ] Results JSON `meta` includes `fail_fast_reason` when applicable
- [ ] Probe timeout reduced to 15s (no change to production call timeout)
- [ ] Config keys have backward-compatible defaults (missing keys don't crash)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] No new external dependencies

## Risks

| Risk | Mitigation |
|------|------------|
| Stderr patterns change across CLI versions | Match conservatively; unknown errors default to retryable |
| False-positive abort on flaky errors | Require same-fingerprint consecutive failures, not just any failures |
| codex/copilot have different error formats | Error classification is backend-aware; default to retryable for unrecognized patterns |
| Reduced probe timeout causes false negatives | 15s is generous for a probe; if CLI needs >15s to start, something is wrong |
| Config backward compatibility | All new keys have defaults via `cfg.get("fail_fast", {}).get("threshold", 3)` |

## References

- `tests/evals/_common.py:33-41` -- existing `CLIConfigError` pattern (extend for `CLIPermanentError`)
- `tests/evals/_common.py:625-701` -- `retry_with_backoff()` (already handles `CLIConfigError` subclasses)
- `tests/evals/_common.py:439-527` -- `_execute_cli()` (add stderr classification here)
- `tests/evals/_common.py:127-309` -- `_detect_cli_caps()` (reduce probe timeout)
- `tests/evals/run_suite.sh:54-112` -- `run_runner()` (add FAIL_FAST parsing)
- `.flow/memory/conventions.md` -- "Retry logic must distinguish non-retryable config errors from transient failures"
- `.flow/memory/conventions.md` -- "CLI exit codes 127/126 misclassified as assertion failures"
