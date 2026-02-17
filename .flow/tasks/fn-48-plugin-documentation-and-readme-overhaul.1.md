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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
