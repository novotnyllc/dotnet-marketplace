"""Shared infrastructure for offline skill evaluation runners.

All eval runners import from this module. Provides config loading,
CLI-based model invocation, retry/backoff with jitter, cost
accounting, run_id/timestamps, JSON extraction from LLM responses,
output writing, and skill content loading with frontmatter stripping.

LLM calls are made via CLI subprocess (claude, codex, copilot) rather
than the Anthropic SDK. The CLI tools handle their own authentication.
"""

import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

EVALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVALS_DIR.parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CONFIG_PATH = EVALS_DIR / "config.yaml"

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_config_cache: Optional[dict] = None


def load_config(config_path: Optional[Path] = None) -> dict:
    """Load config.yaml and return the parsed dict.

    Returns:
        Parsed config dict.
    """
    global _config_cache
    path = config_path or CONFIG_PATH
    if _config_cache is not None and config_path is None:
        return _config_cache

    with open(path) as f:
        cfg = yaml.safe_load(f)

    if not isinstance(cfg, dict):
        raise ValueError(f"Invalid config at {path}: expected YAML mapping, got {type(cfg).__name__}")

    if config_path is None:
        _config_cache = cfg
    return cfg


# ---------------------------------------------------------------------------
# CLI capability detection
# ---------------------------------------------------------------------------

# Per-backend capability cache.  Keys: "{backend}.json_output",
# "{backend}.prompt_mode" (stdin | file_stdin | arg).
_cli_caps: dict[str, Any] = {}
_cli_warnings_emitted: set[str] = set()


def _emit_warning(key: str, message: str) -> None:
    """Emit a one-time warning to stderr, keyed to avoid duplicates."""
    if key not in _cli_warnings_emitted:
        _cli_warnings_emitted.add(key)
        print(f"WARNING: {message}", file=sys.stderr)


def _detect_cli_caps(backend: str) -> dict[str, Any]:
    """Detect CLI capabilities for a backend (once per process).

    Probes the CLI tool in order of preference:
    1. stdin piping
    2. file_stdin (write prompt to temp file, pipe as stdin)
    3. arg (append prompt as positional argument -- last resort)

    For claude, also probes --output-format json independently of
    the prompt transport mode.

    Returns:
        Dict with keys: json_output (bool), prompt_mode (str).
    """
    cache_prefix = backend
    json_key = f"{cache_prefix}.json_output"
    mode_key = f"{cache_prefix}.prompt_mode"

    if json_key in _cli_caps and mode_key in _cli_caps:
        return {"json_output": _cli_caps[json_key], "prompt_mode": _cli_caps[mode_key]}

    # Step 1: verify in PATH
    if shutil.which(backend) is None:
        _emit_warning(
            f"{backend}_not_found",
            f"{backend} CLI not found in PATH. Install it or set "
            f"cli.default to a different backend in config.yaml",
        )
        _cli_caps[json_key] = False
        _cli_caps[mode_key] = "arg"
        return {"json_output": False, "prompt_mode": "arg"}

    # Resolve configured model for probing (avoid hard-coding a model)
    cfg = load_config()
    cli_cfg = cfg.get("cli", {})
    probe_model = cli_cfg.get(backend, {}).get("model")

    # Step 2: probe prompt transport modes in preference order
    prompt_mode = "arg"  # ultimate fallback
    probe_stdout = ""

    def _build_probe_cmd(backend: str, probe_model: Any, use_json: bool) -> list[str]:
        if backend == "claude":
            cmd = ["claude", "-p"]
            if probe_model:
                cmd.extend(["--model", str(probe_model)])
            if use_json:
                cmd.extend(["--output-format", "json"])
            cmd.extend([
                "--tools", "",
                "--no-session-persistence",
                "--disable-slash-commands",
                "--max-turns", "1",
            ])
            return cmd
        elif backend == "codex":
            cmd = ["codex", "--approval-mode", "full-auto"]
            if probe_model:
                cmd.extend(["-m", str(probe_model)])
            cmd.extend(["-q", "-"])
            return cmd
        else:
            # copilot
            return ["copilot", "-p", "-"]

    # Try stdin first
    use_json_probe = backend == "claude"
    probe_cmd = _build_probe_cmd(backend, probe_model, use_json_probe)

    for mode in ("stdin", "file_stdin"):
        try:
            if mode == "stdin":
                proc = subprocess.run(
                    probe_cmd,
                    input="Reply with exactly: OK",
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            else:
                # file_stdin: write to temp file, pipe as stdin
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False, encoding="utf-8"
                ) as tf:
                    tf.write("Reply with exactly: OK")
                    tf_path = tf.name
                try:
                    with open(tf_path) as stdin_file:
                        proc = subprocess.run(
                            probe_cmd,
                            stdin=stdin_file,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )
                finally:
                    Path(tf_path).unlink(missing_ok=True)

            if proc.returncode == 0:
                prompt_mode = mode
                probe_stdout = proc.stdout or ""
                break
            else:
                stderr_preview = (proc.stderr or "")[:200]
                _emit_warning(
                    f"{backend}_probe_{mode}_fail",
                    f"{backend} probe failed in {mode} mode (rc={proc.returncode}): "
                    f"{stderr_preview}",
                )
        except (subprocess.TimeoutExpired, OSError):
            _emit_warning(
                f"{backend}_probe_{mode}_error",
                f"{backend} probe timed out or errored in {mode} mode",
            )

    # Step 3: JSON output support (claude only) -- check independently
    json_output = False
    if backend == "claude":
        if probe_stdout.strip():
            try:
                parsed = json.loads(probe_stdout)
                if isinstance(parsed, dict):
                    json_output = True
            except json.JSONDecodeError:
                pass

        if not json_output:
            _emit_warning(
                f"{backend}_no_json",
                "claude CLI does not support --output-format json or probe "
                "returned non-JSON. Falling back to text mode.",
            )

    _cli_caps[json_key] = json_output
    _cli_caps[mode_key] = prompt_mode

    return {"json_output": json_output, "prompt_mode": prompt_mode}


# ---------------------------------------------------------------------------
# CLI model invocation
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT_INLINE_LIMIT = 4000


def call_model(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    cli: Optional[str] = None,
) -> dict:
    """Call an LLM via CLI subprocess.

    Args:
        system_prompt: System prompt text.
        user_prompt: User prompt text.
        model: CLI-native model string override.
        max_tokens: Max tokens for generation.
        temperature: Sampling temperature.
        cli: CLI backend override (claude, codex, copilot).

    Returns:
        {"text": str, "cost": float, "input_tokens": int,
         "output_tokens": int, "calls": 1}
        cost/token fields are 0 if not available from the CLI output.
        calls is always 1 (used for call-count-based abort logic).
    """
    cfg = load_config()
    cli_cfg = cfg.get("cli", {})
    backend = cli or cli_cfg.get("default", "claude")

    # Resolve model
    if model is None:
        backend_cfg = cli_cfg.get(backend, {})
        model = backend_cfg.get("model")

    caps = _detect_cli_caps(backend)

    # Build the prompt payload
    # For large system prompts or non-claude backends: combine into single payload
    use_system_flag = (
        backend == "claude"
        and len(system_prompt) <= _SYSTEM_PROMPT_INLINE_LIMIT
    )

    if use_system_flag:
        combined_prompt = user_prompt
    else:
        combined_prompt = system_prompt + "\n\n---\n\n" + user_prompt

    # Build CLI command
    cmd = _build_cli_command(backend, model, max_tokens, temperature, caps, use_system_flag, system_prompt)

    # Execute via preferred prompt transport
    result = _execute_cli(cmd, combined_prompt, caps, backend)

    return result


def _build_cli_command(
    backend: str,
    model: Optional[str],
    max_tokens: int,
    temperature: float,
    caps: dict,
    use_system_flag: bool,
    system_prompt: str,
) -> list[str]:
    """Build the CLI command list for a given backend.

    Passes max_tokens and temperature to backends that support them.
    claude: --max-tokens flag supported.
    codex/copilot: best-effort; flags may be silently ignored if not
    supported by the CLI version.
    """
    if backend == "claude":
        cmd = ["claude", "-p"]
        if use_system_flag:
            cmd.extend(["--system-prompt", system_prompt])
        if model:
            cmd.extend(["--model", str(model)])
        if caps["json_output"]:
            cmd.extend(["--output-format", "json"])
        # Pass max_tokens to bound output length
        cmd.extend(["--max-tokens", str(max_tokens)])
        cmd.extend([
            "--tools", "",
            "--no-session-persistence",
            "--disable-slash-commands",
            "--max-turns", "1",
        ])
    elif backend == "codex":
        cmd = ["codex", "--approval-mode", "full-auto"]
        if model:
            cmd.extend(["-m", str(model)])
        cmd.extend(["-q", "-"])
    else:
        # copilot
        cmd = ["copilot", "-p", "-"]

    return cmd


def _execute_cli(
    cmd: list[str],
    prompt: str,
    caps: dict,
    backend: str,
) -> dict:
    """Execute CLI command with the appropriate prompt transport."""
    prompt_mode = caps.get("prompt_mode", "arg")
    result_default = {
        "text": "",
        "cost": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "calls": 1,
    }

    try:
        if prompt_mode == "stdin":
            proc = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120,
            )
        elif prompt_mode == "file_stdin":
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, encoding="utf-8"
            ) as tf:
                tf.write(prompt)
                tf_path = tf.name
            try:
                with open(tf_path) as stdin_file:
                    proc = subprocess.run(
                        cmd,
                        stdin=stdin_file,
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
            finally:
                Path(tf_path).unlink(missing_ok=True)
        else:
            # arg mode: append prompt as positional arg (short prompts only)
            proc = subprocess.run(
                cmd + [prompt[:_SYSTEM_PROMPT_INLINE_LIMIT]],
                capture_output=True,
                text=True,
                timeout=120,
            )
    except subprocess.TimeoutExpired:
        result_default["text"] = ""
        raise RuntimeError(f"{backend} CLI timed out after 120s")
    except OSError as exc:
        raise RuntimeError(f"{backend} CLI execution failed: {exc}")

    if proc.returncode != 0:
        stderr_preview = (proc.stderr or "")[:500]
        raise RuntimeError(
            f"{backend} CLI exited with code {proc.returncode}: {stderr_preview}"
        )

    stdout = proc.stdout or ""

    # Parse response based on backend and capabilities
    return _parse_cli_output(stdout, caps, backend)


def _parse_cli_output(
    stdout: str,
    caps: dict,
    backend: str,
) -> dict:
    """Parse CLI stdout into a structured result dict."""
    result = {
        "text": "",
        "cost": 0.0,
        "input_tokens": 0,
        "output_tokens": 0,
        "calls": 1,
    }

    if not stdout.strip():
        return result

    if backend == "claude" and caps.get("json_output"):
        # Try to parse JSON output from claude
        try:
            data = json.loads(stdout)
            if isinstance(data, dict):
                # Multi-shape detection
                text = _extract_text_from_claude_json(data)
                result["text"] = text

                # Extract usage/cost if available
                usage = data.get("usage", {})
                if isinstance(usage, dict):
                    result["input_tokens"] = usage.get("input_tokens", 0)
                    result["output_tokens"] = usage.get("output_tokens", 0)

                cost_usd = data.get("cost_usd", 0.0)
                if isinstance(cost_usd, (int, float)):
                    result["cost"] = float(cost_usd)

                return result
        except json.JSONDecodeError:
            _emit_warning(
                "claude_json_parse_fail",
                "Failed to parse claude JSON output. Using raw stdout as text.",
            )

    # Fallback: use raw stdout as text
    result["text"] = stdout.strip()
    return result


def _extract_text_from_claude_json(data: dict) -> str:
    """Extract response text from claude JSON output, supporting multiple shapes.

    Shape A: {"result": "...", ...}
    Shape B: {"content": [{"text": "..."}], ...}
    Shape C: {"completion": "..."}
    Unknown: fall back to raw stdout with warning.
    """
    # Shape A: result field (current claude CLI format)
    if "result" in data:
        val = data["result"]
        if isinstance(val, str):
            return val

    # Shape B: content array (API-like format)
    if "content" in data:
        content = data["content"]
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    return block.get("text", "")
            # Try without type check
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    return block["text"]

    # Shape C: completion field (legacy)
    if "completion" in data:
        val = data["completion"]
        if isinstance(val, str):
            return val

    # Unknown shape: warn and dump
    keys = sorted(data.keys())
    _emit_warning(
        "claude_unknown_json_shape",
        f"Unknown claude JSON shape, keys: {keys}. Using raw output as text.",
    )
    return json.dumps(data)


# ---------------------------------------------------------------------------
# Retry with backoff
# ---------------------------------------------------------------------------


def retry_with_backoff(
    fn,
    max_retries: Optional[int] = None,
    backoff_base: Optional[float] = None,
    backoff_jitter: Optional[float] = None,
):
    """Execute fn with exponential backoff and jitter on failure.

    Handles both subprocess failures (RuntimeError from call_model)
    and general exceptions.

    Args:
        fn: Callable to execute. Should raise on failure.
        max_retries: Max retry attempts. Defaults to config value.
        backoff_base: Base for exponential backoff. Defaults to config.
        backoff_jitter: Max random jitter added. Defaults to config.

    Returns:
        The return value of fn on success.

    Raises:
        The last exception if all retries are exhausted.
    """
    cfg = load_config()
    retry_cfg = cfg.get("retry", {})
    retries = max_retries if max_retries is not None else retry_cfg.get("max_retries", 3)
    base = backoff_base if backoff_base is not None else retry_cfg.get("backoff_base", 2.0)
    jitter = backoff_jitter if backoff_jitter is not None else retry_cfg.get("backoff_jitter", 0.5)

    last_exc = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                delay = (base ** attempt) + random.uniform(0, jitter)
                time.sleep(delay)
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# JSON extraction from LLM responses
# ---------------------------------------------------------------------------

_CODE_FENCE_RE = re.compile(r"```(?:json)?\s*\n?(.*?)\n?```", re.DOTALL)
_TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")


def extract_json(text: str) -> Optional[dict]:
    """Extract the first top-level JSON object from LLM response text.

    Handles:
    - JSON wrapped in prose text
    - Markdown code fences around JSON
    - Trailing commas before } or ]

    Uses json.JSONDecoder.raw_decode for robust nested-object parsing
    instead of fragile regex-based brace matching.

    Args:
        text: Raw LLM response text.

    Returns:
        Parsed dict on success, None on failure.
    """
    # First try: extract from code fences
    for fence_match in _CODE_FENCE_RE.finditer(text):
        candidate = fence_match.group(1).strip()
        result = _try_parse_json(candidate)
        if result is not None:
            return result

    # Second try: scan for first valid JSON object using raw_decode
    result = _extract_first_object(text)
    if result is not None:
        return result

    # Third try: strip trailing commas and scan again
    cleaned = _TRAILING_COMMA_RE.sub(r"\1", text)
    return _extract_first_object(cleaned)


def _extract_first_object(text: str) -> Optional[dict]:
    """Scan text for the first valid JSON object using raw_decode."""
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def _try_parse_json(text: str) -> Optional[dict]:
    """Attempt to parse JSON text, handling trailing commas."""
    # Try direct parse first
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        return None
    except json.JSONDecodeError:
        pass

    # Strip trailing commas and retry
    cleaned = _TRAILING_COMMA_RE.sub(r"\1", text)
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    return None


# ---------------------------------------------------------------------------
# Skill content loading
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def load_skill_body(skill_name: str) -> Optional[str]:
    """Load a SKILL.md file, strip YAML frontmatter, return body with delimiters.

    Args:
        skill_name: Name of the skill directory under skills/.

    Returns:
        Skill body wrapped in BEGIN/END delimiters, or None if not found.
    """
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        return None

    content = skill_path.read_text(encoding="utf-8")

    # Strip YAML frontmatter (everything between first and second ---)
    body = _FRONTMATTER_RE.sub("", content, count=1).strip()

    return f"--- BEGIN SKILL CONTENT ---\n{body}\n--- END SKILL CONTENT ---"


def load_skill_description(skill_name: str) -> Optional[str]:
    """Load SKILL.md frontmatter and return the description string.

    Args:
        skill_name: Name of the skill directory under skills/.

    Returns:
        Description string from frontmatter, or None if not found.
    """
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        return None

    content = skill_path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(content)
    if not match:
        return None

    try:
        fm = yaml.safe_load(match.group(1))
        if isinstance(fm, dict):
            return fm.get("description")
    except yaml.YAMLError:
        pass

    return None


# ---------------------------------------------------------------------------
# Run metadata
# ---------------------------------------------------------------------------


def build_run_metadata(
    eval_type: str,
    model: Optional[str] = None,
    judge_model: Optional[str] = None,
    seed: Optional[int] = None,
    cli: Optional[str] = None,
) -> dict:
    """Generate run metadata for results envelope.

    Args:
        eval_type: One of 'effectiveness', 'activation', 'size_impact', 'confusion'.
        model: Generation model override. Defaults to config.
        judge_model: Judge model override. Defaults to config.
        seed: RNG seed override. Defaults to config.
        cli: CLI backend override. Defaults to config.

    Returns:
        Dict with run_id, timestamp, backend, model info, seed, and eval_type.
    """
    cfg = load_config()
    cli_cfg = cfg.get("cli", {})
    backend = cli or cli_cfg.get("default", "claude")
    backend_cfg = cli_cfg.get(backend, {})

    resolved_model = model or backend_cfg.get("model") or "default"
    resolved_judge = judge_model or cli_cfg.get(
        backend, {}
    ).get("model") or "default"

    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "backend": backend,
        "model": resolved_model,
        "judge_model": resolved_judge,
        "seed": seed if seed is not None else cfg.get("rng", {}).get("default_seed", 42),
        "total_cost": 0.0,
        "eval_type": eval_type,
    }


# ---------------------------------------------------------------------------
# Cost tracking
# ---------------------------------------------------------------------------


def track_cost(
    cli_reported_cost: float,
) -> float:
    """Accept CLI-reported cost directly.

    Args:
        cli_reported_cost: Cost reported by CLI (0.0 if unavailable).

    Returns:
        The cost value passed in.
    """
    return cli_reported_cost


# ---------------------------------------------------------------------------
# Results output
# ---------------------------------------------------------------------------


def write_results(
    meta: dict,
    summary: dict[str, Any],
    cases: list[dict],
    output_dir: Optional[Path] = None,
    artifacts: Optional[dict] = None,
) -> Path:
    """Write eval results to JSON following the common envelope format.

    The output envelope structure:
    {
        "meta": { run_id, timestamp, backend, model, judge_model, seed, total_cost, eval_type },
        "summary": { entity_id: { mean, stddev, n, ...per-eval-type scalar metrics } },
        "cases": [ { id, prompt, entity_id, ...per-eval-type details } ],
        "artifacts": { ...optional eval-specific structured data }
    }

    Args:
        meta: Run metadata dict (from build_run_metadata).
        summary: Dict mapping entity_id to scalar metrics.
        cases: List of per-case result dicts.
        output_dir: Output directory. Defaults to config results_dir.
        artifacts: Optional eval-specific structured data.

    Returns:
        Path to the written results file.
    """
    cfg = load_config()
    resolved_dir: Path = output_dir if output_dir is not None else EVALS_DIR / cfg.get("paths", {}).get("results_dir", "results")

    resolved_dir.mkdir(parents=True, exist_ok=True)

    eval_type = meta.get("eval_type", "unknown")
    run_id = meta.get("run_id", "unknown")
    filename = f"{eval_type}_{run_id}.json"

    envelope = {
        "meta": meta,
        "summary": summary,
        "cases": cases,
        "artifacts": artifacts or {},
    }

    output_path = resolved_dir / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)

    return output_path


# ---------------------------------------------------------------------------
# Utility: list skills with rubrics
# ---------------------------------------------------------------------------


def list_skills_with_rubrics(rubrics_dir: Optional[Path] = None) -> list[str]:
    """Return sorted list of skill names that have rubric YAML files.

    Args:
        rubrics_dir: Path to rubrics directory. Defaults to config path.

    Returns:
        Sorted list of skill name strings.
    """
    cfg = load_config()
    resolved_dir: Path = rubrics_dir if rubrics_dir is not None else EVALS_DIR / cfg.get("paths", {}).get("rubrics_dir", "rubrics")

    if not resolved_dir.is_dir():
        return []

    skills = []
    for p in sorted(resolved_dir.iterdir()):
        if p.suffix == ".yaml" and p.name != ".gitkeep":
            skills.append(p.stem)
    return skills


def load_rubric(skill_name: str, rubrics_dir: Optional[Path] = None) -> Optional[dict]:
    """Load and return a parsed rubric YAML for a skill.

    Args:
        skill_name: Skill name (matches rubric filename without .yaml).
        rubrics_dir: Path to rubrics directory. Defaults to config path.

    Returns:
        Parsed rubric dict, or None if not found.
    """
    cfg = load_config()
    resolved_dir: Path = rubrics_dir if rubrics_dir is not None else EVALS_DIR / cfg.get("paths", {}).get("rubrics_dir", "rubrics")

    rubric_path = resolved_dir / f"{skill_name}.yaml"
    if not rubric_path.is_file():
        return None

    with open(rubric_path) as f:
        return yaml.safe_load(f)
