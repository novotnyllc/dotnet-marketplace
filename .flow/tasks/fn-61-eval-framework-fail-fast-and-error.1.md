# fn-61-eval-framework-fail-fast-and-error.1 Error classification and fail-fast infrastructure in _common.py

## Description
Add error classification, a consecutive-failure tracker, and reduced probe timeouts to `_common.py`. This is the infrastructure task -- runners integrate it in task .2.

**Size:** M
**Files:**
- `tests/evals/_common.py` -- new exception type, stderr classification, tracker class, probe timeout
- `tests/evals/config.yaml` -- new `fail_fast` section

## Approach

### 1. New `CLIPermanentError` exception

Add as a subclass of `CLIConfigError` at `_common.py:33`. `retry_with_backoff` already skips `CLIConfigError` subclasses (line 688-691), so this gets non-retryable behavior for free.

### 2. Stderr-based error classification in `_execute_cli()`

At `_common.py:518-522`, where `RuntimeError` is raised on non-zero exit code, add stderr pattern matching before raising:

- Parse `proc.stderr` against two pattern lists (retryable vs permanent)
- Retryable patterns: `overloaded_error`, `529`, `rate_limit`, `429`, `api_error`, `500`, `ECONNREFUSED`, `ENOTFOUND`, `ETIMEDOUT`, `timeout`
- Permanent patterns: `authentication_error`, `401`, `permission_error`, `403`, `invalid_request_error`, `400`, `not_found_error`, `404`, `request_too_large`, `413`, `unknown option`, `invalid flag`, `unrecognized argument`
- Also classify exit codes 126 (permission denied) and 127 (command not found) as permanent per `.flow/memory/conventions.md`
- If permanent match: raise `CLIPermanentError` (skips retries)
- If retryable match or no match: raise `RuntimeError` (retries normally)
- Timeout (`subprocess.TimeoutExpired`) stays as `RuntimeError` (retryable)

### 3. `ConsecutiveFailureTracker` class

Add to `_common.py` after the retry section. Simple stateful tracker:
- `__init__(threshold: int = 3)` -- configurable threshold
- `record_failure(exc: Exception) -> bool` -- returns True when threshold breached with same fingerprint
- `record_success()` -- resets counter
- `reset()` -- explicit reset (for multi-run mode)
- Fingerprint: first 200 chars of `str(exc)`, normalized (collapse whitespace)
- Expose `last_fingerprint` and `consecutive_count` for diagnostics

### 4. Reduce probe timeout

At `_common.py:207` and `:226`, change `timeout=120` to `timeout=15` in the `_run_probe()` helper. Only affects capability detection probes, not production `_execute_cli()` calls (which keep 120s).

### 5. Config keys

Add to `config.yaml`:
```yaml
fail_fast:
  consecutive_threshold: 3    # same-error consecutive failures to abort
  enabled: true               # can be disabled for debugging
```

Load with defaults: `cfg.get("fail_fast", {}).get("consecutive_threshold", 3)`.

## Key context

- `CLIConfigError` is already non-retryable (line 688-691 of `_common.py`). Making `CLIPermanentError` a subclass means zero changes to `retry_with_backoff`.
- The `_cli_caps` probe cache (line 116) means probes only fire once per process. Reducing probe timeout from 120s to 15s saves up to 210s on first invocation with a broken CLI (was: 2 modes x 120s + json probe; now: 2 x 15s + json probe).
- `.flow/memory/conventions.md` explicitly says: "Use a custom exception type that retry_with_backoff re-raises immediately to avoid stalling on deterministic failures."
- `.flow/memory/conventions.md` also notes: "exit code 127 (command not found) and 126 (permission denied) indicate missing/non-executable binary."
## Acceptance
- [ ] `CLIPermanentError` class exists, is a subclass of `CLIConfigError`
- [ ] `_execute_cli()` classifies non-zero exit codes via stderr pattern matching before raising
- [ ] Exit codes 126/127 raise `CLIPermanentError`
- [ ] Known permanent patterns (auth, bad flags) raise `CLIPermanentError`
- [ ] Known retryable patterns (overloaded, rate limit) raise `RuntimeError`
- [ ] Unknown errors default to `RuntimeError` (conservative, retryable)
- [ ] `retry_with_backoff` skips retries for `CLIPermanentError` (inherits from `CLIConfigError` handling)
- [ ] `ConsecutiveFailureTracker` class exists with `record_failure()`, `record_success()`, `reset()`
- [ ] `record_failure()` returns True after N consecutive same-fingerprint failures
- [ ] Probe timeout reduced to 15s in `_run_probe()` (both stdin and file_stdin modes)
- [ ] Production call timeout in `_execute_cli()` unchanged at 120s
- [ ] `config.yaml` has `fail_fast` section with `consecutive_threshold` and `enabled`
- [ ] Missing config keys don't crash (defaults via `.get()`)
- [ ] No new external dependencies added to `requirements.txt`
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
## Done summary
Cancelled - work folded into fn-60
## Evidence
- Commits:
- Tests:
- PRs: