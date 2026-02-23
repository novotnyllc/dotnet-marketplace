#!/usr/bin/env python3
"""Baseline comparison utility -- informational regression detection.

Compares eval results against stored baselines and reports regressions
to stdout. Always exits 0 (informational only, does not gate CI).

Usage:
    python tests/evals/compare_baseline.py
    python tests/evals/compare_baseline.py --results-dir tests/evals/results
    python tests/evals/compare_baseline.py --eval-type effectiveness

Exit codes:
    0 - Always (informational only)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402


def load_latest_result(results_dir: Path, eval_type: str) -> dict | None:
    """Find and load the most recent results file for an eval type."""
    candidates = sorted(
        (p for p in results_dir.iterdir() if p.name.startswith(f"{eval_type}_") and p.suffix == ".json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None
    with open(candidates[0]) as f:
        return json.load(f)


def load_baseline(baselines_dir: Path, eval_type: str) -> dict | None:
    """Load baseline file for an eval type."""
    baseline_path = baselines_dir / f"{eval_type}_baseline.json"
    if not baseline_path.is_file():
        return None
    with open(baseline_path) as f:
        return json.load(f)


def compare_effectiveness(result: dict, baseline: dict, thresholds: dict) -> list[str]:
    """Compare effectiveness results against baseline."""
    findings: list[str] = []
    min_cases = thresholds.get("min_cases_before_compare", 3)
    mean_drop = thresholds.get("mean_drop_threshold", 0.5)
    stddev_mult = thresholds.get("stddev_multiplier", 2)

    result_summary = result.get("summary", {})
    baseline_summary = baseline.get("summary", {})

    for entity_id, current in result_summary.items():
        if entity_id not in baseline_summary:
            findings.append(f"  NEW: {entity_id} (no baseline, not a regression)")
            continue
        base = baseline_summary[entity_id]
        cur_n = current.get("n", 0)
        base_n = base.get("n", 0)
        if cur_n < min_cases or base_n < min_cases:
            continue
        cur_mean = current.get("mean", 0)
        base_mean = base.get("mean", 0)
        base_stddev = base.get("stddev", 0)
        drop = base_mean - cur_mean
        if drop > mean_drop and drop > stddev_mult * base_stddev:
            findings.append(
                f"  REGRESSION: {entity_id} mean dropped {base_mean:.2f} -> {cur_mean:.2f} "
                f"(drop={drop:.2f}, threshold={mean_drop}, {stddev_mult}*stddev={stddev_mult * base_stddev:.2f})"
            )

    return findings


def compare_activation(result: dict, baseline: dict, thresholds: dict) -> list[str]:
    """Compare activation results against baseline."""
    findings: list[str] = []
    min_cases = thresholds.get("min_cases_before_compare", 5)
    tpr_drop = thresholds.get("tpr_drop_threshold", 0.10)
    fpr_increase = thresholds.get("fpr_increase_threshold", 0.05)

    result_summary = result.get("summary", {})
    baseline_summary = baseline.get("summary", {})

    for entity_id, current in result_summary.items():
        if entity_id not in baseline_summary:
            findings.append(f"  NEW: {entity_id} (no baseline)")
            continue
        base = baseline_summary[entity_id]
        cur_n = current.get("n", 0)
        base_n = base.get("n", 0)
        if cur_n < min_cases or base_n < min_cases:
            continue

        cur_tpr = current.get("tpr", 0)
        base_tpr = base.get("tpr", 0)
        if base_tpr - cur_tpr > tpr_drop:
            findings.append(
                f"  REGRESSION: {entity_id} TPR dropped {base_tpr:.2f} -> {cur_tpr:.2f}"
            )

        cur_fpr = current.get("fpr", 0)
        base_fpr = base.get("fpr", 0)
        if cur_fpr - base_fpr > fpr_increase:
            findings.append(
                f"  REGRESSION: {entity_id} FPR increased {base_fpr:.2f} -> {cur_fpr:.2f}"
            )

    return findings


def compare_size_impact(result: dict, baseline: dict, thresholds: dict) -> list[str]:
    """Compare size impact results against baseline."""
    findings: list[str] = []
    min_cases = thresholds.get("min_cases_before_compare", 3)
    score_change = thresholds.get("score_change_threshold", 0.5)

    result_summary = result.get("summary", {})
    baseline_summary = baseline.get("summary", {})

    for entity_id, current in result_summary.items():
        if entity_id not in baseline_summary:
            findings.append(f"  NEW: {entity_id} (no baseline)")
            continue
        base = baseline_summary[entity_id]
        cur_n = current.get("n", 0)
        base_n = base.get("n", 0)
        if cur_n < min_cases or base_n < min_cases:
            continue
        cur_mean = current.get("mean", 0)
        base_mean = base.get("mean", 0)
        if abs(cur_mean - base_mean) > score_change:
            findings.append(
                f"  REGRESSION: {entity_id} score changed {base_mean:.2f} -> {cur_mean:.2f}"
            )

    return findings


def compare_confusion(result: dict, baseline: dict, thresholds: dict) -> list[str]:
    """Compare confusion matrix results against baseline."""
    findings: list[str] = []
    min_cases = thresholds.get("min_cases_before_compare", 5)
    change_threshold = thresholds.get("cross_activation_change_threshold", 0.10)

    result_summary = result.get("summary", {})
    baseline_summary = baseline.get("summary", {})

    for entity_id, current in result_summary.items():
        if entity_id not in baseline_summary:
            findings.append(f"  NEW: {entity_id} (no baseline)")
            continue
        base = baseline_summary[entity_id]
        cur_n = current.get("n", 0)
        base_n = base.get("n", 0)
        if cur_n < min_cases or base_n < min_cases:
            continue

        cur_cross = current.get("cross_activation_rate", 0)
        base_cross = base.get("cross_activation_rate", 0)
        if cur_cross - base_cross > change_threshold:
            findings.append(
                f"  REGRESSION: {entity_id} cross-activation increased "
                f"{base_cross:.2f} -> {cur_cross:.2f}"
            )

    return findings


_COMPARATORS = {
    "effectiveness": compare_effectiveness,
    "activation": compare_activation,
    "size_impact": compare_size_impact,
    "confusion": compare_confusion,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare eval results against baselines (informational, exit 0)"
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=None,
        help="Results directory (default: from config)",
    )
    parser.add_argument(
        "--baselines-dir",
        type=Path,
        default=None,
        help="Baselines directory (default: from config)",
    )
    parser.add_argument(
        "--eval-type",
        type=str,
        default=None,
        choices=["effectiveness", "activation", "size_impact", "confusion"],
        help="Compare only a specific eval type (default: all)",
    )
    args = parser.parse_args()

    cfg = _common.load_config()
    paths = cfg.get("paths", {})
    results_dir = args.results_dir or (_common.EVALS_DIR / paths.get("results_dir", "results"))
    baselines_dir = args.baselines_dir or (_common.EVALS_DIR / paths.get("baselines_dir", "baselines"))
    regression_cfg = cfg.get("regression", {})

    eval_types = [args.eval_type] if args.eval_type else list(_COMPARATORS.keys())
    total_findings: list[str] = []

    for eval_type in eval_types:
        if not results_dir.is_dir():
            print(f"[compare] No results directory: {results_dir}", file=sys.stderr)
            continue

        result = load_latest_result(results_dir, eval_type)
        if result is None:
            print(f"[compare] No results found for: {eval_type}", file=sys.stderr)
            continue

        baseline = load_baseline(baselines_dir, eval_type)
        if baseline is None:
            print(f"[compare] No baseline found for: {eval_type} (skipping comparison)", file=sys.stderr)
            continue

        thresholds = regression_cfg.get(eval_type, {})
        comparator = _COMPARATORS.get(eval_type)
        if comparator is None:
            continue

        findings = comparator(result, baseline, thresholds)
        if findings:
            print(f"\n[compare] === {eval_type.upper()} ===")
            for finding in findings:
                print(finding)
            total_findings.extend(findings)
        else:
            print(f"[compare] {eval_type}: no regressions detected")

    if total_findings:
        regression_count = sum(1 for f in total_findings if "REGRESSION" in f)
        new_count = sum(1 for f in total_findings if "NEW" in f)
        print(f"\n[compare] Summary: {regression_count} regression(s), {new_count} new coverage")
    else:
        print("\n[compare] No regressions detected across all eval types.")

    # Always exit 0 -- informational only
    return 0


if __name__ == "__main__":
    sys.exit(main())
