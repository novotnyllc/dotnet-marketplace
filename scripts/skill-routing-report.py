#!/usr/bin/env python3
"""
Generate a per-skill routing compliance report for dotnet-artisan.

Reads all SKILL.md files and agent files, outputs a JSON report with per-skill
compliance metrics including: description quality, scope/out-of-scope presence,
cross-reference health, and cross-reference cycle involvement.

Usage:
    python3 scripts/skill-routing-report.py --repo-root .
    python3 scripts/skill-routing-report.py --repo-root . --output report.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Import shared agent frontmatter parser
sys.path.insert(0, str(Path(__file__).parent))
from _agent_frontmatter import parse_agent_frontmatter


# Reuse the SKILL.md frontmatter parser from _validate_skills.py
def parse_frontmatter(text: str) -> dict:
    """Parse SKILL.md frontmatter (strict subset: flat key:value only)."""
    result = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*)\s*:\s*(.*)", stripped)
        if not m:
            i += 1
            continue
        key = m.group(1)
        raw_value = m.group(2).strip()
        # Skip flow constructs and sequences
        if raw_value.startswith("[") or raw_value.startswith("{") or raw_value.startswith("- "):
            i += 1
            continue
        # Block scalars
        if raw_value in ("|", ">", "|+", "|-", ">+", ">-"):
            block_lines = []
            i += 1
            while i < len(lines):
                if lines[i].strip() == "" or (len(lines[i]) > 0 and lines[i][0] in (" ", "\t")):
                    block_lines.append(lines[i])
                    i += 1
                else:
                    break
            if block_lines:
                indent = len(block_lines[0]) - len(block_lines[0].lstrip())
                value = "\n".join(bl[indent:] if len(bl) > indent else "" for bl in block_lines)
            else:
                value = ""
            if raw_value.startswith(">"):
                value = re.sub(r"(?<!\n)\n(?!\n)", " ", value)
            result[key] = value.strip()
            continue
        # Quoted strings
        if raw_value.startswith('"') and raw_value.endswith('"') and len(raw_value) > 1:
            result[key] = raw_value[1:-1]
            i += 1
            continue
        if raw_value.startswith("'") and raw_value.endswith("'") and len(raw_value) > 1:
            result[key] = raw_value[1:-1]
            i += 1
            continue
        # Booleans
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


def extract_refs(text: str) -> list:
    """Extract unique [skill:name] references."""
    return list(dict.fromkeys(re.findall(r"\[skill:([a-zA-Z0-9_-]+)\]", text)))


def detect_cycles(ref_graph: dict) -> list:
    """Detect cycles in the cross-reference graph."""
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
                continue
            if neighbor in rec_set:
                idx = rec_stack.index(neighbor)
                cycle_nodes = rec_stack[idx:]
                min_val = min(cycle_nodes)
                min_idx = cycle_nodes.index(min_val)
                rotated = cycle_nodes[min_idx:] + cycle_nodes[:min_idx]
                cycle_key = tuple(rotated)
                if cycle_key not in seen_cycles:
                    seen_cycles.add(cycle_key)
                    cycles.append(list(rotated))
            elif neighbor not in visited:
                dfs(neighbor)
        rec_stack.pop()
        rec_set.remove(node)

    for node in sorted(ref_graph.keys()):
        if node not in visited:
            dfs(node)
    return cycles


def main():
    parser = argparse.ArgumentParser(description="Skill routing compliance report")
    parser.add_argument("--repo-root", required=True, help="Repository root")
    parser.add_argument("--output", default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    skills_dir = repo_root / "skills"
    agents_dir = repo_root / "agents"

    if not skills_dir.is_dir():
        print(f"ERROR: No skills/ directory at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    skill_files = sorted(skills_dir.rglob("SKILL.md"))
    agent_files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []

    # Build known IDs
    skill_dirs = {f.parent.name for f in skill_files}
    agent_stems = {f.stem for f in agent_files}
    known_ids = skill_dirs | agent_stems

    ref_graph = {}
    skill_reports = []

    # Process skills
    for sf in skill_files:
        rel = str(sf.relative_to(repo_root))
        try:
            content = sf.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        except Exception:
            skill_reports.append({"path": rel, "error": "cannot read"})
            continue

        lines = content.split("\n")
        if not lines or lines[0].strip() != "---":
            skill_reports.append({"path": rel, "error": "missing frontmatter"})
            continue

        fm_lines = []
        body_start = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                body_start = i + 1
                break
            fm_lines.append(line)

        if body_start is None:
            skill_reports.append({"path": rel, "error": "unclosed frontmatter"})
            continue

        try:
            parsed = parse_frontmatter("\n".join(fm_lines))
        except Exception:
            skill_reports.append({"path": rel, "error": "invalid frontmatter"})
            continue

        name = parsed.get("name", "")
        if isinstance(name, str):
            name = name.strip()
        else:
            name = ""
        desc = parsed.get("description", "")
        if isinstance(desc, str):
            desc = desc.strip()
        else:
            desc = ""

        body_text = "\n".join(lines[body_start:])
        refs = extract_refs(body_text)
        has_scope = bool(re.search(r"^## Scope\s*$", body_text, re.MULTILINE))
        has_oos = bool(re.search(r"^## Out of scope\s*$", body_text, re.MULTILINE))
        self_ref = name in refs
        unresolved_refs = [r for r in refs if r not in known_ids and r != name]

        if name:
            ref_graph[name] = [r for r in refs if r != name]

        report = {
            "path": rel,
            "type": "skill",
            "name": name,
            "description_length": len(desc),
            "has_scope": has_scope,
            "has_out_of_scope": has_oos,
            "self_reference": self_ref,
            "cross_references": refs,
            "unresolved_references": unresolved_refs,
            "when_prefix": desc.startswith("WHEN "),
        }
        skill_reports.append(report)

    # Process agents
    agent_reports = []
    for af in agent_files:
        rel = str(af.relative_to(repo_root))
        fm = parse_agent_frontmatter(str(af))
        try:
            content = af.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        except Exception:
            agent_reports.append({"path": rel, "error": "cannot read"})
            continue

        refs = extract_refs(content)
        unresolved = [r for r in refs if r not in known_ids]
        stem = af.stem
        if stem:
            ref_graph[stem] = [r for r in refs if r != stem]

        agent_reports.append({
            "path": rel,
            "type": "agent",
            "name": fm.get("name") or stem,
            "description": fm.get("description"),
            "cross_references": refs,
            "unresolved_references": unresolved,
        })

    # Cycle detection
    cycles = detect_cycles(ref_graph)
    cycle_report = []
    for cycle in cycles:
        cycle_report.append({
            "cycle": cycle,
            "length": len(cycle),
        })

    # Build nodes-in-cycles set
    nodes_in_cycles = set()
    for cycle in cycles:
        nodes_in_cycles.update(cycle)

    # Add cycle involvement to skill reports
    for report in skill_reports:
        name = report.get("name", "")
        report["in_cycle"] = name in nodes_in_cycles

    for report in agent_reports:
        name = report.get("name", "")
        report["in_cycle"] = name in nodes_in_cycles

    # Summary
    total_skills = len([r for r in skill_reports if "error" not in r])
    skills_with_scope = sum(1 for r in skill_reports if r.get("has_scope", False))
    skills_with_oos = sum(1 for r in skill_reports if r.get("has_out_of_scope", False))
    skills_with_self_ref = sum(1 for r in skill_reports if r.get("self_reference", False))
    skills_with_when = sum(1 for r in skill_reports if r.get("when_prefix", False))

    output = {
        "summary": {
            "total_skills": total_skills,
            "total_agents": len(agent_reports),
            "known_ids": len(known_ids),
            "skills_with_scope": skills_with_scope,
            "skills_with_out_of_scope": skills_with_oos,
            "skills_with_self_ref": skills_with_self_ref,
            "skills_with_when_prefix": skills_with_when,
            "cross_reference_cycles": len(cycles),
            "nodes_in_cycles": len(nodes_in_cycles),
        },
        "skills": skill_reports,
        "agents": agent_reports,
        "cycles": cycle_report,
    }

    json_output = json.dumps(output, indent=2, sort_keys=False)

    if args.output:
        Path(args.output).write_text(json_output + "\n", encoding="utf-8")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(json_output)


if __name__ == "__main__":
    main()
