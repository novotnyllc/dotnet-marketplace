# Add dotnet-file-io Skill

## Overview

Create a new `dotnet-file-io` skill covering .NET file I/O patterns: FileStream, RandomAccess, FileSystemWatcher, MemoryMappedFile, path handling, temp files, and cross-platform gotchas. Place in `skills/core-csharp/` alongside the existing `dotnet-io-pipelines` (network I/O sibling).

## Scope

**In scope:**
- FileStream construction with `useAsync`/`FileOptions.Asynchronous`
- RandomAccess API (.NET 6+) for offset-based thread-safe I/O
- File convenience methods (`File.ReadAllTextAsync`, `File.ReadLinesAsync`, etc.)
- FileSystemWatcher: event handling, debouncing, buffer overflow, hosted service integration
- MemoryMappedFile: persisted (large files) and non-persisted (IPC)
- Path handling: `Path.Combine` vs `Path.Join` security, cross-platform separators
- Secure temp files: `Path.GetRandomFileName` + `FileMode.CreateNew`
- Cross-platform: case sensitivity, UnixFileMode (.NET 7+), advisory vs mandatory locking
- Error handling: IOException hierarchy, HResult codes, disk-full flush behavior
- Buffer sizing guidance (from dotnet/runtime benchmarks)

**Out of scope (with cross-refs):**
- `System.IO.Pipelines` (PipeReader/PipeWriter) → `[skill:dotnet-io-pipelines]`
- Async/await fundamentals → `[skill:dotnet-csharp-async-patterns]`
- Span/Memory/ArrayPool deep patterns → `[skill:dotnet-performance-patterns]`
- Serialization (JSON, Protobuf) → `[skill:dotnet-serialization]`
- BackgroundService lifecycle → `[skill:dotnet-background-services]`
- Channel<T> producer/consumer → `[skill:dotnet-channels]`
- GC implications of memory-mapped backing arrays → `[skill:dotnet-gc-memory]`
- File upload validation (IFormFile) → `[skill:dotnet-input-validation]`
- System.IO.Compression → out of scope (not covered by any existing skill)

**Boundary decisions:**
- `PipeReader.Create(FileStream)` ownership → dotnet-io-pipelines (it wraps Pipe APIs)
- `MemoryMappedFile` API usage → here; GC/POH implications → dotnet-gc-memory
- `System.IO.Abstractions` for testability → brief mention with cross-ref to testing, not full API coverage
- FileSystemWatcher → kept here (essential patterns + agent gotchas, not a standalone skill)

## Quick commands
```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh && python3 scripts/generate_dist.py --strict && python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] `skills/core-csharp/dotnet-file-io/SKILL.md` created with valid frontmatter
- [ ] Description under 120 chars (target ~85 chars for budget headroom)
- [ ] Cross-references resolve to existing skills
- [ ] Skill registered in `.claude-plugin/plugin.json`
- [ ] `--projected-skills` updated in `scripts/validate-skills.sh`
- [ ] `dotnet-advisor` has catalog entry + routing line for file I/O
- [ ] README.md and AGENTS.md skill counts updated
- [ ] Bidirectional cross-refs added to `dotnet-io-pipelines` and `dotnet-gc-memory`
- [ ] All four validation commands pass
- [ ] SKILL.md under 5,000 words

## References
- .NET 6 File I/O improvements: https://devblogs.microsoft.com/dotnet/file-io-improvements-in-dotnet-6/
- FileStream performance guidelines: https://github.com/dotnet/runtime/discussions/74405
- Microsoft Learn File/Stream I/O: https://learn.microsoft.com/en-us/dotnet/standard/io/
- RandomAccess API: https://learn.microsoft.com/en-us/dotnet/api/system.io.randomaccess
- FileSystemWatcher: https://learn.microsoft.com/en-us/dotnet/api/system.io.filesystemwatcher
- Memory-Mapped Files: https://learn.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files
- Path traversal prevention: https://owasp.org/www-community/attacks/Path_Traversal
- Secure temp files: https://docs.datadoghq.com/security/code_security/static_analysis/static_analysis_rules/csharp-security/unsafe-temp-file/
