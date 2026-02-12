# fn-7: Testing Foundation Skills

## Overview
Delivers comprehensive testing foundation covering strategy, xUnit v3, integration testing, UI testing across frameworks (Blazor, MAUI, Uno), Playwright, snapshot testing, and test quality analysis.

## Scope
**Skills:**
- `dotnet-testing-strategy` - Core testing patterns: unit vs integration vs E2E, when to use what, test organization
- `dotnet-xunit` - Comprehensive xUnit: v3 features, theories, fixtures, parallelism, custom assertions, analyzers
- `dotnet-integration-testing` - WebApplicationFactory, Testcontainers, Aspire testing patterns
- `dotnet-ui-testing-core` - Core UI testing patterns applicable across frameworks
- `dotnet-blazor-testing` - bUnit for Blazor component testing
- `dotnet-maui-testing` - Appium, XHarness for MAUI testing
- `dotnet-uno-testing` - Playwright for Uno WASM, platform-specific testing
- `dotnet-playwright` - Playwright for .NET: browser automation, E2E testing, CI caching
- `dotnet-snapshot-testing` - Verify for snapshot testing: API surfaces, HTTP responses, rendered emails
- `dotnet-test-quality` - Code coverage (coverlet), CRAP analysis, mutation testing (Stryker.NET)

## Key Context
- xUnit v3 is the modern testing standard for .NET
- WebApplicationFactory for in-memory ASP.NET Core testing
- Testcontainers for integration testing with real dependencies
- Playwright is the recommended E2E testing tool
- Verify (VerifyTests) is the standard snapshot testing library
- Skills must reference dotnet-skills testing patterns: https://github.com/Aaronontheweb/dotnet-skills

## Quick Commands
```bash
# Smoke test: verify testing strategy skill exists
fd -e md dotnet-testing-strategy skills/

# Validate xUnit v3 coverage
grep -i "xunit.*v3" skills/testing/dotnet-xunit.md

# Test snapshot testing patterns
grep -i "Verify" skills/testing/dotnet-snapshot-testing.md
```

## Acceptance Criteria
1. All 10 skills written with standard depth and frontmatter
2. Testing strategy skill provides decision tree for unit/integration/E2E
3. xUnit skill covers v3 features, theories, fixtures, parallel execution
4. Integration testing skill documents WebApplicationFactory + Testcontainers patterns
5. UI testing skills cover framework-specific patterns (bUnit, Appium, Playwright)
6. Snapshot testing skill uses Verify library with practical examples
7. Test quality skill covers coverage (coverlet), CRAP analysis, mutation testing
8. Skills cross-reference each other (e.g., integration-testing references testcontainers)

## Test Notes
- Test xUnit skill by validating theory and fixture examples
- Verify Playwright skill includes CI caching patterns
- Check that snapshot testing skill covers scrubbing/filtering patterns

## References
- xUnit Documentation: https://xunit.net/
- WebApplicationFactory: https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-10.0
- Testcontainers: https://dotnet.testcontainers.org/
- Playwright for .NET: https://playwright.dev/dotnet/
- Verify: https://github.com/VerifyTests/Verify
- dotnet-skills testing reference: https://github.com/Aaronontheweb/dotnet-skills
