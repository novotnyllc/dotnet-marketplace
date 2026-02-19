# fn-53-skill-routing-language-hardening.2 Canonical Routing Language Spec

## Description
Define canonical rules for skill routing language as a style guide document. Cover: classifier-style descriptions (≤120 chars, front-loaded action verb, what+when+triggers), explicit scope/out-of-scope section format, normalized cross-reference language (`See [skill:x] for Y` where Y is specific), router precedence language (baseline-first loading of `dotnet-csharp-coding-standards`), and agent file reference conventions.

**Size:** M
**Files:**
- `docs/skill-routing-style-guide.md` (new)
- `CONTRIBUTING-SKILLS.md` (update Section 3 "Writing Effective Descriptions")

## Approach

- Codify the present-participle description style already dominant across 130 skills (e.g., "Building...", "Designing...", "Using...")
- Define mandatory sections: every skill must have `## Scope` and `## Out of scope` with `[skill:]` attribution
- Define cross-reference format: `See [skill:x] for Y.` where Y is a specific topic (not "more details")
- Define agent reference format: agents referenced as `[skill:agent-name]` (same syntax as skills since agents are also loaded via the skill system)
- Include positive/negative examples table (follow pattern at `CONTRIBUTING-SKILLS.md:126-131`)
- Include migration checklist for converting existing descriptions
- Address `--allow-planned-refs`: recommend flipping default to strict in CI (broken refs = errors)

## Key context

- Anthropic best practices: "description must describe what the skill does AND when to use it" -- third person, no filler
- Research: assertive cues create 7x bias, position bias 80.2% for first tool. Descriptions must be factual.
- Budget constraint: 120 chars max per description, 12K warn threshold aggregate. Style guide must emphasize budget-neutral changes.
- Agent descriptions use `WHEN` prefix (5 agents). Skills reject it. Style guide must resolve this inconsistency.
## Acceptance
- [ ] `docs/skill-routing-style-guide.md` exists with: description formula, scope/out-of-scope format, cross-reference format, precedence language, positive/negative examples table, migration checklist
- [ ] `CONTRIBUTING-SKILLS.md` Section 3 updated to reference style guide and incorporate canonical rules
- [ ] Style guide addresses agent vs skill description conventions (resolve WHEN-prefix inconsistency)
- [ ] Style guide addresses `--allow-planned-refs` policy recommendation
- [ ] `./scripts/validate-skills.sh` still passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
