# Cross-Agent Auto-Updating Distribution

## Overview
Replace the current zip-based release workflow (`.github/workflows/release.yml`) with an auto-updatable distribution mechanism. The current approach requires manual download and extraction — cross-agent consumers (Claude Code, Copilot, Codex) have no built-in update mechanism for zip files.

## Scope
- Evaluate and implement one of: GitHub Pages site, dedicated `dist` branch, or GitHub release with manifest
- Ensure the chosen mechanism supports auto-update detection (version manifest, ETag, or commit SHA)
- Update `generate_dist.py` to output to the chosen target
- Update CI/CD workflow to publish on tag push
- Preserve existing `dist/claude/`, `dist/copilot/`, `dist/codex/` structure

## Approach
- **Option A: `dist` branch** — CI pushes generated files to a `dist` branch on each tag. Consumers point at raw GitHub URLs. Auto-update via branch HEAD SHA comparison.
- **Option B: GitHub Pages** — CI deploys to Pages site. Consumers fetch from `<user>.github.io/<repo>/`. Auto-update via version manifest JSON.
- **Option C: Release assets with manifest** — Keep release workflow but add a `manifest.json` with version + checksums. Consumers poll latest release API.

Research from scouts: GitHub Pages is most seamless for cross-agent consumption (stable URLs, CDN-cached, no auth needed for public repos). The `dist` branch approach is simpler but raw.githubusercontent.com has aggressive caching.

## Quick commands
```bash
# Validate dist generation still works
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] Distribution mechanism chosen and documented
- [ ] CI/CD workflow updated to publish automatically on tag push
- [ ] Version manifest exists for consumers to detect updates
- [ ] Existing `dist/` structure preserved (claude/, copilot/, codex/)
- [ ] README updated with new installation/update instructions
- [ ] Old zip-based workflow removed or deprecated

## References
- `.github/workflows/release.yml` — current zip workflow
- `scripts/generate_dist.py` — cross-agent output generator
- `scripts/validate_cross_agent.py` — conformance validator
