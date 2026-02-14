# fn-16-native-aot-and-trimming-skills.3 Integration — plugin registration, validation, and cross-reference audit

## Description
Register all 4 fn-16 skills in `.claude-plugin/plugin.json`, run validation, audit cross-references, and resolve existing `<!-- TODO(fn-16) -->` placeholders in other skills (e.g., `dotnet-serialization`). Single owner of `plugin.json` modifications for this epic.

## Acceptance
- [ ] All 4 skill paths registered in `.claude-plugin/plugin.json` (`skills/native-aot/dotnet-native-aot`, `skills/native-aot/dotnet-aot-architecture`, `skills/native-aot/dotnet-trimming`, `skills/native-aot/dotnet-aot-wasm`)
- [ ] `./scripts/validate-skills.sh` passes for all 4 skills
- [ ] Repo-wide skill `name` uniqueness check passes (no duplicates)
- [ ] Hard cross-references use canonical skill IDs (verified by grep)
- [ ] Soft cross-references noted but excluded from validation commands
- [ ] Each skill has out-of-scope boundary statement (verified by grep)
- [ ] Existing `<!-- TODO(fn-16) -->` placeholders in other skills replaced with canonical `[skill:...]` cross-references
- [ ] `grep -r "TODO(fn-16)" skills/` returns empty after completion
- [ ] No skill references legacy RD.xml (verified by grep)

## Done summary
Registered 4 native-aot skills in plugin.json and replaced 8 TODO(fn-16) placeholders across 4 serialization skills with canonical [skill:...] cross-references.
## Evidence
- Commits: 090fb4e1cbeed1330bd55e853acbf74b778664e6
- Tests: ./scripts/validate-skills.sh, grep -r TODO(fn-16) skills/, grep -rh ^name: skills/*/*/SKILL.md | sort | uniq -d, grep -ri rd.xml skills/native-aot/, grep -l 'Out of scope' skills/native-aot/*/SKILL.md
- PRs: