# fn-14-maui-skills.2 Create dotnet-maui-specialist agent

## Description
Create the `dotnet-maui-specialist` agent following the established pattern from `agents/dotnet-blazor-specialist.md` and `agents/dotnet-uno-specialist.md`. The agent provides deep MAUI expertise for platform-specific development, migration guidance, and AOT optimization.

### Deliverables
- `agents/dotnet-maui-specialist.md` with frontmatter: name, description, model, capabilities, tools
- Agent registered in `.claude-plugin/plugin.json` `agents` array as `"agents/dotnet-maui-specialist.md"`

### Agent Schema
- **Preloaded skills:** `[skill:dotnet-maui-development]`, `[skill:dotnet-maui-aot]`, `[skill:dotnet-version-detection]`, `[skill:dotnet-project-analysis]`
- **Workflow:** detect context → identify platform targets → recommend patterns → delegate to specialist skills
- **Trigger lexicon:** "maui", "maui app", "maui xaml", "maui native aot", "maui ios", "maui android", "maui catalyst", "maui windows", "xamarin migration", "maui hot reload", "maui aot"
- **Delegation boundaries:**
  - `[skill:dotnet-maui-testing]` for Appium and XHarness testing
  - `[skill:dotnet-native-aot]` (soft) for general AOT patterns
  - `[skill:dotnet-ui-chooser]` (soft) for framework selection
- **Explicit boundaries:** Does NOT own testing (delegates to `dotnet-maui-testing`), does NOT own general AOT (delegates to `dotnet-native-aot`), does NOT own framework selection (defers to `dotnet-ui-chooser`). Read-only Bash only.

### Files modified
- `agents/dotnet-maui-specialist.md` (new)
- `.claude-plugin/plugin.json` (add agent path to `agents` array)

## Acceptance
- [ ] `agents/dotnet-maui-specialist.md` exists with required frontmatter (name, description, model, capabilities, tools)
- [ ] Agent registered in `plugin.json` `agents` array
- [ ] Preloads all 4 specified skills (2 MAUI + version-detection + project-analysis)
- [ ] Workflow section documents detect → identify → recommend → delegate flow
- [ ] Trigger lexicon includes all 11 trigger phrases from epic spec
- [ ] Delegation boundaries explicitly defined (testing, AOT, framework selection)
- [ ] Explicit boundaries section documents what agent does NOT own
- [ ] Read-only Bash constraint documented
- [ ] Pattern consistency with `agents/dotnet-blazor-specialist.md` and `agents/dotnet-uno-specialist.md` verified

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
