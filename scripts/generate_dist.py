#!/usr/bin/env python3
"""
Generate dist/ output directories for Claude Code, GitHub Copilot, and OpenAI Codex.

Reads canonical skills/, agents/, hooks/, and .mcp.json sources and produces:
  - dist/claude/   -- mirror of the plugin structure
  - dist/copilot/  -- .github/copilot-instructions.md + per-skill files
  - dist/codex/    -- top-level AGENTS.md + per-category AGENTS.md files

Reuses the frontmatter parser from _validate_skills.py.

Usage:
    python3 scripts/generate_dist.py [--repo-root <path>] [--strict]

Runs without .NET SDK dependency (pure Python).
"""

import argparse
import json
import re
import shutil
import subprocess
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


def get_version_from_git() -> str:
    """Return a version string from git describe --tags, falling back to 0.0.0-dev."""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            version = result.stdout.strip()
            # Strip leading 'v' if present (e.g. v0.1.0 -> 0.1.0)
            if version.startswith("v"):
                version = version[1:]
            return version
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "0.0.0-dev"


def load_agent_names(plugin_json_path: Path) -> list:
    """Read agent names from plugin.json agents array (canonical source of truth)."""
    try:
        data = json.loads(plugin_json_path.read_text(encoding="utf-8"))
        return [Path(a).stem for a in data.get("agents", [])]
    except (json.JSONDecodeError, FileNotFoundError):
        return []


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
        "raw": content,
        "name": parsed.get("name", ""),
        "description": parsed.get("description", ""),
    }


def collect_skills(skills_dir: Path) -> tuple:
    """Collect all SKILL.md files grouped by category (parent dir name).

    Returns (skills_list, skipped_count) so callers can enforce strict mode.
    """
    results = []
    skipped = 0
    for skill_file in sorted(skills_dir.rglob("SKILL.md")):
        category = skill_file.parent.parent.name  # e.g. core-csharp
        skill_name = skill_file.parent.name  # e.g. dotnet-csharp-dependency-injection
        try:
            parsed = parse_skill_file(skill_file)
            results.append(
                {
                    "path": skill_file,
                    "category": category,
                    "dir_name": skill_name,
                    "name": parsed["name"],
                    "description": parsed["description"],
                    "body": parsed["body"],
                    "raw": parsed["raw"],
                }
            )
        except ValueError as e:
            print(f"ERROR: failed to parse {skill_file}: {e}", file=sys.stderr)
            skipped += 1
    return results, skipped


# ---------------------------------------------------------------------------
# Transformation rules
# ---------------------------------------------------------------------------


def build_claude_only_patterns(agent_names: list) -> list:
    """Build regex patterns for Claude-only line detection.

    Agent names are read from plugin.json at runtime (not hardcoded) to stay
    in sync with the canonical source of truth.

    NOTE: For v1, hook and MCP references are omitted entirely from non-Claude
    outputs. The fn-24 spec also describes rewrite rules (e.g., hook sentences
    to manual detection guidance, MCP refs to direct URLs) which are deferred
    to a future iteration. Current behavior matches the spec's "or omitted if
    no manual equivalent" fallback for all cases.
    TODO: Implement selective rewrite rules for Copilot hook/MCP references.
    """
    patterns = []

    if agent_names:
        # Agent references -- match agent names at word boundaries. We use
        # the canonical agent file stems from plugin.json. These names are
        # kebab-cased identifiers (e.g. dotnet-architect) that don't appear
        # as substrings of skill names, so word-boundary matching is safe.
        patterns.append(
            re.compile(
                r"\b(?:" + "|".join(re.escape(a) for a in agent_names) + r")\s+agent\b",
                re.IGNORECASE,
            )
        )

    # Hook references
    patterns.append(
        re.compile(r"(?:SessionStart hook|PostToolUse hook|hook detect)", re.IGNORECASE)
    )

    # MCP tool references (mcp__server__tool or mcp__prefix__ patterns)
    patterns.append(re.compile(r"mcp__\w+__"))

    # ${CLAUDE_PLUGIN_ROOT} path references
    patterns.append(re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}"))

    return patterns


def remove_claude_only_lines(text: str, patterns: list) -> str:
    """Remove lines that reference Claude-only features (agents, hooks, MCP, plugin root).

    Also cleans up orphaned markdown table structures left after line removal
    (e.g., header + separator rows with no data rows).
    """
    lines = text.split("\n")
    filtered = []
    for line in lines:
        if any(p.search(line) for p in patterns):
            continue
        filtered.append(line)

    result = "\n".join(filtered)

    # Clean up orphaned markdown tables: header + separator with no data rows.
    # Pattern: a table header line, separator line, then a blank line (no data rows).
    result = re.sub(
        r"(?m)^\|[^\n]+\|\n\|[-| :]+\|\n(?=\n|$)",
        "",
        result,
    )

    # Collapse runs of 3+ newlines to 2
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result


def transform_crossrefs_copilot(text: str) -> str:
    """Convert [skill:name] to relative links for Copilot format."""
    return re.sub(
        r"\[skill:([a-zA-Z0-9_-]+)\]",
        r"[skill:\1](../\1/SKILL.md)",
        text,
    )


def transform_crossrefs_codex(text: str) -> str:
    """Convert [skill:name] to section anchors for Codex format.

    Anchors are lowercased to match GitHub/standard markdown heading anchor
    generation (headings are lowercased, spaces replaced with hyphens).
    """
    return re.sub(
        r"\[skill:([a-zA-Z0-9_-]+)\]",
        lambda m: f"[{m.group(1)}](#{m.group(1).lower()})",
        text,
    )


def frontmatter_to_heading(name: str, description: str) -> str:
    """Convert frontmatter fields to a heading + description paragraph."""
    lines = [f"# {name}", ""]
    if description:
        lines.append(description)
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Claude output (mirror)
# ---------------------------------------------------------------------------


def generate_claude(repo_root: Path, dist_claude: Path, version: str):
    """Generate dist/claude/ -- mirror of the plugin structure.

    Raises on copy failures so the caller can clean up partial output.
    """
    plugin_dir = repo_root / ".claude-plugin"

    # Copy plugin.json with version stamping
    plugin_json_path = plugin_dir / "plugin.json"
    if plugin_json_path.exists():
        plugin_data = json.loads(read_file(plugin_json_path))
        plugin_data["version"] = version
        dist_plugin = dist_claude / "plugin.json"
        dist_plugin.write_text(
            json.dumps(plugin_data, indent=2) + "\n", encoding="utf-8"
        )

    # Copy marketplace.json with version stamping
    marketplace_json_path = plugin_dir / "marketplace.json"
    if marketplace_json_path.exists():
        marketplace_data = json.loads(read_file(marketplace_json_path))
        marketplace_data["version"] = version
        dist_marketplace = dist_claude / "marketplace.json"
        dist_marketplace.write_text(
            json.dumps(marketplace_data, indent=2) + "\n", encoding="utf-8"
        )

    # Copy skills/
    skills_src = repo_root / "skills"
    if skills_src.is_dir():
        shutil.copytree(skills_src, dist_claude / "skills", dirs_exist_ok=True)

    # Copy agents/
    agents_src = repo_root / "agents"
    if agents_src.is_dir():
        shutil.copytree(agents_src, dist_claude / "agents", dirs_exist_ok=True)

    # Copy hooks/ (hooks.json metadata)
    hooks_src = repo_root / "hooks"
    if hooks_src.is_dir():
        shutil.copytree(hooks_src, dist_claude / "hooks", dirs_exist_ok=True)

    # Copy hook scripts from scripts/hooks/ -- these are referenced by
    # hooks.json via relative paths (e.g. ${CLAUDE_PLUGIN_ROOT}/scripts/hooks/...)
    # so we preserve the directory structure to keep path resolution intact.
    hooks_scripts_src = repo_root / "scripts" / "hooks"
    if hooks_scripts_src.is_dir():
        dest_scripts_hooks = dist_claude / "scripts" / "hooks"
        shutil.copytree(hooks_scripts_src, dest_scripts_hooks, dirs_exist_ok=True)

    # Copy .mcp.json
    mcp_src = repo_root / ".mcp.json"
    if mcp_src.exists():
        shutil.copy2(mcp_src, dist_claude / ".mcp.json")


# ---------------------------------------------------------------------------
# Copilot output
# ---------------------------------------------------------------------------


def generate_copilot(skills: list, claude_only_patterns: list, dist_copilot: Path):
    """Generate dist/copilot/ -- routing index + per-skill files."""
    github_dir = dist_copilot / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)

    skills_dir = dist_copilot / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Build routing index
    index_lines = [
        "# dotnet-artisan -- Copilot Instructions",
        "",
        "Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications.",
        "",
        "## Skill Index",
        "",
    ]

    # Group skills by category
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)

    for cat in sorted(categories.keys()):
        cat_skills = categories[cat]
        index_lines.append(f"### {cat}")
        index_lines.append("")
        for skill in sorted(cat_skills, key=lambda s: s["name"]):
            name = skill["name"]
            dir_name = skill["dir_name"]
            desc = skill["description"]
            # Link to per-skill file using dir_name for path consistency
            index_lines.append(
                f"- [{name}](../skills/{dir_name}/SKILL.md) -- {desc}"
            )
        index_lines.append("")

    # Write routing index with trailing newline
    (github_dir / "copilot-instructions.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )

    # Write per-skill files
    for skill in skills:
        # Use dir_name for output path to match file-system convention
        skill_out_dir = skills_dir / skill["dir_name"]
        skill_out_dir.mkdir(parents=True, exist_ok=True)

        # Transform body: remove Claude-only refs, convert cross-refs
        body = skill["body"].lstrip("\n")
        body = remove_claude_only_lines(body, claude_only_patterns)
        body = transform_crossrefs_copilot(body)

        # Build output: heading + description + body
        output = frontmatter_to_heading(skill["name"], skill["description"])
        output += body.rstrip("\n") + "\n"

        (skill_out_dir / "SKILL.md").write_text(output, encoding="utf-8")


# ---------------------------------------------------------------------------
# Codex output
# ---------------------------------------------------------------------------


def generate_codex(skills: list, claude_only_patterns: list, dist_codex: Path):
    """Generate dist/codex/ -- top-level AGENTS.md + per-category AGENTS.md."""
    skills_dir = dist_codex / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Group by category
    categories = {}
    for skill in skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(skill)

    # Build top-level AGENTS.md (routing index by category)
    top_lines = [
        "# dotnet-artisan",
        "",
        "Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications.",
        "",
        "## Categories",
        "",
    ]

    for cat in sorted(categories.keys()):
        cat_skills = categories[cat]
        top_lines.append(f"### {cat}")
        top_lines.append("")
        for skill in sorted(cat_skills, key=lambda s: s["name"]):
            name = skill["name"]
            desc = skill["description"]
            top_lines.append(
                f"- [{name}](skills/{cat}/AGENTS.md#{name.lower()}) -- {desc}"
            )
        top_lines.append("")

    # Write with trailing newline
    (dist_codex / "AGENTS.md").write_text(
        "\n".join(top_lines) + "\n", encoding="utf-8"
    )

    # Write per-category AGENTS.md
    for cat in sorted(categories.keys()):
        cat_dir = skills_dir / cat
        cat_dir.mkdir(parents=True, exist_ok=True)

        cat_lines = [f"# {cat}", ""]
        cat_skills = sorted(categories[cat], key=lambda s: s["name"])

        for skill in cat_skills:
            # Transform body: remove Claude-only refs, convert cross-refs
            body = skill["body"].lstrip("\n")
            body = remove_claude_only_lines(body, claude_only_patterns)
            body = transform_crossrefs_codex(body)

            # Use name as section anchor target
            cat_lines.append(f"## {skill['name']}")
            cat_lines.append("")
            if skill["description"]:
                cat_lines.append(skill["description"])
                cat_lines.append("")
            cat_lines.append(body.strip())
            cat_lines.append("")
            cat_lines.append("---")
            cat_lines.append("")

        # Write with trailing newline
        (cat_dir / "AGENTS.md").write_text(
            "\n".join(cat_lines) + "\n", encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate dist/ outputs for Claude, Copilot, and Codex"
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Repository root (default: auto-detect from script location)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: <repo-root>/dist)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any SKILL.md files cannot be parsed (default: warn and skip)",
    )
    args = parser.parse_args()

    # Determine repo root
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        repo_root = _SCRIPTS_DIR.parent

    # Determine output dir
    if args.output_dir:
        dist_root = Path(args.output_dir).resolve()
    else:
        dist_root = repo_root / "dist"

    # Validate source directories exist
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        print(f"ERROR: skills/ directory not found at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    plugin_dir = repo_root / ".claude-plugin"
    if not plugin_dir.is_dir():
        print(
            f"ERROR: .claude-plugin/ directory not found at {plugin_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Load agent names from plugin.json (canonical source of truth)
    plugin_json_path = plugin_dir / "plugin.json"
    agent_names = load_agent_names(plugin_json_path)
    if agent_names:
        print(f"Agent names loaded from plugin.json: {len(agent_names)}")

    # Build transformation patterns
    claude_only_patterns = build_claude_only_patterns(agent_names)

    # Get version
    version = get_version_from_git()
    print(f"Version: {version}")

    # Clean and recreate dist/
    if dist_root.exists():
        shutil.rmtree(dist_root)

    dist_claude = dist_root / "claude"
    dist_copilot = dist_root / "copilot"
    dist_codex = dist_root / "codex"

    dist_claude.mkdir(parents=True, exist_ok=True)
    dist_copilot.mkdir(parents=True, exist_ok=True)
    dist_codex.mkdir(parents=True, exist_ok=True)

    # Collect all skills
    skills, skipped = collect_skills(skills_dir)
    if not skills:
        print("ERROR: no SKILL.md files found", file=sys.stderr)
        sys.exit(1)

    if skipped > 0:
        if args.strict:
            print(
                f"ERROR: {skipped} SKILL.md file(s) failed to parse (--strict mode)",
                file=sys.stderr,
            )
            # Clean up partial output
            if dist_root.exists():
                shutil.rmtree(dist_root)
            sys.exit(1)
        else:
            print(
                f"WARNING: {skipped} SKILL.md file(s) skipped due to parse errors",
                file=sys.stderr,
            )

    print(f"Skills found: {len(skills)}")

    # Generate each format, cleaning up on failure
    try:
        print("Generating dist/claude/ ...")
        generate_claude(repo_root, dist_claude, version)

        print("Generating dist/copilot/ ...")
        generate_copilot(skills, claude_only_patterns, dist_copilot)

        print("Generating dist/codex/ ...")
        generate_codex(skills, claude_only_patterns, dist_codex)
    except Exception as e:
        print(f"ERROR: generation failed: {e}", file=sys.stderr)
        # Clean up partial output per spec: no partial dist/ on failure
        if dist_root.exists():
            shutil.rmtree(dist_root)
        sys.exit(1)

    # Summary
    claude_skills = len(list((dist_claude / "skills").rglob("SKILL.md")))
    copilot_skills = len(list((dist_copilot / "skills").rglob("SKILL.md")))
    codex_categories = len(list((dist_codex / "skills").rglob("AGENTS.md")))

    print()
    print("=== Generation Summary ===")
    print(f"  dist/claude/  : {claude_skills} skills (mirror)")
    print(f"  dist/copilot/ : {copilot_skills} skills + routing index")
    print(f"  dist/codex/   : {codex_categories} category AGENTS.md files + routing index")
    print(f"  Version: {version}")
    print()
    print("DONE")


if __name__ == "__main__":
    main()
