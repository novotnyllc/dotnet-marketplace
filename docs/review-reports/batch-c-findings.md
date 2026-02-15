# Batch C Findings: Testing, CI/CD

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | 18 |
| Clean | 1 |
| Needs Work | 14 |
| Critical | 3 |
| Total issues | 23 |
| Critical issues | 3 |
| High issues | 12 |
| Low issues | 8 |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | 2,251 |
| Skills over 120 chars | 11 |
| Projected savings if all trimmed to 120 | 321 chars |

Skills over 120 chars: dotnet-snapshot-testing (152), dotnet-test-quality (149), dotnet-testing-strategy (144), dotnet-playwright (138), dotnet-xunit (133), dotnet-integration-testing (130), dotnet-blazor-testing (129), dotnet-ui-testing-core (126), dotnet-maui-testing (126), dotnet-ado-unique (121), dotnet-gha-deploy (113 -- under limit but included for completeness).

Over-140 fail threshold: dotnet-snapshot-testing (152), dotnet-test-quality (149), dotnet-testing-strategy (144).

Character counts measured using the canonical Python parser (strips YAML quotes, trims whitespace).

## Findings by Skill

### testing

### dotnet-testing-strategy

**Category:** testing
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 144 chars (>140 = fail) -- over 120-char limit; lists too many concerns (organization, naming, mock/fake/stub) |
| 2 | Description Triggering | pass | Good trigger phrases: "how to test", "unit vs integration", "test organization", "naming conventions" |
| 3 | Instruction Clarity | pass | Clear decision tree for unit vs integration vs E2E; actionable coverage thresholds |
| 4 | Progressive Disclosure | pass | 1,698 words -- well under threshold |
| 5 | Cross-References | pass | 15 cross-refs, all resolve correctly; proper [skill:] syntax throughout |
| 6 | Error Handling | pass | Agent Gotchas section with 5 items and 5 strong directives (Do not) |
| 7 | Examples | pass | Concrete naming conventions, test structure examples |
| 8 | Composability | pass | Clear out-of-scope markers with attribution to owning skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | Registered but 144 chars pushes aggregate budget |
| 11 | Progressive Disclosure Compliance | pass | 1,698 words |

**Issues:**
- [Critical] Description at 144 chars exceeds 140-char fail threshold -- trim by removing "mock/fake/stub guidance" and condensing
- [Low] Description could focus on the decision tree aspect which is its primary value

**Proposed description (118 chars):** `"WHEN deciding how to test .NET code. Unit vs integration vs E2E decision tree, test organization, naming conventions."`

---

### dotnet-xunit

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 133 chars (121-140 = warn) -- slightly over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "xUnit", "Fact", "Theory", "fixtures", "IAsyncLifetime" |
| 3 | Instruction Clarity | pass | Clear v2 vs v3 migration notes; concrete fixture patterns |
| 4 | Progressive Disclosure | pass | 1,979 words |
| 5 | Cross-References | pass | 7 cross-refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas with 5 items and 5 strong directives (Do not); covers key v3 migration pitfalls |
| 7 | Examples | pass | Real C# examples with xUnit v3 patterns; correct ValueTask usage for IAsyncLifetime |
| 8 | Composability | pass | Clear scope boundary and out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 133 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,979 words |

**Issues:**
- [High] Description at 133 chars exceeds 120-char target -- trim by condensing parenthetical list

**Proposed description (119 chars):** `"WHEN writing tests with xUnit. v3 Fact/Theory, fixtures, parallelism, IAsyncLifetime, analyzers, v2 compatibility."`

---

### dotnet-integration-testing

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 130 chars (121-140 = warn) -- over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "WebApplicationFactory", "Testcontainers", "Aspire testing", "integration test" |
| 3 | Instruction Clarity | pass | Concrete patterns for WAF, Testcontainers, and Aspire; clear isolation strategies |
| 4 | Progressive Disclosure | pass | 1,977 words |
| 5 | Cross-References | pass | 9 cross-refs, all resolve; proper [skill:] syntax |
| 6 | Error Handling | pass | Agent Gotchas with 6 items and 7 strong directives (6 Do not, 1 Always); covers port conflicts, service registration |
| 7 | Examples | pass | Complete WAF and Testcontainers examples with correct ValueTask for IAsyncLifetime |
| 8 | Composability | pass | Clear scope boundary separating from unit and E2E testing |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 130 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,977 words |

