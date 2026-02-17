# fn-42-restructure-repo-into-marketplace-with.1 Clean up stale files and remove dist pipeline

## Description
Delete stale artifacts from completed work and remove the dist generation pipeline entirely.

**Size:** S
**Files:** Various deletions, `.gitignore`

## Approach

- **Fleet review artifacts**: Delete `docs/fleet-review-rubric.md` and `docs/review-reports/` (historical snapshots from completed fn-29/fn-40 epics)
- **Ralph execution logs**: Delete `scripts/ralph/runs/` (~107 MB of completed execution logs). Keep `scripts/ralph/` itself if it contains config/scripts, just the runs.
- **Dist pipeline**: Delete `scripts/generate_dist.py` and `scripts/validate_cross_agent.py`. These produced `dist/` output for Claude/Copilot/Codex — no longer needed since source files ARE the plugin.
- **Dist output**: Delete any committed files under `dist/` (should already be gitignored, verify). Remove the `dist/` entry from `.gitignore` since there's no dist anymore.
- **Completed flow epics**: Optionally clean up `.flow/` files for completed epics fn-29 and fn-40 (both marked "done"). These are small metadata files — low priority.
- **Python cache**: Delete `scripts/__pycache__/` if present.

## Key Context

- `generate_dist.py` (21 KB) generated dist/claude/, dist/copilot/, dist/codex/ from source
- `validate_cross_agent.py` (42 KB) validated the generated outputs
- Both are referenced in CI workflows — those references will be updated in Task .3
- Cross-ref `[skill:name]` validation was embedded in generate_dist.py — will be extracted in Task .2

## Acceptance
- [ ] `docs/fleet-review-rubric.md` and `docs/review-reports/` deleted
- [ ] `scripts/ralph/runs/` deleted
- [ ] `scripts/generate_dist.py` and `scripts/validate_cross_agent.py` deleted
- [ ] `dist/` entry removed from `.gitignore`
- [ ] `scripts/__pycache__/` cleaned if present
- [ ] No broken imports or references to deleted files in remaining code
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
