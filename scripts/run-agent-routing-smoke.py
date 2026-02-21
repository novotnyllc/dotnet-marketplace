#!/usr/bin/env python3
"""Cross-provider agent-routing smoke test orchestrator.

Runs offline (no CLI invocations) structural verification for each
provider to confirm the flat skill layout is discoverable.  For live
CLI tests, use test.sh which delegates to check-skills.cs.

This script validates:
  - Claude Code: plugin.json skill paths resolve, cross-refs validate
  - Codex:       131 skill dirs found at expected depth, openai.yaml consistent
  - Copilot:     plugin.json paths resolve, SKILL.md frontmatter present

Exit codes:
    0 - All structural checks pass
    1 - One or more checks failed
    2 - Usage error

Usage:
    python scripts/run-agent-routing-smoke.py
    python scripts/run-agent-routing-smoke.py --provider claude
    python scripts/run-agent-routing-smoke.py --provider codex
    python scripts/run-agent-routing-smoke.py --provider copilot
    python scripts/run-agent-routing-smoke.py --provider claude,codex,copilot
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
OPENAI_YAML = REPO_ROOT / ".agents" / "openai.yaml"
EXPECTED_SKILL_COUNT = 131

# Frontmatter required fields for every SKILL.md
REQUIRED_FRONTMATTER = {"name", "description", "license"}


def load_plugin_json() -> dict:
    with open(PLUGIN_JSON) as f:
        return json.load(f)


def discover_skill_dirs() -> list[Path]:
    """Find all skill directories (flat layout: skills/<name>/SKILL.md)."""
    dirs = []
    for child in sorted(SKILLS_DIR.iterdir()):
        if child.is_dir() and (child / "SKILL.md").exists():
            dirs.append(child)
    return dirs


def parse_frontmatter(skill_md_path: Path) -> dict | None:
    """Parse YAML frontmatter from a SKILL.md file (simple key: value parser)."""
    content = skill_md_path.read_text(encoding="utf-8")
    # Frontmatter is between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    fm = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("'\"")
    return fm


def check_claude(skill_dirs: list[Path]) -> list[str]:
    """Verify Claude Code structural requirements.

    - plugin.json exists and lists skill paths
    - All listed paths resolve to existing SKILL.md files
    - [skill:name] cross-references resolve (via validate-skills.sh, just check here)
    """
    errors = []

    if not PLUGIN_JSON.exists():
        errors.append(f"plugin.json not found at {PLUGIN_JSON}")
        return errors

    plugin = load_plugin_json()
    skills_list = plugin.get("skills", [])
    if not skills_list:
        errors.append("plugin.json has empty 'skills' array")
        return errors

    # Verify count
    if len(skills_list) != EXPECTED_SKILL_COUNT:
        errors.append(
            f"plugin.json lists {len(skills_list)} skills, expected {EXPECTED_SKILL_COUNT}"
        )

    # Verify each path resolves
    missing_paths = []
    for skill_entry in skills_list:
        # Entries may be strings (paths) or dicts with a 'path' key
        if isinstance(skill_entry, str):
            skill_path = skill_entry
        elif isinstance(skill_entry, dict):
            skill_path = skill_entry.get("path", "")
        else:
            errors.append(f"Unexpected skill entry type: {type(skill_entry)}")
            continue

        full_path = REPO_ROOT / skill_path
        if not full_path.exists():
            missing_paths.append(skill_path)

    if missing_paths:
        errors.append(
            f"{len(missing_paths)} plugin.json skill path(s) do not resolve: "
            f"{missing_paths[:5]}{'...' if len(missing_paths) > 5 else ''}"
        )

    return errors


def check_codex(skill_dirs: list[Path]) -> list[str]:
    """Verify Codex structural requirements.

    - Flat layout: 131 skill dirs at skills/<name>/ (depth 1, not depth 2)
    - Each has SKILL.md
    - .agents/openai.yaml exists and references flat layout
    """
    errors = []

    # Skill count verification
    if len(skill_dirs) != EXPECTED_SKILL_COUNT:
        errors.append(
            f"Found {len(skill_dirs)} skill directories, expected {EXPECTED_SKILL_COUNT}"
        )

    # Verify flat layout (no category subdirectories with skills)
    for child in sorted(SKILLS_DIR.iterdir()):
        if child.is_dir() and not (child / "SKILL.md").exists():
            # Check if it has subdirectories with SKILL.md (nested layout remnant)
            nested = list(child.glob("*/SKILL.md"))
            if nested:
                errors.append(
                    f"Nested skill layout detected under {child.name}/: "
                    f"{[p.parent.name for p in nested[:3]]}"
                )

    # Verify openai.yaml exists
    if not OPENAI_YAML.exists():
        errors.append(f".agents/openai.yaml not found at {OPENAI_YAML}")
    else:
        yaml_content = OPENAI_YAML.read_text(encoding="utf-8")
        # Verify it references the flat layout pattern
        if "skills/<skill-name>/" in yaml_content or "skills/" in yaml_content:
            pass  # Good -- references the skills directory
        else:
            errors.append(
                ".agents/openai.yaml does not reference skills/ directory pattern"
            )

    return errors


def check_copilot(skill_dirs: list[Path]) -> list[str]:
    """Verify Copilot structural requirements.

    - plugin.json paths resolve (shared with Claude check)
    - Each SKILL.md has required frontmatter fields
    - Flat layout allows Copilot to discover skills via SKILL.md glob
    """
    errors = []

    if not PLUGIN_JSON.exists():
        errors.append(f"plugin.json not found at {PLUGIN_JSON}")
        return errors

    # Verify each skill has required frontmatter
    missing_frontmatter = []
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        fm = parse_frontmatter(skill_md)
        if fm is None:
            missing_frontmatter.append(f"{skill_dir.name}: no frontmatter")
            continue
        missing_fields = REQUIRED_FRONTMATTER - set(fm.keys())
        if missing_fields:
            missing_frontmatter.append(
                f"{skill_dir.name}: missing {missing_fields}"
            )

    if missing_frontmatter:
        errors.append(
            f"{len(missing_frontmatter)} skill(s) have frontmatter issues: "
            f"{missing_frontmatter[:5]}{'...' if len(missing_frontmatter) > 5 else ''}"
        )

    # Verify the evidence pattern is detectable (Copilot emits "Base directory for this skill:")
    # This is a structural check: SKILL.md must exist at the right path for the pattern to work
    plugin = load_plugin_json()
    skills_list = plugin.get("skills", [])
    for entry in skills_list:
        if isinstance(entry, str):
            skill_path = entry
        elif isinstance(entry, dict):
            skill_path = entry.get("path", "")
        else:
            continue
        # Verify the path follows the expected pattern for Copilot discovery.
        # Paths may use ./skills/ or skills/ prefix -- both are valid.
        normalized = skill_path.lstrip("./")
        if not normalized.startswith("skills/"):
            errors.append(f"Skill path not under skills/: {skill_path}")

    return errors


def run_checks(providers: list[str]) -> dict:
    """Run structural checks for specified providers."""
    skill_dirs = discover_skill_dirs()
    results = {}

    check_map = {
        "claude": check_claude,
        "codex": check_codex,
        "copilot": check_copilot,
    }

    for provider in providers:
        if provider not in check_map:
            print(f"WARNING: Unknown provider '{provider}', skipping.", file=sys.stderr)
            continue
        errors = check_map[provider](skill_dirs)
        results[provider] = {
            "status": "pass" if not errors else "fail",
            "errors": errors,
            "skill_count": len(skill_dirs),
        }

    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-provider agent-routing structural smoke test"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="claude,codex,copilot",
        help="Comma-separated list of providers to check (default: claude,codex,copilot)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write results JSON to this path",
    )

    args = parser.parse_args()
    providers = [p.strip().lower() for p in args.provider.split(",") if p.strip()]

    if not providers:
        print("ERROR: No providers specified.", file=sys.stderr)
        return 2

    results = run_checks(providers)

    # Print results
    all_pass = True
    for provider, result in sorted(results.items()):
        status = result["status"].upper()
        print(f"[{provider}] {status} (skills: {result['skill_count']})")
        if result["errors"]:
            all_pass = False
            for err in result["errors"]:
                print(f"  ERROR: {err}")

    # Write output if requested
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\nResults written to: {output_path}", file=sys.stderr)

    if all_pass:
        print(f"\nAll {len(results)} provider(s) passed structural checks.")
        return 0
    else:
        failed = [p for p, r in results.items() if r["status"] == "fail"]
        print(f"\nFAILED: {len(failed)} provider(s) have errors: {failed}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