**Issues:**
- [High] Description at 130 chars exceeds 120-char target -- trim by condensing

**Proposed description (119 chars):** `"WHEN testing with real infrastructure. WebApplicationFactory, Testcontainers, Aspire testing, database fixtures."`

---

### dotnet-ui-testing-core

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 126 chars (121-140 = warn) -- slightly over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "UI testing", "page object model", "selectors", "accessibility testing" |
| 3 | Instruction Clarity | pass | Clear POM patterns, selector strategies, and wait patterns |
| 4 | Progressive Disclosure | pass | 1,557 words |
| 5 | Cross-References | pass | 12 cross-refs; all resolve; comprehensive routing to framework-specific skills |
| 6 | Error Handling | pass | Agent Gotchas with 5 items and 5 strong directives (Do not) |
| 7 | Examples | pass | Concrete POM examples with proper async patterns |
| 8 | Composability | pass | Excellent hub design -- routes to blazor-testing, maui-testing, uno-testing, playwright |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 126 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,557 words |

**Issues:**
- [Low] Description at 126 chars exceeds 120-char target -- minor trim needed

**Proposed description (118 chars):** `"WHEN testing UI across frameworks. Page object model, test selectors, async wait strategies, accessibility testing."`

---

### dotnet-blazor-testing

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 129 chars (121-140 = warn) -- over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "Blazor", "bUnit", "component testing", "JS interop mocking" |
| 3 | Instruction Clarity | pass | Clear bUnit rendering patterns, event handling, cascading parameters |
| 4 | Progressive Disclosure | pass | 1,333 words |
| 5 | Cross-References | pass | 9 cross-refs, all resolve; links to playwright for E2E and ui-testing-core for shared patterns |
| 6 | Error Handling | pass | Agent Gotchas with 5 items and 5 strong directives (Do not) |
| 7 | Examples | pass | Real bUnit code examples; covers component lifecycle testing |
| 8 | Composability | pass | Clear scope boundary between bUnit (unit) and Playwright (E2E) |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 129 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,333 words |

**Issues:**
- [High] Description at 129 chars exceeds 120-char target -- trim by condensing parenthetical

**Proposed description (118 chars):** `"WHEN testing Blazor components. bUnit rendering, events, cascading parameters, JS interop mocking, lifecycle testing."`

---

### dotnet-maui-testing

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 126 chars (121-140 = warn) -- over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "MAUI testing", "Appium", "XHarness", "device testing" |
| 3 | Instruction Clarity | pass | Clear Appium setup and XHarness execution patterns |
| 4 | Progressive Disclosure | pass | 1,374 words |
| 5 | Cross-References | pass | 9 cross-refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas with 5 items and 6 strong directives (5 Do not, 1 Always) |
| 7 | Examples | warn | AppiumFixture.InitializeAsync and DisposeAsync return `Task` (lines 37, 74) but xUnit v3 requires `ValueTask` -- inconsistent with dotnet-xunit and dotnet-integration-testing which correctly use `ValueTask` |
| 8 | Composability | pass | Clear scope boundary and out-of-scope markers |
| 9 | Consistency | warn | IAsyncLifetime return type inconsistency vs category peers (dotnet-xunit, dotnet-integration-testing, dotnet-uno-testing all use ValueTask) |
| 10 | Registration & Budget | warn | 126 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,374 words |

**Issues:**
- [High] AppiumFixture uses `async Task InitializeAsync()` and `async Task DisposeAsync()` (lines 37, 74) but xUnit v3 IAsyncLifetime requires `ValueTask` return types -- dotnet-xunit explicitly documents this change and all other testing peers use `ValueTask`
- [High] Description at 126 chars exceeds 120-char target -- trim needed

