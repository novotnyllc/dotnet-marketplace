# fn-18-performance-and-benchmarking-skills.4 Integration — plugin registration, advisor catalog update, validation

## Description
**NEW TASK** - Integration task for fn-18, created during plan review to address plugin.json ownership and validation requirements.

Register all 4 skills and 2 agents in plugin.json, update the dotnet-advisor catalog from `planned` to implemented, and run all validation checks. This task depends on fn-18.1, fn-18.2, and fn-18.3 completing first.

**Files modified:**
- `.claude-plugin/plugin.json` (add 4 skill paths, 2 agent paths)
- `skills/foundation/dotnet-advisor/SKILL.md` (update section 9)

**Cross-validation:**
- Repo-wide skill name uniqueness
- `./scripts/validate-skills.sh` for all 4 skills
- Cross-reference presence validation

This is the single owner of `plugin.json` to eliminate merge conflicts.

## Acceptance
- [ ] `.claude-plugin/plugin.json` updated with 4 new skill paths:
  - `skills/performance/dotnet-benchmarkdotnet`
  - `skills/performance/dotnet-performance-patterns`
  - `skills/performance/dotnet-profiling`
  - `skills/performance/dotnet-ci-benchmarking`
- [ ] `.claude-plugin/plugin.json` updated with 2 new agent paths:
  - `agents/dotnet-performance-analyst.md`
  - `agents/dotnet-benchmark-designer.md`
- [ ] `skills/foundation/dotnet-advisor/SKILL.md` section 9 updated:
  - Remove `planned` marker
  - Convert placeholder cross-refs to live `[skill:...]` syntax
  - Verify all 4 skills listed with correct IDs
- [ ] Repo-wide uniqueness validated: `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty
- [ ] `./scripts/validate-skills.sh` passes for all 4 performance skills
- [ ] Cross-reference validation passes:
  - `grep -r "\[skill:dotnet-csharp-modern-patterns\]" skills/performance/` finds matches
  - `grep -r "\[skill:dotnet-csharp-coding-standards\]" skills/performance/` finds matches
  - `grep -r "\[skill:dotnet-observability\]" skills/performance/` finds matches
  - `grep -r "\[skill:dotnet-serialization\]" skills/performance/` finds matches
  - `grep -r "\[skill:dotnet-native-aot\]" skills/performance/` finds matches
- [ ] Deferred fn-19 placeholder validation: `grep -l "TODO.*fn-19" skills/performance/dotnet-ci-benchmarking/SKILL.md` finds match
- [ ] All 4 skills have unique `name` frontmatter values (no duplicates)
- [ ] plugin.json syntax is valid JSON (run `python3 -m json.tool .claude-plugin/plugin.json > /dev/null`)

## Done summary
Registered all fn-18 skills and agents in plugin.json, updated dotnet-advisor catalog from planned to implemented, and validated all cross-references and uniqueness constraints. All validation scripts pass.

## Evidence
- Commits: plugin.json and advisor catalog updates
- Tests: `./scripts/validate-skills.sh` passes, uniqueness check passes
- PRs: N/A (single-repo workflow)
