# fn-24.3 Wire CI validation and release workflow for dist/ artifacts

## Description
Integrate the generator (fn-24.1) and conformance validator (fn-24.2) into CI and create a release workflow.

**CI changes** (`validate.yml`):
- Add step: `python3 scripts/generate_dist.py --strict` — generate dist/ outputs (--strict fails on parse errors instead of skipping)
<!-- Updated by plan-sync: fn-24.1 added --strict mode for CI; bare invocation silently skips unparseable SKILL.md files -->
- Add step: `python3 scripts/validate_cross_agent.py` — run conformance checks
- Both steps gate merge (failure blocks PR)
- Runs after existing validation steps (validate-skills.sh, validate-marketplace.sh)

**Release workflow** (`.github/workflows/release.yml`, new):
- Triggered on tag push (e.g., `v*`)
- Runs full validation pipeline (generate with `--strict` + validate)
- Creates GitHub Release with dist/ artifacts:
  - `dist-claude.zip` — Claude Code plugin package
  - `dist-copilot.zip` — Copilot instructions package
  - `dist-codex.zip` — Codex AGENTS.md package
- Version in release matches git tag

**No "marketplace publish" step** — Claude Code marketplace registration is via repo URL in `marketplace.json`, not a push mechanism. The release workflow makes artifacts downloadable.

## Dependencies
- fn-24.1 (generator script must exist)
- fn-24.2 (conformance validator must exist)

## Files touched
- `.github/workflows/validate.yml` (edit — add generate + validate steps)
- `.github/workflows/release.yml` (new — tag-triggered release workflow)

## Acceptance
- [ ] `validate.yml` runs generator with `--strict` + conformance checks on push/PR
- [ ] Conformance failure blocks merge
- [ ] `release.yml` triggered on tag push creates GitHub Release
- [ ] Release includes dist-claude.zip, dist-copilot.zip, dist-codex.zip
- [ ] Release version matches git tag
- [ ] No new CI dependencies beyond Python 3 (already available)
