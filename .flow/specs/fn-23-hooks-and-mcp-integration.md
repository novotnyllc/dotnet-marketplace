# fn-23: Hooks and MCP Integration

## Problem/Goal
Create hooks.json with file-type-specific matchers for smart defaults (format on .cs edit, restore on .csproj edit, validate on .xaml edit), configure MCP servers (Uno Platform, Microsoft Learn, Context7), and define plugin settings for configurable behavior.

## Acceptance Checks
- [ ] hooks.json created with PostToolUse hooks for .cs, .csproj, test files, .xaml
- [ ] .mcp.json configured for Uno Platform MCP, Microsoft Learn MCP, Context7 MCP
- [ ] Plugin settings defined for hook aggressiveness, MCP toggles
- [ ] Hooks fire only for relevant file types with smart filtering
- [ ] Hook concurrency controls implemented (debounce, cancellation, per-solution serialization)
- [ ] Stale-result suppression: diagnostics from runs started before latest edit are discarded
- [ ] Documentation for configuring hook behavior
- [ ] Cross-references to all relevant skills that hooks support

## Hook Concurrency Controls

Background hooks (dotnet format, dotnet restore) must handle rapid-fire edits reliably:

- **Debounce/coalesce**: Rapid edits to the same file debounce into a single format run (e.g., 500ms delay)
- **Cancellation**: New edit to same file cancels in-flight background format
- **Per-solution serialization**: Only one `dotnet restore` runs per solution at a time; subsequent requests queue
- **Stale-result suppression**: If a background run started before the latest edit timestamp, its results are discarded rather than surfaced to the agent

## Key Context
- Hooks should be helpful but not intrusive (configurable aggressiveness)
- File-type-specific matchers prevent hook spam
- MCP servers enhance skills with live documentation lookups
- Settings allow users to disable/tune hooks and MCP integration
