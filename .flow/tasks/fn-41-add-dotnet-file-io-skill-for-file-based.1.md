# fn-41-add-dotnet-file-io-skill-for-file-based.1 Create dotnet-file-io SKILL.md

## Description
Author `skills/core-csharp/dotnet-file-io/SKILL.md` covering .NET file I/O patterns.

**Size:** M
**Files:** `skills/core-csharp/dotnet-file-io/SKILL.md` (new)

## Approach

- Follow existing skill structure at `skills/core-csharp/dotnet-io-pipelines/SKILL.md`
- Frontmatter: `name: dotnet-file-io`, `description` under 120 chars (target ~85 for budget headroom)
- Cross-refs via `[skill:skill-name]` syntax per CLAUDE.md convention

## Sections to cover

1. **FileStream** — `useAsync: true` / `FileOptions.Asynchronous` requirement; when async methods silently block without it
2. **RandomAccess API (.NET 6+)** — offset-based, thread-safe, stateless; eliminates FileStream position synchronization
3. **File convenience methods** — `File.ReadAllTextAsync`, `File.ReadLinesAsync`, when they're appropriate vs streaming
4. **FileSystemWatcher** — event handling, debouncing duplicate events, buffer overflow (default 8KB), hosted service integration, platform differences (inotify/FSEvents/ReadDirectoryChangesW)
5. **MemoryMappedFile** — persisted (large files) vs non-persisted (IPC); API usage only (GC implications → `[skill:dotnet-gc-memory]`)
6. **Path handling** — `Path.Combine` vs `Path.Join` security (Combine silently discards on absolute), cross-platform separators
7. **Secure temp files** — `Path.GetRandomFileName()` + `FileMode.CreateNew` instead of insecure `Path.GetTempFileName()`
8. **Cross-platform** — case sensitivity, `UnixFileMode` (.NET 7+), advisory vs mandatory locking
9. **Error handling** — `IOException` hierarchy, `HResult` codes, disk-full flush behavior
10. **Buffer sizing** — guidance from dotnet/runtime benchmarks (varies by file size)

## Key context

- Path.Combine security: silently drops first argument when second is rooted — Path.Join (.NET 8+) does not
- RandomAccess: no Seek state, thread-safe without synchronization — significant perf win for concurrent reads
- FileSystemWatcher fires duplicate events; debounce with timer pattern or Channel<T> throttle
- `Path.GetTempFileName()` creates zero-byte file with predictable name — use `Path.GetRandomFileName()` instead

## Out-of-scope cross-refs to include

- `[skill:dotnet-io-pipelines]` — PipeReader/PipeWriter, network I/O
- `[skill:dotnet-csharp-async-patterns]` — async/await fundamentals
- `[skill:dotnet-performance-patterns]` — Span/Memory/ArrayPool
- `[skill:dotnet-serialization]` — JSON, Protobuf serialization
- `[skill:dotnet-background-services]` — BackgroundService lifecycle
- `[skill:dotnet-channels]` — Channel<T> producer/consumer
- `[skill:dotnet-gc-memory]` — GC implications of memory-mapped backing arrays
- `[skill:dotnet-input-validation]` — IFormFile upload validation

## References

- .NET 6 File I/O improvements: https://devblogs.microsoft.com/dotnet/file-io-improvements-in-dotnet-6/
- RandomAccess API: https://learn.microsoft.com/en-us/dotnet/api/system.io.randomaccess
- FileSystemWatcher: https://learn.microsoft.com/en-us/dotnet/api/system.io.filesystemwatcher
- Memory-Mapped Files: https://learn.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files
- Path traversal prevention: https://owasp.org/www-community/attacks/Path_Traversal
## Acceptance
- [ ] `skills/core-csharp/dotnet-file-io/SKILL.md` exists with valid YAML frontmatter (`name`, `description`)
- [ ] `name` field matches directory name (`dotnet-file-io`)
- [ ] `description` under 120 characters (target ~85 chars)
- [ ] All 10 topic sections present (FileStream, RandomAccess, File convenience, FileSystemWatcher, MemoryMappedFile, Path handling, Secure temp files, Cross-platform, Error handling, Buffer sizing)
- [ ] Cross-references use `[skill:skill-name]` syntax and resolve to existing skills
- [ ] SKILL.md under 5,000 words
- [ ] No implementation code — patterns and guidance only
## Done summary
Created dotnet-file-io SKILL.md covering 10 .NET file I/O topics: FileStream async, RandomAccess API, File convenience methods, FileSystemWatcher with debouncing, MemoryMappedFile, path handling security, secure temp files, cross-platform considerations, error handling, and buffer sizing guidance. All cross-references resolve, description is 91 chars, and word count is 2,235.
## Evidence
- Commits: e3e774603e1faba1b3f4de30e3befe63e7f7fddd, 1ac4b215158ddcf415b8c38bdd54bc382e5c9314
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: