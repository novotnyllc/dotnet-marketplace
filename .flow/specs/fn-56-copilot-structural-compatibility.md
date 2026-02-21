# Copilot Structural Compatibility

## Overview

Make dotnet-artisan's skill directory layout, YAML frontmatter, and validators compatible with GitHub Copilot CLI and VS Code Copilot Chat, while preserving full Claude Code and Codex functionality.

**Problem:** Copilot discovers skills by scanning one level deep under `skills/`. The current nested layout (`skills/<category>/<skill-name>/SKILL.md`) causes Copilot to interpret category directories as skill names, finding zero actual skills. Additionally, YAML frontmatter quirks (quoted descriptions, missing `license:` field) cause silent load failures in Copilot CLI.

**Constraint — 32-skill display limit:** Copilot CLI has a hard ~32 skill display limit in the system prompt (issues #1464, #1130). **Unverified assumption:** whether `user-invocable: false` skills (120 of 131) are excluded from this budget. With only 11 user-invocable skills, the limit may be a non-issue. This must be verified before designing a routing strategy.

## Research Sources

- **VS Code Copilot Chat source** (`microsoft/vscode-copilot-chat`): `relativePath.split('/')[0]` confirms one-level-deep scanning
- **Copilot CLI changelog**: v0.0.413 did NOT change nested directory behavior; only fixed YAML array `allowed-tools`
- **Copilot CLI v0.0.412**: Added `disable-model-invocation` and `user-invocable: false` support
- **Agent Skills spec** (`agentskills.io/specification`): Defines flat `skill-name/SKILL.md` layout; all reference repos use flat
- **Copilot CLI issues**: #1464 (32-skill limit), #894 (license required), #1024 (quoted descriptions fail), #951 (metadata last field), #1021 (symlinks ignored)
- **dotnet-skills-evals**: DSPy eval framework; compressed-index discovery mechanism tested at 56.5% TPR
- **dotnet-skills issue #48**: Progressive disclosure for skills >500 lines
- **Existing work on `copilot-refactor` branch**: Smoke runners, baseline JSONs, validator updates already committed
- **Skill invocability breakdown**: 11 user-invocable, 120 non-user-invocable (`user-invocable: false`)

## Scope

- Flatten `skills/<category>/<skill-name>/` to `skills/<skill-name>/` (131 directories)
- Update all entries in `.claude-plugin/plugin.json:skills[]` to flat paths
- Migrate all 131 SKILL.md frontmatter for Copilot safety
- Update validators (including similarity detection), baselines, and depth-sensitive scripts
- Verify 32-skill limit behavior with `user-invocable: false`; design routing strategy accordingly
- Update all documentation referencing the nested layout (including behavioral changes: quoting guidance, similarity scoring)

## Out of scope

- Copilot Extensions/Skillsets API (different feature from Agent Skills)
- Changes to hook scripts or MCP server configuration (Copilot handles these differently; addressed if testing reveals issues)
- Copilot CLI installation/distribution (users install separately)

## Approach

1. **Atomic flatten** in a single commit using `git mv` to preserve history. Preflight collision check before any moves.
2. **Frontmatter migration** scripted across all 131 SKILL.md files (raw-line inspection for quoting, not post-parse)
3. **Validator updates** additive — T2 owns all raw-frontmatter Copilot safety checks (BOM, quoted desc, license, metadata ordering) as ERRORs; T3 owns layout guard + similarity detector (glob fix, remove same-category boost, remove category fields)
4. **32-skill strategy**: First verify whether `user-invocable: false` skills count against the limit. If only 11 user-invocable skills count -> limit is a non-issue, just ensure advisor visibility. If all 131 count -> design advisor meta-router fallback.
5. **Documentation** updated in a dedicated pass after structural changes stabilize. Covers path rewrites AND behavioral changes (quoting guidance, similarity scoring). Intermediate commits on the branch may fail CI; PR must be green.

## Canonical skill count

**131 skills.** All specs, scripts (`validate-skills.sh --projected-skills`), docs (AGENTS.md, README.md), and `.agents/openai.yaml` must use this number consistently. Use `jq '.skills|length' .claude-plugin/plugin.json` to verify.

## Risks

- **plugin.json + filesystem inconsistency** causes all Claude Code skill loading to fail -> mitigated by atomic commit
- **Codex sync breaks** due to `find -mindepth 2` in `test.sh` -> explicit fix in flatten task, with SKILL.md existence check
- **Description unquoting** may break YAML for descriptions with special characters -> scripted with raw-line validation
- **Baseline invalidation** across routing-warnings and similarity baselines -> regenerated in validator task
- **Similarity validator `*/*/SKILL.md` glob** finds zero skills after flatten -> fixed in T3
- **Copilot CLI auth in CI** may require token/secrets configuration -> documented in fn-57.4
- **metadata-last field semantics ambiguous** (bug #951) -> T2 verifies exact behavior with test skills before implementing the check; falls back to conservative "ERROR if metadata is last key" if CLI unavailable

## Quick commands

```bash
# Preflight collision check (run BEFORE flatten)
find skills -name SKILL.md -mindepth 3 -maxdepth 3 | xargs -I{} dirname {} | xargs -I{} basename {} | sort | uniq -d

# Verify flat layout (no nested SKILL.md)
for dir in skills/*/*/; do [[ -f "${dir}SKILL.md" ]] && echo "NESTED: $dir"; done

# Verify skill count preserved
find skills -name SKILL.md -maxdepth 2 | wc -l  # should be 131

# Verify plugin.json paths resolve
jq -r '.skills[]' .claude-plugin/plugin.json | while read p; do [[ -f "${p}/SKILL.md" ]] || echo "MISSING: $p"; done

# Run validators
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Acceptance

- [ ] All 131 skills exist at `skills/<skill-name>/SKILL.md` (flat, one level deep)
- [ ] No `skills/<category>/<skill-name>/SKILL.md` paths remain (no nested skills)
- [ ] `plugin.json` skill paths all resolve to existing directories with SKILL.md (`jq '.skills|length'` matches find count)
- [ ] All 131 SKILL.md files have `license: MIT` in frontmatter and unquoted descriptions
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass (including similarity)
- [ ] 32-skill limit behavior verified with `user-invocable: false` skills
- [ ] Routing strategy implemented based on verified behavior
- [ ] AGENTS.md, CONTRIBUTING.md, CONTRIBUTING-SKILLS.md, README.md updated for flat layout AND behavioral changes
- [ ] Git history preserved for all moved files (git mv, not delete+create)
- [ ] Canonical skill count (131) consistent across all specs, scripts, and docs

## Dependencies

- Builds on fn-42 (directory structure), fn-51 (frontmatter), fn-54 (test harness), fn-55 (validator)
- All predecessors are done/merged; no open blockers
- Epic fn-57 (testing) depends on this epic completing first

## References

- VS Code Copilot Chat: `src/platform/customInstructions/common/customInstructionsService.ts`
- Agent Skills spec: https://agentskills.io/specification
- Copilot CLI: https://github.com/github/copilot-cli/
- Issue #48: https://github.com/Aaronontheweb/dotnet-skills/issues/48
- dotnet-skills-evals: https://github.com/Aaronontheweb/dotnet-skills-evals
- microsoft/skills: https://github.com/microsoft/skills (flat layout reference)
