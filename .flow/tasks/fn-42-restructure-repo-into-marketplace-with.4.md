# fn-42-restructure-repo-into-marketplace-with.4 Add .agents/openai.yaml for Codex discovery

## Description
Create `.agents/openai.yaml` at the repo root so Codex can discover the plugin metadata. Minimal file — interface (display name, description) and policy fields.

**Size:** S
**Files:** `.agents/openai.yaml`

## Approach

- Create `.agents/openai.yaml` at the repo root with:
  - `interface.display_name`: "dotnet-artisan"
  - `interface.short_description`: the plugin description
  - `policy.allow_implicit_invocation`: true
- Verify the Codex openai.yaml schema before authoring — if the schema has changed or the URL is unavailable, use the pattern from existing repos (e.g., `anthropics/claude-plugins-official`)
- This file is hand-authored and committed — no generation needed
- This task has no dependencies and can be done in parallel with other tasks

## Key Context

- Codex reads `.agents/` at the repo root for skill discovery
- The skills themselves live at `plugins/dotnet-artisan/skills/` — the openai.yaml provides top-level metadata only
- This does NOT require moving or duplicating skills to `.agents/skills/`

## Acceptance
- [ ] `.agents/openai.yaml` exists at repo root
- [ ] Contains valid, parseable YAML (verified by any YAML parser)
- [ ] Contains `interface` and `policy` keys
- [ ] Display name and description match plugin metadata
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
