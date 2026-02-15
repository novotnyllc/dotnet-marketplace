# Batch A Findings: Foundation, Core C#, Project Structure, Release Management

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | 20 |
| Clean | 11 |
| Needs Work | 6 |
| Critical | 3 |
| Total issues | 13 |
| Critical issues | 4 |
| High issues | 2 |
| Low issues | 7 |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | 2,472 |
| Skills over 120 chars | 3 |
| Projected savings if all trimmed to 120 | 207 chars |

Skills over 120 chars: dotnet-advisor (257), dotnet-project-analysis (166), dotnet-version-detection (144).

Character counts measured using the canonical Python parser from `_validate_skills.py` (strips YAML quotes, trims whitespace).

## Findings by Skill

### foundation

### dotnet-advisor

**Category:** foundation
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 257 chars (>140 = fail) -- massively over 120-char limit; lists too many technologies |
| 2 | Description Triggering | warn | Overly broad -- would trigger for nearly any .NET request; WHEN NOT clause is unusual |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | fail | Two references to `[skill:dotnet-scaffolding-base]` which does not exist (should be `dotnet-scaffold-project`) |
| 6 | Error Handling | pass | Router skill -- N/A for error handling; pass by design |
| 7 | Examples | pass | Router skill -- catalog format is appropriate |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | Registered but description at 257 chars severely impacts aggregate budget |
| 11 | Progressive Disclosure Compliance | pass | 1,518 words -- well under threshold |

**Issues:**
- [Critical] Description is 257 chars (limit: 120) -- trim to formula: `[What] + [When]`, remove exhaustive technology list. The description alone consumes 2x its budget allocation.
- [Critical] Two broken cross-references to `[skill:dotnet-scaffolding-base]` (lines 42, 171) -- replace with `[skill:dotnet-scaffold-project]`
- [High] WHEN NOT clause in description is unconventional -- remove it and let the skill catalog speak for itself

**Proposed description (112 chars):** `"WHEN working with .NET, C#, ASP.NET Core, or related frameworks. Routes queries to specialist skills by context."`

---

### dotnet-version-detection

**Category:** foundation
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 144 chars (>140 = fail) -- over 120-char limit; WHEN NOT clause is unconventional |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve correctly |
| 6 | Error Handling | pass | Covers edge cases (no SDK, MSBuild indirection, inconsistent files) |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 144 chars pushes budget (>120 warn range) |
| 11 | Progressive Disclosure Compliance | pass | 1,561 words |

**Issues:**
- [Critical] Description at 144 chars exceeds 140-char fail threshold -- trim by removing WHEN NOT clause
- [Low] WHEN NOT clause ("WHEN NOT no .NET project present") is double-negative and adds no value

**Proposed description (114 chars):** `"WHEN project has .csproj, global.json, or Directory.Build.props. Detects TFMs, SDK versions, and preview features."`

---

### dotnet-project-analysis

**Category:** foundation
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 166 chars (>140 = fail) -- over 120-char limit; WHEN NOT clause adds little value |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Covers edge cases (no solution, orphaned projects, circular refs) |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | warn | 166 chars significantly over limit (>120 warn range) |
| 11 | Progressive Disclosure Compliance | pass | 1,778 words |

**Issues:**
- [Critical] Description at 166 chars exceeds 140-char fail threshold -- trim by removing WHEN NOT clause and condensing
- [Low] WHEN NOT clause ("WHEN NOT single-file scripts") adds minimal discrimination value

**Proposed description (113 chars):** `"WHEN navigating .NET solution structure, project references, or build configuration. Analyzes .sln, .csproj, CPM."`

---

### plugin-self-publish

**Category:** foundation
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars -- under limit, follows formula |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | Template `[skill:<name>]` occurrences are documentation about the syntax, not broken refs |
| 6 | Error Handling | pass | Includes release checklist |
| 7 | Examples | pass | - |
| 8 | Composability | pass | `disable-model-invocation: true` prevents auto-triggering |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 112 chars |
| 11 | Progressive Disclosure Compliance | pass | 727 words |

**Issues:**
(none)

---

### core-csharp

### dotnet-csharp-modern-patterns

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | Good trigger phrases (records, pattern matching, primary constructors, etc.) |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Gotchas section for primary constructors |
| 7 | Examples | pass | Real C# code examples with TFM annotations |
| 8 | Composability | pass | Clear cross-refs to peer skills |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,348 words |

**Issues:**
(none)

---

### dotnet-csharp-coding-standards

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 114 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Analyzer enforcement section |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 114 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,214 words |

**Issues:**
(none)

---

