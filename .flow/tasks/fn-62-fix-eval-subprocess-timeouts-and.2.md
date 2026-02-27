# fn-62-fix-eval-subprocess-timeouts-and.2 Add per-runner wall-clock timeout to run_suite.sh with macOS shim

## Description
Add a per-runner wall-clock timeout to `run_suite.sh` so that if a Python runner hangs (deadlocked pipe, uncaught exception loop), the suite still progresses. Add a macOS-compatible timeout shim that normalizes exit codes to 124.

**Size:** S
**Files:** `tests/evals/run_suite.sh`

## Approach

### Timeout shim function

- Add a `_timeout_cmd()` shell function that:
  1. Uses `timeout` if available (Linux, or macOS with coreutils)
  2. Falls back to `gtimeout` if available (macOS Homebrew coreutils)
  3. Falls back to a bash watchdog function that: backgrounds the command, sleeps for duration, kills the process group, and `exit 124`
- The bash watchdog explicitly exits 124 to match GNU timeout semantics
- Use `--signal=TERM --kill-after=10s` with GNU/gtimeout; the bash fallback sends SIGTERM then SIGKILL after 10s

### Per-runner timeout values

- activation: 300s, confusion: 300s, effectiveness: 600s, size_impact: 600s
- These are outer safety bounds; per-case budgets from task .1 are the primary defense

### Integration into `run_runner()`

- Wrap the `python3 run_*.py` invocation (L150-194) with the timeout shim
- Preserve stdout capture — wrap only the python command, not the full function
- The shim must be invoked in a way that preserves argv: `_timeout_cmd "$secs" python3 "$EVALS_DIR/run_activation.py" "$@"` — not via `eval` or a flattened string
- Check exit code: if 124, treat as permanent failure and set `SUITE_SKIP_REMAINING=1`

### No global pkill trap

- Do NOT add a blanket `pkill -f` trap — it is dangerous and can kill unrelated user processes
- Task .1 handles process group cleanup at the subprocess level; no global cleanup needed

## Key context

- `run_runner()` at L150-194 captures stdout to extract `TOTAL_CALLS=`, `COST_USD=`, etc. — the timeout wrapper must preserve this capture by wrapping only the python command
- macOS does not ship GNU `timeout`; `gtimeout` via `brew install coreutils` is common but not guaranteed
- GNU `timeout` without `--foreground` sends signals to the entire process group by default
- If runner is killed mid-write, results JSON may be truncated; `run_suite.sh` already handles this via `jq` error checks in the summary section

## Acceptance
- [ ] Each runner invocation in `run_suite.sh` wrapped with a wall-clock timeout
- [ ] Timeout shim works on Linux (GNU timeout), macOS with coreutils (gtimeout), and macOS without coreutils (bash watchdog)
- [ ] All timeout paths normalize exit code to 124
- [ ] Exit code 124 triggers fail-fast (`SUITE_SKIP_REMAINING=1`)
- [ ] No blanket `pkill -f` patterns — cleanup handled by task .1 process group kills
- [ ] Stdout capture for key-value parsing preserved through timeout wrapper
- [ ] Shim invocation preserves argv (no `eval` or flattened strings)
- [ ] `./tests/evals/run_suite.sh --runs 1 --limit 3` completes within bounded time
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: