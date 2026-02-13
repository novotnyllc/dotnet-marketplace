# fn-13-uno-platform-skills.2 Create dotnet-uno-specialist agent

## Description
Create the `dotnet-uno-specialist` agent following the established pattern from `agents/dotnet-blazor-specialist.md`. The agent provides deep Uno Platform expertise for cross-platform project setup, target configuration, Extensions ecosystem guidance, and MVUX patterns.

### Deliverables
- `agents/dotnet-uno-specialist.md` with frontmatter: name, description, model, capabilities, tools
- Agent registered in `.claude-plugin/plugin.json` `agents` array as `"agents/dotnet-uno-specialist.md"`

### Agent Schema
- **Preloaded skills:** `[skill:dotnet-uno-platform]`, `[skill:dotnet-uno-targets]`, `[skill:dotnet-uno-mcp]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`
- **Workflow:** detect context → identify target platforms → recommend patterns → delegate to specialist skills
- **Trigger lexicon:** "uno platform", "uno app", "uno wasm", "uno mobile", "uno desktop", "uno extensions", "mvux", "uno toolkit", "uno themes", "cross-platform uno", "uno embedded"
- **Delegation boundaries:**
  - `[skill:dotnet-uno-testing]` for Playwright WASM and platform-specific testing
  - `[skill:dotnet-aot-wasm]` (soft) for general AOT/trimming patterns
  - `[skill:dotnet-ui-chooser]` (soft) for framework selection
- **Explicit boundaries:** Does NOT own testing (delegates), does NOT own general AOT (delegates), does NOT own framework selection (defers). Read-only Bash only.

## Acceptance
- [ ] `agents/dotnet-uno-specialist.md` exists with required frontmatter (name, description, model, capabilities, tools)
- [ ] Agent registered in `plugin.json` `agents` array
- [ ] Preloads all 5 specified skills (3 Uno + version-detection + project-analysis)
- [ ] Workflow section documents detect → identify → recommend → delegate flow
- [ ] Trigger lexicon includes all 11 trigger phrases from epic spec
- [ ] Delegation boundaries explicitly defined (testing, AOT, framework selection)
- [ ] Explicit boundaries section documents what agent does NOT own
- [ ] Read-only Bash constraint documented
- [ ] Pattern consistency with `agents/dotnet-blazor-specialist.md` verified

## Done summary
Created dotnet-uno-specialist agent at agents/dotnet-uno-specialist.md following the Blazor specialist pattern. Agent preloads 5 skills (dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp, dotnet-version-detection, dotnet-project-analysis), defines a 4-step workflow (detect context, identify targets, recommend patterns, delegate), includes all 11 trigger phrases, documents delegation boundaries for testing/AOT/framework-selection, and is registered in plugin.json.
## Evidence
- Commits: d0f0e98b06d636654a2ddf09296fca0fa6838d71
- Tests: ./scripts/validate-skills.sh
- PRs: