# fn-7-testing-foundation-skills.2 UI testing skills: core patterns, Blazor, MAUI, Uno, Playwright

## Description
Create five UI testing skills: the shared core patterns skill plus four framework-specific skills.

**Skills delivered:**
- `skills/testing/dotnet-ui-testing-core/SKILL.md` -- Core UI testing patterns: page object model, test selectors, async wait strategies, accessibility testing
- `skills/testing/dotnet-blazor-testing/SKILL.md` -- bUnit: component rendering, events, cascading parameters, JS interop mocking
- `skills/testing/dotnet-maui-testing/SKILL.md` -- Appium + XHarness: device/emulator testing, platform-specific behavior
- `skills/testing/dotnet-uno-testing/SKILL.md` -- Playwright for Uno WASM, platform-specific testing, runtime heads
- `skills/testing/dotnet-playwright/SKILL.md` -- Playwright for .NET: browser automation, E2E testing, CI caching, trace viewer, codegen

**File ownership:** This task exclusively owns `skills/testing/dotnet-ui-testing-core/`, `skills/testing/dotnet-blazor-testing/`, `skills/testing/dotnet-maui-testing/`, `skills/testing/dotnet-uno-testing/`, and `skills/testing/dotnet-playwright/`. This task does NOT modify `plugin.json` (Task 4 handles registration).

## Acceptance
- [ ] Five SKILL.md files created with required frontmatter (`name`, `description`)
- [ ] Each skill has: scope boundary, prerequisites, cross-references per matrix, >=2 code examples, gotchas section, references
- [ ] Core UI skill covers: page object model, test selectors, async wait strategies, accessibility testing
- [ ] Blazor testing covers bUnit rendering, events, cascading params, JS interop mocking
- [ ] MAUI testing covers Appium + XHarness with device/emulator patterns
- [ ] Uno testing covers Playwright for WASM, platform-specific heads
- [ ] Playwright skill covers CI caching (browser binary caching), trace viewer, codegen
- [ ] Version assumptions stated: Playwright 1.40+, .NET 8.0+ baseline
- [ ] Cross-references match the epic cross-reference matrix
- [ ] Skill content complete and ready for registration by Task 4

## Done summary
Created five UI testing skills: dotnet-ui-testing-core (page object model, selectors, wait strategies, accessibility), dotnet-blazor-testing (bUnit rendering, events, cascading params, JS interop), dotnet-maui-testing (Appium/XHarness device/emulator), dotnet-uno-testing (Playwright for WASM, runtime heads), and dotnet-playwright (browser automation, CI caching, trace viewer, codegen).
## Evidence
- Commits: baf7627, 60a27c1
- Tests: grep cross-reference matrix compliance, frontmatter validation, code example count verification
- PRs: