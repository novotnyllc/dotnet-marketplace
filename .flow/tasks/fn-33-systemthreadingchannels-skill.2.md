# fn-33-systemthreadingchannels-skill.2 Slim Channels section in background-services and add cross-ref

## Description
Slim the Channels section in skills/architecture/dotnet-background-services/SKILL.md (lines 192-424) to a brief summary with cross-reference to the new standalone [skill:dotnet-channels] skill.

**Size:** S
**Files:** skills/architecture/dotnet-background-services/SKILL.md

## Approach
- Replace ~230-line Channels section with brief "Channels Integration" subsection (~15-20 lines)
- Keep: condensed BackgroundTaskQueue + consumer worker pattern (~15 lines of code) as the integration example
- Remove: Channel options table, multiple consumers section, drain pattern (all moved to [skill:dotnet-channels])
- Add cross-ref paragraph at top of section: `See [skill:dotnet-channels] for comprehensive Channel<T> guidance`
- Preserve the skill focus on BackgroundService, IHostedService, IHostedLifecycleService
## Acceptance
- [ ] Channels section reduced to ~15-20 lines with integration example
- [ ] Cross-ref to [skill:dotnet-channels] added
- [ ] BackgroundTaskQueue + consumer worker pattern preserved as summary
- [ ] Channel options table, multiple consumers, drain pattern removed (covered by new skill)
- [ ] No broken cross-references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
