# fn-23: Hooks and MCP Integration

## Problem/Goal
Create hooks.json with file-type-specific matchers for smart defaults (format on .cs edit, restore on .csproj edit, validate on .xaml edit), configure MCP servers (Uno Platform, Microsoft Learn, Context7), and define plugin settings for configurable behavior.

## Acceptance Checks
- [ ] hooks.json created with PostToolUse hooks for .cs, .csproj, test files, .xaml
- [ ] .mcp.json configured for Uno Platform MCP, Microsoft Learn MCP, Context7 MCP
- [ ] Plugin settings defined for hook aggressiveness, MCP toggles
- [ ] Hooks fire only for relevant file types with smart filtering
- [ ] Documentation for configuring hook behavior
- [ ] Cross-references to all relevant skills that hooks support

## Key Context
- Hooks should be helpful but not intrusive (configurable aggressiveness)
- File-type-specific matchers prevent hook spam
- MCP servers enhance skills with live documentation lookups
- Settings allow users to disable/tune hooks and MCP integration
