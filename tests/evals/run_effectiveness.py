#!/usr/bin/env python3
"""Effectiveness eval runner (L5) -- A/B comparison with LLM judge.

Compares outputs generated WITH and WITHOUT a skill's content loaded,
using rubric criteria to judge quality via an LLM judge.

Usage:
    python tests/evals/run_effectiveness.py --dry-run
    python tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3
    python tests/evals/run_effectiveness.py --cli codex
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
    cli_backend: str,
) -> str:
    """Compute a deterministic hash for a generation cache key.

    Includes all inputs that affect generation output to prevent
    silent stale cache reuse when parameters change.

    Args:
        skill_name: Name of the skill being evaluated.
        prompt_text: The user prompt text.
        run_index: The run iteration index (0-based).
        model: Generation model identifier (CLI-native string).
        temperature: Sampling temperature.
        skill_body: Injected skill body content (with delimiters).
        cli_backend: CLI backend name (claude, codex, copilot).

    Returns:
        Hex digest string used as the cache filename stem.
    """
    key = (
        f"{cli_backend}|{skill_name}|{prompt_text}|{run_index}"
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
        model: Model to use for generation (CLI-native string).
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

    Args:
        judge_parsed: Parsed judge JSON with 'criteria' and 'overall_winner'.
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
        help="List skills with rubrics and exit without CLI calls",
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
    parser.add_argument(
        "--cli",
        type=str,
        choices=["claude", "codex", "copilot"],
        default=None,
        help="Override CLI backend (default: from config.yaml)",
    )
    _common.add_limit_arg(parser)
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Validate --limit
    try:
        _common.validate_limit(args.limit)
    except Exception as exc:
        parser.error(str(exc))

    cfg = _common.load_config()

    # Determine which skills to evaluate
    if args.skill:
        skills = [args.skill]
        rubric = _common.load_rubric(args.skill)
        if rubric is None:
            print(
                f"[effectiveness] No rubric found for skill: {args.skill}",
                file=sys.stderr,
            )
            print(f"TOTAL_CALLS=0")
            print(f"COST_USD=0.0")
            print(f"ABORTED=0")
            print(f"N_CASES=0")
            print(f"FAIL_FAST=0")
            return 0
    else:
        skills = _common.list_skills_with_rubrics()

    if not skills:
        print(
            "[effectiveness] No skills with rubrics found. Nothing to evaluate.",
            file=sys.stderr,
        )
        print(f"TOTAL_CALLS=0")
        print(f"COST_USD=0.0")
        print(f"ABORTED=0")
        print(f"N_CASES=0")
        print(f"FAIL_FAST=0")
        return 0

    # Apply --limit to skills (N skills, each retains all prompts x runs)
    if args.limit is not None:
        seed = args.seed if args.seed is not None else cfg.get("rng", {}).get("default_seed", 42)
        _common.apply_limit_warning(args.limit, "effectiveness")
        skills = _common.apply_limit_to_items(
            skills, args.limit, seed, "effectiveness"
        )

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
            "[effectiveness] Dry run complete. No CLI calls made.",
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
        eval_type="effectiveness",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
        cli=args.cli,
        limit=args.limit,
    )
    temperature = cfg.get("temperature", 0.0)
    max_cost = cfg.get("cost", {}).get("max_cost_per_run", 5.0)
    max_calls = cfg.get("cost", {}).get("max_calls_per_run", 500)
    seed = meta["seed"]
    cli_backend = meta["backend"]

    print(
        f"[effectiveness] Starting eval run {meta['run_id']}", file=sys.stderr
    )
    print(
        f"[effectiveness] Backend: {cli_backend}, Skills: {len(skills)}, Runs per prompt: {args.runs}",
        file=sys.stderr,
    )
    print(
        f"[effectiveness] Model: {meta['model']}, Judge: {meta['judge_model']}, Seed: {seed}",
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
    total_calls = 0
    aborted = False
    fail_fast = False
    fail_fast_reason = ""
    cases: list[dict] = []
    # Collect per-skill improvement values for summary stats
    skill_improvements: dict[str, list[float]] = {s: [] for s in skills}
    skill_wins: dict[str, dict[str, int]] = {
        s: {"enhanced": 0, "baseline": 0, "tie": 0, "error": 0} for s in skills
    }

    # Fail-fast tracker
    ff_cfg = cfg.get("fail_fast", {})
    ff_threshold = ff_cfg.get("consecutive_threshold", 3)
    ff_enabled = ff_cfg.get("enabled", True)
    tracker = _common.ConsecutiveFailureTracker(threshold=ff_threshold)

    for run_idx in range(args.runs):
        if aborted:
            break

        # Reset tracker at start of each run iteration
        tracker.reset()

        for skill_name in skills:
            if aborted:
                break

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
                # Dual abort check
                if total_cost >= max_cost or total_calls >= max_calls:
                    print(
                        f"[effectiveness] ABORT: Limit exceeded "
                        f"(cost=${total_cost:.4f}/{max_cost}, "
                        f"calls={total_calls}/{max_calls})",
                        file=sys.stderr,
                    )
                    aborted = True
                    break

                phash = _prompt_hash(
                    skill_name, user_prompt, run_idx,
                    meta["model"], temperature, skill_body,
                    cli_backend,
                )
                case_id = f"{skill_name}/{prompt_idx}/{run_idx}"

                print(
                    f"[effectiveness] Evaluating {case_id} ...",
                    file=sys.stderr,
                )

                # Budget check closure (captures mutable locals)
                def _budget_exceeded(pending_calls: int = 0) -> bool:
                    return total_cost >= max_cost or (total_calls + pending_calls) >= max_calls

                # --- Generation phase ---
                gen_cost = 0.0
                gen_calls = 0
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
                        enhanced_text, e_cost, e_calls = _generate_code(
                            enhanced_system,
                            user_prompt,
                            meta["model"],
                            temperature,
                            cli=args.cli,
                            budget_check=_budget_exceeded,
                        )
                        gen_cost += e_cost
                        gen_calls += e_calls
                        total_cost += e_cost
                        total_calls += e_calls
                    except Exception as exc:
                        generation_error = f"enhanced generation failed: {exc}"
                        enhanced_text = ""
                        # Account for CLI calls consumed by failed retries
                        total_calls += int(getattr(exc, "calls_consumed", 0))
                        # Track consecutive failures for fail-fast
                        if ff_enabled and tracker.record_failure(exc):
                            fail_fast = True
                            fail_fast_reason = tracker.last_fingerprint
                            print(
                                f"[effectiveness] FAIL_FAST: {ff_threshold} consecutive "
                                f"same-error failures -- aborting",
                                file=sys.stderr,
                            )

                    # Cap check before baseline generation
                    if not generation_error and _budget_exceeded():
                        aborted = True
                        break

                    if not generation_error:
                        try:
                            baseline_text, b_cost, b_calls = _generate_code(
                                BASELINE_SYSTEM_PROMPT,
                                user_prompt,
                                meta["model"],
                                temperature,
                                cli=args.cli,
                                budget_check=_budget_exceeded,
                            )
                            gen_cost += b_cost
                            gen_calls += b_calls
                            total_cost += b_cost
                            total_calls += b_calls
                        except Exception as exc:
                            generation_error = f"baseline generation failed: {exc}"
                            baseline_text = ""
                            # Account for CLI calls consumed by failed retries
                            total_calls += int(getattr(exc, "calls_consumed", 0))
                            # Track consecutive failures for fail-fast
                            if ff_enabled and tracker.record_failure(exc):
                                fail_fast = True
                                fail_fast_reason = tracker.last_fingerprint
                                print(
                                    f"[effectiveness] FAIL_FAST: {ff_threshold} consecutive "
                                    f"same-error failures -- aborting",
                                    file=sys.stderr,
                                )

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
                    if fail_fast:
                        aborted = True
                        break
                    continue

                # --- A/B randomization ---
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
                # Cap check before starting judge
                if _budget_exceeded():
                    aborted = True
                    break

                judge_result: Optional[dict] = None
                try:
                    judge_result = judge_prompt.invoke_judge(
                        user_prompt=user_prompt,
                        response_a=response_a,
                        response_b=response_b,
                        criteria=criteria,
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
                            f"[effectiveness] FAIL_FAST: {ff_threshold} consecutive "
                            f"same-error failures -- aborting",
                            file=sys.stderr,
                        )

                total_cost += judge_result["cost"]
                total_calls += judge_result.get("calls", 0)

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
                    if fail_fast:
                        aborted = True
                        break
                    continue

                # Remap scores based on A/B assignment
                parsed = judge_result["parsed"]
                assert parsed is not None

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

                # Successful case -- reset consecutive failure counter
                tracker.record_success()

                cases.append(case_record)

            if aborted:
                break

        if aborted:
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
    meta["aborted"] = aborted
    if fail_fast:
        meta["fail_fast_reason"] = fail_fast_reason

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )

    # Print summary to stderr
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
    print(f"  Total calls: {total_calls}", file=sys.stderr)
    print(f"[effectiveness] Results written to: {output_path}", file=sys.stderr)

    # Emit runner output contract on stdout
    print(f"TOTAL_CALLS={total_calls}")
    print(f"COST_USD={total_cost:.4f}")
    print(f"ABORTED={'1' if aborted else '0'}")
    print(f"N_CASES={len(cases)}")
    print(f"FAIL_FAST={'1' if fail_fast else '0'}")
    if fail_fast:
        print(f"FAIL_FAST_REASON={fail_fast_reason}")
        print(f"FAIL_FAST_PERMANENT={'1' if tracker.breached_permanent else '0'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
