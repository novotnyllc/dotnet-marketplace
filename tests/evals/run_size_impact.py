#!/usr/bin/env python3
"""Size impact eval runner (L6) -- progressive disclosure validation.

Tests whether skill content format (full body vs summary vs none)
affects output quality, validating progressive disclosure decisions.

For each candidate skill, generates code under three conditions:
  1. Full: Complete SKILL.md body (frontmatter stripped, explicit delimiters)
  2. Summary: Deterministic summary extraction (description + scope)
  3. Baseline: No skill content

Skills with sibling files defined in candidates.yaml get a fourth condition:
  4. Full + Siblings: SKILL.md body + concatenated sibling contents

Pairwise comparisons scored by LLM judge via judge_prompt.py.

Usage:
    python tests/evals/run_size_impact.py --dry-run
    python tests/evals/run_size_impact.py --skill dotnet-xunit
    python tests/evals/run_size_impact.py --cli codex
    python tests/evals/run_size_impact.py --regenerate

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure evals package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402
import judge_prompt  # noqa: E402
import yaml  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FULL_SYSTEM_TEMPLATE = """\
You are an expert .NET developer. Use the following skill reference material \
to inform your response.

{skill_body}

Respond with well-structured, production-quality .NET code and clear explanations."""

SUMMARY_SYSTEM_TEMPLATE = """\
You are an expert .NET developer. Use the following skill summary \
to inform your response.

--- BEGIN SKILL SUMMARY ---
{summary}
--- END SKILL SUMMARY ---

Respond with well-structured, production-quality .NET code and clear explanations."""

FULL_SIBLINGS_SYSTEM_TEMPLATE = """\
You are an expert .NET developer. Use the following skill reference material \
and supplementary content to inform your response.

{skill_body}

{siblings_body}

Respond with well-structured, production-quality .NET code and clear explanations."""

BASELINE_SYSTEM_PROMPT = """\
You are an expert .NET developer. Respond with well-structured, \
production-quality .NET code and clear explanations."""

# Default judge criteria for size impact comparisons
SIZE_IMPACT_CRITERIA = [
    {
        "name": "technical_accuracy",
        "weight": 0.30,
        "description": "Correctness of APIs, patterns, and .NET conventions used.",
    },
    {
        "name": "completeness",
        "weight": 0.25,
        "description": "Coverage of the requested scenario including edge cases and error handling.",
    },
    {
        "name": "best_practices",
        "weight": 0.25,
        "description": "Adherence to modern .NET best practices and idiomatic patterns.",
    },
    {
        "name": "code_quality",
        "weight": 0.20,
        "description": "Readability, structure, naming, and maintainability of the code.",
    },
]

# Pairwise comparison definitions
COMPARISONS = [
    ("full", "baseline"),
    ("full", "summary"),
    ("summary", "baseline"),
]

SIBLING_COMPARISONS = [
    ("full_siblings", "full"),
]

# ---------------------------------------------------------------------------
# Summary extraction (deterministic algorithm)
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?\n)---\s*\n", re.DOTALL)
_SCOPE_SECTION_RE = re.compile(
    r"^##\s+Scope\s*\n(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_CODE_FENCE_RE = re.compile(r"^[ \t]*```[^\n]*\n.*?^[ \t]*```", re.DOTALL | re.MULTILINE)
_CROSS_REF_RE = re.compile(r"\[skill:[^\]]+\]")


def extract_summary(skill_name: str) -> Optional[tuple[str, int]]:
    """Extract a deterministic summary from a SKILL.md file.

    Algorithm:
    1. Strip YAML frontmatter (between first/second ---)
    2. Extract ## Scope section (from heading to next ## or EOF)
    3. Strip code fences and contents
    4. Strip [skill:...] cross-references (keep surrounding text)
    5. Concatenate: frontmatter description + newline + extracted scope text

    Args:
        skill_name: Name of the skill directory under skills/.

    Returns:
        Tuple of (summary_text, byte_count) or None if skill not found.
    """
    skill_path = _common.SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        return None

    content = skill_path.read_text(encoding="utf-8")

    # Normalize CRLF to LF for cross-platform regex matching
    content = content.replace("\r\n", "\n")

    # Step 1: Parse frontmatter for description
    description = ""
    fm_match = _FRONTMATTER_RE.match(content)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1))
            if isinstance(fm, dict):
                description = fm.get("description", "")
        except yaml.YAMLError:
            pass

    # Step 2: Strip frontmatter from body, then extract Scope section
    body = _FRONTMATTER_RE.sub("", content, count=1)
    scope_match = _SCOPE_SECTION_RE.search(body)
    scope_text = scope_match.group(1).strip() if scope_match else ""

    # Step 3: Strip code fences and their contents
    scope_text = _CODE_FENCE_RE.sub("", scope_text)

    # Step 4: Strip cross-references
    scope_text = _CROSS_REF_RE.sub("", scope_text)

    # Clean up whitespace from removals
    scope_text = re.sub(r"\n{3,}", "\n\n", scope_text).strip()

    # Step 5: Concatenate
    summary = f"{description}\n\n{scope_text}" if scope_text else description
    summary = summary.strip()

    if not summary:
        return None

    byte_count = len(summary.encode("utf-8"))
    return summary, byte_count


# ---------------------------------------------------------------------------
# Sibling content loading
# ---------------------------------------------------------------------------


def load_siblings(
    skill_name: str, sibling_names: list[str], max_bytes: int
) -> Optional[tuple[str, int]]:
    """Load and concatenate sibling file contents with byte cap.

    Truncation operates on raw bytes to avoid splitting multi-byte UTF-8
    characters. The byte cap applies to raw file content; the returned
    byte count is computed from the final formatted string (including
    delimiter wrappers) for exact consistency with what gets injected.

    Args:
        skill_name: Name of the skill directory.
        sibling_names: Ordered list of sibling filenames to include.
        max_bytes: Maximum total raw content bytes to include.

    Returns:
        Tuple of (formatted_siblings_text, formatted_byte_count)
        or None if no siblings found.
    """
    skill_dir = _common.SKILLS_DIR / skill_name
    parts = []
    raw_total = 0

    skill_dir_resolved = skill_dir.resolve()

    for sib_name in sibling_names:
        # Defense-in-depth: reject path traversal even if loader validated
        if ".." in sib_name or "/" in sib_name or "\\" in sib_name:
            continue

        sib_path = skill_dir / sib_name
        # Reject symlinks to prevent symlink escape
        if sib_path.is_symlink():
            continue
        if not sib_path.is_file():
            continue
        # Enforce resolved path stays within skill directory
        sib_resolved = sib_path.resolve()
        if not str(sib_resolved).startswith(str(skill_dir_resolved) + os.sep):
            continue

        remaining = max_bytes - raw_total
        if remaining <= 100:
            break

        # Bounded read: only read up to remaining bytes + 1 to detect overflow
        with open(sib_path, "rb") as f:
            raw = f.read(remaining + 1)

        if len(raw) > remaining:
            # Truncate raw bytes, decode ignoring partial chars at boundary
            sib_content = raw[:remaining].decode("utf-8", errors="ignore")
            sib_content += "\n[... truncated ...]"
            raw_total += remaining
        else:
            sib_content = raw.decode("utf-8", errors="replace")
            raw_total += len(raw)

        parts.append(
            f"--- BEGIN SUPPLEMENTARY: {sib_name} ---\n"
            f"{sib_content}\n"
            f"--- END SUPPLEMENTARY: {sib_name} ---"
        )

    if not parts:
        return None

    combined = "\n\n".join(parts)
    # Return byte count of the final formatted string (what actually gets injected)
    formatted_bytes = len(combined.encode("utf-8"))
    return combined, formatted_bytes


# ---------------------------------------------------------------------------
# Candidates loading
# ---------------------------------------------------------------------------


def load_candidates(
    candidates_path: Optional[Path] = None,
) -> list[dict]:
    """Load and validate candidate skills from the YAML dataset.

    Each candidate must have 'skill' (str) and 'test_prompt' (str).
    Optional fields: 'siblings' (list[str]), 'max_sibling_bytes' (int).
    Malformed entries are skipped with a warning to stderr.

    Args:
        candidates_path: Path to candidates.yaml. Defaults to standard location.

    Returns:
        List of validated candidate dicts.
    """
    cfg = _common.load_config()
    if candidates_path is None:
        datasets_dir: Path = _common.EVALS_DIR / cfg.get("paths", {}).get(
            "datasets_dir", "datasets"
        )
        candidates_path = datasets_dir / "size_impact" / "candidates.yaml"

    assert candidates_path is not None  # narrowed above
    if not candidates_path.is_file():
        return []

    with open(candidates_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "candidates" not in data:
        return []

    raw = data["candidates"]
    if not isinstance(raw, list):
        return []

    validated: list[dict] = []
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            print(
                f"[size_impact] WARN: candidates[{i}] is not a dict, skipping",
                file=sys.stderr,
            )
            continue
        if not isinstance(entry.get("skill"), str) or not entry["skill"]:
            print(
                f"[size_impact] WARN: candidates[{i}] missing 'skill' string, skipping",
                file=sys.stderr,
            )
            continue
        if not isinstance(entry.get("test_prompt"), str) or not entry["test_prompt"]:
            print(
                f"[size_impact] WARN: candidates[{i}] ({entry['skill']}) "
                f"missing 'test_prompt' string, skipping",
                file=sys.stderr,
            )
            continue
        # Validate optional siblings shape
        siblings = entry.get("siblings")
        if siblings is not None:
            if not isinstance(siblings, list):
                print(
                    f"[size_impact] WARN: candidates[{i}] ({entry['skill']}) "
                    f"'siblings' must be a list, ignoring siblings",
                    file=sys.stderr,
                )
                entry = {k: v for k, v in entry.items() if k != "siblings"}
            elif not all(isinstance(s, str) for s in siblings):
                print(
                    f"[size_impact] WARN: candidates[{i}] ({entry['skill']}) "
                    f"'siblings' entries must be strings, ignoring siblings",
                    file=sys.stderr,
                )
                entry = {k: v for k, v in entry.items() if k != "siblings"}
            else:
                unsafe = [
                    s for s in siblings
                    if ".." in s or "/" in s or "\\" in s
                ]
                if unsafe:
                    print(
                        f"[size_impact] WARN: candidates[{i}] ({entry['skill']}) "
                        f"siblings contain path separators or '..': {unsafe}, "
                        f"ignoring siblings",
                        file=sys.stderr,
                    )
                    entry = {k: v for k, v in entry.items() if k != "siblings"}

        # Validate optional max_sibling_bytes
        max_sib = entry.get("max_sibling_bytes")
        if max_sib is not None:
            if not isinstance(max_sib, int) or max_sib <= 0:
                print(
                    f"[size_impact] WARN: candidates[{i}] ({entry['skill']}) "
                    f"'max_sibling_bytes' must be a positive int, using default",
                    file=sys.stderr,
                )
                entry = {k: v for k, v in entry.items() if k != "max_sibling_bytes"}

        validated.append(entry)

    return validated


def classify_size_tier(skill_name: str) -> tuple[str, int]:
    """Classify a skill into a size tier based on SKILL.md body size.

    Tier thresholds:
      Small:  < 5KB body
      Medium: 5-15KB body
      Large:  > 15KB body

    Args:
        skill_name: Skill directory name.

    Returns:
        Tuple of (tier_label, body_byte_count).
    """
    skill_path = _common.SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_path.is_file():
        return "unknown", 0

    content = skill_path.read_text(encoding="utf-8")
    content = content.replace("\r\n", "\n")
    body = _FRONTMATTER_RE.sub("", content, count=1).strip()
    body_bytes = len(body.encode("utf-8"))

    if body_bytes < 5000:
        tier = "small"
    elif body_bytes <= 15000:
        tier = "medium"
    else:
        tier = "large"

    return tier, body_bytes


# ---------------------------------------------------------------------------
# Token counting (approximate)
# ---------------------------------------------------------------------------


def estimate_tokens(text: str) -> int:
    """Estimate token count using the ~4 chars per token heuristic.

    Args:
        text: Input text.

    Returns:
        Approximate token count.
    """
    return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Generation helpers
# ---------------------------------------------------------------------------

# Bump when system prompt template or generation logic changes to
# invalidate stale cached generations.
_CACHE_SCHEMA_VERSION = "2"


def _condition_hash(
    skill_name: str,
    prompt_text: str,
    condition: str,
    run_index: int,
    model: str,
    temperature: float,
    content: str,
    cli_backend: str,
) -> str:
    """Compute a deterministic hash for a generation cache key.

    Args:
        skill_name: Skill being evaluated.
        prompt_text: User prompt text.
        condition: Condition label (full, summary, baseline, full_siblings).
        run_index: Run iteration index.
        model: Generation model (CLI-native string).
        temperature: Sampling temperature.
        content: Injected content (affects cache invalidation).
        cli_backend: CLI backend name.

    Returns:
        Hex digest string for cache filename.
    """
    content_digest = hashlib.sha256(content.encode()).hexdigest()[:12]
    key = (
        f"v{_CACHE_SCHEMA_VERSION}|{cli_backend}|{skill_name}|{prompt_text}|{condition}"
        f"|{run_index}|{model}|{temperature}|{content_digest}"
    )
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _generations_dir(output_dir: Path) -> Path:
    """Return the generations cache directory, creating if needed."""
    d = output_dir / "generations"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_cached_generation(
    gen_dir: Path, skill_name: str, chash: str
) -> Optional[dict]:
    """Load a cached generation from disk.

    Args:
        gen_dir: Generations directory.
        skill_name: Skill name (subdirectory).
        chash: Condition hash (filename stem).

    Returns:
        Parsed dict with 'text' key, or None on cache miss.
    """
    cache_path = gen_dir / skill_name / f"{chash}.json"
    if not cache_path.is_file():
        return None
    try:
        with open(cache_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return None

    return data


def _save_generation(
    gen_dir: Path,
    skill_name: str,
    chash: str,
    text: str,
    cost: float,
    model: str,
    condition: str,
) -> None:
    """Save generation output to disk for resume/replay.

    Args:
        gen_dir: Generations directory.
        skill_name: Skill name (subdirectory).
        chash: Condition hash (filename stem).
        text: Generated text.
        cost: Generation cost.
        model: Model used.
        condition: Condition label.
    """
    skill_dir = gen_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    cache_data = {
        "text": text,
        "cost": cost,
        "model": model,
        "condition": condition,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(skill_dir / f"{chash}.json", "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=2)


def _generate_code(
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float,
    cli: Optional[str] = None,
    budget_check=None,
) -> tuple[str, float, int]:
    """Generate code using CLI-based model invocation.

    Args:
        system_prompt: System prompt for the generation.
        user_prompt: User prompt to generate code for.
        model: Model to use (CLI-native string).
        temperature: Sampling temperature.
        cli: CLI backend override.
        budget_check: Optional callable returning True when budget is
            exceeded.  Passed to retry_with_backoff for per-attempt
            enforcement.

    Returns:
        Tuple of (generated_text, cost, calls).
    """

    def _call():
        return _common.call_model(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            max_tokens=4096,
            temperature=temperature,
            cli=cli,
        )

    result = _common.retry_with_backoff(_call, budget_check=budget_check)
    return result["text"], result["cost"], result["calls"]


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------


def _compute_stats(values: list[float]) -> dict:
    """Compute mean, stddev, and n for a list of numeric values."""
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "stddev": 0.0, "n": 0}
    mean = sum(values) / n
    if n < 2:
        return {"mean": mean, "stddev": 0.0, "n": n}
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return {"mean": mean, "stddev": math.sqrt(variance), "n": n}


# ---------------------------------------------------------------------------
# Score computation from judge output
# ---------------------------------------------------------------------------


def _compute_comparison_scores(
    judge_parsed: dict,
    criteria: list[dict],
    condition_a_label: str,
    condition_b_label: str,
    condition_a_is_judge_a: bool,
) -> dict:
    """Compute weighted scores from judge output for a pairwise comparison.

    Remaps judge score_a/score_b to condition labels based on A/B assignment.

    Args:
        judge_parsed: Parsed judge JSON with 'criteria' and 'overall_winner'.
        criteria: Evaluation criteria list with 'name' and 'weight'.
        condition_a_label: Label for the first condition (e.g. "full").
        condition_b_label: Label for the second condition (e.g. "baseline").
        condition_a_is_judge_a: Whether condition_a was presented as Response A.

    Returns:
        Dict with per-condition scores, improvement, winner, and breakdown.
    """
    weight_map = {c["name"]: c["weight"] for c in criteria}
    judge_criteria = judge_parsed.get("criteria", [])

    a_weighted = 0.0
    b_weighted = 0.0
    per_criterion = []

    for jc in judge_criteria:
        name = jc.get("name", "")
        weight = weight_map.get(name, 0.0)

        if condition_a_is_judge_a:
            score_a = jc.get("score_a", 0)
            score_b = jc.get("score_b", 0)
        else:
            score_a = jc.get("score_b", 0)
            score_b = jc.get("score_a", 0)

        per_criterion.append(
            {
                "name": name,
                "weight": weight,
                f"score_{condition_a_label}": score_a,
                f"score_{condition_b_label}": score_b,
                "reasoning": jc.get("reasoning", ""),
            }
        )

        a_weighted += score_a * weight
        b_weighted += score_b * weight

    improvement = a_weighted - b_weighted
    if a_weighted > b_weighted:
        winner = condition_a_label
    elif b_weighted > a_weighted:
        winner = condition_b_label
    else:
        winner = "tie"

    return {
        f"score_{condition_a_label}": round(a_weighted, 4),
        f"score_{condition_b_label}": round(b_weighted, 4),
        "improvement": round(improvement, 4),
        "winner": winner,
        "per_criterion": per_criterion,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Size impact eval runner (L6) -- progressive disclosure validation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show candidate skills and exit without CLI calls",
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Evaluate a single skill by name (must be in candidates.yaml)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override generation model (CLI-native string)",
    )
    parser.add_argument(
        "--judge-model",
        type=str,
        default=None,
        help="Override judge model",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of evaluation runs per condition (default: 1)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="RNG seed for reproducibility (default: from config)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Override output directory for results",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Force re-generation even if cached outputs exist",
    )
    parser.add_argument(
        "--cli",
        type=str,
        choices=["claude", "codex", "copilot"],
        default=None,
        help="Override CLI backend (default: from config.yaml)",
    )
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cfg = _common.load_config()

    # Load candidates
    candidates = load_candidates()
    if not candidates:
        print(
            "[size_impact] No candidates found in datasets/size_impact/candidates.yaml",
            file=sys.stderr,
        )
        print(f"TOTAL_CALLS=0")
        print(f"COST_USD=0.0")
        print(f"ABORTED=0")
        print(f"N_CASES=0")
        print(f"FAIL_FAST=0")
        return 0

    # Filter to single skill if --skill specified
    if args.skill:
        matching = [c for c in candidates if c["skill"] == args.skill]
        if not matching:
            print(
                f"[size_impact] ERROR: Skill '{args.skill}' not found in candidates.yaml. "
                f"Available: {', '.join(c['skill'] for c in candidates)}",
                file=sys.stderr,
            )
            print(f"TOTAL_CALLS=0")
            print(f"COST_USD=0.0")
            print(f"ABORTED=0")
            print(f"N_CASES=0")
            print(f"FAIL_FAST=0")
            return 0
        candidates = matching

    # --- Dry run ---
    if args.dry_run:
        print(
            f"[size_impact] Dry run -- {len(candidates)} candidate skill(s):",
            file=sys.stderr,
        )
        for cand in candidates:
            skill_name = cand["skill"]
            tier, body_bytes = classify_size_tier(skill_name)
            has_siblings = bool(cand.get("siblings"))

            summary_result = extract_summary(skill_name)
            summary_bytes = summary_result[1] if summary_result else 0

            sibling_info = ""
            if has_siblings:
                sib_names = cand["siblings"]
                max_sib = cand.get("max_sibling_bytes", 10000)
                sib_result = load_siblings(skill_name, sib_names, max_sib)
                sib_bytes = sib_result[1] if sib_result else 0
                sibling_info = f", siblings={sib_names} ({sib_bytes}B)"

            full_body = _common.load_skill_body(skill_name)
            full_tok = estimate_tokens(full_body) if full_body else 0
            sum_tok = estimate_tokens(summary_result[0]) if summary_result else 0
            print(
                f"  {skill_name}: tier={tier}, body={body_bytes}B (~{full_tok}tok), "
                f"summary={summary_bytes}B (~{sum_tok}tok)"
                f"{sibling_info}",
                file=sys.stderr,
            )

        conditions_count = sum(
            4 if cand.get("siblings") else 3 for cand in candidates
        )
        comparisons_count = sum(
            len(COMPARISONS) + (len(SIBLING_COMPARISONS) if cand.get("siblings") else 0)
            for cand in candidates
        )
        print(
            f"[size_impact] Would generate {conditions_count} conditions, "
            f"{comparisons_count} comparisons, "
            f"{args.runs} run(s) each.",
            file=sys.stderr,
        )
        print(
            "[size_impact] Dry run complete. No CLI calls made.",
            file=sys.stderr,
        )
        print(f"TOTAL_CALLS=0")
        print(f"COST_USD=0.0")
        print(f"ABORTED=0")
        print(f"N_CASES=0")
        print(f"FAIL_FAST=0")
        return 0

    # --- Full eval execution ---
    meta = _common.build_run_metadata(
        eval_type="size_impact",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
        cli=args.cli,
    )
    temperature = cfg.get("temperature", 0.0)
    max_cost = cfg.get("cost", {}).get("max_cost_per_run", 5.0)
    max_calls = cfg.get("cost", {}).get("max_calls_per_run", 500)
    seed = meta["seed"]
    cli_backend = meta["backend"]

    print(f"[size_impact] Starting eval run {meta['run_id']}", file=sys.stderr)
    print(
        f"[size_impact] Backend: {cli_backend}, Skills: {len(candidates)}, Runs per condition: {args.runs}",
        file=sys.stderr,
    )
    print(
        f"[size_impact] Model: {meta['model']}, Judge: {meta['judge_model']}, Seed: {seed}",
        file=sys.stderr,
    )

    # Set up output paths
    results_dir = (
        args.output_dir
        if args.output_dir is not None
        else _common.EVALS_DIR
        / cfg.get("paths", {}).get("results_dir", "results")
    )
    results_dir.mkdir(parents=True, exist_ok=True)
    gen_dir = _generations_dir(results_dir)

    total_cost = 0.0
    total_calls_count = 0
    aborted = False
    fail_fast = False
    fail_fast_reason = ""
    cases: list[dict] = []

    # Fail-fast tracker
    ff_cfg = cfg.get("fail_fast", {})
    ff_threshold = ff_cfg.get("consecutive_threshold", 3)
    ff_enabled = ff_cfg.get("enabled", True)
    tracker = _common.ConsecutiveFailureTracker(threshold=ff_threshold)

    # Per-skill tracking for summary
    skill_comparisons: dict[str, list[dict]] = {}

    for cand in candidates:
        if aborted:
            break

        skill_name = cand["skill"]
        test_prompt = cand["test_prompt"]
        tier, body_bytes = classify_size_tier(skill_name)
        has_siblings = bool(cand.get("siblings"))

        print(
            f"[size_impact] === {skill_name} (tier={tier}, {body_bytes}B) ===",
            file=sys.stderr,
        )

        if skill_name not in skill_comparisons:
            skill_comparisons[skill_name] = []

        # --- Prepare condition content ---
        full_body = _common.load_skill_body(skill_name)
        if full_body is None:
            print(
                f"[size_impact] WARN: Skill body not found for {skill_name}, skipping",
                file=sys.stderr,
            )
            continue

        summary_result = extract_summary(skill_name)
        if summary_result is None:
            print(
                f"[size_impact] WARN: Could not extract summary for {skill_name}, skipping",
                file=sys.stderr,
            )
            continue
        summary_text, _summary_bytes = summary_result

        siblings_text: Optional[str] = None
        if has_siblings:
            sib_names = cand["siblings"]
            max_sib = cand.get("max_sibling_bytes", 10000)
            sib_result = load_siblings(skill_name, sib_names, max_sib)
            if sib_result:
                siblings_text, _sib_bytes = sib_result

        summary_injected = (
            f"--- BEGIN SKILL SUMMARY ---\n{summary_text}\n--- END SKILL SUMMARY ---"
        )

        condition_prompts = {
            "full": FULL_SYSTEM_TEMPLATE.format(skill_body=full_body),
            "summary": SUMMARY_SYSTEM_TEMPLATE.format(summary=summary_text),
            "baseline": BASELINE_SYSTEM_PROMPT,
        }
        condition_content = {
            "full": full_body,
            "summary": summary_injected,
            "baseline": "",
        }
        condition_sizes = {
            "full": {
                "bytes": len(full_body.encode("utf-8")),
                "tokens_estimated": estimate_tokens(full_body),
            },
            "summary": {
                "bytes": len(summary_injected.encode("utf-8")),
                "tokens_estimated": estimate_tokens(summary_injected),
            },
            "baseline": {
                "bytes": 0,
                "tokens_estimated": 0,
            },
        }

        if siblings_text is not None:
            full_siblings_injected = full_body + "\n\n" + siblings_text
            condition_prompts["full_siblings"] = FULL_SIBLINGS_SYSTEM_TEMPLATE.format(
                skill_body=full_body, siblings_body=siblings_text
            )
            condition_content["full_siblings"] = full_siblings_injected
            condition_sizes["full_siblings"] = {
                "bytes": len(full_siblings_injected.encode("utf-8")),
                "tokens_estimated": estimate_tokens(full_siblings_injected),
            }

        for run_idx in range(args.runs):
            if aborted:
                break

            # Budget check closure (captures mutable locals)
            def _budget_exceeded(pending_calls: int = 0) -> bool:
                return total_cost >= max_cost or (total_calls_count + pending_calls) >= max_calls

            # --- Generate all conditions ---
            generations: dict[str, str] = {}
            gen_costs: dict[str, float] = {}
            generation_error: Optional[str] = None

            for cond_name, sys_prompt in condition_prompts.items():
                # Dual abort check
                if _budget_exceeded():
                    aborted = True
                    print(
                        f"[size_impact] ABORT: Limit exceeded "
                        f"(cost=${total_cost:.4f}/{max_cost}, "
                        f"calls={total_calls_count}/{max_calls})",
                        file=sys.stderr,
                    )
                    break

                chash = _condition_hash(
                    skill_name,
                    test_prompt,
                    cond_name,
                    run_idx,
                    meta["model"],
                    temperature,
                    condition_content[cond_name],
                    cli_backend,
                )

                cached = None
                if not args.regenerate:
                    cached = _load_cached_generation(gen_dir, skill_name, chash)

                if cached is not None:
                    generations[cond_name] = cached["text"]
                    gen_costs[cond_name] = 0.0
                    print(
                        f"[size_impact]   {cond_name}: cached ({chash})",
                        file=sys.stderr,
                    )
                else:
                    try:
                        text, cost, calls = _generate_code(
                            sys_prompt,
                            test_prompt,
                            meta["model"],
                            temperature,
                            cli=args.cli,
                            budget_check=_budget_exceeded,
                        )
                        generations[cond_name] = text
                        gen_costs[cond_name] = cost
                        total_cost += cost
                        total_calls_count += calls

                        _save_generation(
                            gen_dir,
                            skill_name,
                            chash,
                            text,
                            cost,
                            meta["model"],
                            cond_name,
                        )
                        print(
                            f"[size_impact]   {cond_name}: generated (${cost:.4f})",
                            file=sys.stderr,
                        )
                    except Exception as exc:
                        generation_error = f"{cond_name} generation failed: {exc}"
                        # Account for CLI calls consumed by failed retries
                        total_calls_count += int(getattr(exc, "calls_consumed", 0))
                        # Track consecutive failures for fail-fast
                        if ff_enabled and tracker.record_failure(exc):
                            fail_fast = True
                            fail_fast_reason = tracker.last_fingerprint
                            print(
                                f"[size_impact] FAIL_FAST: {ff_threshold} consecutive "
                                f"same-error failures -- aborting",
                                file=sys.stderr,
                            )
                        print(
                            f"[size_impact]   {cond_name}: ERROR - {exc}",
                            file=sys.stderr,
                        )
                        break

            if aborted or generation_error:
                if generation_error:
                    cases.append(
                        {
                            "id": f"{skill_name}/run{run_idx}",
                            "entity_id": skill_name,
                            "skill_name": skill_name,
                            "prompt": test_prompt,
                            "run_index": run_idx,
                            "generation_error": generation_error,
                            "size_tier": tier,
                            "body_bytes": body_bytes,
                            "condition_sizes": condition_sizes,
                            "conditions_present": sorted(condition_prompts.keys()),
                            "model": meta["model"],
                            "judge_model": meta["judge_model"],
                            "run_id": meta["run_id"],
                            "seed": seed,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    )
                if fail_fast:
                    aborted = True
                continue

            # Check for empty/refusal
            empty_conditions = [
                c for c, t in generations.items() if not t.strip()
            ]
            if empty_conditions:
                cases.append(
                    {
                        "id": f"{skill_name}/run{run_idx}",
                        "entity_id": skill_name,
                        "skill_name": skill_name,
                        "prompt": test_prompt,
                        "run_index": run_idx,
                        "generation_error": f"empty/refusal for: {', '.join(empty_conditions)}",
                        "size_tier": tier,
                        "body_bytes": body_bytes,
                        "condition_sizes": condition_sizes,
                        "conditions_present": sorted(condition_prompts.keys()),
                        "model": meta["model"],
                        "judge_model": meta["judge_model"],
                        "run_id": meta["run_id"],
                        "seed": seed,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
                continue

            # --- Pairwise judge comparisons ---
            all_comparisons = list(COMPARISONS)
            if siblings_text is not None:
                all_comparisons.extend(SIBLING_COMPARISONS)

            for cond_a, cond_b in all_comparisons:
                if cond_a not in generations or cond_b not in generations:
                    continue

                # Dual abort check
                if _budget_exceeded():
                    aborted = True
                    break

                # A/B randomization with deterministic seed
                seed_input = (
                    f"{seed}|{skill_name}|{cond_a}|{cond_b}|{run_idx}"
                )
                case_seed = int(
                    hashlib.sha256(seed_input.encode()).hexdigest()[:8], 16
                )
                case_rng = random.Random(case_seed)
                a_is_judge_a = case_rng.random() < 0.5

                if a_is_judge_a:
                    response_a = generations[cond_a]
                    response_b = generations[cond_b]
                    ab_assignment = f"{cond_a}=A,{cond_b}=B"
                else:
                    response_a = generations[cond_b]
                    response_b = generations[cond_a]
                    ab_assignment = f"{cond_a}=B,{cond_b}=A"

                comparison_id = (
                    f"{skill_name}/{cond_a}_vs_{cond_b}/run{run_idx}"
                )
                print(
                    f"[size_impact]   Judging {cond_a} vs {cond_b} "
                    f"(run {run_idx}) ...",
                    file=sys.stderr,
                )

                judge_result: Optional[dict] = None
                try:
                    judge_result = judge_prompt.invoke_judge(
                        user_prompt=test_prompt,
                        response_a=response_a,
                        response_b=response_b,
                        criteria=SIZE_IMPACT_CRITERIA,
                        judge_model=meta["judge_model"],
                        temperature=temperature,
                        cli=args.cli,
                        budget_check=_budget_exceeded,
                    )
                except Exception as exc:
                    judge_result = {
                        "parsed": None,
                        "raw_judge_text": "",
                        "cost": 0.0,
                        "calls": int(getattr(exc, "calls_consumed", 0)),
                        "attempts": 0,
                        "judge_error": f"judge invocation failed: {exc}",
                    }
                    # Track consecutive failures for fail-fast
                    if ff_enabled and tracker.record_failure(exc):
                        fail_fast = True
                        fail_fast_reason = tracker.last_fingerprint
                        print(
                            f"[size_impact] FAIL_FAST: {ff_threshold} consecutive "
                            f"same-error failures -- aborting",
                            file=sys.stderr,
                        )

                total_cost += judge_result["cost"]
                total_calls_count += judge_result.get("calls", 0)

                case_record: dict = {
                    "id": comparison_id,
                    "entity_id": skill_name,
                    "skill_name": skill_name,
                    "prompt": test_prompt,
                    "run_index": run_idx,
                    "comparison": f"{cond_a}_vs_{cond_b}",
                    "condition_a": cond_a,
                    "condition_b": cond_b,
                    "ab_assignment": ab_assignment,
                    "case_seed": case_seed,
                    "size_tier": tier,
                    "body_bytes": body_bytes,
                    "condition_sizes": condition_sizes,
                    "conditions_present": sorted(condition_prompts.keys()),
                    "model": meta["model"],
                    "judge_model": meta["judge_model"],
                    "run_id": meta["run_id"],
                    "seed": seed,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "cost_judge": judge_result["cost"],
                    "cost_generation_allocated": sum(
                        gen_costs.get(c, 0.0) for c in (cond_a, cond_b)
                    ),
                    "judge_attempts": judge_result["attempts"],
                }

                if judge_result["judge_error"]:
                    case_record["judge_error"] = judge_result["judge_error"]
                    case_record["raw_judge_text"] = judge_result[
                        "raw_judge_text"
                    ]
                    cases.append(case_record)
                    if fail_fast:
                        aborted = True
                        break
                    continue

                parsed = judge_result["parsed"]
                assert parsed is not None

                scores = _compute_comparison_scores(
                    parsed,
                    SIZE_IMPACT_CRITERIA,
                    cond_a,
                    cond_b,
                    a_is_judge_a,
                )

                case_record["scores"] = scores
                # Successful case -- reset consecutive failure counter
                tracker.record_success()
                cases.append(case_record)

                skill_comparisons[skill_name].append(
                    {
                        "comparison": f"{cond_a}_vs_{cond_b}",
                        "winner": scores["winner"],
                        "improvement": scores["improvement"],
                        "run_index": run_idx,
                    }
                )

    # --- Build summary ---
    summary: dict[str, dict] = {}
    for cand in candidates:
        skill_name = cand["skill"]
        tier, body_bytes = classify_size_tier(skill_name)
        comps = skill_comparisons.get(skill_name, [])

        # Summarize per comparison type
        comp_summaries: dict[str, dict] = {}
        for comp_type in ["full_vs_baseline", "full_vs_summary", "summary_vs_baseline", "full_siblings_vs_full"]:
            type_comps = [
                c for c in comps if c["comparison"] == comp_type
            ]
            if not type_comps:
                continue

            improvements = [c["improvement"] for c in type_comps]
            winners = [c["winner"] for c in type_comps]
            stats = _compute_stats(improvements)

            parts = comp_type.split("_vs_")
            a_label = parts[0]
            b_label = parts[1]
            wins_a = sum(1 for w in winners if w == a_label)
            wins_b = sum(1 for w in winners if w == b_label)
            ties = sum(1 for w in winners if w == "tie")

            comp_summaries[comp_type] = {
                "mean": round(stats["mean"], 4),
                "stddev": round(stats["stddev"], 4),
                "n": stats["n"],
                f"wins_{a_label}": wins_a,
                f"wins_{b_label}": wins_b,
                "ties": ties,
            }

        # Overall skill summary
        all_improvements = [c["improvement"] for c in comps]
        overall_stats = _compute_stats(all_improvements)
        error_count = sum(
            1
            for c in cases
            if c.get("entity_id") == skill_name
            and (c.get("generation_error") or c.get("judge_error"))
        )

        summary_result = extract_summary(skill_name)
        full_body = _common.load_skill_body(skill_name)

        summary[skill_name] = {
            "size_tier": tier,
            "body_bytes": body_bytes,
            "full_bytes": len(full_body.encode("utf-8")) if full_body else 0,
            "full_tokens_estimated": estimate_tokens(full_body) if full_body else 0,
            "summary_bytes": summary_result[1] if summary_result else 0,
            "summary_tokens_estimated": estimate_tokens(summary_result[0]) if summary_result else 0,
            "mean": round(overall_stats["mean"], 4),
            "stddev": round(overall_stats["stddev"], 4),
            "n": overall_stats["n"],
            "errors": error_count,
            "comparisons": comp_summaries,
        }

    meta["total_cost"] = round(total_cost, 6)
    if fail_fast:
        meta["fail_fast_reason"] = fail_fast_reason

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )

    # Print summary to stderr
    print(f"\n[size_impact] === Summary ===", file=sys.stderr)
    for skill_name, stats in summary.items():
        print(
            f"  {skill_name} (tier={stats['size_tier']}, "
            f"body={stats['body_bytes']}B, "
            f"full={stats['full_bytes']}B/~{stats['full_tokens_estimated']}tok, "
            f"summary={stats['summary_bytes']}B/~{stats['summary_tokens_estimated']}tok):",
            file=sys.stderr,
        )
        for comp_type, comp_stats in stats.get("comparisons", {}).items():
            print(
                f"    {comp_type}: mean={comp_stats['mean']:+.4f} "
                f"(stddev={comp_stats['stddev']:.4f}, n={comp_stats['n']})",
                file=sys.stderr,
            )

    print(f"\n[size_impact] Total cost: ${total_cost:.4f}", file=sys.stderr)
    print(f"  Total calls: {total_calls_count}", file=sys.stderr)
    print(
        f"[size_impact] Results written to: {output_path}", file=sys.stderr
    )

    # Emit runner output contract on stdout
    print(f"TOTAL_CALLS={total_calls_count}")
    print(f"COST_USD={total_cost:.4f}")
    print(f"ABORTED={'1' if aborted else '0'}")
    print(f"N_CASES={len(cases)}")
    print(f"FAIL_FAST={'1' if fail_fast else '0'}")
    if fail_fast:
        print(f"FAIL_FAST_REASON={fail_fast_reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
