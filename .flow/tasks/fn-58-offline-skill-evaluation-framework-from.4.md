# fn-58-offline-skill-evaluation-framework-from.4 CI workflow, baseline regression, and documentation

## Description

Add a GitHub Actions workflow for scheduled evals (all 4 eval types), implement baseline regression tracking (informational, exit 0 always), and update all affected documentation. This is the final integration task — depends on all runners being complete.

**Size:** M
**Files:**
- `.github/workflows/skill-evals.yml` (new workflow: weekly schedule + manual trigger ONLY — NOT on PR/push events)
- `tests/evals/compare_baseline.py` (flesh out skeleton from task .1)
<!-- Updated by plan-sync: fn-58...from.2 — compare_baseline.py uses f"{eval_type}_baseline.json" (underscores, not hyphens) -->
- `tests/evals/baselines/effectiveness_baseline.json` (initial baseline)
- `tests/evals/baselines/activation_baseline.json` (initial baseline)
- `tests/evals/baselines/confusion_baseline.json` (initial baseline)
- `tests/evals/baselines/size_impact_baseline.json` (initial baseline)
- `CONTRIBUTING-SKILLS.md` (new section on skill evals in Section 5)
- `AGENTS.md` (update file structure and validation commands)
- `docs/skill-eval-framework.md` (new reference doc)
- `README.md` (update testing section)
- `CHANGELOG.md` (add entry under [Unreleased])

## Approach

- **Workflow is NOT part of validate.yml and does NOT run on PR/push events.** Only `schedule` (weekly cron) and `workflow_dispatch` (manual).
- Workflow follows the pattern of `.github/workflows/agent-live-routing.yml:1` — secret-gated, artifact upload
- Workflow runs all 4 eval types sequentially: L3 activation -> L4 confusion -> L5 effectiveness -> L6 size impact
- **Informational regression detection** (exit 0 always), dispatched per eval type:
  - **L5 Effectiveness**: `mean_drop > effectiveness.mean_drop_threshold AND drop > effectiveness.stddev_multiplier * stddev` (per-skill, min `effectiveness.min_cases_before_compare` cases)
  - **L3 Activation**: compare `tpr_mean` / `fpr_mean` deltas vs `activation.tpr_drop_threshold` / `activation.fpr_increase_threshold` (per-skill, min `activation.min_cases_before_compare` cases)
  - **L4 Confusion**: compare `cross_activation_rate_mean` delta vs `confusion.cross_activation_change_threshold` (per-group, min `confusion.min_cases_before_compare` cases)
  - **L6 Size Impact**: compare `size_impact_score_mean` delta vs `size_impact.score_change_threshold` (per-skill, min `size_impact.min_cases_before_compare` cases)
  - New entities (absent from baseline) treated as "new coverage", not regressions
  - All 4 eval types have baseline files (even if initially sparse)
  - **Baseline file format**: each stores the `summary` object (plus a small `meta` header with run_id/timestamp). `compare_baseline.py` ignores `cases` and `artifacts` fields.
- Workflow uploads eval results AND generation artifacts
- Layer naming consistent: L3=activation, L4=confusion, L5=effectiveness, L6=size impact
- Workflow installs eval deps via `pip install -r tests/evals/requirements.txt` explicitly
- Doc updates follow existing patterns from docs-gap-scout analysis

## Key context

- `GITHUB_BASE_REF` is empty for `workflow_dispatch`/`schedule` — use committed baseline files.
- In GHA with `set -euo pipefail`, use `set +e` before capturing exit codes.
- New baseline entries are "new coverage", not failures.

## Acceptance
- [ ] `.github/workflows/skill-evals.yml` exists with ONLY `schedule` and `workflow_dispatch` triggers — NO `pull_request` or `push`
- [ ] Workflow is NOT part of validate.yml
- [ ] Workflow skips gracefully when `ANTHROPIC_API_KEY` secret is not set (fork-safe)
- [ ] Workflow runs all 4 eval types: L3 activation, L4 confusion, L5 effectiveness, L6 size impact
- [ ] Baseline files exist for all 4 eval types (even if initially sparse)
- [ ] Eval results AND generation artifacts uploaded as GitHub Actions artifacts
- [ ] `compare_baseline.py` always exits 0 (informational only)
- [ ] Regression detection uses per-eval-type thresholds from `config.yaml`
- [ ] Per-skill minimum `n` cases enforced per eval type before regression comparison
- [ ] New skills treated as "new coverage", not failures
- [ ] Results include `mean`, `stddev`, `n` per skill per metric
- [ ] `CONTRIBUTING-SKILLS.md` Section 5 includes rubric authoring instructions with `test_prompts` requirement
- [ ] `AGENTS.md` file structure and validation commands updated
- [ ] `docs/skill-eval-framework.md` exists with Files/Commands/Concepts structure, documents L3-L6
- [ ] `README.md` testing section references the eval framework
- [ ] `CHANGELOG.md` has `### Added` entry under `## [Unreleased]`
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