**Proposed description (117 chars):** `"WHEN testing .NET MAUI apps. Appium device/emulator testing, XHarness test execution, platform-specific validation."`

---

### dotnet-uno-testing

**Category:** testing
**Overall:** Clean

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 115 chars -- under 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "Uno testing", "Playwright", "WASM testing", "runtime head" |
| 3 | Instruction Clarity | pass | Clear Playwright WASM patterns and platform-specific test strategies |
| 4 | Progressive Disclosure | pass | 1,426 words |
| 5 | Cross-References | pass | 8 cross-refs, all resolve; proper routing to ui-testing-core and playwright |
| 6 | Error Handling | pass | Agent Gotchas with 5 items and 6 strong directives (5 Do not, 1 Always) |
| 7 | Examples | pass | Correct ValueTask for IAsyncLifetime; concrete Playwright patterns for Uno WASM |
| 8 | Composability | pass | Clear scope boundary and out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure; consistent IAsyncLifetime usage |
| 10 | Registration & Budget | pass | 115 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,426 words |

**Issues:**
(none)

---

### dotnet-playwright

**Category:** testing
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 138 chars (121-140 = warn) -- over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "Playwright", "browser tests", "E2E", "trace viewer", "codegen" |
| 3 | Instruction Clarity | pass | Clear setup, test patterns, CI caching, and debugging guidance |
| 4 | Progressive Disclosure | pass | 1,824 words |
| 5 | Cross-References | pass | 7 cross-refs, all resolve |
| 6 | Error Handling | pass | Agent Gotchas with 6 items and 6 strong directives (Do not) |
| 7 | Examples | pass | Concrete Playwright patterns with proper async/await |
| 8 | Composability | pass | Good scope boundary separating from framework-specific testing skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 138 chars pushes budget |
| 11 | Progressive Disclosure Compliance | pass | 1,824 words |

**Issues:**
- [High] Description at 138 chars exceeds 120-char target -- trim by removing "codegen for test scaffolding"

**Proposed description (116 chars):** `"WHEN automating browser tests in .NET. Playwright E2E testing, CI browser caching, trace viewer debugging patterns."`

---

### dotnet-snapshot-testing

**Category:** testing
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 152 chars (>140 = fail) -- significantly over limit; lists too many detail items |
| 2 | Description Triggering | pass | Good triggers: "Verify", "snapshot testing", "API surfaces", "scrubbing" |
| 3 | Instruction Clarity | pass | Clear Verify patterns with scrubbing and custom converters |
| 4 | Progressive Disclosure | pass | 1,695 words |
| 5 | Cross-References | warn | 4 proper [skill:] refs resolve, but 2 bare `dotnet-add-testing` references in Out of scope and Prerequisites sections (lines 12, 14) |
| 6 | Error Handling | pass | Agent Gotchas with 6 items and 8 strong directives (6 Do not, 2 Always) |
| 7 | Examples | pass | Concrete Verify examples with scrubbing patterns |
| 8 | Composability | pass | Clear out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 152 chars severely impacts aggregate budget |
| 11 | Progressive Disclosure Compliance | pass | 1,695 words |

**Issues:**
- [Critical] Description at 152 chars exceeds 140-char fail threshold -- trim by removing "scrubbing/filtering for dates and GUIDs, custom converters"
- [High] Two bare `dotnet-add-testing` references (lines 12, 14) should use `[skill:dotnet-add-testing]` syntax

**Proposed description (120 chars):** `"WHEN verifying complex outputs with Verify. API surfaces, HTTP responses, rendered emails, scrubbing for determinism."`

---

### dotnet-test-quality

**Category:** testing
**Overall:** Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | fail | 149 chars (>140 = fail) -- over limit; lists too many tool names |
| 2 | Description Triggering | pass | Good triggers: "code coverage", "CRAP analysis", "mutation testing", "flaky test" |
| 3 | Instruction Clarity | pass | Clear coverage, CRAP, mutation testing, and flaky test patterns |
| 4 | Progressive Disclosure | pass | 2,343 words -- approaching 3,000-word suggestion threshold |
| 5 | Cross-References | warn | 7 proper [skill:] refs resolve, but 2 bare `dotnet-add-testing` references in Out of scope and Prerequisites (lines 12, 14) |
| 6 | Error Handling | pass | Agent Gotchas with 6 items and 8 strong directives (7 Do not, 1 Always) |
| 7 | Examples | pass | Concrete coverage and CRAP analysis examples |
| 8 | Composability | pass | Clear out-of-scope markers and scope boundary |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | warn | 149 chars severely impacts aggregate budget |
| 11 | Progressive Disclosure Compliance | pass | 2,343 words -- monitor for growth |

**Issues:**
- [Critical] Description at 149 chars exceeds 140-char fail threshold -- trim by condensing tool list
- [High] Two bare `dotnet-add-testing` references (lines 12, 14) should use `[skill:dotnet-add-testing]` syntax

**Proposed description (119 chars):** `"WHEN measuring test effectiveness. Code coverage with coverlet, CRAP analysis, mutation testing, flaky test detection."`

---

### cicd

### dotnet-gha-patterns

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars -- under 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "GitHub Actions", "reusable workflows", "composite actions", "matrix builds" |
| 3 | Instruction Clarity | pass | Clear workflow composition patterns, caching strategies, matrix builds |
| 4 | Progressive Disclosure | pass | 1,727 words |
| 5 | Cross-References | warn | 9 proper [skill:] refs resolve, but 4 bare skill name references in Out of scope section (dotnet-ado-patterns, dotnet-gha-build-test, dotnet-gha-publish, dotnet-gha-deploy) |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 2 strong directives (Do not) |
| 7 | Examples | pass | Complete YAML workflow examples |
| 8 | Composability | pass | Clear out-of-scope markers with attribution |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 116 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,727 words |

**Issues:**
- [High] 4 bare skill name references in Out of scope section should use `[skill:]` syntax: `dotnet-ado-patterns`, `dotnet-gha-build-test`, `dotnet-gha-publish`, `dotnet-gha-deploy`

---

### dotnet-gha-build-test

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 112 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "setup-dotnet", "NuGet caching", "test reporting", "GitHub Actions build" |
| 3 | Instruction Clarity | pass | Clear build and test pipeline patterns with coverage reporting |
| 4 | Progressive Disclosure | pass | 1,458 words |
| 5 | Cross-References | warn | 9 proper [skill:] refs resolve, but 4 bare skill name references in scope boundary and Out of scope (dotnet-gha-patterns, dotnet-gha-publish, dotnet-gha-deploy, dotnet-ado-build-test) |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 3 strong directives (1 Always, 1 Do not, 1 Never) |
| 7 | Examples | pass | Complete YAML workflow examples with test reporting |
| 8 | Composability | pass | Clear scope boundary separating from peer CI/CD skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 112 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,458 words |

**Issues:**
- [High] 4 bare skill name references should use `[skill:]` syntax: `dotnet-gha-patterns`, `dotnet-gha-publish`, `dotnet-gha-deploy`, `dotnet-ado-build-test`

---

### dotnet-gha-publish

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "NuGet push", "container images", "signing", "SBOM", "GitHub Actions publish" |
| 3 | Instruction Clarity | pass | Clear artifact publishing patterns with signing and SBOM generation |
| 4 | Progressive Disclosure | pass | 1,538 words |
| 5 | Cross-References | warn | 17 proper [skill:] refs resolve, but 2 bare skill name references in Out of scope (dotnet-ado-publish, dotnet-gha-deploy) |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 2 strong directives (1 Always, 1 Never) |
| 7 | Examples | pass | Complete YAML publish workflow examples |
| 8 | Composability | pass | Clear out-of-scope markers with attribution |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 116 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,538 words |

**Issues:**
- [Low] 2 bare skill name references in Out of scope should use `[skill:]` syntax: `dotnet-ado-publish`, `dotnet-gha-deploy`

---

### dotnet-gha-deploy

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 113 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "deploy", "Azure Web Apps", "GitHub Pages", "container registries", "environments" |
| 3 | Instruction Clarity | pass | Clear deployment patterns for multiple targets |
| 4 | Progressive Disclosure | pass | 1,787 words |
| 5 | Cross-References | warn | 11 proper [skill:] refs resolve, but 3 bare skill name references in scope boundary and Out of scope (dotnet-gha-publish, dotnet-gha-patterns, dotnet-ado-patterns) |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 3 strong directives (1 Always, 2 Never) |
| 7 | Examples | pass | Complete deployment workflow examples |
| 8 | Composability | pass | Clear scope boundary and out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 113 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,787 words |

**Issues:**
- [Low] 3 bare skill name references should use `[skill:]` syntax: `dotnet-gha-publish`, `dotnet-gha-patterns`, `dotnet-ado-patterns`

---

### dotnet-ado-patterns

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 107 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "Azure DevOps", "YAML pipelines", "templates", "variable groups", "multi-stage" |
| 3 | Instruction Clarity | pass | Clear template patterns, variable groups, and multi-stage pipeline guidance |
| 4 | Progressive Disclosure | pass | 1,890 words |
| 5 | Cross-References | warn | 6 proper [skill:] refs resolve, but 5 bare skill name references in scope boundary and Out of scope (dotnet-ado-unique, dotnet-ado-build-test, dotnet-ado-publish, dotnet-gha-patterns) plus 1 additional bare ref at line 292 |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 0 strong directives -- informational style rather than imperative |
| 7 | Examples | pass | Complete YAML pipeline template examples |
| 8 | Composability | pass | Clear scope boundary and out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 107 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,890 words |

**Issues:**
- [High] 6 bare skill name references should use `[skill:]` syntax: `dotnet-ado-unique` (x2, lines 12 and 14), `dotnet-ado-build-test`, `dotnet-ado-publish`, `dotnet-gha-patterns`, plus bare ref at line 292

---

### dotnet-ado-build-test

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 116 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "Azure DevOps build", "DotNetCoreCLI", "Azure Artifacts", "test results" |
| 3 | Instruction Clarity | pass | Clear build and test task patterns with coverage reporting |
| 4 | Progressive Disclosure | pass | 1,565 words |
| 5 | Cross-References | warn | 9 proper [skill:] refs resolve, but 4 bare skill name references in scope boundary and Out of scope (dotnet-ado-patterns, dotnet-ado-publish, dotnet-ado-unique, dotnet-gha-build-test) |
| 6 | Error Handling | pass | Agent Gotchas with 9 items and 1 strong directive (Never) |
| 7 | Examples | pass | Complete YAML pipeline task examples |
| 8 | Composability | pass | Clear scope boundary separating from peer ADO skills |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 116 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,565 words |

**Issues:**
- [Low] 4 bare skill name references should use `[skill:]` syntax: `dotnet-ado-patterns`, `dotnet-ado-publish`, `dotnet-ado-unique`, `dotnet-gha-build-test`

---

### dotnet-ado-publish

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass | 108 chars -- under limit |
| 2 | Description Triggering | pass | Good triggers: "Azure DevOps publish", "NuGet push", "container images", "ACR" |
| 3 | Instruction Clarity | pass | Clear artifact publishing patterns for ADO pipelines |
| 4 | Progressive Disclosure | pass | 1,529 words |
| 5 | Cross-References | warn | 17 proper [skill:] refs resolve, but 2 bare skill name references in Out of scope (dotnet-gha-publish, dotnet-ado-unique) |
| 6 | Error Handling | pass | Agent Gotchas with 8 items and 1 strong directive (Never) |
| 7 | Examples | pass | Complete YAML pipeline task examples |
| 8 | Composability | pass | Clear out-of-scope markers |
| 9 | Consistency | pass | Matches category peer structure |
| 10 | Registration & Budget | pass | 108 chars |
| 11 | Progressive Disclosure Compliance | pass | 1,529 words |

**Issues:**
- [Low] 2 bare skill name references should use `[skill:]` syntax: `dotnet-gha-publish`, `dotnet-ado-unique`

---

### dotnet-ado-unique

**Category:** cicd
**Overall:** Needs Work

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | warn | 121 chars (121-140 = warn) -- 1 char over 120-char limit |
| 2 | Description Triggering | pass | Good triggers: "environments", "approvals", "service connections", "classic releases", "variable groups" |
| 3 | Instruction Clarity | pass | Clear ADO-exclusive feature patterns |
| 4 | Progressive Disclosure | pass | 2,325 words -- approaching but under threshold |
| 5 | Cross-References | warn | 5 proper [skill:] refs resolve, but 10 bare skill name references across scope boundary and Out of scope (dotnet-ado-patterns, dotnet-ado-build-test, dotnet-ado-publish, dotnet-gha-patterns, dotnet-gha-build-test, dotnet-gha-publish, dotnet-gha-deploy) -- worst offender in the batch |
| 6 | Error Handling | pass | Agent Gotchas with 8 items but 0 strong directives -- informational style; weakest gotchas section in batch |
| 7 | Examples | pass | Complete YAML examples for ADO-exclusive features |
| 8 | Composability | pass | Clear scope boundary separating ADO-exclusive from shared ADO skills |
| 9 | Consistency | warn | Agent Gotchas section has 0 strong directives (DO NOT/NEVER/ALWAYS) while 6 of 7 CI/CD peers have 1-3 each (dotnet-ado-patterns also has 0); weakens actionability |
| 10 | Registration & Budget | warn | 121 chars marginally over limit |
| 11 | Progressive Disclosure Compliance | pass | 2,325 words |

**Issues:**
- [High] 10 bare skill name references should use `[skill:]` syntax -- most systematic cross-reference issue in the batch: `dotnet-ado-patterns` (x2), `dotnet-ado-build-test` (x2), `dotnet-ado-publish` (x2), `dotnet-gha-patterns`, `dotnet-gha-build-test`, `dotnet-gha-publish`, `dotnet-gha-deploy`
- [Low] Description at 121 chars is 1 char over 120-char target -- trim "with" from "Environments with approvals"
- [Low] Agent Gotchas section lacks strong directives (0 DO NOT/NEVER/ALWAYS) while 6 of 7 CI/CD peers have 1-3 each (dotnet-ado-patterns also has 0)

**Proposed description (120 chars):** `"WHEN using ADO-exclusive features. Environments, approvals, service connections, classic releases, variable groups."`

---

## Cross-Cutting Observations

1. **Bare skill name references are systematic in CI/CD skills:** All 8 CI/CD skills use bare text skill names (e.g., `dotnet-ado-patterns` instead of `[skill:dotnet-ado-patterns]`) in their scope boundary and Out of scope sections. This is a systematic pattern producing 39 bare references across the category. The worst offender is `dotnet-ado-unique` with 10 bare references. By contrast, the testing category has only 4 bare references across 2 skills. This is the highest-priority cross-cutting fix.

2. **Testing description budget pressure is severe:** 8 of 10 testing skills (80%) exceed the 120-char target. Three exceed the 140-char fail threshold (dotnet-snapshot-testing at 152, dotnet-test-quality at 149, dotnet-testing-strategy at 144). The CI/CD category is much healthier with only 1 of 8 skills slightly over (dotnet-ado-unique at 121). Trimming all testing descriptions to 120 chars would save approximately 261 chars from the aggregate budget.

3. **xUnit v3 IAsyncLifetime inconsistency in dotnet-maui-testing:** The `dotnet-maui-testing` AppiumFixture uses `async Task InitializeAsync()` and `async Task DisposeAsync()` while `dotnet-xunit` explicitly documents that xUnit v3 changed IAsyncLifetime to return `ValueTask`. Three other testing skills (`dotnet-integration-testing`, `dotnet-uno-testing`, `dotnet-xunit`) correctly use `ValueTask`. This is a technical accuracy issue that could cause agents to generate code that triggers xUnit v3 analyzer warnings.

4. **Agent Gotchas coverage is strong but directive style varies:** All 18 skills have Agent Gotchas sections. Testing skills have 5-6 items each with 5-8 strong directives (predominantly "Do not" imperatives). CI/CD skills have 8-9 items each -- more items than testing -- but use fewer strong directives: GHA skills average 2-3 (Always/Never/Do not), while ADO skills average 0-1. Two outliers (`dotnet-ado-patterns` and `dotnet-ado-unique`) have 0 strong directives, using purely informational phrasing instead of imperative DO NOT/NEVER/ALWAYS directives.

5. **All cross-reference targets resolve correctly:** All 146 `[skill:]` references across the 18 skills point to existing registered skills. No broken references. This is consistent with the Batch B finding of excellent cross-reference target accuracy.

6. **No details.md companions needed:** All 18 skills are under the 3,000-word threshold. The highest is `dotnet-test-quality` at 2,343 words and `dotnet-ado-unique` at 2,325 words. Both are approaching but not yet at the suggestion threshold.

7. **Testing category has more severe issues than CI/CD:** 3 of 10 testing skills are Critical (all due to description length >140 chars), while 0 of 8 CI/CD skills are Critical. However, all 8 CI/CD skills are Needs Work due to the systematic bare cross-reference pattern in scope boundary and Out of scope sections.

8. **CI/CD skills demonstrate excellent description discipline but universal cross-ref issues:** 7 of 8 CI/CD skills are under 120 chars (the sole exception is dotnet-ado-unique at 121). This contrasts sharply with the testing category where only 1 of 10 (dotnet-uno-testing at 115) passes the description quality check cleanly. However, every CI/CD skill has bare skill name references, making the only Clean skill in the entire batch `dotnet-uno-testing`.

9. **Section structure is consistent within and across categories:** All 18 skills follow the same inline-scope pattern (scope boundary and Out of scope on dedicated lines) rather than separate ## Scope sections. This is a convention choice and is internally consistent.

## Recommended Changes

### Critical (must fix)
- Trim `dotnet-snapshot-testing` description from 152 to under 120 chars -- remove "scrubbing/filtering for dates and GUIDs, custom converters"
- Trim `dotnet-test-quality` description from 149 to under 120 chars -- condense tool list
- Trim `dotnet-testing-strategy` description from 144 to under 120 chars -- remove "mock/fake/stub guidance"

### High (should fix)
- Fix `dotnet-maui-testing` AppiumFixture to use `ValueTask` return types for `InitializeAsync` and `DisposeAsync` -- consistent with xUnit v3 and all testing category peers
- Wrap all 39 bare skill name references in CI/CD skills with `[skill:]` syntax -- systematic issue across all 8 skills
- Wrap 4 bare `dotnet-add-testing` references in `dotnet-snapshot-testing` and `dotnet-test-quality` with `[skill:]` syntax
- Trim `dotnet-xunit` description from 133 to under 120 chars
- Trim `dotnet-integration-testing` description from 130 to under 120 chars
- Trim `dotnet-blazor-testing` description from 129 to under 120 chars
- Trim `dotnet-playwright` description from 138 to under 120 chars

### Low (nice to have)
- Trim `dotnet-ui-testing-core` description from 126 to under 120 chars
- Trim `dotnet-maui-testing` description from 126 to under 120 chars
- Trim `dotnet-ado-unique` description from 121 to under 120 chars (1 char over)
- Add strong directives (DO NOT/NEVER/ALWAYS) to `dotnet-ado-unique` and `dotnet-ado-patterns` Agent Gotchas sections for consistency with category peers
- Monitor `dotnet-test-quality` (2,343 words) and `dotnet-ado-unique` (2,325 words) for details.md extraction if content grows
