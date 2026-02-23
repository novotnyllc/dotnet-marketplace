# fn-58-offline-skill-evaluation-framework-from.5 Offline activation eval dataset and runner

## Description

Build an offline activation eval (L3 runner) that tests whether models correctly select skills given developer prompts — without requiring any CLI invocation. Uses shared infrastructure from `_common.py` (task .1).

**Size:** M
**Files:**
- `tests/evals/run_activation.py` (flesh out skeleton from task .1)
- `tests/evals/datasets/activation/core_skills.jsonl` (test cases for core/high-traffic skills)
- `tests/evals/datasets/activation/specialized_skills.jsonl` (test cases for specialized domain skills)
- `tests/evals/datasets/activation/negative_controls.jsonl` (prompts that should NOT activate any target skill)

## Approach

- **Compressed routing index format** (built dynamically from `skills/*/SKILL.md` frontmatter):
  - Fields: `id` + `description` only
  - Sorted by `id` (stable ordering for reproducible baselines)
  - Descriptions truncated to 120 chars (matching style guide limit)
  - Token count of emitted index tracked in results for budget monitoring
  - Format: one skill per line: `- skill-id: description text`

- **Structured activation detection** (avoids substring brittleness):
  - System prompt instructs model: "Given the following skill index and user prompt, return JSON: `{"skills": [...], "reasoning": "..."}`"
  - Primary detection: parse structured JSON via `_common.extract_json()`
  - Fallback (parse failure only): ask Haiku "Did this response indicate skill X should be used?" — rare path
  - Track detection method per case in results

- JSONL format: `{"id": "act-001", "user_prompt": "...", "expected_skills": ["skill-name"], "acceptable_skills": [], "should_activate": true, "category": "domain"}`

- Metrics: TPR, FPR, accuracy, per-skill activation rate, token usage, index token count, cost

- Target: 50+ positive cases across 20+ skills, 15+ negative controls

- Reuse prompts from existing `tests/copilot-smoke/cases.jsonl` and `tests/agent-routing/cases.json` where applicable

## Key context

- Tool-based discovery shows 100% activation + 100% FPR (measures tool-calling bias). Structured JSON avoids this.
- Short/generic skill names like `serialization` cause false positives. Structured response with explicit IDs eliminates this.
- Reference repo best: Sonnet + compressed index = 56.5% TPR, 0% FPR, 84.6% accuracy with 31 skills.
- Stable index ordering ensures baselines are comparable across runs.

## Acceptance
- [ ] `run_activation.py` runs offline activation eval using Anthropic API (no CLI required)
- [ ] Compressed routing index built dynamically: id + description, sorted by id, truncated to 120 chars
- [ ] Index `char_count` tracked in results; overall `usage.input_tokens` from API response recorded (no separate tokenizer dep)
- [ ] Structured JSON response: `{"skills": [...], "reasoning": "..."}`
- [ ] Primary detection: `_common.extract_json()` parse; LLM fallback only on parse failures
- [ ] At least 50 positive activation test cases across 20+ skills
- [ ] At least 15 negative control cases
- [ ] Metrics reported: TPR, FPR, accuracy, per-skill activation rate, token usage, index tokens, cost
- [ ] Results include `mean`, `stddev`, `n` per metric (when --runs > 1)
- [ ] `--dry-run`, `--skill <name>` supported
- [ ] Per-case details in results JSON: prompt, expected, actual, detection_method, pass/fail
- [ ] Reuses at least 10 prompts from existing test infrastructure
## Done summary
Implemented offline activation eval runner (L3) with compressed routing index built dynamically from skill frontmatter, structured JSON detection with LLM fallback, 55 positive test cases across 55 skills and 18 negative controls in 3 JSONL datasets, and full metrics (TPR/FPR/accuracy/per-skill activation rate/token usage/cost) with multi-run stats support.
## Evidence
- Commits: a0f4d0fc71b013a627e2d431bf92a523bafe3ea4
- Tests: python3 tests/evals/run_activation.py --dry-run, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: