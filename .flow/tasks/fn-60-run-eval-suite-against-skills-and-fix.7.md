# fn-60.7 Replace SDK API layer with CLI-based invocations

## Description

The eval runners currently use the Anthropic Python SDK (`anthropic.Anthropic().messages.create(...)`) for all LLM calls. This requires `ANTHROPIC_API_KEY` and does NOT reflect what actual coding clients do. The CLI clients (`claude`, `codex`, `copilot`) are already authenticated locally -- use them directly via subprocess.

This task replaces the entire SDK-based API layer with CLI subprocess invocations. All 4 runners and the shared judge module must be updated.

**Size:** L
**Files:**
- `tests/evals/_common.py` -- replace `get_client()` with `call_model()` CLI wrapper; remove `anthropic` import
- `tests/evals/run_activation.py` -- replace `client.messages.create()` calls with `call_model()`
- `tests/evals/run_confusion_matrix.py` -- replace `client.messages.create()` calls with `call_model()`
- `tests/evals/run_effectiveness.py` -- replace `client.messages.create()` calls with `call_model()`
- `tests/evals/run_size_impact.py` -- replace `client.messages.create()` calls with `call_model()`
- `tests/evals/judge_prompt.py` -- replace `client.messages.create()` in `invoke_judge()` with `call_model()`
- `tests/evals/config.yaml` -- add `cli` section; remove `ANTHROPIC_API_KEY` references
- `tests/evals/requirements.txt` -- remove `anthropic` (keep `pyyaml`)
- `tests/evals/run_suite.sh` -- remove `ANTHROPIC_API_KEY` check

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
        {"text": str, "cost": float, "input_tokens": int, "output_tokens": int}
        cost/token fields are 0 if not available from the CLI output.
    """
```

Implementation per CLI tool:

**`claude` (primary)**:
```bash
claude -p "USER_PROMPT" \
  --system-prompt "SYSTEM_PROMPT" \
  --model MODEL \
  --output-format json \
  --tools "" \
  --no-session-persistence \
  --disable-slash-commands
```
- `--tools ""` disables tool use (pure text generation)
- `--output-format json` returns structured JSON with response and usage
- `--no-session-persistence` prevents session state from accumulating
- `--disable-slash-commands` prevents skill loading during eval
- Parse response text and usage from JSON output
- Pass prompt via stdin (pipe) to avoid shell escaping issues with large prompts

**`codex`**:
```bash
codex exec "SYSTEM_CONTEXT\n\nUSER_PROMPT" -m MODEL
```
- No `--system-prompt` flag -- prepend system prompt to user message
- Model names differ (e.g., `o3`, `o4-mini`)

**`copilot`**:
```bash
copilot -p "SYSTEM_CONTEXT\n\nUSER_PROMPT"
```
- No `--system-prompt` flag -- prepend system prompt to user message
- Uses its own model selection

### Config changes

```yaml
# config.yaml
cli:
  default: claude           # which CLI tool to use (claude | codex | copilot)
  claude:
    model: haiku            # claude model alias
  codex:
    model: o4-mini          # codex model name
  copilot:
    model: null             # copilot picks its own model

# Remove these:
# models:
#   generation_model: claude-haiku-4-20250514
#   judge_model: claude-haiku-4-20250514
# Environment variable overrides: ANTHROPIC_API_KEY...
```

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

All 8 `client.messages.create()` call sites across the 4 runners and judge_prompt.py must be updated. Remove the `client` variable entirely.

### run_suite.sh changes

Remove the `ANTHROPIC_API_KEY` check block (lines 47-53). Remove `ANTHROPIC_API_KEY` from the usage comment. The suite just runs -- CLI clients handle their own auth.

### Prompt passing strategy

Large prompts (routing indices, skill bodies) can exceed shell argument limits. Pass prompts via **stdin pipe** to avoid escaping/length issues:
```python
proc = subprocess.run(
    ["claude", "-p", "--system-prompt", system_prompt, "--model", model,
     "--output-format", "json", "--tools", "", "--no-session-persistence",
     "--disable-slash-commands"],
    input=user_prompt, capture_output=True, text=True, timeout=120,
)
```

### Retry logic

Keep `retry_with_backoff()` but adapt it to handle subprocess failures (non-zero exit codes, timeouts) instead of SDK exceptions.

### Cost tracking

- For `claude --output-format json`: parse usage metadata from JSON output if available
- For other CLIs: set cost/token fields to 0
- Retain `max_cost_per_run` safety cap; if cost data is unavailable, fall back to call-count-based limit (`max_calls_per_run`)

### Skill restore strategy

Unchanged from original .7 spec -- git-based restore mechanism remains valid.

## Acceptance
- [ ] `get_client()` removed from `_common.py`; replaced with `call_model()` CLI wrapper
- [ ] All 8 `client.messages.create()` call sites replaced across runners and judge_prompt.py
- [ ] `anthropic` removed from `requirements.txt`
- [ ] No remaining imports of `anthropic` in any eval file
- [ ] `config.yaml` has `cli` section; no `ANTHROPIC_API_KEY` references anywhere in `tests/evals/`
- [ ] `run_suite.sh` has no `ANTHROPIC_API_KEY` check
- [ ] `call_model()` works with `claude` CLI (primary path -- must work)
- [ ] `call_model()` works with `codex` CLI (secondary path)
- [ ] `call_model()` works with `copilot` CLI (secondary path)
- [ ] `python3 tests/evals/run_activation.py --dry-run` still works
- [ ] `python3 tests/evals/run_activation.py --skill dotnet-xunit` completes one real CLI call successfully
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
