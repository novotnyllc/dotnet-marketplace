# Symbols

## Quick Setup
Run in WinDbg session:

```text
.symfix
.reload
```

For Microsoft symbol server with local cache:

```text
.sympath srv*C:\symbols*https://msdl.microsoft.com/download/symbols
.reload /f
```

## Verify Symbols
- `lm` to inspect module load status.
- `lmv m <module>` to confirm symbol details for a module.
- If stacks show many `Unknown`/raw addresses, symbols are likely incomplete.

## Troubleshooting
- Ensure network access to `msdl.microsoft.com`.
- Use a writable local cache directory.
- Re-run `.reload /f` after changing symbol path.
- If only one module is problematic, use `lmv m <module>` first.
