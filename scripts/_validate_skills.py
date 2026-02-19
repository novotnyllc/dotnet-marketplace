#!/usr/bin/env python3
"""
Validate all SKILL.md files and agent files in the dotnet-artisan plugin.

Checks (skills):
  1.  Required frontmatter fields: name, description
  2.  YAML frontmatter is well-formed (strict subset parser for flat key:value)
  3.  [skill:name] cross-references resolve against known IDs set
  4.  Context budget tracking with stable output keys
  5.  Name-directory consistency (name field must match skill directory name)
  6.  Extra frontmatter field detection (allowed: name, description, user-invocable,
      disable-model-invocation, context, model)
  6b. Type validation for optional fields (boolean/string type checking)
  7.  Description filler phrase detection (routing quality enforcement)
  8.  WHEN prefix regression detection (descriptions must not start with WHEN)
  9.  Scope section presence (## Scope header required)
  10. Out-of-scope section presence (## Out of scope header required)
  11. Out-of-scope attribution format (items should reference owning skill via [skill:])
  12. Self-referential cross-link detection (skill referencing itself -- error)
  13. Cross-reference cycle detection (post-processing, informational report only)

Checks (agents):
  14. Agent bare-ref detection using known IDs allowlist (informational)
  15. AGENTS.md bare-ref detection using known IDs allowlist (informational)

Infrastructure:
  - Known IDs set: {skill directory names} union {agent file stems}
  - ID collision detection between skills and agents (error)
  - BUDGET_STATUS computed from CURRENT_DESC_CHARS only (projected is informational)

Invoked by validate-skills.sh. All validation logic lives here to avoid
per-file subprocess spawning and ensure deterministic YAML parsing.

Uses a strict subset parser (not PyYAML) so validation behavior is identical
across all environments regardless of installed packages.
"""

import argparse
import re
import sys
from pathlib import Path

# Import shared agent frontmatter parser
sys.path.insert(0, str(Path(__file__).parent))
from _agent_frontmatter import parse_agent_frontmatter

# --- Quality Constants ---

# Canonical frontmatter fields. Any field beyond these triggers a warning.
# Reference: https://code.claude.com/docs/en/skills#frontmatter-reference
ALLOWED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "user-invocable",
    "disable-model-invocation",
    "context",
    "model",
}

# Type validation for optional frontmatter fields.
# Boolean fields must be true/false (not quoted strings like "false").
# String fields must be actual strings.
FIELD_TYPES = {
    "name": str,
    "description": str,
    "user-invocable": bool,
    "disable-model-invocation": bool,
    "context": str,
    "model": str,
}

# Filler phrases that reduce description routing quality.
# Case-insensitive patterns matched against the description text.
# "Covers" was the only instance found by the fn-49.1 audit; others are preventive.
FILLER_PHRASES = [
    re.compile(r"\bCovers\b", re.IGNORECASE),
    re.compile(r"\bhelps with\b", re.IGNORECASE),
    re.compile(r"\bguide to\b", re.IGNORECASE),
    re.compile(r"\bcomplete guide\b", re.IGNORECASE),
]

# Pattern to match [skill:name] references (for stripping before bare-ref scan)
SKILL_REF_PATTERN = re.compile(r"\[skill:[a-zA-Z0-9_-]+\]")

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


def has_section_header(body_text: str, header: str) -> bool:
    """Check if body text contains a specific ## level header."""
    pattern = re.compile(r"^## " + re.escape(header) + r"\s*$", re.MULTILINE)
    return bool(pattern.search(body_text))


def extract_oos_items(body_text: str) -> list:
    """Extract items from the Out of scope section.

    Returns list of (line_text, has_skill_ref) tuples for items in the
    Out of scope section (lines starting with - or numbered items).
    """
    items = []
    in_oos = False
    for line in body_text.split("\n"):
        stripped = line.strip()
        # Detect start of Out of scope section
        if re.match(r"^## Out of scope\s*$", stripped):
            in_oos = True
            continue
        # Detect next section header (end of Out of scope)
        if in_oos and re.match(r"^## ", stripped):
            break
        # Collect list items
        if in_oos and (stripped.startswith("- ") or re.match(r"^\d+\.\s", stripped)):
            has_ref = bool(re.search(r"\[skill:[a-zA-Z0-9_-]+\]", stripped))
            items.append((stripped, has_ref))
    return items


def strip_skill_refs(text: str) -> str:
    """Remove [skill:...] spans from text for bare-ref scanning."""
    return SKILL_REF_PATTERN.sub("", text)


