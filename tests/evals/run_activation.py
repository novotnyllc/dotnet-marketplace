#!/usr/bin/env python3
"""Offline activation eval runner (L3) -- API-only skill routing test.

Builds a compressed routing index from skill frontmatter and tests
whether models correctly route prompts to the appropriate skills.

Usage:
    python tests/evals/run_activation.py --dry-run
    python tests/evals/run_activation.py --skill dotnet-xunit
    python tests/evals/run_activation.py --model claude-sonnet-4-20250514

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

# ---------------------------------------------------------------------------
# Routing index construction
# ---------------------------------------------------------------------------

_MAX_DESCRIPTION_CHARS = 120


def build_routing_index(skills_dir: Optional[Path] = None) -> tuple[str, int, int]:
    """Build a compressed routing index from skill frontmatter.

    Reads all skills under skills_dir, extracts id + description,
    truncates descriptions to 120 chars, and sorts by id for stable ordering.

    Args:
        skills_dir: Path to skills directory. Defaults to _common.SKILLS_DIR.

    Returns:
        Tuple of (index_text, skill_count, char_count).
    """
    resolved_dir = skills_dir or _common.SKILLS_DIR
    entries: list[tuple[str, str]] = []

    if not resolved_dir.is_dir():
        return "", 0, 0

    for skill_path in sorted(resolved_dir.iterdir()):
        if not skill_path.is_dir():
            continue
        skill_name = skill_path.name
        description = _common.load_skill_description(skill_name)
        if description is None:
            continue

        # Truncate to style guide limit
        if len(description) > _MAX_DESCRIPTION_CHARS:
            description = description[: _MAX_DESCRIPTION_CHARS - 3] + "..."

        entries.append((skill_name, description))

    lines = [f"- {skill_id}: {desc}" for skill_id, desc in entries]
    index_text = "\n".join(lines)
    return index_text, len(entries), len(index_text)


# ---------------------------------------------------------------------------
# System prompt for activation eval
# ---------------------------------------------------------------------------

_ACTIVATION_SYSTEM_PROMPT = """\
You are a skill router for a .NET development plugin. Given a skill index and \
a developer prompt, determine which skills (if any) should be activated.

Rules:
- Select ONLY skills that are directly relevant to the prompt.
- If no skill is relevant, return an empty skills list.
- Return your answer as JSON only, with no other text.

Required JSON format:
{{"skills": ["skill-id-1", "skill-id-2"], "reasoning": "Brief explanation"}}

Skill index:
{index}"""

_FALLBACK_SYSTEM_PROMPT = """\
You are a JSON classifier. Given a model response and a target skill ID, \
determine if the response indicates the skill should be activated.

Answer with ONLY this JSON (no other text):
{{"activated": true}} or {{"activated": false}}"""


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------


def load_dataset(
    datasets_dir: Path, skill_filter: Optional[str] = None
) -> list[dict]:
    """Load activation test cases from JSONL files.

    Args:
        datasets_dir: Path to the activation datasets directory.
        skill_filter: If set, only include cases where this skill
            appears in expected_skills or acceptable_skills.

    Returns:
        List of parsed test case dicts.
    """
    cases: list[dict] = []
    if not datasets_dir.is_dir():
        return cases

    for jsonl_path in sorted(datasets_dir.iterdir()):
        if jsonl_path.suffix != ".jsonl":
            continue
        with open(jsonl_path) as f:
            for line_num, line in enumerate(f, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                try:
                    case = json.loads(stripped)
                except json.JSONDecodeError:
                    print(
                        f"[activation] WARN: Invalid JSON at {jsonl_path.name}:{line_num}",
                        file=sys.stderr,
                    )
                    continue
                cases.append(case)

    if skill_filter:
        filtered = []
        for case in cases:
            expected = set(case.get("expected_skills", []))
            acceptable = set(case.get("acceptable_skills", []))
            all_relevant = expected | acceptable
            if skill_filter in all_relevant:
                filtered.append(case)
            elif not case.get("should_activate", True):
                # Keep negative controls (they test FPR for all skills)
                filtered.append(case)
        cases = filtered

    return cases


# ---------------------------------------------------------------------------
# Activation detection
# ---------------------------------------------------------------------------


def detect_activation_structured(
    response_text: str,
) -> tuple[Optional[list[str]], str]:
    """Parse structured JSON response to extract activated skill IDs.

    Primary detection path: parse the model's JSON response directly.

    Args:
        response_text: Raw model response text.

    Returns:
        Tuple of (skill_list_or_none, detection_method).
        detection_method is "structured" on success, "parse_failure" on failure.
    """
    parsed = _common.extract_json(response_text)
    if parsed is not None and "skills" in parsed:
        skills = parsed["skills"]
        if isinstance(skills, list) and all(isinstance(s, str) for s in skills):
            return skills, "structured"
    return None, "parse_failure"


def detect_activation_fallback(
    client,
    response_text: str,
    target_skill: str,
    judge_model: str,
    temperature: float,
) -> tuple[bool, float]:
    """LLM fallback detection for when structured parsing fails.

    Asks a fast model whether the response indicates the target skill
    should be used. This is a rare path -- only invoked on parse failures.

    Args:
        client: Anthropic client instance.
        response_text: The original model response that failed to parse.
        target_skill: The skill ID to check for.
        judge_model: Model to use for fallback classification.
        temperature: Sampling temperature.

    Returns:
        Tuple of (activated_bool, cost).
    """
    user_content = (
        f"Target skill: {target_skill}\n\n"
        f"Model response:\n{response_text[:2000]}"
    )

    def _call():
        return client.messages.create(
            model=judge_model,
            max_tokens=100,
            temperature=temperature,
            system=_FALLBACK_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )

    response = _common.retry_with_backoff(_call)
    text = response.content[0].text if response.content else ""
    usage = response.usage
    cost = _common.track_cost(judge_model, usage.input_tokens, usage.output_tokens)

    parsed = _common.extract_json(text)
    if parsed is not None:
        return bool(parsed.get("activated", False)), cost
    return False, cost


# ---------------------------------------------------------------------------
# Statistics
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


# ---------------------------------------------------------------------------
# Metrics computation
# ---------------------------------------------------------------------------


def compute_metrics(
    case_results: list[dict],
) -> tuple[dict, dict]:
    """Compute aggregate and per-skill activation metrics.

    Args:
        case_results: List of evaluated case result dicts.

    Returns:
        Tuple of (overall_metrics, per_skill_metrics).
    """
    # Aggregate counters
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0

    # Per-skill tracking
    per_skill_activated: dict[str, int] = {}
    per_skill_expected: dict[str, int] = {}
    per_skill_correct: dict[str, int] = {}

    for result in case_results:
        should_activate = result.get("should_activate", True)
        expected_skills = set(result.get("expected_skills", []))
        acceptable_skills = set(result.get("acceptable_skills", []))
        activated_skills = set(result.get("activated_skills", []))
        all_valid = expected_skills | acceptable_skills

        total_input_tokens += result.get("input_tokens", 0)
        total_output_tokens += result.get("output_tokens", 0)
        total_cost += result.get("cost", 0.0)

        if should_activate:
            # Positive case: check if at least one expected skill was activated
            hit = bool(activated_skills & all_valid)
            if hit:
                true_positives += 1
            else:
                false_negatives += 1

            # Track per-skill metrics
            for skill in expected_skills:
                per_skill_expected[skill] = per_skill_expected.get(skill, 0) + 1
                if skill in activated_skills:
                    per_skill_activated[skill] = per_skill_activated.get(skill, 0) + 1
                    per_skill_correct[skill] = per_skill_correct.get(skill, 0) + 1
        else:
            # Negative case: no skills should be activated
            if not activated_skills:
                true_negatives += 1
            else:
                false_positives += 1

    total_positive = true_positives + false_negatives
    total_negative = true_negatives + false_positives
    total = total_positive + total_negative

    tpr = true_positives / max(total_positive, 1)
    fpr = false_positives / max(total_negative, 1)
    accuracy = (true_positives + true_negatives) / max(total, 1)

    overall = {
        "tpr": round(tpr, 4),
        "fpr": round(fpr, 4),
        "accuracy": round(accuracy, 4),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "true_negatives": true_negatives,
        "false_negatives": false_negatives,
        "total_positive_cases": total_positive,
        "total_negative_cases": total_negative,
        "total_cases": total,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_cost": round(total_cost, 6),
    }

    # Per-skill activation rates
    per_skill: dict[str, dict] = {}
    for skill in sorted(set(per_skill_expected.keys()) | set(per_skill_activated.keys())):
        expected_count = per_skill_expected.get(skill, 0)
        activated_count = per_skill_activated.get(skill, 0)
        correct_count = per_skill_correct.get(skill, 0)
        per_skill[skill] = {
            "expected_count": expected_count,
            "activated_count": activated_count,
            "correct_count": correct_count,
            "activation_rate": round(
                activated_count / max(expected_count, 1), 4
            ),
        }

    return overall, per_skill


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline activation eval runner (L3) -- API-only skill routing"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show dataset stats and exit without API calls",
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Evaluate activation for a single skill",
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
        help="Override judge model (used for fallback detection only)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of evaluation runs per case (default: 1)",
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
    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cfg = _common.load_config()
    datasets_dir = (
        _common.EVALS_DIR
        / cfg.get("paths", {}).get("datasets_dir", "datasets")
        / "activation"
    )

    # Load dataset
    test_cases = load_dataset(datasets_dir, skill_filter=args.skill)

    if args.dry_run:
        positive = [c for c in test_cases if c.get("should_activate", True)]
        negative = [c for c in test_cases if not c.get("should_activate", True)]

        # Count unique expected skills
        expected_skills: set[str] = set()
        for c in positive:
            expected_skills.update(c.get("expected_skills", []))

        # Build index to report char_count
        index_text, skill_count, char_count = build_routing_index()

        print(
            f"[activation] Dry run -- {len(test_cases)} total case(s)",
            file=sys.stderr,
        )
        print(
            f"[activation]   Positive cases: {len(positive)} across "
            f"{len(expected_skills)} unique skills",
            file=sys.stderr,
        )
        print(
            f"[activation]   Negative controls: {len(negative)}",
            file=sys.stderr,
        )
        print(
            f"[activation]   Routing index: {skill_count} skills, "
            f"{char_count} chars",
            file=sys.stderr,
        )
        if args.skill:
            print(
                f"[activation]   Filter: --skill {args.skill}",
                file=sys.stderr,
            )
        print(
            "[activation] Dry run complete. No API calls made.",
            file=sys.stderr,
        )
        return 0

    # --- Full eval execution ---
    meta = _common.build_run_metadata(
        eval_type="activation",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )
    temperature = cfg.get("temperature", 0.0)
    max_cost = cfg.get("cost", {}).get("max_cost_per_run", 15.0)

    # Build routing index
    index_text, skill_count, index_char_count = build_routing_index()
    if skill_count == 0:
        print(
            "[activation] ERROR: No skills found in routing index.",
            file=sys.stderr,
        )
        return 0

    system_prompt = _ACTIVATION_SYSTEM_PROMPT.format(index=index_text)

    print(
        f"[activation] Starting eval run {meta['run_id']}", file=sys.stderr
    )
    print(
        f"[activation] Model: {meta['model']}, Cases: {len(test_cases)}, "
        f"Runs: {args.runs}",
        file=sys.stderr,
    )
    print(
        f"[activation] Routing index: {skill_count} skills, "
        f"{index_char_count} chars",
        file=sys.stderr,
    )

    client = _common.get_client()

    total_cost = 0.0
    all_case_results: list[dict] = []
    # For multi-run stats (per-case across runs)
    run_results_per_case: dict[str, list[dict]] = {}

    for run_idx in range(args.runs):
        if args.runs > 1:
            print(
                f"\n[activation] === Run {run_idx + 1}/{args.runs} ===",
                file=sys.stderr,
            )

        for case in test_cases:
            if total_cost >= max_cost:
                print(
                    f"[activation] ABORT: Cost limit ${max_cost:.2f} exceeded "
                    f"(spent ${total_cost:.4f})",
                    file=sys.stderr,
                )
                break

            case_id = case.get("id", "unknown")
            user_prompt = case.get("user_prompt", "")
            expected_skills = case.get("expected_skills", [])
            acceptable_skills = case.get("acceptable_skills", [])
            should_activate = case.get("should_activate", True)
            category = case.get("category", "unknown")

            run_case_id = f"{case_id}/run-{run_idx}" if args.runs > 1 else case_id

            print(
                f"[activation]   Evaluating {run_case_id} ...",
                file=sys.stderr,
            )

            # Call model with routing index + user prompt
            input_tokens = 0
            output_tokens = 0
            response_text = ""
            api_error: Optional[str] = None

            try:
                def _call():
                    return client.messages.create(
                        model=meta["model"],
                        max_tokens=512,
                        temperature=temperature,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_prompt}],
                    )

                response = _common.retry_with_backoff(_call)
                response_text = (
                    response.content[0].text if response.content else ""
                )
                usage = response.usage
                input_tokens = usage.input_tokens
                output_tokens = usage.output_tokens
                call_cost = _common.track_cost(
                    meta["model"], input_tokens, output_tokens
                )
                total_cost += call_cost
            except Exception as exc:
                api_error = str(exc)
                call_cost = 0.0

            # Detect activation
            activated_skills: list[str] = []
            detection_method = "error"

            if api_error is None:
                activated_skills_opt, detection_method = (
                    detect_activation_structured(response_text)
                )
                if activated_skills_opt is not None:
                    activated_skills = activated_skills_opt
                else:
                    # Fallback: use LLM to classify per expected skill
                    detection_method = "fallback"
                    if should_activate and expected_skills:
                        for target_skill in expected_skills:
                            activated, fb_cost = detect_activation_fallback(
                                client,
                                response_text,
                                target_skill,
                                meta["judge_model"],
                                temperature,
                            )
                            total_cost += fb_cost
                            if activated:
                                activated_skills.append(target_skill)

            # Determine pass/fail
            if should_activate:
                all_valid = set(expected_skills) | set(acceptable_skills)
                passed = bool(set(activated_skills) & all_valid)
            else:
                passed = len(activated_skills) == 0

            case_result = {
                "id": run_case_id,
                "entity_id": case_id,
                "user_prompt": user_prompt,
                "expected_skills": expected_skills,
                "acceptable_skills": acceptable_skills,
                "activated_skills": activated_skills,
                "should_activate": should_activate,
                "category": category,
                "detection_method": detection_method,
                "passed": passed,
                "run_index": run_idx,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": round(call_cost, 6),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            if api_error:
                case_result["api_error"] = api_error
                case_result["passed"] = False

            all_case_results.append(case_result)

            # Track for multi-run aggregation
            if case_id not in run_results_per_case:
                run_results_per_case[case_id] = []
            run_results_per_case[case_id].append(case_result)

        if total_cost >= max_cost:
            break

    # --- Compute metrics ---
    overall_metrics, per_skill_metrics = compute_metrics(all_case_results)

    # Build summary with mean/stddev/n for multi-run support
    if args.runs > 1:
        # Compute per-run metrics for stddev
        run_tprs: list[float] = []
        run_fprs: list[float] = []
        run_accuracies: list[float] = []

        for run_idx in range(args.runs):
            run_cases = [
                r for r in all_case_results if r.get("run_index") == run_idx
            ]
            if run_cases:
                run_overall, _ = compute_metrics(run_cases)
                run_tprs.append(run_overall["tpr"])
                run_fprs.append(run_overall["fpr"])
                run_accuracies.append(run_overall["accuracy"])

        tpr_stats = _compute_stats(run_tprs)
        fpr_stats = _compute_stats(run_fprs)
        accuracy_stats = _compute_stats(run_accuracies)
    else:
        tpr_stats = {
            "mean": overall_metrics["tpr"],
            "stddev": 0.0,
            "n": 1,
        }
        fpr_stats = {
            "mean": overall_metrics["fpr"],
            "stddev": 0.0,
            "n": 1,
        }
        accuracy_stats = {
            "mean": overall_metrics["accuracy"],
            "stddev": 0.0,
            "n": 1,
        }

    summary: dict = {
        "_overall": {
            "tpr": tpr_stats,
            "fpr": fpr_stats,
            "accuracy": accuracy_stats,
            "true_positives": overall_metrics["true_positives"],
            "false_positives": overall_metrics["false_positives"],
            "true_negatives": overall_metrics["true_negatives"],
            "false_negatives": overall_metrics["false_negatives"],
            "total_positive_cases": overall_metrics["total_positive_cases"],
            "total_negative_cases": overall_metrics["total_negative_cases"],
            "total_cases": overall_metrics["total_cases"],
            "index_char_count": index_char_count,
            "index_skill_count": skill_count,
            "total_input_tokens": overall_metrics["total_input_tokens"],
            "total_output_tokens": overall_metrics["total_output_tokens"],
        },
        **{
            skill: {
                "activation_rate": data["activation_rate"],
                "expected_count": data["expected_count"],
                "activated_count": data["activated_count"],
                "correct_count": data["correct_count"],
            }
            for skill, data in per_skill_metrics.items()
        },
    }

    meta["total_cost"] = round(total_cost, 6)

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=all_case_results,
        output_dir=args.output_dir,
        artifacts={
            "index_char_count": index_char_count,
            "index_skill_count": skill_count,
            "detection_method_counts": _detection_method_counts(all_case_results),
        },
    )

    # Print summary
    print(f"\n[activation] === Summary ===", file=sys.stderr)
    print(
        f"  TPR: {tpr_stats['mean']:.2%} (stddev={tpr_stats['stddev']:.4f}, "
        f"n={tpr_stats['n']})",
        file=sys.stderr,
    )
    print(
        f"  FPR: {fpr_stats['mean']:.2%} (stddev={fpr_stats['stddev']:.4f}, "
        f"n={fpr_stats['n']})",
        file=sys.stderr,
    )
    print(
        f"  Accuracy: {accuracy_stats['mean']:.2%} "
        f"(stddev={accuracy_stats['stddev']:.4f}, n={accuracy_stats['n']})",
        file=sys.stderr,
    )
    print(
        f"  Index: {skill_count} skills, {index_char_count} chars",
        file=sys.stderr,
    )
    print(
        f"  Token usage: {overall_metrics['total_input_tokens']} input, "
        f"{overall_metrics['total_output_tokens']} output",
        file=sys.stderr,
    )
    print(f"  Total cost: ${total_cost:.4f}", file=sys.stderr)
    print(f"\n[activation] Results written to: {output_path}", file=sys.stderr)
    return 0


def _detection_method_counts(cases: list[dict]) -> dict[str, int]:
    """Count occurrences of each detection method across cases.

    Args:
        cases: List of case result dicts.

    Returns:
        Dict mapping detection method name to count.
    """
    counts: dict[str, int] = {}
    for case in cases:
        method = case.get("detection_method", "unknown")
        counts[method] = counts.get(method, 0) + 1
    return counts


if __name__ == "__main__":
    sys.exit(main())
