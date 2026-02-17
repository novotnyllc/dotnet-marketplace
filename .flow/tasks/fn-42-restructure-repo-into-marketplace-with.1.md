# fn-42-restructure-repo-into-marketplace-with.1 Clean up stale files and remove dist pipeline

## Description
Delete stale artifacts from completed work and remove the dist generation pipeline entirely. This task focuses only on removing genuinely stale files — the root plugin.json deletion happens in Task 2 where its replacement is created atomically.

**Size:** S
**Files:** Various deletions, `.gitignore`

## Approach

- **Fleet review artifacts**: Delete `docs/fleet-review-rubric.md` and `docs/review-reports/` (historical snapshots from completed fn-29/fn-40 epics)
- **Ralph execution logs**: Keep `scripts/ralph/` itself (config.env, ralph.sh, etc.) at repo root — it is repo-level dev tooling, not plugin content.
- **Dist pipeline scripts**: Delete `scripts/generate_dist.py` and `scripts/validate_cross_agent.py`
- **Dist output**: Delete the `dist/` directory entirely. Remove the `dist/` entry from `.gitignore`. No new `.gitignore` entries are needed — existing root patterns (`__pycache__/`, etc.) cover build artifacts globally.
- **Python cache**: Delete `scripts/__pycache__/` if present.

**Note**: Root `.claude-plugin/plugin.json` is NOT deleted here. It is deleted atomically in Task 2 when the replacement marketplace.json and per-plugin plugin.json are created, preventing any state where the repo has no discoverable manifest.

## Key Context

- `generate_dist.py` generated dist/claude/, dist/copilot/, dist/codex/ from source
- `validate_cross_agent.py` validated the generated outputs
- Both are referenced in CI workflows — those references are updated in Task 3
- Cross-ref `[skill:name]` validation already exists in `_validate_skills.py` (lines 130-131, 293-305) — no extraction needed
- All tasks happen on a feature branch; intermediate CI breakage is acceptable

## Acceptance
- [ ] `docs/fleet-review-rubric.md` and `docs/review-reports/` deleted
- [ ] `scripts/ralph/runs/` deleted; `scripts/ralph/` (config, scripts) preserved
- [ ] `scripts/generate_dist.py` and `scripts/validate_cross_agent.py` deleted
- [ ] `dist/` directory deleted; `dist/` entry removed from `.gitignore`
- [ ] `scripts/__pycache__/` cleaned if present
- [ ] No broken imports or references to deleted files in remaining code
## Done summary
Deleted stale fleet review artifacts (docs/fleet-review-rubric.md, docs/review-reports/), dist pipeline scripts (generate_dist.py, validate_cross_agent.py), dist/ output directory, scripts/ralph/runs/ execution logs, and scripts/__pycache__/. Removed dist/ entry from .gitignore. scripts/ralph/ dev tooling preserved intact.
## Evidence
- Commits: f3e92e1e8fde45a001eb68b5663c40a32c4ac1e5, eb92b0965e528c79248147766ff76578d8c312c4
- Tests: ./scripts/validate-skills.sh
- PRs: