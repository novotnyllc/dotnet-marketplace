# fn-29-fleet-skill-review-and-improvement-sweep.5 Audit Batch D: API, CLI, Performance, Native AOT

## Description

Review all skills in: api-development (5), cli-tools (5), performance (4), native-aot (4) — 18 skills total. Evaluate each against the 11-dimension rubric from `docs/fleet-review-rubric.md`. Produce findings report using the same structure as batch-a-findings.md (summary table, per-skill evaluations, cross-cutting observations, recommended changes).

### Files

- **Input:** All `SKILL.md` files under `skills/api-development/`, `skills/cli-tools/`, `skills/performance/`, `skills/native-aot/`
- **Rubric:** `docs/fleet-review-rubric.md`
- **Reference template:** `docs/review-reports/batch-a-findings.md`
- **Output:** `docs/review-reports/batch-d-findings.md`

## Acceptance
- [ ] All 18 skills in batch evaluated against all 11 rubric dimensions
- [ ] Findings report at `docs/review-reports/batch-d-findings.md` follows batch-a-findings.md structure: Summary table (Skills reviewed, Clean, Needs Work, Critical), Current Description Budget Impact, per-skill sections (verdict + issues + proposed changes), cross-cutting observations, recommended changes
- [ ] Each skill has a pass/warn/fail rating per dimension with justification
- [ ] Cross-references validated (all `[skill:name]` refs point to existing skills)
- [ ] Description lengths measured and aggregate budget impact noted
- [ ] Issues tagged by severity: Critical (broken refs, budget violations), High, Low

## Done summary
Audited 18 skills across api-development (5), cli-tools (5), performance (4), and native-aot (4) against the 11-dimension rubric. Produced batch-d-findings.md: 13 Clean, 4 Needs Work, 1 Critical (dotnet-ci-benchmarking at 144 chars). Key issues: description budget overages, one bare backtick cross-ref, one stale "not yet landed" reference.
## Evidence
- Commits: 0218c44, 1d4b6b4
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: