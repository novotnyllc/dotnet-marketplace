# fn-60-run-eval-suite-against-skills-and-fix.8 Fix CLI probe and transport reliability

## Description

The CLI probe and transport mechanism in `_common.py` has 5 bugs that caused 8 out of 12 Ralph run attempts to fail with 100% error rate (73/73 cases):

1. **Probe failure permanently degrades to arg mode** (lines 174, 259-277): When both stdin and file_stdin probes fail (even transiently), `prompt_mode` defaults to `"arg"` and gets cached forever. For claude, the code only emits a warning instead of raising an error. Arg mode has a 4k char limit but eval prompts are 15.7k chars = guaranteed 100% failure.

2. **No probe retry** (lines 235-245): Each transport mode is probed exactly once. A single transient failure (rate limit, slow startup, temp auth issue) permanently disables that mode.

3. **Auth/permanent errors not classified** (lines 518-522): When `_execute_cli()` gets a non-zero exit code, it always raises generic `RuntimeError`. `retry_with_backoff` then retries 3 times. For permanent errors (auth failure, bad flags), this wastes time and never succeeds. The error propagates to the runner loop which records it and moves to the next case -- where the same permanent error recurs.

4. **Codex backend uses wrong command entirely** (lines 188-191, 428-431): The code uses `codex --approval-mode full-auto -m MODEL -q -`. The non-interactive mode is `codex exec`, not `codex` with root-level flags. `--approval-mode` and `-q` don't exist. Any codex invocation immediately fails with exit code 2.

5. **Copilot backend misuses `-p -`** (lines 195, 432-434): The code uses `["copilot", "-p", "-"]` assuming `-` means "read from stdin". It doesn't -- copilot treats `-` as the literal prompt text. The actual stdin content is silently ignored. Also missing required subprocess flags (`-s`, `--no-color`, `--allow-all-tools`, `--no-custom-instructions`).

**Size:** M
**Files:**
- `tests/evals/_common.py` -- probe logic, transport, error classification, codex flags
- `tests/evals/config.yaml` -- probe config

## Authoritative CLI reference (from research)

### Claude CLI (`claude -p`)
- **stdin**: Fully supported. `echo "prompt" | claude -p` is the documented usage mode.
- **Flags used by eval code**: `--model`, `--system-prompt`, `--output-format json`, `--no-session-persistence`, `--disable-slash-commands`, `--tools ""` -- all confirmed valid.
- **JSON output schema**: `{"type": "result", "subtype": "success", "result": "...", "total_cost_usd": 0.42, "usage": {"input_tokens": N, "output_tokens": N}}` -- the `_parse_cli_output()` code handles this correctly.
- **Exit codes**: 0 = success, 1 = error. stderr contains the error message.
- **Known issue**: Large stdin inputs (>7000 chars) may produce empty output with exit code 0 (GitHub issue #7263). Eval prompts are ~15.7k chars. If this manifests, the workaround is writing the prompt to a temp file and using file_stdin mode. Monitor for this but don't preemptively switch -- stdin works for the majority of cases in our successful runs.
- **No TTY required**: Works in non-interactive subprocess context.

### Codex CLI (`codex exec`)
- **BROKEN in current eval code**: `_build_transport_probe_cmd()` at line 188 uses `["codex", "--approval-mode", "full-auto", "-m", MODEL, "-q", "-"]`. The non-interactive command is `codex exec`, not `codex` with root flags. `--approval-mode` doesn't exist (it's `-a`). `-q` doesn't exist at all. Immediate exit code 2.
- **Correct non-interactive command**: `codex exec --full-auto --ephemeral -C /tmp -m MODEL -` where `-` means read prompt from stdin. Confirmed by live test: returns "OK" with exit code 0.
- **`--full-auto`**: Convenience alias for `-a on-request --sandbox workspace-write`. Only available on `exec` subcommand.
- **`--ephemeral`**: Don't persist session files (important for eval subprocess).
- **`-C /tmp`**: Set working directory (prevents loading project context, like `_SUBPROCESS_CWD`).
- **`--json`**: Outputs JSONL events. `turn.completed` includes `usage` with `input_tokens`, `cached_input_tokens`, `output_tokens`. No `cost_usd`. Agent message in `item.completed` with `type: "agent_message"`.
- **`-o FILE`**: Write last agent message to file (alternative to parsing stdout).
- **stdin**: `-` as the prompt argument reads from stdin. This is documented in `codex exec --help`: "If not provided as an argument (or if `-` is used), instructions are read from stdin".
- **Model selection**: `-m MODEL` (works on `exec` subcommand).
- **Exit codes**: 0 = success, 2 = argument error, 1 = runtime error.
- **No `-q` flag**: Does not exist. Use `--json` for structured output or `-o FILE` for clean text output.
- **Impact**: Any test using `cli.default: codex` will fail immediately with exit code 2.
- **Action**: Rewrite codex commands to use `codex exec` subcommand with correct flags.

### Copilot CLI (`copilot`)
- **BROKEN in current eval code**: `_build_transport_probe_cmd()` at line 195 and `_build_cli_command()` at line 434 both use `["copilot", "-p", "-"]`. The `-` is treated as the **literal prompt text** (the string "-"), not as a "read from stdin" convention. Stdin content is completely ignored.
- **stdin**: Fully supported since v0.0.414+. Copilot auto-detects stdin pipe when no `-p` flag is present. Confirmed by live test: `echo "Reply with exactly: OK" | copilot -s --no-color --allow-all-tools --no-custom-instructions` returns "OK" with exit code 0.
- **Binary**: Standalone `/opt/homebrew/bin/copilot` (via `brew install copilot-cli`). Also available as `gh copilot` wrapper. Current version: 0.0.415.
- **Required flags for subprocess use**: `-s` (silent, clean stdout only), `--no-color` (no ANSI), `--allow-all-tools` (non-interactive tool approval), `--no-custom-instructions` (skip AGENTS.md loading).
- **Model selection**: `--model <choice>` with enumerated values (claude-sonnet-4.6, gpt-5.3-codex, etc.). Config has `copilot.model: null` which uses default.
- **No JSON output mode**: Correctly detected as unavailable by current code. Output is plain text via stdout (with `-s`).
- **No `--system-prompt` flag**: Correctly handled by combining system+user into single payload for non-claude backends (line 383).
- **Exit codes**: 0 = success, 1 = error. Error messages in stderr.
- **Cost tracking**: Reports "Premium requests" not USD. `cost` field will be 0.0 for copilot.
- **Action**: Fix copilot command in both `_build_transport_probe_cmd()` and `_build_cli_command()`. Remove `-p -`, add `-s --no-color --allow-all-tools --no-custom-instructions`.

## Approach

### Fix 1: Remove transport probing for claude, hardcode stdin

The claude CLI supports stdin piping. This is the documented usage mode for `claude -p`. The probe mechanism was overengineered -- it tested "Reply with exactly: OK" and required exit code 0 + "OK" in stdout, which can fail for any transient reason.

**Replace the probe cascade for claude with a direct stdin default.** In `_detect_cli_caps()`:
- If `backend == "claude"`: set `prompt_mode = "stdin"` directly. Skip transport probing entirely.
- Keep probing for `codex` and `copilot` (less certain about their stdin support).
- Still probe JSON output support for claude (the `--output-format json` probe is independent and useful). Use the hardcoded stdin mode for this probe rather than the probed transport mode -- this avoids the current chicken-and-egg problem where a transport probe failure prevents the JSON probe from running (line 285: `if backend == "claude" and prompt_mode != "arg"`).

### Fix 2: Kill arg mode fallback for claude

After fixing the probe, arg mode should never be reached for claude. But as a safety net: if `prompt_mode` is somehow still `"arg"` for claude, raise `CLIConfigError` immediately (matching what codex/copilot already do at line 261-272) instead of silently degrading with a warning.

Currently (line 259-277):
- codex/copilot: raise `CLIConfigError` -- correct
- claude: emit warning, continue with arg mode -- wrong

Change claude to also raise `CLIConfigError`. Arg mode with a 4k limit is useless for eval prompts and only delays the inevitable failure.

### Fix 3: Add error classification to `_execute_cli()`

Before raising `RuntimeError` at line 521, classify the error by parsing `proc.stderr` and `proc.returncode`:

Add `CLIPermanentError(CLIConfigError)` -- a new exception subclass for permanent runtime errors (auth, bad flags). Since it extends `CLIConfigError`, `retry_with_backoff` automatically skips retries (line 688-691). Zero changes needed to `retry_with_backoff`.

Classification logic in `_execute_cli()` at the non-zero-exit-code path:
- Exit code 126 (permission denied) or 127 (command not found): raise `CLIPermanentError`
- Exit code 2 (argument parsing error, e.g. codex deprecated flags): raise `CLIPermanentError`
- Stderr matches permanent patterns (`authentication_error`, `Could not resolve authentication`, `401`, `permission_error`, `403`, `unknown option`, `invalid flag`, `unexpected argument`): raise `CLIPermanentError`
- Stderr matches retryable patterns (`overloaded_error`, `529`, `rate_limit`, `429`, `timeout`): raise `RuntimeError` (retries normally)
- Unknown: raise `RuntimeError` (default to retryable, conservative)

### Fix 4: Rewrite codex backend to use `codex exec`

In both `_build_transport_probe_cmd()` (line 188-191) and `_build_cli_command()` (line 428-431):
- Command base: `["codex", "exec", "--full-auto", "--ephemeral", "-C", "/tmp"]`
- Model: `-m MODEL` (same flag, works on `exec` subcommand)
- stdin: append `-` as the prompt argument (codex exec reads stdin when `-` is the prompt)
- Remove: `--approval-mode full-auto` (doesn't exist), `-q` (doesn't exist), bare `-` at end of root command

### Fix 5: Fix copilot backend flags

In both `_build_transport_probe_cmd()` (line 195) and `_build_cli_command()` (line 432-434):
- Remove `-p` and `-` entirely — copilot auto-detects stdin pipe
- Add `-s` (silent mode, clean stdout only)
- Add `--no-color` (prevent ANSI escape codes)
- Add `--allow-all-tools` (required for non-interactive execution)
- Add `--no-custom-instructions` (prevent loading AGENTS.md from cwd, matching claude's `--disable-slash-commands`)
- Model flag: `--model MODEL` (same syntax, already correct in config handling)

### Fix 6: Reduce probe timeout for codex/copilot

Change probe timeout from 120s to 15s in `_run_probe()` (lines 208, 226). Probes should fail fast. Keep production call timeout at 120s.

## Key context

- `CLIConfigError` at line 33-41 is already non-retryable in `retry_with_backoff` (line 688-691). Making `CLIPermanentError` a subclass means zero changes needed to `retry_with_backoff`.
- `_cli_caps` cache (line 116) persists for process lifetime. That's fine when the cached value is correct (stdin works). It was a problem when it cached a *wrong* value (arg mode from a failed probe).
- The probe at line 205 sends "Reply with exactly: OK" and checks for "OK" in stdout. This is brittle -- the claude CLI might wrap the response in JSON, add prefixes, etc. Removing the probe for claude eliminates this entire class of fragility.
- The codex breakage (wrong command entirely -- needs `codex exec`, not `codex` with non-existent flags) hasn't blocked Ralph runs because `config.yaml` defaults to `cli.default: claude`. But it makes the codex backend completely non-functional.
- The copilot `-p -` bug is similarly non-blocking (default is claude), but makes the copilot backend send a literal "-" as the prompt, ignoring the real prompt entirely.
- Both codex and copilot bugs were introduced when the backends were first written -- they were never tested with actual CLI invocations, only with the claude backend.
- The large stdin issue (GitHub #7263) was not observed in our 4 successful runs (15.7k chars via stdin, worked fine). Monitor but don't preemptively switch to file_stdin.
## Acceptance
- [ ] Claude backend skips transport probing -- stdin is the default, no probe needed
- [ ] Claude JSON output probe still runs (using stdin mode directly, not dependent on transport probe)
- [ ] codex/copilot still probe transport (existing behavior preserved)
- [ ] Claude raises `CLIConfigError` if prompt_mode is somehow `"arg"` (no silent arg fallback)
- [ ] `CLIPermanentError` class exists as subclass of `CLIConfigError`
- [ ] `_execute_cli()` classifies auth errors, bad flags, exit codes 2/126/127 as `CLIPermanentError`
- [ ] `_execute_cli()` classifies `unexpected argument` in stderr as `CLIPermanentError`
- [ ] `CLIPermanentError` is not retried by `retry_with_backoff` (inherits CLIConfigError behavior)
- [ ] Retryable errors (overloaded, rate limit, timeout) still raise `RuntimeError` and retry normally
- [ ] Codex rewritten to `codex exec --full-auto --ephemeral -C /tmp -m MODEL -` (not root `codex` command)
- [ ] Codex updated in both `_build_transport_probe_cmd()` and `_build_cli_command()`
- [ ] Copilot flags fixed: `-p -` removed, stdin auto-detected by copilot when piped
- [ ] Copilot has `-s --no-color --allow-all-tools --no-custom-instructions` for subprocess use
- [ ] Copilot flags updated in both `_build_transport_probe_cmd()` and `_build_cli_command()`
- [ ] Probe timeout reduced to 15s for codex/copilot probes
- [ ] Production call timeout unchanged at 120s
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
- [ ] `python3 tests/evals/run_activation.py --skill dotnet-xunit` completes one real CLI call
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
- [ ] No new external dependencies
## Done summary
TBD
## Evidence
- Commits:
- Tests:
- PRs: