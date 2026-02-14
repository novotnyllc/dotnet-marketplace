# fn-25: Community Setup and README

## Overview
Create comprehensive community setup for the dotnet-artisan Claude Code plugin: README.md with skill catalog and architecture diagrams, CONTRIBUTING.md with skill authoring guide, CHANGELOG.md with initial release notes, and updated CLAUDE.md/AGENTS.md with plugin-specific instructions and agent delegation patterns.

**Deliverables (5 files):**
- `README.md` — Project overview, installation, skill catalog (97 skills across 18 categories), Mermaid architecture diagrams, cross-agent support, acknowledgements
- `CONTRIBUTING.md` — Skill authoring guide, PR process, validation requirements, directory conventions
- `CHANGELOG.md` — Initial v0.1.0 release notes in Keep a Changelog format
- `CLAUDE.md` — Plugin-specific instructions for Claude Code sessions (currently redirects to AGENTS.md; expand to standalone)
- `AGENTS.md` — Skill routing index and agent delegation patterns (currently only Flow-Next boilerplate; expand)

## Dependencies

**Hard epic dependencies:**
- fn-20 (Packaging & Publishing) — README references installation/publishing; CHANGELOG references packaging milestones
- fn-21 (Documentation Skills) — README references documentation tooling; fn-21's `dotnet-github-docs` teaches the patterns fn-25 applies
- fn-24 (Cross-Agent Build Pipeline) — README documents cross-agent support (Claude/Copilot/Codex); CONTRIBUTING references build pipeline validation

All dependencies are satisfied (fn-20, fn-21, fn-24 all complete).

## Conventions

