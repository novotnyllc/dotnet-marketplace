# Skill Routing Ownership Manifest

> **Historical document (fn-53).** This manifest was generated before the flat layout migration (fn-56). Paths shown as `skills/<category>/<skill-name>/` now resolve to `skills/<skill-name>/` in the current repo. The category column is preserved for audit traceability. Skill count was 130 at the time of this audit; current canonical count is 131.

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
| **Total** | | **131 skills + 14 agents** | |

**Distribution rationale**: T9 (34) exceeds the ~30 target because it collects 8 distinct low-coupling categories (build-system, cli-tools, documentation, packaging, performance, project-structure, release-management, serialization). Moving skills to other tasks would break the natural category grouping and introduce cross-category ownership splits. The skills in T9 are lower-traffic and simpler to normalize, so the higher count does not increase sweep difficulty proportionally.

## Full Manifest

| Skill Path | Category | Assigned Task | Notes |
|------------|----------|---------------|-------|
| skills/dotnet-agent-gotchas/SKILL.md | agent-meta-skills | T5 |  |
| skills/dotnet-build-analysis/SKILL.md | agent-meta-skills | T5 |  |
| skills/dotnet-csproj-reading/SKILL.md | agent-meta-skills | T5 |  |
| skills/dotnet-slopwatch/SKILL.md | agent-meta-skills | T5 | desc 116ch (over-budget risk) |
| skills/dotnet-solution-navigation/SKILL.md | agent-meta-skills | T5 |  |
| skills/dotnet-minimal-apis/SKILL.md | api-development | T5 | routing-test hotspot; desc 113ch (over-budget risk) |
| skills/dotnet-architecture-patterns/SKILL.md | architecture | T5 | routing-test hotspot; zero routing markers |
| skills/dotnet-efcore-patterns/SKILL.md | architecture | T5 | routing-test hotspot; desc 118ch (over-budget risk); zero routing markers |
| skills/dotnet-gha-build-test/SKILL.md | cicd | T5 | routing-test hotspot; desc 119ch (over-budget risk); zero routing markers |
| skills/dotnet-csharp-coding-standards/SKILL.md | core-csharp | T5 | zero routing markers |
| skills/dotnet-advisor/SKILL.md | foundation | T5 | routing-test hotspot; hub skill (226 refs); zero routing markers |
| skills/dotnet-file-based-apps/SKILL.md | foundation | T5 |  |
| skills/dotnet-project-analysis/SKILL.md | foundation | T5 |  |
| skills/dotnet-version-detection/SKILL.md | foundation | T5 | routing-test hotspot; zero routing markers |
| skills/dotnet-security-owasp/SKILL.md | security | T5 | routing-test hotspot; desc 118ch (over-budget risk) |
| skills/dotnet-xunit/SKILL.md | testing | T5 | routing-test hotspot |
| skills/dotnet-aspire-patterns/SKILL.md | architecture | T6 |  |
| skills/dotnet-background-services/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-container-deployment/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-containers/SKILL.md | architecture | T6 |  |
| skills/dotnet-data-access-strategy/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-domain-modeling/SKILL.md | architecture | T6 |  |
| skills/dotnet-efcore-architecture/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-http-client/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-messaging-patterns/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-observability/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-resilience/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-solid-principles/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-structured-logging/SKILL.md | architecture | T6 | zero routing markers |
| skills/dotnet-channels/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-async-patterns/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-code-smells/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-concurrency-patterns/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-csharp-configuration/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-dependency-injection/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-modern-patterns/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-csharp-nullable-reference-types/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-source-generators/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-csharp-type-design-performance/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-editorconfig/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-file-io/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-io-pipelines/SKILL.md | core-csharp | T6 | zero routing markers |
| skills/dotnet-linq-optimization/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-native-interop/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-roslyn-analyzers/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-validation-patterns/SKILL.md | core-csharp | T6 |  |
| skills/dotnet-api-security/SKILL.md | api-development | T7 |  |
| skills/dotnet-api-surface-validation/SKILL.md | api-development | T7 |  |
| skills/dotnet-api-versioning/SKILL.md | api-development | T7 |  |
| skills/dotnet-csharp-api-design/SKILL.md | api-development | T7 |  |
| skills/dotnet-input-validation/SKILL.md | api-development | T7 |  |
| skills/dotnet-library-api-compat/SKILL.md | api-development | T7 |  |
| skills/dotnet-middleware-patterns/SKILL.md | api-development | T7 | zero routing markers |
| skills/dotnet-openapi/SKILL.md | api-development | T7 |  |
| skills/dotnet-ado-build-test/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-ado-patterns/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-ado-publish/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-ado-unique/SKILL.md | cicd | T7 |  |
| skills/dotnet-gha-deploy/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-gha-patterns/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-gha-publish/SKILL.md | cicd | T7 | zero routing markers |
| skills/dotnet-cryptography/SKILL.md | security | T7 |  |
| skills/dotnet-secrets-management/SKILL.md | security | T7 |  |
| skills/dotnet-blazor-testing/SKILL.md | testing | T7 |  |
| skills/dotnet-integration-testing/SKILL.md | testing | T7 |  |
| skills/dotnet-maui-testing/SKILL.md | testing | T7 |  |
| skills/dotnet-playwright/SKILL.md | testing | T7 |  |
| skills/dotnet-snapshot-testing/SKILL.md | testing | T7 |  |
| skills/dotnet-test-quality/SKILL.md | testing | T7 |  |
| skills/dotnet-testing-strategy/SKILL.md | testing | T7 |  |
| skills/dotnet-ui-testing-core/SKILL.md | testing | T7 |  |
| skills/dotnet-uno-testing/SKILL.md | testing | T7 |  |
| skills/dotnet-semantic-kernel/SKILL.md | ai | T8 |  |
| skills/dotnet-localization/SKILL.md | localization | T8 |  |
| skills/dotnet-multi-targeting/SKILL.md | multi-targeting | T8 |  |
| skills/dotnet-version-upgrade/SKILL.md | multi-targeting | T8 |  |
| skills/dotnet-aot-architecture/SKILL.md | native-aot | T8 | zero routing markers |
| skills/dotnet-aot-wasm/SKILL.md | native-aot | T8 |  |
| skills/dotnet-native-aot/SKILL.md | native-aot | T8 |  |
| skills/dotnet-trimming/SKILL.md | native-aot | T8 | routing-test hotspot; zero routing markers |
| skills/dotnet-spectre-console/SKILL.md | tui | T8 |  |
| skills/dotnet-terminal-gui/SKILL.md | tui | T8 |  |
| skills/dotnet-accessibility/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-blazor-auth/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-blazor-components/SKILL.md | ui-frameworks | T8 | routing-test hotspot |
| skills/dotnet-blazor-patterns/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-maui-aot/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-maui-development/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-ui-chooser/SKILL.md | ui-frameworks | T8 | zero routing markers |
| skills/dotnet-uno-mcp/SKILL.md | ui-frameworks | T8 | routing-test hotspot |
| skills/dotnet-uno-platform/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-uno-targets/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-winforms-basics/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-winui/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-wpf-migration/SKILL.md | ui-frameworks | T8 | zero routing markers |
| skills/dotnet-wpf-modern/SKILL.md | ui-frameworks | T8 |  |
| skills/dotnet-build-optimization/SKILL.md | build-system | T9 | zero routing markers |
| skills/dotnet-msbuild-authoring/SKILL.md | build-system | T9 | routing-test hotspot; desc 116ch (over-budget risk); zero routing markers |
| skills/dotnet-msbuild-tasks/SKILL.md | build-system | T9 | zero routing markers |
| skills/dotnet-cli-architecture/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/dotnet-cli-distribution/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/dotnet-cli-packaging/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/dotnet-cli-release-pipeline/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/dotnet-system-commandline/SKILL.md | cli-tools | T9 | routing-test hotspot; desc 112ch (over-budget risk); zero routing markers |
| skills/dotnet-tool-management/SKILL.md | cli-tools | T9 | zero routing markers |
| skills/dotnet-api-docs/SKILL.md | documentation | T9 | zero routing markers |
| skills/dotnet-documentation-strategy/SKILL.md | documentation | T9 | zero routing markers |
| skills/dotnet-github-docs/SKILL.md | documentation | T9 |  |
| skills/dotnet-mermaid-diagrams/SKILL.md | documentation | T9 | zero routing markers |
| skills/dotnet-xml-docs/SKILL.md | documentation | T9 | zero routing markers |
| skills/dotnet-github-releases/SKILL.md | packaging | T9 | zero routing markers |
| skills/dotnet-msix/SKILL.md | packaging | T9 | zero routing markers |
| skills/dotnet-nuget-authoring/SKILL.md | packaging | T9 | zero routing markers |
| skills/dotnet-benchmarkdotnet/SKILL.md | performance | T9 | routing-test hotspot; desc 117ch (over-budget risk); zero routing markers |
| skills/dotnet-ci-benchmarking/SKILL.md | performance | T9 | zero routing markers |
| skills/dotnet-gc-memory/SKILL.md | performance | T9 |  |
| skills/dotnet-performance-patterns/SKILL.md | performance | T9 |  |
| skills/dotnet-profiling/SKILL.md | performance | T9 | zero routing markers |
| skills/dotnet-add-analyzers/SKILL.md | project-structure | T9 |  |
| skills/dotnet-add-ci/SKILL.md | project-structure | T9 |  |
| skills/dotnet-add-testing/SKILL.md | project-structure | T9 |  |
| skills/dotnet-artifacts-output/SKILL.md | project-structure | T9 |  |
| skills/dotnet-modernize/SKILL.md | project-structure | T9 |  |
| skills/dotnet-project-structure/SKILL.md | project-structure | T9 |  |
| skills/dotnet-scaffold-project/SKILL.md | project-structure | T9 |  |
| skills/dotnet-release-management/SKILL.md | release-management | T9 | zero routing markers |
| skills/dotnet-grpc/SKILL.md | serialization | T9 | zero routing markers |
| skills/dotnet-realtime-communication/SKILL.md | serialization | T9 |  |
| skills/dotnet-serialization/SKILL.md | serialization | T9 | zero routing markers |
| skills/dotnet-service-communication/SKILL.md | serialization | T9 | zero routing markers |

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

- Total skill paths assigned: 131
- Total agent paths assigned: 14
- Overlap check: **PASSED** (no skill appears in two tasks)
- Coverage check: **PASSED** (all 131 skills + 14 agents assigned)
