# Cross-Agent Auto-Updating Distribution

## Overview
Replace the current zip-based release workflow (`.github/workflows/release.yml`) with GitHub Pages deployment, enabling auto-updatable distribution for cross-agent consumers (Claude Code, Copilot, Codex). The current approach requires manual download and extraction — cross-agent consumers have no built-in update mechanism for zip files.

## Chosen Mechanism: GitHub Pages

**Decision**: Deploy generated `dist/` contents to GitHub Pages on tag push.

**Rationale** (evaluated against dist-branch and release-asset alternatives):
- **GitHub Pages** (chosen): Stable URLs, CDN-cached (~10-min TTL), no auth needed for public repos, standard deployment via `actions/deploy-pages`. Consumers point at `https://<user>.github.io/<repo>/`.
- **`dist` branch**: Simpler but raw.githubusercontent.com has aggressive caching (5+ min), no CDN, URLs change on force-push. Not recommended.
- **Release assets + manifest**: Requires GitHub API polling, subject to rate limits, more complex consumer integration. Not recommended for this use case.

**Private repo note**: GitHub Pages requires the repo to be public (or GitHub Pro/Enterprise for private repos). For private repos, consumers can still download release assets directly via the GitHub API. The manifest includes both Pages URLs and a note about private repo alternatives.

## Manifest Schema

Each deployment produces `dist/manifest.json` at the Pages root:
```json
{
  "version": "1.2.3",
  "generated_at": "2026-02-14T12:00:00Z",
  "targets": {
    "claude": { "path": "claude/", "sha256": "<checksum-of-directory-contents>" },
    "copilot": { "path": "copilot/", "sha256": "<checksum-of-directory-contents>" },
    "codex": { "path": "codex/", "sha256": "<checksum-of-directory-contents>" }
  }
}
```

**Consumer auto-update contract**: Poll `manifest.json` no more than every 15 minutes. Compare `version` or `sha256` to detect updates. After a new release, content may take up to 10 minutes to propagate via GitHub Pages CDN.

## Pages URL Convention

```
https://<user>.github.io/<repo>/manifest.json
https://<user>.github.io/<repo>/claude/
https://<user>.github.io/<repo>/copilot/
https://<user>.github.io/<repo>/codex/
```

## Scope
- Add manifest generation to `generate_dist.py` (SHA256 checksums, version, timestamp)
- Update `validate_cross_agent.py` to validate manifest schema and checksum correctness
- Replace zip packaging in `release.yml` with GitHub Pages deployment (`actions/deploy-pages`)
- Keep GitHub Release for changelog/tag notes but remove zip artifacts
- Update README with Pages URLs and consumer polling instructions
- Document one-time repo setup requirement (Settings → Pages → Deploy from GitHub Actions)

**Invariant**: Trigger corpus and `validate_cross_agent.py` conformance checks validate `dist/` content, not packaging format — they remain unaffected by the distribution mechanism change.

## Quick commands
```bash
# Validate dist generation still works
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] `generate_dist.py` produces `dist/manifest.json` with version, timestamp, and per-target SHA256 checksums
- [ ] `validate_cross_agent.py` validates manifest presence, JSON schema, and checksum correctness
- [ ] CI/CD workflow deploys `dist/` to GitHub Pages on tag push using `actions/deploy-pages`
- [ ] Workflow has correct permissions (`pages: write`, `id-token: write`)
- [ ] GitHub Release still created for changelog notes (without zip artifacts)
- [ ] Existing `dist/{claude,copilot,codex}/` directory structure preserved
- [ ] README updated with Pages URLs, auto-update polling instructions, and one-time repo setup note
- [ ] Old zip packaging steps removed from release workflow
- [ ] Caching behavior documented: ~10-min CDN TTL, poll no more than every 15 minutes

## References
- `.github/workflows/release.yml` — current zip workflow (to be replaced)
- `scripts/generate_dist.py` — cross-agent output generator (gains manifest generation)
- `scripts/validate_cross_agent.py` — conformance validator (gains manifest validation)
- `actions/deploy-pages` — GitHub's official Pages deployment action
