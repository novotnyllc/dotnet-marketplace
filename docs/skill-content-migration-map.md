# Skill Content Migration Map

Content-preservation verification for the Skill Routing Language Hardening epic (fn-53).
Generated as part of T11 (Content-Preservation Verification).

## Summary

- **Total skills audited**: 130
- **Skills with description changes**: 128
- **Skills with section changes**: 130
- **Total sections dropped**: 6
- **Total sections added**: 263
- **Agents modified**: 12
- **Broken cross-references**: 0
- **Self-referential cross-links**: 0
- **Description budget**: 11,595 / 12,000 chars (OK)
- **Similarity WARN pairs**: 0 (no regression)
- **Similarity max score**: 0.5416 (below 0.55 WARN threshold)

## Section Migration Pattern

The normalization applied a consistent structural change across all 130 skills:

| Change | Count | Migration |
|--------|-------|-----------|
| `Scope` section added | 130 | New section -- skills had no explicit scope boundary |
| `Out of scope` section added | 130 | New section -- skills had no explicit out-of-scope boundary |
| `Overview / Scope Boundary` dropped | 5 | Split into separate `Scope` + `Out of scope` sections |
| `Scope Boundary` dropped | 1 | Split into separate `Scope` + `Out of scope` sections |
| `Activation Guidance` added | 1 | New section in dotnet-slopwatch |
| `Immediate Routing Actions (Do First)` added | 1 | New section in dotnet-advisor |
| `Default Quality Rule` added | 1 | New section in dotnet-advisor |

**Zero sections were dropped without a documented migration target.**
All 6 dropped sections (`Overview / Scope Boundary` x5, `Scope Boundary` x1) were split into dedicated `Scope` and `Out of scope` sections that preserve the original content.

## Description Changes

128 of 130 skills had their descriptions reworded to follow the canonical style guide:

- **Verb-led format**: Descriptions start with a present-tense verb (e.g., "Configures", "Implements", "Routes")
- **Budget-neutral or budget-negative**: Total description chars decreased from ~12,345 to 11,595
- **Factual tone**: Removed promotional/assertive cues ("WHEN", "WHEN NOT" prefixes)
- **Cross-reference syntax**: Routing targets use `[skill:name]` syntax in descriptions where applicable

## Advisor Catalog Status

All 20 category status markers in the `dotnet-advisor` skill catalog were verified and updated:

| Category | Previous Status | Current Status |
|----------|----------------|----------------|
| 1. Foundation & Plugin Infrastructure | `implemented` | `implemented` |
| 2. Core C# & Language Patterns | `planned` | `implemented` (updated) |
| 3. Project Structure & Scaffolding | `planned` | `implemented` (updated) |
| 4. Architecture Patterns | `planned` | `implemented` (updated) |
| 5. Serialization & Communication | `planned` | `implemented` (updated) |
| 6. API Development | `planned` | `implemented` (updated) |
| 7. Security | `planned` | `implemented` (updated) |
| 8. Testing | `planned` | `implemented` (updated) |
| 9. Performance & Benchmarking | `implemented` | `implemented` |
| 10. Native AOT & Trimming | `planned` | `implemented` (updated) |
| 11. CLI Tool Development | `(none)` | `implemented` (updated) |
| 12. UI Frameworks | `planned` | `implemented` (updated) |
| 13. Multi-Targeting & Polyfills | `planned` | `implemented` (updated) |
| 14. Localization & Internationalization | `implemented` | `implemented` |
| 15. Packaging & Publishing | `implemented` | `implemented` |
| 16. Release Management | `implemented` | `implemented` |
| 17. CI/CD | `implemented` | `implemented` |
| 18. Documentation | `implemented` | `implemented` |
| 19. Agent Meta-Skills | `planned` | `implemented` (updated) |
| 20. AI & LLM Integration | `(none)` | `implemented` (updated) |

## Agent Modifications

12 of 14 agent files were modified. 2 agents (dotnet-architect, dotnet-blazor-specialist) had no bare references to normalize.

| Agent | Description | Bare Refs | [skill:] Refs | Sections |
|-------|-------------|-----------|---------------|----------|
| dotnet-architect | unchanged | 0->0 | 7->7 | unchanged |
| dotnet-aspnetcore-specialist | reworded | 3->0 | 7->13 | unchanged |
| dotnet-async-performance-specialist | reworded | 3->0 | 5->10 | unchanged |
| dotnet-benchmark-designer | reworded | 1->0 | 6->7 | unchanged |
| dotnet-blazor-specialist | unchanged | 0->0 | 18->18 | unchanged |
| dotnet-cloud-specialist | reworded | 3->0 | 9->15 | unchanged |
| dotnet-code-review-agent | reworded | 9->0 | 7->16 | unchanged |
| dotnet-csharp-concurrency-specialist | reworded | 1->1 | 3->4 | unchanged |
| dotnet-docs-generator | reworded | 0->0 | 12->12 | unchanged |
| dotnet-maui-specialist | reworded | 0->0 | 17->17 | unchanged |
| dotnet-performance-analyst | reworded | 1->0 | 10->11 | unchanged |
| dotnet-security-reviewer | reworded | 0->0 | 7->7 | unchanged |
| dotnet-testing-specialist | reworded | 5->0 | 8->15 | unchanged |
| dotnet-uno-specialist | reworded | 0->0 | 19->19 | unchanged |

## Similarity Verification

| Metric | Pre-Sweep Baseline | Post-Sweep |
|--------|-------------------|------------|
| Total items | 144 | 144 |
| Total pairs | 10,296 | 10,296 |
| Max composite score | 0.5429 | 0.5416 |
| WARN pairs (>= 0.55) | 0 | 0 |
| ERROR pairs (>= 0.75) | 0 | 0 |
| Suppressed pairs | 1 | 1 |
| New WARNs vs baseline | n/a | 0 |

Max similarity score decreased slightly (0.5429 -> 0.5416), confirming descriptions were differentiated rather than homogenized.

## Validation Results

| Check | Result |
|-------|--------|
| `validate-skills.sh` | PASSED (0 errors, 10 warnings) |
| `validate-marketplace.sh` | PASSED (0 errors, 0 warnings) |
| Broken cross-references | 0 |
| Self-referential cross-links | 0 |
| ID collisions (skill vs agent) | 0 |
| Description budget | 11,595 < 12,000 (OK) |
| BUDGET_STATUS | OK |
| SELF_REF_COUNT | 0 |
| AGENT_BARE_REF_COUNT | 0 |
| AGENTSMD_BARE_REF_COUNT | 0 |

## Per-Category Skill Migration Detail

### foundation (4 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-advisor | reworded | none | Scope, Out of scope, Immediate Routing Actions (Do First), Default Quality Rule | 3/7 |
| dotnet-file-based-apps | reworded | none | Scope, Out of scope | 16/18 |
| dotnet-project-analysis | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-version-detection | reworded | none | Scope, Out of scope | 6/8 |

### core-csharp (18 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-channels | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-csharp-async-patterns | unchanged | none | Scope, Out of scope | 9/11 |
| dotnet-csharp-code-smells | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-csharp-coding-standards | reworded | none | Activation Guidance, Scope, Out of scope | 10/13 |
| dotnet-csharp-concurrency-patterns | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-csharp-configuration | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-csharp-dependency-injection | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-csharp-modern-patterns | unchanged | none | Scope, Out of scope | 16/18 |
| dotnet-csharp-nullable-reference-types | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-csharp-source-generators | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-csharp-type-design-performance | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-editorconfig | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-file-io | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-io-pipelines | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-linq-optimization | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-native-interop | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-roslyn-analyzers | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-validation-patterns | reworded | none | Scope, Out of scope | 11/13 |

### project-structure (7 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-add-analyzers | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-add-ci | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-add-testing | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-artifacts-output | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-modernize | reworded | none | Scope, Out of scope | 5/7 |
| dotnet-project-structure | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-scaffold-project | reworded | none | Scope, Out of scope | 12/14 |

### architecture (15 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-architecture-patterns | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-aspire-patterns | reworded | none | Scope, Out of scope | 13/15 |
| dotnet-background-services | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-container-deployment | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-containers | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-data-access-strategy | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-domain-modeling | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-efcore-architecture | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-efcore-patterns | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-http-client | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-messaging-patterns | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-observability | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-resilience | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-solid-principles | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-structured-logging | reworded | none | Scope, Out of scope | 7/9 |

### serialization (4 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-grpc | reworded | none | Scope, Out of scope | 15/17 |
| dotnet-realtime-communication | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-serialization | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-service-communication | reworded | none | Scope, Out of scope | 7/9 |

### api-development (9 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-api-security | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-api-surface-validation | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-api-versioning | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-csharp-api-design | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-input-validation | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-library-api-compat | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-middleware-patterns | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-minimal-apis | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-openapi | reworded | none | Scope, Out of scope | 10/12 |

### security (3 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-cryptography | reworded | Scope Boundary | Scope, Out of scope | 9/11 |
| dotnet-secrets-management | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-security-owasp | reworded | none | Scope, Out of scope | 14/16 |

### testing (10 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-blazor-testing | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-integration-testing | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-maui-testing | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-playwright | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-snapshot-testing | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-test-quality | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-testing-strategy | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-ui-testing-core | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-uno-testing | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-xunit | reworded | none | Scope, Out of scope | 10/12 |

### performance (5 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-benchmarkdotnet | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-ci-benchmarking | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-gc-memory | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-performance-patterns | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-profiling | reworded | none | Scope, Out of scope | 5/7 |

### native-aot (4 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-aot-architecture | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-aot-wasm | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-native-aot | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-trimming | reworded | none | Scope, Out of scope | 9/11 |

### cli-tools (6 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-cli-architecture | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-cli-distribution | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-cli-packaging | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-cli-release-pipeline | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-system-commandline | reworded | none | Scope, Out of scope | 17/19 |
| dotnet-tool-management | reworded | none | Scope, Out of scope | 9/11 |

### ui-frameworks (14 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-accessibility | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-blazor-auth | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-blazor-components | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-blazor-patterns | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-maui-aot | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-maui-development | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-ui-chooser | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-uno-mcp | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-uno-platform | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-uno-targets | reworded | none | Scope, Out of scope | 12/14 |
| dotnet-winforms-basics | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-winui | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-wpf-migration | reworded | none | Scope, Out of scope | 10/12 |
| dotnet-wpf-modern | reworded | none | Scope, Out of scope | 8/10 |

### multi-targeting (2 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-multi-targeting | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-version-upgrade | reworded | none | Scope, Out of scope | 9/11 |

### localization (1 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-localization | reworded | none | Scope, Out of scope | 8/10 |

### packaging (3 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-github-releases | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-msix | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-nuget-authoring | reworded | none | Scope, Out of scope | 9/11 |

### release-management (1 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-release-management | reworded | none | Scope, Out of scope | 10/12 |

### cicd (8 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-ado-build-test | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-ado-patterns | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-ado-publish | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-ado-unique | reworded | none | Scope, Out of scope | 8/10 |
| dotnet-gha-build-test | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-gha-deploy | reworded | none | Scope, Out of scope | 6/8 |
| dotnet-gha-patterns | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-gha-publish | reworded | none | Scope, Out of scope | 6/8 |

### documentation (5 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-api-docs | reworded | none | Scope, Out of scope | 11/13 |
| dotnet-documentation-strategy | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-github-docs | reworded | none | Scope, Out of scope | 26/28 |
| dotnet-mermaid-diagrams | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-xml-docs | reworded | none | Scope, Out of scope | 8/10 |

### agent-meta-skills (5 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-agent-gotchas | reworded | Overview / Scope Boundary | Scope, Out of scope | 13/15 |
| dotnet-build-analysis | reworded | Overview / Scope Boundary | Scope, Out of scope | 9/11 |
| dotnet-csproj-reading | reworded | Overview / Scope Boundary | Scope, Out of scope | 10/12 |
| dotnet-slopwatch | reworded | Overview / Scope Boundary | Scope, Out of scope | 10/12 |
| dotnet-solution-navigation | reworded | Overview / Scope Boundary | Scope, Out of scope | 9/11 |

### ai (1 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-semantic-kernel | reworded | none | Scope, Out of scope | 10/12 |

### build-system (3 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-build-optimization | reworded | none | Scope, Out of scope | 7/9 |
| dotnet-msbuild-authoring | reworded | none | Scope, Out of scope | 9/11 |
| dotnet-msbuild-tasks | reworded | none | Scope, Out of scope | 10/12 |

### tui (2 skills)

| Skill | Description | Sections Dropped | Sections Added | Sections Preserved |
|-------|-------------|-----------------|----------------|-------------------|
| dotnet-spectre-console | reworded | none | Scope, Out of scope | 13/15 |
| dotnet-terminal-gui | reworded | none | Scope, Out of scope | 14/16 |

