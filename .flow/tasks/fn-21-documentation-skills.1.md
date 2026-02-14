# fn-21-documentation-skills.1 Create documentation strategy and Mermaid skills

## Description
Create two documentation skills: `dotnet-documentation-strategy` (in `skills/documentation/`) and `dotnet-mermaid-diagrams` (in `skills/documentation/`). Each skill needs `name` and `description` frontmatter, comprehensive content with code examples, out-of-scope boundary statements, and cross-references. This task is parallelizable with fn-21.2 (file-disjoint).

**`dotnet-documentation-strategy`** covers:
- Decision tree for choosing documentation tooling based on project context (library vs app, team size, existing ecosystem)
- Starlight (Astro-based): modern default recommendation, Markdown + MDX, built-in search, i18n, versioning, Mermaid support
- Docusaurus (React-based): feature-rich alternative, plugin ecosystem, versioned docs, blog integration, MDX support
- DocFX (community-maintained): .NET-native, XML doc integration, API reference generation, migration note (MS dropped support Nov 2022)
- MarkdownSnippets: `dotnet tool` for including verified code snippets from source files into docs (avoids stale examples)
- Mermaid rendering support across all three platforms (native in GitHub, Starlight, Docusaurus; plugin in DocFX)
- Migration paths between tools (DocFX -> Starlight, Docusaurus -> Starlight)
- Does NOT re-teach CI deployment of doc sites (cross-ref `[skill:dotnet-gha-deploy]`)
- Does NOT re-teach API doc generation specifics (cross-ref `[skill:dotnet-api-docs]`)

**`dotnet-mermaid-diagrams`** covers:
- Architecture diagrams: C4-style context/container/component, layered architecture, microservice topology
- Sequence diagrams: API request flows, async/await patterns, middleware pipeline, authentication flows
- Class diagrams: domain models, DI registration graphs, inheritance hierarchies, interface implementations
- Deployment diagrams: container deployment, Kubernetes pod layout, CI/CD pipeline flow
- ER diagrams: EF Core model relationships, database schema visualization
- State diagrams: workflow states (order processing, saga patterns), state machine patterns
- Flowcharts: decision trees (framework selection, architecture choices)
- Diagram-as-code conventions: naming, grouping, GitHub rendering tips, dark mode considerations
- Does NOT re-teach GitHub-native doc structure (cross-ref `[skill:dotnet-github-docs]`)

**Files created:**
- `skills/documentation/dotnet-documentation-strategy/SKILL.md`
- `skills/documentation/dotnet-mermaid-diagrams/SKILL.md`

**Files NOT modified:** `plugin.json`, `dotnet-advisor/SKILL.md` (handled by fn-21.3)

## Acceptance
- [ ] `skills/documentation/dotnet-documentation-strategy/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-documentation-strategy` covers Starlight (modern default), Docusaurus (React), DocFX (legacy .NET) with decision tree
- [ ] `dotnet-documentation-strategy` covers MarkdownSnippets for code inclusion
- [ ] `dotnet-documentation-strategy` covers migration paths between doc tools
- [ ] `dotnet-documentation-strategy` cross-refs `[skill:dotnet-gha-deploy]` for deployment pipeline without re-teaching CI YAML
- [ ] `dotnet-documentation-strategy` cross-refs `[skill:dotnet-api-docs]` with scope boundary for API docs
- [ ] `dotnet-documentation-strategy` contains out-of-scope boundary statement
- [ ] `skills/documentation/dotnet-mermaid-diagrams/SKILL.md` exists with `name` and `description` frontmatter
- [ ] `dotnet-mermaid-diagrams` covers architecture, sequence, class, deployment, ER, state, and flowchart diagram types
- [ ] `dotnet-mermaid-diagrams` includes actual Mermaid code examples for each diagram type with .NET-specific content
- [ ] `dotnet-mermaid-diagrams` covers diagram-as-code conventions (naming, GitHub rendering, dark mode)
- [ ] `dotnet-mermaid-diagrams` cross-refs `[skill:dotnet-github-docs]` for GitHub doc context
- [ ] `dotnet-mermaid-diagrams` contains out-of-scope boundary statement
- [ ] Description frontmatter < 120 chars per skill

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
