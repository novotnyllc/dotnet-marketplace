# fn-53-skill-routing-language-hardening.2 Canonical Routing Language Spec

## Description
Define canonical rules for skill routing language as a style guide document. Cover: classifier-style descriptions (≤120 chars, front-loaded action verb, what+when+triggers), explicit scope/out-of-scope section format, normalized cross-reference language (`See [skill:x] for Y` where Y is specific), router precedence language (baseline-first loading of `dotnet-csharp-coding-standards`), and agent file reference conventions.

**Size:** M
**Files:**
- `docs/skill-routing-style-guide.md` (new)
- `CONTRIBUTING-SKILLS.md` (update — **all sections** containing description examples: Quick Start (Section 1), Writing Effective Descriptions (Section 3), and any other sections with `WHEN`-prefix or budget example output)

## Approach

- Codify the present-participle description style already dominant across 130 skills (e.g., "Building...", "Designing...", "Using...")
- Define mandatory sections: every skill must have `## Scope` and `## Out of scope` with `[skill:]` attribution
- Define cross-reference format: `See [skill:x] for Y.` where Y is a specific topic (not "more details")
- Define unified reference syntax: `[skill:name]` refers to any routable artifact (skills OR agents). The validator resolves against the union of skill directory names + agent file stems. Explicitly state this in the style guide with examples for both skills and agents.
- Include positive/negative examples table (follow pattern at `CONTRIBUTING-SKILLS.md:126-131`)
- Include migration checklist for converting existing descriptions
- Address CI strict mode: recommend setting `STRICT_REFS=1` in `validate.yml` (broken refs = errors). Local development keeps lenient default.

## Self-references and cycles

- Self-references (skill referencing itself) are always an error.
- Bidirectional references (e.g., `dotnet-advisor` ↔ `dotnet-version-detection`) are legitimate for hub skills. Cycle detection produces an informational report, not validation errors.
- Style guide must explicitly state these rules with examples.

## WHEN-prefix resolution

Agent `description` fields follow the same no-WHEN-prefix rule as skills. Agent descriptions use third-person declarative style: "Analyzes X for Y" not "WHEN analyzing X". This aligns agents and skills under one convention. The style guide must state this explicitly with before/after examples.

**CONTRIBUTING-SKILLS.md full update**: The current contributor guide uses `description: "WHEN ..."` examples in **both the Quick Start (Section 1) and Writing Effective Descriptions (Section 3)**, plus possibly other sections. T2 must replace ALL WHEN-prefix examples throughout the entire file with canonical non-WHEN third-person declarative style. This resolves the existing policy drift between contributor guide and validator (which already warns on WHEN-prefix).

## Budget example output update

Current `CONTRIBUTING-SKILLS.md` shows a sample validator output with `PROJECTED_DESC_CHARS=12000`, which is inconsistent (130 * 120 = 15,600). The budget narrative also implies contributors should reason about projected numbers. T2 must update:
- Sample output to show a realistic `PROJECTED_DESC_CHARS` value (e.g., 15,600)
- Surrounding text to clarify: `BUDGET_STATUS` is derived from `CURRENT_DESC_CHARS` only, and `PROJECTED_DESC_CHARS` is informational (not part of status determination)

## CONTRIBUTING-SKILLS.md scope boundary

T2 writes the canonical style rules across all sections of CONTRIBUTING-SKILLS.md. T12 will add enforcement-specific guidance (validator flags, baseline policy, CI gate configuration) after verification is complete. T2 does NOT cover CI/validator usage patterns — only the style rules and examples themselves.

## Budget threshold semantics

Style guide must clarify: acceptance criterion is `CURRENT_DESC_CHARS < 12,000` (strictly less than). The validator WARN triggers at `>= 12,000`, so exactly 12,000 still yields WARN. PROJECTED_DESC_CHARS is a separate informational metric, not part of BUDGET_STATUS.

## Key context

- Anthropic best practices: "description must describe what the skill does AND when to use it" -- third person, no filler
- Research: assertive cues create 7x bias, position bias 80.2% for first tool. Descriptions must be factual.
- Budget constraint: 120 chars max per description, 12K warn threshold aggregate. Style guide must emphasize budget-neutral changes.
- 5 agent descriptions currently use `WHEN` prefix. Style guide resolves: no WHEN prefix for agents or skills.
- Current CONTRIBUTING-SKILLS.md has WHEN-prefix examples in multiple sections and inconsistent budget sample output. T2 resolves both.

## Acceptance
- [ ] `docs/skill-routing-style-guide.md` exists with: description formula, scope/out-of-scope format, cross-reference format (unified `[skill:]` for skills and agents), precedence language, positive/negative examples table, migration checklist
- [ ] Style guide explicitly documents unified `[skill:]` syntax covering both skills and agents, with examples
- [ ] Style guide explicitly documents self-reference (error) vs cycle (informational report) policy
- [ ] Style guide clarifies budget threshold: `CURRENT_DESC_CHARS < 12,000` and PROJECTED as informational only
- [ ] `CONTRIBUTING-SKILLS.md` ALL WHEN-prefix examples replaced with canonical non-WHEN style across ALL sections (Quick Start, Writing Effective Descriptions, any others)
- [ ] `CONTRIBUTING-SKILLS.md` budget sample output updated: realistic PROJECTED value, text clarifies BUDGET_STATUS is current-only
- [ ] `CONTRIBUTING-SKILLS.md` references style guide and incorporates canonical rules (style rules only; enforcement guidance deferred to T12)
- [ ] Style guide explicitly resolves WHEN-prefix: no-WHEN-prefix for both skills and agents, with third-person declarative style and before/after examples
- [ ] Style guide addresses CI strict mode recommendation (`STRICT_REFS=1`)
- [ ] `./scripts/validate-skills.sh` still passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
