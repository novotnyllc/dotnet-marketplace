#!/usr/bin/env python3
"""Size impact eval runner (L6) -- progressive disclosure validation.

Tests whether skill content format (full body vs summary vs none)
affects output quality, validating progressive disclosure decisions.

Usage:
    python tests/evals/run_size_impact.py --dry-run
    python tests/evals/run_size_impact.py --skill dotnet-xunit
    python tests/evals/run_size_impact.py --model claude-sonnet-4-20250514

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Size impact eval runner (L6) -- progressive disclosure validation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show candidate skills and exit without API calls",
    )
    parser.add_argument(
        "--skill",
        type=str,
        default=None,
        help="Evaluate a single skill by name",
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
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cfg = _common.load_config()
    datasets_dir = _common.EVALS_DIR / cfg.get("paths", {}).get("datasets_dir", "datasets")
    size_impact_dir = datasets_dir / "size_impact"

    # Determine candidate skills (those with rubrics)
    if args.skill:
        skills = [args.skill]
    else:
        skills = _common.list_skills_with_rubrics()

    if args.dry_run:
        print(
            f"[size_impact] Dry run -- {len(skills)} candidate skill(s):",
            file=sys.stderr,
        )
        for skill_name in skills:
            desc = _common.load_skill_description(skill_name)
            desc_preview = (desc[:60] + "...") if desc and len(desc) > 60 else (desc or "N/A")
            print(f"  {skill_name}: {desc_preview}", file=sys.stderr)
        print("[size_impact] Dry run complete. No API calls made.", file=sys.stderr)
        return 0

    # --- Full eval execution (to be implemented in task .6) ---
    meta = _common.build_run_metadata(
        eval_type="size_impact",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )

    print(f"[size_impact] Starting eval run {meta['run_id']}", file=sys.stderr)
    print(f"[size_impact] Skills: {len(skills)}, Runs per condition: {args.runs}", file=sys.stderr)

    # Placeholder: actual size impact eval logic added in task .6
    summary: dict = {}
    cases: list[dict] = []

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )
    print(f"[size_impact] Results written to: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
