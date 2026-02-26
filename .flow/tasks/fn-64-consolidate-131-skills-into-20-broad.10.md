# fn-64-consolidate-131-skills-into-20-broad.10 Update CI gates, validation, docs and regenerate eval baselines

## Description
Delete the complex eval harness, update CI gates, remap smoke tests, regenerate baselines, and update all documentation for the consolidated skill set.

**Size:** M
**Files:** `tests/evals/` (delete entire directory), `tests/copilot-smoke/cases.jsonl`, `tests/copilot-smoke/baseline.json`, `tests/agent-routing/cases.json`, `.github/workflows/validate.yml`, `scripts/validate-skills.sh`, `scripts/similarity-baseline.json`, `scripts/similarity-suppressions.json`, `scripts/routing-warnings-baseline.json`, `README.md`, `CONTRIBUTING-SKILLS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `docs/agent-routing-tests.md`

## Approach

**1. Delete eval harness**
- Delete `tests/evals/` entirely (all runners, datasets, rubrics, baselines, results, config, requirements.txt)
- This removes ~8,100 lines of Python, ~9.6MB of results/generations cache, and eliminates PyYAML eval dependency
- Git history preserves all code if ever needed

**2. Update CI gates**
- `validate.yml` line 213: change `EXPECTED=131` to actual consolidated count
- `validate-skills.sh`: update `--projected-skills` argument
- `validate.yml` copilot-smoke job (lines 287-433): update hardcoded `--case-id` filter to reference new case IDs
- Ensure `STRICT_REFS=1` is the default in CI (catches broken cross-refs post-consolidation)

**3. Remap smoke tests**
- `tests/copilot-smoke/cases.jsonl`: remap all `expected_skill` fields from old to new skill names, reduce to ~10-15 representative cases (1 per consolidated skill + negative controls)
- `tests/copilot-smoke/baseline.json`: regenerate after case remapping
- `tests/agent-routing/cases.json`: remap evidence paths and skill references to new names

**4. Regenerate baselines**
- Run `validate-similarity.py` to produce new `similarity-baseline.json` (fewer, more distinct skills = likely all zeros)
- Clear or regenerate `similarity-suppressions.json` (old pairs like ado-publish/gha-publish no longer exist)
- Regenerate `routing-warnings-baseline.json`

**5. Update documentation**
- `README.md`: update skill count (line 11), category table (lines 53-76), Mermaid diagram skill counts (lines 126-150), "Agent Skill Routing Checks" section (lines 222-228)
- `AGENTS.md`: update skill count (line 28), file structure diagram (line 81)
- `CONTRIBUTING-SKILLS.md`: update Copilot 32-skill section count (lines 117-143), budget math formula (lines 189-200), cross-provider verification command (lines 329-335)
- `CONTRIBUTING.md`: update cross-provider change policy command (line 247), release checklist (lines 254-263)
- `docs/agent-routing-tests.md`: trim to match surviving test infrastructure (remove eval harness references)
- `CHANGELOG.md`: add entry under [Unreleased] for skill consolidation and eval harness removal

## Key context

- Structural validators (`validate-skills.sh`, `validate-marketplace.sh`, `validate-similarity.py`) are the real CI gates — keep them as-is
- The eval harness never ran in CI; it was a local development tool
- With ~20 skills the description budget drops from ~75% to ~15-20%, dramatically improving routing quality
- The similarity detector becomes MORE valuable with broader skills (higher chance of vocabulary overlap)
- All eval JSONL datasets, rubrics, and baselines reference old 131-skill names — remapping would be as much work as deletion, with no CI benefit
## Approach

1. **CI gates**: Update `EXPECTED=N` in `validate.yml:213`, `--projected-skills N` in `validate-skills.sh:71` to match actual consolidated count
2. **Similarity baseline**: Regenerate `similarity-baseline.json` (all zeros expected with fewer, more distinct skills)
3. **Similarity suppressions**: Update or clear `similarity-suppressions.json` (old ado-publish/gha-publish pair no longer exists)
4. **Routing warnings baseline**: Regenerate `routing-warnings-baseline.json`
5. **Eval datasets**: Remap all `expected_skills`, `acceptable_skills`, `expected_skill` fields from old names to new names across activation (73 cases), confusion (54 cases), effectiveness (12 rubrics), size_impact (11 candidates)
6. **Confusion matrix**: Rewrite `DOMAIN_GROUPS` dict in `run_confusion_matrix.py:46-88` for ~20 skills (may simplify significantly)
7. **Copilot smoke tests**: Remap `cases.jsonl` and `baseline.json` (29 cases)
8. **Agent routing tests**: Remap `cases.json` evidence paths
9. **Documentation**: Update skill count and catalog in README.md, CONTRIBUTING-SKILLS.md, AGENTS.md

## Key context

- Description budget drops from ~75% to ~15-20% — significant routing quality improvement
- Confusion matrix eval concept may simplify dramatically with only ~20 skills (fewer overlapping domains)
- Eval dataset remapping is data changes only — no running of actual eval suites here
## Approach

1. **CI gates**: Update `EXPECTED=N` in `validate.yml:213`, `--projected-skills N` in `validate-skills.sh:71` to match actual consolidated count
2. **Similarity baseline**: Regenerate `similarity-baseline.json` (all zeros expected with fewer, more distinct skills)
3. **Similarity suppressions**: Update or clear `similarity-suppressions.json` (old ado-publish/gha-publish pair no longer exists)
4. **Routing warnings baseline**: Regenerate `routing-warnings-baseline.json`
5. **Eval datasets**: Remap all `expected_skills`, `acceptable_skills`, `expected_skill` fields from old names to new names across activation (73 cases), confusion (54 cases), effectiveness (12 rubrics), size_impact (11 candidates)
6. **Confusion matrix**: Rewrite `DOMAIN_GROUPS` dict in `run_confusion_matrix.py:46-88` for ~20 skills (may simplify significantly)
7. **Copilot smoke tests**: Remap `cases.jsonl` and `baseline.json` (29 cases)
8. **Agent routing tests**: Remap `cases.json` evidence paths
9. **Documentation**: Update skill count and catalog in README.md, CONTRIBUTING-SKILLS.md, AGENTS.md
10. **Run full eval suite**: All 4 types (activation, confusion, effectiveness, size_impact), save new baselines

## Key context

- Description budget drops from ~75% to ~15-20% — significant routing quality improvement
- Confusion matrix eval concept may simplify dramatically with only ~20 skills (fewer overlapping domains)
- Eval baselines from fn-60 must be fully regenerated — old baselines are keyed by old skill names
## Acceptance
- [ ] `tests/evals/` directory deleted entirely
- [ ] `validate.yml` EXPECTED count updated to match actual consolidated skill count
- [ ] `validate-skills.sh --projected-skills` updated to new count
- [ ] `STRICT_REFS=1` is default in CI validation step
- [ ] Copilot smoke `cases.jsonl` remapped to new skill names (~10-15 cases)
- [ ] Copilot smoke `baseline.json` regenerated
- [ ] Agent routing `cases.json` remapped to new skill names
- [ ] `similarity-baseline.json` regenerated
- [ ] `similarity-suppressions.json` updated (old pairs removed)
- [ ] `routing-warnings-baseline.json` regenerated
- [ ] README.md updated (skill count, category table, Mermaid diagram)
- [ ] AGENTS.md updated (skill count, file structure)
- [ ] CONTRIBUTING-SKILLS.md updated (count, budget math, verification commands)
- [ ] CONTRIBUTING.md updated (cross-provider command, release checklist)
- [ ] `docs/agent-routing-tests.md` updated for surviving test infrastructure
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` both pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
