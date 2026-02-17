# fn-42-restructure-repo-into-marketplace-with.4 Add .agents/openai.yaml for Codex discovery

## Description
Create `.agents/openai.yaml` at the repo root so Codex's skill-installer can discover the plugin's metadata. Minimal file — just interface and policy fields per the Codex schema.

**Size:** S
**Files:** `.agents/openai.yaml`

## Approach

- Create `.agents/openai.yaml` at the repo root with:
  - `interface.display_name`: "dotnet-artisan" (from plugin marketplace.json)
  - `interface.short_description`: the plugin description
  - `policy.allow_implicit_invocation`: true
- Reference the Codex openai.yaml schema at https://developers.openai.com/codex/skills/ for exact field names and any additional required/optional fields
- This file is hand-authored and committed — no generation needed

## Key Context

- Codex's `$skill-installer` reads `.agents/` at the repo root
- `npx skills add` also reads `.agents/skills/` as a universal agent directory
- The skills themselves live at `plugins/dotnet-artisan/skills/` — the openai.yaml just provides top-level metadata for Codex to display
- This does NOT require moving or duplicating skills to `.agents/skills/` — `npx skills add` supports subdirectory paths to find them at `plugins/dotnet-artisan/`

## Acceptance
- [ ] `.agents/openai.yaml` exists at repo root
- [ ] Contains valid YAML with `interface` and `policy` keys
- [ ] Display name and description match plugin metadata
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
