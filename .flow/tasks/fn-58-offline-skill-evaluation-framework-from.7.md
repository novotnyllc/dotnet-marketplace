# fn-58-offline-skill-evaluation-framework-from.7 Expanded negative controls and confusion matrix tests

## Description

Expand negative controls and build confusion matrix tests (L4 runner) that validate skill disambiguation quality at scale. Uses shared infrastructure from `_common.py` (task .1) and structured JSON activation approach from task .5.

**Size:** M
**Files:**
- `tests/evals/datasets/confusion/confusion_matrix.jsonl` (prompts designed to test disambiguation)
- `tests/evals/datasets/confusion/negative_controls_expanded.jsonl` (additional negative controls)
- `tests/evals/run_confusion_matrix.py` (flesh out skeleton from task .1 — L4 runner)

## Approach

- **Confusion matrix tests**: Group skills by domain overlap, create prompts that could plausibly match 2-3 skills:
  - Testing: `dotnet-xunit`, `dotnet-testing-strategy`, `dotnet-integration-testing`, `dotnet-snapshot-testing`, `dotnet-test-quality`
  - Security: `dotnet-security-owasp`, `dotnet-api-security`, `dotnet-secrets-management`, `dotnet-cryptography`
  - Data: `dotnet-efcore-patterns`, `dotnet-efcore-architecture`, `dotnet-data-access-strategy`
  - Performance: `dotnet-performance-patterns`, `dotnet-benchmarkdotnet`, `dotnet-profiling`, `dotnet-gc-memory`
  - API: `dotnet-minimal-apis`, `dotnet-api-versioning`, `dotnet-openapi`, `dotnet-input-validation`
  - CI/CD: `dotnet-gha-patterns`, `dotnet-gha-build-test`, `dotnet-gha-publish`, `dotnet-gha-deploy`
  - Blazor: `dotnet-blazor-patterns`, `dotnet-blazor-components`, `dotnet-blazor-auth`, `dotnet-blazor-testing`

- **Confusion JSONL schema**:
  ```
  {"id": "cm-001", "group": "testing", "user_prompt": "...", "expected_skill": "dotnet-xunit", "acceptable_skills": ["dotnet-testing-strategy"]}
  ```

- **Multi-label scoring rule**: The structured JSON response returns `{"skills": [...]}`. Evaluation:
  - If `skills` is empty: classify as `no_activation`
  - If `skills` has exactly 1 entry: use that as the predicted skill
  - If `skills` has 2+ entries: classify as `multi_activation`, use `skills[0]` as primary prediction, record all for matrix
  - Pass = `skills[0]` matches `expected_skill` OR is in `acceptable_skills`
  - For the NxN matrix: increment cell `[expected][predicted]` for `skills[0]`; separately track `multi_activation` and `no_activation` counts per group

- **Expanded negative controls**: 15+ prompts for non-.NET topics + "temptation" prompts

- **Analysis**: Per group, build NxN activation matrix. Two threshold types:
  - **Finding flag** (absolute, in report): `absolute_cross_activation > 20%` — flags skills that are frequently confused in the current run
  - **Regression flag** (delta, in `compare_baseline.py`): `delta_cross_activation > 10%` — flags skills whose confusion rate increased vs baseline (uses `confusion.cross_activation_change_threshold` from config)
  - Also flag: low discrimination (2+ skills activated equally), never-activated skills, high `multi_activation` or `no_activation` rates

- Uses same structured JSON response as `run_activation.py` (task .5)
- CLI: `--group <name>` to filter; `--dry-run` to preview without API calls
- Confusion datasets stored under `datasets/confusion/` (separate from activation datasets)
- Results follow the common envelope from `_common.py`: `entity_id` = `group_name`

## Key context

- 131 skills x 21+ categories = exponentially more confusion risk than reference (5 skills).
- Existing similarity detection catches text overlap; confusion matrix catches functional overlap.
- Temptation prompts must naturally overlap with the disallowed skill domain to be testable.

## Acceptance
- [ ] At least 7 domain groups with 3-5 skills each
- [ ] At least 5 confusion matrix prompts per group (35+ total)
- [ ] At least 15 expanded negative control prompts (non-.NET + temptation)
- [ ] `run_confusion_matrix.py` (L4) produces per-group NxN activation matrices
- [ ] `--dry-run` mode shows planned cases without API calls
- [ ] `--group <name>` filters to a single domain group
- [ ] Cross-activation > 20% flagged in report
- [ ] Low-discrimination cases flagged in report
- [ ] Per-prompt breakdown in results: prompt, expected_skill, actual_activations, pass/fail
- [ ] Results include `mean`, `stddev`, `n` per group per metric
- [ ] Report includes "Findings" section listing top cross-activations and low-discrimination prompts (even if empty)
- [ ] Uses structured JSON response approach from task .5
- [ ] Confusion datasets stored under `datasets/confusion/` (not `datasets/activation/`)
## Done summary
Implemented L4 confusion matrix eval runner with 36 prompts across 7 domain groups (testing, security, data, performance, api, cicd, blazor), 18 expanded negative controls (non-.NET + temptation), per-group NxN confusion matrices with locked axes, cross-activation flagging (>20%), index violation tracking, never-activated skill detection, prompt-level low-discrimination findings, and --dry-run/--group CLI support.
## Evidence
- Commits: fe456770, 1afbf78c, 3ee307d5, d3b61fa7
- Tests: python3 tests/evals/run_confusion_matrix.py --dry-run, python3 tests/evals/run_confusion_matrix.py --dry-run --group testing, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: