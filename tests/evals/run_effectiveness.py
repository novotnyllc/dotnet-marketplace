#!/usr/bin/env python3
"""Effectiveness eval runner (L5) -- A/B comparison with LLM judge.

Compares outputs generated WITH and WITHOUT a skill's content loaded,
using rubric criteria to judge quality via an LLM judge.

Usage:
    python tests/evals/run_effectiveness.py --dry-run
    python tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3
    python tests/evals/run_effectiveness.py --model claude-sonnet-4-20250514
    python tests/evals/run_effectiveness.py --regenerate

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import hashlib
import json
import math
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure evals package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402
import judge_prompt  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ENHANCED_SYSTEM_TEMPLATE = """\
You are an expert .NET developer. Use the following skill reference material \
to inform your response.

{skill_body}

Respond with well-structured, production-quality .NET code and clear explanations."""

BASELINE_SYSTEM_PROMPT = """\
You are an expert .NET developer. Respond with well-structured, \
production-quality .NET code and clear explanations."""


# ---------------------------------------------------------------------------
# Generation helpers
# ---------------------------------------------------------------------------


def _prompt_hash(
    skill_name: str,
    prompt_text: str,
    run_index: int,
    model: str,
    temperature: float,
    skill_body: str,
) -> str:
    """Compute a deterministic hash for a generation cache key.

    Includes all inputs that affect generation output to prevent
    silent stale cache reuse when parameters change.

    Args:
        skill_name: Name of the skill being evaluated.
        prompt_text: The user prompt text.
        run_index: The run iteration index (0-based).
        model: Generation model identifier.
        temperature: Sampling temperature.
        skill_body: Injected skill body content (with delimiters).

    Returns:
        Hex digest string used as the cache filename stem.
    """
    key = (
        f"{skill_name}|{prompt_text}|{run_index}"
        f"|{model}|{temperature}|{hashlib.sha256(skill_body.encode()).hexdigest()[:12]}"
    )
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def _generations_dir(output_dir: Path) -> Path:
    """Return the generations cache directory, creating it if needed.

    Args:
        output_dir: The results output directory.

    Returns:
        Path to the generations subdirectory.
    """
    d = output_dir / "generations"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load_cached_generation(
    gen_dir: Path, skill_name: str, phash: str
) -> Optional[dict]:
    """Load a cached generation from disk if it exists and is valid.

    Validates that the cached data contains the required 'enhanced' and
    'baseline' keys with string values. Returns None (cache miss) if the
    file is missing, corrupt, or has an unexpected shape.

    Args:
        gen_dir: Generations directory.
        skill_name: Skill name (subdirectory).
        phash: Prompt hash (filename stem).

    Returns:
        Parsed dict with 'enhanced' and 'baseline' string keys, or None.
    """
    cache_path = gen_dir / skill_name / f"{phash}.json"
    if not cache_path.is_file():
        return None
    try:
        with open(cache_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    # Validate expected shape
    if not isinstance(data, dict):
        return None
    if not isinstance(data.get("enhanced"), str):
        return None
    if not isinstance(data.get("baseline"), str):
        return None

    return data


def _save_generation(
    gen_dir: Path,
    skill_name: str,
    phash: str,
    enhanced_text: str,
    baseline_text: str,
    gen_cost: float,
    model: str,
) -> None:
    """Save generation outputs to disk for resume/replay.

    Args:
        gen_dir: Generations directory.
        skill_name: Skill name (subdirectory).
        phash: Prompt hash (filename stem).
        enhanced_text: Generated output with skill content.
        baseline_text: Generated output without skill content.
        gen_cost: Total generation cost for this pair.
        model: Model used for generation.
    """
    skill_dir = gen_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    cache_data = {
        "enhanced": enhanced_text,
        "baseline": baseline_text,
        "cost": gen_cost,
        "model": model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(skill_dir / f"{phash}.json", "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=2)


def _generate_code(
    client,
    system_prompt: str,
    user_prompt: str,
    model: str,
    temperature: float,
) -> tuple[str, float]:
    """Generate code using the Anthropic API.

    Args:
        client: Anthropic client instance.
        system_prompt: System prompt for the generation.
        user_prompt: User prompt to generate code for.
        model: Model to use for generation.
        temperature: Sampling temperature.

    Returns:
        Tuple of (generated_text, cost).
    """
    def _call():
        return client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

    response = _common.retry_with_backoff(_call)
    text = response.content[0].text if response.content else ""
    usage = response.usage
    cost = _common.track_cost(model, usage.input_tokens, usage.output_tokens)
    return text, cost


# ---------------------------------------------------------------------------
# Statistics helpers
# ---------------------------------------------------------------------------


def _compute_stats(values: list[float]) -> dict:
    """Compute mean, stddev, and n for a list of numeric values.

    Args:
        values: List of float values.

    Returns:
        Dict with 'mean', 'stddev', 'n' keys.
    """
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "stddev": 0.0, "n": 0}
    mean = sum(values) / n
    if n < 2:
        return {"mean": mean, "stddev": 0.0, "n": n}
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return {"mean": mean, "stddev": math.sqrt(variance), "n": n}


def _compute_case_scores(judge_parsed: dict, criteria: list[dict]) -> dict:
    """Compute weighted scores from judge output.

    Assumes judge output has already been validated by
    judge_prompt._validate_judge_response(), which ensures all expected
    criteria are present with valid scores. No normalization is performed;
    if criteria are missing or weights don't sum to 1.0, that indicates
    a validation gap upstream.

    Args:
        judge_parsed: Parsed judge JSON with 'criteria' and 'overall_winner'.
            The caller must have already remapped score_a/score_b so that
            score_a = enhanced and score_b = baseline.
        criteria: Rubric criteria list with 'name' and 'weight'.

    Returns:
        Dict with 'enhanced_score', 'baseline_score', 'improvement',
        'winner', and 'per_criterion' breakdown.
    """
    weight_map = {c["name"]: c["weight"] for c in criteria}
    judge_criteria = judge_parsed.get("criteria", [])

    enhanced_weighted = 0.0
    baseline_weighted = 0.0
    per_criterion = []

    for jc in judge_criteria:
        name = jc.get("name", "")
        weight = weight_map.get(name, 0.0)
        score_a = jc.get("score_a", 0)
        score_b = jc.get("score_b", 0)
        reasoning = jc.get("reasoning", "")

        per_criterion.append({
            "name": name,
            "weight": weight,
            "score_a": score_a,
            "score_b": score_b,
            "reasoning": reasoning,
        })

        enhanced_weighted += score_a * weight
        baseline_weighted += score_b * weight

    improvement = enhanced_weighted - baseline_weighted
    if enhanced_weighted > baseline_weighted:
        winner = "enhanced"
    elif baseline_weighted > enhanced_weighted:
        winner = "baseline"
    else:
        winner = "tie"

    return {
        "enhanced_score": round(enhanced_weighted, 4),
        "baseline_score": round(baseline_weighted, 4),
        "improvement": round(improvement, 4),
        "winner": winner,
        "per_criterion": per_criterion,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Effectiveness eval runner (L5) -- A/B comparison with LLM judge"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List skills with rubrics and exit without API calls",
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Evaluate a single skill by name (default: all with rubrics)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override generation model",
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
        help="Number of evaluation runs per prompt (default: 1)",
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
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    cfg = _common.load_config()

    # Determine which skills to evaluate
    if args.skill:
        skills = [args.skill]
        # Verify rubric exists
        rubric = _common.load_rubric(args.skill)
        if rubric is None:
            print(
                f"[effectiveness] No rubric found for skill: {args.skill}",
                file=sys.stderr,
            )
            return 0
    else:
        skills = _common.list_skills_with_rubrics()

    if not skills:
        print(
            "[effectiveness] No skills with rubrics found. Nothing to evaluate.",
            file=sys.stderr,
        )
        return 0

    if args.dry_run:
        print(
            f"[effectiveness] Dry run -- {len(skills)} skill(s) with rubrics:",
            file=sys.stderr,
        )
        for skill_name in skills:
            rubric = _common.load_rubric(skill_name)
            prompt_count = len(rubric.get("test_prompts", [])) if rubric else 0
            criteria_count = len(rubric.get("criteria", [])) if rubric else 0
            print(
                f"  {skill_name}: {prompt_count} prompt(s), {criteria_count} criteria",
                file=sys.stderr,
            )
        print(
            f"[effectiveness] Would run {args.runs} run(s) per prompt.",
            file=sys.stderr,
        )
        print(
            "[effectiveness] Dry run complete. No API calls made.",
            file=sys.stderr,
        )
        return 0

    # --- Full eval execution ---
    meta = _common.build_run_metadata(
        eval_type="effectiveness",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )
    temperature = cfg.get("temperature", 0.0)
    max_cost = cfg.get("cost", {}).get("max_cost_per_run", 15.0)
    seed = meta["seed"]

    print(
        f"[effectiveness] Starting eval run {meta['run_id']}", file=sys.stderr
    )
    print(
        f"[effectiveness] Skills: {len(skills)}, Runs per prompt: {args.runs}",
        file=sys.stderr,
    )
    print(
        f"[effectiveness] Model: {meta['model']}, Judge: {meta['judge_model']}, Seed: {seed}",
        file=sys.stderr,
    )

    # Set up client and output paths
    client = _common.get_client()
    results_dir = (
        args.output_dir
        if args.output_dir is not None
        else _common.EVALS_DIR
        / cfg.get("paths", {}).get("results_dir", "results")
    )
    results_dir.mkdir(parents=True, exist_ok=True)
    gen_dir = _generations_dir(results_dir)

    total_cost = 0.0
    cases: list[dict] = []
    # Collect per-skill improvement values for summary stats
    skill_improvements: dict[str, list[float]] = {s: [] for s in skills}
    skill_wins: dict[str, dict[str, int]] = {
        s: {"enhanced": 0, "baseline": 0, "tie": 0, "error": 0} for s in skills
    }

    for skill_name in skills:
        rubric = _common.load_rubric(skill_name)
        if rubric is None:
            continue

        skill_body = _common.load_skill_body(skill_name)
        if skill_body is None:
            print(
                f"[effectiveness] WARN: Skill body not found for {skill_name}, skipping",
                file=sys.stderr,
            )
            continue

        test_prompts = rubric.get("test_prompts", [])
        criteria = rubric.get("criteria", [])

        enhanced_system = ENHANCED_SYSTEM_TEMPLATE.format(skill_body=skill_body)

        for prompt_idx, user_prompt in enumerate(test_prompts):
            for run_idx in range(args.runs):
                # Check cost limit
                if total_cost >= max_cost:
                    print(
                        f"[effectiveness] ABORT: Cost limit ${max_cost:.2f} exceeded "
                        f"(spent ${total_cost:.4f})",
                        file=sys.stderr,
                    )
                    break

                phash = _prompt_hash(
                    skill_name, user_prompt, run_idx,
                    meta["model"], temperature, skill_body,
                )
                case_id = f"{skill_name}/{prompt_idx}/{run_idx}"

                print(
                    f"[effectiveness] Evaluating {case_id} ...",
                    file=sys.stderr,
                )

                # --- Generation phase ---
                gen_cost = 0.0
                enhanced_text = ""
                baseline_text = ""
                generation_error: Optional[str] = None

                cached = None
                if not args.regenerate:
                    cached = _load_cached_generation(gen_dir, skill_name, phash)

                if cached is not None:
                    enhanced_text = cached["enhanced"]
                    baseline_text = cached["baseline"]
                    print(
                        f"[effectiveness]   Using cached generation for {phash}",
                        file=sys.stderr,
                    )
                else:
                    try:
                        enhanced_text, e_cost = _generate_code(
                            client,
                            enhanced_system,
                            user_prompt,
                            meta["model"],
                            temperature,
                        )
                        gen_cost += e_cost
                    except Exception as exc:
                        generation_error = f"enhanced generation failed: {exc}"
                        enhanced_text = ""

                    try:
                        baseline_text, b_cost = _generate_code(
                            client,
                            BASELINE_SYSTEM_PROMPT,
                            user_prompt,
                            meta["model"],
                            temperature,
                        )
                        gen_cost += b_cost
                    except Exception as exc:
                        if generation_error:
                            generation_error += f"; baseline generation failed: {exc}"
                        else:
                            generation_error = f"baseline generation failed: {exc}"
                        baseline_text = ""

                    total_cost += gen_cost

                    # Save generations for resume/replay
                    if not generation_error:
                        _save_generation(
                            gen_dir,
                            skill_name,
                            phash,
                            enhanced_text,
                            baseline_text,
                            gen_cost,
                            meta["model"],
                        )

                # Handle empty/refusal
                if not enhanced_text.strip() or not baseline_text.strip():
                    if not generation_error:
                        generation_error = "empty or refusal response"

                if generation_error:
                    cases.append({
                        "id": case_id,
                        "entity_id": skill_name,
                        "skill_name": skill_name,
                        "prompt": user_prompt,
                        "run_index": run_idx,
                        "generation_error": generation_error,
                        "model": meta["model"],
                        "judge_model": meta["judge_model"],
                        "run_id": meta["run_id"],
                        "seed": seed,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "cost": gen_cost,
                    })
                    skill_wins[skill_name]["error"] += 1
                    continue

                # --- A/B randomization ---
                # Derive case_seed from a stable hash of identifying fields
                # so A/B assignment is reproducible regardless of iteration
                # order (--skill X matches the same assignment from a full run)
                seed_input = f"{seed}|{skill_name}|{prompt_idx}|{run_idx}"
                case_seed = int(
                    hashlib.sha256(seed_input.encode()).hexdigest()[:8], 16
                )
                case_rng = random.Random(case_seed)
                enhanced_is_a = case_rng.random() < 0.5

                if enhanced_is_a:
                    response_a = enhanced_text
                    response_b = baseline_text
                    ab_assignment = "enhanced=A,baseline=B"
                else:
                    response_a = baseline_text
                    response_b = enhanced_text
                    ab_assignment = "enhanced=B,baseline=A"

                # --- Judge phase ---
                judge_result: Optional[dict] = None
                try:
                    judge_result = judge_prompt.invoke_judge(
                        client=client,
                        user_prompt=user_prompt,
                        response_a=response_a,
                        response_b=response_b,
                        criteria=criteria,
                        judge_model=meta["judge_model"],
                        temperature=temperature,
                    )
                except Exception as exc:
                    judge_result = {
                        "parsed": None,
                        "raw_judge_text": "",
                        "cost": 0.0,
                        "attempts": 0,
                        "judge_error": f"judge invocation failed: {exc}",
                    }

                total_cost += judge_result["cost"]

                case_record: dict = {
                    "id": case_id,
                    "entity_id": skill_name,
                    "skill_name": skill_name,
                    "prompt": user_prompt,
                    "run_index": run_idx,
                    "model": meta["model"],
                    "judge_model": meta["judge_model"],
                    "run_id": meta["run_id"],
                    "seed": seed,
                    "case_seed": case_seed,
                    "ab_assignment": ab_assignment,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "cost": gen_cost + judge_result["cost"],
                    "judge_attempts": judge_result["attempts"],
                }

                if judge_result["judge_error"]:
                    case_record["judge_error"] = judge_result["judge_error"]
                    case_record["raw_judge_text"] = judge_result["raw_judge_text"]
                    skill_wins[skill_name]["error"] += 1
                    cases.append(case_record)
                    continue

                # Remap scores based on A/B assignment
                parsed = judge_result["parsed"]
                assert parsed is not None  # guaranteed if no judge_error

                # Remap: score_a/score_b in judge output -> enhanced/baseline
                remapped_criteria = []
                for jc in parsed.get("criteria", []):
                    if enhanced_is_a:
                        enhanced_score = jc.get("score_a", 0)
                        baseline_score = jc.get("score_b", 0)
                    else:
                        enhanced_score = jc.get("score_b", 0)
                        baseline_score = jc.get("score_a", 0)
                    remapped_criteria.append({
                        "name": jc.get("name", ""),
                        "score_a": jc.get("score_a", 0),
                        "score_b": jc.get("score_b", 0),
                        "enhanced_score": enhanced_score,
                        "baseline_score": baseline_score,
                        "reasoning": jc.get("reasoning", ""),
                    })

                # Build a remapped parsed dict for scoring
                remapped_parsed = {
                    "criteria": [
                        {
                            "name": rc["name"],
                            "score_a": rc["enhanced_score"],
                            "score_b": rc["baseline_score"],
                            "reasoning": rc["reasoning"],
                        }
                        for rc in remapped_criteria
                    ],
                    "overall_winner": parsed.get("overall_winner", "tie"),
                }

                scores = _compute_case_scores(remapped_parsed, criteria)

                case_record["scores"] = {
                    "enhanced_score": scores["enhanced_score"],
                    "baseline_score": scores["baseline_score"],
                    "improvement": scores["improvement"],
                    "winner": scores["winner"],
                }
                case_record["per_criterion_breakdown"] = remapped_criteria

                skill_improvements[skill_name].append(scores["improvement"])
                skill_wins[skill_name][scores["winner"]] += 1

                cases.append(case_record)

            # Check cost limit after each run batch
            if total_cost >= max_cost:
                print(
                    f"[effectiveness] ABORT: Cost limit exceeded after {skill_name}",
                    file=sys.stderr,
                )
                break

        if total_cost >= max_cost:
            break

    # --- Build summary ---
    summary: dict[str, dict] = {}
    for skill_name in skills:
        improvements = skill_improvements.get(skill_name, [])
        wins = skill_wins.get(skill_name, {})
        stats = _compute_stats(improvements)
        total_cases = sum(wins.get(k, 0) for k in ("enhanced", "baseline", "tie", "error"))

        summary[skill_name] = {
            "mean": round(stats["mean"], 4),
            "stddev": round(stats["stddev"], 4),
            "n": stats["n"],
            "wins_enhanced": wins.get("enhanced", 0),
            "wins_baseline": wins.get("baseline", 0),
            "ties": wins.get("tie", 0),
            "errors": wins.get("error", 0),
            "total_cases": total_cases,
            "win_rate": (
                round(wins.get("enhanced", 0) / max(total_cases - wins.get("error", 0), 1), 4)
            ),
        }

    meta["total_cost"] = round(total_cost, 6)

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )

    # Print summary
    print(f"\n[effectiveness] === Summary ===", file=sys.stderr)
    for skill_name, stats in summary.items():
        print(
            f"  {skill_name}: mean_improvement={stats['mean']:+.4f} "
            f"(stddev={stats['stddev']:.4f}, n={stats['n']}) "
            f"wins={stats['wins_enhanced']}/{stats['total_cases']} "
            f"win_rate={stats['win_rate']:.2%}",
            file=sys.stderr,
        )
    print(f"\n[effectiveness] Total cost: ${total_cost:.4f}", file=sys.stderr)
    print(f"[effectiveness] Results written to: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
