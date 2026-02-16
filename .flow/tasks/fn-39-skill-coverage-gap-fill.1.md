# fn-39-skill-coverage-gap-fill.1 Create dotnet-messaging-patterns and dotnet-io-pipelines skills

## Description
Create two new skills covering the highest-priority messaging and IO gaps:

1. **dotnet-messaging-patterns** (`skills/architecture/dotnet-messaging-patterns/SKILL.md`) — Durable messaging patterns for .NET (pub/sub, competing consumers, dead-letter queues, saga/process manager, delivery guarantees). Covers Azure Service Bus, RabbitMQ, and MassTransit.
2. **dotnet-io-pipelines** (`skills/core-csharp/dotnet-io-pipelines/SKILL.md`) — System.IO.Pipelines for high-performance network I/O (PipeReader, PipeWriter, backpressure, protocol parsers, Kestrel integration).

**Size:** M
**Files:** `skills/architecture/dotnet-messaging-patterns/SKILL.md`, `skills/core-csharp/dotnet-io-pipelines/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Each description under 120 characters (target ~100 chars for budget headroom)
- dotnet-messaging-patterns cross-refs: `[skill:dotnet-background-services]`, `[skill:dotnet-resilience]`, `[skill:dotnet-serialization]`, `[skill:dotnet-channels]`
- dotnet-io-pipelines cross-refs: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-performance-patterns]`
- dotnet-io-pipelines should reference Toub's IO.Pipelines blog post as a knowledge source
- Use latest stable package versions for all NuGet references
- No fn-N spec references in content
- Both skills are self-contained — no external dependency
## Acceptance
- [ ] dotnet-messaging-patterns SKILL.md created with frontmatter
- [ ] Covers pub/sub, competing consumers, DLQ, sagas, delivery guarantees
- [ ] References Azure Service Bus, RabbitMQ, MassTransit
- [ ] dotnet-io-pipelines SKILL.md created with frontmatter
- [ ] Covers PipeReader/PipeWriter, backpressure, protocol parsers
- [ ] Cross-references to related skills use `[skill:...]` syntax
- [ ] Both descriptions under 120 characters
- [ ] Both SKILL.md files under 5,000 words
- [ ] No fn-N spec references in content
- [ ] Package versions are latest stable
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
