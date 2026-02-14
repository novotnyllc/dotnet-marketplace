# fn-21-documentation-skills.2 Create GitHub docs, XML docs, and API docs skills

## Description
Create three documentation skills: `dotnet-github-docs` (GitHub-native documentation), `dotnet-xml-docs` (XML documentation comments), and `dotnet-api-docs` (API documentation generation). All go in `skills/documentation/`. Each skill needs `name` and `description` frontmatter, comprehensive content with code examples, out-of-scope boundary statements, and cross-references. This task is parallelizable with fn-21.1 (file-disjoint).

**`dotnet-github-docs`** covers:
- README structure for .NET projects: badges (NuGet, CI, coverage, license), installation section with `dotnet add package`, quick start with code examples, API reference links, contributing section
- CONTRIBUTING.md patterns: fork-PR workflow, development setup (`dotnet restore`, `dotnet build`, `dotnet test`), coding standards reference, PR review process
- Issue templates: bug report (repro steps, expected/actual, .NET version, OS), feature request (problem/solution/alternatives), question/discussion
- PR templates: description, testing checklist, breaking changes, related issues
- GitHub Pages setup for documentation sites (concept only; deployment pipeline in `[skill:dotnet-gha-deploy]`)
- Repository metadata: `CODEOWNERS`, `.github/FUNDING.yml`, social preview, topics/tags
- Mermaid diagrams in README (cross-ref `[skill:dotnet-mermaid-diagrams]`)
- Does NOT re-teach CI deployment (cross-ref `[skill:dotnet-gha-deploy]`)
- Does NOT re-teach changelog generation (cross-ref `[skill:dotnet-release-management]`)

**`dotnet-xml-docs`** covers:
- All standard XML doc tags: `<summary>`, `<param>`, `<returns>`, `<exception>`, `<remarks>`, `<example>`, `<value>`, `<typeparam>`, `<typeparamref>`, `<paramref>`
- Advanced tags: `<inheritdoc>` (interface implementation, base class override), `<see cref="..."/>`, `<seealso>`, `<c>` and `<code>`
- Enabling XML doc generation: `<GenerateDocumentationFile>true</GenerateDocumentationFile>` in csproj
- Warning suppression for internal APIs: `<NoWarn>CS1591</NoWarn>` strategies, `[assembly: InternalsVisibleTo]` considerations
- XML doc conventions for public libraries: every public member documented, parameter descriptions, exception documentation, code examples in `<example>`
- Auto-generation tooling: IDE quick-fix generation, `///` trigger, GhostDoc patterns
- IntelliSense integration: how XML docs surface in IDE tooltips and autocomplete
- Does NOT re-teach general coding conventions (cross-ref `[skill:dotnet-csharp-coding-standards]`)
- Does NOT re-teach API doc site generation (cross-ref `[skill:dotnet-api-docs]`)

**`dotnet-api-docs`** covers:
- DocFX setup for .NET API reference: `docfx.json` configuration, metadata extraction from assemblies, template customization, cross-referencing between pages
- OpenAPI spec as documentation: using generated OpenAPI 3.x as living API docs, Scalar/Swagger UI embedding, versioned OpenAPI documents (cross-ref `[skill:dotnet-openapi]`)
- Doc site generation from XML comments: XML docs -> DocFX -> static HTML, XML docs -> Starlight with markdown extraction
- Keeping docs in sync with code: CI validation of doc completeness (`-warnaserror:CS1591`), broken link detection, automated doc builds on PR
- API changelog patterns: breaking change documentation, migration guides between major versions, deprecated API tracking
- Versioned API documentation: version selectors in doc sites, maintaining docs for multiple active versions, URL patterns
- Does NOT re-teach OpenAPI generation or configuration (cross-ref `[skill:dotnet-openapi]`)
- Does NOT re-teach CI deployment of doc sites (cross-ref `[skill:dotnet-gha-deploy]`)
- Does NOT re-teach XML doc comment syntax (cross-ref `[skill:dotnet-xml-docs]`)

**Files created:**
- `skills/documentation/dotnet-github-docs/SKILL.md`
- `skills/documentation/dotnet-xml-docs/SKILL.md`
- `skills/documentation/dotnet-api-docs/SKILL.md`

**Files NOT modified:** `plugin.json`, `dotnet-advisor/SKILL.md` (handled by fn-21.3)

## Acceptance
- [ ] `skills/documentation/dotnet-github-docs/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-github-docs` covers README structure with .NET badges, CONTRIBUTING patterns, issue/PR templates, GitHub Pages setup, repo metadata
- [ ] `dotnet-github-docs` cross-refs `[skill:dotnet-gha-deploy]` for GitHub Pages deployment without re-teaching CI YAML
- [ ] `dotnet-github-docs` cross-refs `[skill:dotnet-release-management]` for changelog format
- [ ] `dotnet-github-docs` cross-refs `[skill:dotnet-mermaid-diagrams]` for README diagrams
- [ ] `dotnet-github-docs` cross-refs `[skill:dotnet-project-structure]` for project metadata context
- [ ] `dotnet-github-docs` contains out-of-scope boundary statement
- [ ] `skills/documentation/dotnet-xml-docs/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-xml-docs` covers all standard XML doc tags, `<inheritdoc>`, `GenerateDocumentationFile`, warning suppression, library conventions
- [ ] `dotnet-xml-docs` includes C# code examples with comprehensive XML doc comments
- [ ] `dotnet-xml-docs` cross-refs `[skill:dotnet-csharp-coding-standards]` for general conventions
- [ ] `dotnet-xml-docs` cross-refs `[skill:dotnet-api-docs]` for downstream API doc generation
- [ ] `dotnet-xml-docs` contains out-of-scope boundary statement
- [ ] `skills/documentation/dotnet-api-docs/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-api-docs` covers DocFX setup (docfx.json), OpenAPI-as-documentation, doc-code sync, API changelogs, versioned docs
- [ ] `dotnet-api-docs` includes DocFX configuration example (`docfx.json` snippet)
- [ ] `dotnet-api-docs` cross-refs `[skill:dotnet-openapi]` for OpenAPI generation without re-teaching
- [ ] `dotnet-api-docs` cross-refs `[skill:dotnet-gha-deploy]` for doc site deployment without re-teaching CI
- [ ] `dotnet-api-docs` cross-refs `[skill:dotnet-xml-docs]` for XML comment syntax
- [ ] `dotnet-api-docs` contains out-of-scope boundary statement
- [ ] Description frontmatter < 120 chars per skill

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
