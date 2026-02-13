# fn-13-uno-platform-skills.1 Create Uno Platform skills (platform, targets, MCP)

## Description
Create three Uno Platform skills covering the core ecosystem, per-target deployment, and MCP server integration. Each skill follows canonical frontmatter (`name`, `description`) and uses `[skill:name]` cross-reference syntax. All three skills are registered in `plugin.json` and added to the `dotnet-advisor` catalog.

### Deliverables
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md` — Extensions ecosystem (Navigation, DI, Config, Serialization, Localization, Logging, HTTP, Authentication), MVUX reactive pattern, Toolkit controls, Theme resources (Material/Cupertino/Fluent), Hot Reload, single-project structure
- `skills/ui-frameworks/dotnet-uno-targets/SKILL.md` — Per-target guidance for Web/WASM, iOS, Android, macOS Catalyst, Windows, Linux (Skia/GTK), Embedded (Skia/Framebuffer). Each target section covers: project setup, debugging, packaging/distribution, platform gotchas, AOT/trimming implications, and behavior differences from other targets
- `skills/ui-frameworks/dotnet-uno-mcp/SKILL.md` — MCP server integration: tool detection (`mcp__uno__` prefix), search-then-fetch workflow, init rules invocation, graceful fallback when MCP unavailable, citation requirements, safety guidelines for external data. Must include inline documentation that works without MCP server
- All 3 skills registered in `.claude-plugin/plugin.json` `skills` array
- Ensure `dotnet-advisor` catalog entries and routing are present and deduplicated for all 3 skills

### Cross-references
- Hard: `[skill:dotnet-uno-testing]`, `[skill:dotnet-serialization]`
- Soft: `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]`

### Files modified
- `skills/ui-frameworks/dotnet-uno-platform/SKILL.md` (new)
- `skills/ui-frameworks/dotnet-uno-targets/SKILL.md` (new)
- `skills/ui-frameworks/dotnet-uno-mcp/SKILL.md` (new)
- `.claude-plugin/plugin.json` (add 3 skill paths)
- `skills/foundation/dotnet-advisor/SKILL.md` (ensure catalog entries + routing, deduplicate)

## Acceptance
- [ ] `dotnet-uno-platform` SKILL.md exists with `name` and `description` frontmatter
- [ ] `dotnet-uno-platform` covers all 8 Extensions modules from epic coverage table
- [ ] `dotnet-uno-platform` documents MVUX pattern, Toolkit controls, Theme resources, Hot Reload
- [ ] `dotnet-uno-targets` SKILL.md exists with per-target sections for all 7 targets
- [ ] Each target section includes: setup, debugging, packaging, gotchas, AOT/trimming
- [ ] `dotnet-uno-targets` documents per-target behavior differences (navigation, auth, debugging)
- [ ] `dotnet-uno-mcp` SKILL.md exists with MCP workflow: detection, search, fetch, init rules (`uno_platform_agent_rules_init`, `uno_platform_usage_rules_init`), fallback, citation, safety
- [ ] `dotnet-uno-mcp` includes inline documentation that works without MCP server availability
- [ ] All 3 skills registered in `plugin.json`
- [ ] All 3 skills present in `dotnet-advisor` catalog; no duplicate IDs
- [ ] Hard cross-refs `[skill:dotnet-uno-testing]` and `[skill:dotnet-serialization]` resolve
- [ ] Soft cross-refs `[skill:dotnet-aot-wasm]`, `[skill:dotnet-ui-chooser]` present
- [ ] Each skill description ≤ 120 chars
- [ ] `./scripts/validate-skills.sh` passes

## Done summary
Created three Uno Platform skills: dotnet-uno-platform (Extensions ecosystem with 8 modules, MVUX, Toolkit, themes, Hot Reload), dotnet-uno-targets (per-target guidance for all 7 platforms with setup/debugging/packaging/gotchas/AOT), and dotnet-uno-mcp (MCP server integration with detection, search-fetch workflow, init rules, fallback, citation). All registered in plugin.json and verified in dotnet-advisor catalog.
## Evidence
- Commits: 6d6f913, f76b399, e61ee09
- Tests: ./scripts/validate-skills.sh
- PRs: