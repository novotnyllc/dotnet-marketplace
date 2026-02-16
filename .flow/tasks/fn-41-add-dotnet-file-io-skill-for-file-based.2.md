# fn-41-add-dotnet-file-io-skill-for-file-based.2 Integrate dotnet-file-io into plugin registry and routing

## Description
Register `dotnet-file-io` in the plugin manifest, update routing, counts, and add bidirectional cross-references.

**Size:** S
**Files:**
- `.claude-plugin/plugin.json` — add skill path to `skills` array
- `scripts/validate-skills.sh` line ~43 — bump `--projected-skills` from 121 → 122
- `skills/foundation/dotnet-advisor/SKILL.md` — add catalog entry (~line 36 area) and routing line (~line 193 area) for file I/O queries
- `README.md` — update skill counts at lines 11, 34, and Mermaid diagram (99-122 area)
- `AGENTS.md` — update total count (line 7) and Core C# count (line 12, 14→15)
- `skills/core-csharp/dotnet-io-pipelines/SKILL.md` — add cross-ref to `[skill:dotnet-file-io]`
- `skills/performance/dotnet-gc-memory/SKILL.md` — add cross-ref to `[skill:dotnet-file-io]`
- `CHANGELOG.md` — add entry for new skill

## Approach

- Follow the pattern from recent skill additions (e.g., fn-40 fleet review findings)
- plugin.json: insert `skills/core-csharp/dotnet-file-io` in alphabetical position within core-csharp block
- dotnet-advisor: catalog entry pattern at `skills/foundation/dotnet-advisor/SKILL.md` — match existing format
- Routing line: add pattern matching for file I/O queries (FileStream, RandomAccess, FileSystemWatcher, MemoryMappedFile, Path handling)
- Bidirectional cross-refs: add `[skill:dotnet-file-io]` to io-pipelines and gc-memory where they mention related concepts
- Run all 4 validation commands to confirm everything resolves

## Key context

- Budget currently at ~11,948 chars; adding ~85 chars puts us at ~12,033 — just over WARN threshold but well under 15,000 hard limit
- The `--projected-skills` flag in validate-skills.sh must match the actual count or validation fails
## Acceptance
- [ ] Skill path registered in `.claude-plugin/plugin.json` skills array
- [ ] `--projected-skills` bumped to 122 in `scripts/validate-skills.sh`
- [ ] `dotnet-advisor` has catalog entry for dotnet-file-io
- [ ] `dotnet-advisor` has routing line for file I/O queries
- [ ] README.md skill counts updated (121 → 122)
- [ ] AGENTS.md total and Core C# counts updated
- [ ] `dotnet-io-pipelines` SKILL.md has cross-ref to `[skill:dotnet-file-io]`
- [ ] `dotnet-gc-memory` SKILL.md has cross-ref to `[skill:dotnet-file-io]`
- [ ] CHANGELOG.md has entry for new skill
- [ ] All four validation commands pass: `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh && python3 scripts/generate_dist.py --strict && python3 scripts/validate_cross_agent.py`
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
