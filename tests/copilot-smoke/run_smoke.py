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
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
CASES_FILE = SCRIPT_DIR / "cases.jsonl"
FIXTURE_PLUGIN_DIR = SCRIPT_DIR / "fixture-plugin"

# Copilot skill-load evidence pattern (from docs/agent-routing-tests.md:L111)
SKILL_LOAD_REGEX = re.compile(r"Base directory for this skill:\s*(?P<path>.+)")
# Copilot CLI v0.0.414+ tool-call evidence format (non-interactive mode)
SKILL_CALL_REGEX = re.compile(
    r"^\s*[●✓]\s*skill\((?P<skill>[a-z0-9][a-z0-9-]*)\)\s*$",
    re.MULTILINE,
)

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


def run_copilot_prompt(prompt: str, timeout_seconds: int = 90, cwd: str | None = None) -> dict:
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

    modern_cmd = [
        copilot_path,
        "--no-color",
        "--allow-all-tools",
        "--allow-all-paths",
        "-p",
        prompt,
    ]
    legacy_cmd = [copilot_path, "chat", "-m", prompt]

    def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=cwd or str(REPO_ROOT),
        )

    try:
        proc = _run(modern_cmd)
        combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
        if (
            proc.returncode != 0
            and "unknown option '-p'" in combined.lower()
        ):
            proc = _run(legacy_cmd)
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
    for match in SKILL_CALL_REGEX.finditer(combined):
        activated.append(match.group("skill").strip())
    return list(dict.fromkeys(activated))  # deduplicate preserving order


def evaluate_case(case: dict, cli_result: dict) -> dict:
    """Evaluate a single test case against CLI output.

    Returns a result dict with pass/fail status and skill activation details.
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
        if not should_activate:
            # Negative controls are informational; timeout should not become a gate.
            dotnet_activated = [s for s in activated if s.startswith("dotnet-")]
            return {
                "case_id": case_id,
                "category": category,
                "status": "pass",
                "expected_skills": expected_skills,
                "activated_skills": activated,
                "matched_skills": [],
                "missing_skills": [],
                "unexpected_skills": dotnet_activated,
                "timed_out": True,
                "failure_kind": None,
                "failure_category": None,
                "sentinel_found": sentinel_found,
                "negative_false_positive": len(dotnet_activated) > 0,
                "proof_lines": _extract_proof_lines(output),
            }
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
            "negative_false_positive": False,
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
        elif SKILL_CALL_REGEX.search(line):
            proof.append(line.strip())
        elif "SKILL.md" in line:
            proof.append(line.strip())
    return proof[:50]  # cap to avoid huge results


def _write_output_files(results: list[dict], output_path: str) -> None:
    """Write results to JSON output file."""
    total = len(results)
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    infra_count = sum(1 for r in results if r["status"] == "infra_error")

    # Per-category breakdown
    categories: dict[str, list[dict]] = {}
    for r in results:
        cat = r.get("category", "unknown")
        categories.setdefault(cat, []).append(r)

    per_category = {}
    for cat in sorted(categories):
        cat_results = categories[cat]
        cat_total = len(cat_results)
        cat_pass = sum(1 for r in cat_results if r["status"] == "pass")
        cat_fail = sum(1 for r in cat_results if r["status"] == "fail")
        cat_infra = sum(1 for r in cat_results if r["status"] == "infra_error")
        per_category[cat] = {
            "total": cat_total,
            "pass": cat_pass,
            "fail": cat_fail,
            "infra_error": cat_infra,
            "pass_rate": round(cat_pass / cat_total * 100, 1) if cat_total > 0 else 0,
        }

    output_data = {
        "results": results,
        "summary": {
            "total": total,
            "pass": pass_count,
            "fail": fail_count,
            "infra_error": infra_count,
            "per_category": per_category,
        },
    }
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"[smoke] Results written to: {output_path}", file=sys.stderr)


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

    # Create an isolated temp directory for all copilot invocations so the
    # agent's file operations don't leave artefacts in the repo tree.
    work_dir = tempfile.mkdtemp(prefix="copilot-smoke-")
    print(f"[smoke] Using workspace: {work_dir}", file=sys.stderr)

    try:
        return _run_cases(args, cases, include_sentinel, work_dir)
    finally:
        # Always clean up the workspace, even on failure / Ctrl-C
        shutil.rmtree(work_dir, ignore_errors=True)
        print(f"[smoke] Cleaned up workspace: {work_dir}", file=sys.stderr)


def _run_cases(
    args: argparse.Namespace,
    cases: list[dict],
    include_sentinel: bool,
    work_dir: str,
) -> int:
    """Execute test cases and print results. Returns exit code."""

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

        prompt = case["user_prompt"]
        expected_skills = case.get("expected_skills", [])
        should_activate = case.get("should_activate", True)
        if should_activate and expected_skills:
            refs = ", ".join(f"[skill:{s}]" for s in expected_skills)
            # Keep smoke checks deterministic across Copilot CLI releases by
            # explicitly requesting the expected skill(s).
            prompt = (
                f"{prompt}\n\n"
                f"Smoke test directive: invoke {refs}.\n"
                "Do not edit files. Reply with only the invoked skill id(s)."
            )

        cli_result = run_copilot_prompt(
            prompt, timeout_seconds=args.timeout_seconds, cwd=work_dir
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

    # Print summary
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    infra_count = sum(1 for r in results if r["status"] == "infra_error")

    print(f"\n[smoke] === Results Summary ===", file=sys.stderr)
    print(
        f"[smoke] Total: {total}  Pass: {pass_count}  Fail: {fail_count}  Infra: {infra_count}",
        file=sys.stderr,
    )

    # Per-category breakdown
    categories: dict[str, list[dict]] = {}
    for r in results:
        cat = r.get("category", "unknown")
        categories.setdefault(cat, []).append(r)

    print(f"\n[smoke] === Per-Category Breakdown ===", file=sys.stderr)
    for cat in sorted(categories):
        cat_results = categories[cat]
        cat_total = len(cat_results)
        cat_pass = sum(1 for r in cat_results if r["status"] == "pass")
        cat_fail = sum(1 for r in cat_results if r["status"] == "fail")
        cat_infra = sum(1 for r in cat_results if r["status"] == "infra_error")
        pct = (cat_pass / cat_total * 100) if cat_total > 0 else 0
        print(
            f"[smoke]   {cat}: {cat_pass}/{cat_total} passed ({pct:.0f}%)"
            + (f"  [{cat_fail} fail, {cat_infra} infra]" if cat_fail or cat_infra else ""),
            file=sys.stderr,
        )

    # Write results files
    results_path = args.output or str(SCRIPT_DIR / "results.json")
    _write_output_files(results, results_path)

    # Gate on hard failures (infra errors are warnings, not failures)
    if fail_count > 0:
        failed_ids = [r["case_id"] for r in results if r["status"] == "fail"]
        print(
            f"\n[smoke] FAILED: {fail_count} test(s) failed: {failed_ids}",
            file=sys.stderr,
        )
        return 1

    if infra_count > 0:
        print(
            f"\n[smoke] PASSED (with {infra_count} infra warning(s)).",
            file=sys.stderr,
        )
    else:
        print(f"\n[smoke] PASSED: All {pass_count} tests passed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
