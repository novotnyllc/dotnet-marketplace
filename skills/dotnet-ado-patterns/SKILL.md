---
name: dotnet-ado-patterns
description: Composes Azure DevOps YAML pipelines. Templates, variable groups, multi-stage, triggers.
license: MIT
user-invocable: false
---

# dotnet-ado-patterns

Composable Azure DevOps YAML pipeline patterns for .NET projects: template references with `extends`, `stages`, `jobs`, and `steps` keywords for hierarchical pipeline composition, variable groups and variable templates for centralized configuration, conditional insertion with `${{ if }}` and `${{ each }}` expressions, multi-stage pipelines (build, test, deploy), and pipeline triggers for CI, PR, and scheduled runs.

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

## Template Composition

### Step Template (reusable steps inserted into a job)

```yaml
# templates/steps/dotnet-setup.yml
parameters:
  - name: dotnetVersion
    type: string
    default: '8.0.x'
  - name: nugetFeed
    type: string
    default: ''

steps:
  - task: UseDotNet@2
    displayName: 'Install .NET SDK ${{ parameters.dotnetVersion }}'
    inputs:
      packageType: 'sdk'
      version: ${{ parameters.dotnetVersion }}

  - ${{ if ne(parameters.nugetFeed, '') }}:
    - task: NuGetAuthenticate@1
```

### Extends Template (enforced pipeline structure)

```yaml
# templates/pipeline-policy.yml -- callers cannot bypass this structure
parameters:
  - name: stages
    type: stageList
    default: []

stages:
  - stage: SecurityScan
    jobs:
      - job: Scan
        steps:
          - script: echo "Running mandatory security scan"

  - ${{ each stage in parameters.stages }}:
    - ${{ stage }}
```

```yaml
# azure-pipelines.yml (caller)
extends:
  template: templates/pipeline-policy.yml
  parameters:
    stages:
      - stage: Build
        jobs:
          - job: BuildApp
            steps:
              - script: dotnet build -c Release
```

---

## Variable Groups and Templates

```yaml
# templates/variables/dotnet-defaults.yml
variables:
  dotnetVersion: '8.0.x'
  buildConfiguration: 'Release'

# azure-pipelines.yml
variables:
  - template: templates/variables/dotnet-defaults.yml
  - group: 'kv-production-secrets'   # Key Vault-linked for secrets
  - name: projectPath
    value: 'MyApp.sln'
```

Key Vault secrets resolve at runtime via `$(secret-name)`, not template expressions `${{ }}`.

---

## Pipeline Decorators

Decorators inject steps into every pipeline in an organization, enforcing policies without modifying individual pipeline files. They are defined via ADO extensions (not YAML) and cannot be overridden by callers. Debug by inspecting the expanded pipeline YAML in ADO run logs. See [skill:dotnet-ado-unique] for implementation details including extension manifests and deployment.

---

## Conditional Insertion

```yaml
parameters:
  - name: environments
    type: object
    default:
      - name: staging
        approvals: false
      - name: production
        approvals: true

stages:
  - ${{ each env in parameters.environments }}:
    - stage: Deploy_${{ env.name }}
      jobs:
        - ${{ if eq(env.approvals, true) }}:
          - job: Approve
            pool: server
            steps:
              - task: ManualValidation@0
        - deployment: DeployApp
          environment: ${{ env.name }}
          strategy:
            runOnce:
              deploy:
                steps:
                  - script: echo "Deploying to ${{ env.name }}"
```

---

## Triggers

```yaml
# CI trigger
trigger:
  branches:
    include: [main, release/*]
  paths:
    include: [src/**, tests/**]
    exclude: [docs/**, '*.md']

# PR trigger
pr:
  branches:
    include: [main]
  drafts: false

# Scheduled trigger
schedules:
  - cron: '0 6 * * 1-5'
    branches:
      include: [main]
    always: false   # only run if changes since last

# Pipeline resource trigger (downstream of another pipeline)
resources:
  pipelines:
    - pipeline: buildPipeline
      source: 'MyApp-Build'
      trigger:
        branches:
          include: [main]
```

---

## Agent Gotchas

1. **Template parameter types are enforced at compile time** -- passing a string where `type: boolean` is expected causes a validation error before the pipeline runs.
2. **`extends` templates cannot be overridden** -- callers cannot inject steps before or after mandatory stages.
3. **Variable group secrets are not available in template expressions** -- `${{ variables.mySecret }}` resolves at compile time when secrets are not yet available; use `$(mySecret)` runtime syntax.
4. **`${{ each }}` iterates at compile time** -- runtime variables cannot be used as the iteration source.
5. **Omitting both `trigger` and `pr` enables default CI triggering on all branches** -- explicitly set `trigger: none` to disable.
6. **Path filters use repository root-relative paths** -- use `src/**` not `./src/**`.
7. **Scheduled triggers always run on the default branch first** -- `branches.include` applies after the schedule fires.
8. **Pipeline resource triggers require the source pipeline name** -- use the ADO pipeline name, not the YAML file path.

For extended examples (complete multi-stage pipelines, job templates, coverage integration), see `examples.md` in this skill directory.
