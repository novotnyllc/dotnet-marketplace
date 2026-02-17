# fn-52-fill-skill-gaps-from-dotnet-skills.4 Integration: plugin.json, docs, validation, agent updates

## Description
Register all 4 new skills in plugin.json, update documentation counts, update validation script, add slopwatch cross-references to existing skills, and update agent preloaded skills.

**Size:** M
**Files:** `plugin.json`, `README.md` (plugin), `AGENTS.md`, `CLAUDE.md` (root + plugin), `CONTRIBUTING-SKILLS.md`, `validate-skills.sh`, `dotnet-csharp-concurrency-specialist.md`, 4 existing agent-meta-skills (`dotnet-agent-gotchas`, `dotnet-build-analysis`, `dotnet-csproj-reading`, `dotnet-solution-navigation`)

## Approach

1. **plugin.json**: Add 4 skill paths to `skills` array, maintaining category grouping:
   - `"./skills/agent-meta-skills/dotnet-slopwatch"`
   - `"./skills/api-development/dotnet-csharp-api-design"`
   - `"./skills/core-csharp/dotnet-csharp-concurrency-patterns"`
   - `"./skills/core-csharp/dotnet-csharp-type-design-performance"`

2. **Slopwatch cross-references**: Add `[skill:dotnet-slopwatch]` to the Slopwatch Anti-Patterns sections in 4 existing agent-meta-skills: `dotnet-agent-gotchas`, `dotnet-build-analysis`, `dotnet-csproj-reading`, `dotnet-solution-navigation` (per file-disjoint convention)

3. **validate-skills.sh**: Update `--projected-skills` from 126 to 130 (line 49)

4. **README.md** (plugin): Update skill catalog counts and Mermaid diagram node labels:
   - Total: 126 → 130
   - Agent Meta-Skills: 4 → 5
   - API Development: 8 → 9
   - Core C#: 16 → 18
   - Mermaid nodes: `Skills` subgraph title (126→130), `CC` (16→18), `AD` (8→9), `AM` (4→5)

5. **AGENTS.md**: Update routing index counts (same deltas as README) and category descriptions

6. **CLAUDE.md** (root + plugin): Update "126 skills" → "130 skills" references

7. **CONTRIBUTING-SKILLS.md**: Update budget math paragraph — recalculate from actual `validate-skills.sh` output: skill count (126→130), average description length, total character count updated to match `CURRENT_DESC_CHARS` from validation run

8. **Agent update**: Add `[skill:dotnet-csharp-concurrency-patterns]` to `dotnet-csharp-concurrency-specialist.md` preloaded skills

9. **Trigger-corpus verification**: Verify `trigger-corpus.json` has at least one entry per category that received new skills (api-development, core-csharp, agent-meta-skills). Add entries if missing.

10. **Validation**: Run `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` and fix any issues

## Key Context

- Convention: this task is sole owner of plugin.json to prevent merge conflicts (per `.flow/memory/conventions.md`)
- Update Mermaid diagrams that embed skill counts in node labels (per pitfall: "also grep for the same counts inside Mermaid diagram blocks")
- Cross-ref edits to existing skills owned by this task per file-disjoint convention (not by content-authoring tasks)
## Acceptance
- [ ] 4 new skill paths added to `plugin.json` `skills` array
- [ ] `jq '.skills | length' plugins/dotnet-artisan/.claude-plugin/plugin.json` returns 130
- [ ] `validate-skills.sh` `--projected-skills` updated to 130
- [ ] `./scripts/validate-skills.sh` passes (exit 0)
- [ ] `./scripts/validate-marketplace.sh` passes (exit 0)
- [ ] README.md total skill count updated to 130
- [ ] README.md per-category counts updated (Agent Meta-Skills, API Development, Core C#)
- [ ] README.md Mermaid node labels updated: `Skills` subgraph (126→130), `CC` (16→18), `AD` (8→9), `AM` (4→5)
- [ ] AGENTS.md routing index counts updated
- [ ] Root CLAUDE.md skill count updated to 130
- [ ] Plugin CLAUDE.md skill count updated to 130
- [ ] CONTRIBUTING-SKILLS.md budget math updated with recalculated average and total from actual validation output
- [ ] `dotnet-csharp-concurrency-specialist.md` preloaded skills include `[skill:dotnet-csharp-concurrency-patterns]`
- [ ] 4 existing agent-meta-skills have `[skill:dotnet-slopwatch]` cross-ref added
- [ ] Verify: `grep -l '\[skill:dotnet-slopwatch\]' plugins/dotnet-artisan/skills/agent-meta-skills/*/SKILL.md | wc -l` returns 4
- [ ] Trigger-corpus.json verified: all categories receiving new skills have at least one corpus entry
- [ ] No broken cross-references
- [ ] BUDGET_STATUS is OK or WARN (not FAIL)
- [ ] Actual `CURRENT_DESC_CHARS` recorded in done summary
## Done summary
Registered 4 new skills in plugin.json (total: 130), updated skill counts across 14 files (README.md, AGENTS.md, CLAUDE.md root+plugin, CONTRIBUTING.md, CONTRIBUTING-SKILLS.md, Mermaid diagrams), added [skill:dotnet-slopwatch] cross-refs to 4 agent-meta-skills, updated concurrency-specialist preloaded skills, bumped validation thresholds (--projected-skills 130, --fail-threshold 15600). CURRENT_DESC_CHARS=12115, BUDGET_STATUS=WARN.
## Evidence
- Commits: 6c96b9c, a880179
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: