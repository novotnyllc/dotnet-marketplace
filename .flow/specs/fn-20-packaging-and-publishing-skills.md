# fn-20: Packaging and Publishing Skills

## Problem/Goal
Add modern NuGet packaging, MSIX packaging, and GitHub Releases skills covering central package management, source generators, SourceLink, CI publishing, and release lifecycle management.

## Acceptance Checks
- [ ] `dotnet-nuget-modern` skill covers CPM, source generators, SDK-style projects, SourceLink, CI publish
- [ ] `dotnet-msix` skill covers full MSIX pipeline (creation, signing, distribution, Microsoft Store, sideloading, auto-update)
- [ ] `dotnet-github-releases` skill covers publishing to GitHub Releases with release notes generation
- [ ] Cross-references to CI/CD skills, release management, AOT skills
- [ ] Skills integrate with dotnet-release-management for full lifecycle

## Key Context
- Central Package Management is modern standard for multi-project solutions
- MSIX is modern Windows app packaging (replaces ClickOnce, MSI for many scenarios)
- GitHub Releases + NBGV provide complete release lifecycle
- Skills must integrate with CI/CD pipelines for automated publishing
