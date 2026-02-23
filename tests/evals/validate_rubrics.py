#!/usr/bin/env python3
"""Validate rubric YAML files against the rubric contract.

Uses custom Python checks (no jsonschema dependency). Exits non-zero
on any validation failure.

Usage:
    python tests/evals/validate_rubrics.py
    python tests/evals/validate_rubrics.py --rubrics-dir tests/evals/rubrics
"""

import argparse
import sys
from pathlib import Path

import yaml

EVALS_DIR = Path(__file__).resolve().parent
REPO_ROOT = EVALS_DIR.parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DEFAULT_RUBRICS_DIR = EVALS_DIR / "rubrics"

WEIGHT_TOLERANCE = 0.01


def validate_rubric(rubric_path: Path, errors: list[str]) -> None:
    """Validate a single rubric file and append errors to the list."""
    filename = rubric_path.stem
    prefix = f"{rubric_path.name}"

    try:
        with open(rubric_path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"{prefix}: invalid YAML: {e}")
        return
    except OSError as e:
        errors.append(f"{prefix}: cannot read file: {e}")
        return

    if not isinstance(data, dict):
        errors.append(f"{prefix}: rubric must be a YAML mapping, got {type(data).__name__}")
        return

    # --- skill_name ---
    skill_name = data.get("skill_name")
    if not isinstance(skill_name, str) or not skill_name.strip():
        errors.append(f"{prefix}: missing or empty 'skill_name' field")
    elif skill_name != filename:
        errors.append(
            f"{prefix}: skill_name '{skill_name}' does not match filename '{filename}'"
        )
    else:
        # Verify the skill directory and SKILL.md actually exist
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_md.is_file():
            errors.append(
                f"{prefix}: skill '{skill_name}' not found at {skill_md}"
            )

    # --- test_prompts ---
    test_prompts = data.get("test_prompts")
    if not isinstance(test_prompts, list):
        errors.append(f"{prefix}: 'test_prompts' must be an array")
    elif len(test_prompts) == 0:
        errors.append(f"{prefix}: 'test_prompts' must have at least 1 entry")
    else:
        for i, prompt in enumerate(test_prompts):
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{prefix}: test_prompts[{i}] must be a non-empty string")

    # --- criteria ---
    criteria = data.get("criteria")
    if not isinstance(criteria, list):
        errors.append(f"{prefix}: 'criteria' must be an array")
    elif len(criteria) == 0:
        errors.append(f"{prefix}: 'criteria' must have at least 1 entry")
    else:
        total_weight = 0.0
        seen_names: set[str] = set()
        for i, criterion in enumerate(criteria):
            c_prefix = f"{prefix}: criteria[{i}]"
            if not isinstance(criterion, dict):
                errors.append(f"{c_prefix}: must be a mapping")
                continue

            # name
            name = criterion.get("name")
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{c_prefix}: 'name' must be a non-empty string")
            elif name in seen_names:
                errors.append(f"{c_prefix}: duplicate criterion name '{name}'")
            else:
                seen_names.add(name)

            # weight
            weight = criterion.get("weight")
            if not isinstance(weight, (int, float)):
                errors.append(f"{c_prefix}: 'weight' must be a number")
            elif weight <= 0.0 or weight > 1.0:
                errors.append(f"{c_prefix}: 'weight' must be in (0.0, 1.0], got {weight}")
            else:
                total_weight += float(weight)

            # description
            description = criterion.get("description")
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{c_prefix}: 'description' must be a non-empty string")

        # Weight sum check
        if abs(total_weight - 1.0) > WEIGHT_TOLERANCE:
            errors.append(
                f"{prefix}: criteria weights sum to {total_weight:.4f}, "
                f"must be 1.0 (+/- {WEIGHT_TOLERANCE})"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rubric YAML files")
    parser.add_argument(
        "--rubrics-dir",
        type=Path,
        default=DEFAULT_RUBRICS_DIR,
        help="Path to rubrics directory",
    )
    args = parser.parse_args()

    rubrics_dir = args.rubrics_dir
    if not rubrics_dir.is_dir():
        print(f"Rubrics directory not found: {rubrics_dir}", file=sys.stderr)
        return 1

    rubric_files = sorted(
        p for p in rubrics_dir.iterdir() if p.suffix == ".yaml" and p.name != ".gitkeep"
    )

    if not rubric_files:
        print("No rubric files found (this is OK for task .1).", file=sys.stderr)
        return 0

    errors: list[str] = []
    for rubric_path in rubric_files:
        validate_rubric(rubric_path, errors)

    if errors:
        print(f"Rubric validation FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  ERROR: {err}", file=sys.stderr)
        return 1

    print(f"Validated {len(rubric_files)} rubric(s): all OK.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
