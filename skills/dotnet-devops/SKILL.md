---
name: dotnet-devops
description: Configures CI/CD pipelines, packaging, and operational tooling for .NET. Covers GitHub Actions (build/test, deploy, publish, patterns), Azure DevOps (build/test, publish, patterns, environments), containers (Dockerfiles, deployment), NuGet authoring, MSIX packaging, GitHub Releases, release management (NBGV, SemVer), observability (OpenTelemetry), and structured logging pipelines.
license: MIT
user-invocable: false
---

# dotnet-devops

## Overview

CI/CD, packaging, release management, and operational tooling for .NET. This consolidated skill spans 18 topic areas. Load the appropriate companion file from `references/` based on the routing table below.

## Routing Table

| Topic | Keywords | Companion File |
|-------|----------|----------------|
| GHA build/test | setup-dotnet, NuGet cache, reporting | references/gha-build-test.md |
| GHA deploy | Azure Web Apps, GitHub Pages, containers | references/gha-deploy.md |
| GHA publish | NuGet push, container images, signing, SBOM | references/gha-publish.md |
| GHA patterns | reusable workflows, composite, matrix, cache | references/gha-patterns.md |
| ADO build/test | DotNetCoreCLI, Artifacts, test results | references/ado-build-test.md |
| ADO publish | NuGet push, containers to ACR | references/ado-publish.md |
| ADO patterns | templates, variable groups, multi-stage | references/ado-patterns.md |
| ADO unique | environments, approvals, service connections | references/ado-unique.md |
| Containers | multi-stage Dockerfiles, SDK publish, rootless | references/containers.md |
| Container deployment | Compose, health probes, CI/CD pipelines | references/container-deployment.md |
| NuGet authoring | SDK-style, source generators, multi-TFM | references/nuget-authoring.md |
| MSIX | creation, signing, Store, sideload, auto-update | references/msix.md |
| GitHub Releases | creation, assets, notes, pre-release | references/github-releases.md |
| Release management | NBGV, SemVer, changelogs, branching | references/release-management.md |
| Observability | OpenTelemetry, health checks, custom metrics | references/observability.md |
| Structured logging | aggregation, sampling, PII, correlation | references/structured-logging.md |
| Add CI | CI/CD scaffold, GHA vs ADO detection | references/add-ci.md |
| GitHub docs | README badges, CONTRIBUTING, templates | references/github-docs.md |

## Scope

- GitHub Actions workflows
- Azure DevOps pipelines
- Container builds and deployment
- NuGet/MSIX packaging
- Release management (NBGV, SemVer, changelogs)
- Observability (OpenTelemetry, health checks)
- Structured logging
- GitHub repository documentation

## Out of scope

- API/backend code patterns -> [skill:dotnet-api]
- Build system authoring -> [skill:dotnet-tooling]
- Test authoring -> [skill:dotnet-testing]

## Companion Files

- `references/gha-build-test.md` -- GitHub Actions .NET build/test (setup-dotnet, NuGet cache, reporting)
- `references/gha-deploy.md` -- GitHub Actions deployment (Azure Web Apps, GitHub Pages, containers)
- `references/gha-publish.md` -- GitHub Actions publishing (NuGet push, container images, signing, SBOM)
- `references/gha-patterns.md` -- GitHub Actions composition (reusable workflows, composite, matrix, cache)
- `references/ado-build-test.md` -- Azure DevOps .NET build/test (DotNetCoreCLI, Artifacts, test results)
- `references/ado-publish.md` -- Azure DevOps publishing (NuGet push, containers to ACR)
- `references/ado-patterns.md` -- Azure DevOps composition (templates, variable groups, multi-stage)
- `references/ado-unique.md` -- Azure DevOps exclusive features (environments, approvals, service connections)
- `references/containers.md` -- .NET containerization (multi-stage Dockerfiles, SDK publish, rootless)
- `references/container-deployment.md` -- Container deployment (Compose, health probes, CI/CD pipelines)
- `references/nuget-authoring.md` -- NuGet package authoring (SDK-style, source generators, multi-TFM)
- `references/msix.md` -- MSIX packaging (creation, signing, Store, sideload, auto-update)
- `references/github-releases.md` -- GitHub Releases (creation, assets, notes, pre-release)
- `references/release-management.md` -- Release lifecycle (NBGV, SemVer, changelogs, branching)
- `references/observability.md` -- Observability (OpenTelemetry, health checks, custom metrics)
- `references/structured-logging.md` -- Log pipelines (aggregation, sampling, PII, correlation)
- `references/add-ci.md` -- CI/CD scaffolding (GHA vs ADO detection, workflow templates)
- `references/github-docs.md` -- GitHub documentation (README badges, CONTRIBUTING, templates)
