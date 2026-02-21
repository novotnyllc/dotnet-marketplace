# fn-57-copilot-testing-and-progressive.1 Copilot activation smoke tests

## Description

Create Copilot-specific activation smoke tests that prove skills are discovered, loaded, and correctly used by Copilot CLI. Model test patterns after the dotnet-skills-evals activation eval framework. Include tests for progressive disclosure (sibling file access).

**Size:** M
**Files:** tests/copilot-smoke/ (new directory), tests/copilot-smoke/cases.jsonl (test cases), tests/copilot-smoke/run_smoke.py (runner), tests/copilot-smoke/baseline.json (expected outcomes), tests/copilot-smoke/fixture-plugin/ (test-only fixture with sentinel sibling file)

## Approach

1. **Study dotnet-skills-evals activation eval** at `src/dotnet_skills_evals/eval_activation/`. The framework tests three discovery mechanisms: `tool` (function calling), `compressed` (terse index), `fat` (full descriptions). Our smoke tests should mirror the `tool` mechanism since that matches how Copilot discovers skills.

2. **Create test case dataset** in JSONL format matching dotnet-skills-evals schema:
   ```
   {"id": "smoke-001", "user_prompt": "...", "expected_skills": ["skill-name"], "should_activate": true, "category": "..."}
   ```
   Cover:
   - **Top visible skills**: Direct activation via prompt matching description
   - **Advisor-routed skills**: Prompts that should trigger `dotnet-advisor` which then routes to skills outside the visible set
   - **Negative controls**: Prompts that should NOT trigger any .NET skills
   - **Progressive disclosure**: Verify Copilot can access sibling files (e.g., `reference.md`, `examples.md`) after activating a skill that references them
   - Minimum 25 test cases (10 direct, 5 advisor-routed, 5 negative, 5 progressive disclosure)

3. **Build smoke runner** that:
   - Invokes Copilot CLI with each test prompt
   - Parses output for evidence of skill loading (regex: `Base directory for this skill:\s*(?<path>.+)`)
   - Compares activated skills against expected_skills
   - Produces a `results.json` with per-case pass/fail outcomes

4. **Create a baseline file** (`baseline.json`) capturing the expected outcome for each test case deterministically:
   ```json
   {"smoke-001": {"expected": "pass", "skills": ["dotnet-csharp-async-patterns"]}, ...}
   ```
   Gate on "no unexpected regressions vs baseline" rather than percentage thresholds. When a test case is known-flaky or model-sensitive, mark it as `"flaky": true` in the baseline so CI doesn't fail on it, but still tracks the result.

5. **Integrate with existing test harness**. The `copilot-refactor` branch already has `run-agent-routing-smoke.py` and `compare-agent-routing-baseline.py` — extend rather than replace.

6. **Test advisor meta-routing specifically**: Verify that when the advisor is activated, skills referenced in its compressed catalog can be subsequently loaded on demand.

7. **Test sibling file access** with deterministic evidence using a test-only fixture:
   - Create a test fixture plugin under `tests/copilot-smoke/fixture-plugin/` with a minimal skill that has a sibling reference file containing a unique sentinel string (e.g., `SENTINEL-COPILOT-SIBLING-TEST-7f3a`). The sentinel must NOT appear in the core SKILL.md or any other loaded content.
   - The smoke runner installs this fixture plugin in Copilot before running the sentinel test case (same pattern as `test.sh:prepare_copilot_plugin()`).
   - Create a test prompt that asks for the sentinel string's context. Assert the response contains the sentinel.
   - This keeps production skills untouched and avoids ordering dependencies with fn-57.3.

## Key context

- dotnet-skills-evals `loader.py` scans one level deep only — matches our flat layout
- Existing `tests/agent-routing/cases.json` has routing test cases — Copilot smoke tests are complementary but distinct
- Copilot CLI evidence pattern: `Base directory for this skill:\s*(?<path>.+)` (from `docs/agent-routing-tests.md:L111`)
- Copilot issue #978: "Skills not auto-activated" — descriptions must use strong activation language

## Acceptance
- [ ] Test case dataset exists with >= 25 cases (10 direct, 5 advisor-routed, 5 negative, 5 progressive disclosure)
- [ ] Smoke runner can invoke Copilot CLI and parse skill activation evidence
- [ ] Baseline file captures expected per-case outcomes deterministically
- [ ] Regression comparison gates on "no unexpected regressions vs baseline" (not percentage thresholds)
- [ ] Known-flaky cases marked in baseline; CI does not fail on them but tracks results
- [ ] Negative controls: false activations tracked in baseline (informational, not a gate — occasional false positives are expected)
- [ ] Progressive disclosure: sibling file access verified via sentinel string (unique token in sibling file, asserted in response)
- [ ] Results output in a format compatible with `compare-agent-routing-baseline.py`
- [ ] Runner supports two modes: (1) default — skip with `infra_error` status and warning if Copilot not installed (exit 0); (2) `--require-copilot` — output `infra_error` and exit non-zero if Copilot unavailable (used by CI to enforce the gate on non-fork PRs)
