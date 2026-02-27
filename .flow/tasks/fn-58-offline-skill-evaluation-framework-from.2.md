# fn-58-offline-skill-evaluation-framework-from.2 Author priority rubric YAML files for 10-15 skills

## Description
Author rubric YAML files for 10-15 priority skills, following the schema defined in task .1. Rubrics define per-criterion scoring guidelines that the LLM judge uses to compare skill-loaded vs baseline code output.

**Size:** M
**Files:**
- `tests/evals/rubrics/dotnet-xunit.yaml`
- `tests/evals/rubrics/dotnet-minimal-apis.yaml`
- `tests/evals/rubrics/dotnet-efcore-patterns.yaml`
- `tests/evals/rubrics/dotnet-csharp-coding-standards.yaml`
- `tests/evals/rubrics/dotnet-csharp-async-patterns.yaml`
- `tests/evals/rubrics/dotnet-resilience.yaml`
- `tests/evals/rubrics/dotnet-containers.yaml`
- `tests/evals/rubrics/dotnet-blazor-patterns.yaml`
- `tests/evals/rubrics/dotnet-testing-strategy.yaml`
- `tests/evals/rubrics/dotnet-observability.yaml`
- `tests/evals/rubrics/dotnet-security-owasp.yaml`
- `tests/evals/rubrics/dotnet-native-aot.yaml`
- Additional rubrics as time allows (target 15)

Each rubric also includes 1-2 test prompts (realistic developer questions) that serve as the eval input.

## Approach

- Follow the rubric format from `dotnet-skills-evals/datasets/rubrics/*.yaml` — each rubric has 3-6 weighted criteria
- Read the corresponding `skills/<skill-name>/SKILL.md` to understand what the skill teaches, then write criteria that test whether an LLM *using* the skill produces output aligned with the skill's guidance
- Criteria weights should sum to 1.0 and reflect the relative importance of each aspect
- Test prompts should be realistic developer questions, not quiz-style ("how to X with Y in .NET")
- Prioritization rationale:
  - **User-invocable + code-producing skills** — these have clear A/B testability
  - **High overlap risk** — xunit, testing-strategy, efcore-patterns overlap and rubrics disambiguate value
  - **Broad usage** — coding-standards, async-patterns are loaded frequently via advisor routing
  - **Specialized knowledge** — resilience, native-aot, observability add knowledge the model may not have natively

## Key context

- The reference implementation found that **specialized/niche skills benefit most** from rubrics (+2.33 improvement) while **general-knowledge skills show weaker improvement** (+0.33). Expect rubrics for skills like `dotnet-native-aot` and `dotnet-resilience` to show the strongest A/B signal.
- Non-code skills (dotnet-advisor, dotnet-ui-chooser, dotnet-agent-gotchas) are excluded — they produce routing/guidance, not code, and require a different eval methodology.
- Each rubric should include a `test_prompts` field (array of strings) so the effectiveness runner can self-serve test inputs without a separate dataset file.
## Acceptance
- [ ] At least 10 rubric YAML files exist under `tests/evals/rubrics/`
- [ ] All rubrics pass `python tests/evals/validate_rubrics.py` (schema validation from task .1)
- [ ] Each rubric has 3-6 criteria with weights summing to 1.0 (tolerance ±0.01)
- [ ] Each rubric has at least 1 test prompt in the `test_prompts` field
- [ ] Criteria descriptions reference specific patterns/APIs the skill teaches (not generic "good code" statements)
- [ ] No rubric references a skill that does not exist in `skills/` directory
- [ ] Rubric file names match the skill directory names exactly
## Done summary
Authored 12 priority rubric YAML files for skill effectiveness evaluation under tests/evals/rubrics/. Each rubric has 5 weighted criteria (sum=1.0) referencing specific APIs and patterns from the corresponding SKILL.md, plus 2 realistic developer test prompts for A/B comparison. Skills covered: xunit, minimal-apis, efcore-patterns, csharp-coding-standards, csharp-async-patterns, resilience, containers, blazor-patterns, testing-strategy, observability, security-owasp, and native-aot.
## Evidence
- Commits: 8f98b5ec7c7c4ce50903cbbb26f1319d9e35cbdf
- Tests: python3 tests/evals/validate_rubrics.py, ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh
- PRs: