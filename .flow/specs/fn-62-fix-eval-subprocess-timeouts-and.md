# Fix eval subprocess timeouts and process cleanup

## Overview

Eval tests hang indefinitely because `subprocess.run(timeout=120)` kills only the direct child PID — not the process group. The `claude` CLI is a Node.js app that spawns child processes; those orphans survive SIGKILL and keep pipes open. Combined with no per-runner wall-clock cap and hardcoded timeouts, a single hanging case can block for 8+ minutes (4 attempts x 120s) before the consecutive-failure tracker kicks in.

## Scope

- Fix process tree cleanup in `_execute_cli()` using `Popen` + `start_new_session=True` + `os.killpg()`
- Add `--max-turns 1` to `_build_cli_command()` with automatic feature detection (probe `claude -p --help` once, cache result)
- Add protective env vars (`DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`) to `_subprocess_env()`
- Make timeouts configurable in `config.yaml` with per-eval-type and judge overrides
- Add per-case wall-clock budget in retry layer (stops retries once budget exceeded, regardless of remaining attempts)
- Add per-runner wall-clock timeout in `run_suite.sh` with macOS shim that normalizes exit codes to 124
- Reduce default per-case timeout from 120s to 15s (activation/confusion) and 45s (effectiveness/size_impact/judge)

## Out of scope

- Agent SDK migration (replaces subprocess management entirely — separate effort)
- Eval case content changes (handled by fn-60)
- CI pipeline integration (handled by fn-58)
- Probe hardening (`_detect_cli_caps` probes use 15s timeouts and are acceptable risk — they run once per suite)

## Quick commands

```bash
# Run activation eval with --limit to test timeout behavior
python3 tests/evals/run_activation.py --limit 3

# Full suite with bounded execution
./tests/evals/run_suite.sh --runs 1 --limit 5
```

## Acceptance

- [ ] No single eval case exceeds its per-case wall-clock budget (activation/confusion: 60s, effectiveness/size_impact: 120s) — enforced by retry layer, not just per-attempt timeout
- [ ] No orphaned `claude`/`node` processes after a timed-out case — verified by checking process group is fully reaped
- [ ] `config.yaml` has a `timeouts` section with per-type values including judge calls
- [ ] `run_suite.sh` has per-runner wall-clock timeout (works on both Linux and macOS with exit code 124 normalization)
- [ ] All existing eval tests still pass with the new timeout values
- [ ] Timeout exception message is stable (`"claude CLI timed out"`) for fail-fast fingerprinting — duration logged separately
- [ ] `--max-turns 1` added via automatic feature detection (graceful fallback if flag unsupported)
- [ ] `ProcessLookupError` handled in kill paths; pipes drained in all transport branches

## References

- `tests/evals/_common.py` — `_execute_cli()` L573-663, `_build_cli_command()` L504-544, `_subprocess_env()` L196-215
- `tests/evals/run_suite.sh` — `run_runner()` L150-194
- `tests/evals/config.yaml` — no `timeouts` section currently
- `tests/evals/run_activation.py`, `run_confusion_matrix.py`, `run_effectiveness.py`, `run_size_impact.py`, `judge_prompt.py` — all `call_model()` call sites
- CPython: `subprocess.run` timeout calls `os.kill(pid, SIGKILL)` — does NOT call `os.killpg()`
- anthropics/claude-code#26009, #26224 — known CLI hanging issues
- cc-plugin-eval: two-tier timeout pattern (interrupt_first + hard abort)
