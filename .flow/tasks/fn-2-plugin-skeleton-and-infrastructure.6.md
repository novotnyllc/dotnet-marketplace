## Description
Create the CI validation workflow (GitHub Actions) and the `dotnet-architect` agent that serves as the primary architecture advisor subagent.

**Size:** M
**Files:**
- `.github/workflows/validate.yml`
- `agents/dotnet-architect.md`

## Approach

1. `.github/workflows/validate.yml`:
   - Triggers on push and PR to main
   - Runs exact same commands as local validation:
     ```
     ./scripts/validate-skills.sh
     ./scripts/validate-marketplace.sh
     ```
   - Validates JSON files via jq: `jq empty .claude-plugin/plugin.json .claude-plugin/marketplace.json hooks/hooks.json .mcp.json`
   - Captures budget output by parsing stable keys from validate-skills.sh:
     - CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS
   - Reports budget values in workflow summary
   - Pass/fail: workflow fails if ANY script exits non-zero
   - Target: <2 min total runtime (lightweight, no .NET SDK needed)
2. `dotnet-architect` agent:
   - Description: "Analyzes .NET project context, requirements, and constraints to recommend architecture approaches, framework choices, and design patterns"
   - Use `/plugin-dev:agent-development` for frontmatter format
   - Preloads: [skill:dotnet-advisor], [skill:dotnet-version-detection], [skill:dotnet-project-analysis]
   - Model: sonnet (focused analysis, not orchestration)
   - Tools: Read, Glob, Grep, Bash (read-only analysis)

## Key context

- CI workflow is lightweight validation only (not building .NET code, no SDK install needed)
- dotnet-architect agent is the primary advisor for planning mode
- Agent description must trigger on architecture questions: "what framework", "how to structure", "recommend approach"
- Follow Aaronontheweb/dotnet-skills agent format as reference
- CI must run the EXACT same validation commands used locally (no separate CI-only logic)
- CI parses stable output keys (CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS) for workflow summary
- Depends on fn-2.2 (router skill exists) and fn-2.5 (validation scripts exist)

## Acceptance
- [ ] GitHub Actions workflow triggers on push and PR to main
- [ ] Workflow runs `./scripts/validate-skills.sh` and `./scripts/validate-marketplace.sh` (same as local)
- [ ] Workflow validates JSON files via `jq empty`
- [ ] Workflow parses and reports CURRENT_DESC_CHARS, PROJECTED_DESC_CHARS, BUDGET_STATUS in summary
- [ ] Workflow fails on any validation error (non-zero exit)
- [ ] Workflow completes in <2 minutes
- [ ] dotnet-architect agent has correct frontmatter (name, description, tools, model)
- [ ] Agent description triggers on architecture/recommendation queries
- [ ] Agent preloads foundation skills via [skill:name] references
- [ ] `/plugin-dev:plugin-validator` passes on complete plugin structure
