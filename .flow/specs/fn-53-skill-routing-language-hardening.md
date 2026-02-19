# Skill Routing Language Hardening

## Overview

Standardize routing language across all 130 SKILL.md files and 14 agent files so skills are discovered reliably from non-specific prompts. Descriptions stay concise/high-signal within the 12K char budget, inter-skill references use canonical `[skill:name]` syntax everywhere, and scope/out-of-scope boundaries are explicit. Harden validation scripts and CI gates to enforce these standards going forward.

## Scope

**In scope:**
- All 130 `skills/**/SKILL.md` files (description, scope, out-of-scope, cross-references)
- All 14 `agents/*.md` files (bare-text references → `[skill:]` syntax)
- `AGENTS.md` routing index normalization
- `scripts/_validate_skills.py` and `scripts/validate-skills.sh` (new checks)
- `tests/agent-routing/check-skills.cs` and `cases.json` (assertion hardening)
- `CONTRIBUTING-SKILLS.md`, `CONTRIBUTING.md`, `CLAUDE.md` (guidance updates)
- `.github/workflows/validate.yml` (CI gate updates)

**Out of scope:**
- Changing skill functionality or body content beyond routing sections
- Adding new skills or removing existing ones
- Changing the routing architecture (advisor → domain skill chain)
- Semantic similarity overlap detection (deferred — requires embedding infrastructure)

## Key Context

- Budget is at WARN threshold: 12,345 chars current vs 12,000 warn / 15,600 fail. All description changes must be budget-neutral or budget-negative.
- Research shows assertive cues in descriptions create 7x selection bias; position bias gives 80.2% selection rate to first-listed tools. Descriptions must be factual, not promotional.
- 16 skills have zero routing markers (no trigger, scope, or out-of-scope). These need markers added from scratch.
- 8 of 14 agent files use bare-text references (~50 total) instead of `[skill:]` syntax.
- `--allow-planned-refs` default in CI effectively disables cross-ref validation. Must address in hardening.
- Prior art: fn-29 (fleet review), fn-37 (cleanup sweep), fn-49 (compliance review), fn-51 (frontmatter).

## Quick commands

```bash
# Validate skills
./scripts/validate-skills.sh

# Validate marketplace
./scripts/validate-marketplace.sh

# Run routing tests (single case)
./test.sh --agents claude --case-id foundation-routing
```

## Acceptance

- [ ] All 130 SKILL.md descriptions follow canonical style guide from task 2
- [ ] All cross-references in skills AND agent files use `[skill:name]` syntax
- [ ] All skills have explicit scope/out-of-scope sections
- [ ] Validator enforces new routing-language quality checks
- [ ] Routing compliance report generates per-skill compliance data
- [ ] Routing test assertions use definitive proof (Skill tool invocation, not text mentions)
- [ ] `./scripts/validate-skills.sh` passes with zero errors
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] CI gates updated to enforce "zero errors, zero new warnings vs baseline"
- [ ] CONTRIBUTING-SKILLS.md, CLAUDE.md, CONTRIBUTING.md updated with canonical conventions
- [ ] CHANGELOG.md entry added
- [ ] Description budget stays within WARN threshold (≤12,000 chars)

## Dependency Graph

```text
T1 → T2 → {T3, T4} → T5 → {T6, T7, T8, T9, T10} → T11 → T12
```

Waves:
1. T1 (audit)
2. T2 (spec)
3. T3 + T4 (tooling, parallel)
4. T5 (foundation + high-traffic)
5. T6 + T7 + T8 + T9 + T10 (sweeps + agents, parallel)
6. T11 (verification)
7. T12 (docs + CI + rollout)

## References

- Spec: `.flow/specs/skill-routing-language-hardening-plan.md`
- Agent Skills spec: https://agentskills.io/specification
- Anthropic best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Existing validator: `scripts/_validate_skills.py`
- Routing tests: `tests/agent-routing/check-skills.cs`
