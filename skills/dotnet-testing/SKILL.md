---
name: dotnet-testing
description: Defines .NET testing strategy and practices. Covers test architecture (unit vs integration vs E2E decision tree), xUnit v3 authoring, integration testing (WebApplicationFactory, Testcontainers, Aspire), snapshot testing (Verify), Playwright browser automation, BenchmarkDotNet microbenchmarks, CI benchmark gating, test quality metrics (Coverlet, Stryker.NET), UI testing core patterns, and test doubles patterns.
license: MIT
user-invocable: false
---

# dotnet-testing

## Overview

Testing strategy, frameworks, and quality tooling for .NET applications. This consolidated skill spans 12 topic areas. Load the appropriate companion file from `references/` based on the routing table below.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| Strategy | unit vs integration vs E2E, test doubles | references/testing-strategy.md |
| xUnit | Facts, Theories, fixtures, parallelism | references/xunit.md |
| Integration | WebApplicationFactory, Testcontainers, Aspire | references/integration-testing.md |
| Snapshot | Verify, scrubbing, API responses | references/snapshot-testing.md |
| Playwright | E2E browser, CI caching, trace viewer | references/playwright.md |
| BenchmarkDotNet | microbenchmarks, memory diagnosers | references/benchmarkdotnet.md |
| CI benchmarking | threshold alerts, baseline tracking | references/ci-benchmarking.md |
| Test quality | Coverlet, Stryker.NET, flaky tests | references/test-quality.md |
| Add testing | scaffold xUnit project, coverlet, layout | references/add-testing.md |
| Slopwatch | LLM reward hacking detection | references/slopwatch.md |
| AOT WASM | Blazor/Uno WASM AOT, size, lazy loading | references/aot-wasm.md |
| UI testing core | page objects, selectors, async waits | references/ui-testing-core.md |

## Scope

- Test strategy and architecture
- xUnit v3 test authoring
- Integration testing (WebApplicationFactory, Testcontainers)
- E2E browser testing (Playwright)
- Snapshot testing (Verify)
- Benchmarking (BenchmarkDotNet, CI gating)
- Quality (coverage, mutation testing)
- Cross-framework UI testing patterns
- Test scaffolding

## Out of scope

- UI framework-specific testing (bUnit, Appium) -> [skill:dotnet-ui]
- CI/CD pipeline configuration -> [skill:dotnet-devops]
- Performance profiling -> [skill:dotnet-tooling]

## Companion Files

- `references/testing-strategy.md` -- Unit vs integration vs E2E decision tree, test doubles selection
- `references/xunit.md` -- xUnit v3 Facts, Theories, fixtures, parallelism, IAsyncLifetime
- `references/integration-testing.md` -- WebApplicationFactory, Testcontainers, Aspire, database fixtures
- `references/snapshot-testing.md` -- Verify library, scrubbing, custom converters, HTTP response snapshots
- `references/playwright.md` -- Playwright E2E browser automation, CI caching, trace viewer, codegen
- `references/benchmarkdotnet.md` -- BenchmarkDotNet microbenchmarks, memory diagnosers, baselines
- `references/ci-benchmarking.md` -- CI benchmark regression detection, threshold alerts, baseline tracking
- `references/test-quality.md` -- Coverlet code coverage, Stryker.NET mutation testing, flaky tests
- `references/add-testing.md` -- Scaffold xUnit project, coverlet setup, directory layout
- `references/slopwatch.md` -- Slopwatch CLI for LLM reward hacking detection
- `references/aot-wasm.md` -- Blazor/Uno WASM AOT compilation, size vs speed, lazy loading, Brotli
- `references/ui-testing-core.md` -- Page object model, test selectors, async waits, accessibility testing
