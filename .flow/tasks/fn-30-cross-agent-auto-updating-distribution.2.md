# fn-30-cross-agent-auto-updating-distribution.2 Implement auto-updating distribution pipeline

## Description
Implement the chosen distribution mechanism. Update generate_dist.py if needed and create/modify the CI/CD workflow to publish automatically on tag push. Add version manifest for consumer auto-update detection.

**Size:** M
**Files:** .github/workflows/release.yml, scripts/generate_dist.py, version manifest file

## Approach
- Follow pattern from existing release.yml
- Add version manifest (JSON with version, checksums, timestamp)
- Ensure dist/claude/, dist/copilot/, dist/codex/ structure preserved
## Acceptance
- [ ] CI/CD workflow publishes on tag push
- [ ] Version manifest generated with each publish
- [ ] All three dist targets published
- [ ] Validation scripts pass before publish
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
