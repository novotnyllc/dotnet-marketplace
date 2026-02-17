# Hooks and MCP Server Guide

This guide explains the hooks and MCP server integration included with the dotnet-artisan plugin.

---

## Hooks Overview

The dotnet-artisan plugin includes two hook configurations that fire automatically during Claude Code sessions. Hooks provide smart defaults for .NET development workflows.

### PostToolUse Hook (Write|Edit)

A single hook entry with matcher `Write|Edit` dispatches to `scripts/hooks/post-edit-dotnet.sh`, which inspects the edited file's extension and takes the appropriate action:

| File Pattern | Behavior | Details |
|-------------|----------|---------|
| `*Tests.cs`, `*Test.cs` | Suggests running related tests | Outputs a `systemMessage` with a `dotnet test --filter` command targeting the modified test class |
| `*.cs` | Auto-formats with `dotnet format` | Runs `dotnet format --include <file>` asynchronously; reports results on the next turn |
| `*.csproj` | Suggests `dotnet restore` | Outputs a `systemMessage` recommending restore after project file changes |
| `*.xaml` | Validates XML well-formedness | Uses `xmllint` or falls back to `python3 xml.etree.ElementTree`; reports validation errors |

This hook runs asynchronously (`async: true`) with a 60-second timeout. It never blocks editing (always exits 0).

### SessionStart Hook (startup)

The `scripts/hooks/session-start-context.sh` hook fires once when a new Claude Code session starts. It detects whether the current directory is a .NET project and injects context:

- Counts `.sln`/`.slnx` solution files (up to 3 directories deep)
- Counts `.csproj` project files (up to 3 directories deep)
- Checks for `global.json`
- Extracts the target framework moniker (TFM) from the first `.csproj` found

If .NET project indicators are found, the hook outputs an `additionalContext` message such as:

> This is a .NET project (net10.0) with 3 project(s) in 1 solution(s).

This context helps Claude understand the project environment from the start of the session.

---

## How to Disable Hooks

Plugin hooks can be disabled in two ways:

1. **Disable all hooks globally**: Set `disableAllHooks: true` in your `.claude/settings.json` file. This disables hooks from all plugins, not just dotnet-artisan.

2. **Per-session control**: Use the `/hooks` menu within Claude Code to review and toggle individual hooks during a session. Note that hooks snapshot at session startup; changes via `/hooks` take effect immediately but do not persist across restarts.

To re-enable hooks after disabling, remove the `disableAllHooks` setting or toggle them back on via `/hooks`.

---

## MCP Server Configuration

The plugin configures the following MCP server in `.mcp.json`:

### Context7

| Property | Value |
|----------|-------|
| Transport | stdio |
| Command | `npx -y @upstash/context7-mcp@latest` |
| Purpose | Library documentation lookup covering Microsoft Learn, NuGet, and .NET ecosystem docs |

Context7 provides on-demand documentation lookups that enhance skill guidance with live, up-to-date library references.

**Version note**: The plugin currently uses `@latest` for initial ship. After stabilization, the version may be pinned (e.g., `@1.x.x`) to prevent upstream breaking changes.

### Requirements

- **Node.js** is required for MCP servers that use `npx`. Verify Node.js is installed by running `node --version` in your terminal. You can also check MCP server status with the `/mcp` command inside Claude Code.
- MCP servers start automatically when the plugin is enabled. After enabling or disabling the plugin, restart Claude Code to apply MCP server changes.

---

## Troubleshooting

### `dotnet` not found

The PostToolUse hook checks for `dotnet` in `PATH` before running `dotnet format`. If the .NET SDK is not installed or not in `PATH`, the hook degrades gracefully: it outputs a warning message and exits 0 without blocking.

**Fix**: Install the [.NET SDK](https://dot.net/download) and ensure `dotnet` is available in your shell's `PATH`.

### `npx` not available

MCP servers configured with `npx` (such as Context7) will not start if Node.js is not installed.

**Fix**: Install [Node.js](https://nodejs.org/) (LTS recommended). After installation, restart Claude Code so MCP servers can initialize.

### Hooks not firing

Hooks are snapshotted when a Claude Code session starts. If you install or update the plugin mid-session, hooks from the new version will not fire until the next session.

**Fix**: Restart Claude Code to pick up hook changes. Use `/hooks` to verify hooks are registered.

### `jq` not found

The hook scripts use `jq` to parse JSON input from stdin. If `jq` is not installed, the hook scripts will fail. The `post-edit-dotnet.sh` script requires `jq` for extracting the `file_path` from tool input.

**Fix**: Install `jq` via your system package manager:
- macOS: `brew install jq`
- Ubuntu/Debian: `sudo apt-get install jq`
- Windows: `winget install jqlang.jq`

### XAML validation unavailable

The XAML well-formedness check requires either `xmllint` or `python3`. If neither is available, the hook skips validation and reports a warning.

**Fix**: Install `libxml2-utils` (for `xmllint`) or ensure `python3` is in your `PATH`. On macOS, `python3` is typically pre-installed with Xcode Command Line Tools.
