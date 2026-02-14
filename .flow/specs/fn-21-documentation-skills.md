# fn-21: Documentation Skills

## Overview
Delivers comprehensive documentation skills covering modern tooling recommendation (Starlight vs Docusaurus vs DocFX), Mermaid diagrams for .NET architecture visualization, GitHub-native documentation (README, CONTRIBUTING, templates), XML documentation comments, and API documentation generation. Enables the `dotnet-docs-generator` agent for automated documentation workflows. These skills complement the CI/CD doc deployment capabilities already delivered in fn-19 (`[skill:dotnet-gha-deploy]`).

## Scope
**Skills (5 total):**
- `dotnet-documentation-strategy` — Documentation tooling recommendation: Starlight (Astro-based, modern default), Docusaurus (feature-rich, React-based), DocFX (community-maintained since MS dropped support Nov 2022), MarkdownSnippets for code inclusion, Mermaid support across all platforms, project context-driven recommendation, migration paths between tools
- `dotnet-mermaid-diagrams` — Mermaid diagram reference for .NET: architecture diagrams (C4-style, layer, microservice), sequence diagrams (API flows, async patterns, middleware pipelines), class diagrams (domain models, DI graphs), deployment diagrams (container, Kubernetes), ER diagrams (EF Core models), state diagrams (workflow, saga patterns), diagram-as-code conventions and GitHub rendering
- `dotnet-github-docs` — GitHub-native documentation: README structure and badges for .NET projects, CONTRIBUTING.md with PR process and skill authoring guides, issue/PR templates (bug reports, feature requests), GitHub Pages setup for doc sites, GitHub wiki patterns, repository metadata and social preview
- `dotnet-xml-docs` — XML documentation comments: `<summary>`, `<param>`, `<returns>`, `<exception>`, `<inheritdoc>`, `<see>`/`<seealso>` best practices; enabling `GenerateDocumentationFile`; suppressing warnings for internal APIs; XML doc conventions for public libraries; auto-generation tools; integration with IntelliSense and API doc generation
- `dotnet-api-docs` — API documentation generation: DocFX setup for .NET API reference, OpenAPI spec as documentation (cross-ref `[skill:dotnet-openapi]`), doc site generation from XML comments, keeping docs in sync with code, API changelog patterns, versioned API documentation

**Agents (1 total):**
- `dotnet-docs-generator` — Documentation generation agent that analyzes project structure, recommends documentation tooling, generates Mermaid architecture diagrams, writes XML doc comment skeletons, and scaffolds GitHub-native docs (README, CONTRIBUTING, templates)

**Naming convention:** All skills use `dotnet-` prefix. Noun style for reference skills.

## Dependencies

**Hard epic dependencies:**
- fn-19 (CI/CD): `[skill:dotnet-gha-deploy]` must exist for doc deployment cross-refs in documentation strategy (already shipped)

**Soft epic dependencies:**
- fn-11 (API Development): `[skill:dotnet-openapi]` for OpenAPI as documentation cross-ref (already shipped)
- fn-3 (Core C#): `[skill:dotnet-csharp-coding-standards]` for XML doc comment conventions (already shipped)
- fn-20 (Packaging): `[skill:dotnet-release-management]` for changelog format cross-ref (already shipped)
- fn-4 (Project Structure): `[skill:dotnet-project-structure]` for project metadata used in README generation (already shipped)

**Downstream dependents:**
- fn-25 (Community Setup): depends on fn-21 for README references to documentation tooling

## .NET Version Policy

**Baseline:** .NET 8.0+ (LTS)

| Component | Version | Notes |
|-----------|---------|-------|
| XML doc comments | All .NET | Language feature, not version-specific |
| GenerateDocumentationFile | .NET SDK 6+ | MSBuild property |
| DocFX | v2.x (community) | Community-maintained; works with .NET 8+ |
| Starlight | v0.x+ | Astro-based, framework-agnostic |
| Docusaurus | v3.x | React-based, framework-agnostic |
| MarkdownSnippets | .NET 8+ | dotnet tool for code snippet inclusion |
| Mermaid | v10+ | Rendered by GitHub, Starlight, Docusaurus natively |
| OpenAPI doc generation | .NET 9+ | Microsoft.AspNetCore.OpenApi built-in |

## Conventions

- **Frontmatter:** Required fields are `name` and `description` only
- **Cross-reference syntax:** `[skill:skill-name]` for all skill references
- **Description budget:** Target < 120 characters per skill description
- **Out-of-scope format:** "**Out of scope:**" paragraph with epic ownership attribution
- **Code examples:** Real .NET code, Mermaid diagrams, YAML/Markdown where appropriate
- **Doc tool bias:** Recommend Starlight as modern default, DocFX for existing .NET projects with XML docs, Docusaurus for teams already invested in React ecosystem

## Scope Boundaries

| Concern | fn-21 owns | Other epic owns | Enforcement |
|---------|-----------|-----------------|-------------|
| Doc site deployment | Documentation tooling setup and configuration | fn-19: `dotnet-gha-deploy` (CI pipeline for GitHub Pages, DocFX deployment) | Cross-ref `[skill:dotnet-gha-deploy]`; no re-teach CI YAML |
| OpenAPI specs | API docs referencing OpenAPI output as documentation | fn-11: `dotnet-openapi` (OpenAPI generation, Swashbuckle migration) | Cross-ref `[skill:dotnet-openapi]`; no re-teach OpenAPI config |
| Code standards | XML doc comment best practices | fn-3: `dotnet-csharp-coding-standards` (naming, conventions) | Cross-ref `[skill:dotnet-csharp-coding-standards]`; no re-teach general conventions |
| Changelog format | API changelog patterns in `dotnet-api-docs` | fn-20: `dotnet-release-management` (NBGV, SemVer, changelog generation) | Cross-ref `[skill:dotnet-release-management]`; no re-teach changelog tools |
| README/CONTRIBUTING content | Template structure and best practices for .NET repos | fn-25: `dotnet-community-setup` (actual README/CONTRIBUTING for dotnet-artisan) | fn-21 teaches the patterns; fn-25 applies them to this repo |

## Cross-Reference Classification

| Target Skill | Type | Used By | Notes |
|---|---|---|---|
| `[skill:dotnet-gha-deploy]` | Hard | `dotnet-documentation-strategy`, `dotnet-github-docs`, `dotnet-api-docs` | Doc deployment pipeline |
| `[skill:dotnet-openapi]` | Soft | `dotnet-api-docs` | OpenAPI as API documentation |
| `[skill:dotnet-csharp-coding-standards]` | Soft | `dotnet-xml-docs` | General coding conventions context |
| `[skill:dotnet-release-management]` | Soft | `dotnet-github-docs`, `dotnet-api-docs` | Changelog format |
| `[skill:dotnet-project-structure]` | Soft | `dotnet-github-docs` | Project metadata for README |
| `[skill:dotnet-xml-docs]` | Internal | `dotnet-api-docs`, `dotnet-docs-generator` agent | XML comments feed API doc generation |
| `[skill:dotnet-mermaid-diagrams]` | Internal | `dotnet-github-docs`, `dotnet-docs-generator` agent | Diagrams in READMEs and doc sites |
| `[skill:dotnet-documentation-strategy]` | Internal | `dotnet-docs-generator` agent | Tooling recommendation |

## Task Decomposition

### fn-21.1: Create documentation strategy and Mermaid skills — parallelizable with fn-21.2
**Delivers:** `dotnet-documentation-strategy`, `dotnet-mermaid-diagrams`
- `skills/documentation/dotnet-documentation-strategy/SKILL.md`
- `skills/documentation/dotnet-mermaid-diagrams/SKILL.md`
- All require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-gha-deploy]` (fn-19) for doc site deployment pipeline
  - `[skill:dotnet-api-docs]` (fn-21, internal) scope boundary for API doc generation
  - `[skill:dotnet-github-docs]` (fn-21, internal) for Mermaid in READMEs
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-21.3)

### fn-21.2: Create GitHub docs, XML docs, and API docs skills — parallelizable with fn-21.1
**Delivers:** `dotnet-github-docs`, `dotnet-xml-docs`, `dotnet-api-docs`
- `skills/documentation/dotnet-github-docs/SKILL.md`
- `skills/documentation/dotnet-xml-docs/SKILL.md`
- `skills/documentation/dotnet-api-docs/SKILL.md`
- All require `name` and `description` frontmatter
- Cross-references:
  - `[skill:dotnet-gha-deploy]` (fn-19) for doc deployment and GitHub Pages
  - `[skill:dotnet-openapi]` (fn-11) for OpenAPI as API documentation
  - `[skill:dotnet-csharp-coding-standards]` (fn-3) for XML doc coding conventions
  - `[skill:dotnet-release-management]` (fn-20) for changelog format
  - `[skill:dotnet-project-structure]` (fn-4) for project metadata in README
  - `[skill:dotnet-xml-docs]` (fn-21, internal) for XML comments feeding API docs
  - `[skill:dotnet-mermaid-diagrams]` (fn-21, internal) for diagrams in GitHub docs
- Each skill must contain out-of-scope boundary statements
- Does NOT modify `plugin.json` or `dotnet-advisor/SKILL.md` (handled by fn-21.3)

### fn-21.3: Integration — plugin registration, advisor catalog, agent creation, validation (depends on fn-21.1, fn-21.2)
**Delivers:** Plugin registration, advisor update, `dotnet-docs-generator` agent, validation
- Registers all 5 skill paths in `.claude-plugin/plugin.json` under `skills` array
- Registers `agents/dotnet-docs-generator.md` in `.claude-plugin/plugin.json` under `agents` array
- Updates `skills/foundation/dotnet-advisor/SKILL.md` section 18 (Documentation) from `planned` to `implemented`
- Creates `agents/dotnet-docs-generator.md` agent file with:
  - Preloaded skills: `[skill:dotnet-documentation-strategy]`, `[skill:dotnet-mermaid-diagrams]`, `[skill:dotnet-xml-docs]`
  - Tools: Read, Grep, Glob, Bash, Edit, Write (needs write access for doc generation)
  - Workflow: analyze project -> recommend tooling -> generate diagrams -> write XML doc skeletons -> scaffold GitHub docs
  - Explicit boundaries: does NOT own CI deployment, does NOT own OpenAPI generation
- Runs repo-wide skill name uniqueness check
- Runs `./scripts/validate-skills.sh`
- Validates cross-references present in all 5 skills
- Single owner of `plugin.json` — eliminates merge conflicts

**Execution order:** fn-21.1 and fn-21.2 are parallelizable (file-disjoint, no shared file edits). fn-21.3 depends on both fn-21.1 and fn-21.2.

## Key Context
- Mermaid diagrams preferred over other diagram tools (GitHub renders natively, all major doc tools support)
- DocFX is community-maintained (Microsoft dropped official support November 2022); still widely used in .NET ecosystem
- Starlight (Astro-based) + MarkdownSnippets is the modern recommendation for new doc sites
- Docusaurus remains a strong choice for teams already in React ecosystem
- `dotnet-gha-deploy` (fn-19) already has complete GitHub Pages + DocFX deployment YAML — fn-21 should not re-teach CI config
- `dotnet-openapi` (fn-11) already covers OpenAPI generation — fn-21 focuses on using OpenAPI output as documentation
- No `<!-- TODO(fn-21) -->` placeholders exist in any shipped skills (cross-reference reconciliation will be minimal)
- fn-25 (Community Setup) depends on fn-21 for documentation patterns that will be applied to the dotnet-artisan repo itself

## Quick Commands
```bash
# Validate all 5 skills exist with frontmatter
for s in dotnet-documentation-strategy dotnet-mermaid-diagrams dotnet-github-docs \
         dotnet-xml-docs dotnet-api-docs; do
  test -f "skills/documentation/$s/SKILL.md" && \
  grep -q "^name:" "skills/documentation/$s/SKILL.md" && \
  grep -q "^description:" "skills/documentation/$s/SKILL.md" && \
  echo "OK: $s" || echo "MISSING: $s"
