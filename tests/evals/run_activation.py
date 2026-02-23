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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402


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
        help="Override judge model",
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


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cfg = _common.load_config()
    datasets_dir = _common.EVALS_DIR / cfg.get("paths", {}).get("datasets_dir", "datasets")
    activation_dir = datasets_dir / "activation"

    if args.dry_run:
        # Count JSONL cases
        case_count = 0
        if activation_dir.is_dir():
            for p in activation_dir.iterdir():
                if p.suffix == ".jsonl":
                    with open(p) as f:
                        case_count += sum(
                            1 for line in f if line.strip() and not line.startswith("#")
                        )
        print(f"[activation] Dry run -- {case_count} case(s) in dataset", file=sys.stderr)
        if args.skill:
            print(f"[activation] Filter: --skill {args.skill}", file=sys.stderr)
        print("[activation] Dry run complete. No API calls made.", file=sys.stderr)
        return 0

    # --- Full eval execution (to be implemented in task .5) ---
    meta = _common.build_run_metadata(
        eval_type="activation",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )

    print(f"[activation] Starting eval run {meta['run_id']}", file=sys.stderr)
    print(f"[activation] Model: {meta['model']}", file=sys.stderr)

    # Placeholder: actual activation eval logic added in task .5
    summary: dict = {}
    cases: list[dict] = []

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
    )
    print(f"[activation] Results written to: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
