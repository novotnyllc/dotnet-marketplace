# fn-60.7 Replace SDK API layer with CLI-based invocations

## Description

The eval runners currently use the Anthropic Python SDK (`anthropic.Anthropic().messages.create(...)`) for all LLM calls. This requires `ANTHROPIC_API_KEY` and does NOT reflect what actual coding clients do. The CLI clients (`claude`, `codex`, `copilot`) are already authenticated locally -- use them directly via subprocess.

This task replaces the entire SDK-based API layer with CLI subprocess invocations. All 4 runners and the shared judge module must be updated.

**Depends on:** (none -- this is the first task to execute)
**Size:** L
**Files:**
- `tests/evals/_common.py` -- replace `get_client()` with `call_model()` CLI wrapper; remove `anthropic` import
- `tests/evals/run_activation.py` -- replace `client.messages.create()` calls with `call_model()`; add `--cli` flag
- `tests/evals/run_confusion_matrix.py` -- replace `client.messages.create()` calls with `call_model()`; add `--cli` flag
- `tests/evals/run_effectiveness.py` -- replace `client.messages.create()` calls with `call_model()`; add `--cli` flag
- `tests/evals/run_size_impact.py` -- replace `client.messages.create()` calls with `call_model()`; add `--cli` flag
- `tests/evals/judge_prompt.py` -- replace `client.messages.create()` in `invoke_judge()` with `call_model()`
- `tests/evals/config.yaml` -- add `cli` section with per-backend model names; add `cost.max_calls_per_run`; remove `ANTHROPIC_API_KEY` references
- `tests/evals/requirements.txt` -- remove `anthropic` (keep `pyyaml`)
- `tests/evals/run_suite.sh` -- remove `ANTHROPIC_API_KEY` check; parse stable machine-parseable keys instead of regexing prose

## Approach

### New `call_model()` function in `_common.py`

Replace `get_client()` with a `call_model()` function:

```python
def call_model(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    cli: Optional[str] = None,
) -> dict:
    """Call an LLM via CLI subprocess.

    Returns:
        {"text": str, "cost": float, "input_tokens": int, "output_tokens": int, "calls": 1}
        cost/token fields are 0 if not available from the CLI output.
        calls is always 1 (used for call-count-based abort logic).
    """
```

### CLI capability detection

On first invocation per backend, `call_model()` performs a lightweight capability check:
1. Verify the configured CLI tool is in PATH (`shutil.which()`)
2. Probe capabilities with a trivial prompt for **each backend** (not just claude):
   - **`claude`**: probe `--output-format json` and stdin piping (`-p` without inline arg, prompt via stdin)
   - **`codex`**: probe stdin piping (prompt via stdin to `-q -`)
   - **`copilot`**: probe stdin piping (prompt via stdin to `-p -`)
   - For each backend, determine `prompt_mode`: stdin > file > arg (try in order, cache first working mode)
3. Cache results in a module-level `_cli_caps` dict so detection runs only once per process per backend. Cache keys: `{cli_name}.json_output`, `{cli_name}.prompt_mode` (stdin | file | arg).

If detection fails:
- Emit a one-time actionable diagnostic to stderr with the specific failing capability and remediation steps (e.g., "WARNING: claude CLI does not support --output-format json. Falling back to text mode. Upgrade claude or set cli.default: codex in config.yaml")
- Fall back gracefully: text-only mode (no JSON parsing, cost/usage = 0), arg-based prompt passing

### Implementation per CLI tool

**System prompt transport**: L3/L4 system prompts embed the routing index (~10-15k chars), which exceeds safe CLI argument limits. Strategy:
- When `len(system_prompt) <= 4000`: pass as `--system-prompt "..."` CLI argument (optimization for short prompts)
- When `len(system_prompt) > 4000`: combine into a single stdin payload: `combined = system_prompt + "\n\n---\n\n" + user_prompt`, omit `--system-prompt` flag
- This applies uniformly to ALL backends (claude, codex, copilot)

**`claude` (primary)**:
```bash
# Short system prompt:
claude -p --system-prompt "SYSTEM_PROMPT" --model MODEL \
  --output-format json --tools "" --no-session-persistence \
  --disable-slash-commands --max-turns 1
# Long system prompt (>4k chars): omit --system-prompt, combine into stdin
claude -p --model MODEL --output-format json --tools "" \
  --no-session-persistence --disable-slash-commands --max-turns 1
```
- Pass prompt (user or combined) via **stdin pipe** (`input=prompt` in `subprocess.run()`) -- preferred mode if capability detection confirms stdin works
- Fall back to temp-file-fed-stdin if direct stdin piping is not supported (see capability detection)
- `--tools ""` disables tool use (pure text generation)
- `--output-format json` returns structured JSON with response and usage
- `--max-turns 1` prevents multi-turn loops
- `--no-session-persistence` prevents session state from accumulating
- `--disable-slash-commands` prevents skill loading during eval
- Parse response text from JSON output using multi-shape detection:
  - Shape A: `{"result": "...", "usage": {...}}` (current claude CLI format)
  - Shape B: `{"content": [{"text": "..."}], "usage": {...}}` (API-like format)
  - Shape C: `{"completion": "..."}` (legacy format)
  - Unknown shape: fall back to **raw stdout as text**, emit one-time warning with top-level keys encountered (e.g., "WARNING: Unknown claude JSON shape, keys: ['foo', 'bar']. Using raw output as text.")
- Extract usage/cost fields from whichever shape matches; default to 0 if not found
- Fallback: if JSON mode unavailable, capture stdout as plain text

**`codex`**:
```bash
echo "SYSTEM_CONTEXT\n\nUSER_PROMPT" | codex --approval-mode full-auto -m MODEL -q -
```
- No `--system-prompt` flag -- prepend system prompt to user message
- Model names differ (e.g., `o3`, `o4-mini`)
- Prompt transport: prefer **stdin pipe** (same as claude) to avoid arg length limits; fall back to temp file if stdin not accepted. Capability detection probes codex stdin support on first call.

**`copilot`**:
```bash
echo "SYSTEM_CONTEXT\n\nUSER_PROMPT" | copilot -p -
```
- No `--system-prompt` flag -- prepend system prompt to user message
- Uses its own model selection
- Prompt transport: prefer **stdin pipe**; fall back to temp file. Capability detection probes copilot stdin support on first call.

### Config changes

```yaml
# config.yaml
cli:
  default: claude           # which CLI tool to use (claude | codex | copilot)
  claude:
    model: haiku            # CLI-native model string (not SDK model ID)
  codex:
    model: o4-mini          # codex model name
  copilot:
    model: null             # copilot picks its own model

cost:
  max_cost_per_run: 5.00    # dollar-based cap (effective when CLI reports cost)
  max_calls_per_run: 500    # call-count cap (always effective; safety net when cost unavailable)
```

**Config contract**: `cli.default` selects the backend. Per-backend `model` is a CLI-native string. `build_run_metadata()` stores `cli.default` as `backend` and the resolved model string as `model` in result envelopes. This keeps metadata meaningful and stable for baselines/compare.

### Runner changes

Each runner's `main()` function currently does:
```python
client = _common.get_client()
# ... then later:
response = client.messages.create(model=..., system=..., messages=[...])
text = response.content[0].text
```

Replace with:
```python
result = _common.call_model(system_prompt=..., user_prompt=..., model=...)
text = result["text"]
```

All `client.messages.create()` call sites across the 4 runners and judge_prompt.py must be updated. Remove the `client` variable entirely. Verify completeness via grep: no remaining `client.messages.create` or `anthropic` imports anywhere under `tests/evals/`.

### `--cli` flag on all runners

All 4 runners get a new `--cli {claude,codex,copilot}` argparse flag that overrides `config.yaml:cli.default` for that run. The flag is passed through to `call_model()`.

### run_suite.sh changes

- Remove the `ANTHROPIC_API_KEY` check block (lines 47-53)
- Remove `ANTHROPIC_API_KEY` from the usage comment
- Parse stable machine-parseable keys from runner stdout: `TOTAL_CALLS=`, `COST_USD=`, `ABORTED=`, `N_CASES=`
- Replace prose-regex cost extraction with key-based parsing

### Runner output contract

Each runner prints these keys to **stdout** (not stderr) as the last output before exiting:
```
TOTAL_CALLS=<int>
COST_USD=<float>
ABORTED=0|1
N_CASES=<int>
```

