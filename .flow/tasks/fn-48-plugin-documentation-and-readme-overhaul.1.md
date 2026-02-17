# fn-48-plugin-documentation-and-readme-overhaul.1 Reconcile skill and agent counts across plugin.json, README, CLAUDE.md, AGENTS.md

## Description
Audit the actual skill count in plugin.json vs what README.md, CLAUDE.md, and AGENTS.md report. Fix all discrepancies to reflect the true count.

**Size:** S
**Files:** `.claude-plugin/plugin.json`, `README.md`, `CLAUDE.md`, `AGENTS.md`

## Approach

- Count entries in plugin.json `skills` array and `agents` array
- Compare against README.md (line 12: "122 skills", "9 agents"), CLAUDE.md, AGENTS.md
- Fix all documents to show accurate counts
- Fix agent table in README to list all 14 agents
## Acceptance
- [ ] Skill count matches across plugin.json, README, CLAUDE.md, AGENTS.md
- [ ] Agent count = 14 across all documents
- [ ] README agent table lists all 14 agents
- [ ] All validation scripts pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
