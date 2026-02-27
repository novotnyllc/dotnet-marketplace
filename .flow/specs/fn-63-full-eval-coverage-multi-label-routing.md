# Full Eval Coverage: Multi-Label Routing + Content Quality for All 131 Skills

## Overview

fn-60 built eval infrastructure and fixed ~21 skills. But only 81/131 skills have activation test cases, only 12 have effectiveness rubrics, and the confusion matrix eval forces single-label selection on a multi-label router. **The router returns several skills per query, not one.** Skills compose — "write xUnit integration tests for EF Core" should route to dotnet-xunit + dotnet-integration-testing + dotnet-efcore-patterns.

This epic closes three gaps:
1. **Coverage**: Every skill gets activation test cases and effectiveness rubrics (not just the ~20% that had them)
2. **Scoring**: Activation eval switches from "any match" to set-based precision/recall/F1 (multi-label)
3. **Confusion matrix**: Retired — replaced by multi-label activation which covers the same ground without the false mutual-exclusivity assumption

**Core workflow**: Process skills in batches of 3-5. Each batch: generate test cases → run eval → fix issues → verify → commit → next batch. eval-progress.json tracks all 131 skills so work resumes across sessions.

Supersedes fn-60 tasks .4/.5/.6 (content fixes, quality bar, baselines). fn-60 tasks .1-.3 and .7-.9 were infrastructure that remains valid.

## Approach

### Phase 1: Infra (Task .1)
- Write script to auto-generate activation test cases from skill SKILL.md (description + scope + out-of-scope sections)
- Generate 2-3 positive + 1 negative case per skill for all 50 uncovered skills
- Redesign activation scoring: set-based F1 (precision = correct activations / total activations, recall = activated expected / total expected)
- Add `required_skills` support: when present, ALL listed skills must activate for a pass (not just any)
- Retire confusion matrix runner (`run_confusion_matrix.py`) — multi-label activation replaces it
- Update `run_suite.sh` and quality bar thresholds

### Phase 2: Full Activation + Routing Fixes (Tasks .2, .3)
- Run activation across ALL test cases (existing 73 + ~150 new auto-generated)
- Initialize eval-progress.json for all 131 skills
- Triage by severity: missing activation > wrong activation > low F1
- Fix routing descriptions in batches of 3-5
- Special handling for 4 `context: fork` skills (dotnet-version-detection, dotnet-solution-navigation, dotnet-project-analysis, dotnet-build-analysis) — these auto-load, test differently
- Exempt dotnet-advisor (always-loaded meta-router) from standard activation testing
- Verify each batch with targeted re-runs

### Phase 3: Rubric Expansion + Content Fixes (Tasks .4, .5)
- Auto-generate baseline effectiveness rubrics from skill body content (criteria derived from skill's key concepts, APIs, patterns)
- Generate in batches of ~30 skills, run effectiveness, fix content issues
- Refine rubrics that produce suspicious results (100% win rate = too easy, 0% = too hard)
- Fix content in batches of 3-5 skills, verify with `--regenerate`

### Phase 4: Verification + Baselines (Task .6)
- Full-coverage activation run, verify quality bar
- Full-coverage effectiveness run for all rubric'd skills
- Run size impact on expanded candidate list
- Save baselines for regression tracking
- Final eval-progress.json audit: all 131 skills verified

## Quality Bar

### L3 Activation (multi-label, set-based)
- Mean F1 >= 0.70 across all positive cases
- Per-case precision >= 0.50 (no case activates mostly wrong skills)
- FPR <= 20% on negative controls
- No skill with 0% recall across all its test cases (every skill must activate somewhere)

### L5 Effectiveness
- No skill at 0% win rate without documented variance exception (min n=6)
- Per-skill win rate target >= 50%
- Aggregate micro-average win rate tracked (not gating)

### L6 Size Impact
- No baseline sweep (no skill where baseline wins all runs)
- full > baseline in >= 55% of comparisons

### L4 Confusion — RETIRED
Replaced by multi-label activation (L3) with set-based F1. The confusion matrix assumed mutual exclusivity; skills are composable.

## Special Skill Categories

| Category | Skills | Eval Treatment |
|----------|--------|----------------|
| Always-loaded meta-router | dotnet-advisor | Exempt from activation; test that it correctly delegates |
| Auto-load fork context | dotnet-version-detection, dotnet-solution-navigation, dotnet-project-analysis, dotnet-build-analysis | Test activation differently — these are auto-invoked, not user-triggered |
| User-invocable (11 skills) | dotnet-advisor, dotnet-scaffold-project, dotnet-ui-chooser, etc. | Test with direct user request prompts |
| Standard (120 skills) | All others | Standard activation + effectiveness eval |

## Quick Commands

```bash
# Generate activation cases for uncovered skills
python3 tests/evals/scripts/generate_activation_cases.py --uncovered-only

# Run activation on all cases
python3 tests/evals/run_activation.py

# Run activation for specific skill
python3 tests/evals/run_activation.py --skill dotnet-xunit

# Run effectiveness for specific skill
python3 tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 1 --regenerate

# Generate rubrics for uncovered skills
python3 tests/evals/scripts/generate_rubrics.py --uncovered-only --batch-size 30

# Validate skills after edits
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

## Scope

**In scope:**
- Auto-generating activation test cases for all 50 uncovered skills
- Redesigning activation scoring to multi-label (set-based F1)
- Retiring confusion matrix eval
- Running activation across all 131 skills and fixing routing issues
- Auto-generating effectiveness rubrics for uncovered skills
- Running effectiveness and fixing content issues
- Full-coverage baselines
- Supersedes fn-60 tasks .4/.5/.6

**Out of scope:**
- New eval types beyond L3/L5/L6
- CI workflow integration (fn-58.4)
- Subprocess timeout fixes (fn-62 — work around with targeted runs)
- Hand-crafting individual rubrics (auto-generate then refine)

## Acceptance

- [ ] All 131 skills have activation test cases (0 uncovered)
- [ ] Activation scoring uses set-based F1 (precision/recall), not "any match"
- [ ] Confusion matrix runner retired, removed from run_suite.sh and quality bar
- [ ] Multi-skill composition cases exist (prompts expecting 2-3 skills to co-activate)
- [ ] eval-progress.json tracks all 131 skills with routing_status and content_status
- [ ] L3 quality bar met: mean F1 >= 0.70, FPR <= 20%, no 0-recall skills
- [ ] All skills with effectiveness rubrics meet L5 bar: per-skill win rate >= 50%
- [ ] No L6 baseline sweeps
- [ ] Full-coverage baselines saved to tests/evals/baselines/
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass

## Dependencies

- **fn-62** (subprocess timeouts): Soft dependency — work around with targeted `--skill` runs which are less timeout-prone. Full-coverage runs in task .6 may need fn-62 complete.
- **fn-60**: Tasks .1-.3, .7-.9 remain valid infrastructure. Tasks .4-.6 superseded by this epic.

## Risks

| Risk | Mitigation |
|------|------------|
| Auto-generated test cases are ambiguous or wrong | Validate with activation dry-run; human review 10% sample; flaky cases marked `exception` and refined later |
| Auto-generated rubrics too generic → meaningless L5 results | Derive criteria from skill body content (specific APIs, patterns); flag 100% win rate rubrics for refinement |
| 131-skill runs hit subprocess timeouts | Use targeted `--skill` runs in batches; fn-62 fixes the root cause |
| Description edits for routing break other skills | validate-skills.sh after each batch; targeted re-runs; description budget check |
| Cost explosion at 131-skill scale | Per-runner budget caps in config.yaml; batch processing limits blast radius; targeted runs minimize calls |
| Multi-label scoring invalidates existing baselines | Clean break — new baselines from full-coverage multi-label runs; old single-label results archived |
| Rubric expansion is unbounded work | Auto-generate baseline rubrics; prioritize by skill usage frequency; accept "good enough" over "perfect" |
