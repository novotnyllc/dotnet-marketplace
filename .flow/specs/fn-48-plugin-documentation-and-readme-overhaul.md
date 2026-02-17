# fn-48 Plugin Documentation and README Overhaul

## Overview

Overhaul the plugin documentation. Reconcile skill/agent counts and rewrite README.md with installation instructions, accurate counts, and a complete overview. Review CONTRIBUTING.md and CONTRIBUTING-SKILLS.md for accuracy.

**Dependencies:** Runs after fn-43 through fn-47 complete (needs accurate post-batch counts). Expected skill count: 132 (127 current + 5 new).

## Scope

**In:** README.md rewrite with installation instructions, accurate counts, skill category overview. Fix CLAUDE.md and AGENTS.md counts. Review CONTRIBUTING.md and CONTRIBUTING-SKILLS.md for accuracy.

**Out:** Skill content changes (no SKILL.md edits). Plugin manifest changes.

## Key Context

- Current README says "9 specialist agents" but there are 14
- Current plugin.json has 127 skill entries but docs say "122" — 5 skills added without doc updates
- Post-batch count: 132 skills (127 + 5 new from fn-43-47), 14 agents
- README should cover: what the plugin does, how to install, skill categories overview, agent overview

## Quick commands

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] Skill count = 132 across plugin.json, README, CLAUDE.md, AGENTS.md
- [ ] Agent count = 14 across all documents
- [ ] README agent table lists all 14 agents
- [ ] README has installation instructions
- [ ] README has skill category overview covering all 22 categories
- [ ] CONTRIBUTING.md and CONTRIBUTING-SKILLS.md reviewed for accuracy
- [ ] `--projected-skills` in validate-skills.sh updated to 132
- [ ] All validation scripts pass

## References

- `README.md` (current state)
- `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`
- `.claude-plugin/plugin.json` (authoritative skill/agent counts)