### dotnet-csharp-async-patterns

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 109 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Comprehensive Agent Gotchas section (5 items) |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 109 chars |
| 11 | Progressive Disclosure Compliance | pass | 930 words |

**Issues:**
(none)

---

### dotnet-csharp-nullable-reference-types

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 114 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Agent Gotchas section (5 items) |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 114 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,256 words |

**Issues:**
(none)

---

### dotnet-csharp-dependency-injection

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 103 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Captive dependency warning, scope validation section |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 103 chars |
| 11 | Progressive Disclosure Compliance | pass | 856 words |

**Issues:**
(none)

---

### dotnet-csharp-configuration

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 114 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | ValidateOnStart, validation patterns covered |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 114 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,304 words |

**Issues:**
(none)

---

### dotnet-csharp-source-generators

**Category:** core-csharp
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars |
| 2 | Description Triggering | pass | Good trigger phrases covering both creating and consuming |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Diagnostic reporting, debugging section |
| 7 | Examples | pass | Full IIncrementalGenerator example with NuGet packages listed |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 115 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,614 words |

**Issues:**
(none)

---

### dotnet-csharp-code-smells

**Category:** core-csharp
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 102 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Error handling is the topic itself |
| 7 | Examples | pass | - |
| 8 | Composability | warn | References "planned fn-9 `dotnet-agent-gotchas` skill" -- fn-9 is implemented; update the scope boundary text |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 102 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,179 words; has details.md properly referenced |

**Issues:**
- [High] Out of Scope text says "planned fn-9 `dotnet-agent-gotchas` skill" but this skill exists and is registered -- update to reference it as `[skill:dotnet-agent-gotchas]` and remove "planned"

---

### dotnet-roslyn-analyzers

**Category:** core-csharp
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Meta-diagnostics section |
| 7 | Examples | pass | Full analyzer+codefix+test examples with NuGet packages listed |
| 8 | Composability | pass | Clear scope boundary |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | warn | 2,709 words -- approaching the ~3,000 word threshold for details.md extraction |

**Issues:**
- [Low] At 2,709 words, this skill is approaching the 3,000-word threshold. The extensive testing section and meta-diagnostics table could be extracted to a `details.md` companion. Not urgent but monitor if content grows.

---

### project-structure

### dotnet-project-structure

**Category:** project-structure
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 118 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | - |
| 7 | Examples | pass | Full MSBuild XML examples |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 118 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,106 words |

**Issues:**
(none)

---

### dotnet-scaffold-project

**Category:** project-structure
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | - |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 112 chars |
| 11 | Progressive Disclosure Compliance | pass | 970 words |

**Issues:**
(none)

---

### dotnet-add-analyzers

**Category:** project-structure
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 107 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | - |
| 7 | Examples | pass | - |
| 8 | Composability | pass | - |
| 9 | Consistency | warn | The grep command in the incremental adoption pattern uses `-oP` (PCRE) which is not available on macOS default grep |
| 10 | Registration & Budget | pass | 107 chars |
| 11 | Progressive Disclosure Compliance | pass | 947 words |

**Issues:**
- [Low] Grep command `grep -oP 'CA\d+'` uses PCRE flag not available on macOS default grep -- use `grep -oE 'CA[0-9]+'` for portability (per pitfalls memory: POSIX character classes)

---

### dotnet-add-ci

**Category:** project-structure
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | Clear scope boundary |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | - |
| 6 | Error Handling | pass | Explains key decisions |
| 7 | Examples | pass | Full GHA and ADO templates |
| 8 | Composability | pass | Clear scope boundary to depth CI skills |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 713 words |

**Issues:**
(none)

---

### dotnet-add-testing

**Category:** project-structure
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 16+ cross-refs resolve |
| 6 | Error Handling | pass | - |
| 7 | Examples | pass | - |
| 8 | Composability | pass | Clear scope boundary |
| 9 | Consistency | warn | Uses `--` for list separators in "What's Next" section while most peer skills use the same format, but missing Agent Gotchas section that some peers have |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 925 words |

**Issues:**
- [Low] No Agent Gotchas section -- peer skills like dotnet-csharp-async-patterns have one. Consider adding common test scaffolding mistakes (forgetting to add project references, missing CPM version entries).

---

### dotnet-modernize

**Category:** project-structure
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 106 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | References "fn-10 (Version Management depth epic)" and "fn-10" multiple times as bare text, not as skill cross-refs -- these are epic references which is technically acceptable but reduces navigability |
| 6 | Error Handling | pass | - |
| 7 | Examples | pass | Comprehensive scanning commands |
| 8 | Composability | pass | Clear scope boundary |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 106 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,581 words |

**Issues:**
- [Low] "fn-10" epic references in "What's Next" section could point to concrete skills when the multi-targeting skills exist -- currently [skill:dotnet-multi-targeting] and [skill:dotnet-version-upgrade] exist on disk but are not registered in plugin.json (flagged as Batch B issue)

---

### release-management

### dotnet-release-management

**Category:** release-management
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 117 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All refs resolve |
| 6 | Error Handling | pass | Agent Gotchas section (8 items) |
| 7 | Examples | pass | Full version.json, cliff.toml, branching diagrams |
| 8 | Composability | pass | Extensive scope boundary and out-of-scope documentation |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 117 chars |
| 11 | Progressive Disclosure Compliance | warn | 2,543 words -- approaching 3,000-word threshold |

**Issues:**
- [Low] At 2,543 words, approaching the details.md extraction threshold. The cliff.toml configuration and branching diagrams are candidates for extraction. Not urgent.

---

## Cross-Cutting Observations

1. **WHEN NOT clauses in descriptions:** Three foundation skills (dotnet-advisor, dotnet-version-detection, dotnet-project-analysis) use "WHEN NOT" negative clauses in their descriptions. This is unconventional and wastes budget characters. The WHEN NOT information adds little discrimination value -- Claude already knows when a skill does NOT apply from the positive WHEN clause.

2. **Description budget pressure from foundation skills:** The three over-limit descriptions in foundation contribute 207 chars of excess beyond the 120-char target. Trimming these to 120 chars each would save 207 chars from the aggregate budget (currently at 12,458).

3. **Broken cross-reference pattern:** `dotnet-scaffolding-base` appears twice in dotnet-advisor but the actual skill is named `dotnet-scaffold-project`. This is likely a rename that was not fully propagated.

4. **Stale "planned" references:** dotnet-csharp-code-smells references "planned fn-9 `dotnet-agent-gotchas` skill" but dotnet-agent-gotchas is implemented and registered. The Out of Scope text needs updating.

5. **Word count distribution:** All 20 skills are well within the 5,000-word SKILL.md limit. Two skills (dotnet-roslyn-analyzers at 2,709 and dotnet-release-management at 2,543) are approaching the 3,000-word details.md extraction suggestion threshold but are not yet at a level that requires action.

6. **Consistent quality in core-csharp category:** 8 of 9 core-csharp skills are Clean -- all have proper cross-references, Agent Gotchas sections, concrete examples, and stay within budget. The one exception (dotnet-csharp-code-smells) has only a minor stale reference issue. This category serves as the quality benchmark for other batches.

7. **grep portability:** dotnet-add-analyzers uses `grep -oP` (PCRE) which is not available on macOS default grep. Per pitfalls memory, commands should use POSIX character classes and ERE flags for portability.

8. **details.md usage:** Only dotnet-csharp-code-smells uses a details.md companion, and it does so correctly (2 references from SKILL.md). This is appropriate given the code examples would otherwise bloat the SKILL.md.

## Recommended Changes

### Critical (must fix)
- Trim `dotnet-advisor` description from 257 to under 120 chars -- remove exhaustive technology list and WHEN NOT clause
- Fix 2 broken `[skill:dotnet-scaffolding-base]` cross-references in `dotnet-advisor` to `[skill:dotnet-scaffold-project]`
- Trim `dotnet-project-analysis` description from 166 to under 120 chars (>140 = fail per rubric)
- Trim `dotnet-version-detection` description from 144 to under 120 chars (>140 = fail per rubric)

### High (should fix)
- Remove WHEN NOT clauses from all three foundation skill descriptions (dotnet-advisor, dotnet-version-detection, dotnet-project-analysis) to save budget and follow convention
- Update `dotnet-csharp-code-smells` Out of Scope text to remove "planned" and use `[skill:dotnet-agent-gotchas]` cross-ref syntax
- Consider adding an Agent Gotchas section to `dotnet-add-testing` (common scaffolding mistakes)

### Low (nice to have)
- Fix `grep -oP` to `grep -oE` in `dotnet-add-analyzers` for macOS portability
- Monitor `dotnet-roslyn-analyzers` (2,709 words) and `dotnet-release-management` (2,543 words) for details.md extraction if content grows
- Update `dotnet-modernize` "What's Next" fn-10 references to concrete skill cross-refs once multi-targeting skills are registered
- Add missing Agent Gotchas section to `dotnet-add-testing`
- Trim whitespace from description end if any trailing spaces exist
- Consider bidirectional cross-refs: dotnet-csharp-code-smells references dotnet-csharp-async-patterns but not vice versa for the code-smell-specific gotchas
