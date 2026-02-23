#!/usr/bin/env python3
"""Confusion matrix eval runner (L4) -- disambiguation quality testing.

Tests whether overlapping skills within domain groups cause misrouting,
building NxN confusion matrices per group.

Usage:
    python tests/evals/run_confusion_matrix.py --dry-run
    python tests/evals/run_confusion_matrix.py --group testing
    python tests/evals/run_confusion_matrix.py --model claude-sonnet-4-20250514

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
        description="Confusion matrix eval runner (L4) -- disambiguation quality"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show dataset groups and exit without API calls",
    )
    parser.add_argument(
        "--group",
        type=str,
        default=None,
        help="Evaluate a single domain group by name",
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
    confusion_dir = datasets_dir / "confusion"

    if args.dry_run:
        # Count JSONL groups
        group_count = 0
        case_count = 0
        groups: list[str] = []
        if confusion_dir.is_dir():
            for p in sorted(confusion_dir.iterdir()):
                if p.suffix == ".jsonl":
                    group_count += 1
                    groups.append(p.stem)
                    with open(p) as f:
                        case_count += sum(
                            1 for line in f if line.strip() and not line.startswith("#")
                        )
        print(
            f"[confusion] Dry run -- {group_count} group(s), {case_count} case(s) in dataset",
            file=sys.stderr,
        )
        if groups:
            for g in groups:
                print(f"  group: {g}", file=sys.stderr)
        if args.group:
            print(f"[confusion] Filter: --group {args.group}", file=sys.stderr)
        print("[confusion] Dry run complete. No API calls made.", file=sys.stderr)
        return 0

    # --- Full eval execution (to be implemented in task .7) ---
    meta = _common.build_run_metadata(
        eval_type="confusion",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
    )

    print(f"[confusion] Starting eval run {meta['run_id']}", file=sys.stderr)
    print(f"[confusion] Model: {meta['model']}", file=sys.stderr)

    # Placeholder: actual confusion matrix logic added in task .7
    summary: dict = {}
    cases: list[dict] = []
    artifacts: dict = {"confusion_matrices": {}}

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=cases,
        output_dir=args.output_dir,
        artifacts=artifacts,
    )
    print(f"[confusion] Results written to: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
