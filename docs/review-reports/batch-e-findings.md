# Batch E Findings: UI Frameworks, Agent Meta-Skills

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | 17 |
| Clean | 3 |
| Needs Work | 10 |
| Critical | 4 |
| Total issues | 16 |
| Critical issues | 4 |
| High issues | 9 |
| Low issues | 3 |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | 2,094 |
| Skills over 120 chars | 5 |
| Projected savings if all trimmed to 120 | 208 chars |

Skills over 120 chars: dotnet-agent-gotchas (183), dotnet-csproj-reading (178), dotnet-solution-navigation (163), dotnet-build-analysis (158), dotnet-blazor-patterns (126).

Character counts measured using the canonical Python parser (strips YAML quotes, trims whitespace).

## Findings by Skill

### ui-frameworks

### dotnet-blazor-patterns

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 126 chars (121-140 = warn) -- slightly over 120-char target |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 6 refs resolve correctly |
| 6 | Error Handling | pass | 6 Agent Gotchas covering common Blazor mistakes |
| 7 | Examples | pass | Concrete C# and Razor code examples throughout |
| 8 | Composability | pass | Clear scope boundaries with dotnet-blazor-components and dotnet-blazor-auth |
| 9 | Consistency | pass | Matches ui-frameworks peer structure |
| 10 | Registration & Budget | warn | Registered but 126 chars pushes budget (>120 warn) |
| 11 | Progressive Disclosure Compliance | pass | 2,054 words -- well under threshold |

**Issues:**
- [High] Description at 126 chars slightly over 120-char target -- trim by condensing feature list
- [Low] Description could be more concise by removing "AOT-safe patterns" (niche concern for a patterns skill)

**Proposed description (118 chars):** `"WHEN building Blazor apps. Hosting models, render modes, routing, enhanced navigation, streaming rendering, prerender."`

---

### dotnet-blazor-components

**Category:** ui-frameworks
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 107 chars -- follows formula |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 6 refs resolve correctly |
| 6 | Error Handling | pass | 6 Agent Gotchas |
| 7 | Examples | pass | Concrete Razor and C# examples |
| 8 | Composability | pass | Clear scope boundary with dotnet-blazor-patterns |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 107 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,169 words |

**Issues:** (none)

---

### dotnet-blazor-auth

**Category:** ui-frameworks
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 120 chars -- exactly at limit |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 7 refs resolve correctly |
| 6 | Error Handling | pass | 6 Agent Gotchas covering auth-specific pitfalls |
| 7 | Examples | pass | Auth flow code examples per hosting model |
| 8 | Composability | pass | Cross-refs to dotnet-security-owasp and dotnet-api-security for depth |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 120 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,569 words |

**Issues:** (none)

---

### dotnet-uno-platform

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 117 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" marker on `[skill:dotnet-aot-wasm]` -- skill exists and is registered |
| 6 | Error Handling | pass | 8 Agent Gotchas |
| 7 | Examples | pass | XAML and C# examples |
| 8 | Composability | pass | Well-scoped with dotnet-uno-targets and dotnet-uno-mcp |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 117 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,104 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-aot-wasm]` -- skill exists and is registered in plugin.json; remove stale markers

---

### dotnet-uno-targets

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" markers on `[skill:dotnet-aot-wasm]` at lines 12 and 85 -- skill exists |
| 6 | Error Handling | pass | 7 Agent Gotchas plus per-platform Platform Gotchas subsections |
| 7 | Examples | pass | Platform-specific config and build examples |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 116 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,970 words -- approaching 3,000 threshold but still under |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-aot-wasm]` in two locations -- skill exists and is registered; remove stale markers

---

### dotnet-uno-mcp

**Category:** ui-frameworks
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 104 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | Clear workflow steps for MCP tool usage |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 3 refs resolve correctly |
| 6 | Error Handling | pass | 6 Agent Gotchas plus Fallback section |
| 7 | Examples | pass | MCP tool invocation examples with fully qualified IDs |
| 8 | Composability | pass | Well-scoped as MCP integration layer for Uno |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 104 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,948 words |

**Issues:** (none)

---

### dotnet-maui-development

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" marker on `[skill:dotnet-native-aot]` -- skill exists and is registered |
| 6 | Error Handling | pass | 8 Agent Gotchas including MAUI-specific caveats |
| 7 | Examples | pass | XAML, C#, and platform service examples |
| 8 | Composability | pass | Cross-refs to dotnet-uno-platform as migration alternative |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 112 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,648 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists and is registered; remove stale markers

---

### dotnet-maui-aot

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 109 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" markers on `[skill:dotnet-native-aot]`, `[skill:dotnet-aot-wasm]`, and `[skill:dotnet-aot-architecture]` -- all three exist and are registered |
| 6 | Error Handling | pass | 5 Agent Gotchas covering AOT-specific issues |
| 7 | Examples | pass | MSBuild property and csproj examples |
| 8 | Composability | pass | Well-scoped as AOT specialization for MAUI |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 109 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,893 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on three AOT skills (`dotnet-native-aot`, `dotnet-aot-wasm`, `dotnet-aot-architecture`) -- all exist and are registered; remove stale markers

---

### dotnet-winui

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 106 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists |
| 6 | Error Handling | pass | 9 Agent Gotchas -- highest count in category |
| 7 | Examples | pass | XAML x:Bind, packaging, and migration examples |
| 8 | Composability | pass | Cross-refs to dotnet-wpf-modern and dotnet-wpf-migration |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 106 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,099 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists and is registered; remove stale markers

---

### dotnet-wpf-modern

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 106 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists |
| 6 | Error Handling | pass | 7 Agent Gotchas |
| 7 | Examples | pass | C# host builder, MVVM Toolkit, and Fluent theme examples |
| 8 | Composability | pass | Clear scope with dotnet-winui and dotnet-wpf-migration |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 106 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,719 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists and is registered; remove stale markers

---

### dotnet-wpf-migration

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 107 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 7 refs resolve correctly |
| 6 | Error Handling | pass | 7 Agent Gotchas covering migration-specific pitfalls |
| 7 | Examples | pass | Migration step examples per path |
| 8 | Composability | pass | Hub skill linking to framework-specific skills |
| 9 | Consistency | warn | Missing `## Prerequisites` section that 11 of 13 ui-frameworks peers have |
| 10 | Registration & Budget | pass | 107 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,735 words |

**Issues:**
- [Low] Missing `## Prerequisites` section -- 11 of 13 ui-frameworks skills have one; add for consistency

---

### dotnet-winforms-basics

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 105 chars |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | - |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | warn | Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists |
| 6 | Error Handling | pass | 8 Agent Gotchas |
| 7 | Examples | pass | DPI-aware drawing, dark mode, and DI examples |
| 8 | Composability | pass | Cross-refs to dotnet-wpf-migration and dotnet-winui |
| 9 | Consistency | pass | - |
| 10 | Registration & Budget | pass | 105 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 1,925 words |

**Issues:**
- [High] Stale "(may not exist yet)" and "(soft dependency)" markers on `[skill:dotnet-native-aot]` -- skill exists and is registered; remove stale markers

---

### dotnet-ui-chooser

**Category:** ui-frameworks
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 99 chars -- concise |
| 2 | Description Triggering | pass | - |
| 3 | Instruction Clarity | pass | Decision tree format is actionable |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 8 refs resolve correctly -- widest cross-ref set in category |
| 6 | Error Handling | pass | 8 Agent Gotchas |
| 7 | Examples | pass | Decision tree format appropriate for chooser skill |
| 8 | Composability | pass | Routes to framework-specific skills |
| 9 | Consistency | warn | Missing `## Prerequisites` section that 11 of 13 ui-frameworks peers have |
| 10 | Registration & Budget | pass | 99 chars, registered |
| 11 | Progressive Disclosure Compliance | pass | 2,322 words |

**Issues:**
- [Low] Missing `## Prerequisites` section -- add for consistency with category peers

---

### agent-meta-skills

### dotnet-agent-gotchas

**Category:** agent-meta-skills
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 183 chars (>140 = fail) -- lists all 9 categories inline |
| 2 | Description Triggering | warn | Overly broad -- "generating or modifying .NET code" would trigger on nearly any .NET request |
| 3 | Instruction Clarity | pass | Anti-Pattern / Corrected format is very clear |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 8 refs resolve correctly |
| 6 | Error Handling | pass | The entire skill IS error handling guidance |
| 7 | Examples | pass | Anti-pattern and corrected code pairs throughout |
| 8 | Composability | pass | Cross-refs to domain-specific skills for depth |
| 9 | Consistency | pass | Matches agent-meta-skills structure (Overview, Categories, Slopwatch) |
| 10 | Registration & Budget | fail | 183 chars severely impacts budget -- 63 chars over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,033 words |

**Issues:**
- [Critical] Description at 183 chars far exceeds 140-char fail threshold -- remove inline category enumeration
- [High] Description trigger "generating or modifying .NET code" is overly broad -- narrow to "making common .NET mistakes"

**Proposed description (115 chars):** `"WHEN generating or modifying .NET code. Catches common agent mistakes: async, NuGet, deprecated APIs, trimming, DI."`

---

### dotnet-build-analysis

**Category:** agent-meta-skills
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 158 chars (>140 = fail) -- lists too many sub-topics inline |
| 2 | Description Triggering | pass | "interpreting MSBuild output" is specific |
| 3 | Instruction Clarity | pass | Error code tables and pattern examples are actionable |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 3 refs resolve correctly |
| 6 | Error Handling | pass | The entire skill covers build error interpretation |
| 7 | Examples | pass | MSBuild output examples with annotations |
| 8 | Composability | pass | Cross-refs to dotnet-csproj-reading for project file specifics |
| 9 | Consistency | pass | Matches agent-meta-skills structure |
| 10 | Registration & Budget | fail | 158 chars severely impacts budget -- 38 chars over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,708 words |

**Issues:**
- [Critical] Description at 158 chars exceeds 140-char fail threshold -- condense sub-topic list

**Proposed description (116 chars):** `"WHEN interpreting MSBuild output, NuGet errors, or analyzer warnings. Error codes, restore failures, CI drift fixes."`

---

### dotnet-csproj-reading

**Category:** agent-meta-skills
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 178 chars (>140 = fail) -- enumerates all subsections inline |
| 2 | Description Triggering | pass | "reading or modifying .csproj files" is specific |
| 3 | Instruction Clarity | pass | Annotated XML examples are excellent |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 3 refs resolve correctly |
| 6 | Error Handling | pass | Slopwatch Anti-Patterns section covers common mistakes |
| 7 | Examples | pass | Annotated XML examples for every subsection |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | Matches agent-meta-skills structure |
| 10 | Registration & Budget | fail | 178 chars severely impacts budget -- 58 chars over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,079 words |

**Issues:**
- [Critical] Description at 178 chars exceeds 140-char fail threshold -- remove exhaustive subsection list

**Proposed description (116 chars):** `"WHEN reading or modifying .csproj files. SDK-style structure, PropertyGroup/ItemGroup, conditions, CPM, build props."`

---

### dotnet-solution-navigation

**Category:** agent-meta-skills
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 163 chars (>140 = fail) -- lists all subsections inline |
| 2 | Description Triggering | pass | "orienting in a .NET solution" is specific |
| 3 | Instruction Clarity | pass | Discovery patterns and heuristics are actionable |
| 4 | Progressive Disclosure | pass | - |
| 5 | Cross-References | pass | All 3 refs resolve correctly |
| 6 | Error Handling | pass | Slopwatch Anti-Patterns section |
| 7 | Examples | pass | CLI commands and discovery heuristics |
| 8 | Composability | pass | - |
| 9 | Consistency | pass | Matches agent-meta-skills structure |
| 10 | Registration & Budget | fail | 163 chars severely impacts budget -- 43 chars over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,024 words |

**Issues:**
- [Critical] Description at 163 chars exceeds 140-char fail threshold -- condense sub-topic list

**Proposed description (114 chars):** `"WHEN orienting in a .NET solution. Entry points, solution files (.sln/.slnx), dependency graphs, config locations."`

---

## Cross-Cutting Observations

### 1. Stale "may not exist yet" markers across 7 ui-frameworks skills

Seven skills reference `[skill:dotnet-native-aot]` or `[skill:dotnet-aot-wasm]` with "(may not exist yet)" and/or "(soft dependency)" markers. All three referenced AOT skills (`dotnet-native-aot`, `dotnet-aot-wasm`, `dotnet-aot-architecture`) now exist and are registered in plugin.json. The stale markers should be removed from:

- dotnet-uno-platform (dotnet-aot-wasm)
- dotnet-uno-targets (dotnet-aot-wasm, 2 locations)
- dotnet-maui-development (dotnet-native-aot)
- dotnet-maui-aot (dotnet-native-aot, dotnet-aot-wasm, dotnet-aot-architecture)
- dotnet-winui (dotnet-native-aot)
- dotnet-wpf-modern (dotnet-native-aot)
- dotnet-winforms-basics (dotnet-native-aot)

This is a systematic issue likely caused by skills being authored before the native-aot batch (Batch D) landed.

### 2. Agent-meta-skills descriptions are consistently over budget

All four agent-meta-skills have descriptions over 120 chars, with three exceeding the 140-char fail threshold. The pattern is identical: each description enumerates all subsections/categories inline. Trimming to the `[What] + [When]` formula with a condensed feature list would save 208 chars from the aggregate budget.

### 3. UI-frameworks skills are well-structured and consistent

The 13 ui-frameworks skills show strong structural consistency: all have `## Agent Gotchas`, `## References`, and 11 of 13 have `## Prerequisites`. Code examples are concrete and compilable. Cross-references use proper `[skill:name]` syntax throughout. The only structural gaps are the missing Prerequisites sections in dotnet-wpf-migration and dotnet-ui-chooser.

### 4. No details.md companion files needed

All 17 skills are under 3,000 words (highest is dotnet-uno-targets at 2,970). No skill requires a details.md companion file at this time. The progressive disclosure dimensions are uniformly passing.

### 5. Agent-meta-skills follow a distinct but consistent internal structure

The four agent-meta-skills use a different section pattern from ui-frameworks (Overview/Scope Boundary, numbered Subsections/Categories, Slopwatch Anti-Patterns, Cross-References, References) but are internally consistent with each other. This is appropriate -- the categories serve different purposes.

## Recommended Changes

### Critical (must fix)

- Description in dotnet-agent-gotchas (183 chars) -- trim to ~115 chars using proposed description
- Description in dotnet-csproj-reading (178 chars) -- trim to ~116 chars using proposed description
- Description in dotnet-solution-navigation (163 chars) -- trim to ~114 chars using proposed description
- Description in dotnet-build-analysis (158 chars) -- trim to ~116 chars using proposed description

### High (should fix)

- Stale "(may not exist yet)" markers in dotnet-uno-platform -- remove; dotnet-aot-wasm exists
- Stale "(may not exist yet)" markers in dotnet-uno-targets (2 locations) -- remove; dotnet-aot-wasm exists
- Stale "(may not exist yet)" markers in dotnet-maui-development -- remove; dotnet-native-aot exists
- Stale "(may not exist yet)" markers in dotnet-maui-aot (3 skills referenced) -- remove; all AOT skills exist
- Stale "(may not exist yet)" markers in dotnet-winui -- remove; dotnet-native-aot exists
- Stale "(may not exist yet)" markers in dotnet-wpf-modern -- remove; dotnet-native-aot exists
- Stale "(may not exist yet)" markers in dotnet-winforms-basics -- remove; dotnet-native-aot exists
- Description in dotnet-blazor-patterns (126 chars) -- trim to ~118 chars using proposed description
- dotnet-agent-gotchas trigger phrase "generating or modifying .NET code" is overly broad -- narrow activation scope

### Low (nice to have)

- Missing `## Prerequisites` in dotnet-wpf-migration -- add for consistency with 11/13 ui-frameworks peers
- Missing `## Prerequisites` in dotnet-ui-chooser -- add for consistency with 11/13 ui-frameworks peers
- dotnet-blazor-patterns description could drop "AOT-safe patterns" for tighter scope signal
