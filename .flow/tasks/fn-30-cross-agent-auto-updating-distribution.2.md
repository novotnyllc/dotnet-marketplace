# fn-30-cross-agent-auto-updating-distribution.2 Update docs and deprecate zip workflow

## Description
Update README with GitHub Pages URLs, consumer auto-update polling instructions, and one-time repo setup documentation. Remove zip packaging from the release workflow. Add distribution evaluation rationale.

**Size:** S
**Files:** `README.md`, `CONTRIBUTING.md`, `.github/workflows/release.yml`

## Approach
1. **Update README installation section**:
   - Replace zip download instructions with Pages URLs
   - Add per-platform auto-update instructions (Claude Code, Copilot, Codex)
   - Document `manifest.json` polling contract: poll no more than every 15 minutes, ~10-min CDN TTL
   - Note one-time repo setup requirement: Settings → Pages → Deploy from GitHub Actions
2. **Document private repo considerations**:
   - GitHub Pages requires public repo (or GitHub Pro/Enterprise for private)
   - For private repos, consumers can use GitHub API to fetch release assets as fallback
3. **Verify zip packaging removal** (completed by Task 1):
   - Confirm no zip creation steps remain in release.yml (Task 1 already replaced with `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`)
   - Confirm GitHub Release still created via `softprops/action-gh-release@v2` for changelog notes (no zip attachments)
<!-- Updated by plan-sync: fn-30.1 already removed zip packaging and replaced with GitHub Pages deployment -->
4. **Update CONTRIBUTING.md** if it references the zip-based release process

## Acceptance
- [ ] README installation instructions point to Pages URLs (`https://<user>.github.io/<repo>/`)
- [ ] Auto-update polling contract documented (15-min poll interval, 10-min CDN TTL)
- [ ] One-time repo setup documented (Pages → Deploy from GitHub Actions)
- [ ] Private repo considerations noted
- [ ] Zip packaging steps confirmed absent from release workflow (already removed by Task 1)
<!-- Updated by plan-sync: fn-30.1 already removed zip packaging from release.yml -->
- [ ] CONTRIBUTING.md updated if it references old release process
## Done summary
Updated README with GitHub Pages distribution URLs, auto-update manifest polling contract (15-min interval, 10-min CDN TTL), one-time repo setup instructions, and private repository considerations. Added release/deployment summary to CONTRIBUTING.md. Verified release.yml has no zip packaging remnants.
## Evidence
- Commits: ea0e32e314ab5f0f5a2bcff8a6f3317718ae07e6
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: