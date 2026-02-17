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
- [x] `.agents/openai.yaml` exists at repo root
- [x] Contains valid, parseable YAML (verified by Ruby YAML parser)
- [x] Contains `interface` and `policy` keys
- [x] Display name and description match plugin metadata
## Done summary
Created .agents/openai.yaml at repo root for Codex discovery with interface (display_name, short_description matching plugin.json) and policy (allow_implicit_invocation: true) fields.
## Task
Create `.agents/openai.yaml` at repo root for Codex plugin discovery.

## Review Summary
Conducted John Carmack-level specification review using RepoPrompt backend.

### Initial Review Verdict: NEEDS_WORK
- Critical: Schema authenticity unverified
- Major (2): File location concerns, no CI validation
- Minor (3): Description drift, weak criteria, missing refs
- Nitpick (2): dependencies.tools clarity, directory creation

### Re-Review Findings
Reviewer downgraded critical to major (mitigated by pragmatic fallback). File location and task refs addressed in spec. Schema concern acceptable with documentation.

**Final Verdict: SHIP**

### Recommended Actions Before Implementation
1. Add YAML comment noting schema source is community convention
2. Create `.agents/` directory explicitly (not just openai.yaml file)
3. File follow-up to add CI validation to validate.yml

## Review Process
- Backend: RepoPrompt
- Initial prompt: Specification review with schema validation focus
- Re-review: Addressed findings and clarifications
- Files reviewed: Task spec, plugin.json, CLAUDE.md, sibling task .3

## Outcome
Task spec is SHIP-ready for implementation. One follow-up task recommended (CI validation integration).
## Evidence
- Commits:
- Tests: ruby -ryaml -e YAML.safe_load(File.read(.agents/openai.yaml))
- PRs: