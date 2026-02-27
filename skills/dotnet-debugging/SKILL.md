---
name: dotnet-debugging
description: Debugs Windows applications using WinDbg and crash dump analysis including MCP server integration, live process attach, dump file triage, hang detection, high-CPU diagnosis, memory leak investigation, kernel debugging, symbol configuration, scenario command packs, diagnostic report generation, and SOS extension workflows for .NET runtime inspection.
license: MIT
user-invocable: true
---

# dotnet-debugging

## Overview

Windows user-mode debugging using WinDbg MCP tools. Applicable to any Windows application -- native, managed (.NET/CLR), or mixed-mode. Guides investigation of crash dumps, application hangs, high CPU, and memory pressure through structured command packs and report templates.

**Platform:** Windows only.

## Routing Table

| Topic | Keywords | Description | Companion File |
|-------|----------|-------------|----------------|
| MCP setup | MCP server, WinDbg, configuration | MCP server configuration | references/mcp-setup.md |
| MCP access | MCP access, tool IDs, dispatch | MCP access patterns | references/access-mcp.md |
| Common patterns | debug patterns, SOS, CLR | Common debugging patterns | references/common-patterns.md |
| Dump workflow | dump file, .dmp, crash dump | Dump file analysis workflow | references/dump-workflow.md |
| Live attach | live process, cdb, attach | Live process attach guide | references/live-attach.md |
| Symbols | symbol server, .symfix, PDB | Symbol configuration | references/symbols.md |
| Sanity check | verify, environment, baseline | Sanity check procedures | references/sanity-check.md |
| Scenario packs | command pack, triage, workflow | Scenario command packs | references/scenario-command-packs.md |
| Capture playbooks | capture, procdump, triggers | Capture playbooks | references/capture-playbooks.md |
| Report template | diagnostic report, evidence | Diagnostic report template | references/report-template.md |
| Crash triage | crash, exception, access violation | Crash triage | references/task-crash.md |
| Hang triage | hang, deadlock, freeze | Hang triage | references/task-hang.md |
| High-CPU triage | high CPU, runaway thread, spin | High-CPU triage | references/task-high-cpu.md |
| Memory triage | memory leak, heap, LOH | Memory leak triage | references/task-memory.md |
| Kernel debugging | kernel, BSOD, bugcheck | Kernel debugging | references/task-kernel.md |
| Unknown triage | unknown issue, general triage | Unknown issue triage | references/task-unknown.md |

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

- .NET SDK diagnostic tools (dotnet-counters, dotnet-trace, dotnet-dump) -> [skill:dotnet-tooling]
- GC tuning and managed memory optimization -> [skill:dotnet-tooling]
- Performance benchmarking and regression detection -> [skill:dotnet-testing]
- Application performance architecture patterns -> [skill:dotnet-tooling]
- Application-level logging -> [skill:dotnet-devops]
- Unit/integration test debugging -> [skill:dotnet-testing]

## MCP Tool Contract

These tool IDs are the WinDbg MCP server's exported names (single-underscore `mcp_...`), not the `mcp__...` dispatch prefix used by some hosts.

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

## References

- [WinDbg MCP](https://github.com/anthropics/windbg-mcp) -- MCP server for WinDbg integration
- [WinDbg Documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) -- Microsoft debugger documentation
