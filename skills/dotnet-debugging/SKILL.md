---
name: dotnet-debugging
description: Debugs Windows applications using WinDbg and crash dump analysis. Covers MCP server integration, live process attach, dump file triage, crash analysis, hang detection, high-CPU diagnosis, memory leak investigation, kernel debugging, symbol configuration, scenario command packs, diagnostic report generation, and SOS extension workflows for .NET runtime inspection.
license: MIT
user-invocable: true
---

# dotnet-debugging

## Overview

Windows user-mode debugging using WinDbg MCP tools. Applicable to any Windows application -- native, managed (.NET/CLR), or mixed-mode. Guides investigation of crash dumps, application hangs, high CPU, and memory pressure through structured command packs and report templates.

**Platform:** Windows only.

## Scope

- Crash dump analysis (.dmp files) for any Windows process (native, .NET, or mixed-mode)
- Live process attach via cdb debug server
- Hang and deadlock diagnosis (thread analysis, lock detection)
- High CPU triage (runaway thread identification)
- Memory pressure and leak investigation via native heap analysis
- Kernel dump triage (BSOD / bugcheck analysis)
- COM/RPC wait chain and UI message pump analysis
- Structured diagnostic reports with stack evidence

## Out of scope

- .NET SDK diagnostic tools (dotnet-counters, dotnet-trace, dotnet-dump) -- see [skill:dotnet-tooling] (read `references/profiling.md`)
- GC tuning and managed memory optimization -- see [skill:dotnet-tooling] (read `references/gc-memory.md`)
- Performance benchmarking and regression detection -- see [skill:dotnet-testing] (read `references/benchmarkdotnet.md`)
- Application performance architecture patterns -- see [skill:dotnet-tooling] (read `references/performance-patterns.md`)
- Application-level logging -- see [skill:dotnet-devops] (read `references/structured-logging.md`)
- Unit/integration test debugging -- see [skill:dotnet-testing]

## MCP Tool Contract

Use these `mcp-windbg` operations:

| Operation | Purpose |
|-----------|---------|
| `mcp_mcp-windbg_open_windbg_remote` | Attach to a live debug server |
| `mcp_mcp-windbg_open_windbg_dump` | Open a saved dump file |
| `mcp_mcp-windbg_run_windbg_cmd` | Execute debugger commands |
| `mcp_mcp-windbg_close_windbg_remote` | Detach from live session |
| `mcp_mcp-windbg_close_windbg_dump` | Close dump session |

## Diagnostic Workflow

### Preflight: Symbols

Before any analysis, configure symbols to get meaningful stacks:

1. Set Microsoft symbol server: `.symfix` (sets `srv*` to Microsoft public symbols)
2. Add application symbols: `.sympath+ C:\path\to\your\pdbs`
3. Reload modules: `.reload /f`
4. Verify: `lm` (list modules -- check for "deferred" vs "loaded" status)

Without correct symbols, stacks show raw addresses instead of function names.

### Crash Dump Analysis

1. Open dump: `mcp_mcp-windbg_open_windbg_dump` with dump file path
2. Load SOS for managed code: `.loadby sos clr` (Framework) or `.loadby sos coreclr` (.NET Core)
3. Get exception context: `!pe` (print exception), `!analyze -v` (automatic analysis)
4. Inspect threads: `~*e !clrstack` (all managed stacks), `!threads` (thread list)
5. Check managed heap: `!dumpheap -stat` (heap summary), `!gcroot <addr>` (object roots)

### Hang / Deadlock Diagnosis

1. Attach or open dump, load SOS
2. List all threads: `!threads`, identify waiting threads with `!syncblk` (sync block table)
3. Detect deadlocks: `!dlk` (SOS deadlock detection)
4. Inspect thread stacks: `~Ns !clrstack` for specific thread N
5. Check wait reasons: `!waitchain` for COM/RPC chains, `!mda` for MDA diagnostics

### High CPU Triage

1. Attach to live process or collect multiple dumps 10-30 seconds apart
2. Use `!runaway` to identify threads consuming the most CPU time
3. Inspect hot thread stacks: `~Ns kb` (native stack), `~Ns !clrstack` (managed stack)
4. Look for tight loops, blocked finalizer threads, or excessive GC

### Memory Pressure Investigation

1. Open dump, load SOS
2. Managed heap: `!dumpheap -stat` (type statistics), `!dumpheap -type <TypeName>` (filter)
3. Find leaked objects: `!gcroot <address>` (trace GC roots to pinned or static references)
4. Native heap: `!heap -s` (heap summary), `!heap -l` (leak detection)
5. LOH fragmentation: `!eeheap -gc` (GC heap segments)

## Report Template

```
## Diagnostic Report

**Symptom:** [crash/hang/high-cpu/memory-leak]
**Process:** [name, PID, bitness]
**Dump type:** [full/mini/live-attach]

### Evidence
- Exception: [type and message, or N/A]
- Faulting thread: [ID, managed/native, stack summary]
- Key stacks: [condensed callstack with module!function]

### Root Cause
[Concise analysis backed by stack/heap evidence]

### Recommendations
[Numbered action items]
```

## Guardrails

- Do not claim certainty without callee-side evidence
- Do not call it a deadlock unless lock/wait evidence supports it
- Preserve user privacy: do not include secrets from environment blocks in reports

Cross-references: [skill:dotnet-tooling] for .NET SDK diagnostic tools (`references/profiling.md`) and GC/memory tuning (`references/gc-memory.md`).

## Companion Files

- `references/mcp-setup.md` -- MCP server configuration
- `references/access-mcp.md` -- MCP access patterns
- `references/common-patterns.md` -- Common debugging patterns
- `references/dump-workflow.md` -- Dump file analysis workflow
- `references/live-attach.md` -- Live process attach guide
- `references/symbols.md` -- Symbol configuration
- `references/sanity-check.md` -- Sanity check procedures
- `references/scenario-command-packs.md` -- Scenario command packs
- `references/capture-playbooks.md` -- Capture playbooks
- `references/report-template.md` -- Diagnostic report template
- `references/task-crash.md` -- Crash triage
- `references/task-hang.md` -- Hang triage
- `references/task-high-cpu.md` -- High-CPU triage
- `references/task-memory.md` -- Memory leak triage
- `references/task-kernel.md` -- Kernel debugging
- `references/task-unknown.md` -- Unknown issue triage

## References

- [WinDbg MCP](https://github.com/anthropics/windbg-mcp) -- MCP server for WinDbg integration
- [WinDbg Documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) -- Microsoft debugger documentation
