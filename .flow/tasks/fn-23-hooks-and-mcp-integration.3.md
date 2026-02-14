# fn-23-hooks-and-mcp-integration.3 Document hook/MCP behavior and validate

## Description
Ensure hooks and MCP integration are documented and validation scripts cover the new files. This task does NOT implement a plugin settings system (Claude Code plugins have no user-configurable settings mechanism), but documents how users can control behavior.

**Dependencies:** This task depends on fn-23.1 and fn-23.2 (hooks and MCP must exist before validation can verify them).

### Documentation Deliverables

Add a section to the plugin's documentation covering:

1. **What hooks do**: Brief explanation of each hook behavior:
   - `.cs` edits: auto-formats with `dotnet format` (async, reports on next turn)
   - `.csproj` edits: suggests running `dotnet restore`
   - `.xaml` edits: validates XML well-formedness
   - `*Tests.cs` edits: suggests running related tests
   - Session start: detects .NET project type and injects context
2. **How to disable hooks**: Point users to `disableAllHooks: true` in `.claude/settings.json` or `/hooks` menu
3. **MCP server requirements**: Node.js required for Context7 (`npx`); how to check with `/mcp`
4. **Troubleshooting**: Common issues:
   - `dotnet` not found: install .NET SDK, hook degrades gracefully
   - `npx` not available: install Node.js, MCP servers won't start
   - Hooks not firing: restart Claude Code (hooks snapshot at startup)
   - `jq` not found: install jq or hook script falls back to python

### Validation Additions to validate-marketplace.sh

Add after the existing mcpServers path check:

```bash
# --- hooks validation ---

# 1. Validate hooks/hooks.json has a "hooks" key
if ! jq -e '.hooks' hooks/hooks.json >/dev/null 2>&1; then
  echo "ERROR: hooks/hooks.json missing 'hooks' key"
  ERRORS=$((ERRORS + 1))
fi

# 2. Validate .mcp.json has "mcpServers" key
if ! jq -e '.mcpServers' .mcp.json >/dev/null 2>&1; then
  echo "ERROR: .mcp.json missing 'mcpServers' key"
  ERRORS=$((ERRORS + 1))
fi

# 3. Check all scripts/hooks/*.sh are executable
if ls scripts/hooks/*.sh 1>/dev/null 2>&1; then
  for script in scripts/hooks/*.sh; do
    if [ ! -x "$script" ]; then
      echo "ERROR: $script is not executable (chmod +x needed)"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi
```

### Implementation Notes
- Documentation can be inline in a skill SKILL.md, in a hooks guide file, or prepared for fn-25 (README)
- Validation should be lightweight and match existing script patterns (error counter, sequential checks)
- Keep documentation concise; users can read Claude Code docs for hook system details

## Acceptance
- [ ] Documentation exists explaining what each hook does (format, restore, XAML, tests, session context)
- [ ] Documentation explains how to disable hooks (`disableAllHooks` or `/hooks` menu)
- [ ] Documentation explains MCP server requirements (Node.js for npx)
- [ ] Documentation includes troubleshooting for common issues
- [ ] `validate-marketplace.sh` validates `hooks/hooks.json` has `hooks` key (not just valid JSON)
- [ ] `validate-marketplace.sh` validates `.mcp.json` has `mcpServers` key
- [ ] `validate-marketplace.sh` checks `scripts/hooks/*.sh` for executable permission
- [ ] All validation passes (exit 0)

## Done summary
Added docs/hooks-and-mcp-guide.md documenting hook behaviors, disable instructions, MCP server requirements, and troubleshooting. Extended validate-marketplace.sh with hooks content validation (hooks key, mcpServers key, executable permissions).
## Evidence
- Commits: 34753cb611c323d997f5a093f499ddbc9b952a32
- Tests: bash scripts/validate-marketplace.sh
- PRs: