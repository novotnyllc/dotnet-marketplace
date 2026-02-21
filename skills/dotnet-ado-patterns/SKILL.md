---
name: dotnet-ado-patterns
description: Composes Azure DevOps YAML pipelines. Templates, variable groups, multi-stage, triggers.
license: MIT
user-invocable: false
---

# dotnet-ado-patterns

Composable Azure DevOps YAML pipeline patterns for .NET projects: template references with `extends`, `stages`, `jobs`, and `steps` keywords for hierarchical pipeline composition, variable groups and variable templates for centralized configuration, pipeline decorators for organization-wide policy injection, conditional insertion with `${{ if }}` and `${{ each }}` expressions, multi-stage pipelines (build, test, deploy), and pipeline triggers for CI, PR, and scheduled runs.

**Version assumptions:** Azure Pipelines YAML schema. `DotNetCoreCLI@2` task for .NET 8/9/10 builds. Template expressions syntax v2.

## Scope

- Template references with extends, stages, jobs, and steps keywords
- Variable groups and variable templates for centralized configuration
- Pipeline decorators for organization-wide policy injection
- Conditional insertion with ${{ if }} and ${{ each }} expressions
- Multi-stage pipelines (build, test, deploy)
- Pipeline triggers for CI, PR, and scheduled runs

## Out of scope

- Starter CI templates -- see [skill:dotnet-add-ci]
- CLI release pipelines (tag-triggered build-package-release for CLI tools) -- see [skill:dotnet-cli-release-pipeline]
- ADO-unique features (environments, service connections, classic releases) -- see [skill:dotnet-ado-unique]
- Build/test specifics -- see [skill:dotnet-ado-build-test]
- Publishing pipelines -- see [skill:dotnet-ado-publish]
- GitHub Actions workflow patterns -- see [skill:dotnet-gha-patterns]

Cross-references: [skill:dotnet-add-ci] for starter templates that these patterns extend, [skill:dotnet-cli-release-pipeline] for CLI-specific release automation.

---


For detailed YAML examples (stage/job/step templates, extends, variable groups, conditional insertion, multi-stage pipelines, triggers), see `examples.md` in this skill directory.

## Agent Gotchas

1. **Template parameter types are enforced at compile time** -- passing a string where `type: boolean` is expected causes a validation error before the pipeline runs; always match types exactly.
2. **`extends` templates cannot be overridden** -- callers cannot inject steps before or after the mandatory stages; this is by design for policy enforcement.
3. **Variable group secrets are not available in template expressions** -- `${{ variables.mySecret }}` resolves at compile time when secrets are not yet available; use `$(mySecret)` runtime syntax instead.
4. **`${{ each }}` iterates at compile time** -- the loop generates YAML before the pipeline runs; runtime variables cannot be used as the iteration source.
5. **CI and PR triggers are mutually exclusive with `trigger: none` and `pr: none`** -- omitting both `trigger` and `pr` sections enables default CI triggering on all branches; explicitly set `trigger: none` to disable.
6. **Path filters in triggers use repository root-relative paths** -- do not prefix paths with `/` or `./`; use `src/**` not `./src/**`.
7. **Scheduled triggers always run on the default branch first** -- the `branches.include` filter applies after the schedule fires; the schedule itself is only evaluated from the default branch YAML.
8. **Pipeline resource triggers require the source pipeline name, not the YAML file path** -- use the pipeline name as shown in ADO, not the `azure-pipelines.yml` file path.