- **Agent Skills open standard**: The plugin follows the Agent Skills open standard for skill authoring. All public-facing docs (README, CONTRIBUTING) must reference this standard and link to its specification.
- **Skill catalog format**: Category-level summary table with skill counts and representative examples (not full 97-skill enumeration — that's too long for a README)
- **Mermaid diagrams**: Minimum 2 diagrams — (1) plugin architecture overview, (2) agent delegation flow
- **CHANGELOG format**: Keep a Changelog (https://keepachangelog.com/) with SemVer
- **CLAUDE.md pattern**: Standalone content (not just `@AGENTS.md` redirect) with plugin-specific instructions
- **AGENTS.md pattern**: Preserve existing Flow-Next section; add skill routing index and agent delegation patterns above it
- **Version consistency**: CHANGELOG v0.1.0 must match `plugin.json` and `marketplace.json` version

## Task Decomposition

### fn-25.1: Create README.md with skill catalog and Mermaid diagrams — parallelizable with fn-25.2
**Delivers:** `README.md`
- Required sections: project name/tagline, CI status badge, installation, skill catalog table, Mermaid architecture diagrams, cross-agent support, usage examples, acknowledgements, license
- Skill catalog: table by category with count and representative skills (18 categories, 97 total skills)
- Mermaid diagrams: (1) plugin structure (skills → categories → agents), (2) agent delegation (user query → dotnet-advisor → specialist agent → skill)
- Cross-agent section: Claude/Copilot/Codex via fn-24's dist/ pipeline
- References Agent Skills open standard
- Data sources: `plugin.json` (skill list), `marketplace.json` (metadata), `skills/` directory layout
- Does NOT modify `CLAUDE.md`, `AGENTS.md`, `plugin.json`

### fn-25.2: Create CONTRIBUTING.md and CHANGELOG.md — parallelizable with fn-25.1
**Delivers:** `CONTRIBUTING.md`, `CHANGELOG.md`
- **CONTRIBUTING.md**: skill authoring guide (SKILL.md frontmatter: `name`, `description`; cross-reference syntax `[skill:name]`; description budget <120 chars; directory convention `skills/<category>/<skill-name>/SKILL.md`), PR process (fork → branch → validate → submit), validation requirements (`validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py --strict`, `validate_cross_agent.py`), development prerequisites (Python 3, jq), reference to Agent Skills open standard
- **CHANGELOG.md**: Keep a Changelog format, initial v0.1.0 (matching plugin.json version), sections covering all major milestones shipped (fn-2 through fn-24)
- Does NOT modify `README.md`, `CLAUDE.md`, `AGENTS.md`, `plugin.json`

### fn-25.3: Update CLAUDE.md and AGENTS.md with plugin instructions (depends on fn-25.1, fn-25.2)
**Delivers:** Updated `CLAUDE.md`, updated `AGENTS.md`
- **CLAUDE.md**: Replace `@AGENTS.md` redirect with standalone plugin instructions: validation commands, development workflow, key conventions (frontmatter, cross-refs, budget), file structure overview, reference to AGENTS.md for skill routing
- **AGENTS.md**: Preserve existing Flow-Next section; add above it: skill routing index (condensed category → skill mapping), agent delegation patterns (which agent handles which domain), cross-references to README and CONTRIBUTING
- Must not conflict with `dotnet-advisor` skill's internal routing logic
- Does NOT modify `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `plugin.json`

**Execution order:** fn-25.1 and fn-25.2 are parallelizable (file-disjoint). fn-25.3 depends on both (needs to reference README structure and CONTRIBUTING conventions for consistency).

## Acceptance Checks
- [ ] `README.md` exists with sections: installation, skill catalog table, Mermaid architecture diagrams (≥2), cross-agent support, acknowledgements, license
- [ ] `README.md` skill catalog shows 18 categories / 97 skills with per-category counts
- [ ] `README.md` references the Agent Skills open standard
- [ ] `CONTRIBUTING.md` exists with skill authoring guide, PR process, validation commands, directory conventions
- [ ] `CONTRIBUTING.md` references the Agent Skills open standard
- [ ] `CONTRIBUTING.md` lists all validation scripts: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py`, `validate_cross_agent.py`
- [ ] `CHANGELOG.md` exists in Keep a Changelog format with `## [0.1.0]` initial release (version matches plugin.json)
- [ ] `CLAUDE.md` contains standalone plugin instructions (not just `@AGENTS.md` redirect)
- [ ] `AGENTS.md` contains skill routing index and agent delegation patterns plus existing Flow-Next section
- [ ] Cross-references to documentation skills (fn-21) and build pipeline (fn-24) present in README
- [ ] fn-25.1 and fn-25.2 are file-disjoint and parallelizable
- [ ] fn-25.3 depends on fn-25.1 + fn-25.2

## Quick Commands
```bash
# Verify all community docs exist
for f in README.md CONTRIBUTING.md CHANGELOG.md; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done

# Verify README has required sections
for section in "Installation" "Skill Catalog" "Architecture" "Cross-Agent" "Acknowledgements" "License"; do
  grep -qi "$section" README.md && echo "OK: $section" || echo "MISSING: $section in README"
done

# Verify Mermaid diagrams in README
count=$(grep -c '```mermaid' README.md 2>/dev/null || echo 0)
[[ "$count" -ge 2 ]] && echo "OK: $count mermaid diagrams" || echo "MISSING: need ≥2 mermaid diagrams, found $count"

# Verify Agent Skills open standard referenced
grep -qi "Agent Skills" README.md && echo "OK: README refs standard" || echo "MISSING: standard ref in README"
grep -qi "Agent Skills" CONTRIBUTING.md && echo "OK: CONTRIBUTING refs standard" || echo "MISSING: standard ref in CONTRIBUTING"

# Verify CHANGELOG format and version
grep -q "Keep a Changelog" CHANGELOG.md && echo "OK: changelog format" || echo "MISSING: format reference"
grep -q "\[0.1.0\]" CHANGELOG.md && echo "OK: version 0.1.0" || echo "MISSING: version 0.1.0"

# Verify CONTRIBUTING validation commands
for cmd in "validate-skills" "validate-marketplace" "generate_dist" "validate_cross_agent"; do
  grep -q "$cmd" CONTRIBUTING.md && echo "OK: $cmd" || echo "MISSING: $cmd in CONTRIBUTING"
done

# Verify CLAUDE.md is not just a redirect
lines=$(wc -l < CLAUDE.md)
[[ "$lines" -gt 5 ]] && echo "OK: CLAUDE.md has content ($lines lines)" || echo "WARN: CLAUDE.md too short ($lines lines)"

# Verify AGENTS.md has skill routing
grep -qi "skill" AGENTS.md && echo "OK: AGENTS.md has skill content" || echo "MISSING: skill routing in AGENTS.md"
grep -qi "flow-next" AGENTS.md && echo "OK: Flow-Next preserved" || echo "MISSING: Flow-Next section"
```

## Key Context
- Plugin has 97 skills across 18 categories and 9 specialist agents
- `marketplace.json` author: Claire Novotny LLC, repo: novotnyllc/dotnet-marketplace, license: MIT
- `dotnet-advisor` is the central routing agent; AGENTS.md skill index should complement (not duplicate) its internal catalog
- fn-21's `dotnet-github-docs` skill teaches README/CONTRIBUTING patterns — fn-25 applies them to this specific repo
- fn-24's cross-agent pipeline generates dist/claude, dist/copilot, dist/codex from canonical SKILL.md sources
- No CI enforcement of community doc presence currently (future improvement, not fn-25 scope)
- Acknowledgements should credit: Claude Code plugin system / Agent Skills standard, .NET community, contributors

## References
- Keep a Changelog: https://keepachangelog.com/
- Agent Skills open standard: (link to specification when available)
- Claude Code plugin documentation: https://docs.anthropic.com/en/docs/claude-code/plugins
