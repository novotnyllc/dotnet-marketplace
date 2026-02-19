# Skill Routing Language Hardening

## Overview

Standardize routing language across all 130 SKILL.md files and 14 agent files so skills are discovered reliably from non-specific prompts. Descriptions stay concise/high-signal within the 12K char budget, inter-skill references use canonical `[skill:name]` syntax everywhere, and scope/out-of-scope boundaries are explicit. Harden validation scripts and CI gates to enforce these standards going forward.

## Scope

**In scope:**
- All 130 `skills/**/SKILL.md` files (description, scope, out-of-scope, cross-references)
- All 14 `agents/*.md` files (bare-text references → `[skill:]` syntax)
- `scripts/_validate_skills.py` and `scripts/validate-skills.sh` (new checks)
- `tests/agent-routing/check-skills.cs` and `cases.json` (assertion hardening)
- `CONTRIBUTING-SKILLS.md`, `CONTRIBUTING.md`, `CLAUDE.md` (guidance updates)
- `.github/workflows/validate.yml` (CI gate updates)

**Out of scope:**
- Changing skill functionality or body content beyond routing sections
- Adding new skills or removing existing ones
- Changing the routing architecture (advisor → domain skill chain)
- Semantic similarity overlap detection (deferred — requires embedding infrastructure)
- `README.md` delegation flow diagrams (content lives there, not in AGENTS.md)

## Key Context

- Budget is at WARN threshold: 12,345 chars current vs 12,000 warn / 15,600 fail. All description changes must be budget-neutral or budget-negative.
- Research shows assertive cues in descriptions create 7x selection bias; position bias gives 80.2% selection rate to first-listed tools. Descriptions must be factual, not promotional.
- 16 skills have zero routing markers (no trigger, scope, or out-of-scope). These need markers added from scratch.
- 8 of 14 agent files use bare-text references (~50 total) instead of `[skill:]` syntax.
- CI currently runs without `STRICT_REFS=1`, so cross-ref validation is lenient. Must enable strict mode.
- Prior art: fn-29 (fleet review), fn-37 (cleanup sweep), fn-49 (compliance review), fn-51 (frontmatter).

## Cross-Reference Conventions

**Unified `[skill:]` syntax** — `[skill:name]` refers to any routable artifact (skills OR agents). The validator resolves references against the union of skill directory names + agent file names. This is consistent with how both skills and agents are loaded via the skill system.

**Self-references** — A skill referencing itself via `[skill:]` is always an error.

**Cycles** — Bidirectional references (e.g., `dotnet-advisor` ↔ `dotnet-version-detection`) are legitimate and expected for hub skills. Cycle detection produces a **report** (informational), not validation errors. Self-references are the only structural error.

## Agent File Validation Strategy

Agent frontmatter uses full YAML with sequences (e.g., `preloaded-skills` lists). The SKILL validator's subset YAML parser (`_validate_skills.py`) rejects sequences. Therefore, agent validation uses **regex extraction** for `name:` and `description:` scalar fields only — it does NOT reuse the SKILL YAML parser. This is a dedicated code path in the validator.

## Bare-Reference Detection Strategy

Bare-ref detection (backtick-wrapped or bold-wrapped identifiers like `` `dotnet-testing-specialist` ``) uses an **allowlist of known IDs**: the union of skill directory names and agent file stems. Only tokens matching known IDs are flagged. This avoids false positives on .NET CLI tools (`dotnet-counters`, `dotnet-trace`, `dotnet-dump`, etc.) and other non-skill identifiers.

## Budget Threshold Semantics

- Acceptance criterion: `CURRENT_DESC_CHARS < 12,000` (strictly less than).
- `BUDGET_STATUS` in validator output reflects CURRENT chars only.
- `PROJECTED_DESC_CHARS` (from `--projected-skills` and `--max-desc-chars`) is reported as a separate informational metric, not included in `BUDGET_STATUS`.
- The validator's WARN condition triggers at `>= 12,000`, so reaching exactly 12,000 counts as WARN. Acceptance requires being below this threshold.

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
- [ ] All cross-references in skills AND agent files use `[skill:name]` syntax (unified syntax for skills and agents)
- [ ] All skills have explicit scope/out-of-scope sections
- [ ] Validator enforces new routing-language quality checks (skills and agents via separate code paths)
- [ ] Routing compliance report generates per-skill compliance data
- [ ] Routing test assertions use definitive proof (Skill tool invocation, not text mentions)
- [ ] `./scripts/validate-skills.sh` passes with zero errors
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] CI gates updated: `STRICT_REFS=1` enabled, zero errors enforced, zero new warnings vs baseline
- [ ] CONTRIBUTING-SKILLS.md, CLAUDE.md, CONTRIBUTING.md updated with canonical conventions
- [ ] CHANGELOG.md entry added
- [ ] `CURRENT_DESC_CHARS < 12,000` (strictly below WARN threshold)

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
