#!/usr/bin/env python3
"""Effectiveness eval runner (L5) -- A/B comparison with LLM judge.

Compares outputs generated WITH and WITHOUT a skill's content loaded,
using rubric criteria to judge quality via an LLM judge.

Usage:
    python tests/evals/run_effectiveness.py --dry-run
    python tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3
    python tests/evals/run_effectiveness.py --model claude-sonnet-4-20250514

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import sys
from pathlib import Path

# Ensure evals package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402


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
    return parser


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
        print("[effectiveness] No skills with rubrics found. Nothing to evaluate.", file=sys.stderr)
        return 0

    if args.dry_run:
        print(f"[effectiveness] Dry run -- {len(skills)} skill(s) with rubrics:", file=sys.stderr)
        for skill_name in skills:
            rubric = _common.load_rubric(skill_name)
            prompt_count = len(rubric.get("test_prompts", [])) if rubric else 0
            criteria_count = len(rubric.get("criteria", [])) if rubric else 0
            print(
                f"  {skill_name}: {prompt_count} prompt(s), {criteria_count} criteria",
                file=sys.stderr,
            )
        print(f"[effectiveness] Would run {args.runs} run(s) per prompt.", file=sys.stderr)
        print("[effectiveness] Dry run complete. No API calls made.", file=sys.stderr)
        return 0

    # --- Full eval execution (to be implemented in task .3) ---
    meta = _common.build_run_metadata(
        eval_type="effectiveness",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )

    print(f"[effectiveness] Starting eval run {meta['run_id']}", file=sys.stderr)
    print(f"[effectiveness] Skills: {len(skills)}, Runs per prompt: {args.runs}", file=sys.stderr)
    print(
        f"[effectiveness] Model: {meta['model']}, Judge: {meta['judge_model']}",
        file=sys.stderr,
    )

    # Placeholder: actual generation + judging logic added in task .3
    summary: dict = {}
    cases: list[dict] = []

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )
    print(f"[effectiveness] Results written to: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
