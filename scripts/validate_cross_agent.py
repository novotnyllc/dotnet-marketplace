#!/usr/bin/env python3
"""
Cross-agent conformance validator for dist/ outputs.

Validates behavioral equivalence across Claude, Copilot, and Codex generated
outputs by running 7 conformance checks:

  1. Routing parity       -- every SKILL.md description appears in all formats
  2. Trigger coverage     -- corpus entries match expected skills in all formats
  3. Graceful degradation -- Claude-only features absent from Copilot/Codex
  4. Structural comparison-- body content identical after known transformations
  5. Cross-ref integrity  -- [skill:name] resolved correctly per format
  6. Corpus completeness  -- every skill category has at least one corpus entry
  7. Manifest validation  -- manifest.json schema, required fields, SHA256 correctness

Usage:
    python3 scripts/validate_cross_agent.py [--repo-root <path>] [--dist-dir <path>]

Reuses the frontmatter parser from _validate_skills.py. No .NET SDK dependency.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Import shared frontmatter parser from _validate_skills.py
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from _validate_skills import parse_frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def read_file(path: Path) -> str:
    """Read a file with CRLF normalization."""
    content = path.read_text(encoding="utf-8")
    return content.replace("\r\n", "\n").replace("\r", "\n")


def parse_skill_file(path: Path) -> dict:
    """Parse a SKILL.md file into frontmatter dict + body string."""
    content = read_file(path)
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing opening ---")

    fm_lines = []
    body_start = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(line)

    if body_start is None:
        raise ValueError(f"{path}: missing closing ---")

    fm_text = "\n".join(fm_lines)
    parsed = parse_frontmatter(fm_text)
    body = "\n".join(lines[body_start:])

    return {
        "frontmatter": parsed,
        "body": body,
        "name": parsed.get("name", ""),
        "description": parsed.get("description", ""),
    }


def load_agent_names(plugin_json_path: Path) -> list:
    """Read agent names from plugin.json agents array (canonical source of truth)."""
    try:
        data = json.loads(plugin_json_path.read_text(encoding="utf-8"))
        return [Path(a).stem for a in data.get("agents", [])]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def normalize_whitespace(text: str) -> str:
    """Normalize text for comparison: collapse whitespace, strip blank lines."""
    lines = text.split("\n")
    normalized = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            # Collapse internal whitespace
            stripped = re.sub(r"\s+", " ", stripped)
            normalized.append(stripped)
    return "\n".join(normalized)


# ---------------------------------------------------------------------------
# Check 1: Routing parity
# ---------------------------------------------------------------------------


def check_routing_parity(
    canonical_skills: list, dist_dir: Path
) -> list:
    """Verify every canonical SKILL.md description appears in all generated formats.

    Returns a list of failure dicts with skill name, format, and reason.
    """
    failures = []

    copilot_index_path = dist_dir / "copilot" / ".github" / "copilot-instructions.md"
    codex_index_path = dist_dir / "codex" / "AGENTS.md"

    if not copilot_index_path.exists():
        failures.append({
            "skill": "(global)",
            "format": "copilot",
            "reason": "copilot-instructions.md not found",
        })
        return failures

    if not codex_index_path.exists():
        failures.append({
            "skill": "(global)",
            "format": "codex",
            "reason": "AGENTS.md not found",
        })
        return failures

    copilot_index = read_file(copilot_index_path)
    codex_index = read_file(codex_index_path)

    for skill in canonical_skills:
        name = skill["name"]
        description = skill["description"]

        if not description:
            continue

        # Normalize the description for fuzzy matching: collapse whitespace
        desc_normalized = re.sub(r"\s+", " ", description.strip())

        # Check Claude: description should be in the original SKILL.md frontmatter
        claude_skill_path = dist_dir / "claude" / "skills" / skill["category"] / skill["dir_name"] / "SKILL.md"
        if claude_skill_path.exists():
            claude_content = read_file(claude_skill_path)
            claude_content_normalized = re.sub(r"\s+", " ", claude_content)
            if desc_normalized not in claude_content_normalized:
                failures.append({
                    "skill": name,
                    "format": "claude",
                    "reason": f"description not found in dist/claude/ skill file",
                })
        else:
            failures.append({
                "skill": name,
                "format": "claude",
                "reason": f"skill file not found: {claude_skill_path.relative_to(dist_dir)}",
            })

        # Check Copilot: description should appear in routing index
        copilot_normalized = re.sub(r"\s+", " ", copilot_index)
        if desc_normalized not in copilot_normalized:
            failures.append({
                "skill": name,
                "format": "copilot",
                "reason": "description not found in copilot-instructions.md routing index",
            })

        # Check Codex: description should appear in AGENTS.md routing index
        codex_normalized = re.sub(r"\s+", " ", codex_index)
        if desc_normalized not in codex_normalized:
            failures.append({
                "skill": name,
                "format": "codex",
                "reason": "description not found in AGENTS.md routing index",
            })

    return failures


# ---------------------------------------------------------------------------
# Check 2: Trigger coverage
# ---------------------------------------------------------------------------


def check_trigger_coverage(
    corpus: list, canonical_skills: list, dist_dir: Path
) -> list:
    """Validate corpus entries match expected skills in all formats.

    For each corpus entry, verify the expected_skill exists in all three
    output formats (its description is routable from the index/routing file).

    Returns a list of failure dicts.
    """
    failures = []

    # Build lookup of canonical skills by dir_name
    skill_by_dir = {s["dir_name"]: s for s in canonical_skills}

    copilot_index_path = dist_dir / "copilot" / ".github" / "copilot-instructions.md"
    codex_index_path = dist_dir / "codex" / "AGENTS.md"

    copilot_index = read_file(copilot_index_path) if copilot_index_path.exists() else ""
    codex_index = read_file(codex_index_path) if codex_index_path.exists() else ""

    for entry in corpus:
        query = entry["query"]
        expected = entry["expected_skill"]
        category = entry["category"]

        # Verify expected skill exists in canonical source
        if expected not in skill_by_dir:
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "canonical",
                "reason": f"expected skill '{expected}' not found in canonical skills/",
            })
            continue

        skill = skill_by_dir[expected]

        # Check Claude format: skill directory exists in dist/claude/
        claude_skill = dist_dir / "claude" / "skills" / category / expected / "SKILL.md"
        if not claude_skill.exists():
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "claude",
                "reason": f"skill not found at {claude_skill.relative_to(dist_dir)}",
            })

        # Check Copilot format: skill referenced in routing index
        if expected not in copilot_index:
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "copilot",
                "reason": f"skill '{expected}' not referenced in copilot-instructions.md",
            })

        # Check Copilot format: per-skill file exists
        copilot_skill = dist_dir / "copilot" / "skills" / expected / "SKILL.md"
        if not copilot_skill.exists():
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "copilot",
                "reason": f"per-skill file not found at {copilot_skill.relative_to(dist_dir)}",
            })

        # Check Codex format: skill referenced in AGENTS.md
        if expected not in codex_index:
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "codex",
                "reason": f"skill '{expected}' not referenced in AGENTS.md",
            })

        # Check Codex format: category AGENTS.md exists and contains skill
        codex_cat = dist_dir / "codex" / "skills" / category / "AGENTS.md"
        if codex_cat.exists():
            codex_cat_content = read_file(codex_cat)
            if skill["name"] not in codex_cat_content:
                failures.append({
                    "query": query,
                    "expected_skill": expected,
                    "format": "codex",
                    "reason": f"skill name '{skill['name']}' not found in category AGENTS.md",
                })
        else:
            failures.append({
                "query": query,
                "expected_skill": expected,
                "format": "codex",
                "reason": f"category AGENTS.md not found: {codex_cat.relative_to(dist_dir)}",
            })

    return failures


# ---------------------------------------------------------------------------
# Check 3: Graceful degradation
# ---------------------------------------------------------------------------


def check_graceful_degradation(
    agent_names: list, dist_dir: Path
) -> list:
    """Detect Claude-only feature references in non-Claude outputs.

    Checks that hooks, MCP tools, agent references, and plugin root paths
    are absent from Copilot and Codex outputs.

    Returns a list of failure dicts.
    """
    failures = []

    # Build detection patterns (same as generate_dist.py)
    patterns = []
    pattern_names = []

    if agent_names:
        patterns.append(
            re.compile(
                r"\b(?:" + "|".join(re.escape(a) for a in agent_names) + r")\s+agent\b",
                re.IGNORECASE,
            )
        )
        pattern_names.append("agent-reference")

    patterns.append(
        re.compile(r"(?:SessionStart hook|PostToolUse hook|hook detect)", re.IGNORECASE)
    )
    pattern_names.append("hook-reference")

    patterns.append(re.compile(r"mcp__\w+__"))
    pattern_names.append("mcp-tool-reference")

    patterns.append(re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}"))
    pattern_names.append("plugin-root-path")

    # Scan Copilot output
    copilot_dir = dist_dir / "copilot"
    if copilot_dir.exists():
        for md_file in sorted(copilot_dir.rglob("*.md")):
            content = read_file(md_file)
            rel_path = md_file.relative_to(dist_dir)
            for line_num, line in enumerate(content.split("\n"), 1):
                for pat, pat_name in zip(patterns, pattern_names):
                    m = pat.search(line)
                    if m:
                        failures.append({
                            "file": str(rel_path),
                            "line": line_num,
                            "format": "copilot",
                            "pattern": pat_name,
                            "match": m.group(0),
                            "reason": f"Claude-only {pat_name} found: '{m.group(0)}'",
                        })

    # Scan Codex output
    codex_dir = dist_dir / "codex"
    if codex_dir.exists():
        for md_file in sorted(codex_dir.rglob("*.md")):
            content = read_file(md_file)
            rel_path = md_file.relative_to(dist_dir)
            for line_num, line in enumerate(content.split("\n"), 1):
                for pat, pat_name in zip(patterns, pattern_names):
                    m = pat.search(line)
                    if m:
                        failures.append({
                            "file": str(rel_path),
                            "line": line_num,
                            "format": "codex",
                            "pattern": pat_name,
                            "match": m.group(0),
                            "reason": f"Claude-only {pat_name} found: '{m.group(0)}'",
                        })

    return failures


# ---------------------------------------------------------------------------
# Check 4: Structural comparison
# ---------------------------------------------------------------------------


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter (--- ... ---) from text."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return text
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "\n".join(lines[i + 1:])
    return text


def _strip_crossrefs(text: str) -> str:
    """Normalize cross-references to a canonical placeholder.

    Handles all three formats:
      - [skill:name]           (Claude)
      - [skill:name](../path)  (Copilot)
      - [name](#anchor)        (Codex)
    """
    # Copilot: [skill:name](../name/SKILL.md) -> XREF:name
    text = re.sub(
        r"\[skill:([a-zA-Z0-9_-]+)\]\(\.\./[a-zA-Z0-9_-]+/SKILL\.md\)",
        r"XREF:\1",
        text,
    )
    # Codex: [name](#anchor) -> XREF:name (only for skill-like names)
    text = re.sub(
        r"\[([a-zA-Z0-9_-]+)\]\(#[a-zA-Z0-9_-]+\)",
        r"XREF:\1",
        text,
    )
    # Claude: [skill:name] -> XREF:name
    text = re.sub(
        r"\[skill:([a-zA-Z0-9_-]+)\]",
        r"XREF:\1",
        text,
    )
    return text


def _strip_generated_prefix(text: str, name: str, description: str) -> str:
    """Remove the generated heading + description prefix from transformed output.

    generate_dist.py prepends: '# {name}\\n\\n{description}\\n\\n' to the body.
    We strip exactly that prefix to recover the original body content.
    """
    # Build the expected prefix pattern
    prefix = f"# {name}\n"
    if not text.startswith(prefix):
        return text

    rest = text[len(prefix):]

    # Strip blank lines after heading
    while rest.startswith("\n"):
        rest = rest[1:]

    # Strip description paragraph if present
    if description:
        desc_normalized = description.strip()
        rest_line_end = rest.find("\n")
        if rest_line_end == -1:
            rest_line_end = len(rest)
        first_line = rest[:rest_line_end].strip()

        if first_line == desc_normalized:
            rest = rest[rest_line_end:]
            # Strip blank lines after description
            while rest.startswith("\n"):
                rest = rest[1:]

    return rest


def _strip_generated_codex_prefix(text: str, name: str, description: str) -> str:
    """Remove the generated ## heading + description prefix from a Codex section.

    generate_dist.py produces sections like:
      ## {name}
      <blank>
      {description}
      <blank>
      {body}
      ---
    """
    prefix = f"## {name}\n"
    if not text.startswith(prefix):
        return text

    rest = text[len(prefix):]

    # Strip blank lines after heading
    while rest.startswith("\n"):
        rest = rest[1:]

    # Strip description paragraph if present
    if description:
        desc_normalized = description.strip()
        rest_line_end = rest.find("\n")
        if rest_line_end == -1:
            rest_line_end = len(rest)
        first_line = rest[:rest_line_end].strip()

        if first_line == desc_normalized:
            rest = rest[rest_line_end:]
            # Strip blank lines after description
            while rest.startswith("\n"):
                rest = rest[1:]

    return rest


def _build_claude_only_patterns(agent_names: list) -> list:
    """Build regex patterns for Claude-only line detection (same as generate_dist.py)."""
    patterns = []
    if agent_names:
        patterns.append(
            re.compile(
                r"\b(?:" + "|".join(re.escape(a) for a in agent_names) + r")\s+agent\b",
                re.IGNORECASE,
            )
        )
    patterns.append(
        re.compile(r"(?:SessionStart hook|PostToolUse hook|hook detect)", re.IGNORECASE)
    )
    patterns.append(re.compile(r"mcp__\w+__"))
    patterns.append(re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}"))
    return patterns


def _remove_claude_only_lines(text: str, patterns: list) -> str:
    """Remove lines matching Claude-only patterns and clean up orphaned tables."""
    lines = text.split("\n")
    filtered = [line for line in lines if not any(p.search(line) for p in patterns)]
    result = "\n".join(filtered)
    # Clean orphaned markdown tables
    result = re.sub(
        r"(?m)^\|[^\n]+\|\n\|[-| :]+\|\n(?=\n|$)",
        "",
        result,
    )
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


def check_structural_comparison(
    canonical_skills: list, agent_names: list, dist_dir: Path
) -> list:
    """After applying known transformations, compare remaining body content.

    For each skill, extract the body from:
      - Claude: raw SKILL.md body (strip frontmatter)
      - Copilot: per-skill file (strip heading/desc, reverse cross-ref transform)
      - Codex: per-category AGENTS.md section (extract section, strip heading/desc)

    After normalizing cross-refs and removing Claude-only lines from the
    Claude baseline, the remaining content should be textually identical
    modulo whitespace.

    Returns a list of failure dicts with diff snippets.
    """
    failures = []
    claude_only_patterns = _build_claude_only_patterns(agent_names)
    all_skill_names = {s["name"] for s in canonical_skills}

    for skill in canonical_skills:
        name = skill["name"]
        dir_name = skill["dir_name"]
        category = skill["category"]
        skill_desc = skill["description"]

        # --- Claude body ---
        claude_path = dist_dir / "claude" / "skills" / category / dir_name / "SKILL.md"
        if not claude_path.exists():
            continue  # Already caught in routing parity

        claude_raw = read_file(claude_path)
        claude_body = _strip_frontmatter(claude_raw).lstrip("\n")

        # Build the expected baseline: Claude body with Claude-only lines
        # removed and cross-refs normalized
        baseline = _remove_claude_only_lines(claude_body, claude_only_patterns)
        baseline = _strip_crossrefs(baseline)
        # Strip trailing --- separators (visual dividers, not structural)
        baseline = re.sub(r"\n---\s*$", "", baseline.rstrip())
        baseline_normalized = normalize_whitespace(baseline)

        # --- Copilot body ---
        copilot_path = dist_dir / "copilot" / "skills" / dir_name / "SKILL.md"
        if copilot_path.exists():
            copilot_raw = read_file(copilot_path)
            copilot_body = _strip_generated_prefix(copilot_raw, name, skill_desc)
            copilot_body = _strip_crossrefs(copilot_body)
            copilot_body = re.sub(r"\n---\s*$", "", copilot_body.rstrip())
            copilot_normalized = normalize_whitespace(copilot_body)

            if baseline_normalized != copilot_normalized:
                # Generate a compact diff snippet
                diff = _compact_diff(baseline_normalized, copilot_normalized)
                failures.append({
                    "skill": name,
                    "format": "copilot",
                    "reason": "structural mismatch after transformation",
                    "diff": diff,
                })

        # --- Codex body ---
        codex_cat_path = dist_dir / "codex" / "skills" / category / "AGENTS.md"
        if codex_cat_path.exists():
            codex_content = read_file(codex_cat_path)
            codex_section = _extract_codex_section(codex_content, name, all_skill_names)
            if codex_section is not None:
                # Codex sections start with ## name, desc paragraph, then body
                codex_body = _strip_generated_codex_prefix(codex_section, name, skill_desc)
                codex_body = _strip_crossrefs(codex_body)
                codex_body = re.sub(r"\n---\s*$", "", codex_body.rstrip())
                codex_normalized = normalize_whitespace(codex_body)

                if baseline_normalized != codex_normalized:
                    diff = _compact_diff(baseline_normalized, codex_normalized)
                    failures.append({
                        "skill": name,
                        "format": "codex",
                        "reason": "structural mismatch after transformation",
                        "diff": diff,
                    })

    return failures


def _extract_codex_section(content: str, skill_name: str, all_skill_names: set) -> str | None:
    """Extract a single skill section from a Codex category AGENTS.md.

    Sections are structured as:
      ## skill-name
      <blank>
      description
      <blank>
      body content (may contain ## subsection headings and --- separators)
      <blank>
      ---
      <blank>
      ## next-skill-name

    Since body content itself can contain --- separators and ## headings,
    we delimit sections by looking for the next ## heading that matches a
    known skill name from the canonical set.
    """
    lines = content.split("\n")
    in_section = False
    section_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped == f"## {skill_name}":
            in_section = True
            section_lines = [line]
            continue

        if in_section:
            # Check if this is a new skill section heading
            if stripped.startswith("## "):
                heading_text = stripped[3:].strip()
                if heading_text in all_skill_names and heading_text != skill_name:
                    break
            section_lines.append(line)

    if not section_lines:
        return None

    # Trim trailing --- separator and blank lines
    while section_lines and section_lines[-1].strip() in ("", "---"):
        section_lines.pop()

    return "\n".join(section_lines)


def _compact_diff(expected: str, actual: str, context: int = 2) -> str:
    """Generate a compact unified-style diff showing first differences.

    Returns at most 20 lines of diff output to keep reports readable.
    """
    expected_lines = expected.split("\n")
    actual_lines = actual.split("\n")

    diff_lines = []
    max_lines = 20

    # Find first difference
    for i in range(max(len(expected_lines), len(actual_lines))):
        exp = expected_lines[i] if i < len(expected_lines) else "<EOF>"
        act = actual_lines[i] if i < len(actual_lines) else "<EOF>"

        if exp != act:
            start = max(0, i - context)
            end = min(max(len(expected_lines), len(actual_lines)), i + context + 1)

            diff_lines.append(f"@@ line {i + 1} @@")
            for j in range(start, end):
                e = expected_lines[j] if j < len(expected_lines) else "<EOF>"
                a = actual_lines[j] if j < len(actual_lines) else "<EOF>"
                if e == a:
                    diff_lines.append(f"  {e}")
                else:
                    diff_lines.append(f"- {e}")
                    diff_lines.append(f"+ {a}")

                if len(diff_lines) >= max_lines:
                    diff_lines.append("... (truncated)")
                    return "\n".join(diff_lines)
            break

    if not diff_lines:
        diff_lines.append(f"(expected {len(expected_lines)} lines, got {len(actual_lines)} lines)")

    return "\n".join(diff_lines)


# ---------------------------------------------------------------------------
# Check 5: Cross-reference integrity
# ---------------------------------------------------------------------------


def check_crossref_integrity(
    canonical_skills: list, dist_dir: Path
) -> list:
    """Validate [skill:name] references are handled correctly per format.

    - Claude: preserved as-is ([skill:name])
    - Copilot: resolved to relative file links ([skill:name](../name/SKILL.md))
    - Codex: resolved to section anchors ([name](#name))

    Returns a list of failure dicts.
    """
    failures = []

    # Build set of valid skill names (dir_name used for cross-refs)
    valid_skills = {s["dir_name"] for s in canonical_skills}

    # --- Claude ---
    claude_skills_dir = dist_dir / "claude" / "skills"
    if claude_skills_dir.exists():
        for md_file in sorted(claude_skills_dir.rglob("SKILL.md")):
            content = read_file(md_file)
            rel_path = md_file.relative_to(dist_dir)
            refs = re.findall(r"\[skill:([a-zA-Z0-9_-]+)\]", content)
            for ref in refs:
                if ref not in valid_skills:
                    failures.append({
                        "file": str(rel_path),
                        "format": "claude",
                        "ref": ref,
                        "reason": f"unresolved [skill:{ref}] -- no matching skill directory",
                    })

    # --- Copilot ---
    copilot_skills_dir = dist_dir / "copilot" / "skills"
    if copilot_skills_dir.exists():
        for md_file in sorted(copilot_skills_dir.rglob("*.md")):
            content = read_file(md_file)
            rel_path = md_file.relative_to(dist_dir)

            # Check for un-transformed [skill:name] (should not exist)
            bare_refs = re.findall(r"\[skill:([a-zA-Z0-9_-]+)\](?!\()", content)
            for ref in bare_refs:
                failures.append({
                    "file": str(rel_path),
                    "format": "copilot",
                    "ref": ref,
                    "reason": f"un-transformed bare [skill:{ref}] -- should be relative link",
                })

            # Check resolved links point to existing files
            resolved = re.findall(
                r"\[skill:([a-zA-Z0-9_-]+)\]\(\.\./([a-zA-Z0-9_-]+)/SKILL\.md\)", content
            )
            for ref_name, link_target in resolved:
                target_path = copilot_skills_dir / link_target / "SKILL.md"
                if not target_path.exists():
                    failures.append({
                        "file": str(rel_path),
                        "format": "copilot",
                        "ref": ref_name,
                        "reason": f"broken link: ../{ link_target}/SKILL.md does not exist",
                    })

    # --- Codex ---
    codex_dir = dist_dir / "codex"
    if codex_dir.exists():
        for md_file in sorted(codex_dir.rglob("*.md")):
            content = read_file(md_file)
            rel_path = md_file.relative_to(dist_dir)

            # Check for un-transformed [skill:name] (should not exist)
            bare_refs = re.findall(r"\[skill:([a-zA-Z0-9_-]+)\]", content)
            for ref in bare_refs:
                failures.append({
                    "file": str(rel_path),
                    "format": "codex",
                    "ref": ref,
                    "reason": f"un-transformed bare [skill:{ref}] -- should be section anchor",
                })

            # Check anchor references point to valid section headings within
            # the same file or a related category file
            anchor_refs = re.findall(
                r"\[([a-zA-Z0-9_-]+)\]\(#([a-zA-Z0-9_-]+)\)", content
            )
            # Extract all ## headings in the file for local anchor resolution
            headings = set()
            for line in content.split("\n"):
                m = re.match(r"^##\s+(.+)", line)
                if m:
                    heading_text = m.group(1).strip().lower()
                    headings.add(heading_text)

            # Also build a global heading set from all codex files
            # (anchors may reference cross-file sections in routing index)
            global_headings = set()
            for codex_md in codex_dir.rglob("*.md"):
                codex_content = read_file(codex_md)
                for line in codex_content.split("\n"):
                    m = re.match(r"^##\s+(.+)", line)
                    if m:
                        global_headings.add(m.group(1).strip().lower())

            for display_name, anchor in anchor_refs:
                # Codex anchors are lowercased skill names
                if anchor.lower() not in headings and anchor.lower() not in global_headings:
                    failures.append({
                        "file": str(rel_path),
                        "format": "codex",
                        "ref": display_name,
                        "reason": f"broken anchor #{anchor} -- no matching ## heading found",
                    })

    return failures


# ---------------------------------------------------------------------------
# Corpus completeness
# ---------------------------------------------------------------------------


def check_corpus_completeness(
    corpus: list, canonical_skills: list
) -> list:
    """Verify every skill category has at least one corpus entry.

    Returns a list of failure dicts for uncovered categories.
    """
    failures = []

    # Get all categories from canonical skills
    all_categories = {s["category"] for s in canonical_skills}

    # Get categories covered by corpus
    corpus_categories = {e["category"] for e in corpus}

    for cat in sorted(all_categories):
        if cat not in corpus_categories:
            failures.append({
                "category": cat,
                "reason": f"category '{cat}' has no trigger corpus entry",
            })

    return failures


# ---------------------------------------------------------------------------
# Check 7: Manifest validation
# ---------------------------------------------------------------------------


def _compute_directory_sha256(directory: Path) -> str:
    """Compute a SHA256 checksum over the sorted file contents of a directory.

    Must match the algorithm in generate_dist.py exactly.
    """
    h = hashlib.sha256()
    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file():
            rel = file_path.relative_to(directory)
            h.update(str(rel).encode("utf-8"))
            h.update(file_path.read_bytes())
    return h.hexdigest()


def check_manifest_validation(dist_dir: Path) -> list:
    """Validate dist/manifest.json presence, JSON schema, and checksum correctness.

    Schema requirements:
      - version: non-empty string
      - generated_at: non-empty string in ISO 8601 format
      - targets: object with claude, copilot, codex keys
      - Each target: {path: string, sha256: string}
      - SHA256 checksums must match actual directory contents

    Returns a list of failure dicts.
    """
    failures = []

    manifest_path = dist_dir / "manifest.json"
    if not manifest_path.exists():
        failures.append({
            "field": "manifest.json",
            "reason": "manifest.json not found in dist/",
        })
        return failures

    # Parse JSON
    try:
        manifest_text = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as e:
        failures.append({
            "field": "manifest.json",
            "reason": f"invalid JSON: {e}",
        })
        return failures

    # Validate top-level fields
    if not isinstance(manifest, dict):
        failures.append({
            "field": "manifest.json",
            "reason": "root must be a JSON object",
        })
        return failures

    # version
    version = manifest.get("version")
    if not isinstance(version, str) or not version.strip():
        failures.append({
            "field": "version",
            "reason": "missing or empty 'version' field (expected non-empty string)",
        })

    # generated_at
    generated_at = manifest.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at.strip():
        failures.append({
            "field": "generated_at",
            "reason": "missing or empty 'generated_at' field (expected ISO 8601 string)",
        })
    elif not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", generated_at):
        failures.append({
            "field": "generated_at",
            "reason": f"'generated_at' not in expected ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ): {generated_at}",
        })

    # targets
    targets = manifest.get("targets")
    if not isinstance(targets, dict):
        failures.append({
            "field": "targets",
            "reason": "missing or invalid 'targets' field (expected object)",
        })
        return failures

    required_targets = ("claude", "copilot", "codex")
    for target_name in required_targets:
        target = targets.get(target_name)
        if not isinstance(target, dict):
            failures.append({
                "field": f"targets.{target_name}",
                "reason": f"missing or invalid target '{target_name}' (expected object)",
            })
            continue

        # Validate path field
        path_val = target.get("path")
        if not isinstance(path_val, str) or not path_val.strip():
            failures.append({
                "field": f"targets.{target_name}.path",
                "reason": f"missing or empty 'path' in target '{target_name}'",
            })

        # Validate sha256 field
        sha256_val = target.get("sha256")
        if not isinstance(sha256_val, str) or not sha256_val.strip():
            failures.append({
                "field": f"targets.{target_name}.sha256",
                "reason": f"missing or empty 'sha256' in target '{target_name}'",
            })
            continue

        # Validate checksum matches actual directory contents
        target_dir = dist_dir / target_name
        if target_dir.is_dir():
            actual_sha256 = _compute_directory_sha256(target_dir)
            if sha256_val != actual_sha256:
                failures.append({
                    "field": f"targets.{target_name}.sha256",
                    "reason": (
                        f"SHA256 mismatch for '{target_name}': "
                        f"manifest={sha256_val[:16]}... actual={actual_sha256[:16]}..."
                    ),
                })
        else:
            failures.append({
                "field": f"targets.{target_name}",
                "reason": f"target directory '{target_name}/' not found but listed in manifest",
            })

    return failures


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def print_check_report(
    check_name: str, check_num: int, failures: list
) -> bool:
    """Print per-check report. Returns True if passed."""
    status = "PASS" if not failures else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"Check {check_num}: {check_name} -- {status}")
    print(f"{'=' * 60}")

    if not failures:
        print("  All checks passed.")
        return True

    for f in failures:
        # Build a one-line summary
        parts = []
        for key in ["skill", "query", "file", "category", "field"]:
            if key in f:
                parts.append(f"{key}={f[key]}")
        if "format" in f:
            parts.append(f"format={f['format']}")
        if "pattern" in f:
            parts.append(f"pattern={f['pattern']}")

        context = ", ".join(parts)
        print(f"  FAIL: {context}")
        print(f"        {f['reason']}")

        if "diff" in f:
            for diff_line in f["diff"].split("\n")[:15]:
                print(f"        {diff_line}")

    print(f"\n  Total failures: {len(failures)}")
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Cross-agent conformance validator for dist/ outputs"
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root (default: auto-detect from script location)",
    )
    parser.add_argument(
        "--dist-dir",
        default=None,
        help="dist/ directory (default: <repo-root>/dist)",
    )
    args = parser.parse_args()

    # Determine paths
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        repo_root = _SCRIPTS_DIR.parent

    if args.dist_dir:
        dist_dir = Path(args.dist_dir).resolve()
    else:
        dist_dir = repo_root / "dist"

    # Validate dist/ exists
    if not dist_dir.is_dir():
        print(f"ERROR: dist/ directory not found at {dist_dir}", file=sys.stderr)
        print("Run 'python3 scripts/generate_dist.py' first.", file=sys.stderr)
        sys.exit(1)

    for subdir in ["claude", "copilot", "codex"]:
        if not (dist_dir / subdir).is_dir():
            print(f"ERROR: dist/{subdir}/ not found", file=sys.stderr)
            sys.exit(1)

    # Load canonical skills
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        print(f"ERROR: skills/ directory not found at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    canonical_skills = []
    for skill_file in sorted(skills_dir.rglob("SKILL.md")):
        category = skill_file.parent.parent.name
        dir_name = skill_file.parent.name
        try:
            parsed = parse_skill_file(skill_file)
            canonical_skills.append({
                "path": skill_file,
                "category": category,
                "dir_name": dir_name,
                "name": parsed["name"],
                "description": parsed["description"],
                "body": parsed["body"],
            })
        except ValueError as e:
            print(f"WARNING: failed to parse {skill_file}: {e}", file=sys.stderr)

    if not canonical_skills:
        print("ERROR: no canonical SKILL.md files found", file=sys.stderr)
        sys.exit(1)

    print(f"Canonical skills loaded: {len(canonical_skills)}")

    # Load trigger corpus
    corpus_path = repo_root / "tests" / "trigger-corpus.json"
    if not corpus_path.exists():
        print(f"ERROR: trigger corpus not found at {corpus_path}", file=sys.stderr)
        sys.exit(1)

    corpus = json.loads(read_file(corpus_path))
    print(f"Trigger corpus entries: {len(corpus)}")

    # Load agent names for graceful degradation check
    plugin_json = repo_root / ".claude-plugin" / "plugin.json"
    agent_names = load_agent_names(plugin_json)
    print(f"Agent names loaded: {len(agent_names)}")

    # Run all 5 checks + corpus completeness
    all_passed = True

    # Check 1: Routing parity
    failures_1 = check_routing_parity(canonical_skills, dist_dir)
    if not print_check_report("Routing parity", 1, failures_1):
        all_passed = False

    # Check 2: Trigger coverage
    failures_2 = check_trigger_coverage(corpus, canonical_skills, dist_dir)
    if not print_check_report("Trigger coverage", 2, failures_2):
        all_passed = False

    # Check 3: Graceful degradation
    failures_3 = check_graceful_degradation(agent_names, dist_dir)
    if not print_check_report("Graceful degradation", 3, failures_3):
        all_passed = False

    # Check 4: Structural comparison
    failures_4 = check_structural_comparison(canonical_skills, agent_names, dist_dir)
    if not print_check_report("Structural comparison", 4, failures_4):
        all_passed = False

    # Check 5: Cross-reference integrity
    failures_5 = check_crossref_integrity(canonical_skills, dist_dir)
    if not print_check_report("Cross-reference integrity", 5, failures_5):
        all_passed = False

    # Corpus completeness (bonus check)
    failures_cc = check_corpus_completeness(corpus, canonical_skills)
    if not print_check_report("Corpus completeness", 6, failures_cc):
        all_passed = False

    # Check 7: Manifest validation
    failures_7 = check_manifest_validation(dist_dir)
    if not print_check_report("Manifest validation", 7, failures_7):
        all_passed = False

    # Summary
    total_failures = (
        len(failures_1)
        + len(failures_2)
        + len(failures_3)
        + len(failures_4)
        + len(failures_5)
        + len(failures_cc)
        + len(failures_7)
    )

    print()
    print("=" * 60)
    print("=== Cross-Agent Conformance Summary ===")
    print("=" * 60)
    print(f"  Check 1 (Routing parity):       {'PASS' if not failures_1 else 'FAIL'} ({len(failures_1)} failures)")
    print(f"  Check 2 (Trigger coverage):      {'PASS' if not failures_2 else 'FAIL'} ({len(failures_2)} failures)")
    print(f"  Check 3 (Graceful degradation):  {'PASS' if not failures_3 else 'FAIL'} ({len(failures_3)} failures)")
    print(f"  Check 4 (Structural comparison): {'PASS' if not failures_4 else 'FAIL'} ({len(failures_4)} failures)")
    print(f"  Check 5 (Cross-ref integrity):   {'PASS' if not failures_5 else 'FAIL'} ({len(failures_5)} failures)")
    print(f"  Check 6 (Corpus completeness):   {'PASS' if not failures_cc else 'FAIL'} ({len(failures_cc)} failures)")
    print(f"  Check 7 (Manifest validation):   {'PASS' if not failures_7 else 'FAIL'} ({len(failures_7)} failures)")
    print()
    print(f"  Total failures: {total_failures}")
    print()

    if all_passed:
        print("PASSED: All cross-agent conformance checks passed.")
        sys.exit(0)
    else:
        print(f"FAILED: {total_failures} conformance failure(s) found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
