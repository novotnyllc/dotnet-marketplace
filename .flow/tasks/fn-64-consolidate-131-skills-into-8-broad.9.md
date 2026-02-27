# fn-64.9 Update agents, advisor, hooks, and plugin.json for 8 consolidated skills

## Description
Update all 14 agent definitions, rewrite dotnet-advisor routing catalog, update hooks, and atomically update `plugin.json` to reference the 8 consolidated skill names. This task owns the manifest update that tasks 2-6 deferred.

**Size:** M
**Files:** `agents/*.md` (14 files), `skills/dotnet-advisor/SKILL.md`, `scripts/hooks/session-start-context.sh`, `scripts/hooks/user-prompt-dotnet-reminder.sh`, `hooks/hooks.json`, `.claude-plugin/plugin.json`

## Approach

1. **Update plugin.json**: Remove all 131 old skill paths from the `skills` array. Add the 8 new skill paths (`skills/dotnet-csharp`, `skills/dotnet-api`, `skills/dotnet-ui`, `skills/dotnet-testing`, `skills/dotnet-devops`, `skills/dotnet-tooling`, `skills/dotnet-debugging`, `skills/dotnet-advisor`). This is the single atomic manifest update.
2. **Rewrite dotnet-advisor**: Replace 363-line routing catalog (21 categories, 131 skills) with 8 consolidated skills. The routing catalog becomes dramatically simpler — 8 entries with rich keyword descriptions pointing to the right skill. Each entry includes companion file hints (e.g., "for async patterns, read `references/async-patterns.md` from `dotnet-csharp`"). Specifically:
   - Replace "Immediate Routing Actions → invoke dotnet-csharp-coding-standards" with "invoke dotnet-csharp (read references/coding-standards.md)"
   - Rebuild the entire category-to-skill mapping (21 categories → 8 skills)
   - Update all `[skill:old-name]` references
3. **Update agent preloaded skills**: Each agent's `## Preloaded Skills` section lists `[skill:old-name]` refs. Replace with `[skill:new-name]`. Examples:
   - `dotnet-testing-specialist`: 5 individual skill refs → `[skill:dotnet-testing]`
   - `dotnet-aspnetcore-specialist`: 7 individual skill refs → `[skill:dotnet-api]`
   - `dotnet-code-review-agent`: 7 individual skill refs → `[skill:dotnet-csharp]` + `[skill:dotnet-api]`
   - `dotnet-blazor-specialist`: 5 refs → `[skill:dotnet-ui]`
   - (apply pattern to all 14 agents)
4. **Update agent routing tables**: Replace all inline `[skill:old-name]` references in Knowledge Sources, Explicit Boundaries, Routing Tables with new names. Add companion file path hints where appropriate.
5. **Update hooks**: Both hook scripts reference `[skill:dotnet-advisor]` — this name survives. Verify no other skill refs in hooks.
6. **Verify `STRICT_REFS=1` passes**: All `[skill:name]` refs must resolve to actual skill directory names.

## Key context

- 14 agents at `agents/*.md` — each has Preloaded Skills, Knowledge Sources, Explicit Boundaries sections
- `dotnet-code-review-agent` alone references 15+ individual skill names — biggest update
- With 8 skills, agents may preload 1-2 skills instead of 5-7 (simpler, faster loading)
- Agents can specify companion file paths in their routing sections to help the model find the right deep content
- The advisor rewrite is the most impactful change — goes from 363 lines to ~50 lines

## Acceptance
- [ ] `plugin.json` updated: 131 old paths removed, 8 new paths added
- [ ] dotnet-advisor SKILL.md rewritten for 8 consolidated skills (including companion file hints)
- [ ] "invoke dotnet-csharp-coding-standards" replaced with "invoke dotnet-csharp" + reference hint
- [ ] All 14 agent files updated with correct `[skill:new-name]` references
- [ ] No `[skill:old-name]` references remain anywhere in agents/ or skills/
- [ ] Hooks verified (dotnet-advisor name survives)
- [ ] `STRICT_REFS=1 ./scripts/validate-skills.sh` passes

## Done summary
Updated plugin.json from 131 to 8 skill paths, rewrote dotnet-advisor routing catalog with companion file hints for 8 consolidated skills, and updated all 14 agent files to reference new consolidated skill names with companion file path guidance. All 110 companion file references verified. Specialist agent routing expanded to cover all 14 agents.
## Evidence
- Commits: cbd299e, a6cfd26
- Tests: STRICT_REFS=1 ./scripts/validate-skills.sh (0 errors in agents/new skills), ./scripts/validate-marketplace.sh (PASSED)
- PRs: