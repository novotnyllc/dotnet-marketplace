# fn-21: Documentation Skills

## Problem/Goal
Add comprehensive documentation skills covering modern tooling recommendation (Starlight vs Docusaurus vs DocFX), Mermaid diagrams, GitHub-native docs, XML docs, and API documentation generation. Enable dotnet-docs-generator agent.

## Acceptance Checks
- [ ] `dotnet-documentation-strategy` skill recommends tooling based on project context (Starlight modern, Docusaurus feature-rich, DocFX legacy)
- [ ] `dotnet-mermaid-diagrams` skill provides dedicated Mermaid reference for .NET projects (architecture, sequence, class, deployment diagrams)
- [ ] `dotnet-github-docs` skill covers GitHub-native documentation (README, CONTRIBUTING, templates, GitHub Pages)
- [ ] `dotnet-xml-docs` skill covers XML doc comments best practices, auto-generation, integration
- [ ] `dotnet-api-docs` skill covers API doc generation (OpenAPI specs, doc site generation, keeping in sync)
- [ ] `dotnet-docs-generator` agent generates documentation with Mermaid diagrams
- [ ] Cross-references to CI/CD for doc deployment

## Key Context
- Mermaid diagrams preferred over other diagram tools
- DocFX is community-maintained (MS dropped official support Nov 2022)
- Starlight + MarkdownSnippets is modern choice
- All modern tools support Mermaid
