## Description
Create the foundational plugin directory structure and manifests for dotnet-artisan following Claude Code plugin conventions. This task creates minimal placeholder SKILL.md files so the structure passes validation.

**Size:** M
**Files:**
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `skills/foundation/dotnet-advisor/SKILL.md` (placeholder with valid frontmatter)
- `skills/foundation/dotnet-version-detection/SKILL.md` (placeholder)
- `skills/foundation/dotnet-project-analysis/SKILL.md` (placeholder)
- `skills/foundation/plugin-self-publish/SKILL.md` (placeholder)
- `agents/dotnet-architect.md` (placeholder with valid agent frontmatter)
- `hooks/hooks.json` (empty hooks structure)
- `.mcp.json` (empty MCP structure)
- `scripts/` (empty dir)

## Approach

1. Use `/plugin-dev:plugin-structure` skill FIRST to understand correct plugin conventions
2. Create `.claude-plugin/plugin.json` following this exact schema:
   ```json
   {
     "name": "dotnet-artisan",
     "version": "0.1.0",
     "description": "Comprehensive .NET development skills for modern C#, ASP.NET, MAUI, Blazor, and cloud-native applications",
     "skills": [
       "skills/foundation/dotnet-advisor",
       "skills/foundation/dotnet-version-detection",
       "skills/foundation/dotnet-project-analysis",
       "skills/foundation/plugin-self-publish"
     ],
     "agents": ["agents/dotnet-architect.md"],
     "hooks": "hooks/hooks.json",
     "mcpServers": ".mcp.json"
   }
   ```
   - `skills`: array of directory paths (each must contain `SKILL.md`)
   - `agents`: array of file paths (each `.md` with agent frontmatter)
   - `hooks`: string path to hooks.json
   - `mcpServers`: string path to .mcp.json
3. Create `marketplace.json` with marketplace metadata
4. Create placeholder SKILL.md files with valid frontmatter (name, description) so structure validates
5. Create placeholder agent file with valid agent frontmatter
6. Create category directories under `skills/` per spec (foundation/, core-csharp/, architecture/, etc.)
7. Create empty placeholder structures for hooks and MCP (populated in fn-23)

## Key context

- Follow Aaronontheweb/dotnet-skills plugin.json format as reference
- Plugin components must be at plugin root, NOT inside `.claude-plugin/`
- Use `${CLAUDE_PLUGIN_ROOT}` for all plugin-relative paths in hooks/MCP configs
- License: MIT, Author: Claire Novotny LLC
- Required SKILL.md frontmatter: `name` (string), `description` (string). See epic spec for canonical set.
- Placeholder SKILL.md files must have valid frontmatter but can have minimal body content (e.g., "Implementation in fn-2.X")
- Placeholder agent file must have valid frontmatter (name, description, tools)

## Acceptance
- [ ] `.claude-plugin/plugin.json` validates against canonical schema (skills=array of dir paths, agents=array of file paths, hooks=string path, mcpServers=string path)
- [ ] `.claude-plugin/marketplace.json` has correct metadata
- [ ] `skills/` directory has category subdirectories matching spec categories
- [ ] `agents/` directory exists with placeholder dotnet-architect.md
- [ ] `hooks/hooks.json` is valid empty hooks structure
- [ ] `.mcp.json` is valid empty MCP configuration
- [ ] All placeholder SKILL.md files have valid frontmatter (name, description)
- [ ] `/plugin-dev:plugin-validator` passes on the complete structure (placeholders make this possible)
- [ ] Plugin can be symlinked to `~/.claude/plugins/dotnet-artisan` for local testing
