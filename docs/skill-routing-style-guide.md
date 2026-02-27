# Skill Routing Style Guide

Canonical rules for writing skill and agent descriptions, scope sections, and cross-references in dotnet-artisan. All new and modified skills must follow these conventions.

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

### The 600-Character Target

Each description must be **at most 600 characters**. This is a budget constraint derived from the aggregate context window limit, not a style preference.

**Budget math:** The plugin loads all skill descriptions into the context window at session start. With 8 broad skills, the projected maximum is 4,800 characters (8 * 600). The validator enforces a FAIL threshold at 15,600 characters and a WARN threshold at 12,000 characters. With only 8 skills, each description can be significantly richer while staying well under budget (~25% of the 15,600 cap).

### Budget Threshold Semantics

The validator computes `BUDGET_STATUS` from `CURRENT_DESC_CHARS` only:

- **Acceptance criterion:** `CURRENT_DESC_CHARS < 12,000` (strictly less than)
- **BUDGET_STATUS:** Derived from `CURRENT_DESC_CHARS` only:
  - `OK`: `CURRENT_DESC_CHARS < 12,000`
  - `WARN`: `CURRENT_DESC_CHARS >= 12,000`
  - `FAIL`: `CURRENT_DESC_CHARS >= 15,600`
- **PROJECTED_DESC_CHARS:** Informational metric only (8 * 600 = 4,800). Not part of BUDGET_STATUS determination.
- Reaching exactly 12,000 counts as WARN. Acceptance requires being strictly below.

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

`[skill:name]` refers to any routable artifact -- **both skills and agents**. The validator resolves references against the union of skill directory names and agent file stems (without `.md`).

```markdown
# Referencing a skill
See [skill:dotnet-csharp] for async/await guidance (read references/async-patterns.md).

# Referencing an agent
Route to [skill:dotnet-security-reviewer] for security audit.
```

### Rules

1. **Always use `[skill:name]`** -- bare text skill/agent names are not machine-parseable
2. The `name` must match an existing skill directory name or agent file stem
3. The topic after "for" must be **specific** (not "more details" or "related patterns")
4. Unresolved references produce validation warnings (errors in strict mode)

### Self-References and Cycles

- **Self-references** (a skill referencing itself via `[skill:]`) are **always an error**. The validator rejects self-references.
- **Bidirectional references** (e.g., `[skill:dotnet-advisor]` in dotnet-tooling and `[skill:dotnet-tooling]` in dotnet-advisor) are **legitimate** and expected for hub skills. Cycle detection produces an **informational report**, not validation errors.

### Examples

| Quality | Reference | Problem |
|---------|-----------|---------|
| Good | `See [skill:dotnet-csharp] for async/await guidance (read references/async-patterns.md).` | Specific topic |
| Good | `Route to [skill:dotnet-architect] for framework selection decisions.` | Agent reference, specific topic |
| Bad | `See [skill:dotnet-csharp-async-patterns] for more details.` | Vague topic -- "more details" |
| Bad | `See dotnet-csharp-async-patterns for async guidance.` | Bare text -- not machine-parseable |
| Bad | `See [skill:dotnet-my-skill] for patterns.` | Self-reference (if written in dotnet-my-skill) |

---

## 4. Router Precedence Language

### Baseline-First Loading

`dotnet-csharp` is the **baseline skill** -- it loads first for any C# code path (read `references/coding-standards.md`). Other skills build on top of its conventions, never contradict them.

When writing skill content:
- Do not restate rules from dotnet-csharp's coding standards
- Reference it explicitly: `See [skill:dotnet-csharp] for baseline C# conventions.`
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
4. Include "Do not route for ..." disambiguation in the body (not the `description:` field) if needed

---

## 6. Invocation Contract

Every SKILL.md must satisfy three structural rules so the validator can confirm the skill is machine-invocable. These rules are purely structural and checkable without human judgment.

### Rules

1. **Scope bullets** -- `## Scope` contains at least one unordered bullet (`- `) within its section boundaries.
2. **Out-of-scope bullets** -- `## Out of scope` contains at least one unordered bullet (`- `) within its section boundaries.
3. **OOS cross-reference** -- At least one `## Out of scope` bullet contains a `[skill:<id>]` string.

**Only unordered bullets count.** Numbered lists (`1.`, `2.`, etc.) do not satisfy rules 1--3. This ensures machine-parseable, uniform section structure.

**No "Use when:" phrasing requirement.** The contract does not mandate any particular phrasing pattern in descriptions or body text. The three structural rules above are the complete contract.

**Note:** This contract applies to SKILL.md files only. Agent files (`agents/*.md`) use a different structure and are not subject to these rules. A separate invocation-signal convention for agents will be defined in a follow-up effort.

### Rule 3: Presence vs Resolution

Rule 3 checks that the `[skill:` string appears inside at least one OOS bullet. It does **not** validate that the referenced skill ID actually exists -- that is the job of `STRICT_REFS`. The two checks are independent:

| Toggle | What it checks | Default |
|--------|---------------|---------|
| `STRICT_INVOCATION` | Structural presence of bullets and `[skill:]` strings (rules 1--3) | WARN |
| `STRICT_REFS` | Referenced skill IDs resolve to existing skill directories or agent file stems | WARN |

These are independent toggles. Enabling one does not enable or require the other.

### Validation Behavior

By default, invocation contract violations produce warnings:

```
WARN:  skills/<skill-name>/SKILL.md -- INVOCATION_CONTRACT: Scope section has 0 unordered bullets (need >=1)
WARN:  skills/<skill-name>/SKILL.md -- INVOCATION_CONTRACT: Out of scope section has 0 unordered bullets (need >=1)
WARN:  skills/<skill-name>/SKILL.md -- INVOCATION_CONTRACT: No OOS bullet contains [skill:] cross-reference
```

The validator emits a summary key: `INVOCATION_CONTRACT_WARN_COUNT=<N>`.

Set `STRICT_INVOCATION=1` to promote contract warnings to errors (exit 1):

```bash
# Local: strict invocation contract enforcement
STRICT_INVOCATION=1 ./scripts/validate-skills.sh

# CI: add to workflow env
env:
  STRICT_INVOCATION: 1
```

### Positive Example

A skill that satisfies the invocation contract (from `dotnet-tooling`):

```markdown
## Scope

- .NET SDK, MSBuild, and project file management (.csproj, .sln, Directory.Build.props)
- NuGet package management, Central Package Management (CPM), version pinning
- TFM detection, multi-targeting, SDK version detection and preview feature gating
- Build, publish, and deployment configuration (AOT, trimming, single-file)

## Out of scope

- C# language patterns and coding standards -- see [skill:dotnet-csharp]
- ASP.NET Core / web API patterns -- see [skill:dotnet-api]
- CI/CD pipelines and container builds -- see [skill:dotnet-devops]
```

All three rules pass: Scope has 4 unordered bullets, OOS has 3 unordered bullets, and every OOS bullet contains `[skill:]`.

### Negative Example

A skill that fails the invocation contract:

```markdown
## Scope

1. Reading TFM from .csproj
2. Multi-targeting detection

## Out of scope

- Project structure analysis beyond TFM
- Framework upgrade migration steps
```

Failures:
- **Rule 1 fails**: Scope uses numbered list items, not unordered bullets.
- **Rule 3 fails**: No OOS bullet contains a `[skill:]` cross-reference. (Rule 2 passes: OOS has 2 unordered bullets.)

### Rollout Playbook

The invocation contract ships in **WARN-only mode** by default. All 8 skills have been audited and comply. CI can flip to `STRICT_INVOCATION=1` to enforce the contract as a merge gate. The warning count (`INVOCATION_CONTRACT_WARN_COUNT`) serves as a regression metric.

---

## 7. CI Strict Mode

### STRICT_REFS Recommendation

Set `STRICT_REFS=1` in `.github/workflows/validate.yml` to make broken cross-references into errors (not warnings). This prevents new skills from shipping with unresolved references.

Local development retains the lenient default (`STRICT_REFS` unset or `0`) so authors can iterate on skills before their cross-reference targets exist.

```yaml
# In validate.yml
env:
  STRICT_REFS: 1
```

`STRICT_REFS=1` is enabled in CI. The validator resolves `[skill:]` references against both skill directory names and agent file stems.

### STRICT_INVOCATION Recommendation

Set `STRICT_INVOCATION=1` in `.github/workflows/validate.yml` to make invocation contract violations into errors (not warnings). This prevents new skills from shipping without proper Scope/OOS structure.

```yaml
# In validate.yml
env:
  STRICT_INVOCATION: 1
```

`STRICT_INVOCATION` and `STRICT_REFS` are independent toggles. See section 6 for the invocation contract rules and rollout plan.

---

## 8. Companion Files (`references/`)

Skills use a `references/` subdirectory for extended content that would bloat the main SKILL.md. The SKILL.md Routing Table indexes these files by topic.

### When to Use

- Extended code examples, diagnostic tables, or deep-dive content for a specific topic area
- Content that would push SKILL.md beyond the 5,000-word limit
- Topics that only a subset of users need (progressive disclosure)

### Naming Convention

- Files live at `skills/<skill-name>/references/<topic>.md`
- Use lowercase kebab-case filenames: `async-patterns.md`, `coding-standards.md`
- Each file must have an H1 title (`# ...`) in human-readable Title Case (e.g., `# Async Patterns`)
- Known acronyms are preserved in titles: EF, MSBuild, gRPC, WinUI, MAUI, AOT, WPF, WinForms, TUI, LINQ, DI
- Titles must NOT use slug-style names (e.g., `# dotnet-async-patterns` is invalid)

### Structure Rules

- **No `## Scope` or `## Out of scope` sections.** Scope boundaries belong in the parent SKILL.md only. Reference files inherit their scope from the Routing Table entry.
- **`[skill:]` cross-references** may appear in reference files but must resolve against the same known IDs set (skill directory names + agent file stems) used for SKILL.md validation. Unresolved refs are always errors (no `--allow-planned-refs` downgrade).
- **No frontmatter required.** Reference files are plain markdown with an H1 title.

### Routing Table Integration

Each domain SKILL.md has a Routing Table that indexes its companion files:

```markdown
## Routing Table

| Topic | Keywords | Description | Companion File |
|-------|----------|-------------|----------------|
| Async/await | async, Task, ConfigureAwait | async/await, Task patterns | references/async-patterns.md |
```

The validator verifies that every file path in the `Companion File` column exists on disk.

---

## 9. `[skill:]` Syntax for Skills and Agents

The `[skill:name]` syntax is the universal cross-reference format for **both skills and agents**. There is no separate `[agent:]` syntax.

### Resolution Rules

- The `<name>` must match either a **skill directory name** (e.g., `dotnet-csharp`) or an **agent file stem** (e.g., `dotnet-security-reviewer`, the filename without `.md`)
- The validator resolves against the union of both sets: `known_ids = {skill dirs} | {agent stems}`
- Unresolved references produce warnings (or errors when `STRICT_REFS=1`)

### Examples

```markdown
# Referencing a skill
See [skill:dotnet-csharp] for async/await guidance.

# Referencing an agent (same syntax)
Route to [skill:dotnet-security-reviewer] for security audit.
Route to [skill:dotnet-architect] for framework selection decisions.
```

### Rationale

A unified syntax simplifies tooling and avoids the need for authors to distinguish between skills and agents when writing cross-references. The validator handles both transparently.

---

## 10. Migration Checklist

When normalizing an existing skill to match this style guide:

- [ ] **Description**: Replace WHEN prefix with third-person declarative verb. Verify under 600 characters.
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
