# fn-29-fleet-skill-review-and-improvement-sweep.6 Audit Batch E: UI Frameworks, Agent Meta-Skills

## Description

Review all skills in: ui-frameworks (13), agent-meta-skills (4) — 17 skills total. Evaluate each against the 11-dimension rubric from `docs/fleet-review-rubric.md`. Produce findings report using the same structure as batch-a-findings.md (summary table, per-skill evaluations, cross-cutting observations, recommended changes).

### Files

- **Input:** All `SKILL.md` files under `skills/ui-frameworks/`, `skills/agent-meta-skills/`
- **Rubric:** `docs/fleet-review-rubric.md`
- **Reference template:** `docs/review-reports/batch-a-findings.md`
- **Output:** `docs/review-reports/batch-e-findings.md`

## Acceptance
- [ ] All 17 skills in batch evaluated against all 11 rubric dimensions
- [ ] Findings report at `docs/review-reports/batch-e-findings.md` follows batch-a-findings.md structure: Summary table (Skills reviewed, Clean, Needs Work, Critical), Current Description Budget Impact, per-skill sections (verdict + issues + proposed changes), cross-cutting observations, recommended changes
- [ ] Each skill has a pass/warn/fail rating per dimension with justification
- [ ] Cross-references validated (all `[skill:name]` refs point to existing skills)
- [ ] Description lengths measured and aggregate budget impact noted
- [ ] Issues tagged by severity: Critical (broken refs, budget violations), High, Low

## Done summary
Audited 17 skills in Batch E (13 ui-frameworks + 4 agent-meta-skills) against the 11-dimension rubric. Found 3 Clean, 10 Needs Work, 4 Critical. Key findings: 4 agent-meta-skills have descriptions over 140 chars (fail), 7 ui-frameworks skills have stale "(may not exist yet)" markers on AOT skills that now exist.
## Evidence
- Commits: 12dab990c1c2bdb4c0b6a4128d26c7e3b80ff8fd
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: