# fn-36-library-api-compatibility-skills.3 Register skills in plugin.json, update dotnet-advisor catalog and AGENTS.md counts

## Description
Register both new skills in plugin.json, add them to the dotnet-advisor catalog under API Development, update skill counts in AGENTS.md and README.md, and add trigger-corpus entries.

**Size:** S
**Files:** .claude-plugin/plugin.json, skills/foundation/dotnet-advisor/SKILL.md, AGENTS.md, README.md
**Depends on:** fn-36-library-api-compatibility-skills.1, fn-36-library-api-compatibility-skills.2

## Approach
- Add `skills/api-development/dotnet-library-api-compat` and `skills/api-development/dotnet-api-surface-validation` to plugin.json skills array
- Add both skills to dotnet-advisor catalog under "API Development" section
- Update skill count in AGENTS.md (111 → 113) and README.md
- Add trigger-corpus entries for the new api-development skills
- Run all validation commands

## Acceptance
- [ ] Both skills registered in plugin.json — `grep -c 'dotnet-library-api-compat\|dotnet-api-surface-validation' .claude-plugin/plugin.json`
- [ ] Both skills in dotnet-advisor catalog — `grep -c 'dotnet-library-api-compat\|dotnet-api-surface-validation' skills/foundation/dotnet-advisor/SKILL.md`
- [ ] Skill count updated in AGENTS.md — `grep '113 skills' AGENTS.md`
- [ ] Trigger-corpus entries added
- [ ] All validation commands pass: `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh && python3 scripts/generate_dist.py --strict && python3 scripts/validate_cross_agent.py`

## Done summary
Registered dotnet-library-api-compat and dotnet-api-surface-validation in plugin.json, added both to dotnet-advisor catalog and routing sections, updated skill counts from 111 to 113 across AGENTS.md, README.md, CLAUDE.md (including Mermaid diagram), and added two trigger-corpus entries for binary compatibility and API surface validation queries.
## Evidence
- Commits: 6a2964d5c03503bafcc8a60fea39145ba2691b64
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: