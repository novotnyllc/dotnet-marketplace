# fn-61-eval-framework-fail-fast-and-error.2 Integrate fail-fast into runners and suite orchestrator

## Description
Wire the fail-fast infrastructure from task .1 into all 4 eval runners and the suite orchestrator. Each runner gets a `ConsecutiveFailureTracker` in its main loop. `run_suite.sh` parses the new `FAIL_FAST` output key and decides whether to skip remaining runners.

**Size:** M
**Files:**
- `tests/evals/run_activation.py` -- add tracker to main loop
- `tests/evals/run_confusion_matrix.py` -- add tracker to main loop
- `tests/evals/run_effectiveness.py` -- add tracker to main loop
- `tests/evals/run_size_impact.py` -- add tracker to main loop
- `tests/evals/run_suite.sh` -- parse FAIL_FAST, handle skipped runners

## Approach

### Runner integration (all 4 runners)

Same pattern in each runner's main case loop. Follow `run_activation.py` as the template:

1. Create tracker before the batch loop:
   ```
   tracker = _common.ConsecutiveFailureTracker(threshold=cfg_threshold)
   ```
2. After the existing `except Exception as exc:` block (which records `api_error`), add:
   ```
   if tracker.record_failure(exc):
       fail_fast = True; fail_fast_reason = tracker.last_fingerprint; break
   ```
3. After a successful case (no exception), add `tracker.record_success()`
4. Reset tracker at the start of each `--runs` iteration: `tracker.reset()`
5. Emit `FAIL_FAST=1` or `FAIL_FAST=0` on stdout alongside existing keys
6. Emit `FAIL_FAST_REASON=<fingerprint>` when `FAIL_FAST=1`
7. Add `fail_fast_reason` to results JSON `meta` dict when applicable
8. When `fail_fast=True`, also set `aborted=True` (FAIL_FAST implies ABORTED)

**Multi-call-per-case runners** (effectiveness, size_impact): Any unrecoverable exception within a case's generation or judge calls counts as one case-level failure for the tracker. The existing per-case exception handling already captures this -- the tracker wraps at the case level, not the individual CLI call level.

### Suite orchestrator (`run_suite.sh`)

1. Initialize all cost/call variables to `"0"` at script top (prevents `float("")` crash on skipped runners)
2. Parse `FAIL_FAST` and `FAIL_FAST_REASON` from each runner's stdout using existing `parse_runner_key()` helper
3. After each runner, check `FAIL_FAST=1`:
   - If reason contains permanent error indicators (`authentication`, `permission`, `not found`, `unknown option`): skip remaining runners, set `SUITE_FAIL_FAST=1`
   - If reason is transient (rate limit, overloaded): continue to next runner (transient issues may resolve)
4. Add `fail_fast_runners` array and `suite_fail_fast` boolean to `suite_summary.json`
5. Print `[suite] FAIL FAST: <runner> aborted due to <reason>, skipping remaining runners` to stderr

### Output contract

Each runner emits (on stdout, after existing keys):
```
FAIL_FAST=0|1
FAIL_FAST_REASON=<fingerprint when FAIL_FAST=1>
```

## Key context

- All 4 runners already have the same exception-handling pattern: `except Exception as exc: api_error = str(exc)`. The tracker integration is mechanical.
- Effectiveness runner makes 2 gen + 1 judge calls per case (`run_effectiveness.py:527-569`). Size impact makes 3-4 gen + N judge calls. In both cases, the existing per-case try/except captures the failure at the case level.
- `run_suite.sh:173-203` sums costs via Python snippet using `float(os.environ.get(..., '0'))`. Empty string from a skipped runner would crash -- must initialize to `"0"`.
- `judge_prompt.invoke_judge()` has its own retry loop (up to 3 attempts for parse failures) at `judge_prompt.py:178-221`. Judge parse failures are NOT the same as CLI errors -- they're expected behavior. The tracker should only see exceptions that propagate out of the case-level try/except, which already filters appropriately.
## Acceptance
- [ ] All 4 runners create a `ConsecutiveFailureTracker` and wire it into the main loop
- [ ] Tracker resets at the start of each `--runs` iteration
- [ ] Deterministic errors (auth, bad flags) trigger fail-fast within 3 cases
- [ ] Transient errors (timeout, rate limit) still retry normally and don't trigger premature abort
- [ ] `FAIL_FAST=0|1` emitted on stdout by all 4 runners
- [ ] `FAIL_FAST_REASON=<fingerprint>` emitted when `FAIL_FAST=1`
- [ ] `FAIL_FAST=1` implies `ABORTED=1`
- [ ] Results JSON `meta` includes `fail_fast_reason` when applicable
- [ ] Partial results written correctly on fail-fast abort
- [ ] `run_suite.sh` parses FAIL_FAST from each runner
- [ ] Suite skips remaining runners on permanent fail-fast reason
- [ ] Suite continues on transient fail-fast reason
- [ ] Suite summary JSON includes `fail_fast_runners` and `suite_fail_fast`
- [ ] No `float("")` crash when a runner is skipped (variables initialized to "0")
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
- [ ] `./tests/evals/run_suite.sh --dry-run` still works
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
## Done summary
Cancelled - work folded into fn-60
## Evidence
- Commits:
- Tests:
- PRs: