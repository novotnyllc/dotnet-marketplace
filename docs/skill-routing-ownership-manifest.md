# Skill Routing Ownership Manifest

Generated for fn-53-skill-routing-language-hardening.1 (T1).
Each skill path maps to exactly one downstream editing task (T5-T10).
Zero overlaps: no skill path appears in two tasks.

## Task Distribution Summary

| Task | Title | Count | Categories |
|------|-------|-------|------------|
| T5 (fn-53.5) | Normalize Foundation and High-Traffic Skills | 16 | agent-meta-skills, api-development, architecture, cicd, core-csharp, foundation, security, testing |
| T6 (fn-53.6) | Category Sweep - Core, Architecture | 30 | architecture, core-csharp |
| T7 (fn-53.7) | Category Sweep - API, Security, Testing, CI | 26 | api-development, cicd, security, testing |
| T8 (fn-53.8) | Category Sweep - UI, NativeAOT, TUI, MultiTarget | 24 | ai, localization, multi-targeting, native-aot, tui, ui-frameworks |
| T9 (fn-53.9) | Category Sweep - Long Tail | 34 | build-system, cli-tools, documentation, packaging, performance, project-structure, release-management, serialization |
| T10 (fn-53.10) | Agent File Normalization | 14 | agents |
| **Total** | | **130 skills + 14 agents** | |

**Distribution rationale**: T9 (34) exceeds the ~30 target because it collects 8 distinct low-coupling categories (build-system, cli-tools, documentation, packaging, performance, project-structure, release-management, serialization). Moving skills to other tasks would break the natural category grouping and introduce cross-category ownership splits. The skills in T9 are lower-traffic and simpler to normalize, so the higher count does not increase sweep difficulty proportionally.

## Full Manifest

| Skill Path | Category | Assigned Task | Notes |
|------------|----------|---------------|-------|
| skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md | agent-meta-skills | T5 |  |
| skills/agent-meta-skills/dotnet-build-analysis/SKILL.md | agent-meta-skills | T5 |  |
| skills/agent-meta-skills/dotnet-csproj-reading/SKILL.md | agent-meta-skills | T5 |  |
| skills/agent-meta-skills/dotnet-slopwatch/SKILL.md | agent-meta-skills | T5 | desc 116ch (over-budget risk) |
| skills/agent-meta-skills/dotnet-solution-navigation/SKILL.md | agent-meta-skills | T5 |  |
| skills/api-development/dotnet-minimal-apis/SKILL.md | api-development | T5 | routing-test hotspot; desc 113ch (over-budget risk) |
| skills/architecture/dotnet-architecture-patterns/SKILL.md | architecture | T5 | routing-test hotspot; zero routing markers |
| skills/architecture/dotnet-efcore-patterns/SKILL.md | architecture | T5 | routing-test hotspot; desc 118ch (over-budget risk); zero routing markers |
| skills/cicd/dotnet-gha-build-test/SKILL.md | cicd | T5 | routing-test hotspot; desc 119ch (over-budget risk); zero routing markers |
| skills/core-csharp/dotnet-csharp-coding-standards/SKILL.md | core-csharp | T5 | zero routing markers |
| skills/foundation/dotnet-advisor/SKILL.md | foundation | T5 | routing-test hotspot; hub skill (226 refs); zero routing markers |
| skills/foundation/dotnet-file-based-apps/SKILL.md | foundation | T5 |  |
| skills/foundation/dotnet-project-analysis/SKILL.md | foundation | T5 |  |
| skills/foundation/dotnet-version-detection/SKILL.md | foundation | T5 | routing-test hotspot; zero routing markers |
| skills/security/dotnet-security-owasp/SKILL.md | security | T5 | routing-test hotspot; desc 118ch (over-budget risk) |
| skills/testing/dotnet-xunit/SKILL.md | testing | T5 | routing-test hotspot |
| skills/architecture/dotnet-aspire-patterns/SKILL.md | architecture | T6 |  |
| skills/architecture/dotnet-background-services/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-container-deployment/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-containers/SKILL.md | architecture | T6 |  |
| skills/architecture/dotnet-data-access-strategy/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-domain-modeling/SKILL.md | architecture | T6 |  |
| skills/architecture/dotnet-efcore-architecture/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-http-client/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-messaging-patterns/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-observability/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-resilience/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-solid-principles/SKILL.md | architecture | T6 | zero routing markers |
| skills/architecture/dotnet-structured-logging/SKILL.md | architecture | T6 | zero routing markers |
| skills/core-csharp/dotnet-channels/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-async-patterns/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-code-smells/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-concurrency-patterns/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-csharp-configuration/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-dependency-injection/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-modern-patterns/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-csharp-nullable-reference-types/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-source-generators/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-csharp-type-design-performance/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-editorconfig/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-file-io/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-io-pipelines/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/core-csharp/dotnet-linq-optimization/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-native-interop/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-roslyn-analyzers/SKILL.md | core-csharp | T6 |  |
| skills/core-csharp/dotnet-validation-patterns/SKILL.md | core-csharp | T6 |  |
| skills/api-development/dotnet-api-security/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-api-surface-validation/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-api-versioning/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-csharp-api-design/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-input-validation/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-library-api-compat/SKILL.md | api-development | T7 |  |
| skills/api-development/dotnet-middleware-patterns/SKILL.md | api-development | T7 | zero routing markers |
| skills/api-development/dotnet-openapi/SKILL.md | api-development | T7 |  |
| skills/cicd/dotnet-ado-build-test/SKILL.md | cicd | T7 | zero routing markers |
| skills/cicd/dotnet-ado-patterns/SKILL.md | cicd | T7 | zero routing markers |
| skills/cicd/dotnet-ado-publish/SKILL.md | cicd | T7 | zero routing markers |
| skills/cicd/dotnet-ado-unique/SKILL.md | cicd | T7 |  |
| skills/cicd/dotnet-gha-deploy/SKILL.md | cicd | T7 | zero routing markers |
| skills/cicd/dotnet-gha-patterns/SKILL.md | cicd | T7 | zero routing markers |
| skills/cicd/dotnet-gha-publish/SKILL.md | cicd | T7 | zero routing markers |
| skills/security/dotnet-cryptography/SKILL.md | security | T7 |  |
| skills/security/dotnet-secrets-management/SKILL.md | security | T7 |  |
| skills/testing/dotnet-blazor-testing/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-integration-testing/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-maui-testing/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-playwright/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-snapshot-testing/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-test-quality/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-testing-strategy/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-ui-testing-core/SKILL.md | testing | T7 |  |
| skills/testing/dotnet-uno-testing/SKILL.md | testing | T7 |  |
| skills/ai/dotnet-semantic-kernel/SKILL.md | ai | T8 |  |
| skills/localization/dotnet-localization/SKILL.md | localization | T8 |  |
| skills/multi-targeting/dotnet-multi-targeting/SKILL.md | multi-targeting | T8 |  |
| skills/multi-targeting/dotnet-version-upgrade/SKILL.md | multi-targeting | T8 |  |
| skills/native-aot/dotnet-aot-architecture/SKILL.md | native-aot | T8 | zero routing markers |
| skills/native-aot/dotnet-aot-wasm/SKILL.md | native-aot | T8 |  |
| skills/native-aot/dotnet-native-aot/SKILL.md | native-aot | T8 |  |
| skills/native-aot/dotnet-trimming/SKILL.md | native-aot | T8 | routing-test hotspot; zero routing markers |
| skills/tui/dotnet-spectre-console/SKILL.md | tui | T8 |  |
| skills/tui/dotnet-terminal-gui/SKILL.md | tui | T8 |  |
| skills/ui-frameworks/dotnet-accessibility/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-blazor-auth/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-blazor-components/SKILL.md | ui-frameworks | T8 | routing-test hotspot |
| skills/ui-frameworks/dotnet-blazor-patterns/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-maui-aot/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-maui-development/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-ui-chooser/SKILL.md | ui-frameworks | T8 | zero routing markers |
| skills/ui-frameworks/dotnet-uno-mcp/SKILL.md | ui-frameworks | T8 | routing-test hotspot |
| skills/ui-frameworks/dotnet-uno-platform/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-uno-targets/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-winforms-basics/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-winui/SKILL.md | ui-frameworks | T8 |  |
| skills/ui-frameworks/dotnet-wpf-migration/SKILL.md | ui-frameworks | T8 | zero routing markers |
| skills/ui-frameworks/dotnet-wpf-modern/SKILL.md | ui-frameworks | T8 |  |
| skills/build-system/dotnet-build-optimization/SKILL.md | build-system | T9 | zero routing markers |
| skills/build-system/dotnet-msbuild-authoring/SKILL.md | build-system | T9 | routing-test hotspot; desc 116ch (over-budget risk); zero routing markers |
| skills/build-system/dotnet-msbuild-tasks/SKILL.md | build-system | T9 | zero routing markers |
| skills/cli-tools/dotnet-cli-architecture/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/cli-tools/dotnet-cli-distribution/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/cli-tools/dotnet-cli-packaging/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/cli-tools/dotnet-cli-release-pipeline/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/cli-tools/dotnet-system-commandline/SKILL.md | cli-tools | T9 | routing-test hotspot; desc 112ch (over-budget risk); zero routing markers |
| skills/cli-tools/dotnet-tool-management/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/documentation/dotnet-api-docs/SKILL.md | documentation | T9 | zero routing markers |
| skills/documentation/dotnet-documentation-strategy/SKILL.md | documentation | T9 | zero routing markers |
| skills/documentation/dotnet-github-docs/SKILL.md | documentation | T9 |  |
| skills/documentation/dotnet-mermaid-diagrams/SKILL.md | documentation | T9 | zero routing markers |
| skills/documentation/dotnet-xml-docs/SKILL.md | documentation | T9 | zero routing markers |
| skills/packaging/dotnet-github-releases/SKILL.md | packaging | T9 | zero routing markers |
| skills/packaging/dotnet-msix/SKILL.md | packaging | T9 | zero routing markers |
| skills/packaging/dotnet-nuget-authoring/SKILL.md | packaging | T9 | zero routing markers |
| skills/performance/dotnet-benchmarkdotnet/SKILL.md | performance | T9 | routing-test hotspot; desc 117ch (over-budget risk); zero routing markers |
| skills/performance/dotnet-ci-benchmarking/SKILL.md | performance | T9 | zero routing markers |
| skills/performance/dotnet-gc-memory/SKILL.md | performance | T9 |  |
| skills/performance/dotnet-performance-patterns/SKILL.md | performance | T9 |  |
| skills/performance/dotnet-profiling/SKILL.md | performance | T9 | zero routing markers |
| skills/project-structure/dotnet-add-analyzers/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-add-ci/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-add-testing/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-artifacts-output/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-modernize/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-project-structure/SKILL.md | project-structure | T9 |  |
| skills/project-structure/dotnet-scaffold-project/SKILL.md | project-structure | T9 |  |
| skills/release-management/dotnet-release-management/SKILL.md | release-management | T9 | zero routing markers |
| skills/serialization/dotnet-grpc/SKILL.md | serialization | T9 | zero routing markers |
| skills/serialization/dotnet-realtime-communication/SKILL.md | serialization | T9 |  |
| skills/serialization/dotnet-serialization/SKILL.md | serialization | T9 | zero routing markers |
| skills/serialization/dotnet-service-communication/SKILL.md | serialization | T9 | zero routing markers |

### T10: Agent Files

| Agent Path | Assigned Task | Notes |
|------------|---------------|-------|
| agents/dotnet-architect.md | T10 | 2 bare refs to convert |
| agents/dotnet-aspnetcore-specialist.md | T10 | 8 bare refs to convert |
| agents/dotnet-async-performance-specialist.md | T10 | 7 bare refs to convert |
| agents/dotnet-benchmark-designer.md | T10 | 3 bare refs to convert |
| agents/dotnet-blazor-specialist.md | T10 | 2 bare refs to convert |
| agents/dotnet-cloud-specialist.md | T10 | 8 bare refs to convert |
| agents/dotnet-code-review-agent.md | T10 | 11 bare refs to convert |
| agents/dotnet-csharp-concurrency-specialist.md | T10 | 3 bare refs to convert |
| agents/dotnet-docs-generator.md | T10 | 2 bare refs to convert |
| agents/dotnet-maui-specialist.md | T10 | 2 bare refs to convert |
| agents/dotnet-performance-analyst.md | T10 | 3 bare refs to convert |
| agents/dotnet-security-reviewer.md | T10 | 2 bare refs to convert |
| agents/dotnet-testing-specialist.md | T10 | 9 bare refs to convert |
| agents/dotnet-uno-specialist.md | T10 | 2 bare refs to convert |

## Verification

- Total skill paths assigned: 130
- Total agent paths assigned: 14
- Overlap check: **PASSED** (no skill appears in two tasks)
- Coverage check: **PASSED** (all 130 skills + 14 agents assigned)
