# fn-40-fleet-review-findings-implementation.2 Update documentation and archive review artifacts

## Description
Update all project documentation to reflect the current state after fleet review findings are resolved (task 1) and fn-37 cleanup is complete. Archive the fleet review rubric and consolidated findings as historical snapshots. Add a CHANGELOG entry documenting the resolution.

**Size:** M
**Files:**
- `README.md` -- skill counts, category table, architecture diagram
- `CLAUDE.md` -- skill count, budget numbers (including WARN threshold if adjusted in task 1)
- `AGENTS.md` -- routing index counts, category table
- `CHANGELOG.md` -- new entry under `[Unreleased]`
- `docs/fleet-review-rubric.md` -- archive annotation
- `docs/review-reports/consolidated-findings.md` -- archive annotation

## Approach

1. Run `./scripts/validate-skills.sh` to get final skill count and budget numbers
2. Search for the current skill/category count string (e.g., "113 skills across 21 categories") in README.md, CLAUDE.md, AGENTS.md and update all occurrences to match actual `plugin.json` registered count
3. Update the mermaid diagram skill counts in README.md (search for "Skill Categories" or the diagram block)
4. If WARN threshold was adjusted in task 1, update CLAUDE.md budget section to reflect the new threshold
5. Verify all three docs have identical skill/category counts
6. Add CHANGELOG.md entry under `[Unreleased]`:
   - `### Changed` for description trimming and threshold adjustment (if applicable)
   - `### Fixed` for fleet review finding resolution
   - Include metrics: budget before/after chars, number of descriptions trimmed
   - Reference fn-29 (audit), fn-37 (cleanup), fn-40 (this epic)
7. Add archive header to fleet review docs:
   ```markdown
   > **Historical snapshot (completed YYYY-MM-DD).** Most findings resolved by fn-30 through fn-40. See CHANGELOG.md for details.
   ```
8. Run all 4 validation commands
9. Verify no regressions from fn-37 changes (`grep -r 'fn-[0-9]' skills/` should return zero hits if fn-37 completed)

## Key context

- README.md, CLAUDE.md, AGENTS.md all reference skill/category counts -- use grep-based search (not line numbers) to find and update all occurrences, since fn-37 or task 1 may have shifted line numbers
- CHANGELOG.md uses keep-a-changelog format with `### Added`, `### Changed`, `### Fixed`, `### Removed` section headers
- The fleet review rubric (`docs/fleet-review-rubric.md`) is reusable for future audits -- annotate as historical but don't delete
- Per memory conventions: count updates across multiple files must stay in sync
## Approach

1. Run `./scripts/validate-skills.sh` to get final skill count and budget numbers
2. Search for the current skill/category count string (e.g., "113 skills across 21 categories") in README.md, CLAUDE.md, AGENTS.md and update all occurrences to match actual `plugin.json` registered count
3. Update the mermaid diagram skill counts in README.md (search for "Skill Categories" or the diagram block)
4. If WARN threshold was adjusted in task 1, update CLAUDE.md budget section to reflect the new threshold
5. Verify all three docs have identical skill/category counts
6. Add CHANGELOG.md entry under `[Unreleased]`:
   - `### Changed` for description trimming and threshold adjustment (if applicable)
   - `### Fixed` for fleet review finding resolution
   - Include metrics: budget before/after chars, number of descriptions trimmed
   - Reference fn-29 (audit), fn-37 (cleanup), fn-40 (this epic)
7. Add archive header to fleet review docs:
   ```markdown
   > **Historical snapshot (completed YYYY-MM-DD).** Most findings resolved by fn-30 through fn-40. See CHANGELOG.md for details.
   ```
8. Run all 4 validation commands
9. Verify no regressions from fn-37 changes (`grep -r 'fn-[0-9]' skills/` should return zero hits if fn-37 completed)

## Key context

- README.md, CLAUDE.md, AGENTS.md all reference skill/category counts -- use grep-based search (not line numbers) to find and update all occurrences, since fn-37 or task 1 may have shifted line numbers
- CHANGELOG.md uses keep-a-changelog format with `### Added`, `### Changed`, `### Fixed`, `### Removed` section headers
- The fleet review rubric (`docs/fleet-review-rubric.md`) is reusable for future audits -- annotate as historical but don't delete
- Per memory conventions: count updates across multiple files must stay in sync
## Approach

1. Run `./scripts/validate-skills.sh` to get final skill count and budget numbers
2. Update counts in README.md (L11, L34, L98-119 mermaid diagram), CLAUDE.md (L3, L19, L39), AGENTS.md (L7, L9-31)
3. Verify all three docs have identical skill/category counts
4. Add CHANGELOG.md entry under `[Unreleased]` with:
   - Description budget improvement (before → after chars)
   - Number of descriptions trimmed
   - Reference to fn-29 (audit), fn-37 (cleanup), fn-40 (this epic)
5. Add archive header to fleet review docs:
   ```markdown
   > **Historical snapshot (completed YYYY-MM-DD).** Most findings resolved by fn-30 through fn-40. See CHANGELOG.md for details.
   ```
6. Run all 4 validation commands

## Key context

- README.md, CLAUDE.md, AGENTS.md all reference "113 skills across 21 categories" -- update all three consistently
- Per memory conventions: count updates across multiple files must stay in sync (README L11 ↔ CLAUDE.md L3 ↔ AGENTS.md L7)
- The fleet review rubric (`docs/fleet-review-rubric.md`) is reusable for future audits -- annotate as historical but don't delete
- CHANGELOG.md uses keep-a-changelog format (Added/Changed/Fixed/Removed sections)
## Acceptance
- [ ] README.md, CLAUDE.md, AGENTS.md all show identical skill and category counts
- [ ] Counts match actual `plugin.json` registered skill count (verified by `jq '.skills | length'`)
- [ ] If WARN threshold was adjusted in task 1, CLAUDE.md budget section reflects the new threshold
- [ ] CHANGELOG.md has entry under `[Unreleased]` with `### Changed` and/or `### Fixed` sections documenting fleet review resolution with budget metrics
- [ ] `docs/fleet-review-rubric.md` has archive annotation header
- [ ] `docs/review-reports/consolidated-findings.md` has archive annotation header
- [ ] All 4 validation commands pass: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py --strict`, `validate_cross_agent.py`
- [ ] No regressions from fn-37 changes (zero `fn-[0-9]` references in skill files if fn-37 completed)
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
