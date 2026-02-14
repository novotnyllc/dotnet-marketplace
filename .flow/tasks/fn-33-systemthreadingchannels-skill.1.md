# fn-33-systemthreadingchannels-skill.1 Create standalone dotnet-channels skill

## Description
Create skills/core-csharp/dotnet-channels/SKILL.md as a standalone deep skill for System.Threading.Channels. Extract and expand coverage currently embedded in dotnet-background-services (lines 192-424).

**Size:** M
**Files:** skills/core-csharp/dotnet-channels/SKILL.md, .claude-plugin/plugin.json

## Approach
- Channel<T> fundamentals: bounded vs unbounded creation
- BoundedChannelFullMode: Wait, DropNewest, DropOldest, DropWrite with use cases
- Producer/consumer patterns: single and multiple readers/writers
- Cancellation and graceful shutdown (drain patterns)
- IAsyncEnumerable integration: ChannelReader.ReadAllAsync()
- Performance: SingleReader/SingleWriter creation options
- Cross-ref to [skill:dotnet-background-services] and [skill:dotnet-csharp-async-patterns]
## Acceptance
- [ ] Full Channel<T> coverage
- [ ] All BoundedChannelFullMode modes with use cases
- [ ] Producer/consumer patterns (single and multi reader/writer)
- [ ] IAsyncEnumerable integration
- [ ] Performance optimizations
- [ ] Graceful shutdown/drain
- [ ] Cross-refs correct
- [ ] Registered in plugin.json
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
