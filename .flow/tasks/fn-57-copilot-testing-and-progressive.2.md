# fn-57-copilot-testing-and-progressive.2 Cross-provider regression tests

## Description

Verify that Claude Code, Codex, and Copilot all correctly discover and use skills after the structural changes in fn-56. Catch regressions by comparing against pre-flatten baselines from the `main` branch.

**Size:** M
**Files:** tests/agent-routing/ (existing), test.sh, tests/agent-routing/provider-baseline.json, .github/workflows/agent-live-routing.yml

## Approach

1. **Use `main` branch as pre-flatten baseline**: The `agent-live-routing.yml` workflow already uses `baseline_ref` (default `main`) as the comparison point. No manual "capture before starting" step needed — `main` represents the pre-flatten state.

2. **Post-flatten verification for Claude Code**:
   - Run `./test.sh --agents claude` — verify all existing test cases pass
   - Key check: `plugin.json` paths resolve correctly from Claude Code's plugin loader
   - Key check: `[skill:name]` cross-references still resolve (validator already checks this)
   - Key check: hooks still find scripts via `${CLAUDE_PLUGIN_ROOT}` (path-independent, should be fine)

3. **Post-flatten verification for Codex**:
   - Run `./test.sh --agents codex` — verify skill sync works
   - Key check: `test.sh` find depth fix from fn-56.1 actually works (finds 131 skill dirs)
   - Key check: `.agents/openai.yaml` path pattern updated

4. **Post-flatten verification for Copilot**:
   - Run `./test.sh --agents copilot`
   - Key check: Copilot can discover skills from flat layout
   - Key check: Evidence pattern `Base directory for this skill:` appears in output

5. **Compare against `main` baseline**: Use the workflow's built-in baseline comparison mechanism to diff pre/post results. Flag any regressions.

6. **Update `provider-baseline.json`** with new expected pass/fail per provider per test case if behavior intentionally changes. Include justification comments for any changes.

## Key context

- `test.sh` already handles per-provider setup: `prepare_claude_plugin()`, `prepare_codex_plugin()`, `prepare_copilot_plugin()` (L89-108)
- `provider-baseline.json` defines expected pass/fail per provider per test case
- The `copilot-refactor` branch already has `run-agent-routing-smoke.py` and `compare-agent-routing-baseline.py`
- CI `agent-live-routing.yml` uses `baseline_ref` parameter pointing to `main` by default

## Acceptance
- [ ] `main` branch used as pre-flatten baseline (no manual capture step needed)
- [ ] Claude Code: all existing test cases pass on flat layout
- [ ] Codex: skill sync discovers 131 skills from flat layout
- [ ] Copilot: discovers skills from flat layout
- [ ] Baseline comparison shows no unintentional regressions vs `main`
- [ ] `provider-baseline.json` updated with any intentional behavior changes + justification comments
- [ ] All three providers can be tested via `./test.sh --agents claude,codex,copilot`
