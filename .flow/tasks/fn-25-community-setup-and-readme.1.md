# fn-25-community-setup-and-readme.1 Create README.md with skill catalog and Mermaid diagrams

## Description
Create `README.md` at the repo root for the dotnet-artisan Claude Code plugin. The README is the primary public-facing document and must be comprehensive but approachable.

**Required sections (in order):**
1. **Project name and tagline** — "dotnet-artisan" with description from `marketplace.json`
2. **Badges** — CI status (GitHub Actions `validate.yml`), license (MIT), version (0.1.0)
3. **Overview** — What the plugin provides: 97 skills across 18 categories, 9 specialist agents, hooks, MCP integration
4. **Installation** — `claude plugin add` command (or equivalent installation method from Claude Code plugin docs)
5. **Skill Catalog** — Table grouped by category (18 rows), columns: Category | Skills | Count | Example skills (2-3 per category). Do NOT enumerate all 97 skills individually. Data source: `plugin.json` skills array and `skills/` directory structure.
6. **Agents** — Table of 9 agents with name and one-line description. Data source: `plugin.json` agents array and agent file frontmatter.
7. **Architecture** — Mermaid diagrams:
   - Diagram 1: Plugin structure overview — shows skill categories as groups, agents as nodes, routing from dotnet-advisor to specialists
   - Diagram 2: Agent delegation flow — user query → dotnet-advisor routing → specialist agent → skill loading → response
8. **Cross-Agent Support** — Explain fn-24's dist/ pipeline: canonical SKILL.md → generated outputs for Claude Code, GitHub Copilot, OpenAI Codex. Reference transformation rules (cross-refs, agent omission, hook rewriting).
9. **Usage Examples** — 2-3 concrete examples of asking Claude Code questions that trigger skills
10. **Contributing** — Brief section pointing to CONTRIBUTING.md
11. **Acknowledgements** — Credits: Claude Code plugin system / Agent Skills open standard, .NET community and ecosystem, contributors
12. **License** — MIT with link to LICENSE file (if exists) or inline

**References the Agent Skills open standard** with explanation and link.

**Files created:** `README.md`
**Files NOT modified:** `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `plugin.json`

## Acceptance
- [ ] `README.md` exists at repo root
- [ ] Contains all 12 required sections listed above
- [ ] Skill catalog table has 18 category rows with accurate counts totaling 97
- [ ] Contains ≥2 Mermaid diagrams (architecture + delegation flow)
- [ ] Cross-agent support section references fn-24 dist/ pipeline
- [ ] References Agent Skills open standard
- [ ] Acknowledgements section credits Claude Code plugin system, .NET community, contributors
- [ ] Badges include CI status, license, version
- [ ] Quick commands pass:
  ```bash
  for section in "Installation" "Skill Catalog" "Architecture" "Cross-Agent" "Acknowledgements" "License"; do
    grep -qi "$section" README.md
  done
  grep -c '```mermaid' README.md  # ≥2
  grep -qi "Agent Skills" README.md
  ```

## Done summary
Created README.md with all 12 required sections including skill catalog table (18 categories, 97 skills with accurate per-category counts), 2 Mermaid architecture diagrams (plugin structure overview and agent delegation flow), cross-agent support documentation referencing the dist/ pipeline, Agent Skills open standard references, and CI/license/version badges.
## Evidence
- Commits: bc773b996745b8b65b9513c0c6affbaaf2df0e25
- Tests: grep section checks, mermaid diagram count, Agent Skills reference check
- PRs: