# fn-23: Hooks and MCP Integration

## Problem/Goal
Create hooks.json with file-type-specific matchers for smart defaults (format on .cs edit, restore on .csproj edit, test suggestion on test file edit, validate on .xaml edit), configure MCP servers (Context7 for library docs), and document hook behavior for plugin users.

## Dependencies
- **Hard**: fn-2 (Plugin Skeleton) — provides `hooks/hooks.json` and `.mcp.json` stubs, `plugin.json` references
- **Soft**: fn-12 (Blazor Skills), fn-13 (Uno Platform Skills) — MCP servers enhance these skills with live docs

## Scope

**In scope:**
- `hooks/hooks.json` with PostToolUse hooks for `.cs`, `.csproj`, `.xaml`, and test file matchers
- `.mcp.json` configured for Context7 MCP (covers Microsoft Learn, NuGet, and general .NET ecosystem docs)
- Hook scripts in `scripts/hooks/` directory (bash, invoked by hooks.json)
- Documentation for configuring hook behavior (disable, troubleshoot)

**Out of scope:**
- Debounce/cancellation/per-solution serialization (these are Claude Code runtime features, not plugin-controllable; hooks run synchronously or async but the plugin cannot implement its own debounce logic within the hook system)
- Stale-result suppression (same reason: not controllable at plugin level)
- Plugin settings system (Claude Code plugins do not have a user-configurable settings mechanism; users control hooks via `disableAllHooks` or removing hook entries)
- PreToolUse hooks for blocking (not appropriate for a best-practices plugin; too intrusive)

## Hooks Architecture

### Hook Event Selection

The plugin uses these hook events:

| Event | Matcher | Purpose | Type | Async |
|-------|---------|---------|------|-------|
| `PostToolUse` | `Write\|Edit` | Single script dispatches by file extension: `.cs` format, `.csproj` restore suggestion, `.xaml` validation, `*Tests.cs` test suggestion | `command` | `true` |
| `SessionStart` | `startup` | Detect .NET SDK version and project type, inject context | `command` | `false` |

**Note on PostToolUse consolidation:** A single hook entry with matcher `Write|Edit` routes to one script (`post-edit-dotnet.sh`) that dispatches internally by file extension. This avoids multiple hook entries with the same matcher and keeps dispatch logic in one place.

**Note on SessionStart matcher:** Claude Code SessionStart events support matchers: `startup`, `resume`, `clear`, `compact`. Using `"startup"` ensures the context hook fires only on new sessions, not on resume/clear/compact (which already have context).

### Hook Script Design

All hook scripts:
- Live in `scripts/hooks/` directory (must be created by task 1)
- Are referenced via `${CLAUDE_PLUGIN_ROOT}/scripts/hooks/<name>.sh`
- Read JSON from stdin, extract relevant fields with `jq`
- Use file extension checks to filter (e.g., only act on `.cs` files)
- Exit 0 for success (stdout shown in verbose mode)
- Exit 0 with JSON `systemMessage` or `additionalContext` for feedback
- Never exit 2 (plugin hooks should advise, not block)

### Hook Output Format

Scripts output JSON to stdout on exit 0:

```json
// PostToolUse: feedback message to Claude
{"systemMessage": "dotnet format applied to Program.cs"}

// PostToolUse: tool missing warning
{"systemMessage": "dotnet not found in PATH -- skipping format. Install .NET SDK to enable auto-formatting."}

// SessionStart: context injection
{"additionalContext": "This is a .NET 9 project (net9.0) with 3 projects in solution."}
```

### File Extension Filtering

Since Claude Code matchers filter on tool name (not file path), each hook script must extract `file_path` from `tool_input` and check the extension:

```bash
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
case "$FILE_PATH" in
  *Tests.cs|*Test.cs) # suggest running tests ;;
  *.cs) # run dotnet format ;;
  *.csproj) # suggest dotnet restore ;;
  *.xaml) # check XML well-formedness ;;
  *) exit 0 ;; # ignore other files
esac
```

### Async vs Sync

- `dotnet format` hook: `async: true` (runs in background, takes 5-30s, reports results on next turn)
- `dotnet restore` suggestion: handled within async script (fast stdout)
- XAML validation: handled within async script (fast XML check)
- Test suggestion: handled within async script (fast stdout)
- SessionStart context: sync (fast, reads files only)

## MCP Server Architecture

### Server Selection

| Server | Transport | Purpose | Command |
|--------|-----------|---------|---------|
| Context7 | stdio | Library documentation lookup (covers Microsoft Learn, NuGet, .NET ecosystem) | `npx -y @upstash/context7-mcp@latest` |

### Version Stability Note

Context7 uses `@latest` for initial ship. After stabilization, evaluate pinning to a specific version (e.g., `@1.x.x`) to prevent upstream breaking changes. Document this as a follow-up item.

### Environment Variable Expansion

`.mcp.json` uses `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths where needed. API keys use `${VAR_NAME}` syntax for user-provided credentials.

### Server Lifecycle

Plugin MCP servers start automatically when plugin is enabled. Users must restart Claude Code after enabling/disabling plugin to apply MCP server changes.

## Task Decomposition

| Task | Deliverables | Files touched | Dependencies |
|------|-------------|---------------|--------------|
| fn-23.1 | `hooks/hooks.json`, hook scripts in `scripts/hooks/` | `hooks/hooks.json` (edit), `scripts/hooks/post-edit-dotnet.sh` (new), `scripts/hooks/session-start-context.sh` (new) | None |
| fn-23.2 | `.mcp.json` with MCP server configs | `.mcp.json` (edit) | None |
| fn-23.3 | Documentation, validation updates | `scripts/validate-marketplace.sh` (edit) | fn-23.1, fn-23.2 |

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| `dotnet format` not installed on user machine | Hook script fails silently | Script checks for `dotnet` command availability, exits 0 with warning if missing |
| MCP servers require npx/node not available | MCP tools unavailable | Document Node.js requirement; servers degrade gracefully (Claude works without them) |
| Hook scripts slow down editing workflow | User frustration | Use `async: true` for slow operations; fast checks stay sync |
| XAML validation false positives | Noisy output | Only check XML well-formedness, not schema validation |
| Context7 `@latest` upstream breakage | MCP tools stop working | Pin version after stabilization (follow-up) |

## Acceptance Checks
- [ ] `hooks/hooks.json` contains PostToolUse hook with `Write|Edit` matcher (single entry, internal dispatch)
- [ ] `hooks/hooks.json` contains SessionStart hook with `startup` matcher
- [ ] Hook scripts in `scripts/hooks/` are executable, read stdin JSON, filter by file extension
- [ ] `post-edit-dotnet.sh` handles `.cs` (format), `.csproj` (restore), `.xaml` (validation), `*Tests.cs` (test suggestion)
- [ ] `dotnet format` hook uses `async: true` and reports results via `systemMessage`
- [ ] `.mcp.json` configured with Context7 MCP server
- [ ] SessionStart hook detects .NET project type and returns `additionalContext`
- [ ] All hook scripts handle missing tools gracefully (exit 0 with warning, never exit 2)
- [ ] Hook output follows documented JSON format (`systemMessage` or `additionalContext`)
- [ ] `validate-marketplace.sh` passes (exit 0) including new hook/MCP validation checks
- [ ] Hook scripts use `${CLAUDE_PLUGIN_ROOT}` for portable paths
- [ ] Task 3 depends on tasks 1 and 2

## Key Context
- Claude Code hooks.json plugin format requires `{"hooks": {...}}` wrapper (not bare events)
- Optional `"description"` field at top level for plugin hooks
- Matchers are regex on tool name, not file path -- file filtering must happen in script
- SessionStart matchers filter on how session started: `startup`, `resume`, `clear`, `compact`
- Plugin hooks merge with user/project hooks when plugin is enabled
- Hooks snapshot at session start; mid-session edits require `/hooks` menu review
- `${CLAUDE_PLUGIN_ROOT}` is available in hook command strings
- Inline `mcpServers` in plugin.json has a known parsing bug -- use `.mcp.json` file reference
