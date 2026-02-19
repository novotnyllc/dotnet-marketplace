#!/usr/bin/env python3
"""
Shared agent frontmatter parser for dotnet-artisan validation tools.

Parsing contract:
  - Parses only top-level `name:` and `description:` fields with zero indentation.
  - Supported value forms:
    - Plain scalars:        description: Some text
    - Single-quoted strings: description: 'Some text'
    - Double-quoted strings: description: "Some text"
    - Block scalars:         description: | (or >) with indented continuation lines
  - Returns None for fields it cannot parse.
  - Ignores sequences, flow constructs ([, {), and nested mappings entirely.

Consumers:
  - scripts/_validate_skills.py (T3 -- agent validation)
  - scripts/validate-similarity.py (T13 -- similarity detection)

Ownership: T3 creates and owns this file. T13 imports it as-is.
"""

import re
from pathlib import Path


def parse_agent_frontmatter(file_path: str) -> dict:
    """Parse name and description from an agent markdown file's YAML frontmatter.

    Args:
        file_path: Path to the agent .md file.

    Returns:
        A dict with keys 'name' and 'description', each either a string or None.
        Returns {'name': None, 'description': None} if frontmatter is missing
        or cannot be parsed.
    """
    result = {"name": None, "description": None}

    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except Exception:
        return result

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # Check for opening delimiter
    if not lines or lines[0].strip() != "---":
        return result

    # Find closing delimiter and extract frontmatter lines
    fm_lines = []
    fm_end = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            fm_end = i
            break
        fm_lines.append(line)

    if fm_end is None:
        return result

    # Parse only top-level name: and description: with zero indentation
    target_fields = {"name", "description"}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]

        # Must start at column 0 (no leading whitespace) to be top-level
        if line != line.lstrip():
            i += 1
            continue

        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Match key: value at zero indentation
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)", line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        raw_value = m.group(2).strip()

        if key not in target_fields:
            i += 1
            continue

        # Skip flow constructs and sequences
        if raw_value.startswith("[") or raw_value.startswith("{") or raw_value.startswith("- "):
            i += 1
            continue

        # Handle block scalars (| and >)
        if raw_value in ("|", ">", "|+", "|-", ">+", ">-"):
            block_lines = []
            i += 1
            while i < len(fm_lines):
                bl = fm_lines[i]
                if bl.strip() == "" or (len(bl) > 0 and bl[0] in (" ", "\t")):
                    block_lines.append(bl)
                    i += 1
                else:
                    break
            if block_lines:
                indent = len(block_lines[0]) - len(block_lines[0].lstrip())
                value = "\n".join(
                    bl[indent:] if len(bl) > indent else "" for bl in block_lines
                )
            else:
                value = ""
            if raw_value.startswith(">"):
                value = re.sub(r"(?<!\n)\n(?!\n)", " ", value)
            result[key] = value.strip() if value.strip() else None
            continue

        # Handle double-quoted strings
        if raw_value.startswith('"'):
            if raw_value.endswith('"') and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                # Unclosed quote -- return None for this field
                pass
            i += 1
            continue

        # Handle single-quoted strings
        if raw_value.startswith("'"):
            if raw_value.endswith("'") and len(raw_value) > 1:
                result[key] = raw_value[1:-1]
            else:
                pass
            i += 1
            continue

        # Plain scalar
        if raw_value:
            result[key] = raw_value
        i += 1

    return result
