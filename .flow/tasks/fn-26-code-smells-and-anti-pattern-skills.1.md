## Description

Create the `dotnet-csharp-code-smells` SKILL.md at `skills/core-csharp/dotnet-csharp-code-smells/SKILL.md`. This skill provides proactive code-smell and anti-pattern detection that triggers during ALL C# workflow modes (planning, implementation, review).

**Size:** M
**Files:**
- `skills/core-csharp/dotnet-csharp-code-smells/SKILL.md` (main skill)
- `skills/core-csharp/dotnet-csharp-code-smells/details.md` (supporting file with detailed examples)

## Approach

- Follow the SKILL.md pattern at `skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md` for frontmatter format
- Use broad description: `"WHEN writing, reviewing, or planning C# code. Catches code smells, anti-patterns, and common pitfalls."`
- Structure body as scannable checklist/table (not prose) — the agent needs to quickly identify relevant patterns
- Each anti-pattern entry: Smell | Why harmful | Fix | CA rule or cross-ref
- Keep SKILL.md under 300 lines; put detailed code examples in `details.md` supporting file
- Cross-reference existing skills for already-covered patterns:
  - Async gotchas → `[skill:dotnet-csharp-async-patterns]`
  - Naming/style → `[skill:dotnet-csharp-coding-standards]`
  - DI lifetime misuse → `[skill:dotnet-csharp-dependency-injection]`
  - NRT mistakes → `[skill:dotnet-csharp-nullable-reference-types]`
  - LLM-specific mistakes → plain text "(planned: fn-9 `dotnet-agent-gotchas`)" — do NOT use `[skill:...]` syntax for skills that don't yet exist
- Cover these UNCOVERED categories (the gaps):
  1. **Resource management**: Missing `using`/IDisposable, undisposed fields, wrong Dispose pattern (ref CA2000, CA2213)
  2. **Warning suppression hacks**: Invoking events with `null` to suppress CS0067, dummy variable assignments. Correct alternatives: `#pragma warning disable CS0067` or explicit event accessors `{ add {} remove {} }`
  3. **LINQ anti-patterns**: Premature `.ToList()` in middle of chains, multiple enumeration of IEnumerable, client-side evaluation in EF Core
  4. **Event handling leaks**: Not unsubscribing (memory leaks), raising events in constructor, async void event handlers (only valid use of async void)
  5. **Design smells**: God classes (>500 lines), methods >30 lines, parameter lists >5 params, feature envy
  6. **Exception handling gaps**: Empty catch blocks, catching base `Exception` (CA1031), swallowing with log-only, throwing in finally

## Key context

- The user's motivating examples MUST both appear in `details.md` as "bad pattern → correct fix" code snippets:
  - `TryEnqueue` with async lambda: exceptions not routed through `TaskCompletionSource` — document under "async exception routing" with cross-ref to `[skill:dotnet-csharp-async-patterns]`
  - `SuppressWarnings` invoking events with `null` args — document under "warning suppression hacks" with alternatives: `#pragma warning disable CS0067` or `event Action E { add {} remove {} }`
- Where CA rules exist for a smell, reference them (so agent knows: "analyzer already catches this, ensure it's enabled")
- Scope boundary: this skill covers general code smells. `dotnet-agent-gotchas` (fn-9, planned) covers LLM-specific generation mistakes. Document this boundary in the skill's Out of Scope section. Use plain text reference, not `[skill:...]` syntax.
## Acceptance
- [ ] SKILL.md exists at `skills/core-csharp/dotnet-csharp-code-smells/SKILL.md`
- [ ] Frontmatter has `name: dotnet-csharp-code-smells` and broad description triggering on all C# modes
- [ ] Covers IDisposable misuse with CA2000/CA2213 references
- [ ] Covers warning suppression hacks (CS0067 examples, correct alternatives)
- [ ] Covers LINQ anti-patterns (premature materialization, multiple enumeration, client-side eval)
- [ ] Covers event handling leaks (unsubscribe, constructor raising, async void handlers)
- [ ] Covers design smells (God classes, long methods, long parameter lists)
- [ ] Covers exception handling gaps (empty catch, base Exception, log-and-swallow)
- [ ] Each entry has: Smell | Why harmful | Fix | CA rule or cross-ref
- [ ] Cross-references existing skills (not duplicating their content)
- [ ] Scope boundary with fn-9 documented in Out of Scope section using plain text (not `[skill:...]` syntax for planned skills)
- [ ] SKILL.md body <300 lines; detailed examples in `details.md`
- [ ] Supporting `details.md` file with code examples for each anti-pattern category
- [ ] `details.md` includes both motivating examples: TryEnqueue async lambda exception routing (bad→fix) and CS0067 warning suppression hack (bad→fix)