def find_bare_refs(text: str, known_ids: set) -> list:
    """Find bare references to known IDs in text after stripping [skill:] spans.

    Also strips markdown link URLs to avoid false positives on link targets.
    Returns list of matched bare IDs.
    """
    # Strip [skill:...] spans
    cleaned = strip_skill_refs(text)
    # Strip markdown link URLs: [text](url) -> [text]
    cleaned = re.sub(r"\]\([^)]*\)", "]", cleaned)
    # Strip inline code that contains skill refs (already valid in backticks)
    # but keep other inline code for scanning

    found = []
    for known_id in sorted(known_ids):
        # Match word-boundary-delimited occurrences
        pattern = re.compile(r"(?<![a-zA-Z0-9_-])" + re.escape(known_id) + r"(?![a-zA-Z0-9_-])")
        if pattern.search(cleaned):
            found.append(known_id)
    return found


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

    # Extract body text and cross-references
    body_text = "\n".join(lines[body_start:])
    refs = extract_refs(body_text)

    # Check for scope sections
    has_scope = has_section_header(body_text, "Scope")
    has_oos = has_section_header(body_text, "Out of scope")
    oos_items = extract_oos_items(body_text) if has_oos else []

    # Type-validate optional fields (warnings, not errors)
    type_warnings = []
    for field_name, expected_type in FIELD_TYPES.items():
        if field_name in parsed and field_name not in ("name", "description"):
            value = parsed[field_name]
            if value is not None and not isinstance(value, expected_type):
                type_warnings.append(
                    f"frontmatter field '{field_name}' should be {expected_type.__name__} "
                    f"(got {type(value).__name__}: {value!r})"
                )

    return {
        "path": path,
        "valid": True,
        "name": name,
        "description": description,
        "desc_len": len(description),
        "refs": refs,
        "field_errors": field_errors,
        "type_warnings": type_warnings,
        "all_fields": set(parsed.keys()),
        "has_scope": has_scope,
        "has_oos": has_oos,
        "oos_items": oos_items,
    }


# --- Cycle Detection ---


def detect_cycles(ref_graph: dict) -> list:
    """Detect cycles in the cross-reference graph using DFS.

    Args:
        ref_graph: dict mapping skill_name -> list of referenced skill names

    Returns:
        List of cycles, where each cycle is a list of skill names forming a cycle
        path (last element repeats the first to show the loop).
    """
    seen_cycles = set()
    cycles = []
    rec_stack = []
    rec_set = set()
    visited = set()

    def dfs(node):
        visited.add(node)
        rec_stack.append(node)
        rec_set.add(node)

        for neighbor in ref_graph.get(node, []):
            if neighbor == node:
                # Self-reference handled separately as error
                continue
            if neighbor in rec_set:
                # Extract cycle from stack
                idx = rec_stack.index(neighbor)
                cycle_nodes = rec_stack[idx:]
                # Normalize: rotate so smallest node is first
                min_val = min(cycle_nodes)
                min_idx = cycle_nodes.index(min_val)
                rotated = cycle_nodes[min_idx:] + cycle_nodes[:min_idx]
                cycle_key = tuple(rotated)
                if cycle_key not in seen_cycles:
                    seen_cycles.add(cycle_key)
                    cycles.append(list(rotated) + [rotated[0]])
            elif neighbor not in visited:
                dfs(neighbor)

        rec_stack.pop()
        rec_set.remove(node)

    for node in sorted(ref_graph.keys()):
        if node not in visited:
            dfs(node)

    return cycles


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
    agents_dir = repo_root / "agents"

    if not skills_dir.is_dir():
        print(f"ERROR: No skills/ directory found at {skills_dir}")
        sys.exit(1)

    # Collect all SKILL.md files
    skill_files = sorted(skills_dir.rglob("SKILL.md"))

    if not skill_files:
        print(f"ERROR: No SKILL.md files found under {skills_dir}")
        sys.exit(1)

    # --- Build known IDs set ---
    # Skill directory names
    valid_skill_dirs = {f.parent.name for f in skill_files}

    # Agent file stems (filename without .md)
    agent_files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []
    agent_stems = {f.stem for f in agent_files}

    # Known IDs = skills union agents
    known_ids = valid_skill_dirs | agent_stems

    errors = 0
    warnings = 0
    total_desc_chars = 0
    skill_count = 0

    # Quality check counters (reported as stable output keys)
    name_dir_mismatches = 0
    extra_field_count = 0
    type_warning_count = 0
    filler_phrase_count = 0
    when_prefix_count = 0
    missing_scope_count = 0
    missing_oos_count = 0
    self_ref_count = 0
    agent_bare_ref_count = 0
    agentsmd_bare_ref_count = 0

    # Cross-reference graph for cycle detection
    ref_graph = {}

    print("=== SKILL.md Validation (parser: strict-subset) ===")
    print()

    # --- ID collision detection ---
    id_collisions = valid_skill_dirs & agent_stems
    if id_collisions:
        for collision in sorted(id_collisions):
            print(
                f"ERROR: ID collision between skill and agent: {collision}. "
                "Rename one to avoid ambiguity."
            )
            errors += 1
        print()

    if args.allow_planned_refs:
        print(
            "NOTE: --allow-planned-refs -- unresolved cross-references downgraded to warnings"
        )
        print()

    # Process each skill file
    for skill_file in skill_files:
        rel_path = skill_file.relative_to(repo_root)
        result = process_file(str(skill_file))

        if not result["valid"]:
            print(f"ERROR: {rel_path} -- invalid YAML frontmatter: {result['error']}")
            errors += 1
            continue

        name = result["name"]
        description = result["description"]
        desc_len = result["desc_len"]
        refs = result["refs"]
        all_fields = result["all_fields"]

        # Report field-level errors (type or missing)
        for fe in result.get("field_errors", []):
            print(f"ERROR: {rel_path} -- {fe}")
            errors += 1

        # --- Quality checks ---

        # Check 5: Name-directory consistency
        dir_name = skill_file.parent.name
        if name and name != dir_name:
            print(
                f"WARN:  {rel_path} -- name '{name}' does not match directory '{dir_name}'"
            )
            warnings += 1
            name_dir_mismatches += 1

        # Check 6: Extra frontmatter fields beyond allowed set
        extra_fields = all_fields - ALLOWED_FRONTMATTER_FIELDS
        if extra_fields:
            extras = ", ".join(sorted(extra_fields))
            print(
                f"WARN:  {rel_path} -- extra frontmatter fields: {extras}"
            )
            warnings += 1
            extra_field_count += len(extra_fields)

        # Check 6b: Type validation for optional fields
        for tw in result.get("type_warnings", []):
            print(f"WARN:  {rel_path} -- {tw}")
            warnings += 1
            type_warning_count += 1

        # Check 7: Filler phrase detection in description
        if description:
            for pattern in FILLER_PHRASES:
                match = pattern.search(description)
                if match:
                    print(
                        f"WARN:  {rel_path} -- description contains filler phrase '{match.group()}'"
                    )
                    warnings += 1
                    filler_phrase_count += 1

        # Check 8: WHEN prefix regression detection
        if description and description.startswith("WHEN "):
            print(
                f"WARN:  {rel_path} -- description starts with 'WHEN ' prefix (removed in fn-49.2)"
            )
            warnings += 1
            when_prefix_count += 1

        # Check 9: Scope section presence
        if not result["has_scope"]:
            print(f"WARN:  {rel_path} -- missing '## Scope' section")
            warnings += 1
            missing_scope_count += 1

        # Check 10: Out-of-scope section presence
        if not result["has_oos"]:
            print(f"WARN:  {rel_path} -- missing '## Out of scope' section")
            warnings += 1
            missing_oos_count += 1

        # Check 11: Out-of-scope attribution format
        if result["has_oos"]:
            for item_text, has_ref in result["oos_items"]:
                if not has_ref:
                    print(
                        f"WARN:  {rel_path} -- out-of-scope item lacks [skill:] attribution: "
                        f"{item_text[:60]}"
                    )
                    warnings += 1

        # Check 12: Self-referential cross-link detection (ERROR)
        if name and name in refs:
            print(
                f"ERROR: {rel_path} -- self-referential cross-link [skill:{name}]"
            )
            errors += 1
            self_ref_count += 1

        # Build cross-reference graph for cycle detection
        if name:
            ref_graph[name] = [r for r in refs if r != name]

        # Track budget only for valid descriptions
        if description:
            total_desc_chars += desc_len
            skill_count += 1

            if desc_len > args.max_desc_chars:
                print(
                    f"WARN:  {rel_path} -- description is {desc_len} chars (target: <={args.max_desc_chars})"
                )
                warnings += 1

        # Validate cross-references against known IDs set
        for ref_name in refs:
            if ref_name == name:
                # Already reported as self-ref error above
                continue
            if ref_name not in known_ids:
                if args.allow_planned_refs:
                    print(
                        f"WARN:  {rel_path} -- unresolved cross-reference [skill:{ref_name}] (planned skill, no directory yet)"
                    )
                    warnings += 1
                else:
                    print(
                        f"ERROR: {rel_path} -- broken cross-reference [skill:{ref_name}] (no matching skill or agent found)"
                    )
                    errors += 1

    # --- Agent file scanning ---
    print()
    print("=== Agent File Validation ===")
    print()

    for agent_file in agent_files:
        rel_path = agent_file.relative_to(repo_root)
        agent_stem = agent_file.stem

        # Parse agent frontmatter using shared module
        fm = parse_agent_frontmatter(str(agent_file))

        # Read full file content for cross-ref and bare-ref scanning
        try:
            agent_content = agent_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"ERROR: {rel_path} -- cannot read: {e}")
            errors += 1
            continue

        agent_content = agent_content.replace("\r\n", "\n").replace("\r", "\n")

        # Extract [skill:] refs from agent file and validate
        agent_refs = extract_refs(agent_content)
        for ref_name in agent_refs:
            if ref_name not in known_ids:
                if args.allow_planned_refs:
                    print(
                        f"WARN:  {rel_path} -- unresolved cross-reference [skill:{ref_name}]"
                    )
                    warnings += 1
                else:
                    print(
                        f"ERROR: {rel_path} -- broken cross-reference [skill:{ref_name}] (no matching skill or agent found)"
                    )
                    errors += 1

        # Build agent cross-ref graph entries
        if agent_stem:
            ref_graph[agent_stem] = [r for r in agent_refs if r != agent_stem]

        # Bare-ref detection in agent files (informational, not error)
        bare_refs = find_bare_refs(agent_content, known_ids)
        if bare_refs:
            for bare_id in bare_refs:
                print(
                    f"INFO:  {rel_path} -- bare reference to '{bare_id}' (not wrapped in [skill:])"
                )
            agent_bare_ref_count += len(bare_refs)

    # --- AGENTS.md bare-ref scanning ---
    agentsmd_path = repo_root / "AGENTS.md"
    if agentsmd_path.is_file():
        try:
            agentsmd_content = agentsmd_path.read_text(encoding="utf-8")
            agentsmd_content = agentsmd_content.replace("\r\n", "\n").replace("\r", "\n")
            agentsmd_bare_refs = find_bare_refs(agentsmd_content, known_ids)
            if agentsmd_bare_refs:
                for bare_id in agentsmd_bare_refs:
                    print(
                        f"INFO:  AGENTS.md -- bare reference to '{bare_id}' (not wrapped in [skill:])"
                    )
                agentsmd_bare_ref_count += len(agentsmd_bare_refs)
        except Exception as e:
            print(f"WARN:  AGENTS.md -- cannot read: {e}")
            warnings += 1

    # --- Cross-reference cycle detection (informational) ---
    print()
    print("=== Cross-Reference Cycle Report ===")

    cycles = detect_cycles(ref_graph)
    if cycles:
        print(f"Found {len(cycles)} cross-reference cycle(s) (informational, not errors):")
        for cycle in cycles:
            cycle_str = " -> ".join(cycle)
            print(f"  CYCLE: {cycle_str}")
    else:
        print("No cross-reference cycles detected.")

    # --- Budget Report ---
    print()
    print("=== Budget Report ===")

    projected_desc_chars = args.projected_skills * args.max_desc_chars

    # Determine budget status from CURRENT_DESC_CHARS only
    # (projected is informational, not part of status determination)
    budget_status = "OK"
    if total_desc_chars >= args.fail_threshold:
        budget_status = "FAIL"
    elif total_desc_chars >= args.warn_threshold:
        budget_status = "WARN"

    # Stable CI-parseable output keys
    print(f"CURRENT_DESC_CHARS={total_desc_chars}")
    print(f"PROJECTED_DESC_CHARS={projected_desc_chars}")
    print(f"BUDGET_STATUS={budget_status}")
    print(f"NAME_DIR_MISMATCHES={name_dir_mismatches}")
    print(f"EXTRA_FIELD_COUNT={extra_field_count}")
    print(f"TYPE_WARNING_COUNT={type_warning_count}")
    print(f"FILLER_PHRASE_COUNT={filler_phrase_count}")
    print(f"WHEN_PREFIX_COUNT={when_prefix_count}")
    print(f"MISSING_SCOPE_COUNT={missing_scope_count}")
    print(f"MISSING_OOS_COUNT={missing_oos_count}")
    print(f"SELF_REF_COUNT={self_ref_count}")
    print(f"AGENT_BARE_REF_COUNT={agent_bare_ref_count}")
    print(f"AGENTSMD_BARE_REF_COUNT={agentsmd_bare_ref_count}")

    print()
    print(f"Skills validated: {skill_count}")
    print(f"Agents scanned: {len(agent_files)}")
    print(f"Known IDs: {len(known_ids)} ({len(valid_skill_dirs)} skills + {len(agent_stems)} agents)")
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
