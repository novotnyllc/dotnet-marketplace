# fn-62-fix-eval-subprocess-timeouts-and.1 Fix _execute_cli process group kill and add --max-turns + configurable timeouts

## Description
Refactor `_execute_cli()` in `_common.py` to use `subprocess.Popen` with `start_new_session=True` instead of `subprocess.run`, so the entire process tree is killed on timeout via `os.killpg()`. Add `--max-turns 1` via automatic feature detection. Make timeouts configurable via `config.yaml` with per-eval-type overrides. Add a shared per-case deadline mechanism in the runners. Thread timeout through `call_model()` via an optional `timeout_s` parameter with safe defaults.

**Size:** M
**Files:** `tests/evals/_common.py`, `tests/evals/config.yaml`, `tests/evals/run_activation.py`, `tests/evals/run_confusion_matrix.py`, `tests/evals/run_effectiveness.py`, `tests/evals/run_size_impact.py`, `tests/evals/judge_prompt.py`

## Approach

### Process group kill (all 3 transport branches in `_execute_cli`)

- Replace `subprocess.run()` at L573-663 with `Popen(start_new_session=True)` + `communicate(timeout=N)` in all 3 transport modes (stdin, file_stdin, arg)
- In `TimeoutExpired` handler: `os.killpg(proc.pid, signal.SIGTERM)` → 3s grace via `proc.communicate(timeout=3)` → `os.killpg(proc.pid, signal.SIGKILL)` → `proc.wait()`
- Wrap `killpg` calls in `try/except ProcessLookupError` (process may have already exited)
- Always call `proc.communicate()` or `proc.wait()` after kill to drain pipes and reap zombie
- Ensure temp files from file_stdin mode are deleted in a `finally` block covering the entire Popen lifecycle (not just the happy path)
- Use `start_new_session=True` (Python 3.2+, portable) instead of `process_group=0` (Python 3.11+)

### Timeout exception stability

- Raise `RuntimeError("claude CLI timed out")` — NO duration in the message string
- Log the actual duration and timeout value to stderr separately
- This keeps `ConsecutiveFailureTracker` fingerprints stable regardless of config values

### Configurable timeouts

Add `timeouts` section to `config.yaml`. All values are in **seconds (integers)**:

```yaml
timeouts:
  # Per-attempt timeout: max seconds for a single subprocess.Popen.communicate() call
  per_attempt:
    activation: 15
    confusion: 15
    effectiveness: 45
    size_impact: 45
    judge: 45
    activation_fallback: 15
  # Per-case budget: max total seconds for all attempts+retries on one eval case
  per_case_budget:
    activation: 60
    confusion: 60
    effectiveness: 120
    size_impact: 120
  # Infrastructure timeouts
  probe: 15         # CLI capability probe timeout
  kill_grace: 3     # seconds between SIGTERM and SIGKILL
```

**Precedence**: explicit `timeout_s` arg > role-based config key > hardcoded default (45s per-attempt, 120s per-case).

Read from config via `load_config().get("timeouts", {})` with `.get()` chains for backward compat with configs lacking the section.

### Shared per-case deadline

Each runner computes `case_deadline = time.monotonic() + budget_s` **once per case** at the start of the case loop iteration. The same `case_deadline` (or a lightweight `CaseDeadline` object) is passed into **every** `retry_with_backoff()` and `call_model()` call within that case — including primary calls, fallback classifier calls, and judge calls. `retry_with_backoff()` checks remaining time before each attempt: if `time.monotonic() >= case_deadline`, skip retry; if remaining time < per-attempt timeout, clamp timeout to remaining time.

### `--max-turns 1` feature detection

- On first `_build_cli_command()` call, probe `claude -p --help` (cached via module-level flag)
- If stdout/stderr contains `--max-turns`, add `["--max-turns", "1"]` to args
- If not found, skip and log warning — `--tools ""` already prevents agentic turns as fallback
- Cache result so probe runs once per process, not per call

### Env vars

- Add to `_subprocess_env()`: `DISABLE_TELEMETRY=1`, `DISABLE_ERROR_REPORTING=1`
- Do NOT add undocumented env vars — these are unverified

### Call site updates

- Each runner: compute `case_deadline` once per case, pass to all `call_model()` / `retry_with_backoff()` invocations within that case
- `run_activation.py`: pass deadline to primary call AND fallback classifier calls
- `run_confusion_matrix.py`: pass deadline to primary call
- `run_effectiveness.py`: pass deadline to generation AND judge calls
- `run_size_impact.py`: pass deadline to generation AND judge calls
- `judge_prompt.py`: accept `case_deadline` parameter, respect it across multi-attempt judge retries

## Key context

- `start_new_session=True` makes the child the session leader; `os.killpg(proc.pid, ...)` works because `pid == pgid` when session leader
- `Popen.communicate(timeout=N)` uses internal threads for pipe reading — safe to call `os.killpg()` after `TimeoutExpired` because the threads receive broken-pipe and terminate
- The `ConsecutiveFailureTracker` fingerprints by `str(exc)` — varying timeout values in the message would fragment fingerprints
- `load_config()` has a module-level cache (`_config_cache`); use `.get("timeouts", {}).get(key, default)` to handle configs that lack the section

## Acceptance
- [ ] `_execute_cli()` uses `Popen(start_new_session=True)`, not `subprocess.run`, in all 3 transport branches
- [ ] Timeout triggers `os.killpg(proc.pid, SIGTERM)` → 3s grace → `os.killpg(proc.pid, SIGKILL)` with `ProcessLookupError` handling
- [ ] Pipes always drained via `proc.communicate()` or `proc.wait()` after kill in all branches
- [ ] Temp files from file_stdin cleaned up in `finally` block covering full Popen lifecycle
- [ ] `config.yaml` has `timeouts` section with `per_attempt`, `per_case_budget`, `probe`, `kill_grace` — all in seconds
- [ ] Config precedence: explicit arg > config key > hardcoded default
- [ ] Timeout values read from config with `.get()` defaults for backward compat
- [ ] `call_model()` accepts optional `timeout_s` and `case_deadline` parameters; all runner call sites and `judge_prompt.py` pass them
- [ ] Shared `case_deadline` computed once per case and threaded through ALL calls in that case (primary + fallback + judge)
- [ ] `retry_with_backoff()` respects `case_deadline`: skips retry if expired, clamps timeout if near expiry
- [ ] Timeout exception message is stable: `"claude CLI timed out"` (no duration in string)
- [ ] `--max-turns 1` added via cached feature detection; graceful fallback if unsupported
- [ ] `_subprocess_env()` sets `DISABLE_TELEMETRY=1` and `DISABLE_ERROR_REPORTING=1`
- [ ] `python3 tests/evals/run_activation.py --limit 3` completes without hanging
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: