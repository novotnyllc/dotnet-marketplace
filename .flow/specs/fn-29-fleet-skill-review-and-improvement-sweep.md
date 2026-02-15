# fn-29: Fleet Skill Review and Improvement Sweep

## Overview

Deploy a fleet of parallel worker agents to review all 99 skills in dotnet-artisan against best practices from Anthropic's skill authoring guide and this repo's conventions. Each agent reviews a batch of skills by category, produces a findings report, and then implements approved improvements. A coordinator task merges findings and resolves cross-cutting issues.

## Approach

**Phase 1 — Audit:** Parallel agents each review a batch of skill categories. Each agent evaluates every SKILL.md in its assigned categories against the review rubric (below) and produces a structured findings report.

**Phase 2 — Implement:** After audit findings are consolidated, parallel agents implement improvements within their assigned categories. Changes are committed per-category for clean review.

**Phase 3 — Validate:** Run all four validation commands, verify context budget, and ensure cross-references are intact.

### Review Rubric (per skill)

Each skill is evaluated on these dimensions:

1. **Description Quality** — Does it follow the formula: `[What it does] + [When to use it]`? Is it under 120 chars? Does it include trigger phrases a user would actually say?
2. **Description Triggering** — Would Claude correctly trigger this skill from typical user requests? Any over/under-triggering risks?
3. **Instruction Clarity** — Are instructions specific and actionable (not vague)? Are critical steps explicit?
4. **Progressive Disclosure** — Is SKILL.md focused on core instructions? Are detailed references linked rather than inlined? Is it under 5,000 words?
5. **Cross-References** — Does it use `[skill:name]` syntax for all skill references? Are cross-references accurate and pointing to existing skills? Are bidirectional references present where appropriate?
6. **Error Handling** — Does it include troubleshooting or common pitfalls for the .NET domain it covers?
7. **Examples** — Does it include concrete examples showing the skill in action?
8. **Composability** — Does it work well alongside other skills? Does it avoid assuming it's the only loaded skill?
9. **Consistency** — Does it follow the same patterns as peer skills in its category (section headers, code example format, cross-ref placement, Agent Gotchas presence)?
10. **Registration & Budget** — Is the skill registered in plugin.json? Is the description under 120 chars? What is the aggregate budget impact of any proposed description change?
11. **Progressive Disclosure Compliance** — Does the skill use a `details.md` companion file if SKILL.md exceeds ~3,000 words or has extensive code examples? Is `details.md` properly referenced from the main SKILL.md?

### Category Batches for Parallel Workers

Batches are designed so each worker handles ~9-20 skills (99 total across 18 categories):

- **Batch A (20 skills):** core-csharp (9), foundation (4), project-structure (6), release-management (1)
- **Batch B (19 skills):** architecture (10), serialization (4), security (3), multi-targeting (2)
- **Batch C (18 skills):** testing (10), cicd (8)
- **Batch D (18 skills):** api-development (5), cli-tools (5), performance (4), native-aot (4)
- **Batch E (17 skills):** ui-frameworks (13), agent-meta-skills (4)
- **Batch F (9 skills):** documentation (5), packaging (3), localization (1)

**Note:** Batch totals sum to 101 but actual plugin.json count is 99. Task 1 must reconcile by verifying against `jq '.skills | length' .claude-plugin/plugin.json` and adjusting batch assignments to match.

## Scope

### Task 1: Create Review Rubric and Coordination Plan

Produce a `docs/fleet-review-rubric.md` that contains:
- The evaluation rubric (11 dimensions above) with scoring guidance (pass/warn/fail per dimension)
- Per-skill output template (structured markdown for findings)
- Category batch assignments with verified skill counts (reconcile against plugin.json)
- Instructions for worker agents (what to read, how to evaluate, what to output)

This task produces the coordination artifacts the fleet needs. No skill changes yet.

### Task 2: Audit Batch A — Foundation & Core C# & Project Structure

Review all skills in: core-csharp (9), foundation (4), project-structure (6), release-management (1).
Produce findings report at `docs/review-reports/batch-a-findings.md`.

### Task 3: Audit Batch B — Architecture & Serialization & Security

Review all skills in: architecture (10), serialization (4), security (3), multi-targeting (2).
Produce findings report at `docs/review-reports/batch-b-findings.md`.

### Task 4: Audit Batch C — Testing & CI/CD

Review all skills in: testing (10), cicd (8).
Produce findings report at `docs/review-reports/batch-c-findings.md`.

### Task 5: Audit Batch D — API & CLI & Performance & Native AOT

Review all skills in: api-development (5), cli-tools (5), performance (4), native-aot (4).
Produce findings report at `docs/review-reports/batch-d-findings.md`.

### Task 6: Audit Batch E — UI Frameworks & Agent Meta-Skills

Review all skills in: ui-frameworks (13), agent-meta-skills (4).
Produce findings report at `docs/review-reports/batch-e-findings.md`.

### Task 7: Audit Batch F — Documentation & Packaging & Localization

Review all skills in: documentation (5), packaging (3), localization (1).
Produce findings report at `docs/review-reports/batch-f-findings.md`.

### Task 8: Consolidate Findings and Prioritize Changes

Merge all batch findings into a single prioritized improvement plan at `docs/review-reports/consolidated-findings.md`. Identify:
- Critical issues (broken cross-refs, missing descriptions, over-budget descriptions)
- High-value improvements (better trigger phrases, clearer instructions)
- Low-priority polish (formatting, minor wording)
- Cross-cutting patterns (issues that affect many skills similarly)
- Projected description budget impact: current total, proposed total, delta vs 12K warn / 15K fail thresholds

### Task 9: Implement Improvements — Batches A+B

Apply all Critical and High-value improvements from consolidated findings to skills in Batches A and B. Commit per-category. Do not modify descriptions without verifying aggregate budget impact.

**File ownership:** Modifies only `SKILL.md` and `details.md` files within assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Validation gate:** Run `./scripts/validate-skills.sh` after all changes to catch regressions early.

### Task 10: Implement Improvements — Batches C+D

Apply all Critical and High-value improvements from consolidated findings to skills in Batches C and D. Commit per-category. Do not modify descriptions without verifying aggregate budget impact.

**File ownership:** Modifies only `SKILL.md` and `details.md` files within assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Validation gate:** Run `./scripts/validate-skills.sh` after all changes to catch regressions early.

### Task 11: Implement Improvements — Batches E+F

Apply all Critical and High-value improvements from consolidated findings to skills in Batches E and F. Commit per-category. Do not modify descriptions without verifying aggregate budget impact.

**File ownership:** Modifies only `SKILL.md` and `details.md` files within assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Validation gate:** Run `./scripts/validate-skills.sh` after all changes to catch regressions early.

### Task 12: Final Validation and Context Budget Check

**File ownership:** Sole owner of plugin.json, AGENTS.md, and README.md modifications.

- Run all four validation commands
- Check total context budget (all descriptions < 15,000 chars, warn at 12,000)
- Verify all cross-references resolve to existing skills
- Update plugin.json, AGENTS.md, README.md if any skills were added/removed/renamed
- Clean up docs/review-reports/ (keep consolidated findings, archive batch reports)

## Quick commands

- `./scripts/validate-skills.sh`
- `./scripts/validate-marketplace.sh`
- `python3 scripts/generate_dist.py --strict`
- `python3 scripts/validate_cross_agent.py`

## Task Dependencies

```
Task 1 (rubric) → Tasks 2-7 (audit, parallel) → Task 8 (consolidation) → Tasks 9-11 (implement, parallel) → Task 12 (validation)
```

- Task 1: no dependencies (first task)
- Tasks 2-7: each depends on task 1 (rubric must exist before auditing)
- Task 8: depends on tasks 2-7 (consolidation requires all audit reports)
- Tasks 9-11: each depends on task 8 (implementation requires prioritized findings); tasks 9-11 can run in parallel (disjoint file sets)
- Task 12: depends on tasks 9-11 (validation requires all implementations)

## Acceptance

- [ ] All 99 skills reviewed against the 11-dimension rubric
- [ ] Findings reports produced for all 6 batches
- [ ] Consolidated improvement plan prioritized with budget impact projection
- [ ] All Critical and High-value improvements implemented
- [ ] All four validation commands pass
- [ ] Total context budget within limits (< 15,000 chars, ideally < 12,000)
- [ ] All cross-references valid
- [ ] Clean git history with per-category commits
- [ ] Shared file ownership enforced (plugin.json, AGENTS.md, README.md only modified in task 12)

## Dependencies

- fn-28 (Skill Authoring How-To Manual) should complete first so the review rubric aligns with the documented conventions

## References

- CONTRIBUTING-SKILLS.md (produced by fn-28)
- CLAUDE.md (repo conventions)
- Anthropic's "The Complete Guide to Building Skills for Claude"
- Agent Skills open standard: https://github.com/anthropics/agent-skills
