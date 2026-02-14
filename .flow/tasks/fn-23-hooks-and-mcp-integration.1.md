# fn-23-hooks-and-mcp-integration.1 Create hooks.json with file-type-specific matchers

## Description
Populate `hooks/hooks.json` with PostToolUse and SessionStart hooks. Create `scripts/hooks/` directory and the corresponding bash scripts.

### hooks.json Structure

```json
{
  "description": "dotnet-artisan: smart defaults for .NET development",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/post-edit-dotnet.sh",
            "async": true,
            "timeout": 60
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hooks/session-start-context.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

**SessionStart matcher note:** Claude Code SessionStart events support matchers: `startup`, `resume`, `clear`, `compact`. Using `"startup"` ensures context injection fires only on new sessions. This is documented behavior per Claude Code hooks reference.

### Directory Setup

Create `scripts/hooks/` directory. Ensure both scripts are `chmod +x`.

### Hook Scripts

**`scripts/hooks/post-edit-dotnet.sh`** (async PostToolUse):
1. Read JSON from stdin into `INPUT` variable
2. Extract `tool_input.file_path` using `jq`
3. Switch on file extension (order matters -- test files before general .cs):
   - `*Tests.cs` / `*Test.cs`: Return suggestion to run related tests
   - `*.cs`: Run `dotnet format <file>` if `dotnet` is available. Return results.
   - `*.csproj`: Return suggestion to run `dotnet restore`.
   - `*.xaml`: Run XML well-formedness check (`xmllint --noout` or python `xml.etree`). Return result.
   - Other: `exit 0` silently.
4. Never exit 2. If tools are missing, exit 0 with a warning.

**`scripts/hooks/session-start-context.sh`** (sync SessionStart):
1. Check if current directory contains `.sln`, `.csproj`, or `global.json`
2. If found, extract TFM from first `.csproj`, output `additionalContext`
3. If not a .NET project, exit 0 silently

### Hook Output Format

Each script outputs JSON to stdout on exit 0:

```bash
# PostToolUse: success message
echo '{"systemMessage": "dotnet format applied to Program.cs"}'

# PostToolUse: tool missing
echo '{"systemMessage": "dotnet not found in PATH -- skipping format. Install .NET SDK to enable auto-formatting."}'

# PostToolUse: test suggestion
echo '{"systemMessage": "Test file modified: UserServiceTests.cs. Consider running: dotnet test --filter UserServiceTests"}'

# PostToolUse: restore suggestion
echo '{"systemMessage": "Project file modified. Consider running: dotnet restore"}'

# PostToolUse: XAML validation result
echo '{"systemMessage": "XAML validation: MainWindow.xaml is well-formed"}'

# SessionStart: context injection
echo '{"additionalContext": "This is a .NET 9 project (net9.0) with 3 projects in solution."}'
```

### Implementation Notes
- Scripts must be `chmod +x`
- Scripts use `jq` for JSON parsing (available on most systems; fallback to python if needed)
- All paths use `${CLAUDE_PLUGIN_ROOT}` in hooks.json
- The `post-edit-dotnet.sh` script is marked `async: true` because `dotnet format` can take 5-30 seconds
- Test file patterns: match `*Tests.cs` and `*Test.cs` before `*.cs` in case statement

## Acceptance
- [ ] `scripts/hooks/` directory exists
- [ ] `hooks/hooks.json` is valid JSON with `{"description": "...", "hooks": {...}}` wrapper
- [ ] PostToolUse matcher is `Write|Edit` (regex matching both tools)
- [ ] PostToolUse hook has `"async": true` and `"timeout": 60`
- [ ] SessionStart matcher is `"startup"` (fires only on new sessions)
- [ ] `post-edit-dotnet.sh` exists in `scripts/hooks/`, is executable (`chmod +x`)
- [ ] `session-start-context.sh` exists in `scripts/hooks/`, is executable (`chmod +x`)
- [ ] `post-edit-dotnet.sh` reads stdin JSON, extracts file_path, switches on extension
- [ ] `.cs` handler runs `dotnet format` (or warns if unavailable), outputs `systemMessage` JSON
- [ ] `*Tests.cs` / `*Test.cs` handler suggests running tests, outputs `systemMessage` JSON
- [ ] `.csproj` handler suggests `dotnet restore`, outputs `systemMessage` JSON
- [ ] `.xaml` handler checks XML well-formedness, outputs `systemMessage` JSON
- [ ] `session-start-context.sh` detects .NET project type and outputs `additionalContext` JSON
- [ ] No hook script ever exits with code 2
- [ ] SessionStart hook actually fires when tested in a Claude Code session
- [ ] `validate-marketplace.sh` passes (exit 0)

## Done summary
Created hooks.json with PostToolUse and SessionStart hooks, plus two executable bash scripts in scripts/hooks/.

**Deliverables:**
- `hooks/hooks.json`: PostToolUse (Write|Edit, async, 60s timeout) and SessionStart (startup, 10s timeout)
- `scripts/hooks/post-edit-dotnet.sh`: Dispatches by file extension — test files suggest running tests, .cs runs dotnet format, .csproj suggests restore, .xaml validates XML well-formedness
- `scripts/hooks/session-start-context.sh`: Detects .NET projects via .sln/.csproj/global.json, extracts TFM, injects additionalContext

**Key implementation details:**
- All scripts exit 0 (never exit 2) — advise only, never block
- XAML validation uses xmllint with python3 fallback (injection-safe via sys.argv)
- Session-start uses portable sed for TFM extraction (no PCRE dependency)
- All smoke tests pass for .cs, *Tests.cs, *Test.cs, .csproj, .xaml (valid+invalid), non-.NET files, empty input
- validate-marketplace.sh passes (0 errors, 0 warnings)
## Evidence
- Commits:
- Tests: Smoke tests: .cs format, *Tests.cs/*Test.cs test suggestion, .csproj restore, .xaml valid/invalid, non-.NET file silent exit, empty input silent exit, session-start non-.NET dir silent exit, session-start .NET dir context injection
- PRs: