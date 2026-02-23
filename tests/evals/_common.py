"""Shared infrastructure for offline skill evaluation runners.

All eval runners import from this module. Provides config loading,
Anthropic client wrapper, retry/backoff with jitter, token/cost
accounting, run_id/timestamps, JSON extraction from LLM responses,
output writing, and skill content loading with frontmatter stripping.
"""

import json
import os
import random
import re
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
    """Load config.yaml and merge environment variable overrides.

    Reads ANTHROPIC_API_KEY from the environment and injects it into
    the returned config dict under the 'api_key' key.

    Returns:
        Parsed config dict with env overrides applied.
    """
    global _config_cache
    path = config_path or CONFIG_PATH
    if _config_cache is not None and config_path is None:
        return _config_cache

    with open(path) as f:
        cfg = yaml.safe_load(f)

    if not isinstance(cfg, dict):
        raise ValueError(f"Invalid config at {path}: expected YAML mapping, got {type(cfg).__name__}")

    # Inject API key from environment
    cfg["api_key"] = os.environ.get("ANTHROPIC_API_KEY", "")

    if config_path is None:
        _config_cache = cfg
    return cfg


# ---------------------------------------------------------------------------
# Anthropic client
# ---------------------------------------------------------------------------


def get_client(api_key: Optional[str] = None):
    """Create an Anthropic client instance.

    Args:
        api_key: Optional API key override. Falls back to config/env.

    Returns:
        An anthropic.Anthropic client instance.

    Raises:
        ImportError: If the anthropic package is not installed.
        ValueError: If no API key is available.
    """
    import anthropic

    key = api_key or load_config().get("api_key", "")
    if not key:
        raise ValueError(
            "No Anthropic API key found. Set ANTHROPIC_API_KEY environment variable."
        )
    return anthropic.Anthropic(api_key=key)


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
) -> dict:
    """Generate run metadata for results envelope.

    Args:
        eval_type: One of 'effectiveness', 'activation', 'size_impact', 'confusion'.
        model: Generation model override. Defaults to config.
        judge_model: Judge model override. Defaults to config.
        seed: RNG seed override. Defaults to config.

    Returns:
        Dict with run_id, timestamp, model info, seed, and eval_type.
    """
    cfg = load_config()
    models = cfg.get("models", {})

    return {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model or models.get("generation_model", "claude-haiku-4-20250514"),
        "judge_model": judge_model or models.get("judge_model", "claude-haiku-4-20250514"),
        "seed": seed if seed is not None else cfg.get("rng", {}).get("default_seed", 42),
        "total_cost": 0.0,
        "eval_type": eval_type,
    }


# ---------------------------------------------------------------------------
# Cost tracking
# ---------------------------------------------------------------------------

# Approximate per-token costs (USD) for common models
_COST_TABLE = {
    "claude-haiku-4-20250514": {"input": 0.80 / 1_000_000, "output": 4.00 / 1_000_000},
    "claude-sonnet-4-20250514": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
}


def track_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Estimate API call cost from token counts.

    Args:
        model: Model identifier string.
        input_tokens: Number of input tokens.
        output_tokens: Number of output tokens.

    Returns:
        Estimated cost in USD.
    """
    costs = _COST_TABLE.get(model, {"input": 1.0 / 1_000_000, "output": 5.0 / 1_000_000})
    return (input_tokens * costs["input"]) + (output_tokens * costs["output"])


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
        "meta": { run_id, timestamp, model, judge_model, seed, total_cost, eval_type },
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
    if output_dir is None:
        output_dir = EVALS_DIR / cfg.get("paths", {}).get("results_dir", "results")

    output_dir.mkdir(parents=True, exist_ok=True)

    eval_type = meta.get("eval_type", "unknown")
    run_id = meta.get("run_id", "unknown")
    filename = f"{eval_type}_{run_id}.json"

    envelope = {
        "meta": meta,
        "summary": summary,
        "cases": cases,
        "artifacts": artifacts or {},
    }

    output_path = output_dir / filename
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
    if rubrics_dir is None:
        rubrics_dir = EVALS_DIR / cfg.get("paths", {}).get("rubrics_dir", "rubrics")

    if not rubrics_dir.is_dir():
        return []

    skills = []
    for p in sorted(rubrics_dir.iterdir()):
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
    if rubrics_dir is None:
        rubrics_dir = EVALS_DIR / cfg.get("paths", {}).get("rubrics_dir", "rubrics")

    rubric_path = rubrics_dir / f"{skill_name}.yaml"
    if not rubric_path.is_file():
        return None

    with open(rubric_path) as f:
        return yaml.safe_load(f)
