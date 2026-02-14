# fn-20-packaging-and-publishing-skills.2 Create GitHub Releases and Release Management skills

## Description
Create two release-focused skills: `dotnet-github-releases` (in `skills/packaging/`) and `dotnet-release-management` (in `skills/release-management/`). Each skill needs `name` and `description` frontmatter, comprehensive content with code examples, out-of-scope boundary statements, and cross-references. This task is parallelizable with fn-20.1 (file-disjoint).

**`dotnet-github-releases`** covers:
- Release creation via `gh release create` CLI and GitHub API
- Asset attachment patterns (NuGet packages, binaries, SBOMs, checksums)
- `softprops/action-gh-release` GHA action usage (brief, cross-ref `[skill:dotnet-gha-publish]` for full CI workflow)
- Release notes generation strategies (GitHub auto-generated, changelog-based, conventional commits)
- Pre-release management (draft releases, pre-release flag, promoting pre-release to stable)
- Tag-triggered vs release-triggered workflows (concept only, cross-ref CI skills for YAML)
- Does NOT re-teach CLI-specific release pipelines (cross-ref `[skill:dotnet-cli-release-pipeline]`)
- Does NOT re-teach GHA workflow syntax (cross-ref `[skill:dotnet-gha-patterns]`)

**`dotnet-release-management`** covers:
- NBGV (`Nerdbank.GitVersioning`) setup: `version.json` configuration, version height, public release vs pre-release
- SemVer 2.0 strategy for .NET libraries (when to bump major/minor/patch)
- SemVer for applications (build metadata, deployment versioning)
- Changelog generation (Keep a Changelog format, auto-generation with tools, conventional commit integration)
- Pre-release version workflows (alpha → beta → rc → stable)
- Release branching patterns (release branches, hotfix branches, trunk-based with tags)
- Does NOT re-teach plugin-specific release workflow (cross-ref `[skill:plugin-self-publish]`)
- Does NOT re-teach CI publish workflows (cross-ref `[skill:dotnet-gha-publish]`/`[skill:dotnet-ado-publish]`)

**Files created:**
- `skills/packaging/dotnet-github-releases/SKILL.md`
- `skills/release-management/dotnet-release-management/SKILL.md`

**Files NOT modified:** `plugin.json`, `dotnet-advisor/SKILL.md` (handled by fn-20.3)

## Acceptance
- [ ] `skills/packaging/dotnet-github-releases/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-github-releases` covers release creation, asset attachment, release notes generation, pre-release management
- [ ] `dotnet-github-releases` cross-refs `[skill:dotnet-cli-release-pipeline]` with scope boundary
- [ ] `dotnet-github-releases` cross-refs `[skill:dotnet-gha-publish]` for CI workflow context
- [ ] `dotnet-github-releases` contains out-of-scope boundary statement
- [ ] `skills/release-management/dotnet-release-management/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-release-management` covers NBGV, SemVer strategy, changelog generation, pre-release workflows, release branching
- [ ] `dotnet-release-management` cross-refs `[skill:plugin-self-publish]` with scope boundary
- [ ] `dotnet-release-management` contains out-of-scope boundary statement
- [ ] Description frontmatter < 120 chars per skill

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
