# Run Eval Suite Against Skills and Fix to Quality Bar

## Overview

Epic fn-58 built a comprehensive offline evaluation framework with 4 runners (activation, confusion, effectiveness, size impact), 12 rubrics, 73 activation cases, 36 confusion cases, and 11 size impact candidates. But it never actually **ran** the evals or **fixed** anything based on the results.

This epic closes the loop: run all 4 eval types against the current 131-skill catalog, analyze failures, fix skill descriptions and content until they hit a reasonable quality bar, and save initial baselines for future regression tracking.

**Supported platforms:** macOS and Linux. Windows is not supported by the eval framework (bash scripts, subprocess piping).

## Task Execution Order

**Task .7 (CLI migration) is the BLOCKER for all other tasks.** Despite being numbered .7, it MUST execute first. Dependencies are **machine-enforced** via Flow task JSON metadata (each task's `depends_on` array in `.flow/tasks/*.json`): .1 depends on .7, .2 depends on .1, .3/.4 depend on .2, .5 depends on .3+.4, .6 depends on .5. `flowctl ready` reads these dependencies and only surfaces .7 as the first actionable task. Each task spec also has a human-readable `Depends on:` line for redundancy.

Execution order: **.7** -> .1 -> .2 -> .3/.4 (sequential, .3 first) -> .5 -> .6

## Quality Bar ("Good Enough" Thresholds)

These thresholds account for the inherent difficulty of each eval type and the fact that we're routing across 131 skills with a small (haiku) model. Perfect scores are not expected.

### L3 Activation
- **TPR >= 75%** -- 3/4 positive cases route to the correct skill
- **FPR <= 20%** -- negative controls mostly rejected
- **Accuracy >= 70%** -- overall correctness across positive + negative

### L4 Confusion
- **Per-group accuracy >= 60%** -- overlapping skills are inherently hard
- **Cross-activation rate <= 35%** -- some confusion is expected within groups
- **No "never-activated" skills** -- every skill in a group gets predicted at least once (documented exception allowed if the model systematically cannot route to a niche skill within a small case set). Check via `artifacts.findings[]` where `type == "never_activated"`.
- **Negative control pass rate >= 70%**

### L5 Effectiveness
- **Overall win rate >= 50%** -- enhanced beats baseline at least half the time
- **Mean improvement > 0** -- net positive across all skills
- **No individual skill has 0% win rate** unless documented as a variance exception. With only 2 prompts x 3 runs = 6 cases per skill, 0% can occur by variance even for mildly helpful skills. Document exception with rationale if a skill's mean improvement is non-negative but wins are 0.

### L6 Size Impact
- **full > baseline** in >= 55% of `full_vs_baseline` comparisons (aggregate across all candidates, excluding errors)
- **No skill where baseline consistently beats full** -- defined as baseline sweep: `wins_baseline == n` for that candidate's `full_vs_baseline` comparisons (with `--runs 3`, this means baseline wins all 3 runs). This indicates the skill's full content is actively harmful.

These thresholds are deliberately achievable. If initial results are dramatically below them, it signals description/content problems to fix, not unrealistic targets. If results exceed them, great -- the bar may be raised later.

## Scope

**In scope:**
- Running all 4 eval types (activation, confusion, effectiveness, size impact)
- Analyzing results to identify worst-performing skills, descriptions, and confusion pairs
- Fixing skill frontmatter descriptions to improve activation routing
- Fixing overlapping skill descriptions to reduce cross-activation
- Improving skill content for skills with poor effectiveness scores
- Re-running evals to validate fixes
- Saving initial baseline JSON files for regression tracking
- Blocking fn-58.4 (CI workflow) on this epic's completion

**Out of scope:**
- Adding new rubrics beyond the existing 12
- Adding new activation/confusion test cases
- Setting up CI (that's fn-58.4, which this blocks)

## Approach

### Prerequisites (task .7 -- EXECUTE FIRST)

**CLI-based API layer**: The eval runners currently use the Anthropic Python SDK (`anthropic.Anthropic().messages.create(...)`) for all LLM calls. This requires `ANTHROPIC_API_KEY` to be set. **This is wrong.** The coding CLI clients (`claude`, `codex`, `copilot`) are already authenticated locally and must be used instead.

Task .7 replaces the entire SDK-based API layer with CLI subprocess invocations:

- **`_common.py`**: Replace `get_client()` and all `client.messages.create()` patterns with a `call_model()` function that shells out to the configured CLI tool
- **CLI tools** (all locally installed and already authenticated):
  - `claude -p "prompt" --system-prompt "..." --model haiku --output-format json --tools ""`
  - `codex --approval-mode full-auto "prompt" -m model`
  - `copilot -p "prompt"`
- **Config**: `config.yaml` gets a `cli` section specifying which tool to use (default: `claude`). Model names are CLI-native strings (e.g. `haiku` for claude, `o4-mini` for codex), not SDK model IDs.
- **No SDK dependency**: Remove `anthropic` from `requirements.txt` for the API call path. Keep `pyyaml` for config parsing.

The `claude` CLI is the primary backend because it supports `--system-prompt`, `--model`, and `--output-format json`. For `codex` and `copilot`, system prompts are prepended to the user message.

**CLI capability detection**: `call_model()` performs one-time capability detection on first invocation to verify the configured CLI tool supports the expected flags (e.g., `--output-format json`, stdin piping). If detection fails, it emits a one-time actionable diagnostic (e.g., "your claude CLI doesn't support --output-format json; upgrade or switch backend") and falls back gracefully: text-only mode with cost/usage fields set to 0.

**CLI override flag**: All 4 runners accept `--cli {claude,codex,copilot}` to override the config default at runtime.

**Skill loading**: Eval runners already load skills from `REPO_ROOT/skills/` (the local checkout). No plugin installation needed -- skills are read directly from the repo, not from any installed plugin location.

**Skill restore**: Tasks .3/.4 modify SKILL.md files. Restore mechanism is git-based:
- Commit clean state before starting fixes
- Each fix batch gets its own commit
- `git checkout -- skills/` restores any file to its committed state
- `git revert <commit>` undoes an entire fix batch if it makes things worse

### Iteration Strategy

This is an iterative improve-measure loop:

1. **Run** all 4 eval types against current skills
2. **Analyze** -- identify worst performers, common failure patterns
3. **Fix routing** (task .3) -- description edits for activation/confusion
4. **Fix content** (task .4) -- body edits for effectiveness, executed AFTER .3 to isolate attribution
5. **Re-run** -- verify improvement, check for regressions
6. **Save baselines** once thresholds are met

**Important**: Tasks .3 and .4 both edit `skills/*/SKILL.md` but target different sections (frontmatter descriptions vs body content). They should be executed sequentially -- .3 first (routing fixes), then .4 (content fixes) -- even though the dependency graph allows parallelism. This isolates attribution ("did the improvement come from description or content?") and avoids merge conflicts on the same files.

Expect 1-3 fix-rerun iterations. Focus on high-leverage fixes first (description clarity for activation/confusion, content quality for effectiveness).

### Cost Expectations

CLI invocations use the CLI's own billing/credits. Token-level cost tracking depends on CLI output format:
- `claude --output-format json` includes usage metadata -- cost can be extracted
- `codex`/`copilot` report usage in their own formats -- extraction is best-effort

Per eval runner invocation (approximate):
- Activation: ~73 CLI calls
- Confusion: ~54 CLI calls
- Effectiveness with `--runs 3`: ~216 CLI calls (12 skills x 2 prompts x 3 runs x 3 calls/case)
- Size impact with `--runs 3`: ~297 CLI calls (11 candidates x ~3 comparison types x 3 runs x 3 calls/case)

**Safety caps**: Runners enforce a dual abort mechanism -- **(cost OR call-count) caps**, whichever triggers first:
- `config.yaml:cost.max_cost_per_run` -- dollar-based cap (effective when CLI reports cost)
- `config.yaml:cost.max_calls_per_run` -- call-count cap (always effective, provides safety when cost data is unavailable)

`call_model()` returns `calls=1` per invocation and runners increment a shared counter for uniform abort logic regardless of backend.

### Runner Output Contract

All runners emit stable machine-parseable summary keys on stdout for `run_suite.sh` to consume:
- `TOTAL_CALLS=<int>` -- number of CLI calls made
- `COST_USD=<float>` -- total cost (0.0 if unavailable)
- `ABORTED=0|1` -- whether the run was cut short by a cap
- `N_CASES=<int>` -- number of eval cases executed

`run_suite.sh` parses these keys instead of regexing prose lines. This ensures consistent behavior across CLI backends.

### Schema Invariants

**Result envelope `summary` shape is unchanged across the CLI migration.** The `summary` object schema for all 4 eval types must remain stable so that `compare_baseline.py` continues to work without modification. Task .7 acceptance explicitly requires this.

### Fix Priority

1. **Activation failures** -- fix descriptions so the model can find skills
2. **Confusion cross-activations** -- differentiate overlapping skills
3. **Effectiveness losses** -- improve content for skills that underperform baseline
4. **Size impact anomalies** -- investigate skills where baseline beats full

### CI Auth Note

Local eval runs use authenticated CLI tools (no API keys needed). CI-based eval runs (fn-58.4) will need a separate auth story -- likely CLI auth via GitHub Actions secrets. This is explicitly fn-58.4's scope, not this epic's. We are removing SDK coupling here; CI auth is handled downstream.

## Quick Commands

```bash
# Run each eval type (CLI clients must be authenticated -- no API key needed)
python3 tests/evals/run_activation.py
python3 tests/evals/run_confusion_matrix.py
python3 tests/evals/run_effectiveness.py --runs 3
python3 tests/evals/run_size_impact.py --runs 3

# Run a single skill/group
python3 tests/evals/run_activation.py --skill dotnet-xunit
python3 tests/evals/run_confusion_matrix.py --group testing
python3 tests/evals/run_effectiveness.py --skill dotnet-xunit --runs 3

# Dry-run (no CLI calls)
python3 tests/evals/run_activation.py --dry-run

# Override CLI tool
python3 tests/evals/run_activation.py --cli codex
```

## Acceptance

- [ ] All 4 eval types have been run at least once with real CLI calls (not dry-run)
- [ ] Results analyzed and findings documented per task
- [ ] Skill descriptions fixed where activation/confusion results indicated problems
- [ ] Skill content improved where effectiveness results showed regression vs baseline
- [ ] Re-run results meet the quality bar thresholds above (or documented rationale for exceptions)
- [ ] Initial baseline JSON files saved to `tests/evals/baselines/`
- [ ] `./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh` still pass
- [ ] fn-58.4 unblocked (has dependency on this epic's final task)
- [ ] Result envelope `summary` schema unchanged across CLI migration (compare_baseline.py compatibility)

## Risks

| Risk | Mitigation |
|------|------------|
| CLI tool not in PATH | Task .7 validates availability at startup with actionable diagnostics |
| CLI flags differ by version | Capability detection in `call_model()` with fallback to text-only mode |
| CLI subprocess overhead | Each call spawns a process -- slower than SDK but acceptable for eval workload |
| Cost tracking unavailable | Dual cap: dollar-based + call-count-based; abort on whichever triggers first |
| Skill modifications need restore | Git-based: commit before fixes, `git checkout -- skills/` to restore |
| Fixing one skill breaks another | Re-run full suite after each fix batch; baselines track regressions |
| Quality bar too high for haiku | Thresholds designed for haiku; can lower if systematically unachievable with documented rationale |
| Description changes break copilot smoke tests | Run `validate-skills.sh` after each change batch |
| .3/.4 file conflicts | Execute sequentially (.3 first, then .4) even though deps allow parallelism |
| Summary schema drift breaks baselines | Schema invariant enforced in task .7 acceptance; compare_baseline.py tested after migration |
| L5 0% win rate by variance | Exception mechanism: 0% allowed with documented rationale if sample size insufficient |
| CI auth differs from local | fn-58.4 handles CI auth separately; this epic removes SDK coupling only |
