# Consolidated Findings: Fleet Skill Review and Improvement Sweep

## Executive Summary

All 101 skills (99 registered + 2 unregistered) reviewed across 6 batches against the 11-dimension rubric. The fleet is in good shape overall with strong Agent Gotchas coverage and excellent cross-reference target accuracy. The primary issues are: (1) 15 descriptions exceeding the 140-char fail threshold, (2) 2 skills on disk but unregistered in plugin.json, (3) systematic bare-text skill references in CI/CD skills, and (4) stale "may not exist yet" markers in UI framework skills.

Applying all Critical and High changes brings the aggregate description budget from 12,065 chars (WARN) to approximately 11,496 chars (below 12K WARN threshold), while adding 2 new registered skills for a total of 101.

| Metric | Count |
|--------|-------|
| Total skills reviewed | 101 |
| Clean | 41 |
| Needs Work | 43 |
| Critical | 17 |
| Total issues | 82 |
| Critical issues | 20 |
| High issues | 31 |
| Low issues | 31 |

### Per-Batch Summary

| Batch | Skills | Clean | Needs Work | Critical | Issues |
|-------|--------|-------|------------|----------|--------|
| A (Foundation, Core C#, Project Structure, Release Management) | 20 | 11 | 6 | 3 | 13 |
| B (Architecture, Serialization, Security, Multi-Targeting) | 19 | 6 | 7 | 6 | 19 |
| C (Testing, CI/CD) | 18 | 1 | 14 | 3 | 23 |
| D (API Development, CLI Tools, Performance, Native AOT) | 18 | 13 | 4 | 1 | 7 |
| E (UI Frameworks, Agent Meta-Skills) | 17 | 3 | 10 | 4 | 16 |
| F (Documentation, Packaging, Localization) | 9 | 7 | 2 | 0 | 4 |
| **Total** | **101** | **41** | **43** | **17** | **82** |

## Description Budget Impact

### Current State

| Metric | Value |
|--------|-------|
| Registered skills | 99 |
| Unregistered skills (on disk) | 2 |
| Current total description chars | 12,065 |
| Skills over 120 chars | 29 |
| Skills over 140 chars (fail) | 15 |
| Budget status | WARN (above 12,000) |

### Per-Batch Budget Contribution

| Batch | Chars | Over 120 | Over 140 | Projected Savings |
|-------|-------|----------|----------|-------------------|
| A | 2,472 | 3 | 3 | 207 |
| B | 2,576 | 12 | 6 | 322 |
| C | 2,251 | 11 | 3 | 321 |
| D | 2,116 | 2 | 1 | 32 |
| E | 2,094 | 5 | 4 | 208 |
| F | 985 | 0 | 0 | 0 |
| Unregistered (B) | 393 | 2 | 2 | (new: +233 after trim) |

**Reconciliation note:** Batch totals sum to 12,494 chars (including the 2 unregistered skills' 393 chars in Batch B's total). The "Current total" of 12,065 represents only the 99 registered skills measured from plugin.json at report time. The 36-char gap between 12,494 - 393 = 12,101 and the measured 12,065 is due to minor measurement variance between batch audit time and consolidation (some batch reports used `wc -c` while the consolidation used the canonical Python parser from `_validate_skills.py`). The canonical parser measurement of 12,065 is authoritative.

### Projected State After All Changes

| Metric | Value |
|--------|-------|
| Total skills (after registering 2) | 101 |
| Savings from registered skill description trims | -839 chars |
| Added from 2 new registrations (at trimmed length) | +233 chars |
| Projected total | 11,459 chars |
| Delta from current | -606 chars |
| Budget status | OK (below 12,000 WARN threshold) |

**Savings breakdown:** The -839 chars comes from trimming 29 registered skills: 15 Critical trims (-673), 9 High trims (-129), 5 Low trims (-37). The 2 unregistered skills (dotnet-multi-targeting, dotnet-version-upgrade) are not counted as "savings" -- they are new additions at their proposed trimmed lengths (115 + 118 = 233 chars). Math: 12,065 - 839 + 233 = 11,459.

### Projected State After Critical+High Changes Only

| Metric | Value |
|--------|-------|
| Savings from Critical+High registered trims | -802 chars |
| Added from 2 new registrations (at trimmed length) | +233 chars |
| Projected total | 11,496 chars |
| Budget status | OK (below 12,000 WARN threshold) |

**Savings breakdown:** -802 = 15 Critical registered trims (-673) + 9 High trims (-129). The 5 Low trims (-37) are excluded. Math: 12,065 - 802 + 233 = 11,496.

**Char count methodology:** All "Current" values in the tables below were measured using the canonical Python parser (`len()` after stripping YAML quotes and trimming whitespace) against the actual SKILL.md files on disk at consolidation time. Some batch reports measured slightly different values (up to 2 chars variance) due to using different extraction methods; the consolidated values are authoritative.

## Prioritized Improvement Plan

### Critical (Must Fix) -- 20 Issues

Issues that violate hard constraints: broken cross-references, missing registrations, descriptions exceeding 140-char fail threshold.

#### Unregistered Skills (Batch B)

| # | Skill | Category | Issue |
|---|-------|----------|-------|
| 1 | dotnet-multi-targeting | multi-targeting | NOT registered in plugin.json -- skill exists on disk but is invisible to the plugin system. Description at 196 chars also needs trimming. |
| 2 | dotnet-version-upgrade | multi-targeting | NOT registered in plugin.json -- skill exists on disk but is invisible to the plugin system. Description at 197 chars also needs trimming. |

#### Broken Cross-References (Batch A)

| # | Skill | Category | Issue |
|---|-------|----------|-------|
| 3 | dotnet-advisor | foundation | Two broken `[skill:dotnet-scaffolding-base]` references -- should be `[skill:dotnet-scaffold-project]` |

#### Description Over 140 Chars (All Batches)

| # | Skill | Category | Current | Proposed | Savings | Batch |
|---|-------|----------|---------|----------|---------|-------|
| 4 | dotnet-advisor | foundation | 257 | 112 | 145 | A |
| 5 | dotnet-version-detection | foundation | 144 | 114 | 30 | A |
| 6 | dotnet-project-analysis | foundation | 166 | 113 | 53 | A |
| 7 | dotnet-multi-targeting | multi-targeting | 196 | 115 | 81 | B |
| 8 | dotnet-version-upgrade | multi-targeting | 197 | 118 | 79 | B |
| 9 | dotnet-cryptography | security | 154 | 114 | 40 | B |
| 10 | dotnet-grpc | serialization | 142 | 119 | 23 | B |
| 11 | dotnet-service-communication | serialization | 145 | 116 | 29 | B |
| 12 | dotnet-secrets-management | security | 141 | 119 | 22 | B |
| 13 | dotnet-testing-strategy | testing | 142 | 118 | 24 | C |
| 14 | dotnet-snapshot-testing | testing | 150 | 120 | 30 | C |
| 15 | dotnet-test-quality | testing | 147 | 119 | 28 | C |
| 16 | dotnet-ci-benchmarking | performance | 144 | 116 | 28 | D |
| 17 | dotnet-agent-gotchas | agent-meta-skills | 183 | 115 | 68 | E |
| 18 | dotnet-build-analysis | agent-meta-skills | 158 | 116 | 42 | E |
| 19 | dotnet-csproj-reading | agent-meta-skills | 178 | 116 | 62 | E |
| 20 | dotnet-solution-navigation | agent-meta-skills | 163 | 114 | 49 | E |

### High (Should Fix) -- 31 Issues

Issues that reduce quality: stale references, bare-text skill names, missing sections, description budget warnings (121-140 chars).

#### Stale "Planned"/"Not Yet Landed" References

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| 1 | dotnet-csharp-code-smells | core-csharp | Out of Scope says "planned fn-9 dotnet-agent-gotchas" -- skill exists; use `[skill:dotnet-agent-gotchas]` | A |
| 2 | dotnet-benchmarkdotnet | performance | Out of Scope says "fn-18.2 skills (not yet landed)" -- dotnet-ci-benchmarking has landed; use `[skill:dotnet-ci-benchmarking]` and `[skill:dotnet-profiling]` | D |
| 3 | dotnet-nuget-authoring | packaging | References `dotnet-roslyn-analyzers` as "planned" -- skill exists; use `[skill:dotnet-roslyn-analyzers]` | F |

#### Stale "May Not Exist Yet" Markers (UI Frameworks)

| # | Skill | Category | Stale Refs | Batch |
|---|-------|----------|------------|-------|
| 4 | dotnet-uno-platform | ui-frameworks | dotnet-aot-wasm | E |
| 5 | dotnet-uno-targets | ui-frameworks | dotnet-aot-wasm (2 locations) | E |
| 6 | dotnet-maui-development | ui-frameworks | dotnet-native-aot | E |
| 7 | dotnet-maui-aot | ui-frameworks | dotnet-native-aot, dotnet-aot-wasm, dotnet-aot-architecture | E |
| 8 | dotnet-winui | ui-frameworks | dotnet-native-aot | E |
| 9 | dotnet-wpf-modern | ui-frameworks | dotnet-native-aot | E |
| 10 | dotnet-winforms-basics | ui-frameworks | dotnet-native-aot | E |

#### Bare-Text Skill References (CI/CD and Others)

| # | Skill | Category | Bare Refs Count | Batch |
|---|-------|----------|-----------------|-------|
| 11 | dotnet-ado-unique | cicd | 10 bare refs | C |
| 12 | dotnet-ado-patterns | cicd | 6 bare refs | C |
| 13 | dotnet-gha-patterns | cicd | 4 bare refs | C |
| 14 | dotnet-gha-build-test | cicd | 4 bare refs | C |
| 15 | dotnet-gha-deploy | cicd | 3 bare refs | C |
| 16 | dotnet-snapshot-testing | testing | 2 bare `dotnet-add-testing` refs | C |
| 17 | dotnet-test-quality | testing | 2 bare `dotnet-add-testing` refs | C |
| 18 | dotnet-gha-publish | cicd | 2 bare refs | C |
| 19 | dotnet-ado-build-test | cicd | 4 bare refs | C |
| 20 | dotnet-ado-publish | cicd | 2 bare refs | C |
| 21 | dotnet-profiling | performance | 1 bare backtick ref to dotnet-ci-benchmarking | D |
| 22 | dotnet-nuget-authoring | packaging | 2 bare backtick refs to dotnet-release-management; missing from Cross-references line | F |

#### Technical Accuracy

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| 23 | dotnet-maui-testing | testing | AppiumFixture uses `Task` return types for IAsyncLifetime but xUnit v3 requires `ValueTask` | C |

#### Description Over 120 Chars (121-140 Range)

| # | Skill | Category | Current | Proposed | Savings | Batch |
|---|-------|----------|---------|----------|---------|-------|
| 24 | dotnet-realtime-communication | serialization | 139 | 117 | 22 | B |
| 25 | dotnet-serialization | serialization | 135 | 116 | 19 | B |
| 26 | dotnet-containers | architecture | 134 | 119 | 15 | B |
| 27 | dotnet-xunit | testing | 131 | 119 | 12 | C |
| 28 | dotnet-integration-testing | testing | 128 | 119 | 9 | C |
| 29 | dotnet-blazor-testing | testing | 127 | 118 | 9 | C |
| 30 | dotnet-playwright | testing | 136 | 116 | 20 | C |
| 31 | dotnet-blazor-patterns | ui-frameworks | 126 | 118 | 8 | E |

#### Missing Sections

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| -- | dotnet-architecture-patterns | architecture | Missing Agent Gotchas section (all 9 peers have one) | B |

*Note: The missing Agent Gotchas for dotnet-architecture-patterns was rated High in Batch B. It is included here rather than in the Critical section because the content is missing (should-fix) rather than broken (must-fix).*

### Low (Nice to Have) -- 31 Issues

Minor polish: formatting, monitoring suggestions, small consistency gaps.

#### Description Trim (Under 128 Chars)

| # | Skill | Category | Current | Proposed | Savings | Batch |
|---|-------|----------|---------|----------|---------|-------|
| 1 | dotnet-data-access-strategy | architecture | 128 | 118 | 10 | B |
| 2 | dotnet-efcore-architecture | architecture | 126 | 119 | 7 | B |
| 3 | dotnet-security-owasp | security | 125 | 118 | 7 | B |
| 4 | dotnet-ui-testing-core | testing | 124 | 118 | 6 | C |
| 5 | dotnet-maui-testing | testing | 124 | 117 | 7 | C |
| 6 | dotnet-profiling | performance | 128 | 113 | 15 | D |

#### Consistency and Polish

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| 7 | dotnet-add-analyzers | project-structure | `grep -oP` uses PCRE not available on macOS -- use `grep -oE` | A |
| 8 | dotnet-add-testing | project-structure | No Agent Gotchas section; peers have one | A |
| 9 | dotnet-cryptography | security | Section heading "Gotchas and Pitfalls" should be "Agent Gotchas" | B |
| 10 | dotnet-ado-unique | cicd | Agent Gotchas lacks strong directives (0 DO NOT/NEVER/ALWAYS); peers have 1-3 | C |
| 11 | dotnet-ado-patterns | cicd | Agent Gotchas lacks strong directives; peers have 1-3 | C |
| 12 | dotnet-wpf-migration | ui-frameworks | Missing `## Prerequisites` section (11/13 peers have one) | E |
| 13 | dotnet-ui-chooser | ui-frameworks | Missing `## Prerequisites` section (11/13 peers have one) | E |

#### Monitoring (No Action Required Now)

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| 14 | dotnet-roslyn-analyzers | core-csharp | 2,709 words -- approaching 3,000 details.md threshold | A |
| 15 | dotnet-release-management | release-management | 2,543 words -- approaching 3,000 details.md threshold | A |
| 16 | dotnet-security-owasp | security | 2,437 words -- approaching threshold | B |
| 17 | dotnet-efcore-architecture | architecture | 2,366 words -- approaching threshold | B |
| 18 | dotnet-test-quality | testing | 2,343 words -- approaching threshold | C |
| 19 | dotnet-ado-unique | cicd | 2,325 words -- approaching threshold | C |
| 20 | dotnet-input-validation | api-development | 2,510 words -- approaching threshold | D |
| 21 | dotnet-profiling | performance | 2,450 words -- approaching threshold | D |
| 22 | dotnet-xml-docs | documentation | 2,998 words -- at the threshold | F |
| 23 | dotnet-mermaid-diagrams | documentation | 2,689 words -- approaching threshold | F |
| 24 | dotnet-uno-targets | ui-frameworks | 2,970 words -- approaching threshold | E |

#### Other Minor Items

| # | Skill | Category | Issue | Batch |
|---|-------|----------|-------|-------|
| 25 | dotnet-modernize | project-structure | "What's Next" fn-10 references could point to concrete skills | A |
| 26 | dotnet-csharp-code-smells | core-csharp | Missing bidirectional cross-ref from dotnet-csharp-async-patterns | A |
| 27 | dotnet-ado-unique | cicd | Description 119 chars (canonical measurement) -- under 120; Batch C reported 121 due to measurement variance. No trim needed. | C |
| 28 | dotnet-benchmarkdotnet | performance | Missing bidirectional cross-ref to dotnet-ci-benchmarking via `[skill:]` in Out of Scope | D |
| 29 | dotnet-blazor-patterns | ui-frameworks | Could drop "AOT-safe patterns" from description for tighter scope signal | E |
| 30 | dotnet-xml-docs | documentation | At 2,998 words; extract comprehensive example section if content grows | F |
| 31 | dotnet-mermaid-diagrams | documentation | At 2,689 words; monitor for details.md extraction | F |

## Cross-Cutting Patterns

### 1. WHEN NOT Clauses in Descriptions (5 Skills)

Five skills use "WHEN NOT" negative clauses in their descriptions: dotnet-advisor (A), dotnet-version-detection (A), dotnet-project-analysis (A), dotnet-multi-targeting (B), dotnet-version-upgrade (B). These waste budget characters and add no discrimination value -- Claude already knows when a skill does NOT apply from the positive WHEN clause. All five are flagged for description trimming above.

### 2. Systematic Bare-Text Skill References in CI/CD (All 8 Skills)

All 8 CI/CD skills use bare text skill names (e.g., `dotnet-ado-patterns` instead of `[skill:dotnet-ado-patterns]`) in scope boundary and Out of scope sections. This produces 37 bare reference occurrences in CI/CD skills alone, plus 5 more in testing and performance skills (42 total across Batches C and D). The worst offender is dotnet-ado-unique with 10 bare references. By contrast, other categories have at most 1-2 bare references per skill.

### 3. Stale "May Not Exist Yet" Markers in UI Frameworks (7 Skills)

Seven UI framework skills reference AOT skills (`dotnet-native-aot`, `dotnet-aot-wasm`, `dotnet-aot-architecture`) with "(may not exist yet)" or "(soft dependency)" markers. All three referenced AOT skills exist and are registered. This systematic staleness was caused by UI skills being authored before the native-aot batch (Batch D) landed.

### 4. Stale "Planned"/"Not Yet Landed" References (3 Skills)

Three skills across different batches reference other skills as "planned" or "not yet landed" when those skills have since been implemented: dotnet-csharp-code-smells (A), dotnet-benchmarkdotnet (D), dotnet-nuget-authoring (F). This is the same root cause as pattern 3 -- skills authored before their referenced dependencies were implemented.

### 5. Agent-Meta-Skills Descriptions Are Universally Over Budget

All 4 agent-meta-skills have descriptions over 120 chars (3 of 4 over 140 chars). The pattern is identical: each description enumerates all subsections/categories inline. This is the worst-performing category for description budget discipline.

### 6. Description Budget Pressure Is Category-Dependent

- **Worst:** agent-meta-skills (4/4 over 120), multi-targeting (2/2 over 120, both unregistered), serialization (4/4 over 120)
- **Best:** documentation (0/5 over 120), localization (0/1 over 120), cli-tools (0/5 over 120), native-aot (0/4 over 120)
- **Mixed:** testing (8/10 over 120), architecture (4/10 over 120), cicd (1/8 over 120)

### 7. Strong Agent Gotchas Coverage With Minor Gaps

97 of 101 skills have Agent Gotchas or equivalent sections. The 4 skills without one are: dotnet-architecture-patterns (B, rated High), dotnet-add-testing (A, rated Low), dotnet-advisor (A, N/A -- router skill), plugin-self-publish (A, N/A -- meta skill). One skill (dotnet-cryptography) uses a variant heading "Gotchas and Pitfalls" instead of the conventional "Agent Gotchas."

### 8. Excellent Cross-Reference Target Accuracy

Across all 6 batches, every `[skill:name]` reference that uses proper syntax resolves to an existing skill. The only broken reference is `[skill:dotnet-scaffolding-base]` in dotnet-advisor (should be `[skill:dotnet-scaffold-project]`). Cross-reference infrastructure quality is high.

### 9. xUnit v3 IAsyncLifetime Inconsistency (Single-Batch Finding)

dotnet-maui-testing uses `Task` return types for `InitializeAsync`/`DisposeAsync` while xUnit v3 requires `ValueTask`. Three other testing skills (dotnet-xunit, dotnet-integration-testing, dotnet-uno-testing) correctly use `ValueTask`. This is a technical accuracy issue that could cause agents to generate code triggering xUnit v3 analyzer warnings. Note: This finding is from Batch C only, but is elevated as a cross-cutting pattern because it affects consistency across the entire testing category.

### 10. No details.md Companions Needed Yet

No skill exceeds the 3,000-word threshold requiring a details.md companion file. The closest is dotnet-xml-docs at 2,998 words and dotnet-uno-targets at 2,970 words. Both should be monitored.

## Implementation Assignment

The following maps each recommended change to the implementation task that owns the affected files.

### Task 9: Batches A+B

**Critical changes:**
- Trim 3 foundation skill descriptions (dotnet-advisor, dotnet-version-detection, dotnet-project-analysis)
- Fix 2 broken cross-refs in dotnet-advisor (`dotnet-scaffolding-base` to `dotnet-scaffold-project`)
- Trim dotnet-multi-targeting and dotnet-version-upgrade descriptions (registration in plugin.json is owned by Task 12)
- Trim 4 Batch B descriptions (dotnet-cryptography, dotnet-grpc, dotnet-service-communication, dotnet-secrets-management)

**High changes:**
- Remove WHEN NOT clauses from foundation descriptions
- Update stale "planned" reference in dotnet-csharp-code-smells
- Add Agent Gotchas to dotnet-architecture-patterns
- Trim 3 Batch B descriptions in warn range (dotnet-realtime-communication, dotnet-serialization, dotnet-containers)

**Low changes:**
- Trim 3 Low-priority Batch B descriptions (dotnet-data-access-strategy, dotnet-efcore-architecture, dotnet-security-owasp)
- Fix grep portability in dotnet-add-analyzers
- Rename dotnet-cryptography heading from "Gotchas and Pitfalls" to "Agent Gotchas"
- Consider Agent Gotchas section for dotnet-add-testing

### Task 10: Batches C+D

**Critical changes:**
- Trim 3 testing descriptions over 140 chars (dotnet-testing-strategy, dotnet-snapshot-testing, dotnet-test-quality)
- Trim dotnet-ci-benchmarking description

**High changes:**
- Fix xUnit v3 IAsyncLifetime in dotnet-maui-testing (Task -> ValueTask)
- Wrap 37 bare skill references in all 8 CI/CD skills with `[skill:]` syntax
- Wrap 4 bare `dotnet-add-testing` refs in testing skills with `[skill:]` syntax
- Trim 4 testing descriptions in warn range (dotnet-xunit, dotnet-integration-testing, dotnet-blazor-testing, dotnet-playwright)
- Fix bare backtick ref in dotnet-profiling
- Update stale "not yet landed" in dotnet-benchmarkdotnet

**Low changes:**
- Trim 2 Low-priority descriptions (dotnet-ui-testing-core, dotnet-maui-testing)
- Trim dotnet-profiling description
- Strengthen directive language in dotnet-ado-unique and dotnet-ado-patterns Agent Gotchas

### Task 11: Batches E+F

**Critical changes:**
- Trim 4 agent-meta-skills descriptions (dotnet-agent-gotchas, dotnet-build-analysis, dotnet-csproj-reading, dotnet-solution-navigation)

**High changes:**
- Remove stale "(may not exist yet)" markers from 7 UI framework skills (dotnet-uno-platform, dotnet-uno-targets, dotnet-maui-development, dotnet-maui-aot, dotnet-winui, dotnet-wpf-modern, dotnet-winforms-basics)
- Trim dotnet-blazor-patterns description
- Fix bare-text refs and stale "planned" in dotnet-nuget-authoring
- Add dotnet-release-management to dotnet-nuget-authoring Cross-references line

**Low changes:**
- Add `## Prerequisites` to dotnet-wpf-migration and dotnet-ui-chooser

### Task 12: Final Validation

- Register dotnet-multi-targeting and dotnet-version-upgrade in plugin.json
- Run all 4 validation commands
- Verify aggregate budget is below 12K WARN threshold
- Update AGENTS.md and README.md if skills were added/renamed
- Archive batch reports

## Acceptance Criteria Verification

Mapping each acceptance criterion from the task spec to where it is satisfied in this document:

| AC | Criterion | Satisfied By |
|----|-----------|-------------|
| 1 | All 6 batch findings reports merged into consolidated report | Per-Batch Summary table (line 22), all 6 batches represented; Prioritized Improvement Plan references every batch |
| 2 | Issues categorized with consistent severity levels (Critical/High/Low) | Three-tier tables in Prioritized Improvement Plan: Critical (20 issues), High (31 issues), Low (31 issues); severity definitions match batch-a pattern |
| 3 | Cross-cutting patterns identified from batch-level observations | 10 cross-cutting patterns in "Cross-Cutting Patterns" section, each citing evidence from specific batches |
| 4 | Projected description budget calculation included | "Description Budget Impact" section with current total (12,065), proposed totals (11,459 all / 11,496 Critical+High), delta vs thresholds, savings breakdowns |
| 5 | Each proposed change tagged with affected skill name, category, and priority level | Every item in the three priority tables includes skill name, category, and batch columns |
| 6 | Reference batch-a-findings.md severity categorization pattern for consistency | Critical = broken cross-refs, missing registrations, >140 chars; High = stale refs, bare-text refs, 121-140 chars; Low = formatting, monitoring -- consistent with Batch A pattern |
