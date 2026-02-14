# fn-33-systemthreadingchannels-skill.2 Slim Channels section in background-services and add cross-ref

## Description
Slim the Channels section in skills/architecture/dotnet-background-services/SKILL.md (lines 192-424) to a brief summary with cross-reference to the new standalone [skill:dotnet-channels] skill.

**Size:** S
**Files:** skills/architecture/dotnet-background-services/SKILL.md

## Approach
- Replace ~230-line Channels section with brief "Channels Integration" subsection (~20-30 lines)
- Keep only BackgroundService + Channel integration pattern
- Add [skill:dotnet-channels] cross-ref for full guidance
- Preserve the skill focus on BackgroundService, IHostedService, IHostedLifecycleService
## Acceptance
- [ ] Channels section reduced to ~20-30 lines
- [ ] Cross-ref to [skill:dotnet-channels] added
- [ ] BackgroundService + Channel integration pattern preserved
- [ ] No broken cross-references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
