# fn-63-full-eval-coverage-multi-label-routing.1 Multi-label scoring + test case generation + retire confusion matrix

## Description
Three infrastructure changes that all downstream tasks depend on:

**1. Auto-generate activation test cases for 50 uncovered skills.**
Write `tests/evals/scripts/generate_activation_cases.py` that:
- Reads each skill's SKILL.md (description + `## Scope` + `## Out of scope` sections)
- Uses an LLM (haiku via CLI) to generate 2-3 positive test prompts and 1 negative per skill
- Includes multi-skill composition cases: prompts that should activate 2-3 related skills together (e.g., `expected_skills: ["dotnet-xunit", "dotnet-integration-testing"]`)
- Outputs to `tests/evals/datasets/activation/auto_generated.jsonl` in the same schema as `core_skills.jsonl`
- Uses existing 73 hand-written cases as few-shot examples for quality
- Validates generated cases: no references to non-existent skills, no duplicate IDs, JSONL schema compliance
- Skips dotnet-advisor (always-loaded meta-router) and 4 fork-context skills (they auto-load, don't compete for routing)

**2. Redesign activation scoring for multi-label routing.**
The router returns SEVERAL skills, not one. Current scoring at `run_activation.py:706-708` passes if ANY expected skill is in the activated set. Change to set-based precision/recall/F1:
- `precision = |activated ∩ valid| / |activated|` (of skills activated, how many were correct?)
- `recall = |activated ∩ expected| / |expected|` (of expected skills, how many activated?)
- `F1 = 2 * precision * recall / (precision + recall)`
- Keep existing `expected_skills` + `acceptable_skills` semantics: expected = must activate, acceptable = also valid
- A case passes when F1 > 0 (at least one correct skill activated)
- Add aggregate metrics: mean F1, mean precision, mean recall across all positive cases
- Update per-case result JSON to include `precision`, `recall`, `f1` fields

**3. Retire confusion matrix runner.**
The confusion matrix forces single-skill selection ("Select ONLY the single most relevant skill" at `run_confusion_matrix.py:99`). Skills compose, they don't compete. Multi-label activation replaces this eval dimension.
- Remove `run_confusion_matrix.py` from `run_suite.sh`
- Remove L4 confusion thresholds from quality bar
- Keep `run_confusion_matrix.py` file (don't delete) but mark deprecated with a comment
- Update `config.yaml` regression section: remove confusion entries

**Depends on:** nothing (first task)
**Size:** M
**Files:**
- `tests/evals/scripts/generate_activation_cases.py` (new)
- `tests/evals/datasets/activation/auto_generated.jsonl` (new)
- `tests/evals/run_activation.py` (scoring redesign)
- `tests/evals/run_suite.sh` (remove confusion runner)
- `tests/evals/config.yaml` (remove confusion regression thresholds)

## Approach

- Generation script: follow pattern at `run_activation.py:35-76` (`build_routing_index`) for skill loading. Use `_common.load_skill_description()` and `_common.load_skill_body()` for content extraction.
- Scoring redesign: modify `compute_metrics()` at `run_activation.py:276-365`. Keep backward compatibility — old metrics (TPR, FPR, accuracy) still computed alongside new F1 metrics.
- Multi-skill composition cases: generate using skill's `## Scope` to identify natural co-activation patterns (e.g., skills that reference each other via `[skill:...]` cross-refs in their body).
- Test case validation: run `--dry-run` to verify all expected_skills exist in the routing index.

## Key context

- Activation dataset schema: `{"id", "user_prompt", "expected_skills", "acceptable_skills", "should_activate", "category"}` — see `datasets/activation/core_skills.jsonl`
- The 4 fork-context skills: dotnet-version-detection, dotnet-solution-navigation, dotnet-project-analysis, dotnet-build-analysis — these have `context: fork` and `model: haiku` in frontmatter
- Cross-ref syntax `[skill:name]` in skill bodies identifies natural skill pairs for composition cases
- Memory pitfall: eval runners exit 0 even on partial runs. Validate case counts, not just exit code.
## Acceptance
- [ ] `generate_activation_cases.py` script exists and generates test cases for all 50 uncovered skills
- [ ] Auto-generated cases follow same JSONL schema as `core_skills.jsonl`
- [ ] At least 10 multi-skill composition cases exist (prompts with 2+ expected_skills)
- [ ] dotnet-advisor and 4 fork-context skills excluded from standard activation generation
- [ ] No generated case references a non-existent skill
- [ ] Activation scoring computes set-based F1 (precision + recall) per case
- [ ] Per-case result JSON includes `precision`, `recall`, `f1` fields
- [ ] Aggregate metrics include mean F1, mean precision, mean recall
- [ ] `run_confusion_matrix.py` removed from `run_suite.sh`
- [ ] L4 confusion thresholds removed from quality bar
- [ ] `config.yaml` confusion regression section removed
- [ ] `--dry-run` validates all generated cases without CLI calls
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` pass
## Done summary
Cancelled — superseded by skill consolidation effort.
## Evidence
- Commits:
- Tests:
- PRs: