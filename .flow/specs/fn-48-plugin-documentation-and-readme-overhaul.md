# fn-48 Plugin Documentation and README Overhaul

## Overview

Overhaul the plugin documentation. The README.md needs accurate installation instructions, correct skill/agent counts, and a complete overview of what the plugin provides. CONTRIBUTING.md and CONTRIBUTING-SKILLS.md should be reviewed for accuracy.

## Scope

**In:** README.md rewrite with installation instructions, accurate counts, skill category overview, agent list. Review CONTRIBUTING.md and CONTRIBUTING-SKILLS.md for accuracy.

**Out:** Skill content changes (no SKILL.md edits). Plugin manifest changes.

## Key Context

- Current README says "9 specialist agents" but there are 14
- Current README says "122 skills" but plugin.json has 127 entries — needs reconciliation
- README should cover: what the plugin does, how to install, skill categories overview, agent overview, quick start

## Quick commands

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] README.md has correct installation instructions
- [ ] Skill count reconciled and accurate
- [ ] Agent count accurate (14)
- [ ] Skill category overview covers all 22 categories
- [ ] CONTRIBUTING.md reviewed for accuracy
- [ ] CONTRIBUTING-SKILLS.md reviewed for accuracy
- [ ] All validation scripts pass

## References

- `README.md` (current state)
- `CONTRIBUTING.md`, `CONTRIBUTING-SKILLS.md`
- `.claude-plugin/plugin.json` (authoritative skill/agent counts)