All other runner output (progress, diagnostics, per-skill details) goes to **stderr**. `run_suite.sh` captures stdout to parse the key-value lines and captures stderr separately for logging. This avoids mixing parseable keys with prose output.

### Dual abort mechanism

Runners enforce **(cost OR call-count) caps**, whichever triggers first:
- `call_model()` returns `calls=1`; runners increment a shared `total_calls` counter
- Before each call: check `total_calls >= max_calls_per_run` OR `total_cost >= max_cost_per_run`
- If either triggers: write partial results, print `ABORTED=1`, exit 0

### Prompt passing strategy (uniform across backends)

Large prompts (routing indices, skill bodies) can exceed shell argument limits. `call_model()` uses a **uniform prompt transport strategy** across ALL backends:

1. **Prefer stdin pipe** (`input=combined_prompt` in `subprocess.run()`) -- probed per-backend during capability detection
2. **Fall back to temp-file-fed-stdin** if direct stdin piping fails -- write prompt to `tempfile.NamedTemporaryFile`, then `open()` and pass file object as `stdin` to `subprocess.run()`. This is internal plumbing; the CLI still sees stdin, not a file path argument. Clean up temp file after.
3. **Last resort: positional arg** -- only for very short prompts (<4k chars) where the backend accepts inline args

Note: "temp file fallback" does NOT mean passing a file path as a CLI argument (most CLIs don't support that). It means using a temp file as an intermediary to feed stdin reliably.

The transport mode is cached per-backend in `_cli_caps[backend].prompt_mode` (stdin | file_stdin | arg).

Example (claude, stdin mode):
```python
proc = subprocess.run(
    ["claude", "-p", "--model", model,
     "--output-format", "json", "--tools", "", "--no-session-persistence",
     "--disable-slash-commands", "--max-turns", "1"],
    input=combined_prompt, capture_output=True, text=True, timeout=120,
)
```

### Cache key updates

Effectiveness and size-impact runners use cache keys to avoid redundant generations. Cache keys currently hash `model` but not the CLI backend. Update `_prompt_hash()` and `_condition_hash()` to incorporate `cli_backend + resolved_model_string` (even if model is None) so caches are backend-stable and cannot be polluted across different CLI tools.

### Retry logic

Keep `retry_with_backoff()` but adapt it to handle subprocess failures (non-zero exit codes, timeouts) instead of SDK exceptions.

### Cost tracking

- `COST_USD` is **CLI-reported** when available (e.g., `claude --output-format json` includes usage metadata), otherwise 0
- For `codex`/`copilot` and `claude` text-fallback: cost = 0, tokens = 0
- `track_cost()` in `_common.py`: update to accept CLI-reported cost directly instead of estimating from SDK model IDs. If CLI reports cost, use it. If not, `COST_USD=0.0` and the call-count cap provides safety. Remove any SDK-model-ID-based estimation tables that would produce misleading numbers with CLI model strings like `haiku` or `o4-mini`.
- Retain `max_cost_per_run` safety cap alongside `max_calls_per_run`

### Schema invariants

**Critical**: The result envelope `summary` shape for all 4 eval types MUST remain unchanged after migration. `compare_baseline.py` depends on specific scalar keys per eval type. Pinned per-type contracts:

- **L3 Activation**: `summary._overall` contains `tpr`, `fpr`, `accuracy`, `n`, `tpr_stats`, `fpr_stats`, `accuracy_stats`, `true_positives`
- **L4 Confusion**: `summary[group]` contains `accuracy`, `cross_activation_rate`, `n`, `accuracy_stats`, `cross_activation_stats`, `multi_activation_count`, `no_activation_count`, `total_cases`; `summary._negative_controls` contains `pass_rate`, `passed`, `failed`, `n`
- **L5 Effectiveness**: `summary[skill]` contains `mean`, `stddev`, `n`, `wins_enhanced`, `wins_baseline`, `ties`, `errors`, `total_cases`, `win_rate` (note: keys are `wins_enhanced`/`wins_baseline`, NOT `wins`/`losses`)
- **L6 Size Impact**: `summary[candidate]` contains `size_tier`, `body_bytes`, `full_bytes`, `full_tokens_estimated`, `summary_bytes`, `summary_tokens_estimated`, `mean`, `stddev`, `n`, `errors` (flat scalars for `compare_baseline.py`) AND `comparisons` dict with per-comparison-type entries (e.g., `full_vs_baseline`) each containing `mean`, `stddev`, `n`, `wins_full`, `wins_baseline`, `ties` (richer block for quality-bar validation). Both must be present.

Verify by running `compare_baseline.py` after migration against a pre-migration result file. If any key is missing or renamed, the migration is incomplete.

### Skill restore strategy

Unchanged from original .7 spec -- git-based restore mechanism remains valid.

## Acceptance
- [ ] `get_client()` removed from `_common.py`; replaced with `call_model()` CLI wrapper
- [ ] No remaining `client.messages.create` calls anywhere under `tests/evals/` (verify: `grep -r "client.messages.create" tests/evals/` returns nothing)
- [ ] No remaining `anthropic` imports anywhere under `tests/evals/` (verify: `grep -r "import anthropic\|from anthropic" tests/evals/` returns nothing)
- [ ] `anthropic` removed from `requirements.txt`
- [ ] `config.yaml` has `cli` section with per-backend model names; has `cost.max_calls_per_run`; no `ANTHROPIC_API_KEY` references anywhere in `tests/evals/`
- [ ] `run_suite.sh` has no `ANTHROPIC_API_KEY` check; parses `TOTAL_CALLS=`/`COST_USD=`/`ABORTED=`/`N_CASES=` keys
- [ ] All 4 runners accept `--cli {claude,codex,copilot}` override flag
- [ ] `call_model()` performs one-time per-backend capability detection (JSON output + prompt transport: stdin/file/arg) with actionable diagnostics on failure
- [ ] Prompt transport is uniform across backends (stdin preferred, file fallback, arg last resort) -- not just claude
- [ ] `call_model()` parses multiple known JSON shapes with fallback to raw stdout + warning on unknown shape
- [ ] Cache keys in effectiveness/size-impact runners incorporate CLI backend + resolved model string
- [ ] `call_model()` works with `claude` CLI (primary path -- must work)
- [ ] `call_model()` works with `codex` CLI (secondary path)
- [ ] `call_model()` works with `copilot` CLI (secondary path)
- [ ] Dual abort: both cost-based and call-count-based caps enforced
- [ ] `track_cost()` uses CLI-reported cost (not SDK model ID estimation); `COST_USD=0.0` when cost unavailable
- [ ] Runners emit `TOTAL_CALLS=`/`COST_USD=`/`ABORTED=`/`N_CASES=` on stdout
- [ ] Result envelope `summary` schema unchanged for all 4 eval types (verify with `compare_baseline.py`)
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
- [ ] Large system prompts (L3/L4 routing index, ~10-15k chars) pass through without arg-length failures
- [ ] `python3 tests/evals/run_activation.py --skill dotnet-xunit` completes one real CLI call successfully (exercises index-sized system prompt)
- [ ] `python3 tests/evals/run_confusion_matrix.py --group testing --dry-run` works (verifies confusion index assembly)
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass

## Done summary
Replaced the entire Anthropic SDK API layer with CLI-based subprocess invocations (claude/codex/copilot) across all 4 eval runners, judge module, and shared infrastructure. Added per-backend capability detection with actionable diagnostics, dual abort mechanism (cost + call-count caps), machine-parseable runner output contract, non-retryable CLIConfigError for deterministic failures, and accurate call-count tracking through retry failures.
## Evidence
- Commits: 562a7b0ccc5a54cab643b8c1d9bb707b6b2882d6, bbbfcbc, adf46c9, 0891e39, 820fb80, 4576405, fc99de1, 9843bdd
- Tests: python3 tests/evals/run_activation.py --dry-run, python3 tests/evals/run_confusion_matrix.py --group testing --dry-run, python3 tests/evals/run_effectiveness.py --dry-run, python3 tests/evals/run_size_impact.py --dry-run, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, grep -r client.messages.create tests/evals/, grep -r 'import anthropic' tests/evals/, grep -r ANTHROPIC_API_KEY tests/evals/
- PRs: