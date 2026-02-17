#!/usr/bin/env python3
"""
Validate all SKILL.md files in the dotnet-artisan plugin.

Checks:
  1. Required frontmatter fields: name, description
  2. YAML frontmatter is well-formed (strict subset parser for flat key:value)
  3. [skill:name] cross-references point to existing skill directories
  4. Context budget tracking with stable output keys

Invoked by validate-skills.sh. All validation logic lives here to avoid
per-file subprocess spawning and ensure deterministic YAML parsing.

Uses a strict subset parser (not PyYAML) so validation behavior is identical
across all environments regardless of installed packages.
"""

import argparse
import re
import sys
from pathlib import Path

# --- YAML Parsing ---


def parse_frontmatter(text: str) -> dict:
    """Parse frontmatter using a strict subset parser.

    Accepts only flat key: value mappings (the YAML subset used in SKILL.md
    frontmatter). Rejects flow constructs ([, {) and sequences (- ).

    Uses a deterministic strict parser so validation is environment-independent
    (no PyYAML dependency, identical behavior locally and in CI).
    """
    result = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Must be key: value (or key:)
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)", stripped)
        if not m:
            raise ValueError(
                f"line {i + 2}: invalid YAML syntax: {stripped[:60]}"
            )

        key = m.group(1)
        raw_value = m.group(2).strip()

        # Reject flow constructs that indicate non-flat YAML
        if raw_value.startswith("[") or raw_value.startswith("{"):
            raise ValueError(
                f"line {i + 2}: flow collections not allowed in frontmatter: {raw_value[:40]}"
            )

        # Handle block scalars (| and >)
        if raw_value in ("|", ">", "|+", "|-", ">+", ">-"):
            block_lines = []
            i += 1
            while i < len(lines):
                if lines[i].strip() == "" or (
                    len(lines[i]) > 0 and lines[i][0] in (" ", "\t")
                ):
                    block_lines.append(lines[i])
                    i += 1
                else:
                    break
            if block_lines:
                indent = len(block_lines[0]) - len(block_lines[0].lstrip())
                value = "\n".join(
                    l[indent:] if len(l) > indent else "" for l in block_lines
                )
            else:
                value = ""
            if raw_value.startswith(">"):
                value = re.sub(r"(?<!\n)\n(?!\n)", " ", value)
            result[key] = value.strip()
            continue

        # Handle double-quoted strings
        if raw_value.startswith('"'):
            if raw_value.endswith('"') and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                raise ValueError(f"line {i + 2}: unclosed double quote")
            i += 1
            continue

        # Handle single-quoted strings
        if raw_value.startswith("'"):
            if raw_value.endswith("'") and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                raise ValueError(f"line {i + 2}: unclosed single quote")
            i += 1
            continue

        # Reject sequence items
        if raw_value.startswith("- "):
            raise ValueError(
                f"line {i + 2}: sequences not allowed in frontmatter"
            )

        # Handle booleans and other scalars
        if raw_value.lower() in ("true", "yes"):
            result[key] = True
        elif raw_value.lower() in ("false", "no"):
            result[key] = False
        elif raw_value.lower() in ("null", "~", ""):
            result[key] = None
        else:
            result[key] = raw_value

        i += 1

    return result


# --- File Processing ---


def extract_refs(body_text: str) -> list:
    """Extract unique [skill:name] cross-references from body text."""
    return list(dict.fromkeys(re.findall(r"\[skill:([a-zA-Z0-9_-]+)\]", body_text)))


def process_file(path: str) -> dict:
    """Process a single SKILL.md file. Returns a result dict."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"path": path, "valid": False, "error": str(e)}

    # Normalize CRLF to LF
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    lines = content.split("\n")

    # Check for opening delimiter
    if not lines or lines[0].strip() != "---":
        return {"path": path, "valid": False, "error": "missing opening ---"}

    # Find closing delimiter and extract frontmatter
    fm_lines = []
    body_start = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(line)

    if body_start is None:
        return {"path": path, "valid": False, "error": "missing closing ---"}

    fm_text = "\n".join(fm_lines)

    # Parse YAML frontmatter
    try:
        parsed = parse_frontmatter(fm_text)
    except ValueError as e:
        return {"path": path, "valid": False, "error": str(e)}

    # Extract and type-validate required fields
    name_raw = parsed.get("name")
    desc_raw = parsed.get("description")
    field_errors = []

    if name_raw is None or (isinstance(name_raw, str) and not name_raw.strip()):
        field_errors.append("missing required frontmatter field: name")
    elif not isinstance(name_raw, str):
        field_errors.append(
            f"frontmatter field 'name' must be a string (got {type(name_raw).__name__})"
        )

    if desc_raw is None or (isinstance(desc_raw, str) and not desc_raw.strip()):
        field_errors.append("missing required frontmatter field: description")
    elif not isinstance(desc_raw, str):
        field_errors.append(
            f"frontmatter field 'description' must be a string (got {type(desc_raw).__name__})"
        )

    name = name_raw.strip() if isinstance(name_raw, str) else ""
    description = desc_raw.strip() if isinstance(desc_raw, str) else ""

    # Extract cross-references from body
    body_text = "\n".join(lines[body_start:])
    refs = extract_refs(body_text)

    return {
        "path": path,
        "valid": True,
        "name": name,
        "description": description,
        "desc_len": len(description),
        "refs": refs,
        "field_errors": field_errors,
    }


# --- Main ---


def main():
    parser = argparse.ArgumentParser(description="Validate SKILL.md files")
    parser.add_argument("--repo-root", required=True, help="Repository root")
    parser.add_argument(
        "--projected-skills", type=int, default=100, help="Projected skill count"
    )
    parser.add_argument(
        "--max-desc-chars", type=int, default=120, help="Max description chars"
    )
    parser.add_argument(
        "--warn-threshold", type=int, default=12000, help="Budget warn threshold"
    )
    parser.add_argument(
        "--fail-threshold", type=int, default=15000, help="Budget fail threshold"
    )
    parser.add_argument(
        "--allow-planned-refs",
        action="store_true",
        help="Downgrade unresolved refs to warnings",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skills_dir = repo_root / "skills"

    if not skills_dir.is_dir():
        print(f"ERROR: No skills/ directory found at {skills_dir}")
        sys.exit(1)

    # Collect all SKILL.md files
    skill_files = sorted(skills_dir.rglob("SKILL.md"))

    if not skill_files:
        print(f"ERROR: No SKILL.md files found under {skills_dir}")
        sys.exit(1)

    # Build set of valid skill directory names
    valid_skill_dirs = {f.parent.name for f in skill_files}

    errors = 0
    warnings = 0
    total_desc_chars = 0
    skill_count = 0

    print("=== SKILL.md Validation (parser: strict-subset) ===")
    print()

    if args.allow_planned_refs:
        print(
            "NOTE: --allow-planned-refs -- unresolved cross-references downgraded to warnings"
        )
        print()

    # Process each file
    for skill_file in skill_files:
        rel_path = skill_file.relative_to(repo_root)
        result = process_file(str(skill_file))

        if not result["valid"]:
            print(f"ERROR: {rel_path} -- invalid YAML frontmatter: {result['error']}")
            errors += 1
            continue

        description = result["description"]
        desc_len = result["desc_len"]
        refs = result["refs"]

        # Report field-level errors (type or missing)
        for fe in result.get("field_errors", []):
            print(f"ERROR: {rel_path} -- {fe}")
            errors += 1

        # Track budget only for valid descriptions
        if description:
            total_desc_chars += desc_len
            skill_count += 1

            if desc_len > args.max_desc_chars:
                print(
                    f"WARN:  {rel_path} -- description is {desc_len} chars (target: <={args.max_desc_chars})"
                )
                warnings += 1

        # Validate cross-references
        for ref_name in refs:
            if ref_name not in valid_skill_dirs:
                if args.allow_planned_refs:
                    print(
                        f"WARN:  {rel_path} -- unresolved cross-reference [skill:{ref_name}] (planned skill, no directory yet)"
                    )
                    warnings += 1
                else:
                    print(
                        f"ERROR: {rel_path} -- broken cross-reference [skill:{ref_name}] (no skill directory found)"
                    )
                    errors += 1

    # --- Budget Report ---
    print()
    print("=== Budget Report ===")

    projected_desc_chars = args.projected_skills * args.max_desc_chars

    # Determine budget status
    budget_status = "OK"
    if (
        total_desc_chars >= args.fail_threshold
        or projected_desc_chars > args.fail_threshold
    ):
        budget_status = "FAIL"
    elif (
        total_desc_chars >= args.warn_threshold
        or projected_desc_chars >= args.warn_threshold
    ):
        budget_status = "WARN"

    # Stable CI-parseable output keys
    print(f"CURRENT_DESC_CHARS={total_desc_chars}")
    print(f"PROJECTED_DESC_CHARS={projected_desc_chars}")
    print(f"BUDGET_STATUS={budget_status}")

    print()
    print(f"Skills validated: {skill_count}")
    print(f"Current budget: {total_desc_chars} / {args.fail_threshold} chars")
    print(
        f"Projected budget ({args.projected_skills} skills x {args.max_desc_chars} chars): {projected_desc_chars} chars"
    )

    if budget_status == "WARN":
        print(
            f"WARNING: Budget approaching limit (WARN threshold: {args.warn_threshold} chars)"
        )
        warnings += 1

    if budget_status == "FAIL":
        print(
            f"FAIL: Budget exceeds hard limit (FAIL threshold: {args.fail_threshold} chars)"
        )
        errors += 1

    # --- Summary ---
    print()
    print("=== Summary ===")
    print(f"Errors: {errors}")
    print(f"Warnings: {warnings}")

    if errors > 0:
        print()
        print(f"FAILED: {errors} error(s) found")
        sys.exit(1)

    print()
    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
