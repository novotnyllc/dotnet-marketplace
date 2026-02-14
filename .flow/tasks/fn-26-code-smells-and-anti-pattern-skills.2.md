## Description

Register the new `dotnet-csharp-code-smells` skill in plugin infrastructure and update all catalog docs to reflect the addition.

**Size:** S
**Files:**
- `.claude-plugin/plugin.json` (add skill path)
- `skills/foundation/dotnet-advisor/SKILL.md` (add catalog entry + routing)
- `docs/dotnet-artisan-spec.md` (update Core C# section skill count and list)
- `.flow/specs/fn-1-dotnet-artisan-comprehensive-net-coding.md` (add fn-26 row to Wave 1 table, update fn-3 skill count)

## Approach

- Add `"skills/core-csharp/dotnet-csharp-code-smells"` to plugin.json skills array (no trailing slash, follow pattern of `"skills/core-csharp/dotnet-csharp-modern-patterns"`)
- Add catalog entry in dotnet-advisor SKILL.md section 2 (Core C#): `[skill:dotnet-csharp-code-smells]` with brief routing description
- Add routing logic entry so the advisor routes to this skill when code review or code quality topics arise
- Update `docs/dotnet-artisan-spec.md` Core C# section: add `[skill:dotnet-csharp-code-smells]` bullet with description, update count. Use canonical `[skill:dotnet-csharp-code-smells]` cross-reference syntax everywhere (never bare skill name).
- Update fn-1 umbrella spec deterministically:
  - Add new row to Wave 1 table: `| fn-26 | Code Smells & Anti-Patterns | 1 skill | depends on fn-2 |`
  - Update fn-3 row skill count from "7 skills + 1 agent" to "8 skills + 1 agent" (this skill belongs to Core C# category)
  - Add fn-26 node to mermaid dependency graph: `FN2 --> FN26[fn-26: Code Smells]`
- Run `./scripts/validate-skills.sh` and verify `BUDGET_STATUS=OK` or `BUDGET_STATUS=WARN`

## Shared file contention

This task modifies high-contention registry files also touched by other Wave 1 epics. All edits are additive (append to arrays/tables), minimizing conflict surface. If other fn-3 tasks have pending PRs touching these same files, coordinate merge order or resolve conflicts during merge.

## Key context

- Follow convention at `skills/foundation/dotnet-advisor/SKILL.md` for catalog and routing format
- Plugin.json pattern: `"skills/core-csharp/dotnet-csharp-modern-patterns"` (no trailing slash)
- Cross-reference IDs must use canonical name: `[skill:dotnet-csharp-code-smells]` (never bare skill name)
- Budget math: current 3,085 chars + ~95 chars = ~3,180 chars (well within 12,000 WARN)
## Acceptance
- [ ] `plugin.json` skills array includes `"skills/core-csharp/dotnet-csharp-code-smells"`
- [ ] `dotnet-advisor` SKILL.md has catalog entry for `[skill:dotnet-csharp-code-smells]` in section 2
- [ ] `dotnet-advisor` routing logic updated to route code quality/review queries to the new skill
- [ ] `docs/dotnet-artisan-spec.md` Core C# section updated with new skill and count using canonical `[skill:dotnet-csharp-code-smells]` syntax
- [ ] `fn-1` umbrella spec: fn-26 row added to Wave 1 table as `| fn-26 | Code Smells & Anti-Patterns | 1 skill | depends on fn-2 |`
- [ ] `fn-1` umbrella spec: fn-3 row updated from "7 skills + 1 agent" to "8 skills + 1 agent"
- [ ] `fn-1` umbrella spec: mermaid graph includes fn-26 node with dependency on fn-2
- [ ] `./scripts/validate-skills.sh` passes with `BUDGET_STATUS=OK` or `BUDGET_STATUS=WARN`
- [ ] No cross-reference uses bare skill name (all use `[skill:dotnet-csharp-code-smells]` syntax)

## Done summary
Registered dotnet-csharp-code-smells skill in plugin.json, added catalog entry and routing logic in dotnet-advisor SKILL.md, updated docs/dotnet-artisan-spec.md Core C# section, and updated fn-1 umbrella spec with fn-26 Wave 1 table row, fn-3 skill count bump to 8, and mermaid dependency graph node.
## Evidence
- Commits: bc75a77147c8516e3c267caf5924110bed30948c
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: