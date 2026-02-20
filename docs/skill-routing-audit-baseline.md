# Skill Routing Audit Baseline

Generated for fn-53-skill-routing-language-hardening.1 (T1).

## Summary Statistics

- **Total skills**: 130
- **Total agents**: 14
- **Total description chars**: 12,345
- **Total cross-references ([skill:] syntax)**: 1,735 occurrences (not deduplicated; counts every `[skill:...]` match in skill bodies)
- **Skills without ANY routing markers**: 58
- **Agent bare-text references**: 64 across 14 agents
- **Routing test cases**: 14

## Budget Status

- Current description chars: 12,345
- WARN threshold: 12,000
- FAIL threshold: 15,600
- Status: **WARN** (at 12,345 chars, above 12,000 WARN threshold)

## Routing Marker Coverage

Routing markers are headings that help the model determine when to use a skill:
- **Scope / Scope Boundary**: Defines what the skill covers
- **Out-of-scope**: Defines what the skill does NOT cover
- **Trigger / Prerequisites**: Signals when to load this skill

| Marker | Count | Coverage |
|--------|-------|----------|
| Scope section | 24 | 18% |
| Out-of-scope section | 0 | 0% |
| Trigger/Prerequisites | 58 | 44% |
| Zero markers | 58 | 44% |

### Skills with Zero Routing Markers

- `api-development/dotnet-middleware-patterns`
- `architecture/dotnet-architecture-patterns`
- `architecture/dotnet-background-services`
- `architecture/dotnet-container-deployment`
- `architecture/dotnet-data-access-strategy`
- `architecture/dotnet-efcore-architecture`
- `architecture/dotnet-efcore-patterns`
- `architecture/dotnet-http-client`
- `architecture/dotnet-messaging-patterns`
- `architecture/dotnet-observability`
- `architecture/dotnet-resilience`
- `architecture/dotnet-solid-principles`
- `architecture/dotnet-structured-logging`
- `build-system/dotnet-build-optimization`
- `build-system/dotnet-msbuild-authoring`
- `build-system/dotnet-msbuild-tasks`
- `cicd/dotnet-ado-build-test`
- `cicd/dotnet-ado-patterns`
- `cicd/dotnet-ado-publish`
- `cicd/dotnet-gha-build-test`
- `cicd/dotnet-gha-deploy`
- `cicd/dotnet-gha-patterns`
- `cicd/dotnet-gha-publish`
- `cli-tools/dotnet-cli-architecture`
- `cli-tools/dotnet-cli-distribution`
- `cli-tools/dotnet-cli-packaging`
- `cli-tools/dotnet-cli-release-pipeline`
- `cli-tools/dotnet-system-commandline`
- `cli-tools/dotnet-tool-management`
- `core-csharp/dotnet-channels`
- `core-csharp/dotnet-csharp-async-patterns`
- `core-csharp/dotnet-csharp-code-smells`
- `core-csharp/dotnet-csharp-coding-standards`
- `core-csharp/dotnet-csharp-configuration`
- `core-csharp/dotnet-csharp-dependency-injection`
- `core-csharp/dotnet-csharp-nullable-reference-types`
- `core-csharp/dotnet-csharp-source-generators`
- `core-csharp/dotnet-io-pipelines`
- `documentation/dotnet-api-docs`
- `documentation/dotnet-documentation-strategy`
- `documentation/dotnet-mermaid-diagrams`
- `documentation/dotnet-xml-docs`
- `foundation/dotnet-advisor`
- `foundation/dotnet-version-detection`
- `native-aot/dotnet-aot-architecture`
- `native-aot/dotnet-trimming`
- `packaging/dotnet-github-releases`
- `packaging/dotnet-msix`
- `packaging/dotnet-nuget-authoring`
- `performance/dotnet-benchmarkdotnet`
- `performance/dotnet-ci-benchmarking`
- `performance/dotnet-profiling`
- `release-management/dotnet-release-management`
- `serialization/dotnet-grpc`
- `serialization/dotnet-serialization`
- `serialization/dotnet-service-communication`
- `ui-frameworks/dotnet-ui-chooser`
- `ui-frameworks/dotnet-wpf-migration`

## Per-Skill Audit

| Skill | Category | Desc Len | Refs (occurrences) | Scope | OOS | Trigger | Top-3 Overlap (Jaccard) |
|-------|----------|----------|--------------------|-------|-----|---------|------------------------|
| dotnet-agent-gotchas | agent-meta-skills | 92 | 28 | Y | - | Y | dotnet-csharp-async-patterns (0.2222); dotnet-csharp-code-smells (0.2105); dotnet-csharp-coding-standards (0.2000) |
| dotnet-build-analysis | agent-meta-skills | 93 | 10 | Y | - | Y | dotnet-artifacts-output (0.0952); dotnet-solid-principles (0.0909); dotnet-agent-gotchas (0.0870) |
| dotnet-csproj-reading | agent-meta-skills | 93 | 10 | Y | - | Y | dotnet-project-analysis (0.2222); dotnet-nuget-authoring (0.1500); dotnet-msbuild-authoring (0.1364) |
| dotnet-slopwatch | agent-meta-skills | 116 | 6 | Y | - | Y | dotnet-version-detection (0.0645); dotnet-add-testing (0.0417); dotnet-blazor-auth (0.0400) |
| dotnet-solution-navigation | agent-meta-skills | 88 | 11 | Y | - | Y | dotnet-project-analysis (0.1000); dotnet-scaffold-project (0.1000); dotnet-project-structure (0.0952) |
| dotnet-semantic-kernel | ai | 98 | 9 | - | - | Y | dotnet-benchmarkdotnet (0.1000); dotnet-ado-unique (0.0500); dotnet-ado-patterns (0.0455) |
| dotnet-api-security | api-development | 98 | 11 | - | - | Y | dotnet-blazor-auth (0.1000); dotnet-api-surface-validation (0.0455); dotnet-grpc (0.0455) |
| dotnet-api-surface-validation | api-development | 95 | 18 | - | - | Y | dotnet-playwright (0.1000); dotnet-snapshot-testing (0.1000); dotnet-ado-build-test (0.0526) |
| dotnet-api-versioning | api-development | 89 | 5 | - | - | Y | dotnet-http-client (0.1111); dotnet-minimal-apis (0.0909); dotnet-input-validation (0.0588) |
| dotnet-csharp-api-design | api-development | 103 | 14 | Y | - | Y | dotnet-http-client (0.0556); dotnet-middleware-patterns (0.0556); dotnet-csharp-nullable-reference-types (0.0526) |
| dotnet-input-validation | api-development | 88 | 17 | - | - | Y | dotnet-validation-patterns (0.0714); dotnet-http-client (0.0667); dotnet-api-versioning (0.0588) |
| dotnet-library-api-compat | api-development | 94 | 14 | Y | - | Y | dotnet-csharp-source-generators (0.0588); dotnet-localization (0.0556); dotnet-release-management (0.0556) |
| dotnet-middleware-patterns | api-development | 87 | 6 | - | - | - | dotnet-architecture-patterns (0.1579); dotnet-grpc (0.1111); dotnet-minimal-apis (0.1000) |
| dotnet-minimal-apis | api-development | 113 | 12 | - | - | Y | dotnet-grpc (0.1429); dotnet-architecture-patterns (0.1304); dotnet-middleware-patterns (0.1000) |
| dotnet-openapi | api-development | 87 | 5 | - | - | Y | dotnet-api-docs (0.1765); dotnet-documentation-strategy (0.0625); dotnet-csharp-dependency-injection (0.0556) |
| dotnet-architecture-patterns | architecture | 105 | 14 | - | - | - | dotnet-middleware-patterns (0.1579); dotnet-minimal-apis (0.1304); dotnet-grpc (0.0909) |
| dotnet-aspire-patterns | architecture | 98 | 12 | Y | - | Y | dotnet-observability (0.1333); dotnet-integration-testing (0.0625); dotnet-ado-unique (0.0588) |
| dotnet-background-services | architecture | 94 | 10 | - | - | - | dotnet-release-management (0.0714); dotnet-blazor-components (0.0625); dotnet-efcore-patterns (0.0625) |
| dotnet-container-deployment | architecture | 94 | 16 | - | - | - | dotnet-artifacts-output (0.1053); dotnet-add-ci (0.0909); dotnet-gha-deploy (0.0526) |
| dotnet-containers | architecture | 93 | 12 | Y | - | - | dotnet-ado-patterns (0.1176); dotnet-nuget-authoring (0.1176); dotnet-roslyn-analyzers (0.0667) |
| dotnet-data-access-strategy | architecture | 101 | 11 | - | - | - | dotnet-service-communication (0.2000); dotnet-efcore-patterns (0.0952); dotnet-csharp-type-design-performance (0.0909) |
| dotnet-domain-modeling | architecture | 95 | 17 | Y | - | - | dotnet-validation-patterns (0.0556); dotnet-blazor-patterns (0.0526); dotnet-spectre-console (0.0500) |
| dotnet-efcore-architecture | architecture | 90 | 12 | - | - | - | dotnet-mermaid-diagrams (0.0588); dotnet-serialization (0.0476); dotnet-architecture-patterns (0.0455) |
| dotnet-efcore-patterns | architecture | 118 | 11 | - | - | - | dotnet-data-access-strategy (0.0952); dotnet-background-services (0.0625); dotnet-release-management (0.0588) |
| dotnet-http-client | architecture | 93 | 11 | - | - | - | dotnet-api-versioning (0.1111); dotnet-resilience (0.1053); dotnet-input-validation (0.0667) |
| dotnet-messaging-patterns | architecture | 93 | 8 | - | - | - | dotnet-accessibility (0.0000); dotnet-add-analyzers (0.0000); dotnet-add-ci (0.0000) |
| dotnet-observability | architecture | 87 | 10 | - | - | - | dotnet-aspire-patterns (0.1333); dotnet-msbuild-tasks (0.0667); dotnet-build-optimization (0.0588) |
| dotnet-resilience | architecture | 96 | 9 | - | - | - | dotnet-http-client (0.1053); dotnet-input-validation (0.0556); dotnet-openapi (0.0526) |
| dotnet-solid-principles | architecture | 91 | 8 | - | - | - | dotnet-csharp-code-smells (0.1000); dotnet-csharp-dependency-injection (0.1000); dotnet-csharp-coding-standards (0.0952) |
| dotnet-structured-logging | architecture | 95 | 8 | - | - | - | dotnet-linq-optimization (0.0556); dotnet-ado-patterns (0.0526); dotnet-snapshot-testing (0.0526) |
| dotnet-build-optimization | build-system | 86 | 12 | - | - | - | dotnet-tool-management (0.1176); dotnet-msbuild-authoring (0.0952); dotnet-gha-patterns (0.0588) |
| dotnet-msbuild-authoring | build-system | 116 | 5 | - | - | - | dotnet-version-detection (0.2000); dotnet-project-structure (0.1429); dotnet-csproj-reading (0.1364) |
| dotnet-msbuild-tasks | build-system | 89 | 3 | - | - | - | dotnet-msbuild-authoring (0.1053); dotnet-observability (0.0667); dotnet-system-commandline (0.0556) |
| dotnet-ado-build-test | cicd | 89 | 13 | - | - | - | dotnet-ado-publish (0.1765); dotnet-ado-patterns (0.1111); dotnet-add-ci (0.1000) |
| dotnet-ado-patterns | cicd | 100 | 12 | - | - | - | dotnet-add-ci (0.1429); dotnet-containers (0.1176); dotnet-ado-build-test (0.1111) |
| dotnet-ado-publish | cicd | 95 | 19 | - | - | - | dotnet-gha-publish (0.2941); dotnet-ado-build-test (0.1765); dotnet-add-ci (0.1429) |
| dotnet-ado-unique | cicd | 93 | 15 | Y | - | - | dotnet-github-releases (0.0625); dotnet-aspire-patterns (0.0588); dotnet-cli-release-pipeline (0.0526) |
| dotnet-gha-build-test | cicd | 119 | 14 | - | - | - | dotnet-gha-patterns (0.1667); dotnet-cli-release-pipeline (0.1429); dotnet-gha-publish (0.1429) |
| dotnet-gha-deploy | cicd | 87 | 15 | - | - | - | dotnet-gha-publish (0.2500); dotnet-add-ci (0.1579); dotnet-gha-patterns (0.1333) |
| dotnet-gha-patterns | cicd | 98 | 13 | - | - | - | dotnet-cli-release-pipeline (0.1875); dotnet-gha-build-test (0.1667); dotnet-gha-deploy (0.1333) |
| dotnet-gha-publish | cicd | 91 | 19 | - | - | - | dotnet-ado-publish (0.2941); dotnet-gha-deploy (0.2500); dotnet-gha-build-test (0.1429) |
| dotnet-cli-architecture | cli-tools | 96 | 13 | - | - | - | dotnet-ado-unique (0.0476); dotnet-aspire-patterns (0.0476); dotnet-cli-release-pipeline (0.0435) |
| dotnet-cli-distribution | cli-tools | 93 | 22 | - | - | - | dotnet-cli-release-pipeline (0.0952); dotnet-file-based-apps (0.0952); dotnet-service-communication (0.0952) |
| dotnet-cli-packaging | cli-tools | 87 | 12 | - | - | - | dotnet-ado-publish (0.1000); dotnet-add-testing (0.0526); dotnet-tool-management (0.0526) |
| dotnet-cli-release-pipeline | cli-tools | 88 | 13 | - | - | - | dotnet-gha-patterns (0.1875); dotnet-gha-build-test (0.1429); dotnet-github-releases (0.1176) |
| dotnet-system-commandline | cli-tools | 112 | 12 | - | - | - | dotnet-csharp-configuration (0.1000); dotnet-file-based-apps (0.1000); dotnet-msbuild-authoring (0.0909) |
| dotnet-tool-management | cli-tools | 86 | 8 | - | - | - | dotnet-build-optimization (0.1176); dotnet-roslyn-analyzers (0.0625); dotnet-validation-patterns (0.0625) |
| dotnet-channels | core-csharp | 91 | 4 | - | - | - | dotnet-validation-patterns (0.0625); dotnet-csharp-configuration (0.0526); dotnet-io-pipelines (0.0526) |
| dotnet-csharp-async-patterns | core-csharp | 97 | 4 | - | - | - | dotnet-agent-gotchas (0.2222); dotnet-csharp-code-smells (0.1667); dotnet-csharp-nullable-reference-types (0.1111) |
| dotnet-csharp-code-smells | core-csharp | 89 | 8 | - | - | - | dotnet-agent-gotchas (0.2105); dotnet-csharp-async-patterns (0.1667); dotnet-csharp-nullable-reference-types (0.1053) |
| dotnet-csharp-coding-standards | core-csharp | 105 | 5 | - | - | - | dotnet-agent-gotchas (0.2000); dotnet-advisor (0.1364); dotnet-csharp-code-smells (0.0952) |
| dotnet-csharp-concurrency-patterns | core-csharp | 106 | 8 | - | - | Y | dotnet-artifacts-output (0.0556); dotnet-benchmarkdotnet (0.0556); dotnet-csharp-async-patterns (0.0556) |
| dotnet-csharp-configuration | core-csharp | 89 | 2 | - | - | - | dotnet-validation-patterns (0.1875); dotnet-secrets-management (0.1765); dotnet-system-commandline (0.1000) |
| dotnet-csharp-dependency-injection | core-csharp | 98 | 3 | - | - | - | dotnet-solid-principles (0.1000); dotnet-agent-gotchas (0.0952); dotnet-integration-testing (0.0556) |
| dotnet-csharp-modern-patterns | core-csharp | 95 | 5 | Y | - | - | dotnet-version-detection (0.0800); dotnet-uno-platform (0.0526); dotnet-csharp-code-smells (0.0500) |
| dotnet-csharp-nullable-reference-types | core-csharp | 92 | 2 | - | - | - | dotnet-agent-gotchas (0.1579); dotnet-csharp-async-patterns (0.1111); dotnet-csharp-code-smells (0.1053) |
| dotnet-csharp-source-generators | core-csharp | 97 | 3 | - | - | - | dotnet-localization (0.1538); dotnet-aot-architecture (0.1333); dotnet-nuget-authoring (0.1250) |
| dotnet-csharp-type-design-performance | core-csharp | 109 | 9 | - | - | Y | dotnet-performance-patterns (0.1765); dotnet-gc-memory (0.0952); dotnet-data-access-strategy (0.0909) |
| dotnet-editorconfig | core-csharp | 100 | 11 | Y | - | - | dotnet-msbuild-authoring (0.0909); dotnet-modernize (0.0588); dotnet-roslyn-analyzers (0.0556) |
| dotnet-file-io | core-csharp | 85 | 14 | Y | - | - | dotnet-io-pipelines (0.1111); dotnet-documentation-strategy (0.0588); dotnet-file-based-apps (0.0526) |
| dotnet-io-pipelines | core-csharp | 95 | 6 | - | - | - | dotnet-file-io (0.1111); dotnet-channels (0.0526); dotnet-winforms-basics (0.0500) |
| dotnet-linq-optimization | core-csharp | 97 | 9 | Y | - | - | dotnet-performance-patterns (0.1176); dotnet-structured-logging (0.0556); dotnet-csharp-type-design-performance (0.0500) |
| dotnet-native-interop | core-csharp | 93 | 11 | - | - | Y | dotnet-native-aot (0.1579); dotnet-maui-testing (0.0556); dotnet-uno-testing (0.0556) |
| dotnet-roslyn-analyzers | core-csharp | 96 | 7 | Y | - | - | dotnet-containers (0.0667); dotnet-tool-management (0.0625); dotnet-scaffold-project (0.0588) |
| dotnet-validation-patterns | core-csharp | 88 | 11 | - | - | Y | dotnet-csharp-configuration (0.1875); dotnet-input-validation (0.0714); dotnet-blazor-patterns (0.0625) |
| dotnet-api-docs | documentation | 90 | 25 | - | - | - | dotnet-openapi (0.1765); dotnet-documentation-strategy (0.1053); dotnet-agent-gotchas (0.0909) |
| dotnet-documentation-strategy | documentation | 92 | 15 | - | - | - | dotnet-api-docs (0.1053); dotnet-testing-strategy (0.1053); dotnet-ui-chooser (0.1000) |
| dotnet-github-docs | documentation | 92 | 25 | - | - | Y | dotnet-add-ci (0.0909); dotnet-gha-patterns (0.0556); dotnet-github-releases (0.0556) |
| dotnet-mermaid-diagrams | documentation | 94 | 9 | - | - | - | dotnet-efcore-architecture (0.0588); dotnet-csharp-type-design-performance (0.0556); dotnet-architecture-patterns (0.0500) |
| dotnet-xml-docs | documentation | 91 | 9 | - | - | - | dotnet-api-docs (0.0526); dotnet-accessibility (0.0000); dotnet-add-analyzers (0.0000) |
| dotnet-advisor | foundation | 89 | 226 | - | - | - | dotnet-version-detection (0.1538); dotnet-csharp-coding-standards (0.1364); dotnet-csharp-async-patterns (0.0952) |
| dotnet-file-based-apps | foundation | 85 | 6 | - | - | Y | dotnet-add-testing (0.1111); dotnet-scaffold-project (0.1053); dotnet-system-commandline (0.1000) |
| dotnet-project-analysis | foundation | 87 | 5 | - | - | Y | dotnet-csproj-reading (0.2222); dotnet-project-structure (0.1667); dotnet-secrets-management (0.1176) |
| dotnet-version-detection | foundation | 99 | 6 | - | - | - | dotnet-msbuild-authoring (0.2000); dotnet-advisor (0.1538); dotnet-nuget-authoring (0.1200) |
| dotnet-localization | localization | 95 | 17 | Y | - | - | dotnet-csharp-source-generators (0.1538); dotnet-nuget-authoring (0.1176); dotnet-serialization (0.1111) |
| dotnet-multi-targeting | multi-targeting | 87 | 7 | - | - | Y | dotnet-solid-principles (0.0952); dotnet-wpf-modern (0.0952); dotnet-csharp-coding-standards (0.0909) |
| dotnet-version-upgrade | multi-targeting | 86 | 8 | - | - | Y | dotnet-add-testing (0.1053); dotnet-add-analyzers (0.0909); dotnet-add-ci (0.0870) |
| dotnet-aot-architecture | native-aot | 92 | 17 | - | - | - | dotnet-serialization (0.1579); dotnet-csharp-source-generators (0.1333); dotnet-localization (0.0588) |
| dotnet-aot-wasm | native-aot | 88 | 14 | Y | - | - | dotnet-uno-testing (0.1111); dotnet-native-aot (0.0952); dotnet-cli-distribution (0.0909) |
| dotnet-native-aot | native-aot | 95 | 21 | Y | - | - | dotnet-native-interop (0.1579); dotnet-maui-aot (0.1429); dotnet-ado-publish (0.1000) |
| dotnet-trimming | native-aot | 109 | 11 | - | - | - | dotnet-security-owasp (0.1429); dotnet-native-aot (0.0952); dotnet-csharp-concurrency-patterns (0.0500) |
| dotnet-github-releases | packaging | 91 | 16 | - | - | - | dotnet-release-management (0.1429); dotnet-cli-release-pipeline (0.1176); dotnet-gha-patterns (0.0667) |
| dotnet-msix | packaging | 94 | 18 | - | - | - | dotnet-winui (0.1000); dotnet-github-releases (0.0556); dotnet-gha-publish (0.0476) |
| dotnet-nuget-authoring | packaging | 90 | 20 | - | - | - | dotnet-csproj-reading (0.1500); dotnet-csharp-source-generators (0.1250); dotnet-version-detection (0.1200) |
| dotnet-benchmarkdotnet | performance | 117 | 18 | - | - | - | dotnet-gc-memory (0.1000); dotnet-security-owasp (0.1000); dotnet-semantic-kernel (0.1000) |
| dotnet-ci-benchmarking | performance | 92 | 12 | - | - | - | dotnet-artifacts-output (0.1000); dotnet-winforms-basics (0.0476); dotnet-api-surface-validation (0.0455) |
| dotnet-gc-memory | performance | 99 | 12 | Y | - | - | dotnet-performance-patterns (0.1053); dotnet-benchmarkdotnet (0.1000); dotnet-csharp-type-design-performance (0.0952) |
| dotnet-performance-patterns | performance | 88 | 19 | Y | - | - | dotnet-csharp-type-design-performance (0.1765); dotnet-linq-optimization (0.1176); dotnet-gc-memory (0.1053) |
| dotnet-profiling | performance | 93 | 14 | - | - | - | dotnet-build-optimization (0.0588); dotnet-csharp-code-smells (0.0556); dotnet-csharp-type-design-performance (0.0556) |
| dotnet-add-analyzers | project-structure | 97 | 6 | - | - | Y | dotnet-add-testing (0.1667); dotnet-scaffold-project (0.1579); dotnet-add-ci (0.1364) |
| dotnet-add-ci | project-structure | 93 | 6 | - | - | Y | dotnet-add-testing (0.1579); dotnet-gha-deploy (0.1579); dotnet-ado-patterns (0.1429) |
| dotnet-add-testing | project-structure | 88 | 17 | - | - | Y | dotnet-add-analyzers (0.1667); dotnet-add-ci (0.1579); dotnet-scaffold-project (0.1176) |
| dotnet-artifacts-output | project-structure | 90 | 8 | - | - | Y | dotnet-container-deployment (0.1053); dotnet-ci-benchmarking (0.1000); dotnet-build-analysis (0.0952) |
| dotnet-modernize | project-structure | 95 | 17 | - | - | Y | dotnet-agent-gotchas (0.1176); dotnet-csharp-async-patterns (0.0625); dotnet-winforms-basics (0.0625) |
| dotnet-project-structure | project-structure | 93 | 5 | - | - | Y | dotnet-scaffold-project (0.2353); dotnet-project-analysis (0.1667); dotnet-msbuild-authoring (0.1429) |
| dotnet-scaffold-project | project-structure | 94 | 6 | - | - | Y | dotnet-project-structure (0.2353); dotnet-add-analyzers (0.1579); dotnet-add-testing (0.1176) |
| dotnet-release-management | release-management | 93 | 13 | - | - | - | dotnet-github-releases (0.1429); dotnet-background-services (0.0714); dotnet-blazor-components (0.0588) |
| dotnet-cryptography | security | 93 | 9 | Y | - | Y | dotnet-validation-patterns (0.0526); dotnet-secrets-management (0.0500); dotnet-tool-management (0.0500) |
| dotnet-secrets-management | security | 91 | 6 | - | - | Y | dotnet-csharp-configuration (0.1765); dotnet-project-analysis (0.1176); dotnet-validation-patterns (0.0625) |
| dotnet-security-owasp | security | 118 | 11 | - | - | Y | dotnet-trimming (0.1429); dotnet-benchmarkdotnet (0.1000); dotnet-csharp-configuration (0.0952) |
| dotnet-grpc | serialization | 87 | 14 | - | - | - | dotnet-minimal-apis (0.1429); dotnet-middleware-patterns (0.1111); dotnet-realtime-communication (0.1000) |
| dotnet-realtime-communication | serialization | 96 | 13 | Y | - | - | dotnet-service-communication (0.1579); dotnet-grpc (0.1000); dotnet-integration-testing (0.0556) |
| dotnet-serialization | serialization | 100 | 12 | - | - | - | dotnet-aot-architecture (0.1579); dotnet-csharp-source-generators (0.1176); dotnet-localization (0.1111) |
| dotnet-service-communication | serialization | 92 | 24 | - | - | - | dotnet-data-access-strategy (0.2000); dotnet-realtime-communication (0.1579); dotnet-wpf-migration (0.1000) |
| dotnet-blazor-testing | testing | 89 | 9 | - | - | Y | dotnet-blazor-components (0.1667); dotnet-blazor-patterns (0.1111); dotnet-integration-testing (0.0556) |
| dotnet-integration-testing | testing | 90 | 9 | - | - | Y | dotnet-xunit (0.1176); dotnet-maui-testing (0.0667); dotnet-uno-testing (0.0667) |
| dotnet-maui-testing | testing | 86 | 9 | - | - | Y | dotnet-uno-testing (0.1429); dotnet-accessibility (0.1333); dotnet-maui-development (0.1333) |
| dotnet-playwright | testing | 92 | 7 | - | - | Y | dotnet-api-surface-validation (0.1000); dotnet-gha-patterns (0.0556); dotnet-profiling (0.0556) |
| dotnet-snapshot-testing | testing | 89 | 6 | - | - | Y | dotnet-api-surface-validation (0.1000); dotnet-integration-testing (0.0556); dotnet-structured-logging (0.0526) |
| dotnet-test-quality | testing | 100 | 9 | - | - | Y | dotnet-add-testing (0.1111); dotnet-ui-testing-core (0.1000); dotnet-testing-strategy (0.0952) |
| dotnet-testing-strategy | testing | 87 | 15 | - | - | Y | dotnet-add-testing (0.1053); dotnet-documentation-strategy (0.1053); dotnet-service-communication (0.0952) |
| dotnet-ui-testing-core | testing | 87 | 12 | - | - | Y | dotnet-accessibility (0.1111); dotnet-test-quality (0.1000); dotnet-ui-chooser (0.0909) |
| dotnet-uno-testing | testing | 90 | 8 | - | - | Y | dotnet-uno-targets (0.1765); dotnet-maui-testing (0.1429); dotnet-accessibility (0.1333) |
| dotnet-xunit | testing | 106 | 7 | - | - | Y | dotnet-integration-testing (0.1176); dotnet-roslyn-analyzers (0.0556); dotnet-add-testing (0.0526) |
| dotnet-spectre-console | tui | 95 | 12 | - | - | Y | dotnet-artifacts-output (0.0526); dotnet-domain-modeling (0.0500); dotnet-cli-distribution (0.0476) |
| dotnet-terminal-gui | tui | 99 | 11 | - | - | Y | dotnet-add-testing (0.0476); dotnet-artifacts-output (0.0455); dotnet-project-structure (0.0435) |
| dotnet-accessibility | ui-frameworks | 98 | 19 | - | - | Y | dotnet-maui-testing (0.1333); dotnet-uno-testing (0.1333); dotnet-blazor-auth (0.1176) |
| dotnet-blazor-auth | ui-frameworks | 97 | 13 | - | - | Y | dotnet-accessibility (0.1176); dotnet-api-security (0.1000); dotnet-ui-chooser (0.0952) |
| dotnet-blazor-components | ui-frameworks | 109 | 13 | - | - | Y | dotnet-blazor-testing (0.1667); dotnet-background-services (0.0625); dotnet-github-releases (0.0588) |
| dotnet-blazor-patterns | ui-frameworks | 92 | 13 | - | - | Y | dotnet-blazor-testing (0.1111); dotnet-validation-patterns (0.0625); dotnet-blazor-auth (0.0556) |
| dotnet-maui-aot | ui-frameworks | 98 | 12 | - | - | Y | dotnet-native-aot (0.1429); dotnet-add-analyzers (0.0870); dotnet-aot-wasm (0.0870) |
| dotnet-maui-development | ui-frameworks | 90 | 14 | - | - | Y | dotnet-maui-testing (0.1333); dotnet-uno-testing (0.0625); dotnet-accessibility (0.0588) |
| dotnet-ui-chooser | ui-frameworks | 92 | 15 | - | - | - | dotnet-wpf-migration (0.2632); dotnet-documentation-strategy (0.1000); dotnet-blazor-auth (0.0952) |
| dotnet-uno-mcp | ui-frameworks | 97 | 30 | - | - | Y | dotnet-add-ci (0.0833); dotnet-uno-testing (0.0500); dotnet-uno-platform (0.0455) |
| dotnet-uno-platform | ui-frameworks | 92 | 14 | - | - | Y | dotnet-uno-testing (0.1250); dotnet-uno-targets (0.1000); dotnet-maui-testing (0.0588) |
| dotnet-uno-targets | ui-frameworks | 95 | 11 | - | - | Y | dotnet-uno-testing (0.1765); dotnet-accessibility (0.1053); dotnet-uno-platform (0.1000) |
| dotnet-winforms-basics | ui-frameworks | 98 | 13 | Y | - | Y | dotnet-modernize (0.0625); dotnet-aot-architecture (0.0526); dotnet-artifacts-output (0.0526) |
| dotnet-winui | ui-frameworks | 99 | 14 | - | - | Y | dotnet-file-based-apps (0.1000); dotnet-msix (0.1000); dotnet-wpf-migration (0.1000) |
| dotnet-wpf-migration | ui-frameworks | 100 | 24 | - | - | - | dotnet-ui-chooser (0.2632); dotnet-service-communication (0.1000); dotnet-winui (0.1000) |
| dotnet-wpf-modern | ui-frameworks | 99 | 12 | - | - | Y | dotnet-multi-targeting (0.0952); dotnet-profiling (0.0556); dotnet-maui-development (0.0526) |

## Top Overlap Hotspots (by Jaccard)

Top 30 most similar description pairs by set Jaccard (stopword-stripped):

| Rank | Skill A | Skill B | Jaccard |
|------|---------|---------|---------|
| 1 | dotnet-ado-publish | dotnet-gha-publish | 0.2941 |
| 2 | dotnet-ui-chooser | dotnet-wpf-migration | 0.2632 |
| 3 | dotnet-gha-deploy | dotnet-gha-publish | 0.2500 |
| 4 | dotnet-project-structure | dotnet-scaffold-project | 0.2353 |
| 5 | dotnet-agent-gotchas | dotnet-csharp-async-patterns | 0.2222 |
| 6 | dotnet-csproj-reading | dotnet-project-analysis | 0.2222 |
| 7 | dotnet-agent-gotchas | dotnet-csharp-code-smells | 0.2105 |
| 8 | dotnet-agent-gotchas | dotnet-csharp-coding-standards | 0.2000 |
| 9 | dotnet-data-access-strategy | dotnet-service-communication | 0.2000 |
| 10 | dotnet-msbuild-authoring | dotnet-version-detection | 0.2000 |
| 11 | dotnet-cli-release-pipeline | dotnet-gha-patterns | 0.1875 |
| 12 | dotnet-csharp-configuration | dotnet-validation-patterns | 0.1875 |
| 13 | dotnet-ado-build-test | dotnet-ado-publish | 0.1765 |
| 14 | dotnet-api-docs | dotnet-openapi | 0.1765 |
| 15 | dotnet-csharp-configuration | dotnet-secrets-management | 0.1765 |
| 16 | dotnet-csharp-type-design-performance | dotnet-performance-patterns | 0.1765 |
| 17 | dotnet-uno-targets | dotnet-uno-testing | 0.1765 |
| 18 | dotnet-add-analyzers | dotnet-add-testing | 0.1667 |
| 19 | dotnet-blazor-components | dotnet-blazor-testing | 0.1667 |
| 20 | dotnet-csharp-async-patterns | dotnet-csharp-code-smells | 0.1667 |
| 21 | dotnet-gha-build-test | dotnet-gha-patterns | 0.1667 |
| 22 | dotnet-project-analysis | dotnet-project-structure | 0.1667 |
| 23 | dotnet-add-analyzers | dotnet-scaffold-project | 0.1579 |
| 24 | dotnet-add-ci | dotnet-add-testing | 0.1579 |
| 25 | dotnet-add-ci | dotnet-gha-deploy | 0.1579 |
| 26 | dotnet-agent-gotchas | dotnet-csharp-nullable-reference-types | 0.1579 |
| 27 | dotnet-aot-architecture | dotnet-serialization | 0.1579 |
| 28 | dotnet-architecture-patterns | dotnet-middleware-patterns | 0.1579 |
| 29 | dotnet-native-aot | dotnet-native-interop | 0.1579 |
| 30 | dotnet-realtime-communication | dotnet-service-communication | 0.1579 |

## Agent Bare-Text Reference Counts

Bare-text references to skill/agent IDs in agent files (should be `[skill:]` syntax):

| Agent | Bare Refs | Details |
|-------|-----------|---------|
| dotnet-architect | 2 | dotnet-architect(2) |
| dotnet-aspnetcore-specialist | 8 | dotnet-async-performance-specialist(2), dotnet-blazor-specialist(2), dotnet-aspnetcore-specialist(2), dotnet-security-reviewer(2) |
| dotnet-async-performance-specialist | 7 | dotnet-csharp-concurrency-specialist(2), dotnet-performance-analyst(2), dotnet-async-performance-specialist(2), dotnet-benchmark-designer(1) |
| dotnet-benchmark-designer | 3 | dotnet-benchmark-designer(2), dotnet-performance-analyst(1) |
| dotnet-blazor-specialist | 2 | dotnet-blazor-specialist(2) |
| dotnet-cloud-specialist | 8 | dotnet-cloud-specialist(2), dotnet-architect(2), dotnet-security-reviewer(2), dotnet-performance-analyst(1), dotnet-containers(1) |
| dotnet-code-review-agent | 11 | dotnet-code-review-agent(2), dotnet-benchmark-designer(1), dotnet-csharp-concurrency-specialist(1), dotnet-performance-analyst(1), dotnet-cloud-specialist(1) |
| dotnet-csharp-concurrency-specialist | 3 | dotnet-csharp-concurrency-specialist(2), dotnet-csharp-async-patterns(1) |
| dotnet-docs-generator | 2 | dotnet-docs-generator(2) |
| dotnet-maui-specialist | 2 | dotnet-maui-specialist(2) |
| dotnet-performance-analyst | 3 | dotnet-performance-analyst(2), dotnet-benchmark-designer(1) |
| dotnet-security-reviewer | 2 | dotnet-security-reviewer(2) |
| dotnet-testing-specialist | 9 | dotnet-benchmark-designer(2), dotnet-testing-specialist(2), dotnet-security-reviewer(2), dotnet-uno-specialist(1), dotnet-blazor-specialist(1) |
| dotnet-uno-specialist | 2 | dotnet-uno-specialist(2) |
| **Total** | **64** | |

### AGENTS.md Bare References

No bare-text references found in AGENTS.md (all references already use `[skill:]` or no skill refs present).

## Routing Test Hotspots

Skills referenced in `tests/agent-routing/cases.json`:

| Skill | Test Cases |
|-------|------------|
| dotnet-advisor | advisor-routing-maintainable-app |
| dotnet-architecture-patterns | architecture-layering |
| dotnet-benchmarkdotnet | perf-benchmark-design |
| dotnet-blazor-components | ui-blazor-component |
| dotnet-efcore-patterns | data-efcore-query |
| dotnet-gha-build-test | ci-gha-build-test |
| dotnet-minimal-apis | api-minimal-endpoints |
| dotnet-msbuild-authoring | build-msbuild-target |
| dotnet-security-owasp | security-owasp-review |
| dotnet-system-commandline | cli-system-commandline |
| dotnet-trimming | aot-trimming |
| dotnet-uno-mcp | uno-mcp-routing-skill-id-only |
| dotnet-version-detection | foundation-version-detection |
| dotnet-xunit | testing-xunit-strategy |

## Category Breakdown

| Category | Count | Skills |
|----------|-------|--------|
| agent-meta-skills | 5 | dotnet-agent-gotchas, dotnet-build-analysis, dotnet-csproj-reading, dotnet-slopwatch, dotnet-solution-navigation |
| ai | 1 | dotnet-semantic-kernel |
| api-development | 9 | dotnet-api-security, dotnet-api-surface-validation, dotnet-api-versioning, dotnet-csharp-api-design, dotnet-input-validation, dotnet-library-api-compat, dotnet-middleware-patterns, dotnet-minimal-apis, dotnet-openapi |
| architecture | 15 | dotnet-architecture-patterns, dotnet-aspire-patterns, dotnet-background-services, dotnet-container-deployment, dotnet-containers, dotnet-data-access-strategy, dotnet-domain-modeling, dotnet-efcore-architecture, dotnet-efcore-patterns, dotnet-http-client, dotnet-messaging-patterns, dotnet-observability, dotnet-resilience, dotnet-solid-principles, dotnet-structured-logging |
| build-system | 3 | dotnet-build-optimization, dotnet-msbuild-authoring, dotnet-msbuild-tasks |
| cicd | 8 | dotnet-ado-build-test, dotnet-ado-patterns, dotnet-ado-publish, dotnet-ado-unique, dotnet-gha-build-test, dotnet-gha-deploy, dotnet-gha-patterns, dotnet-gha-publish |
| cli-tools | 6 | dotnet-cli-architecture, dotnet-cli-distribution, dotnet-cli-packaging, dotnet-cli-release-pipeline, dotnet-system-commandline, dotnet-tool-management |
| core-csharp | 18 | dotnet-channels, dotnet-csharp-async-patterns, dotnet-csharp-code-smells, dotnet-csharp-coding-standards, dotnet-csharp-concurrency-patterns, dotnet-csharp-configuration, dotnet-csharp-dependency-injection, dotnet-csharp-modern-patterns, dotnet-csharp-nullable-reference-types, dotnet-csharp-source-generators, dotnet-csharp-type-design-performance, dotnet-editorconfig, dotnet-file-io, dotnet-io-pipelines, dotnet-linq-optimization, dotnet-native-interop, dotnet-roslyn-analyzers, dotnet-validation-patterns |
| documentation | 5 | dotnet-api-docs, dotnet-documentation-strategy, dotnet-github-docs, dotnet-mermaid-diagrams, dotnet-xml-docs |
| foundation | 4 | dotnet-advisor, dotnet-file-based-apps, dotnet-project-analysis, dotnet-version-detection |
| localization | 1 | dotnet-localization |
| multi-targeting | 2 | dotnet-multi-targeting, dotnet-version-upgrade |
| native-aot | 4 | dotnet-aot-architecture, dotnet-aot-wasm, dotnet-native-aot, dotnet-trimming |
| packaging | 3 | dotnet-github-releases, dotnet-msix, dotnet-nuget-authoring |
| performance | 5 | dotnet-benchmarkdotnet, dotnet-ci-benchmarking, dotnet-gc-memory, dotnet-performance-patterns, dotnet-profiling |
| project-structure | 7 | dotnet-add-analyzers, dotnet-add-ci, dotnet-add-testing, dotnet-artifacts-output, dotnet-modernize, dotnet-project-structure, dotnet-scaffold-project |
| release-management | 1 | dotnet-release-management |
| security | 3 | dotnet-cryptography, dotnet-secrets-management, dotnet-security-owasp |
| serialization | 4 | dotnet-grpc, dotnet-realtime-communication, dotnet-serialization, dotnet-service-communication |
| testing | 10 | dotnet-blazor-testing, dotnet-integration-testing, dotnet-maui-testing, dotnet-playwright, dotnet-snapshot-testing, dotnet-test-quality, dotnet-testing-strategy, dotnet-ui-testing-core, dotnet-uno-testing, dotnet-xunit |
| tui | 2 | dotnet-spectre-console, dotnet-terminal-gui |
| ui-frameworks | 14 | dotnet-accessibility, dotnet-blazor-auth, dotnet-blazor-components, dotnet-blazor-patterns, dotnet-maui-aot, dotnet-maui-development, dotnet-ui-chooser, dotnet-uno-mcp, dotnet-uno-platform, dotnet-uno-targets, dotnet-winforms-basics, dotnet-winui, dotnet-wpf-migration, dotnet-wpf-modern |

## Agent Description Inventory

| Agent | Desc Len |
|-------|----------|
| dotnet-architect | 246 |
| dotnet-aspnetcore-specialist | 301 |
| dotnet-async-performance-specialist | 287 |
| dotnet-benchmark-designer | 299 |
| dotnet-blazor-specialist | 241 |
| dotnet-cloud-specialist | 335 |
| dotnet-code-review-agent | 233 |
| dotnet-csharp-concurrency-specialist | 276 |
| dotnet-docs-generator | 340 |
| dotnet-maui-specialist | 285 |
| dotnet-performance-analyst | 302 |
| dotnet-security-reviewer | 165 |
| dotnet-testing-specialist | 323 |
| dotnet-uno-specialist | 317 |
