# fn-64.10 Delete eval harness, update CI gates, smoke tests, and docs

## Description
Delete the complex eval harness, update CI gates and validator thresholds, remap smoke tests, regenerate baselines, and update all documentation and discovery metadata for the 8 consolidated skills. This is the final task — CI must pass on the combined diff of all tasks.

**Size:** M
**Files:** `tests/evals/` (delete entire directory), `tests/copilot-smoke/cases.jsonl`, `tests/copilot-smoke/baseline.json`, `tests/agent-routing/cases.json`, `.github/workflows/validate.yml`, `scripts/validate-skills.sh`, `scripts/similarity-baseline.json`, `scripts/similarity-suppressions.json`, `scripts/routing-warnings-baseline.json`, `.agents/openai.yaml`, `README.md`, `CONTRIBUTING-SKILLS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `docs/agent-routing-tests.md`

## Approach

**1. Delete eval harness**
- Delete `tests/evals/` entirely (all runners, datasets, rubrics, baselines, results, config, requirements.txt)
- This removes ~8,100 lines of Python, ~9.6MB of results/generations cache, and eliminates PyYAML eval dependency
- Git history preserves all code if ever needed

**2. Update CI gates and validator thresholds**
- `validate.yml` line 213: change `EXPECTED=131` to `EXPECTED=8`
- `validate-skills.sh`: update `--projected-skills 8`
- `validate-skills.sh`: raise `--max-desc-chars` from 120 to 600 (8 skills can have richer descriptions)
- Ensure `STRICT_REFS=1` is the default in CI validation step
- Verify `validate-marketplace.sh` passes after legacy directory deletion (manifest/filesystem consistency gate)

**3. Remap smoke tests (preserve case IDs, remap expected_skills)**
- `tests/copilot-smoke/cases.jsonl`: **preserve existing case IDs** (CI `--case-id` filter stays unchanged). Only remap `expected_skill` fields from old to new skill names. Optionally prune cases not referenced by the CI `--case-id` filter. Target ~10-15 representative cases.
- `tests/copilot-smoke/baseline.json`: regenerate after case remapping
- `tests/agent-routing/cases.json`: remap evidence paths and skill references to new names
- **Do NOT change the `--case-id` list in `validate.yml`** — it references the preserved IDs

**4. Regenerate baselines**
- Run `validate-similarity.py` to produce new `similarity-baseline.json` (fewer, more distinct skills = likely all zeros)
- Clear or regenerate `similarity-suppressions.json` (old pairs like ado-publish/gha-publish no longer exist)
- Regenerate `routing-warnings-baseline.json`

**5. Update discovery metadata**
- `.agents/openai.yaml`: update description text from "131 skills" to "8 broad skills" and update skill listing

**6. Update documentation**
- `README.md`: update skill count (line 11), category table (lines 53-76), Mermaid diagram skill counts (lines 126-150), "Agent Skill Routing Checks" section (lines 222-228)
- `AGENTS.md`: update skill count (line 28), file structure diagram (line 81)
- `CONTRIBUTING-SKILLS.md`: update skill count section (lines 117-143), description policy (120→600 chars per skill), budget math formula (lines 189-200), cross-provider verification command (lines 329-335)
- `CONTRIBUTING.md`: update cross-provider change policy command (line 247), release checklist (lines 254-263)
- `docs/agent-routing-tests.md`: trim to match surviving test infrastructure (remove eval harness references)
- `CHANGELOG.md`: add entry under [Unreleased] for skill consolidation and eval harness removal

**7. Final validation**
- Run `STRICT_REFS=1 ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` and confirm both pass
- Verify total description budget is under 3,900 chars (~25% of 15,600 cap)

## Key context

- Structural validators (`validate-skills.sh`, `validate-marketplace.sh`, `validate-similarity.py`) are the real CI gates — keep them as-is
- The eval harness never ran in CI; it was a local development tool
- With 8 skills the description budget drops from ~75% to ~10%, dramatically improving routing quality
- The similarity detector becomes MORE valuable with broader skills (higher chance of vocabulary overlap)
- Smoke test strategy: preserve existing case IDs (minimize CI filter churn), remap expected_skills to new names
- This task is the last to execute — CI must pass on the combined diff of all tasks in the single PR

## Acceptance
- [ ] `tests/evals/` directory deleted entirely
- [ ] `validate.yml` EXPECTED count updated to 8
- [ ] `validate-skills.sh --projected-skills 8` and `--max-desc-chars 600` updated
- [ ] `STRICT_REFS=1` is default in CI validation step
- [ ] Copilot smoke `cases.jsonl`: existing case IDs preserved, `expected_skill` fields remapped to 8-skill names
- [ ] CI `--case-id` filter in `validate.yml` NOT changed (it references preserved IDs)
- [ ] Copilot smoke `baseline.json` regenerated
- [ ] Agent routing `cases.json` remapped to new skill names
- [ ] `similarity-baseline.json` regenerated
- [ ] `similarity-suppressions.json` updated (old pairs removed)
- [ ] `routing-warnings-baseline.json` regenerated
- [ ] `.agents/openai.yaml` updated for 8 skills
- [ ] README.md updated (skill count, category table, Mermaid diagram)
- [ ] AGENTS.md updated (skill count, file structure)
- [ ] CONTRIBUTING-SKILLS.md updated (count, description policy 120→600, budget math, verification commands)
- [ ] CONTRIBUTING.md updated (cross-provider command, release checklist)
- [ ] `docs/agent-routing-tests.md` updated for surviving test infrastructure
- [ ] `validate-skills.sh && validate-marketplace.sh` both pass on combined diff
- [ ] Total description budget under 3,900 chars (~25% of 15,600 cap)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
