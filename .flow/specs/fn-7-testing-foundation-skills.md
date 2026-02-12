# fn-7: Testing Foundation Skills

## Overview
Delivers comprehensive testing foundation covering strategy, xUnit v3, integration testing, UI testing across frameworks (Blazor, MAUI, Uno), Playwright, snapshot testing, and test quality analysis.

## Scope Boundary
**In scope:** Testing design patterns, testing framework usage, test quality analysis, and testing strategy guidance.

**Out of scope / Owned by other skills:**
- Test project scaffolding (directory layout, xUnit project creation, coverlet setup, editorconfig overrides) -- owned by [skill:dotnet-add-testing]
- CI test reporting and pipeline integration -- owned by fn-19

The boundary is: `dotnet-add-testing` handles "how to create a test project"; fn-7 skills handle "how to write effective tests."

## Skills
Each skill lives at `skills/testing/<skill-name>/SKILL.md` (folder-per-skill convention).

- `dotnet-testing-strategy` -- Core testing patterns: unit vs integration vs E2E decision tree, test organization, naming conventions, when to use mocks vs fakes vs stubs
- `dotnet-xunit` -- xUnit v3 features: `[Fact]`/`[Theory]`, fixtures (`IClassFixture`, `ICollectionFixture`), parallel execution, `IAsyncLifetime`, custom assertions, analyzers; includes xUnit v2 compatibility notes
- `dotnet-integration-testing` -- WebApplicationFactory, Testcontainers, Aspire testing patterns, database fixtures, test isolation
- `dotnet-ui-testing-core` -- Core UI testing patterns applicable across frameworks: page object model, test selectors, async wait strategies, accessibility testing
- `dotnet-blazor-testing` -- bUnit for Blazor component testing: rendering, events, cascading parameters, JS interop mocking
- `dotnet-maui-testing` -- Appium + XHarness for MAUI testing: device/emulator testing, platform-specific behavior
- `dotnet-uno-testing` -- Playwright for Uno WASM, platform-specific testing, runtime heads
- `dotnet-playwright` -- Playwright for .NET: browser automation, E2E testing, CI caching, trace viewer, codegen
- `dotnet-snapshot-testing` -- Verify (VerifyTests): API surfaces, HTTP responses, rendered emails, scrubbing/filtering, custom converters
- `dotnet-test-quality` -- Code coverage (coverlet + ReportGenerator), CRAP analysis, mutation testing (Stryker.NET), flaky test detection

## Minimum Supported Versions
- xUnit: v3 primary, v2 compatibility notes where behavior differs
- .NET: 8.0+ (LTS baseline); note when features require 9.0+ or 10.0+
- Playwright: 1.40+ for .NET
- Testcontainers: 3.x+
- Verify: 20.x+

## Cross-Reference Matrix
Each skill MUST include outbound `[skill:...]` cross-references as follows:

| Skill | Required Outbound Refs |
|---|---|
| `dotnet-testing-strategy` | `dotnet-xunit`, `dotnet-integration-testing`, `dotnet-snapshot-testing`, `dotnet-test-quality`, `dotnet-add-testing` |
| `dotnet-xunit` | `dotnet-testing-strategy`, `dotnet-integration-testing` |
| `dotnet-integration-testing` | `dotnet-testing-strategy`, `dotnet-xunit`, `dotnet-snapshot-testing` |
| `dotnet-ui-testing-core` | `dotnet-testing-strategy`, `dotnet-playwright`, `dotnet-blazor-testing`, `dotnet-maui-testing`, `dotnet-uno-testing` |
| `dotnet-blazor-testing` | `dotnet-ui-testing-core`, `dotnet-xunit` |
| `dotnet-maui-testing` | `dotnet-ui-testing-core`, `dotnet-xunit` |
| `dotnet-uno-testing` | `dotnet-ui-testing-core`, `dotnet-playwright` |
| `dotnet-playwright` | `dotnet-ui-testing-core`, `dotnet-testing-strategy` |
| `dotnet-snapshot-testing` | `dotnet-testing-strategy`, `dotnet-integration-testing` |
| `dotnet-test-quality` | `dotnet-testing-strategy`, `dotnet-xunit` |

## fn-7 Reconciliation Scope
After all fn-7 skills land, replace ALL `<!-- TODO: fn-7 reconciliation -->` and `<!-- TODO(fn-7): ... -->` placeholders across the `skills/` directory with canonical `[skill:...]` cross-references. Affected skills span TWO categories:

**Architecture** (tracked in `skills/architecture/FN7-RECONCILIATION.md`):
`dotnet-architecture-patterns`, `dotnet-background-services`, `dotnet-resilience`, `dotnet-http-client`, `dotnet-observability`, `dotnet-efcore-patterns`, `dotnet-efcore-architecture`, `dotnet-data-access-strategy`, `dotnet-containers`, `dotnet-container-deployment`

**Serialization**:
`dotnet-serialization`, `dotnet-grpc`, `dotnet-service-communication`, `dotnet-realtime-communication`

Verification after reconciliation:
```bash
# Confirm no fn-7 TODOs remain in skills/
grep -rl "TODO.*fn-7\|fn-7.*TODO" skills/  # expect empty
```

## Quick Commands
```bash
# Smoke test: verify testing strategy skill exists
ls skills/testing/dotnet-testing-strategy/SKILL.md

# Validate xUnit v3 coverage
grep -i "xunit.*v3" skills/testing/dotnet-xunit/SKILL.md

# Test snapshot testing patterns
grep -i "Verify" skills/testing/dotnet-snapshot-testing/SKILL.md

# Verify all 10 skills registered in plugin.json
grep -c "skills/testing/" .claude-plugin/plugin.json  # expect 10

# Verify no fn-7 TODOs remain
grep -rl "TODO.*fn-7" skills/  # expect empty after reconciliation
```

## Acceptance Criteria
1. All 10 skills written at `skills/testing/<name>/SKILL.md` with required frontmatter (`name`, `description`)
2. Each skill has: description, scope boundary, prerequisites, cross-references, ≥2 practical code examples, gotchas/pitfalls section, references
3. Testing strategy skill provides decision tree for unit/integration/E2E with concrete criteria
4. xUnit skill covers v3 features with v2 compatibility notes where behavior differs
5. Integration testing skill documents WebApplicationFactory + Testcontainers + Aspire testing patterns
6. UI testing skills cover framework-specific patterns (bUnit, Appium, Playwright) with `dotnet-ui-testing-core` owning shared patterns
7. Snapshot testing skill uses Verify library with scrubbing/filtering and custom converter examples
8. Test quality skill covers coverage (coverlet + ReportGenerator), CRAP analysis, mutation testing (Stryker.NET)
9. Cross-references validated against the cross-reference matrix above (grep-based check)
10. All 10 skills registered in `.claude-plugin/plugin.json` skills array
11. All `TODO(fn-7)` and `TODO: fn-7 reconciliation` placeholders in `skills/` replaced with canonical `[skill:...]` refs
12. Updated `skills/architecture/FN7-RECONCILIATION.md` verification commands to include serialization scope

## Test Notes
- Validate xUnit skill theory and fixture examples compile conceptually
- Verify Playwright skill includes CI caching patterns (browser binary caching)
- Check snapshot testing skill covers scrubbing/filtering patterns for dates, GUIDs
- Confirm cross-reference matrix compliance with grep
- Confirm no overlap with `dotnet-add-testing` (scaffolding) -- fn-7 skills reference it, not duplicate it

## References
- xUnit Documentation: https://xunit.net/
- WebApplicationFactory: https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests
- Testcontainers: https://dotnet.testcontainers.org/
- Playwright for .NET: https://playwright.dev/dotnet/
- Verify: https://github.com/VerifyTests/Verify
- Coverlet: https://github.com/coverlet-coverage/coverlet
- Stryker.NET: https://stryker-mutator.io/docs/stryker-net/introduction/
