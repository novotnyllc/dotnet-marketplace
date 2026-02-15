# fn-33-systemthreadingchannels-skill.1 Create standalone dotnet-channels skill

## Description
Create skills/core-csharp/dotnet-channels/SKILL.md as a standalone deep skill for System.Threading.Channels. Extract and expand coverage currently embedded in dotnet-background-services (lines 192-424).

**Size:** M
**Files:** skills/core-csharp/dotnet-channels/SKILL.md, .claude-plugin/plugin.json

## Approach
- Frontmatter: `name: dotnet-channels`, `description: "WHEN using producer/consumer queues. Channel<T>, bounded/unbounded, backpressure, drain patterns"` (~95 chars)
- Channel<T> fundamentals: bounded vs unbounded creation
- BoundedChannelFullMode: Wait, DropNewest, DropOldest, DropWrite with use cases
- `itemDropped` callback for drop modes (.NET 7+)
- Producer/consumer patterns: single and multiple readers/writers
- Cancellation and graceful shutdown (drain patterns)
- Author new IAsyncEnumerable section (not present in source material): cover `ReadAllAsync()`, `await foreach`, integration with LINQ async operators
- Performance: SingleReader/SingleWriter creation flags, TryWrite/TryRead fast paths, WaitToReadAsync+TryRead consumer pattern, bounded channel memory behavior
- Cross-ref to [skill:dotnet-background-services] and [skill:dotnet-csharp-async-patterns]
- Add `skills/core-csharp/dotnet-channels` to the `skills` array in `.claude-plugin/plugin.json`
## Acceptance
- [ ] Full Channel<T> coverage (bounded/unbounded)
- [ ] All BoundedChannelFullMode modes with use cases
- [ ] `itemDropped` callback (.NET 7+) covered
- [ ] Producer/consumer patterns (single and multi reader/writer)
- [ ] IAsyncEnumerable integration (new content: ReadAllAsync, await foreach)
- [ ] Performance section: SingleReader/SingleWriter, TryWrite/TryRead, WaitToReadAsync+TryRead
- [ ] Graceful shutdown/drain
- [ ] Cross-refs correct
- [ ] Registered in plugin.json
- [ ] Description under 120 chars, budget verified
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
