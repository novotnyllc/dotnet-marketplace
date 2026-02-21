#!/usr/bin/env python3
"""Copilot activation smoke test runner.

Invokes Copilot CLI with test prompts and verifies skill activation
by parsing output for evidence of skill loading.

Usage:
    python tests/copilot-smoke/run_smoke.py
    python tests/copilot-smoke/run_smoke.py --require-copilot
    python tests/copilot-smoke/run_smoke.py --category direct
    python tests/copilot-smoke/run_smoke.py --case-id smoke-001

Exit codes:
    0 - All tests passed (or Copilot not installed without --require-copilot)
    1 - Test failures or regressions detected
    2 - Infrastructure error (Copilot required but not installed)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CASES_FILE = SCRIPT_DIR / "cases.jsonl"
BASELINE_FILE = SCRIPT_DIR / "baseline.json"
FIXTURE_PLUGIN_DIR = SCRIPT_DIR / "fixture-plugin"

# Copilot skill-load evidence pattern (from docs/agent-routing-tests.md:L111)
SKILL_LOAD_REGEX = re.compile(r"Base directory for this skill:\s*(?P<path>.+)")

# Sentinel string for progressive disclosure verification
SENTINEL_STRING = "SENTINEL-COPILOT-SIBLING-TEST-7f3a"

# Sentinel test case (progressive disclosure via fixture plugin)
SENTINEL_CASE = {
    "id": "smoke-sentinel",
    "user_prompt": "Look up the dotnet-sentinel-test skill and tell me what the verification sentinel value is from its reference.md sibling file.",
    "expected_skills": ["dotnet-sentinel-test"],
    "should_activate": True,
    "category": "progressive-disclosure",
}


def have_copilot() -> bool:
    """Check if the copilot CLI is available."""
    return shutil.which("copilot") is not None


def load_cases(path: Path) -> list[dict]:
    """Load test cases from JSONL file."""
    cases = []
    seen_ids: set[str] = set()
    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError as e:
                print(
                    f"WARNING: Skipping malformed case at line {line_num}: {e}",
                    file=sys.stderr,
                )
                continue
            # Validate required fields
            if "id" not in case or "user_prompt" not in case:
                print(
                    f"WARNING: Skipping case at line {line_num}: missing 'id' or 'user_prompt'",
                    file=sys.stderr,
                )
                continue
            # Detect duplicate IDs
            if case["id"] in seen_ids:
                print(
                    f"WARNING: Skipping duplicate case ID '{case['id']}' at line {line_num}",
                    file=sys.stderr,
                )
                continue
            seen_ids.add(case["id"])
            cases.append(case)
    return cases


def load_baseline(path: Path) -> dict:
    """Load expected outcomes baseline."""
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def install_fixture_plugin() -> bool:
    """Install the sentinel test fixture plugin into Copilot for sibling file testing."""
    if not have_copilot():
        return False
    fixture_dir = str(FIXTURE_PLUGIN_DIR)
    try:
        # Best-effort cleanup before install for idempotency
        uninstall_fixture_plugin()

        # Add fixture as a marketplace source (keyed by path)
        r1 = subprocess.run(
            ["copilot", "plugin", "marketplace", "add", fixture_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r1.returncode != 0:
            print(
                f"WARNING: marketplace add failed (exit {r1.returncode}): {r1.stderr}",
                file=sys.stderr,
            )
            return False

        # Install the fixture plugin
        r2 = subprocess.run(
            [
                "copilot",
                "plugin",
                "install",
                "dotnet-sentinel-fixture@dotnet-sentinel-fixture",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if r2.returncode != 0:
            print(
                f"WARNING: plugin install failed (exit {r2.returncode}): {r2.stderr}",
                file=sys.stderr,
            )
            return False

        return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        print(f"WARNING: Failed to install fixture plugin: {e}", file=sys.stderr)
        return False


def uninstall_fixture_plugin() -> None:
    """Remove the sentinel test fixture plugin from Copilot."""
    if not have_copilot():
        return
    fixture_dir = str(FIXTURE_PLUGIN_DIR)
    try:
        subprocess.run(
            [
                "copilot",
                "plugin",
                "uninstall",
                "dotnet-sentinel-fixture@dotnet-sentinel-fixture",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Remove by path (same identifier used in add) and by name as fallback
        subprocess.run(
            ["copilot", "plugin", "marketplace", "remove", "-f", fixture_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        subprocess.run(
            ["copilot", "plugin", "marketplace", "remove", "-f", "dotnet-sentinel-fixture"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass  # Best-effort cleanup


def run_copilot_prompt(prompt: str, timeout_seconds: int = 90) -> dict:
    """Run a single prompt through the Copilot CLI and capture output.

    Returns a dict with keys: stdout, stderr, exit_code, timed_out, started.
    """
    result = {
        "stdout": "",
        "stderr": "",
        "exit_code": -1,
        "timed_out": False,
        "started": False,
    }

    copilot_path = shutil.which("copilot")
    if copilot_path is None:
        return result

    cmd = [copilot_path, "chat", "-m", prompt]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=str(REPO_ROOT),
        )
        result["stdout"] = proc.stdout or ""
        result["stderr"] = proc.stderr or ""
        result["exit_code"] = proc.returncode
        result["started"] = True
    except subprocess.TimeoutExpired as e:
        def _to_str(x: object) -> str:
            if x is None:
                return ""
            if isinstance(x, bytes):
                return x.decode("utf-8", errors="replace")
            return str(x)

        result["stdout"] = _to_str(e.stdout)
        result["stderr"] = _to_str(e.stderr)
        result["timed_out"] = True
        result["started"] = True
    except FileNotFoundError:
        pass  # started remains False
    except subprocess.SubprocessError:
        result["started"] = True

    return result


def parse_activated_skills(output: str) -> list[str]:
    """Parse Copilot output for skill activation evidence.

    Looks for the 'Base directory for this skill:' pattern and extracts
    skill names from the path.
    """
    activated = []
    combined = output
    for match in SKILL_LOAD_REGEX.finditer(combined):
        path = match.group("path").strip()
        # Normalize path separators
        path = path.replace("\\", "/")
        # Extract skill name from path (last component of skills/<skill-name>/)
        parts = path.rstrip("/").split("/")
        for i, part in enumerate(parts):
            if part == "skills" and i + 1 < len(parts):
                activated.append(parts[i + 1])
                break
        else:
            # Fallback: use the last path component
            if parts:
                activated.append(parts[-1])
    return list(dict.fromkeys(activated))  # deduplicate preserving order


def evaluate_case(case: dict, cli_result: dict) -> dict:
    """Evaluate a single test case against CLI output.

    Returns a result dict compatible with compare-agent-routing-baseline.py format.
    """
    case_id = case["id"]
    expected_skills = case.get("expected_skills", [])
    should_activate = case.get("should_activate", True)
    category = case.get("category", "unknown")

    output = cli_result["stdout"] + "\n" + cli_result["stderr"]

    # Handle infra failures
    if not cli_result["started"]:
        return {
            "case_id": case_id,
            "category": category,
            "status": "infra_error",
            "expected_skills": expected_skills,
            "activated_skills": [],
            "matched_skills": [],
            "missing_skills": expected_skills if should_activate else [],
            "unexpected_skills": [],
            "timed_out": False,
            "failure_kind": None,
            "failure_category": "transport",
            "sentinel_found": False,
            "negative_false_positive": False,
            "proof_lines": [],
        }

    is_sentinel_case = case_id == "smoke-sentinel"

    if cli_result["timed_out"]:
        activated = parse_activated_skills(output)
        sentinel_found = SENTINEL_STRING in output
        # Sentinel case: even on timeout, fail if sentinel not found
        failure_kind = "timeout"
        if is_sentinel_case and not sentinel_found:
            failure_kind = "missing_sentinel"
        return {
            "case_id": case_id,
            "category": category,
            "status": "fail",
            "expected_skills": expected_skills,
            "activated_skills": activated,
            "matched_skills": [s for s in expected_skills if s in activated],
            "missing_skills": [s for s in expected_skills if s not in activated],
            "unexpected_skills": [s for s in activated if s not in expected_skills],
            "timed_out": True,
            "failure_kind": failure_kind,
            "failure_category": "timeout",
            "sentinel_found": sentinel_found,
            "proof_lines": _extract_proof_lines(output),
        }

    # Exit codes 126 (permission denied) and 127 (command not found) are transport errors
    if cli_result["exit_code"] in (126, 127):
        return {
            "case_id": case_id,
            "category": category,
            "status": "infra_error",
            "expected_skills": expected_skills,
            "activated_skills": [],
            "matched_skills": [],
            "missing_skills": expected_skills if should_activate else [],
            "unexpected_skills": [],
            "timed_out": False,
            "failure_kind": None,
            "failure_category": "transport",
            "sentinel_found": False,
            "negative_false_positive": False,
            "proof_lines": [],
        }

    activated = parse_activated_skills(output)
    sentinel_found = SENTINEL_STRING in output

    # Collect proof lines
    proof_lines = _extract_proof_lines(output)

    if should_activate:
        matched = [s for s in expected_skills if s in activated]
        missing = [s for s in expected_skills if s not in activated]
        unexpected = [s for s in activated if s not in expected_skills]

        if not missing:
            status = "pass"
            failure_kind = None
            failure_category = None
        else:
            status = "fail"
            if not activated:
                failure_kind = "skill_not_loaded"
            elif missing and activated:
                failure_kind = "missing_required"
            else:
                failure_kind = "unknown"
            failure_category = "assertion"

        # Sentinel case: skill activation alone is insufficient --
        # the sentinel string from reference.md must also appear in output
        if is_sentinel_case and status == "pass" and not sentinel_found:
            status = "fail"
            failure_kind = "missing_sentinel"
            failure_category = "assertion"
    else:
        # Negative control: no .NET skills should activate.
        # False activations are informational, not a gate -- occasional
        # false positives are expected (per spec). We record them as pass
        # with a negative_false_positive flag for observability.
        dotnet_activated = [s for s in activated if s.startswith("dotnet-")]
        matched = []
        missing = []
        # Always pass for negative controls; false activations are tracked
        # but do not gate the regression comparison.
        status = "pass"
        failure_kind = None
        failure_category = None
        if dotnet_activated:
            unexpected = dotnet_activated
        else:
            unexpected = []

    # Track negative-control false positives for observability
    negative_false_positive = (
        not should_activate and len(unexpected) > 0
    )

    return {
        "case_id": case_id,
        "category": category,
        "status": status,
        "expected_skills": expected_skills,
        "activated_skills": activated,
        "matched_skills": matched,
        "missing_skills": missing,
        "unexpected_skills": unexpected,
        "timed_out": cli_result["timed_out"],
        "failure_kind": failure_kind,
        "failure_category": failure_category,
        "sentinel_found": sentinel_found,
        "negative_false_positive": negative_false_positive,
        "proof_lines": proof_lines,
    }


def _extract_proof_lines(output: str) -> list[str]:
    """Extract lines from output that contain skill activation evidence."""
    proof = []
    for line in output.splitlines():
        if SKILL_LOAD_REGEX.search(line):
            proof.append(line.strip())
        elif "SKILL.md" in line:
            proof.append(line.strip())
    return proof[:50]  # cap to avoid huge results


def compare_baseline(results: list[dict], baseline: dict) -> dict:
    """Compare results against baseline for regression detection.

    Returns a summary dict with regressions, improvements, and per-case deltas.
    """
    regressions = []
    improvements = []
    flaky_failures = []
    deltas = {}

    for r in results:
        case_id = r["case_id"]
        actual_status = r["status"]

        if case_id not in baseline:
            # Missing baseline entry is a hard failure -- every case must
            # have a deterministic expected outcome in baseline.json
            regressions.append(case_id)
            deltas[case_id] = {"status": actual_status, "delta": "MISSING_BASELINE"}
            continue

        entry = baseline[case_id]
        expected_status = entry.get("expected", "pass")
        is_flaky = entry.get("flaky", False)

        # Validate baseline skills match case expected_skills (detect drift)
        baseline_skills = sorted(entry.get("skills", []))
        case_skills = sorted(r.get("expected_skills", []))
        if baseline_skills != case_skills:
            regressions.append(case_id)
            deltas[case_id] = {
                "status": actual_status,
                "delta": "BASELINE_SKILL_DRIFT",
                "baseline_skills": baseline_skills,
                "case_skills": case_skills,
            }
            continue

        if actual_status == expected_status:
            deltas[case_id] = {"status": actual_status, "delta": "OK"}
        elif expected_status == "pass" and actual_status in ("fail", "infra_error"):
            if is_flaky:
                flaky_failures.append(case_id)
                deltas[case_id] = {
                    "status": actual_status,
                    "delta": "FLAKY_FAIL",
                }
            else:
                regressions.append(case_id)
                deltas[case_id] = {
                    "status": actual_status,
                    "delta": "REGRESSION",
                }
        elif expected_status in ("fail", "infra_error") and actual_status == "pass":
            improvements.append(case_id)
            deltas[case_id] = {"status": actual_status, "delta": "IMPROVED"}
        else:
            deltas[case_id] = {"status": actual_status, "delta": "CHANGED"}

    return {
        "regressions": regressions,
        "improvements": improvements,
        "flaky_failures": flaky_failures,
        "deltas": deltas,
        "has_regressions": len(regressions) > 0,
    }


def format_results_for_baseline_compare(results: list[dict]) -> dict:
    """Format results in a structure compatible with compare-agent-routing-baseline.py.

    Produces an envelope matching the agent-routing results format.
    """
    batch_id = str(uuid.uuid4())
    agent_results = []
    for r in results:
        agent_results.append(
            {
                "case_id": r["case_id"],
                "agent": "copilot",
                "status": r["status"],
                "timed_out": r.get("timed_out", False),
                "failure_kind": r.get("failure_kind"),
                "failure_category": r.get("failure_category"),
                "tool_use_proof_lines": r.get("proof_lines", []),
            }
        )
    return {
        "batch_run_id": batch_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": "copilot",
        "source": "copilot-smoke",
        "results": agent_results,
    }


def _write_output_files(results: list[dict], output_path: str) -> None:
    """Write both output_data and agent-routing-compatible results files."""
    total = len(results)
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    infra_count = sum(1 for r in results if r["status"] == "infra_error")

    output_data = {
        "results": results,
        "summary": {
            "total": total,
            "pass": pass_count,
            "fail": fail_count,
            "infra_error": infra_count,
        },
    }
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"[smoke] Results written to: {output_path}", file=sys.stderr)

    # Also write in agent-routing-compatible format
    envelope = format_results_for_baseline_compare(results)
    envelope_path = str(Path(output_path).parent / "results-agent-routing-compat.json")
    with open(envelope_path, "w") as f:
        json.dump(envelope, f, indent=2)
    print(
        f"[smoke] Agent-routing compatible results: {envelope_path}",
        file=sys.stderr,
    )


def _should_include_sentinel(args: argparse.Namespace) -> bool:
    """Check if sentinel case should be included based on filters."""
    if args.case_id:
        case_ids = [c.strip() for c in args.case_id.split(",")]
        if "smoke-sentinel" not in case_ids:
            return False
    if args.category:
        categories = [c.strip() for c in args.category.split(",")]
        if "progressive-disclosure" not in categories:
            return False
    return True


def _build_full_case_list(args: argparse.Namespace) -> list[dict]:
    """Build the complete case list including sentinel, respecting filters."""
    cases = load_cases(CASES_FILE)

    if args.category:
        categories = [c.strip() for c in args.category.split(",")]
        cases = [c for c in cases if c.get("category") in categories]

    if args.case_id:
        case_ids = [c.strip() for c in args.case_id.split(",")]
        cases = [c for c in cases if c["id"] in case_ids]

    if _should_include_sentinel(args):
        cases.append(SENTINEL_CASE)

    return cases


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copilot activation smoke test runner"
    )
    parser.add_argument(
        "--require-copilot",
        action="store_true",
        help="Exit non-zero if Copilot CLI is not installed",
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter cases by category (comma-separated)",
    )
    parser.add_argument(
        "--case-id",
        type=str,
        default=None,
        help="Filter to specific case ID(s) (comma-separated)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=90,
        help="Per-invocation timeout in seconds (default: 90)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write results JSON to this path",
    )

    args = parser.parse_args()

    # Check Copilot availability
    if not have_copilot():
        if args.require_copilot:
            print(
                "ERROR: Copilot CLI not installed (exit 2).",
                file=sys.stderr,
            )
            exit_code = 2
        else:
            print(
                "WARNING: Copilot CLI not installed. Skipping smoke tests (exit 0).",
                file=sys.stderr,
            )
            exit_code = 0

        # Write infra_error results if output requested (consistent format)
        if args.output:
            all_cases = _build_full_case_list(args)
            infra_results = []
            for case in all_cases:
                infra_results.append(
                    {
                        "case_id": case["id"],
                        "category": case.get("category", "unknown"),
                        "status": "infra_error",
                        "expected_skills": case.get("expected_skills", []),
                        "activated_skills": [],
                        "matched_skills": [],
                        "missing_skills": case.get("expected_skills", []) if exit_code != 0 else [],
                        "unexpected_skills": [],
                        "timed_out": False,
                        "failure_kind": None,
                        "failure_category": "transport",
                        "sentinel_found": False,
                        "negative_false_positive": False,
                        "proof_lines": [],
                    }
                )
            _write_output_files(infra_results, args.output)
        return exit_code

    # Load and filter test cases (shared logic with no-Copilot path)
    cases = _build_full_case_list(args)
    if not cases:
        print("WARNING: No cases matched filters.", file=sys.stderr)
        return 0

    include_sentinel = _should_include_sentinel(args)

    # Install fixture plugin for sentinel test
    fixture_installed = False
    if include_sentinel:
        print("[smoke] Installing sentinel fixture plugin...", file=sys.stderr)
        fixture_installed = install_fixture_plugin()
        if not fixture_installed:
            print(
                "WARNING: Could not install fixture plugin; sentinel test may fail.",
                file=sys.stderr,
            )

    baseline = load_baseline(BASELINE_FILE)

    # Run test cases
    total = len(cases)
    results = []
    print(f"[smoke] Running {total} test cases...", file=sys.stderr)

    for i, case in enumerate(cases, 1):
        case_id = case["id"]
        print(
            f"[smoke] [{i}/{total}] Running {case_id} ({case.get('category', 'unknown')})...",
            file=sys.stderr,
        )

        cli_result = run_copilot_prompt(
            case["user_prompt"], timeout_seconds=args.timeout_seconds
        )
        result = evaluate_case(case, cli_result)
        results.append(result)

        status_marker = {
            "pass": "PASS",
            "fail": "FAIL",
            "infra_error": "INFRA",
        }.get(result["status"], "????")

        print(
            f"[smoke] [{i}/{total}] {case_id}: {status_marker}",
            file=sys.stderr,
        )
        if result["status"] == "fail":
            if result.get("missing_skills"):
                print(
                    f"[smoke]   missing: {result['missing_skills']}",
                    file=sys.stderr,
                )
            if result.get("unexpected_skills"):
                print(
                    f"[smoke]   unexpected: {result['unexpected_skills']}",
                    file=sys.stderr,
                )

    # Cleanup fixture plugin
    if fixture_installed:
        print("[smoke] Removing sentinel fixture plugin...", file=sys.stderr)
        uninstall_fixture_plugin()

    # Compare against baseline
    comparison = compare_baseline(results, baseline)

    # Print summary
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    infra_count = sum(1 for r in results if r["status"] == "infra_error")

    print(f"\n[smoke] === Results Summary ===", file=sys.stderr)
    print(
        f"[smoke] Total: {total}  Pass: {pass_count}  Fail: {fail_count}  Infra: {infra_count}",
        file=sys.stderr,
    )

    if comparison["regressions"]:
        print(
            f"[smoke] REGRESSIONS ({len(comparison['regressions'])}): {comparison['regressions']}",
            file=sys.stderr,
        )
    if comparison["improvements"]:
        print(
            f"[smoke] Improvements ({len(comparison['improvements'])}): {comparison['improvements']}",
            file=sys.stderr,
        )
    if comparison["flaky_failures"]:
        print(
            f"[smoke] Flaky failures ({len(comparison['flaky_failures'])}): {comparison['flaky_failures']}",
            file=sys.stderr,
        )

    # Write results files
    results_path = args.output or str(SCRIPT_DIR / "results.json")
    _write_output_files(results, results_path)

    # Gate on regressions (not percentage thresholds)
    if comparison["has_regressions"]:
        print(
            f"\n[smoke] FAILED: {len(comparison['regressions'])} unexpected regression(s) vs baseline.",
            file=sys.stderr,
        )
        return 1

    print(f"\n[smoke] PASSED: No unexpected regressions vs baseline.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
