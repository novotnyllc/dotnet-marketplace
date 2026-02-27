# fn-60-run-eval-suite-against-skills-and-fix.9 Add error classification and fail-fast to eval runners

## Description
Wire error classification from task .8 into all 4 eval runners and `run_suite.sh` so that permanent errors abort early instead of running all 73-300+ cases against a broken wall.

**Size:** M
**Files:**
- `tests/evals/run_activation.py` -- add consecutive-failure tracking to main loop
- `tests/evals/run_confusion_matrix.py` -- same
- `tests/evals/run_effectiveness.py` -- same
- `tests/evals/run_size_impact.py` -- same
- `tests/evals/run_suite.sh` -- parse FAIL_FAST, handle skipped runners
- `tests/evals/config.yaml` -- fail-fast threshold config

## Approach

### ConsecutiveFailureTracker

Add to `_common.py` (task .8 already modifies this file; this class can be added in .8 or .9 -- implementer's choice, just don't duplicate work):

A simple class tracking consecutive case-level failures with the same error fingerprint:
- `__init__(threshold: int = 3)` from config
- `record_failure(exc) -> bool` returns True when threshold breached
- `record_success()` resets counter
- `reset()` for multi-run boundaries
- Fingerprint: first 200 chars of `str(exc)`, whitespace-collapsed

### Runner integration

All 4 runners follow the same pattern. In each runner's main case loop:

After the existing `except Exception as exc:` (which records `api_error`):
```
if tracker.record_failure(exc):
    fail_fast = True
    fail_fast_reason = tracker.last_fingerprint
    break
```

After a successful case: `tracker.record_success()`

At the start of each `--runs` iteration: `tracker.reset()`

Multi-call-per-case runners (effectiveness: 2 gen + 1 judge; size_impact: 3-4 gen + N judge): any unrecoverable exception propagating from the case-level try/except counts as one failure. The tracker operates at the case level, not individual CLI call level.

### Output contract

Add to each runner's stdout output:
```
FAIL_FAST=0|1
FAIL_FAST_REASON=<fingerprint when 1>
```
When `FAIL_FAST=1`, also set `ABORTED=1`.

Add `fail_fast_reason` to results JSON `meta` when applicable.

### Suite orchestrator

In `run_suite.sh`:
1. Initialize all cost/call/case variables to `"0"` before running (prevents `float("")` crash if a runner is skipped)
2. Parse `FAIL_FAST` key from each runner's stdout
3. If `FAIL_FAST=1` with a permanent error reason (auth, permission, CLI not found): skip remaining runners
4. If `FAIL_FAST=1` with a transient reason: continue to next runner
5. Add `fail_fast_runners` list to `suite_summary.json`

### Config

Add to `config.yaml`:
```yaml
fail_fast:
  consecutive_threshold: 3
  enabled: true
```

Load with defaults: `cfg.get("fail_fast", {}).get("consecutive_threshold", 3)`.

## Key context

- All 4 runners already have `except Exception as exc: api_error = str(exc)` at the case level. The tracker wraps around this existing pattern.
- `run_suite.sh:173-203` sums costs with `float(os.environ.get(..., '0'))`. An empty string from a skipped runner would crash -- must initialize all variables.
- The existing `ABORTED` key only reflects budget exhaustion. `FAIL_FAST` is a new signal for error-based abort. They're independent but `FAIL_FAST=1` implies `ABORTED=1`.
- `judge_prompt.invoke_judge()` has its own retry loop for parse failures. Those are expected behavior, not CLI errors. The tracker only sees exceptions that escape the case-level try/except.
- Task .8 adds `CLIPermanentError(CLIConfigError)` -- this exception type is the primary signal for permanent vs transient classification. `isinstance(exc, CLIConfigError)` catches both `CLIConfigError` and `CLIPermanentError`.
- **Permanent error patterns** (from .8 research): auth failures, bad flags, exit code 2/126/127, `unexpected argument`. These will never resolve by retrying.
- **Transient error patterns**: rate limits (429), overloaded (529), timeouts. These may resolve for the next runner or after a delay.
- The codex backend flags were broken (deprecated `--approval-mode`) and the copilot backend misused `-p -` (literal "-" as prompt, ignoring stdin). Task .8 fixes both. If the suite encounters a `CLIPermanentError` from codex or copilot, that's a permanent error for that specific runner but doesn't affect the claude runner -- suite should continue to remaining runners.
## Acceptance
- [ ] `ConsecutiveFailureTracker` class exists in `_common.py` (or wherever .8 placed it)
- [ ] All 4 runners create a tracker and wire it into the main case loop
- [ ] 3 consecutive same-error failures trigger early abort (not 73)
- [ ] Tracker resets at start of each `--runs` iteration
- [ ] Successful cases reset the consecutive counter
- [ ] `FAIL_FAST=0|1` emitted on stdout by all 4 runners
- [ ] `FAIL_FAST_REASON=<fingerprint>` emitted when FAIL_FAST=1
- [ ] FAIL_FAST=1 implies ABORTED=1
- [ ] Results JSON `meta` includes `fail_fast_reason` when applicable
- [ ] Partial results written on abort (existing behavior preserved)
- [ ] `run_suite.sh` parses FAIL_FAST from each runner
- [ ] Suite skips remaining runners on permanent fail-fast
- [ ] Suite continues on transient fail-fast
- [ ] All cost/call variables initialized to "0" (no float("") crash on skipped runners)
- [ ] `config.yaml` has `fail_fast` section with backward-compatible defaults
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
- [ ] `./tests/evals/run_suite.sh --dry-run` still works
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
## Done summary
Added ConsecutiveFailureTracker to _common.py and wired fail-fast behavior into all 4 eval runners (activation, confusion_matrix, effectiveness, size_impact) and run_suite.sh. Runners emit FAIL_FAST/FAIL_FAST_REASON/FAIL_FAST_PERMANENT on stdout; suite uses FAIL_FAST_PERMANENT for robust permanent/transient classification with regex fallback. Restructured effectiveness and size_impact loop order so run_idx is outermost for proper tracker.reset() at --runs boundaries.
## Evidence
- Commits: 4807a4d, 9b9166c, bf717bf, 54170cf
- Tests: python3 -c 'import py_compile; ...' (all 5 Python files), python3 tests/evals/run_activation.py --dry-run, python3 tests/evals/run_confusion_matrix.py --dry-run, python3 tests/evals/run_effectiveness.py --dry-run, python3 tests/evals/run_size_impact.py --dry-run, bash tests/evals/run_suite.sh --dry-run, ConsecutiveFailureTracker unit tests, retry_with_backoff calls_consumed tests, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: