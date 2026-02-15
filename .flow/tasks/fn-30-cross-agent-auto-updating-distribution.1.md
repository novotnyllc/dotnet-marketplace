# fn-30-cross-agent-auto-updating-distribution.1 Implement GitHub Pages distribution with manifest

## Description
Implement GitHub Pages distribution with manifest
## Approach
1. **Manifest generation in `generate_dist.py`**:
   - After generating `dist/{claude,copilot,codex}/`, compute SHA256 checksums for each target directory (hash of sorted file contents)
   - Write `dist/manifest.json` with schema: `{version, generated_at, targets: {claude: {path, sha256}, copilot: {path, sha256}, codex: {path, sha256}}}`
   - Version comes from existing `git describe --tags` logic
   - Timestamp in ISO 8601 UTC format
2. **Validation updates in `validate_cross_agent.py`**:
   - Validate `dist/manifest.json` exists after generation
   - Validate JSON schema (required fields: version, generated_at, targets with all three keys)
   - Validate SHA256 checksums match actual directory contents
3. **Replace zip workflow with Pages deployment in `release.yml`**:
   - Keep existing validation gates (validate-skills, validate-marketplace, generate_dist, validate_cross_agent)
   - Remove zip packaging steps and release asset uploads
   - Add `actions/upload-pages-artifact` to upload `dist/` directory
   - Add `actions/deploy-pages` to deploy to GitHub Pages
   - Add required permissions: `pages: write`, `id-token: write`
   - Keep GitHub Release creation for changelog notes (without zip attachments)

**Invariant**: Trigger corpus (`tests/trigger-corpus.json`) and existing conformance checks validate `dist/` content, not packaging — they remain unaffected.

## Acceptance
- [ ] `generate_dist.py` produces `dist/manifest.json` with version, generated_at (ISO 8601), and per-target SHA256 checksums
- [ ] `validate_cross_agent.py` validates manifest presence, JSON schema, and checksum correctness
- [ ] Release workflow deploys `dist/` to GitHub Pages via `actions/deploy-pages` on tag push
- [ ] Workflow has correct permissions (`pages: write`, `id-token: write`)
- [ ] GitHub Release still created for changelog/tag notes (without zip artifacts)
- [ ] Existing `dist/{claude,copilot,codex}/` structure preserved
- [ ] All four validation commands pass: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py --strict`, `validate_cross_agent.py`
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
