# fn-26: Code Smells and Anti-Pattern Skills

## Overview
Adds a dedicated code-smell and anti-pattern skill that Claude loads **proactively during all C# workflow modes** (planning, implementation, review). The skill covers common pitfalls that existing skills do not address: IDisposable misuse, warning suppression hacks, LINQ anti-patterns, event handling leaks, and design smells.

The skill complements (not duplicates) existing coverage:
- [skill:dotnet-csharp-async-patterns] already covers async gotchas (blocking on `.Result`, `async void`, fire-and-forget)
- [skill:dotnet-csharp-coding-standards] already covers naming, style, file organization
- [skill:dotnet-csharp-dependency-injection] already covers captive dependency
- [skill:dotnet-csharp-nullable-reference-types] already covers NRT annotation mistakes
- fn-9 `dotnet-agent-gotchas` (planned) will cover LLM-specific generation mistakes

This epic focuses on the **gap**: general developer-facing code smells that any C# developer (human or AI) should avoid.

## Motivation

Real-world code review feedback like these should be caught proactively:
1. **Async lambda exception routing**: `TryEnqueue` with async lambda — exceptions inside the lambda not routed through `TaskCompletionSource`, causing silent failures
2. **Warning suppression hacks**: Invoking events with `null` args to suppress CS0067 instead of using `#pragma warning disable CS0067` — creates misleading behavior and masks real bugs

These are NOT currently covered by any existing skill. Both motivating examples MUST appear in `details.md` as "bad pattern → correct fix" snippets.

## Scope

**Skills (1 new):**
- `dotnet-csharp-code-smells` — Proactive code smell and anti-pattern detection during writing, reviewing, or planning C# code

**Scope boundary with fn-9:** This skill covers general .NET code smells (patterns any developer should avoid). fn-9's `dotnet-agent-gotchas` covers LLM-specific generation mistakes (wrong NuGet packages, bad project structure, MSBuild errors). Cross-reference in SKILL.md uses plain text "(planned: fn-9 `dotnet-agent-gotchas`)" — not `[skill:...]` syntax — since the target skill does not yet exist.

**Scope boundary with fn-4:** `dotnet-add-analyzers` configures Roslyn analyzers (CA rules). This skill documents which patterns to watch for during code review and planning, complementing (not replacing) static analysis. Where a CA rule exists, the skill references it (e.g., "CA2000 already catches this — ensure analyzers are enabled").

## Anti-Pattern Categories to Cover (gaps only)

| Category | What's Missing | Already Covered By |
|----------|---------------|-------------------|
| Resource management (IDisposable) | Missing `using`, undisposed fields, wrong Dispose pattern | — (NOT covered) |
| Warning suppression hacks | Invoking events with `null` to suppress CS0067, dummy assignments | — (NOT covered) |
| LINQ misuse | Premature `.ToList()`, client-side evaluation, multiple enumeration | — (NOT covered) |
| Event handling leaks | Not unsubscribing, raising in constructor, `async void` handler misuse | Partially by concurrency specialist agent |
| Design smells | God classes, long methods (>30 lines), long parameter lists (>5 params) | — (NOT covered) |
| Exception handling | Empty catch, catching base `Exception`, swallowing with log-only | Partially by [skill:dotnet-csharp-async-patterns] (fire-and-forget section) |
| String abuse | Concatenation in loops, missing `StringComparison`, raw string over interpolation | Partially by [skill:dotnet-csharp-coding-standards] |
| Mutable static state | `static` mutable fields without synchronization | Covered by concurrency specialist agent |

Categories marked "NOT covered" are the primary focus. Categories marked "Partially" get brief mentions with cross-references.

## "Always-On" Triggering Strategy

The skill uses a broad `description` field to match virtually any C# interaction:
```yaml
description: "WHEN writing, reviewing, or planning C# code. Catches code smells, anti-patterns, and common pitfalls."
```

This triggers the skill during ALL workflow modes. To manage context size:
1. Keep SKILL.md body concise (<300 lines) with a checklist format
2. Move detailed examples and explanations to supporting files (e.g., `details.md`)
3. Structure as scannable table, not prose — the agent needs to quickly identify relevant patterns

**Trigger verification**: There is no automated matcher test available. Verification is manual: the description field must contain the broad "WHEN writing, reviewing, or planning C# code" pattern, matching the convention used by other always-on skills (e.g., `dotnet-csharp-coding-standards`). The `validate-skills.sh` script confirms description format and budget compliance.

## Shared File Contention

Task fn-26.2 modifies high-contention registry files (`plugin.json`, `dotnet-advisor/SKILL.md`, `dotnet-artisan-spec.md`, fn-1 umbrella spec). These files are also modified by other Wave 1 epics. Mitigation: fn-26.2 should be implemented after fn-3 tasks that touch these same files are merged, or conflicts should be resolved during merge. All edits are additive (append to arrays/tables), minimizing conflict surface.

## Key Context

- Description budget: currently 3,085 chars across 25 skills. Adding ~95 chars. Well within 12,000 WARN threshold.
- Existing `dotnet-advisor` routing table needs a new entry for the code-smell skill.
- `fn-1` umbrella spec and `docs/dotnet-artisan-spec.md` need updated skill counts.
- Validation: `./scripts/validate-skills.sh` must pass after adding new SKILL.md.

## Quick Commands
```bash
# Verify skill exists and has frontmatter
test -f skills/core-csharp/dotnet-csharp-code-smells/SKILL.md && echo OK || echo MISSING
grep "^name:" skills/core-csharp/dotnet-csharp-code-smells/SKILL.md
grep "^description:" skills/core-csharp/dotnet-csharp-code-smells/SKILL.md

# Validate all skills pass
./scripts/validate-skills.sh

# Check budget impact
grep CURRENT_DESC_CHARS < <(./scripts/validate-skills.sh 2>&1)
```

## Acceptance Criteria
1. `dotnet-csharp-code-smells` skill exists at `skills/core-csharp/dotnet-csharp-code-smells/SKILL.md` with `name` and `description` frontmatter
2. Description uses the broad "WHEN writing, reviewing, or planning C# code" pattern to trigger during all modes
3. Skill covers at minimum: IDisposable misuse, warning suppression hacks, LINQ anti-patterns, event handling leaks, design smells
4. Each anti-pattern entry includes: the smell, why it's harmful, the fix, and a cross-reference to the relevant skill or CA rule
5. Skill body is <300 lines; detailed examples are in supporting files
6. No duplication with existing skills — cross-references for already-covered patterns (async gotchas → [skill:dotnet-csharp-async-patterns], naming → [skill:dotnet-csharp-coding-standards])
7. Scope boundary with fn-9 is documented (general code smells vs LLM-specific mistakes); reference uses plain text "(planned: fn-9)" not `[skill:...]` syntax
8. Registered in `plugin.json` skills array
9. Added to `dotnet-advisor` skill catalog (section 2: Core C#) and routing logic
10. `./scripts/validate-skills.sh` passes with `BUDGET_STATUS=OK` or `BUDGET_STATUS=WARN`
11. `fn-1` umbrella spec updated: fn-26 added to Wave 1 table as new row (`fn-26 | Code Smells & Anti-Patterns | 1 skill | depends on fn-2`), and fn-3 row's skill count updated from "7 skills + 1 agent" to "8 skills + 1 agent" (since this skill belongs to Core C# category)
12. `docs/dotnet-artisan-spec.md` Core C# section updated with `dotnet-csharp-code-smells` bullet using canonical `[skill:dotnet-csharp-code-smells]` cross-reference syntax
13. Both motivating examples (TryEnqueue async lambda exception routing and CS0067 warning suppression hack) appear in `details.md` with "bad pattern → correct fix" code snippets
14. All cross-references in updated docs use canonical `[skill:dotnet-csharp-code-smells]` syntax (never bare skill name)

## References
- Microsoft Code Quality Rules: https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/
- David Fowler Async Guidance: https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md
- Framework Design Guidelines: https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/
- Microsoft Engineering C# Code Review Checklist: https://microsoft.github.io/code-with-engineering-playbook/code-reviews/recipes/csharp/
- CS0067 Best Practices: https://learn.microsoft.com/en-us/dotnet/csharp/misc/cs0067
