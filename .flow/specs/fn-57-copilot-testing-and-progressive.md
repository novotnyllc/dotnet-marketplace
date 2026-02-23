# Copilot Testing and Progressive Disclosure

## Overview

Prove that Copilot actually loads and uses dotnet-artisan skills after the structural changes in fn-56, catch regressions in Claude Code and Codex, optimize oversized skills for multi-platform delivery via progressive disclosure, and harden CI to gate on Copilot success.

**Problem:** The plugin currently has no automated proof that Copilot discovers, loads, or correctly uses any skills. The CI workflow has `continue-on-error: true` for Copilot, silently swallowing failures. Additionally, 11+ skills exceed 500 lines and may confuse models or hit platform size limits (per dotnet-skills-evals data: truncation improved results for oversized skills).

## Scope

- Copilot activation smoke tests using dotnet-skills-evals patterns
- Cross-provider regression tests (Claude Code, Codex, Copilot)
- Progressive disclosure refactoring for all skills >500 lines (issue #48)
- CI hardening: Copilot gate, version pinning, auth handling, frontmatter safety checks

## Out of scope

- Structural directory changes (covered by fn-56)
- Frontmatter migration (covered by fn-56)
- New skill content authoring

## Approach

1. **Smoke tests** modeled on dotnet-skills-evals activation eval pattern: test cases with expected_skills, verified against Copilot CLI output
2. **Regression tests** verify existing Claude Code and Codex behavior unchanged after flatten
3. **Progressive disclosure** following the Agent Skills spec: SKILL.md core <500 lines with sibling reference files (referenced via normal file paths, NOT `[skill:]` syntax)
4. **CI hardening** incremental: first verify Copilot passes, then remove `continue-on-error`, with proper auth/infra-error handling

## Risks

- **Copilot CLI not available in CI runners** → version-pinned install step with auth handling and infra_error policy
- **32-skill limit masks real failures** → smoke tests must target both visible and advisor-routed skills
- **Progressive disclosure changes skill behavior** → before/after effectiveness comparison using eval patterns
- **Eval framework external dependency** → pin dotnet-skills-evals version or vendor test patterns
- **Forks can't run Copilot tests** → graceful skip with annotation for fork PRs

## Quick commands

```bash
# Run Copilot smoke tests
python tests/copilot-smoke/run_smoke.py --provider copilot

# Run cross-provider regression
./test.sh --agents claude,codex,copilot

# Check skill sizes
find skills -name SKILL.md -exec wc -l {} + | sort -rn | head -20

# Verify no skill exceeds 500 lines
find skills -name SKILL.md -exec sh -c 'lines=$(wc -l < "$1"); [ "$lines" -gt 500 ] && echo "OVER: $1 ($lines lines)"' _ {} \;
```

## Acceptance

- [ ] Copilot smoke tests exist and pass: verify skill discovery, activation, and content loading
- [ ] Claude Code regression tests pass: all existing test cases unchanged
- [ ] Codex regression tests pass: skill sync works with flat layout
- [ ] All 11+ oversized skills refactored to <500 lines with sibling reference files
- [ ] Sibling files referenced via normal file paths, not `[skill:]` syntax
- [ ] CI workflow gates on Copilot success (continue-on-error removed)
- [ ] Copilot CLI version pinned in CI workflow with auth handling
- [ ] Infra errors vs test failures distinguished in CI
- [ ] Frontmatter safety checks in CI (no BOM, no quoted descriptions, license present)
- [ ] Fork CI behavior documented and graceful

## Dependencies

- Depends on fn-56 (structural compatibility) completing first
- Uses patterns from dotnet-skills-evals (https://github.com/Aaronontheweb/dotnet-skills-evals)
- References dotnet-skills issue #48 for progressive disclosure requirements

## References

- dotnet-skills-evals: https://github.com/Aaronontheweb/dotnet-skills-evals
- Issue #48: https://github.com/Aaronontheweb/dotnet-skills/issues/48
- Copilot CLI issues: #1464 (32-skill limit), #978 (skills not auto-activated)
- Agent Skills spec progressive disclosure: https://agentskills.io/specification
- Existing CI: .github/workflows/agent-live-routing.yml, .github/workflows/validate.yml
