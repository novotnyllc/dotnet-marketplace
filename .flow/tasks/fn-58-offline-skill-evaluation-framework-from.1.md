# fn-58-offline-skill-evaluation-framework-from.1 Scaffold eval directory, rubric schema, and runner skeleton

## Description
Scaffold the `tests/evals/` directory structure, define the rubric contract, create the eval configuration, build the shared infrastructure module, and create the skeleton Python runners that later tasks will flesh out.

**Size:** M
**Files:**
- `tests/evals/_common.py` (shared module: config loading, Anthropic client wrapper, retry/backoff with jitter, token/cost accounting, run_id/timestamps, JSON extraction from LLM responses, output writing, skill content loading with frontmatter stripping)
- `tests/evals/run_effectiveness.py` (skeleton runner with CLI args, config loading, dry-run mode)
- `tests/evals/run_activation.py` (skeleton runner)
- `tests/evals/run_size_impact.py` (skeleton runner)
- `tests/evals/run_confusion_matrix.py` (skeleton runner)
- `tests/evals/compare_baseline.py` (baseline comparison utility — informational, exit 0)
- `tests/evals/config.yaml` (eval configuration: models, temperature, retry policy, cost limits, RNG seed, per-eval-type regression thresholds)
- `tests/evals/rubric_schema.yaml` (documentation of rubric contract — not a formal JSON Schema)
- `tests/evals/validate_rubrics.py` (custom Python rubric validation — no jsonschema dep)
- `tests/evals/rubrics/` (empty directory, populated by task .2)
- `tests/evals/baselines/` (empty directory for baseline JSON files)
- `tests/evals/results/` (output directory for eval results, generations stored separately from judge scores)
- `tests/evals/datasets/activation/` (JSONL files for L3 activation evals)
- `tests/evals/datasets/confusion/` (JSONL files for L4 confusion matrix evals)
- `tests/evals/datasets/size_impact/` (candidate configs for L6)
- `tests/evals/reports/` (output directory for human-readable reports)
- `tests/evals/requirements.txt` (Python dependencies)

## Approach

- **Shared module `_common.py`** is the backbone — all runners import from it. Contains:
  - `load_config()`: Read config.yaml, merge env var overrides (`ANTHROPIC_API_KEY`). Note: `OPENROUTER_API_KEY` is reserved for future use and unused in this epic.
  - `get_client()`: Anthropic client wrapper with configurable model
  - `retry_with_backoff()`: Exponential backoff with jitter, configurable max retries
  - `extract_json()`: Extract first top-level `{...}` block from LLM response via regex, then `json.loads`. Returns parsed dict or None.
  - `load_skill_body()`: Read SKILL.md, strip YAML frontmatter (everything between first/second `---`), return body with explicit delimiters
  - `load_skill_description()`: Read SKILL.md frontmatter, return description string
  - `build_run_metadata()`: Generate run_id, timestamp, model info, RNG seed
  - `track_cost()`: Token counting and cost estimation per API call
  - `write_results()`: JSON output with generations and judge scores in separate files

- Runner skeletons follow the pattern of `tests/copilot-smoke/run_smoke.py:1` — argparse CLI with common flags: `--dry-run`, `--model`, `--judge-model`, `--runs`, `--seed`. L3/L5/L6 runners accept `--skill`; L4 runner accepts `--group`.

- **Rubric contract** (documented in `rubric_schema.yaml`, enforced by `validate_rubrics.py`):
  - Required fields: `skill_name` (string, must match filename), `test_prompts` (array of strings, minItems=1), `criteria` (array of objects)
  - Each criterion: `name` (string), `weight` (float), `description` (string, non-empty)
  - Constraint: weights sum to 1.0 (tolerance ±0.01)
  - `validate_rubrics.py` uses custom Python checks (no `jsonschema` dep), exits non-zero on failure

- Config file should be comprehensive from the start. **Per-eval-type regression thresholds** (split keys):
  - Models: `generation_model`, `judge_model` (defaults: haiku, haiku)
  - Temperature: 0.0 (for both generation and judging)
  - Retry: `max_retries` (3), `backoff_base` (2.0), `backoff_jitter` (0.5)
  - Cost: `max_cost_per_run` (15.0)
  - RNG: `default_seed` (42)
  - Paths: results_dir, baselines_dir, rubrics_dir, datasets_dir, reports_dir
  - Regression thresholds (per eval type):
    - `effectiveness.mean_drop_threshold` (0.5), `effectiveness.stddev_multiplier` (2), `effectiveness.min_cases_before_compare` (3)
    - `activation.tpr_drop_threshold` (0.10), `activation.fpr_increase_threshold` (0.05), `activation.min_cases_before_compare` (5)
    - `size_impact.score_change_threshold` (0.5), `size_impact.min_cases_before_compare` (3)
    - `confusion.cross_activation_change_threshold` (0.10), `confusion.min_cases_before_compare` (5)

- **Results JSON contract** — All runners must produce results following a common envelope defined in `_common.py`:
  ```
  {
    "meta": { "run_id", "timestamp", "model", "judge_model", "seed", "total_cost", "eval_type" },
    "summary": { "entity_id": { "mean", "stddev", "n", ...per-eval-type scalar metrics } },
    "cases": [ { "id", "prompt", "entity_id", ...per-eval-type details } ],
    "artifacts": { ...optional eval-specific structured data }
  }
  ```
  Where `entity_id` is `skill_name` for L3/L5/L6 and `group_name` for L4.
  - `summary` contains only scalar metrics used for regression detection (what `compare_baseline.py` consumes)
  - `artifacts` is for eval-specific structured data that doesn't fit scalar metrics. L4 uses this for NxN confusion matrices:
    ```
    "artifacts": { "confusion_matrices": { "<group>": { "skills": [...], "matrix": [[...]], "no_activation": N, "multi_activation": N }}}
    ```
  - L3/L5/L6 may leave `artifacts` empty

- **Directory scaffolding**:
  - Committed directories with `.gitkeep`: `datasets/activation/`, `datasets/confusion/`, `datasets/size_impact/`, `rubrics/`, `baselines/`
  - Runtime-only directories (NOT committed): `results/`, `reports/`, `results/generations/`
  - Add `tests/evals/.gitignore` with: `results/`, `reports/`

- `requirements.txt` includes: `anthropic`, `pyyaml` (minimal deps — no `jsonschema`)

## Key context

- The shared module pattern prevents duplication: tasks .3, .5, .6, .7 all need config loading, retry, cost tracking, JSON extraction. Centralizing in .1 means later tasks consume only.
- Config should be "finished" in task .1 so later tasks mostly read from it, reducing merge-conflict risk.
- The `extract_json()` function must handle: JSON wrapped in prose, trailing commas (strip before parse), markdown code fences around JSON.
- Per-eval-type config keys prevent mismatch between activation (min 5 cases) and effectiveness (min 3 cases) thresholds.
- Dataset directories are split by eval type (activation/, confusion/, size_impact/) to keep ownership clear.

## Acceptance
- [ ] `tests/evals/` directory exists with all listed files; committed dirs have `.gitkeep`; `tests/evals/.gitignore` excludes `results/` and `reports/`
- [ ] `_common.py` exports: `load_config`, `get_client`, `retry_with_backoff`, `extract_json`, `load_skill_body`, `load_skill_description`, `build_run_metadata`, `track_cost`, `write_results`
- [ ] `extract_json()` handles: JSON in prose, markdown code fences, trailing commas; returns parsed dict or None
- [ ] `load_skill_body()` strips YAML frontmatter and wraps body in explicit delimiters
- [ ] `rubric_schema.yaml` documents required fields: `skill_name`, `test_prompts[]` (min 1), `criteria[]` (name, weight, description)
- [ ] `validate_rubrics.py` enforces rubric contract using custom Python checks (no jsonschema dep), exits non-zero on failure
- [ ] `validate_rubrics.py` checks: weights sum to 1.0 ±0.01, test_prompts non-empty, skill_name matches filename, no empty descriptions
- [ ] All skeleton runners accept `--dry-run`; L3/L5/L6 accept `--skill`, L4 accepts `--group`; all accept `--model`, `--judge-model`, `--runs`, `--seed`
- [ ] `config.yaml` includes per-eval-type regression thresholds with separate `min_cases_before_compare` per eval type
- [ ] `config.yaml` includes: models, temperature (0.0), retry, cost limits, RNG seed, paths
- [ ] `compare_baseline.py` exits 0 always (informational), reports regressions to stdout
- [ ] `requirements.txt` includes only `anthropic` and `pyyaml`
- [ ] `run_effectiveness.py --dry-run` lists skills with rubrics and exits 0 without API calls
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
