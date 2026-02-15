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
Slimmed the ~230-line Channels section in dotnet-background-services SKILL.md to a ~48-line Channels Integration section with a condensed BackgroundTaskQueue + consumer worker example and cross-references to the new standalone [skill:dotnet-channels] skill. Removed Channel options table, multiple consumers, and drain pattern (all covered by the standalone skill).
## Evidence
- Commits: 4935b645233f7d3bc53571aa6ed531e975b49388
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: