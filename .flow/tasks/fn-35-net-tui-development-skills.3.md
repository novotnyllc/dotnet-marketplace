# fn-35-net-tui-development-skills.3 Register TUI skills and update counts

## Description
Register both TUI skills in plugin.json, update README.md/CLAUDE.md/AGENTS.md with new skill counts and TUI category, add trigger-corpus entries for routing tests, and run full validation.

**Size:** S
**Depends on:** .1, .2
**Files:** .claude-plugin/plugin.json, README.md, CLAUDE.md, AGENTS.md, scripts/trigger-corpus.json

## Approach
- Add `skills/tui/dotnet-terminal-gui` and `skills/tui/dotnet-spectre-console` to plugin.json skills array
- Update README.md skill catalog with new TUI category section and total counts
- Update CLAUDE.md skill/category counts
- Add TUI category row to AGENTS.md routing index
- Add trigger-corpus.json entries for TUI-related queries
- Run all four validation commands

## Acceptance
- [ ] Both skills registered in plugin.json skills array
- [ ] README.md lists TUI category with both skills, total counts updated
- [ ] CLAUDE.md counts updated
- [ ] AGENTS.md routing index has TUI category row
- [ ] Trigger corpus has entries routing TUI queries to correct skills
- [ ] `./scripts/validate-skills.sh` passes
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] `python3 scripts/generate_dist.py --strict` passes
- [ ] `python3 scripts/validate_cross_agent.py` passes

## Verification
```bash
grep -c "dotnet-terminal-gui\|dotnet-spectre-console" .claude-plugin/plugin.json  # expect 2
grep -i "tui" AGENTS.md  # expect routing row
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh && python3 scripts/generate_dist.py --strict && python3 scripts/validate_cross_agent.py
```

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
