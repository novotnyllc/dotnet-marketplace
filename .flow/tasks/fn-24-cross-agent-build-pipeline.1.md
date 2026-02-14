# fn-24.1 Create dist/ generator script for Claude, Copilot, and Codex outputs

## Description
Create `scripts/generate_dist.py` — a Python script that reads the canonical `skills/`, `agents/`, `hooks/`, and `.mcp.json` sources and produces three output directories under `dist/`:

- `dist/claude/` — mirror of the plugin structure (plugin.json, marketplace.json, skills/, agents/, hooks/, .mcp.json)
- `dist/copilot/` — `.github/copilot-instructions.md` (routing index) + `skills/<name>.md` per skill with Copilot conventions
- `dist/codex/` — top-level `AGENTS.md` (routing index by category) + `skills/<category>/AGENTS.md` per category

The generator applies transformation rules defined in the epic spec:
- `[skill:name]` → preserved (Claude), relative link (Copilot), section anchor (Codex)
- Agent/hook/MCP references → preserved (Claude), omitted or rewritten (Copilot/Codex) per transformation table
- SKILL.md frontmatter (`name`, `description`) → preserved (Claude), heading+paragraph (Copilot/Codex)

The script reuses the existing frontmatter parser from `_validate_skills.py` where possible.

Version stamping: reads version from `git describe --tags` and stamps `plugin.json`/`marketplace.json` version fields during generation.

## Files touched
- `scripts/generate_dist.py` (new)
- `.gitignore` (add `dist/`)

## Acceptance
- [ ] `python3 scripts/generate_dist.py` produces `dist/claude/`, `dist/copilot/`, `dist/codex/` from canonical sources
- [ ] Claude output mirrors plugin structure faithfully
- [ ] Copilot output has `copilot-instructions.md` routing index and per-skill files
- [ ] Codex output has top-level `AGENTS.md` and per-category `AGENTS.md` files
- [ ] Transformation rules applied: agent/hook/MCP refs omitted from non-Claude outputs
- [ ] `[skill:name]` cross-refs converted per format (relative link for Copilot, anchor for Codex)
- [ ] `dist/` added to `.gitignore`
- [ ] Version stamped from git tags
- [ ] Script runs without .NET SDK dependency (pure Python + bash)

## Done summary
Created scripts/generate_dist.py that reads canonical skills/, agents/, hooks/, and .mcp.json sources and produces dist/claude/ (mirror), dist/copilot/ (routing index + per-skill files with relative cross-ref links), and dist/codex/ (top-level AGENTS.md + per-category AGENTS.md with section anchors). Applies transformation rules to omit Claude-only features (agents, hooks, MCP tools) from non-Claude outputs, stamps version from git tags, and supports --strict mode for CI. Added dist/ to .gitignore.
## Evidence
- Commits: 86c690d1f4e62f1d9e7a2a17adedfe3e30e23321, f4fe385acfc6a9e468f0b932e28b3452cf900eb3
- Tests: bash scripts/validate-skills.sh, bash scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict
- PRs: