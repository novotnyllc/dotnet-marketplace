# fn-19: CI/CD Skills

## Problem/Goal
Add comprehensive CI/CD skills for GitHub Actions and Azure DevOps covering composable patterns, build/test/publish workflows, and platform-unique features. Support both platforms equally with reusable patterns.

## Acceptance Checks
- [ ] `dotnet-gha-patterns` skill covers composable GitHub Actions (reusable workflows, composite actions, matrix builds)
- [ ] `dotnet-gha-build-test`, `dotnet-gha-publish`, `dotnet-gha-deploy` skills cover scenario-specific workflows
- [ ] `dotnet-ado-patterns` skill covers composable ADO YAML + ADO-unique features (Environments, Gates, Approvals)
- [ ] `dotnet-ado-build-test`, `dotnet-ado-publish`, `dotnet-ado-unique` skills cover scenarios + unique capabilities
- [ ] Cross-references to AOT, CLI distribution, package publishing, benchmarking skills
- [ ] Skills integrate with dotnet-cli-unified-pipeline for multi-platform package publishing

## Key Context
- Both platforms supported equally (no bias)
- Composability is key for maintainability
- ADO has unique features (classic pipelines, release management) that GHA doesn't
- Skills must support Native AOT build workflows and multi-platform distribution
