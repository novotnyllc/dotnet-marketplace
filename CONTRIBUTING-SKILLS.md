# Skill Authoring Guide

This guide covers everything you need to create, test, and ship a skill for **dotnet-artisan**. It merges the patterns from the [Anthropic Skill Authoring Guide](https://github.com/anthropics/agent-skills/blob/main/docs/skill-authoring-guide.md) with dotnet-artisan conventions.

For the general contribution workflow (prerequisites, PRs, code of conduct), see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 1. Quick Start

Create a working skill in five minutes using `dotnet-csharp-code-smells` as a reference.

**Step 1 -- Create the folder:**

```bash
mkdir -p skills/core-csharp/dotnet-my-new-skill
```

**Step 2 -- Write the SKILL.md:**

```markdown
---
name: dotnet-my-new-skill
description: "WHEN writing C# code. Detects common pitfalls in X."
---

# dotnet-my-new-skill

Guidance body goes here. See section 4 for writing instructions.

Cross-references: [skill:dotnet-csharp-coding-standards] for related patterns.
```

**Step 3 -- Register in plugin.json:**

Open `.claude-plugin/plugin.json` and add your skill path to the `skills` array:

```json
"skills/core-csharp/dotnet-my-new-skill"
```

**Step 4 -- Validate:**

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

**Step 5 -- Commit and PR.**

That's it. Read on for the details behind each step.

---

## 2. Skill Anatomy

### Folder Structure

Every skill lives in a category directory:

```
skills/<category>/<skill-name>/
  SKILL.md          # Required -- main skill file (casing matters)
  details.md        # Optional -- extended content, examples, deep dives
```

The `<skill-name>` directory name must match the `name` field in SKILL.md frontmatter exactly.

### SKILL.md Format

A skill file has two parts: **frontmatter** and **body**.

```markdown
---
name: dotnet-csharp-code-smells
description: "WHEN writing, reviewing, or planning C# code. Catches code smells and anti-patterns."
---

# dotnet-csharp-code-smells

Body content starts here...
```

**Frontmatter fields** (YAML between `---` fences):

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Must match directory name exactly |
| `description` | Yes | Target under 120 characters (see section 3) |

No other frontmatter fields are recognized. Keep it minimal.

### Companion Files

When a skill needs extended code examples, diagnostic tables, or deep-dive content that would bloat the main SKILL.md, extract it into a `details.md` file in the same directory. Reference it from the body:

```markdown
See `details.md` for code examples of each pattern.
```

This keeps the primary skill lean while making extended content available to agents that need depth. See `skills/core-csharp/dotnet-csharp-code-smells/details.md` for a working example.

---

## 3. Writing Effective Descriptions

The `description` field is the most important line in your skill. It determines when Claude activates your skill from the catalog.

### The Formula

Structure descriptions as: **[What] + [When] + [Triggers]**

```yaml
# Good -- tells Claude what, when, and why to activate
description: "WHEN writing, reviewing, or planning C# code. Catches code smells and anti-patterns."

# Bad -- vague, no activation context
description: "Helps with code quality stuff"
```

### Good vs. Bad Examples

| Quality | Description | Problem |
|---------|-------------|---------|
| Good | `WHEN writing C# async code. Patterns for async/await, cancellation, and parallel execution.` | Clear trigger, specific scope |
| Good | `Detects and fixes common .NET dependency injection lifetime misuse and registration errors.` | Actionable, precise |
| Bad | `C# patterns` | Too vague; matches everything and nothing |
| Bad | `Complete guide to everything about async programming in C# including all patterns, best practices, and common mistakes that developers make.` | 146 chars, over budget |

### The 120-Character Target

Each description must target **under 120 characters**. This is a budget constraint, not a style preference.

**Budget math:** The plugin loads all skill descriptions into Claude's context window at session start. With 100 skills at 120 characters each, the catalog consumes ~12,000 characters (the warning threshold). The hard fail threshold is 15,000 characters.

The validation script reports the current budget:

```
CURRENT_DESC_CHARS=12458
PROJECTED_DESC_CHARS=12000
BUDGET_STATUS=WARN
```

If your description pushes the budget over the warning threshold, shorten it or shorten other descriptions to compensate.

---

## 4. Writing Instructions

The body of SKILL.md contains the guidance Claude uses when the skill is active.

### Progressive Disclosure

Structure content in layers of increasing depth:

1. **Frontmatter** -- Name and description (always loaded in catalog)
2. **SKILL.md body** -- Core guidance, patterns, decision trees (loaded when skill activates)
3. **`details.md`** -- Extended examples, edge cases (available on demand)

This mirrors the Anthropic guide's recommendation: keep the primary skill focused on actionable guidance, and push verbose examples into companion files.

### Cross-Reference Syntax

Reference other skills using the machine-parseable syntax:

```markdown
See [skill:dotnet-csharp-async-patterns] for async/await guidance.
```

Rules:
- Always use `[skill:skill-name]` -- bare text skill names are not machine-parseable
- The skill name must match an existing `name` field in another SKILL.md
- Unresolved references produce validation warnings

### Content Patterns

- Use real .NET code examples, not pseudocode
- Include tables for pattern catalogs (smell/fix/rule format works well)
- Add an **Agent Gotchas** section for common AI agent mistakes
- Mark scope boundaries with "**Out of scope:**" plus attribution to the owning skill
- Include a **References** section linking to Microsoft Learn and authoritative sources

### Size Limit

Keep SKILL.md under **5,000 words**. If you need more space, use `details.md` for the overflow. Oversized skills degrade Claude's ability to follow instructions because they compete for context window space.

---

## 5. Testing Your Skill

### Triggering Test

Before validating, manually test that your skill activates correctly:

1. Start a Claude Code session in a .NET project with dotnet-artisan installed
2. Ask a question that should trigger your skill
3. Verify Claude references your skill's guidance in the response

### Validation Commands

Both commands must pass before merging. Run them from the repo root:

**1. Skill validation** -- Checks frontmatter structure, required fields, directory naming, description length, cross-references, and budget:

```bash
./scripts/validate-skills.sh
```

**2. Marketplace validation** -- Verifies `plugin.json` and `marketplace.json` consistency, confirms every registered skill path exists on disk:

```bash
./scripts/validate-marketplace.sh
```

**Run both in sequence:**

```bash
./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
```

If either command fails, fix the issue before committing. The same commands run in CI on every push and PR.

---

## 6. Common Patterns

These five patterns from the Anthropic skill authoring guide apply directly to dotnet-artisan skills.

### Sequential Workflow

Guide Claude through ordered steps. Used in scaffolding and migration skills.

```markdown
## Workflow
1. Detect project type with [skill:dotnet-project-analysis]
2. Check target framework via [skill:dotnet-version-detection]
3. Apply migration steps based on detected version
```

Example: [skill:dotnet-modernize] walks through SDK upgrade steps in order.

### Multi-MCP Coordination

Combine MCP server data with skill guidance. The plugin integrates Context7, Uno Platform, and Microsoft Learn MCP servers.

```markdown
Use `mcp__context7__query-docs` to fetch current API documentation,
then apply the patterns from this skill.
```

Example: [skill:dotnet-uno-mcp] coordinates Uno Platform MCP tools with skill guidance.

### Iterative Refinement

Build-test-fix loops for quality skills. Structure guidance so Claude can iterate.

```markdown
1. Run analyzers: `dotnet build /warnaserror`
2. Review each warning against the table below
3. Apply the fix pattern
4. Re-run to confirm resolution
```

Example: [skill:dotnet-csharp-code-smells] provides smell/fix tables for iterative cleanup.

### Context-Aware Tool Selection

Help Claude choose the right tool based on project context.

```markdown
## Decision Tree
- If `*.csproj` contains `<OutputType>Exe</OutputType>` -> console app patterns
- If `*.csproj` contains `<Project Sdk="Microsoft.NET.Sdk.Web">` -> web API patterns
```

Example: [skill:dotnet-data-access-strategy] selects between EF Core, Dapper, and raw ADO.NET based on project characteristics.

### Domain-Specific Intelligence

Encode domain expertise that general LLMs lack.

```markdown
## CA Rules Quick Reference
| Rule | Description |
|------|-------------|
| CA2000 | Dispose objects before losing scope |
```

Example: [skill:dotnet-csharp-code-smells] encodes Roslyn analyzer rule knowledge with fix patterns.

---

## 7. Troubleshooting

### SKILL.md Casing

The file must be named exactly `SKILL.md` (uppercase). The validation script looks for this exact casing. `skill.md`, `Skill.md`, and other variants will not be found.

### YAML Frontmatter

- Frontmatter must be enclosed between two `---` lines
- The `name` value must match the directory name exactly
- Quote descriptions that contain colons, commas, or special YAML characters
- Do not add extra frontmatter fields beyond `name` and `description`

### Skill Not Triggering

If your skill is not activating in Claude Code sessions:

1. Verify the skill is registered in `.claude-plugin/plugin.json`
2. Check that the `description` contains clear activation triggers (see section 3)
3. Confirm the `name` field matches the directory name
4. Run `./scripts/validate-marketplace.sh` to verify registration

### Description Budget Exceeded

If validation reports `BUDGET_STATUS=WARN` or `BUDGET_STATUS=FAIL`:

1. Check `CURRENT_DESC_CHARS` in the validation output
2. Shorten your description -- remove filler words, focus on triggers
3. If still over budget, audit other skills for descriptions that can be tightened

### Cross-Reference Resolution

If validation reports unresolved cross-references:

1. Verify the target skill name matches an existing `name` frontmatter field
2. Check for typos in `[skill:exact-name-here]`
3. If the target skill does not exist yet, the reference will produce a warning

---

## 8. Pre-Commit Checklist

Before committing a new or modified skill:

- [ ] **Folder created** at `skills/<category>/<skill-name>/`
- [ ] **SKILL.md** exists with correct casing
- [ ] **Frontmatter** has `name` and `description` fields
- [ ] **`name` matches** the directory name exactly
- [ ] **Description under 120 characters** (check budget math)
- [ ] **Cross-references** use `[skill:skill-name]` syntax
- [ ] **Registered in plugin.json** -- skill path added to the `skills` array
- [ ] **Validation passes** -- both commands run clean:
  ```bash
  ./scripts/validate-skills.sh && ./scripts/validate-marketplace.sh
  ```
- [ ] **Commit message** follows conventional commits (`feat(<scope>): ...`)

---

## References

- [Anthropic Skill Authoring Guide](https://github.com/anthropics/agent-skills/blob/main/docs/skill-authoring-guide.md) -- the complete six-chapter guide this manual adapts
- [Agent Skills Open Standard](https://github.com/anthropics/agent-skills) -- specification for skill format and discovery
- [CONTRIBUTING.md](CONTRIBUTING.md) -- general contribution workflow, prerequisites, and PR process
- [CLAUDE.md](CLAUDE.md) -- project conventions and validation commands
- Example skill: [`skills/core-csharp/dotnet-csharp-code-smells/SKILL.md`](skills/core-csharp/dotnet-csharp-code-smells/SKILL.md) -- well-structured skill with companion `details.md`
