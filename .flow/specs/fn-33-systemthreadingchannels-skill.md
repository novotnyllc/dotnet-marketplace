# System.Threading.Channels Skill

## Overview
Extract and expand the Channels coverage currently embedded in `dotnet-background-services` (lines 192-424) into a standalone deep skill. The existing coverage is decent but buried; it deserves first-class treatment as a standalone skill.

## Scope
- Create `skills/core-csharp/dotnet-channels/SKILL.md` as a standalone skill
- Cover: Channel<T>, bounded vs unbounded, BoundedChannelFullMode (Wait, DropNewest, DropOldest, DropWrite), backpressure patterns
- `itemDropped` callback for drop modes (.NET 7+)
- Producer/consumer patterns, multiple readers/writers, cancellation
- Channel as async enumerable (IAsyncEnumerable integration via `ChannelReader.ReadAllAsync()`) — net-new content, not present in source material
- Integration with BackgroundService (cross-ref to `[skill:dotnet-background-services]`)
- Performance considerations: SingleReader/SingleWriter flags, TryWrite/TryRead fast paths, WaitToReadAsync+TryRead consumer pattern, bounded channel memory behavior
- Graceful shutdown and drain patterns
- Remove or slim the Channels section from background-services to avoid duplication (replace with cross-ref)

## Quick commands
```bash
./scripts/validate-skills.sh && \
./scripts/validate-marketplace.sh && \
python3 scripts/generate_dist.py --strict && \
python3 scripts/validate_cross_agent.py
```

## Acceptance
- [ ] Standalone `dotnet-channels` skill created with full Channel<T> coverage
- [ ] Bounded/unbounded patterns, BoundedChannelFullMode modes documented
- [ ] `itemDropped` callback for drop modes (.NET 7+)
- [ ] Producer/consumer, multiple readers/writers, IAsyncEnumerable patterns
- [ ] Performance section covering SingleReader/SingleWriter, TryWrite/TryRead fast paths, WaitToReadAsync+TryRead pattern
- [ ] Graceful shutdown/drain patterns
- [ ] Cross-ref to `[skill:dotnet-background-services]` for hosted service integration
- [ ] Background-services skill updated to cross-ref Channels instead of inline coverage
- [ ] Registered in `plugin.json` skills array
- [ ] Skill description under 120 characters, budget verified via validation
- [ ] No fn-N spec references
- [ ] Budget constraint respected (all four validation commands pass)

## References
- `skills/architecture/dotnet-background-services/SKILL.md:192-424` — current Channels coverage
- System.Threading.Channels API docs
