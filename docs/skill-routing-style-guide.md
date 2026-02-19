# Skill Routing Style Guide

Canonical rules for writing skill and agent descriptions, scope sections, and cross-references in dotnet-artisan. All new and modified skills must follow these conventions. Downstream sweep tasks (T5--T10) apply these rules to existing skills.

---

## 1. Description Formula

Structure every description as: **Action + Domain + Differentiator**

Use **third-person declarative** style with a present-tense or present-participle verb. Front-load the most specific action verb. Do not start with "WHEN", "A skill that", "Helps with", or other filler.

### Formula

```
<Action verb/participle> <specific .NET domain> <differentiating detail>.
```

### Positive and Negative Examples

| Quality | Description | Chars | Verdict |
|---------|-------------|-------|---------|
| Good | `Routes .NET/C# work to specialist skills and loads coding-standards first for code paths.` | 89 | Specific action, clear trigger |
| Good | `Writing async/await code. Task patterns, ConfigureAwait, cancellation, and common agent pitfalls.` | 97 | Present-participle lead, scope clear |
| Good | `Detects and fixes common .NET dependency injection lifetime misuse and registration errors.` | 92 | Actionable, precise domain |
| Good | `Navigating .NET solution structure or build configuration. Analyzes .sln, .csproj, CPM.` | 87 | Two signal verbs, concrete artifacts |
| Bad | `WHEN writing C# async code. Patterns for async/await.` | 52 | WHEN prefix -- violates style rule |
| Bad | `C# patterns` | 12 | Too vague; matches everything |
| Bad | `Complete guide to everything about async programming in C# including all patterns, best practices, and common mistakes.` | 118 | Promotional filler, non-specific |
| Bad | `Helps with code quality stuff` | 30 | No activation signal, no domain |
| Bad | `A skill that provides guidance on testing strategies for .NET developers.` | 73 | "A skill that" filler, passive |

### WHEN-Prefix Rule

**Do not use WHEN prefix** in descriptions for skills or agents. The `WHEN` prefix was an early convention that creates assertive cues. Research shows assertive cues in tool descriptions create 7x selection bias. Descriptions must be factual and classifier-style, not imperative.

This rule applies equally to:
- **Skill descriptions** in SKILL.md frontmatter
- **Agent descriptions** in `agents/*.md` frontmatter

Agent descriptions use the same third-person declarative style as skills.

**Before/after examples (agents):**

| Before (WHEN prefix) | After (declarative) |
|----------------------|---------------------|
| `WHEN analyzing ASP.NET Core middleware, request pipelines...` | `Analyzes ASP.NET Core middleware, request pipelines...` |
| `WHEN debugging race conditions, deadlocks...` | `Debugs race conditions, deadlocks...` |
| `WHEN reviewing .NET code for security vulnerabilities...` | `Reviews .NET code for security vulnerabilities...` |
| `WHEN building .NET MAUI apps.` | `Builds .NET MAUI apps.` |
| `WHEN designing .NET benchmarks...` | `Designs .NET benchmarks...` |

**Before/after examples (skills):**

| Before (WHEN prefix) | After (declarative) |
|----------------------|---------------------|
| `WHEN writing C# async code. Patterns for async/await.` | `Writing async/await code. Task patterns, ConfigureAwait, cancellation.` |
| `WHEN writing, reviewing, or planning C# code. Catches code smells.` | `Detects code smells and anti-patterns in C# code during writing and review.` |

### The 120-Character Target

Each description must target **under 120 characters**. This is a budget constraint derived from the aggregate context window limit, not a style preference.

**Budget math:** The plugin loads all skill descriptions into the context window at session start. With 130 skills, the aggregate must stay below 12,000 characters (WARN threshold) and 15,600 characters (FAIL threshold = 130 * 120).

### Budget Threshold Semantics

- **Acceptance criterion:** `CURRENT_DESC_CHARS < 12,000` (strictly less than)
- **BUDGET_STATUS:** Should be derived from `CURRENT_DESC_CHARS` only, not projected chars. The canonical thresholds are:
  - `OK`: `CURRENT_DESC_CHARS < 12,000`
  - `WARN`: `CURRENT_DESC_CHARS >= 12,000`
  - `FAIL`: `CURRENT_DESC_CHARS >= 15,600`
- **PROJECTED_DESC_CHARS:** Informational metric only (130 * 120 = 15,600). Should not be part of BUDGET_STATUS determination.
- Reaching exactly 12,000 counts as WARN. Acceptance requires being strictly below.

> **Note:** The current validator (`_validate_skills.py`) also factors `PROJECTED_DESC_CHARS` into `BUDGET_STATUS`. T3 will update the validator to decouple projected from status, matching this canonical policy.

All description changes during sweeps must be **budget-neutral or budget-negative** (same or fewer total characters).

---

## 2. Scope and Out-of-Scope Sections

Every skill must include explicit scope boundaries using these markdown headings.

### Required Format

```markdown
## Scope

- Specific topic A covered by this skill
- Specific topic B covered by this skill

## Out of scope

- Topic X -- see [skill:dotnet-other-skill]
- Topic Y -- see [skill:dotnet-another-skill]
```

### Rules

1. **Scope** lists what the skill covers, using bullet points with concrete topics
2. **Out of scope** lists what the skill does NOT cover, with attribution to the owning skill using `[skill:]` syntax
3. Both sections use `##` level headings (not inline bold labels)
4. Out-of-scope items must include a cross-reference to the skill that owns the excluded topic
5. At minimum, list the most common confusion boundaries (skills a user might pick this one instead of)

---

## 3. Cross-Reference Format

### Unified `[skill:]` Syntax

`[skill:name]` refers to any routable artifact -- **both skills and agents**. The validator should resolve references against the union of skill directory names and agent file stems (without `.md`).

> **Note:** The current validator (`_validate_skills.py`) resolves `[skill:]` references against skill directory names only. T3 will extend validation to include agent file stems in the known-IDs set.

```markdown
# Referencing a skill
See [skill:dotnet-csharp-async-patterns] for async/await guidance.

# Referencing an agent
Route to [skill:dotnet-security-reviewer] for security audit.
```

### Rules

1. **Always use `[skill:name]`** -- bare text skill/agent names are not machine-parseable
2. The `name` must match an existing skill directory name or agent file stem
3. The topic after "for" must be **specific** (not "more details" or "related patterns")
4. Unresolved references produce validation warnings (errors in strict mode)

### Self-References and Cycles

- **Self-references** (a skill referencing itself via `[skill:]`) are **always an error**. T3 will add a validator check that rejects self-references.
- **Bidirectional references** (e.g., `[skill:dotnet-advisor]` in dotnet-version-detection and `[skill:dotnet-version-detection]` in dotnet-advisor) are **legitimate** and expected for hub skills. Cycle detection produces an **informational report**, not validation errors.

### Examples

| Quality | Reference | Problem |
|---------|-----------|---------|
| Good | `See [skill:dotnet-csharp-async-patterns] for async/await guidance.` | Specific topic |
| Good | `Route to [skill:dotnet-architect] for framework selection decisions.` | Agent reference, specific topic |
| Bad | `See [skill:dotnet-csharp-async-patterns] for more details.` | Vague topic -- "more details" |
| Bad | `See dotnet-csharp-async-patterns for async guidance.` | Bare text -- not machine-parseable |
| Bad | `See [skill:dotnet-my-skill] for patterns.` | Self-reference (if written in dotnet-my-skill) |

---

## 4. Router Precedence Language

### Baseline-First Loading

`dotnet-csharp-coding-standards` is the **baseline skill** -- it loads first for any C# code path. Other skills build on top of its conventions, never contradict them.

When writing skill content:
- Do not restate rules from dotnet-csharp-coding-standards
- Reference it explicitly: `See [skill:dotnet-csharp-coding-standards] for baseline C# conventions.`
- If your skill overrides a baseline convention for a specific domain, state the override explicitly with rationale

### Advisor Routing

`dotnet-advisor` is the **routing hub** -- it delegates to domain skills based on the user's request. Skills referenced from dotnet-advisor get higher routing priority.

---

## 5. Agent Description Conventions

Agent descriptions follow the **same no-WHEN-prefix rule** as skills. Use third-person declarative style.

### Format

```yaml
description: "Analyzes X for Y. Routes to Z for edge cases."
```

### Rules

1. No WHEN prefix
2. Third-person declarative ("Analyzes", "Debugs", "Reviews", not "WHEN analyzing")
3. Include trigger phrases after the description when useful: `Triggers on: keyword1, keyword2.`
4. Include WHEN NOT routing in the description body (not description field) if needed for disambiguation

---

## 6. CI Strict Mode

### STRICT_REFS Recommendation

Set `STRICT_REFS=1` in `.github/workflows/validate.yml` to make broken cross-references into errors (not warnings). This prevents new skills from shipping with unresolved references.

Local development retains the lenient default (`STRICT_REFS` unset or `0`) so authors can iterate on skills before their cross-reference targets exist.

```yaml
# In validate.yml
env:
  STRICT_REFS: 1
```

---

## 7. Migration Checklist

When normalizing an existing skill to match this style guide:

- [ ] **Description**: Replace WHEN prefix with third-person declarative verb. Verify under 120 characters.
- [ ] **Scope section**: Add `## Scope` with bullet list of covered topics (if missing).
- [ ] **Out-of-scope section**: Add `## Out of scope` with attributed `[skill:]` cross-references (if missing).
- [ ] **Cross-references**: Convert all bare-text skill/agent names to `[skill:name]` syntax.
- [ ] **Self-references**: Remove any `[skill:]` references to the skill's own name.
- [ ] **Budget check**: Verify the description change is budget-neutral or budget-negative.
- [ ] **Validate**: Run `./scripts/validate-skills.sh` to confirm no new errors.

### Budget-Neutral Change Pattern

When rewriting a description, measure before and after:

```bash
# Before: count chars of old description
echo -n "old description text" | wc -c

# After: count chars of new description
echo -n "new description text" | wc -c
```

The new description must have the same or fewer characters than the old one.

---

## References

- [CONTRIBUTING-SKILLS.md](../CONTRIBUTING-SKILLS.md) -- skill authoring guide with detailed instructions
- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) -- "description must describe what the skill does AND when to use it"
- [Agent Skills Open Standard](https://github.com/anthropics/agent-skills) -- specification for skill format and discovery
- Research: assertive cues create 7x selection bias (arxiv 2602.14878v1)
- Research: position bias gives 80.2% selection rate to first-listed tools (arxiv 2511.01854)
