# fn-29-fleet-skill-review-and-improvement-sweep.12 Final validation and context budget check

## Description

Run all four validation commands, verify context budget, check all cross-references, and update shared files (plugin.json, AGENTS.md, README.md) if any skills were added/removed/renamed. Clean up review reports — keep consolidated findings, archive batch reports.

**File ownership:** This task is the sole owner of modifications to `plugin.json`, `AGENTS.md`, and `README.md`. All shared-file updates (skill counts, routing index, catalog) happen here.

### Files

- **Validation:** `./scripts/validate-skills.sh`, `./scripts/validate-marketplace.sh`, `python3 scripts/generate_dist.py --strict`, `python3 scripts/validate_cross_agent.py`
- **Shared files (sole owner):** `.claude-plugin/plugin.json`, `AGENTS.md`, `README.md`
- **Cleanup:** `docs/review-reports/batch-{a..f}-findings.md` (archive or remove), keep `docs/review-reports/consolidated-findings.md`

## Acceptance
- [ ] `./scripts/validate-skills.sh` passes
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] `python3 scripts/generate_dist.py --strict` passes
- [ ] `python3 scripts/validate_cross_agent.py` passes
- [ ] Total description budget < 15,000 chars (warn if > 12,000)
- [ ] All `[skill:name]` cross-references resolve to existing skills
- [ ] plugin.json skill count matches actual skill directories on disk
- [ ] AGENTS.md skill counts updated if changed
- [ ] Batch findings reports archived or removed; consolidated findings retained

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
