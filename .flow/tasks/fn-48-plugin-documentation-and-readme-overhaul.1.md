# fn-48-plugin-documentation-and-readme-overhaul.1 Reconcile skill and agent counts across plugin.json, README, CLAUDE.md, AGENTS.md

## Description
Reconcile skill and agent counts across all documents, then rewrite README.md with installation instructions, skill category overview, and complete agent list. Review CONTRIBUTING.md and CONTRIBUTING-SKILLS.md for accuracy.

**Size:** M (merged from original two tasks — count reconciliation is inseparable from README rewrite)
**Files:** `.claude-plugin/plugin.json`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`, `scripts/validate-skills.sh`

## Approach

- Count entries in plugin.json `skills` and `agents` arrays (expected: 132 skills, 14 agents post-batch)
- Fix all documents to show accurate counts
- Rewrite README with: what the plugin does, installation instructions, 22-category skill overview, all 14 agents, quick start
- Review CONTRIBUTING.md and CONTRIBUTING-SKILLS.md for path accuracy
- Update `--projected-skills` in validate-skills.sh to 132
## Approach

- Count entries in plugin.json `skills` array and `agents` array
- Compare against README.md (line 12: "122 skills", "9 agents"), CLAUDE.md, AGENTS.md
- Fix all documents to show accurate counts
- Fix agent table in README to list all 14 agents
## Acceptance
- [ ] Skill count = 132 across plugin.json, README, CLAUDE.md, AGENTS.md
- [ ] Agent count = 14 across all documents with complete agent table
- [ ] README has installation instructions
- [ ] README has skill category overview covering all 22 categories
- [ ] CONTRIBUTING.md reviewed for accuracy
- [ ] CONTRIBUTING-SKILLS.md reviewed for accuracy
- [ ] `--projected-skills` set to 132 in validate-skills.sh
- [ ] All validation scripts pass
## Done summary
Reconciled skill and agent counts across all documentation files (README.md, CLAUDE.md, AGENTS.md, CONTRIBUTING.md, CONTRIBUTING-SKILLS.md) at both root and plugin levels. Updated total skill count from 122 to 127, fixed per-category counts in tables and Mermaid diagrams for Foundation (4->5), Core C# (15->16), Project Structure (6->7), CLI Tools (5->6), and UI Frameworks (13->14), and updated budget math in CONTRIBUTING-SKILLS.md. All validation scripts pass.
## Evidence
- Commits: decb291ed3da92e8d793983eb8f1919de2ed86cb
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: