# fn-23-hooks-and-mcp-integration.2 Configure MCP servers (.mcp.json)

## Description
Populate `.mcp.json` with MCP server configurations for external documentation services that enhance the plugin's skills.

### .mcp.json Structure

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "env": {}
    }
  }
}
```

### Server Selection Rationale

**Context7** (primary):
- Provides library documentation lookup for any .NET library
- Covers Microsoft Learn docs, NuGet package docs, and general .NET ecosystem
- Single server that handles broad documentation needs
- No API key required, just npx

**Uno Platform MCP and Microsoft Learn MCP** (deferred):
- These are already accessible through Context7 and through deferred MCP tools configured in this project
- Only add dedicated servers if they provide capabilities beyond Context7
- Check Anthropic MCP registry for official server availability before adding

### Version Stability

The initial config uses `@upstash/context7-mcp@latest` for convenience. **Follow-up item:** After initial ship and stabilization, evaluate pinning to a specific version (e.g., `@1.x.x`) to prevent upstream breaking changes from silently breaking the plugin. This tradeoff (ship now with @latest, pin later) should be documented in the task's done summary.

### Implementation Notes
- Use `${CLAUDE_PLUGIN_ROOT}` for any plugin-relative paths in server configs
- Use `${VAR_NAME}` syntax for any user-provided API keys
- Test that `npx -y @upstash/context7-mcp@latest` starts successfully before shipping

### Validation
- `.mcp.json` must be valid JSON
- Must have top-level `mcpServers` key (even if empty)
- Server command must be available (npx requires Node.js)

## Acceptance
- [ ] `.mcp.json` contains at least one MCP server configuration (Context7)
- [ ] `.mcp.json` is valid JSON with `mcpServers` top-level key
- [ ] Context7 server config uses `npx -y @upstash/context7-mcp@latest`
- [ ] Any API-key-requiring servers use `${VAR_NAME}` env var expansion
- [ ] `validate-marketplace.sh` passes (exit 0)
- [ ] Server starts successfully when tested manually with `npx -y @upstash/context7-mcp@latest`
- [ ] Done summary notes the @latest vs pinned version tradeoff

## Done summary
Populated `.mcp.json` with Context7 MCP server configuration (`npx -y @upstash/context7-mcp@latest`) for library documentation lookup covering Microsoft Learn, NuGet, and .NET ecosystem docs. No API key required. Note: uses `@latest` tag for initial ship convenience; evaluate pinning to a specific version (e.g., `@1.x.x`) after stabilization to prevent upstream breaking changes.
## Evidence
- Commits: 5784087de655a3f00ef145645c47c0ea5753deab
- Tests: bash scripts/validate-marketplace.sh, jq empty .mcp.json, npx -y @upstash/context7-mcp@latest (manual server start test)
- PRs: