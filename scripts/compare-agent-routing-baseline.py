#!/usr/bin/env python3
"""Compare agent-routing results for regressions.

Reads one or more results.json files (produced by check-skills.cs) and
checks every (case_id, provider) result against the uniform expectation:
all cases must pass and must not time out.

If an explicit baseline file exists, it is loaded and used instead.
Otherwise a synthetic all-pass baseline is generated from the result set.
Optionally compares against a git ref's baseline for regression detection.

Exit codes:
    0 - No regressions detected
    1 - Regressions or missing data detected
    2 - Usage error

Usage:
    python scripts/compare-agent-routing-baseline.py results1.json [results2.json ...]
    python scripts/compare-agent-routing-baseline.py --baseline-ref main results.json
    python scripts/compare-agent-routing-baseline.py --results-dir downloaded-artifacts/
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASELINE_PATH = REPO_ROOT / "tests" / "agent-routing" / "provider-baseline.json"
PROVIDERS = ["claude", "codex", "copilot"]


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_baseline_from_ref(ref: str, relative_path: str) -> dict | None:
    """Load provider-baseline.json from a git ref."""
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{relative_path}"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=30,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError):
        return None


def collect_results(paths: list[Path]) -> tuple[list[dict], list[str]]:
    """Collect all result tuples from one or more results.json files.

    Returns (tuples, errors) where errors lists any duplicate (case_id, agent)
    entries detected across files.
    """
    tuples = []
    seen: set[tuple[str, str]] = set()
    errors: list[str] = []
    for path in paths:
        data = load_json(path)
        results = data.get("results", [])
        for r in results:
            agent = str(r["agent"]).strip().lower()
            key = (r["case_id"], agent)
            if key in seen:
                errors.append(
                    f"Duplicate result for ({r['case_id']}, {agent}) in {path}"
                )
                continue
            seen.add(key)
            tuples.append({
                "case_id": r["case_id"],
                "agent": agent,
                "status": r["status"],
                "timed_out": r.get("timed_out", False),
            })
    return tuples, errors


def find_results_files(directory: Path) -> list[Path]:
    """Recursively find all results.json files under a directory."""
    return sorted(directory.rglob("results.json"))


def compare(
    result_tuples: list[dict],
    current_baseline: dict | None,
    ref_baseline: dict | None,
) -> dict:
    """Compare results against baselines.

    When current_baseline is None, no static expectation checking is done —
    regressions are detected only via ref-baseline comparison (previous run
    on the base branch passed but this run failed).

    Returns a summary dict with regressions, improvements, new entries,
    and a per-case delta table.
    """
    regressions = []
    improvements = []
    new_entries = []
    missing_baseline = []
    missing_results = []
    rows = {}

    # Check that every provider has at least one result
    seen_providers = {t["agent"] for t in result_tuples}
    for p in PROVIDERS:
        if p not in seen_providers:
            missing_results.append(f"No results for provider '{p}'")

    # Group results by case_id
    by_case: dict[str, dict[str, dict]] = {}
    for t in result_tuples:
        by_case.setdefault(t["case_id"], {})[t["agent"]] = t

    for case_id in sorted(by_case):
        row_delta = "OK"
        provider_statuses = {}

        for provider in PROVIDERS:
            result = by_case[case_id].get(provider)
            if result is None:
                provider_statuses[provider] = "-"
                missing_results.append(
                    f"Missing result for case '{case_id}' provider '{provider}'"
                )
                if row_delta not in ("REGRESSION",):
                    row_delta = "MISSING_RESULT"
                continue

            status = result["status"]
            timed_out = result["timed_out"]
            display = f"{status} (timeout)" if timed_out else status
            provider_statuses[provider] = display

            # Static baseline checking (only when explicit file exists)
            if current_baseline is not None:
                current_entry = current_baseline.get(case_id, {}).get(provider)
                if current_entry is None:
                    missing_baseline.append(f"{case_id}/{provider}")
                    row_delta = "MISSING_BASELINE"
                else:
                    cur_expected = current_entry.get("expected_status", "pass")
                    cur_allow_timeout = current_entry.get("allow_timeout", False)
                    status_rank = {"infra_error": 0, "fail": 1, "pass": 2}

                    actual_rank = status_rank.get(status, -1)
                    expected_rank = status_rank.get(cur_expected, -1)

                    if actual_rank < expected_rank:
                        regressions.append(
                            f"{case_id}/{provider}: expected {cur_expected}, got {status}"
                        )
                        row_delta = "REGRESSION"

                    if timed_out and not cur_allow_timeout:
                        regressions.append(f"{case_id}/{provider}: timed out but allow_timeout=false")
                        row_delta = "REGRESSION"

            # Ref-baseline comparison: detect regressions vs the base branch.
            # When no static baseline file exists, this is the only regression gate.
            if ref_baseline is not None:
                ref_entry = ref_baseline.get(case_id, {}).get(provider)
                if ref_entry is None:
                    if row_delta == "OK":
                        row_delta = "NEW"
                else:
                    ref_expected = ref_entry.get("expected_status", "pass")
                    # Regression: ref expected pass but we got worse
                    if current_baseline is None:
                        status_rank = {"infra_error": 0, "fail": 1, "pass": 2}
                        ref_rank = status_rank.get(ref_expected, -1)
                        actual_rank = status_rank.get(status, -1)
                        if actual_rank < ref_rank:
                            regressions.append(
                                f"{case_id}/{provider}: was {ref_expected} on base, now {status}"
                            )
                            row_delta = "REGRESSION"
                    # Improvement: ref expected fail but now passes
                    if ref_expected in ("fail", "infra_error") and status == "pass":
                        improvements.append(f"{case_id}/{provider}")
                        if row_delta == "OK":
                            row_delta = "IMPROVEMENT"
            else:
                if row_delta == "OK" and current_baseline is None:
                    row_delta = "NEW"

        if row_delta == "NEW":
            new_entries.append(case_id)

        rows[case_id] = {"providers": provider_statuses, "delta": row_delta}

    return {
        "regressions": regressions,
        "improvements": improvements,
        "new_entries": new_entries,
        "missing_baseline": missing_baseline,
        "missing_results": missing_results,
        "rows": rows,
        "has_failures": (
            len(regressions) > 0
            or len(missing_baseline) > 0
            or len(missing_results) > 0
        ),
    }


def format_markdown_report(comparison: dict, baseline_ref: str | None) -> str:
    """Format the comparison as a markdown report."""
    lines = []
    lines.append("## Agent Live Routing Delta Report")
    lines.append("")
    if baseline_ref:
        lines.append(f"**Baseline ref:** `{baseline_ref}`")
    else:
        lines.append("**Baseline ref:** current working tree only (no ref comparison)")
    lines.append("")
    lines.append("| case_id | claude | codex | copilot | delta |")
    lines.append("|---------|--------|-------|---------|-------|")

    for case_id, row in sorted(comparison["rows"].items()):
        p = row["providers"]
        lines.append(
            f"| {case_id} | {p.get('claude', '-')} | {p.get('codex', '-')} | {p.get('copilot', '-')} | {row['delta']} |"
        )

    lines.append("")
    lines.append(
        f"**Regressions:** {len(comparison['regressions'])} | "
        f"**Improvements:** {len(comparison['improvements'])} | "
        f"**New:** {len(comparison['new_entries'])}"
    )

    if comparison["regressions"]:
        lines.append("")
        lines.append("**RESULT: REGRESSION DETECTED**")
        for r in comparison["regressions"]:
            lines.append(f"- {r}")

    if comparison["missing_baseline"]:
        lines.append("")
        lines.append("**MISSING BASELINE ENTRIES:**")
        for m in comparison["missing_baseline"]:
            lines.append(f"- {m}")

    if comparison["missing_results"]:
        lines.append("")
        lines.append("**MISSING RESULTS:**")
        for m in comparison["missing_results"]:
            lines.append(f"- {m}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare agent-routing results against provider-baseline.json"
    )
    parser.add_argument(
        "results",
        nargs="*",
        help="Path(s) to results.json file(s)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=None,
        help="Directory to recursively search for results.json files",
    )
    parser.add_argument(
        "--baseline",
        type=str,
        default=str(DEFAULT_BASELINE_PATH),
        help="Path to baseline file (default: tests/agent-routing/provider-baseline.json; all-pass if missing)",
    )
    parser.add_argument(
        "--baseline-ref",
        type=str,
        default=None,
        help="Git ref (e.g. 'main', 'origin/main') to load baseline from for regression comparison",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write markdown report to file instead of stdout",
    )

    args = parser.parse_args()

    # Collect results files
    results_paths: list[Path] = []
    if args.results_dir:
        results_dir = Path(args.results_dir)
        if not results_dir.is_dir():
            print(f"ERROR: --results-dir not a directory: {results_dir}", file=sys.stderr)
            return 2
        results_paths = find_results_files(results_dir)
    if args.results:
        results_paths.extend(Path(p) for p in args.results)

    if not results_paths:
        print("ERROR: No results files specified. Use positional args or --results-dir.", file=sys.stderr)
        return 2

    for p in results_paths:
        if not p.exists():
            print(f"ERROR: Results file not found: {p}", file=sys.stderr)
            return 2

    # Collect results first (needed for synthetic baseline generation)
    result_tuples, duplicate_errors = collect_results(results_paths)
    if not result_tuples:
        print("ERROR: No result tuples found in provided files.", file=sys.stderr)
        return 1

    if duplicate_errors:
        for err in duplicate_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        print(
            f"ERROR: {len(duplicate_errors)} duplicate result(s) detected. "
            f"Fix artifact merging before comparing.",
            file=sys.stderr,
        )
        return 1

    # Load baselines
    baseline_path = Path(args.baseline)
    current_baseline: dict | None = None
    if baseline_path.exists():
        current_baseline = load_json(baseline_path)
    else:
        print(
            f"INFO: No baseline file at {baseline_path}; regressions detected via ref comparison only.",
            file=sys.stderr,
        )

    ref_baseline = None
    if args.baseline_ref:
        relative_path = "tests/agent-routing/provider-baseline.json"
        ref_baseline = load_baseline_from_ref(args.baseline_ref, relative_path)
        # Missing ref baseline is not fatal — just skip ref comparison

    comparison = compare(result_tuples, current_baseline, ref_baseline)
    report = format_markdown_report(comparison, args.baseline_ref)

    if args.output:
        Path(args.output).write_text(report + "\n")
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)

    if comparison["has_failures"]:
        failure_parts = []
        if comparison["regressions"]:
            failure_parts.append(f"{len(comparison['regressions'])} regression(s)")
        if comparison["missing_baseline"]:
            failure_parts.append(f"{len(comparison['missing_baseline'])} missing baseline entries")
        if comparison["missing_results"]:
            failure_parts.append(f"{len(comparison['missing_results'])} missing results")
        print(f"\nFAILED: {', '.join(failure_parts)}.", file=sys.stderr)
        return 1

    print("\nPASSED: No regressions detected.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
