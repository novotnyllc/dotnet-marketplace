#!/usr/bin/env python3
"""Confusion matrix eval runner (L4) -- disambiguation quality testing.

Tests whether overlapping skills within domain groups cause misrouting,
building NxN confusion matrices per group.

Loads confusion matrix prompts from datasets/confusion/confusion_matrix.jsonl
and expanded negative controls from datasets/confusion/negative_controls_expanded.jsonl.

Each confusion matrix prompt targets a specific skill within a domain group
of overlapping skills. The runner presents the prompt with a group-scoped
routing index and evaluates whether the model selects the correct skill.

Uses CLI-based model invocation via _common.call_model().

Usage:
    python tests/evals/run_confusion_matrix.py --dry-run
    python tests/evals/run_confusion_matrix.py --group testing
    python tests/evals/run_confusion_matrix.py --cli codex

Exit codes:
    0 - Eval completed (informational, always exit 0)
"""

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _common  # noqa: E402

# ---------------------------------------------------------------------------
# Domain group definitions
# ---------------------------------------------------------------------------

# Maps group name -> list of skills in that group.
# The routing index for each group only includes these skills,
# forcing the model to disambiguate within the overlap zone.
DOMAIN_GROUPS: dict[str, list[str]] = {
    "testing": [
        "dotnet-xunit",
        "dotnet-testing-strategy",
        "dotnet-integration-testing",
        "dotnet-snapshot-testing",
        "dotnet-test-quality",
    ],
    "security": [
        "dotnet-security-owasp",
        "dotnet-api-security",
        "dotnet-secrets-management",
        "dotnet-cryptography",
    ],
    "data": [
        "dotnet-efcore-patterns",
        "dotnet-efcore-architecture",
        "dotnet-data-access-strategy",
    ],
    "performance": [
        "dotnet-benchmarkdotnet",
        "dotnet-performance-patterns",
        "dotnet-profiling",
        "dotnet-gc-memory",
    ],
    "api": [
        "dotnet-minimal-apis",
        "dotnet-api-versioning",
        "dotnet-openapi",
        "dotnet-input-validation",
    ],
    "cicd": [
        "dotnet-gha-patterns",
        "dotnet-gha-build-test",
        "dotnet-gha-publish",
        "dotnet-gha-deploy",
    ],
    "blazor": [
        "dotnet-blazor-patterns",
        "dotnet-blazor-components",
        "dotnet-blazor-auth",
        "dotnet-blazor-testing",
    ],
}

# ---------------------------------------------------------------------------
# System prompt for confusion eval
# ---------------------------------------------------------------------------

_CONFUSION_SYSTEM_PROMPT = """\
You are a skill router for a .NET development plugin. Given a skill index and \
a developer prompt, determine which skill should be activated.

Rules:
- Select ONLY the single most relevant skill from the index.
- If no skill is relevant, return an empty skills list.
- Return your answer as JSON only, with no other text.

Required JSON format:
{{"skills": ["skill-id"], "reasoning": "Brief explanation"}}

Skill index:
{index}"""

_MAX_DESCRIPTION_CHARS = 120


# ---------------------------------------------------------------------------
# Group-scoped routing index
# ---------------------------------------------------------------------------


def build_group_index(group_skills: list[str]) -> tuple[str, int]:
    """Build a routing index scoped to a domain group's skills.

    Only includes skills from the specified group, forcing the model
    to disambiguate within the overlap zone.

    Args:
        group_skills: List of skill names in the group.

    Returns:
        Tuple of (index_text, skill_count).
    """
    entries: list[tuple[str, str]] = []
    for skill_name in sorted(group_skills):
        description = _common.load_skill_description(skill_name)
        if description is None:
            continue

        if not isinstance(description, str):
            description = str(description)
        description = " ".join(description.splitlines()).strip()
        if not description:
            continue

        if len(description) > _MAX_DESCRIPTION_CHARS:
            description = description[: _MAX_DESCRIPTION_CHARS - 3] + "..."

        entries.append((skill_name, description))

    lines = [f"- {skill_id}: {desc}" for skill_id, desc in entries]
    return "\n".join(lines), len(entries)


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------


def load_confusion_cases(
    confusion_dir: Path,
    group_filter: Optional[str] = None,
) -> tuple[list[dict], list[dict]]:
    """Load confusion matrix and negative control cases from JSONL files.

    Args:
        confusion_dir: Path to the confusion datasets directory.
        group_filter: If set, only include confusion matrix cases for this group.

    Returns:
        Tuple of (confusion_cases, negative_cases).
    """
    confusion_cases: list[dict] = []
    negative_cases: list[dict] = []

    if not confusion_dir.is_dir():
        return confusion_cases, negative_cases

    for jsonl_path in sorted(confusion_dir.iterdir()):
        if jsonl_path.suffix != ".jsonl":
            continue
        is_negative = "negative" in jsonl_path.stem
        with open(jsonl_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                try:
                    case = json.loads(stripped)
                except json.JSONDecodeError:
                    print(
                        f"[confusion] WARN: Invalid JSON at {jsonl_path.name}:{line_num}",
                        file=sys.stderr,
                    )
                    continue
                if is_negative:
                    negative_cases.append(case)
                else:
                    confusion_cases.append(case)

    if group_filter:
        confusion_cases = [
            c for c in confusion_cases if c.get("group") == group_filter
        ]

    return confusion_cases, negative_cases


# ---------------------------------------------------------------------------
# Activation detection (reuses structured JSON approach from task .5)
# ---------------------------------------------------------------------------


def detect_skills_structured(
    response_text: str,
) -> tuple[Optional[list[str]], str]:
    """Parse structured JSON response to extract activated skill IDs.

    Args:
        response_text: Raw model response text.

    Returns:
        Tuple of (skill_list_or_none, detection_method).
    """
    parsed = _common.extract_json(response_text)
    if parsed is not None and "skills" in parsed:
        skills = parsed["skills"]
        if isinstance(skills, list) and all(isinstance(s, str) for s in skills):
            return skills, "structured"
    return None, "parse_failure"


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def _compute_stats(values: list[float]) -> dict:
    """Compute mean, stddev, and n for a list of numeric values."""
    n = len(values)
    if n == 0:
        return {"mean": 0.0, "stddev": 0.0, "n": 0}
    mean = sum(values) / n
    if n < 2:
        return {"mean": mean, "stddev": 0.0, "n": n}
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return {"mean": mean, "stddev": math.sqrt(variance), "n": n}


# ---------------------------------------------------------------------------
# Confusion matrix computation
# ---------------------------------------------------------------------------


def build_confusion_matrices(
    case_results: list[dict],
) -> dict[str, dict]:
    """Build per-group NxN confusion matrices from case results.

    For each group, builds a matrix where rows are expected skills and
    columns are predicted skills. Axes are locked to the declared
    DOMAIN_GROUPS skills to ensure stable NxN dimensions across runs.
    Out-of-group predictions are tracked separately.

    Args:
        case_results: List of evaluated confusion case result dicts.

    Returns:
        Dict mapping group_name -> {
            "matrix": {expected: {predicted: count}},
            "multi_activation_count": int,
            "no_activation_count": int,
            "out_of_group_count": int,
            "total_cases": int,
            "skills": [sorted skill list from DOMAIN_GROUPS],
        }
    """
    # Group cases by their domain group
    grouped: dict[str, list[dict]] = defaultdict(list)
    for result in case_results:
        group = result.get("group")
        if group:
            grouped[group].append(result)

    matrices: dict[str, dict] = {}
    for group_name, results in sorted(grouped.items()):
        # Lock axes to declared group skills (stable across runs)
        group_skills = DOMAIN_GROUPS.get(group_name, [])
        sorted_skills = sorted(group_skills)

        # Build NxN matrix with fixed axes
        matrix: dict[str, dict[str, int]] = {}
        for skill in sorted_skills:
            matrix[skill] = {s: 0 for s in sorted_skills}

        multi_activation_count = 0
        no_activation_count = 0
        out_of_group_count = 0

        for r in results:
            expected = r.get("expected_skill", "")
            activated = r.get("activated_skills", [])
            classification = r.get("classification", "")

            if classification == "no_activation":
                no_activation_count += 1
                continue

            if classification == "multi_activation":
                multi_activation_count += 1
                # Don't enter multi-activations into NxN matrix; only count them separately
                continue

            # Enter single-activation cases into the confusion matrix
            if classification == "single_activation" and activated and expected in matrix:
                primary = activated[0]
                if primary in matrix[expected]:
                    matrix[expected][primary] += 1
                else:
                    # Prediction outside the group (hallucination)
                    out_of_group_count += 1

        matrices[group_name] = {
            "matrix": matrix,
            "multi_activation_count": multi_activation_count,
            "no_activation_count": no_activation_count,
            "out_of_group_count": out_of_group_count,
            "total_cases": len(results),
            "skills": sorted_skills,
        }

    return matrices


def compute_cross_activation_rates(
    matrices: dict[str, dict],
) -> dict[str, dict]:
    """Compute cross-activation rates and flags from confusion matrices.

    For each group, computes the percentage of predictions that went
    to the wrong skill (cross-activation rate).

    Args:
        matrices: Per-group confusion matrix data.

    Returns:
        Dict mapping group_name -> {
            "cross_activation_rate": float,
            "per_skill_cross_activation": {skill: float},
            "flagged_cross_activations": [{expected, predicted, rate}],
            "low_discrimination_skills": [skill_names],
        }
    """
    rates: dict[str, dict] = {}

    for group_name, data in sorted(matrices.items()):
        matrix = data["matrix"]
        skills = data["skills"]

        # Per-skill cross-activation
        per_skill_cross: dict[str, float] = {}
        flagged: list[dict] = []
        total_correct = 0
        total_incorrect = 0

        for expected_skill in skills:
            if expected_skill not in matrix:
                continue
            row = matrix[expected_skill]
            row_total = sum(row.values())
            if row_total == 0:
                per_skill_cross[expected_skill] = 0.0
                continue

            correct = row.get(expected_skill, 0)
            incorrect = row_total - correct
            total_correct += correct
            total_incorrect += incorrect

            cross_rate = incorrect / row_total
            per_skill_cross[expected_skill] = round(cross_rate, 4)

            # Flag specific cross-activations > 20% (absolute finding flag)
            for predicted_skill, count in row.items():
                if predicted_skill == expected_skill:
                    continue
                if count > 0:
                    pair_rate = count / row_total
                    if pair_rate > 0.20:
                        flagged.append({
                            "expected": expected_skill,
                            "predicted": predicted_skill,
                            "rate": round(pair_rate, 4),
                            "count": count,
                            "total": row_total,
                        })

        # Overall cross-activation rate for group
        all_predictions = total_correct + total_incorrect
        overall_cross_rate = (
            total_incorrect / all_predictions if all_predictions > 0 else 0.0
        )

        # Low discrimination: skills where 2+ other skills got equal or higher
        # predictions than the correct skill
        low_disc: list[str] = []
        for expected_skill in skills:
            if expected_skill not in matrix:
                continue
            row = matrix[expected_skill]
            correct_count = row.get(expected_skill, 0)
            competitors = [
                s for s, c in row.items()
                if s != expected_skill and c >= correct_count and c > 0
            ]
            if len(competitors) >= 2:
                low_disc.append(expected_skill)

        # Index violation rate: predictions outside the group
        out_of_group = data.get("out_of_group_count", 0)
        total_predictions = all_predictions + out_of_group
        index_violation_rate = (
            out_of_group / total_predictions if total_predictions > 0 else 0.0
        )

        rates[group_name] = {
            "cross_activation_rate": round(overall_cross_rate, 4),
            "index_violation_rate": round(index_violation_rate, 4),
            "out_of_group_count": out_of_group,
            "per_skill_cross_activation": per_skill_cross,
            "flagged_cross_activations": sorted(
                flagged, key=lambda x: x["rate"], reverse=True
            ),
            "low_discrimination_skills": sorted(low_disc),
        }

    return rates


# ---------------------------------------------------------------------------
# Findings report
# ---------------------------------------------------------------------------


def generate_findings(
    matrices: dict[str, dict],
    cross_rates: dict[str, dict],
    negative_results: list[dict],
    confusion_results: Optional[list[dict]] = None,
) -> list[dict]:
    """Generate findings section for the report.

    Lists top cross-activations and low-discrimination prompts,
    even if empty (required by acceptance criteria).

    Args:
        matrices: Per-group confusion matrix data.
        cross_rates: Per-group cross-activation rate data.
        negative_results: Results from negative control cases.
        confusion_results: Individual case results for prompt-level findings.

    Returns:
        List of finding dicts with severity, group, description.
    """
    findings: list[dict] = []
    case_results = confusion_results or []

    # Cross-activation findings (absolute > 20%)
    for group_name, rates in sorted(cross_rates.items()):
        for flagged in rates["flagged_cross_activations"]:
            example_ids = [
                r.get("id", "")
                for r in case_results
                if r.get("group") == group_name
                and r.get("expected_skill") == flagged["expected"]
                and r.get("classification") == "single_activation"
                and r.get("activated_skills", [None])[0:1] == [flagged["predicted"]]
            ][:3]

            findings.append({
                "severity": "warning",
                "group": group_name,
                "type": "cross_activation",
                "description": (
                    f"High cross-activation in group '{group_name}': "
                    f"expected '{flagged['expected']}' but predicted "
                    f"'{flagged['predicted']}' at {flagged['rate']:.0%} rate "
                    f"({flagged['count']}/{flagged['total']} cases)"
                ),
                "expected": flagged["expected"],
                "predicted": flagged["predicted"],
                "rate": flagged["rate"],
                "example_case_ids": example_ids,
            })

    # Low discrimination: skill-level aggregate
    for group_name, rates in sorted(cross_rates.items()):
        for skill in rates["low_discrimination_skills"]:
            findings.append({
                "severity": "warning",
                "group": group_name,
                "type": "low_discrimination_skill",
                "description": (
                    f"Low discrimination for '{skill}' in group '{group_name}': "
                    f"2+ other skills received equal or more activations"
                ),
                "skill": skill,
            })

    # Low discrimination: prompt-level (multi_activation cases)
    for r in case_results:
        if r.get("classification") == "multi_activation":
            findings.append({
                "severity": "info",
                "group": r.get("group", "unknown"),
                "type": "low_discrimination_prompt",
                "description": (
                    f"Low discrimination prompt '{r.get('id', 'unknown')}' "
                    f"in group '{r.get('group', 'unknown')}': "
                    f"expected '{r.get('expected_skill', '')}', "
                    f"got multiple activations: {r.get('activated_skills', [])}"
                ),
                "case_id": r.get("id", ""),
                "expected_skill": r.get("expected_skill", ""),
                "activated_skills": r.get("activated_skills", []),
                "user_prompt": r.get("user_prompt", ""),
            })

    # Never-activated skills: skills that were never predicted in any case
    for group_name, data in sorted(matrices.items()):
        matrix = data["matrix"]
        group_skills = data["skills"]
        for skill in group_skills:
            col_sum = sum(
                matrix[row_skill].get(skill, 0) for row_skill in group_skills
                if row_skill in matrix
            )
            if col_sum == 0 and data["total_cases"] > 0:
                findings.append({
                    "severity": "info",
                    "group": group_name,
                    "type": "never_activated",
                    "description": (
                        f"Skill '{skill}' was never predicted in group "
                        f"'{group_name}' ({data['total_cases']} cases)"
                    ),
                    "skill": skill,
                })

    # High multi_activation rate per group
    for group_name, data in sorted(matrices.items()):
        total = data["total_cases"]
        multi = data["multi_activation_count"]
        if total > 0 and multi / total > 0.20:
            findings.append({
                "severity": "info",
                "group": group_name,
                "type": "high_multi_activation",
                "description": (
                    f"High multi-activation rate in group '{group_name}': "
                    f"{multi}/{total} cases ({multi / total:.0%})"
                ),
                "rate": round(multi / total, 4),
            })

    # High no_activation rate per group
    for group_name, data in sorted(matrices.items()):
        total = data["total_cases"]
        no_act = data["no_activation_count"]
        if total > 0 and no_act / total > 0.20:
            findings.append({
                "severity": "info",
                "group": group_name,
                "type": "high_no_activation",
                "description": (
                    f"High no-activation rate in group '{group_name}': "
                    f"{no_act}/{total} cases ({no_act / total:.0%})"
                ),
                "rate": round(no_act / total, 4),
            })

    # Index violations: model predicted skills outside the group
    for group_name, rates_data in sorted(cross_rates.items()):
        oog = rates_data.get("out_of_group_count", 0)
        viol_rate = rates_data.get("index_violation_rate", 0.0)
        if oog > 0:
            findings.append({
                "severity": "info" if viol_rate <= 0.10 else "warning",
                "group": group_name,
                "type": "index_violation",
                "description": (
                    f"Index violations in group '{group_name}': "
                    f"{oog} prediction(s) outside group index "
                    f"({viol_rate:.0%} violation rate)"
                ),
                "out_of_group_count": oog,
                "index_violation_rate": viol_rate,
            })

    # Negative control failures
    neg_failures = [r for r in negative_results if not r.get("passed", True)]
    if neg_failures:
        findings.append({
            "severity": "warning",
            "group": "_negative_controls",
            "type": "negative_control_failure",
            "description": (
                f"{len(neg_failures)} of {len(negative_results)} expanded "
                f"negative controls incorrectly activated skills"
            ),
            "failure_count": len(neg_failures),
            "total_count": len(negative_results),
        })

    return findings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Confusion matrix eval runner (L4) -- disambiguation quality"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show dataset groups and exit without CLI calls",
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
    parser.add_argument(
        "--cli",
        type=str,
        choices=["claude", "codex", "copilot"],
        default=None,
        help="Override CLI backend (default: from config.yaml)",
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
    )
    confusion_dir = datasets_dir / "confusion"

    # Validate --group if provided
    if args.group and args.group not in DOMAIN_GROUPS:
        print(
            f"[confusion] ERROR: Unknown group '{args.group}'. "
            f"Valid groups: {', '.join(sorted(DOMAIN_GROUPS.keys()))}",
            file=sys.stderr,
        )
        return 0

    # Load datasets
    confusion_cases, negative_cases = load_confusion_cases(
        confusion_dir, group_filter=args.group
    )

    if args.dry_run:
        # Summarize dataset contents
        groups: dict[str, int] = defaultdict(int)
        for c in confusion_cases:
            groups[c.get("group", "unknown")] += 1

        total_confusion = len(confusion_cases)
        total_negative = len(negative_cases)

        print(
            f"[confusion] Dry run -- {len(groups)} group(s), "
            f"{total_confusion} confusion case(s), "
            f"{total_negative} negative control(s)",
            file=sys.stderr,
        )
        for g, count in sorted(groups.items()):
            group_skills = DOMAIN_GROUPS.get(g, [])
            index_text, skill_count = build_group_index(group_skills)
            print(
                f"  group: {g} -- {count} cases, {skill_count} skills in index",
                file=sys.stderr,
            )
        if args.group:
            print(
                f"[confusion] Filter: --group {args.group}", file=sys.stderr
            )
        print(
            "[confusion] Dry run complete. No CLI calls made.",
            file=sys.stderr,
        )
        # Emit runner output contract
        print(f"TOTAL_CALLS=0")
        print(f"COST_USD=0.0")
        print(f"ABORTED=0")
        print(f"N_CASES={total_confusion + total_negative}")
        return 0

    # --- Full eval execution ---
    meta = _common.build_run_metadata(
        eval_type="confusion",
        model=args.model,
        judge_model=args.judge_model,
        seed=args.seed,
        cli=args.cli,
    )
    temperature = cfg.get("temperature", 0.0)
    max_cost = cfg.get("cost", {}).get("max_cost_per_run", 5.0)
    max_calls = cfg.get("cost", {}).get("max_calls_per_run", 500)

    # Pre-build group indices and validate skills exist
    group_indices: dict[str, tuple[str, int]] = {}
    active_groups = (
        [args.group] if args.group else sorted(DOMAIN_GROUPS.keys())
    )

    # Validate that all declared skills actually exist in the repo
    missing_skills: dict[str, list[str]] = {}
    for g in active_groups:
        skills = DOMAIN_GROUPS.get(g, [])
        missing = [
            s for s in skills
            if _common.load_skill_description(s) is None
        ]
        if missing:
            missing_skills[g] = missing
        if skills:
            group_indices[g] = build_group_index(skills)

    if missing_skills:
        print(
            "[confusion] ERROR: Missing skills in DOMAIN_GROUPS "
            "(no description in skills/ directory):",
            file=sys.stderr,
        )
        for g, skills_list in sorted(missing_skills.items()):
            print(f"  {g}: {skills_list}", file=sys.stderr)
        print(
            "[confusion] Aborting: cannot build valid routing indices with "
            "missing skills. Add the skills or update DOMAIN_GROUPS.",
            file=sys.stderr,
        )
        _common.write_results(
            meta=meta,
            summary={"_run_status": {
                "ok": False,
                "reason": "missing_skills",
                "missing_skills": missing_skills,
                "n": 0,
            }},
            cases=[],
            output_dir=args.output_dir,
            artifacts={"missing_skills": missing_skills},
        )
        print(f"TOTAL_CALLS=0")
        print(f"COST_USD=0.0")
        print(f"ABORTED=1")
        print(f"N_CASES=0")
        return 0

    print(
        f"[confusion] Starting eval run {meta['run_id']}", file=sys.stderr
    )
    print(
        f"[confusion] Backend: {meta['backend']}, Model: {meta['model']}, "
        f"Confusion cases: {len(confusion_cases)}, "
        f"Negative controls: {len(negative_cases)}, "
        f"Runs: {args.runs}",
        file=sys.stderr,
    )

    total_cost = 0.0
    total_calls = 0
    aborted = False
    all_confusion_results: list[dict] = []
    all_negative_results: list[dict] = []

    # Budget check closure (captures mutable locals)
    def _budget_exceeded(pending_calls: int = 0) -> bool:
        return total_cost >= max_cost or (total_calls + pending_calls) >= max_calls

    for run_idx in range(args.runs):
        if args.runs > 1:
            print(
                f"\n[confusion] === Run {run_idx + 1}/{args.runs} ===",
                file=sys.stderr,
            )

        # --- Evaluate confusion matrix cases ---
        for case in confusion_cases:
            # Dual abort check
            if _budget_exceeded():
                print(
                    f"[confusion] ABORT: Limit exceeded "
                    f"(cost=${total_cost:.4f}/{max_cost}, "
                    f"calls={total_calls}/{max_calls})",
                    file=sys.stderr,
                )
                aborted = True
                break

            case_id = case.get("id", "unknown")
            group = case.get("group", "unknown")
            user_prompt = case.get("user_prompt", "")
            expected_skill = case.get("expected_skill", "")
            acceptable_skills = case.get("acceptable_skills", [])

            run_case_id = (
                f"{case_id}/run-{run_idx}" if args.runs > 1 else case_id
            )

            # Get group-scoped index
            index_text, skill_count = group_indices.get(group, ("", 0))
            if skill_count == 0:
                print(
                    f"[confusion]   SKIP {run_case_id} -- no index for "
                    f"group '{group}'",
                    file=sys.stderr,
                )
                all_confusion_results.append({
                    "id": run_case_id,
                    "entity_id": group,
                    "group": group,
                    "user_prompt": user_prompt,
                    "expected_skill": expected_skill,
                    "acceptable_skills": acceptable_skills,
                    "activated_skills": [],
                    "classification": "skipped_no_index",
                    "detection_method": "skipped",
                    "passed": False,
                    "run_index": run_idx,
                    "cost": 0.0,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                continue

            system_prompt = _CONFUSION_SYSTEM_PROMPT.format(index=index_text)

            print(
                f"[confusion]   Evaluating {run_case_id} ({group}) ...",
                file=sys.stderr,
            )

            # Call model
            response_text = ""
            call_cost = 0.0
            api_error: Optional[str] = None

            try:
                def _call(
                    _sys=system_prompt,
                    _prompt=user_prompt,
                    _model=meta["model"],
                ):
                    return _common.call_model(
                        system_prompt=_sys,
                        user_prompt=_prompt,
                        model=_model,
                        max_tokens=512,
                        temperature=temperature,
                        cli=args.cli,
                    )

                result = _common.retry_with_backoff(
                    _call, budget_check=_budget_exceeded
                )
                response_text = result["text"]
                call_cost = result["cost"]
                total_cost += call_cost
                total_calls += result["calls"]
            except Exception as exc:
                api_error = str(exc)
                call_cost = 0.0
                # Account for CLI calls consumed by failed retries
                total_calls += int(getattr(exc, "calls_consumed", 0))

            # Detect activated skills
            activated_skills: list[str] = []
            detection_method = "error"
            classification = "error"

            if api_error is None:
                skills_opt, detection_method = detect_skills_structured(
                    response_text
                )
                if skills_opt is not None:
                    activated_skills = skills_opt
                    if len(activated_skills) == 0:
                        classification = "no_activation"
                    elif len(activated_skills) == 1:
                        classification = "single_activation"
                    else:
                        classification = "multi_activation"
                else:
                    classification = "parse_failure"

            # Determine pass/fail
            # Multi-activation should fail for confusion eval (select ONLY the single most relevant skill)
            all_valid = {expected_skill} | set(acceptable_skills)
            all_valid.discard("")
            if classification == "single_activation":
                passed = activated_skills[0] in all_valid
            else:
                passed = False

            case_result = {
                "id": run_case_id,
                "entity_id": group,
                "group": group,
                "user_prompt": user_prompt,
                "expected_skill": expected_skill,
                "acceptable_skills": acceptable_skills,
                "activated_skills": activated_skills,
                "classification": classification,
                "detection_method": detection_method,
                "passed": passed,
                "run_index": run_idx,
                "cost": round(call_cost, 6),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            if api_error:
                case_result["api_error"] = api_error
                case_result["passed"] = False

            all_confusion_results.append(case_result)

        if aborted:
            break

        # --- Evaluate expanded negative controls ---
        all_group_skills: list[str] = []
        for g in active_groups:
            all_group_skills.extend(DOMAIN_GROUPS.get(g, []))
        full_index_text, _ = build_group_index(
            sorted(set(all_group_skills))
        )
        neg_system_prompt = _CONFUSION_SYSTEM_PROMPT.format(
            index=full_index_text
        )

        for case in negative_cases:
            # Dual abort check
            if _budget_exceeded():
                print(
                    f"[confusion] ABORT: Limit exceeded "
                    f"(cost=${total_cost:.4f}/{max_cost}, "
                    f"calls={total_calls}/{max_calls})",
                    file=sys.stderr,
                )
                aborted = True
                break

            case_id = case.get("id", "unknown")
            user_prompt = case.get("user_prompt", "")
            category = case.get("category", "unknown")

            run_case_id = (
                f"{case_id}/run-{run_idx}" if args.runs > 1 else case_id
            )

            print(
                f"[confusion]   Evaluating neg {run_case_id} ({category}) ...",
                file=sys.stderr,
            )

            response_text = ""
            api_error = None
            call_cost = 0.0

            try:
                def _neg_call(
                    _sys=neg_system_prompt,
                    _prompt=user_prompt,
                    _model=meta["model"],
                ):
                    return _common.call_model(
                        system_prompt=_sys,
                        user_prompt=_prompt,
                        model=_model,
                        max_tokens=512,
                        temperature=temperature,
                        cli=args.cli,
                    )

                result = _common.retry_with_backoff(
                    _neg_call, budget_check=_budget_exceeded
                )
                response_text = result["text"]
                call_cost = result["cost"]
                total_cost += call_cost
                total_calls += result["calls"]
            except Exception as exc:
                api_error = str(exc)
                call_cost = 0.0
                # Account for CLI calls consumed by failed retries
                total_calls += int(getattr(exc, "calls_consumed", 0))

            activated_skills = []
            detection_method = "error"

            if api_error is None:
                skills_opt, detection_method = detect_skills_structured(
                    response_text
                )
                if skills_opt is not None:
                    activated_skills = skills_opt
                else:
                    detection_method = "parse_failure"

            if detection_method == "parse_failure":
                passed = False
            else:
                passed = len(activated_skills) == 0

            neg_result = {
                "id": run_case_id,
                "entity_id": "_negative_controls",
                "user_prompt": user_prompt,
                "expected_skills": [],
                "activated_skills": activated_skills,
                "should_activate": False,
                "category": category,
                "detection_method": detection_method,
                "passed": passed,
                "run_index": run_idx,
                "cost": round(call_cost, 6),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

            if api_error:
                neg_result["api_error"] = api_error
                neg_result["passed"] = False

            all_negative_results.append(neg_result)

        if aborted:
            break

    # --- Build confusion matrices ---
    matrices = build_confusion_matrices(all_confusion_results)
    cross_rates = compute_cross_activation_rates(matrices)
    findings = generate_findings(
        matrices, cross_rates, all_negative_results, all_confusion_results
    )

    # --- Compute per-group summary with mean/stddev/n ---
    summary: dict[str, dict] = {}

    for group_name in sorted(set(r.get("group", "") for r in all_confusion_results)):
        if not group_name:
            continue

        group_results = [
            r for r in all_confusion_results if r.get("group") == group_name
        ]

        if args.runs > 1:
            run_accuracies: list[float] = []
            run_cross_rates_list: list[float] = []

            for run_idx in range(args.runs):
                run_cases = [
                    r for r in group_results if r.get("run_index") == run_idx
                ]
                if run_cases:
                    passed_count = sum(
                        1 for r in run_cases if r.get("passed", False)
                    )
                    run_acc = passed_count / len(run_cases)
                    run_accuracies.append(run_acc)

                    run_matrices = build_confusion_matrices(run_cases)
                    run_cross = compute_cross_activation_rates(run_matrices)
                    if group_name in run_cross:
                        run_cross_rates_list.append(
                            run_cross[group_name]["cross_activation_rate"]
                        )

            accuracy_stats = _compute_stats(run_accuracies)
            cross_stats = _compute_stats(run_cross_rates_list)
        else:
            passed_count = sum(
                1 for r in group_results if r.get("passed", False)
            )
            group_acc = (
                passed_count / len(group_results) if group_results else 0.0
            )
            accuracy_stats = {"mean": group_acc, "stddev": 0.0, "n": 1}

            group_cross = cross_rates.get(group_name, {}).get(
                "cross_activation_rate", 0.0
            )
            cross_stats = {"mean": group_cross, "stddev": 0.0, "n": 1}

        group_matrix_data = matrices.get(group_name, {})

        summary[group_name] = {
            "accuracy": accuracy_stats["mean"],
            "cross_activation_rate": cross_stats["mean"],
            "n": len(group_results),
            "accuracy_stats": accuracy_stats,
            "cross_activation_stats": cross_stats,
            "multi_activation_count": group_matrix_data.get(
                "multi_activation_count", 0
            ),
            "no_activation_count": group_matrix_data.get(
                "no_activation_count", 0
            ),
            "total_cases": group_matrix_data.get("total_cases", 0),
        }

    # Add negative control summary
    if all_negative_results:
        neg_passed = sum(
            1 for r in all_negative_results if r.get("passed", False)
        )
        neg_total = len(all_negative_results)
        neg_pass_rate = neg_passed / neg_total if neg_total > 0 else 0.0
        summary["_negative_controls"] = {
            "pass_rate": round(neg_pass_rate, 4),
            "passed": neg_passed,
            "failed": neg_total - neg_passed,
            "n": neg_total,
        }

    # Combine all case results
    all_cases = all_confusion_results + all_negative_results

    # Serialize matrices for JSON output
    serializable_matrices: dict[str, dict] = {}
    for group_name, data in matrices.items():
        serializable_matrices[group_name] = {
            "matrix": {
                expected: dict(predicted_counts)
                for expected, predicted_counts in data["matrix"].items()
            },
            "multi_activation_count": data["multi_activation_count"],
            "no_activation_count": data["no_activation_count"],
            "out_of_group_count": data["out_of_group_count"],
            "total_cases": data["total_cases"],
            "skills": data["skills"],
        }

    meta["total_cost"] = round(total_cost, 6)

    output_path = _common.write_results(
        meta=meta,
        summary=summary,
        cases=all_cases,
        output_dir=args.output_dir,
        artifacts={
            "confusion_matrices": serializable_matrices,
            "cross_activation_rates": cross_rates,
            "findings": findings,
            "domain_groups": {
                g: DOMAIN_GROUPS[g]
                for g in active_groups
                if g in DOMAIN_GROUPS
            },
        },
    )

    # --- Print summary to stderr ---
    print(f"\n[confusion] === Summary ===", file=sys.stderr)

    for group_name, group_summary in sorted(summary.items()):
        if group_name == "_negative_controls":
            continue
        acc = group_summary.get("accuracy", 0.0)
        cross = group_summary.get("cross_activation_rate", 0.0)
        n = group_summary.get("n", 0)
        multi = group_summary.get("multi_activation_count", 0)
        no_act = group_summary.get("no_activation_count", 0)
        print(
            f"  {group_name}: accuracy={acc:.2%}, "
            f"cross_activation={cross:.2%}, "
            f"multi={multi}, no_activation={no_act}, n={n}",
            file=sys.stderr,
        )

    if "_negative_controls" in summary:
        neg = summary["_negative_controls"]
        print(
            f"  negative_controls: pass_rate={neg['pass_rate']:.2%}, "
            f"passed={neg['passed']}/{neg['n']}",
            file=sys.stderr,
        )

    print(f"\n[confusion] === Findings ===", file=sys.stderr)
    if findings:
        for f in findings:
            print(
                f"  [{f['severity']}] {f['description']}",
                file=sys.stderr,
            )
    else:
        print("  No findings (all metrics within thresholds).", file=sys.stderr)

    print(f"\n[confusion] Total cost: ${total_cost:.4f}", file=sys.stderr)
    print(f"  Total calls: {total_calls}", file=sys.stderr)
    print(
        f"[confusion] Results written to: {output_path}", file=sys.stderr
    )

    # Emit runner output contract on stdout
    print(f"TOTAL_CALLS={total_calls}")
    print(f"COST_USD={total_cost:.4f}")
    print(f"ABORTED={'1' if aborted else '0'}")
    print(f"N_CASES={len(all_cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