done

# Repo-wide skill name uniqueness
grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d  # expect empty

# Verify scope boundary statements in all 5 skills
grep -l "Out of scope\|out of scope\|Scope boundary" skills/documentation/*/SKILL.md | wc -l  # expect 5

# Verify cross-references
grep -r "\[skill:dotnet-gha-deploy\]" skills/documentation/
grep -r "\[skill:dotnet-openapi\]" skills/documentation/
grep -r "\[skill:dotnet-release-management\]" skills/documentation/

# Verify plugin.json registration (after fn-21.3)
for s in dotnet-documentation-strategy dotnet-mermaid-diagrams dotnet-github-docs \
         dotnet-xml-docs dotnet-api-docs; do
  grep -q "skills/documentation/$s" .claude-plugin/plugin.json && echo "OK: $s" || echo "MISSING: $s"
done

# Verify agent registration (after fn-21.3)
grep -q "agents/dotnet-docs-generator.md" .claude-plugin/plugin.json && echo "OK: agent" || echo "MISSING: agent"

# Verify advisor section 18 updated (after fn-21.3)
grep "### 18. Documentation" skills/foundation/dotnet-advisor/SKILL.md | grep -v "planned"

# Canonical validation
./scripts/validate-skills.sh
```

## Acceptance Criteria
1. All 5 skills exist at `skills/documentation/<skill-name>/SKILL.md` with `name` and `description` frontmatter
2. `dotnet-documentation-strategy` recommends Starlight (modern default), Docusaurus (React ecosystem), DocFX (legacy .NET), with project-context-driven decision tree, and covers MarkdownSnippets for code inclusion
3. `dotnet-mermaid-diagrams` covers architecture diagrams (C4-style, layers, microservices), sequence diagrams (API flows, async), class diagrams (domain models), deployment diagrams, ER diagrams (EF Core), and state diagrams for .NET patterns
4. `dotnet-github-docs` covers README structure with .NET badges, CONTRIBUTING.md patterns, issue/PR templates, GitHub Pages setup, and repository metadata
5. `dotnet-xml-docs` covers all standard XML doc tags, `GenerateDocumentationFile` MSBuild property, `<inheritdoc>`, warning suppression for internal APIs, and integration with IntelliSense
6. `dotnet-api-docs` covers DocFX setup for API reference, OpenAPI-as-documentation pattern, doc-code sync strategies, API changelogs, and versioned API docs
7. `dotnet-documentation-strategy` cross-references `[skill:dotnet-gha-deploy]` for deployment pipeline — does not re-teach CI YAML
8. `dotnet-api-docs` cross-references `[skill:dotnet-openapi]` for OpenAPI generation — does not re-teach OpenAPI config
9. `dotnet-xml-docs` cross-references `[skill:dotnet-csharp-coding-standards]` for general conventions context
10. Each skill contains explicit out-of-scope boundary statements for related epics
11. `dotnet-docs-generator` agent exists at `agents/dotnet-docs-generator.md` with proper frontmatter, preloaded skills, workflow, and explicit boundaries
12. All 5 skills registered in `.claude-plugin/plugin.json` (fn-21.3)
13. Agent registered in `.claude-plugin/plugin.json` under `agents` (fn-21.3)
14. `skills/foundation/dotnet-advisor/SKILL.md` section 18 updated from `planned` to `implemented` (fn-21.3)
15. `./scripts/validate-skills.sh` passes for all 5 skills
16. Skill `name` frontmatter values are unique repo-wide (no duplicates)
17. fn-21.1 and fn-21.2 are fully parallelizable (file-disjoint, no shared file edits)
18. fn-21.3 depends on fn-21.1 + fn-21.2 and is the single owner of `plugin.json`

## Test Notes
- Verify documentation strategy skill includes decision tree with project context (library vs app, team size, existing tooling)
- Verify Mermaid diagrams skill includes actual Mermaid code examples for each diagram type
- Verify GitHub docs skill includes actual template examples (issue templates, PR templates)
- Verify XML docs skill includes C# code examples with comprehensive XML doc comments
- Verify API docs skill includes DocFX configuration example (`docfx.json`)
- Verify scope boundary statements clearly differentiate fn-21 from fn-19 (CI deployment), fn-11 (OpenAPI), fn-3 (coding standards)
- Run `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` to confirm no duplicate names repo-wide

## References
- Starlight: https://starlight.astro.build/
- Docusaurus: https://docusaurus.io/
- DocFX: https://dotnet.github.io/docfx/
- MarkdownSnippets: https://github.com/SimonCropp/MarkdownSnippets
- Mermaid: https://mermaid.js.org/
- GitHub Pages: https://docs.github.com/en/pages
- XML Documentation Comments: https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/
- DocFX community maintenance: https://github.com/dotnet/docfx (transferred from Microsoft)
