# fn-58-offline-skill-evaluation-framework-from.3 Build A/B effectiveness eval runner with LLM judge

## Description

Implement the A/B effectiveness eval runner (L5) that compares code generated with skill content injected vs code generated without it, using an LLM judge to score both outputs against the rubric criteria. Uses shared infrastructure from `_common.py` (task .1).

**Size:** M
**Files:**
- `tests/evals/run_effectiveness.py` (flesh out the skeleton from task .1)
- `tests/evals/judge_prompt.py` (LLM judge prompt templates and response parsing)

## Approach

- For each skill with a rubric:
  1. Read the skill SKILL.md content via `_common.load_skill_body()` (frontmatter stripped, explicit delimiters)
  2. For each test prompt in the rubric:
     a. **Enhanced run**: System prompt includes the skill body (delimited), user prompt is the test prompt -> generate code
     b. **Baseline run**: System prompt is generic ("You are a .NET developer"), same user prompt -> generate code
  3. **Store generations**: Write enhanced and baseline outputs to `results/generations/` (separate from judge scores) for resume/replay
  4. **Judge step**: Randomize A/B ordering using seeded RNG (seed from config, recorded per case), present both outputs + rubric criteria to judge model, collect per-criterion scores
  5. **Score**: Compute per-criterion winner, overall winner, mean improvement

- **Judge prompt contract** (in `judge_prompt.py`):
  - Present both outputs with randomized labels (Response A / Response B)
  - Include the rubric criteria with descriptions
  - Instruct: "Output ONLY a JSON object with this exact structure"
  - Expected JSON: `{"criteria": [{"name": "...", "score_a": N, "score_b": N, "reasoning": "..."}], "overall_winner": "A|B|tie"}`
  - Use `_common.extract_json()` to parse response
  - On parse failure: retry up to 2x with progressively stricter prompt
  - On final failure: record `judge_error`, store raw judge text in results

- **Resume/replay support**: If `results/generations/<skill>/<prompt_hash>.json` exists and `--regenerate` flag is NOT set, skip generation and go straight to judging.

- Edge cases: empty/refusal -> `generation_error`; all retries exhausted -> `judge_error`; rate limits -> `_common.retry_with_backoff()`

- Use `_common.track_cost()` for every API call; abort if `max_cost_per_run` exceeded

## Key context

- Use `temperature=0.0` for both generation and judging (reproducibility).
- Position bias well-documented. Seeded RNG makes A/B assignment reproducible.
- Cost: ~$0.02-0.05 per case. 15 rubrics x 2 prompts x 3 trials = $2-5 per suite.

## Acceptance
- [ ] `run_effectiveness.py` generates code for both enhanced (with skill body, frontmatter stripped) and baseline conditions
- [ ] Skill content injected with explicit delimiters
- [ ] A/B ordering randomized per case using seeded RNG; seed and assignment recorded in results
- [ ] LLM judge produces per-criterion scores (1-5) via structured JSON
- [ ] Judge response parsed via `_common.extract_json()`; up to 2 retries with stricter prompt on failure
- [ ] Raw judge text stored on all parse failures for debugging
- [ ] Generations stored separately in `results/generations/` for resume/replay
- [ ] `--regenerate` flag forces re-generation even if cached outputs exist
- [ ] Results JSON includes: skill_name, prompt, scores, winner, per_criterion_breakdown, model, judge_model, run_id, seed, timestamp, cost, A/B_assignment
- [ ] `--dry-run`, `--skill <name>`, `--runs N` supported
- [ ] Summary statistics include `mean`, `stddev`, `n` per skill
- [ ] Run aborts if `max_cost_per_run` exceeded
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
