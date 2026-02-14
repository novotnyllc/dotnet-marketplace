# fn-17.3 Integration — plugin registration, validation, and cross-reference audit

## Description
Register all 5 CLI skills in plugin.json, run validation, and audit cross-references for correctness. Resolve any existing TODO(fn-17) placeholders in other skills.

## Delivers
- Plugin registration in `.claude-plugin/plugin.json`
- Cross-reference audit across all CLI skills
- Validation pass for all 5 skills
- Resolution of `<!-- TODO(fn-17) -->` placeholders in other skills

## Acceptance
- [ ] All 5 skill paths registered in `.claude-plugin/plugin.json`
- [ ] `./scripts/validate-skills.sh` passes for all 5 skills
- [ ] Skill `name` frontmatter values are unique repo-wide (`grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty)
- [ ] Cross-references use canonical `[skill:skill-name]` syntax and resolve to existing skills
- [ ] Scope boundary statements present in each skill
- [ ] Existing `<!-- TODO(fn-17) -->` placeholders in other skills are resolved with canonical cross-refs (check `dotnet-native-aot` for CLI cross-ref placeholder)
- [ ] Soft cross-refs (fn-19 CI/CD, fn-7 testing) noted but not enforced in hard validation commands

## Dependencies
- fn-17.1 (System.CommandLine and architecture skills must exist)
- fn-17.2 (distribution, packaging, and pipeline skills must exist)

## Done summary
Registered all 5 CLI tool skills in plugin.json and updated dotnet-advisor to use canonical CLI skill names (dotnet-cli-distribution, dotnet-cli-packaging, dotnet-cli-release-pipeline) replacing stale planned names. Removed `planned` tag from CLI section. All validation passes with 0 errors and unique skill names.
## Evidence
- Commits: 4a362ae7db03c84ed5f9ced167485b447b42b7e7
- Tests: ./scripts/validate-skills.sh, grep -rh '^name:' skills/*/*/SKILL.md | sort | uniq -d, grep -r 'TODO(fn-17)' skills/
- PRs: