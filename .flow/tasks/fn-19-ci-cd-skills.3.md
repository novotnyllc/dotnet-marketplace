# fn-19-ci-cd-skills.3 Integration — plugin registration, advisor catalog, validation, cross-reference reconciliation

## Description
Register all 8 CI/CD skills in plugin.json, update the dotnet-advisor catalog section 17 from `planned` to `implemented`, reconcile deferred fn-19 placeholders in other skills, and run all validation checks. This task depends on fn-19.1 and fn-19.2 completing first.

**Files modified:**
- `.claude-plugin/plugin.json` (add 8 skill paths)
- `skills/foundation/dotnet-advisor/SKILL.md` (update section 17)
- `skills/performance/dotnet-ci-benchmarking/SKILL.md` (resolve 5 `<!-- TODO(fn-19) -->` placeholders)

**fn-18 reconciliation:**
Replace all `<!-- TODO(fn-19) -->` placeholders in `skills/performance/dotnet-ci-benchmarking/SKILL.md` with canonical `[skill:dotnet-gha-patterns]` cross-references. Note: the existing placeholders reference `dotnet-github-actions` which is not the canonical name — use `dotnet-gha-patterns` instead. 5 placeholders at lines 16, 104, 226, 389, 503.

**Existing fn-19 references:**
Multiple skills reference "fn-19" in bare text (not `[skill:...]` syntax). Update the most prominent ones in skills that directly cross-reference fn-19 depth patterns to use canonical skill names where appropriate.

**Cross-validation:**
- Repo-wide skill name uniqueness
- `./scripts/validate-skills.sh` for all 8 skills
- Cross-reference presence validation
- JSON syntax validation for plugin.json

This is the single owner of `plugin.json` to eliminate merge conflicts.

## Acceptance
- [ ] `.claude-plugin/plugin.json` updated with 8 new skill paths:
  - `skills/cicd/dotnet-gha-patterns`
  - `skills/cicd/dotnet-gha-build-test`
  - `skills/cicd/dotnet-gha-publish`
  - `skills/cicd/dotnet-gha-deploy`
  - `skills/cicd/dotnet-ado-patterns`
  - `skills/cicd/dotnet-ado-build-test`
  - `skills/cicd/dotnet-ado-publish`
  - `skills/cicd/dotnet-ado-unique`
- [ ] `skills/foundation/dotnet-advisor/SKILL.md` section 17 updated:
  - Remove `planned` marker (change to `implemented`)
  - Verify all 8 skills listed with correct IDs
- [ ] fn-18 placeholder reconciliation:
  - `grep -r "TODO(fn-19)" skills/performance/` returns empty
  - `grep -r "\[skill:dotnet-gha-patterns\]" skills/performance/dotnet-ci-benchmarking/SKILL.md` finds matches
  - No references to `dotnet-github-actions` remain (it was a placeholder name, not canonical)
- [ ] Repo-wide uniqueness validated: `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty
- [ ] `./scripts/validate-skills.sh` passes for all 8 CI/CD skills
- [ ] Cross-reference validation passes:
  - `grep -r "\[skill:dotnet-native-aot\]" skills/cicd/` finds matches
  - `grep -r "\[skill:dotnet-cli-release-pipeline\]" skills/cicd/` finds matches
  - `grep -r "\[skill:dotnet-containers\]" skills/cicd/` finds matches
  - `grep -r "\[skill:dotnet-ci-benchmarking\]" skills/cicd/` finds matches
  - `grep -r "\[skill:dotnet-add-ci\]" skills/cicd/` finds matches
- [ ] All 8 skills have unique `name` frontmatter values
- [ ] plugin.json syntax is valid JSON (`python3 -m json.tool .claude-plugin/plugin.json > /dev/null`)
- [ ] Scope boundary statements present in all 8 skills: `grep -l "Out of scope\|Scope boundary" skills/cicd/*/SKILL.md | wc -l` returns 8

## Done summary
Registered all 8 CI/CD skills in plugin.json, updated advisor catalog section 17 from planned to implemented, replaced 5 TODO(fn-19) placeholders in dotnet-ci-benchmarking with canonical [skill:dotnet-gha-patterns] cross-references, and updated bare fn-19 mentions across 11 other skills to use canonical [skill:...] syntax.
## Evidence
- Commits: 7a581c3
- Tests: ./scripts/validate-skills.sh, python3 -m json.tool .claude-plugin/plugin.json
- PRs: