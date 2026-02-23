---
name: dotnet-mermaid-diagrams
description: Creates Mermaid diagrams for .NET. Architecture, sequence, class, deployment, ER, flowcharts.
license: MIT
user-invocable: false
---

# dotnet-mermaid-diagrams

Mermaid diagram reference for .NET projects: architecture diagrams (C4-style context, container, component views, layered architecture, microservice topology), sequence diagrams (API request flows, async/await patterns, middleware pipeline, authentication flows), class diagrams (domain models, DI registration graphs, inheritance hierarchies, interface implementations), deployment diagrams (container deployment, Kubernetes pod layout, CI/CD pipeline flow), ER diagrams (EF Core model relationships, database schema visualization), state diagrams (workflow states, order processing, saga patterns, state machine patterns), and flowcharts (decision trees, framework selection, architecture choices). Includes diagram-as-code conventions for naming, grouping, GitHub rendering, and dark mode considerations.

**Version assumptions:** Mermaid v10+ (supported by GitHub, Starlight, Docusaurus natively). GitHub renders Mermaid in Markdown files, issues, PRs, and discussions. .NET 8.0+ baseline for code examples.

For complete diagram examples, see `examples.md` in this skill directory.

## Scope

- Architecture diagrams (C4-style, layered, microservice topology)
- Sequence diagrams (API flows, async/await, middleware pipeline)
- Class diagrams (domain models, DI graphs, inheritance)
- Deployment diagrams (containers, Kubernetes, CI/CD flow)
- ER diagrams (EF Core models, database schema)
- Diagram-as-code conventions (naming, grouping, dark mode)

## Out of scope

- Documentation platform configuration for Mermaid rendering -- see [skill:dotnet-documentation-strategy]
- GitHub-native doc structure and README patterns -- see [skill:dotnet-github-docs]
- CI/CD pipeline deployment of doc sites -- see [skill:dotnet-gha-deploy]

Cross-references: [skill:dotnet-documentation-strategy] for Mermaid rendering setup across doc platforms, [skill:dotnet-github-docs] for embedding diagrams in GitHub-native docs, [skill:dotnet-gha-deploy] for doc site deployment.

---

## Supported Diagram Types

### Architecture Diagrams

- **C4-Style Context** -- system in its environment with external actors (10-12 nodes max)
- **C4-Style Container** -- high-level technology choices and interactions (15-20 nodes max)
- **C4-Style Component** -- internal structure of a single service (15-20 nodes max)
- **Layered Architecture** -- Presentation, Application, Domain, Infrastructure layers
- **Microservice Topology** -- services, messaging, observability connections

### Sequence Diagrams

- **API Request Flow** -- HTTP request through middleware, auth, controller, service, database
- **Async/Await Pattern** -- thread pool behavior, cache miss/hit, await points
- **Middleware Pipeline** -- request/response flow through ASP.NET Core middleware chain
- **Authentication Flow** -- OAuth 2.0/OIDC with BFF pattern

### Class Diagrams

- **Domain Model** -- entities, value objects, enumerations, relationships
- **DI Registration Graph** -- singleton/scoped/transient lifetime visualization
- **Interface Implementation Hierarchy** -- generic repository pattern with inheritance

### Deployment Diagrams

- **Container Deployment** -- Docker host with app, database, cache, reverse proxy
- **Kubernetes Pod Layout** -- cluster, namespace, deployments, services, config
- **CI/CD Pipeline Flow** -- build, test, package, deploy stages

### ER Diagrams

- **EF Core Relationship Visualization** -- one-to-many, one-to-one, many-to-many with entity details
- **Database Schema with Indexes** -- audit logs, soft delete, multi-tenant patterns

### State Diagrams

- **Order Processing Workflow** -- draft through delivery with payment states
- **Saga Pattern** -- distributed transaction with compensation steps
- **State Machine Pattern** -- MassTransit-style event-driven state transitions

### Flowcharts

- **Framework Selection Decision Tree** -- web vs desktop, API vs UI, framework choices
- **Architecture Decision Flowchart** -- monolith vs microservices, communication patterns

---

## Diagram-as-Code Conventions

### Naming Conventions

- Use PascalCase for node IDs: `OrderService`, `CustomerDB`
- Use descriptive labels with technology: `API["Order API<br/>(ASP.NET Core)"]`
- Use consistent abbreviations: DB (database), API (endpoint), SVC (service), MQ (message queue)
- Prefix subgraphs with the layer or tier name: `subgraph DataTier["Data Tier"]`

### Grouping Patterns

- Group by architectural layer (Presentation, Application, Domain, Infrastructure)
- Group by deployment boundary (containers, pods, VMs)
- Group by team ownership in microservice diagrams
- Use subgraphs for visual grouping -- limit nesting to 2 levels for readability

### GitHub Rendering Tips

- GitHub renders Mermaid in fenced code blocks with the `mermaid` language identifier in Markdown files, issues, PRs, and discussions
- Maximum recommended diagram size: ~50 nodes for readable rendering
- GitHub uses a light theme by default -- avoid light-colored fill that disappears on white backgrounds
- Diagrams auto-size to container width -- keep node labels concise (under 30 characters per line)
- Use `<br/>` for line breaks within node labels (not `\n`)
- Test diagrams in GitHub before merging -- syntax errors render as raw text

### Dark Mode Considerations

- Avoid hardcoded colors that fail in dark mode -- use Mermaid theme variables when possible
- Default Mermaid colors work in both light and dark themes on GitHub
- If using custom `style` directives, test in both GitHub light and dark modes
- Prefer semantic `classDef` styles over inline `style` for maintainability
- The `neutral` theme (`%%{init: {'theme': 'neutral'}}%%`) provides the best cross-theme compatibility on GitHub

### Diagram Size Guidelines

| Diagram Type | Recommended Max Nodes | Notes |
|---|---|---|
| C4 Context | 10-12 | One system + external actors |
| C4 Container | 15-20 | Internal containers + data stores |
| C4 Component | 15-20 | Single service internals |
| Sequence | 8 participants | More becomes unreadable |
| Class | 10-15 classes | Split into multiple diagrams |
| ER | 10-12 entities | Split by bounded context |
| State | 12-15 states | Split complex workflows |
| Flowchart | 15-20 nodes | Keep decision trees focused |

---

## Agent Gotchas

1. **Always use `.NET-specific content` in diagrams** -- do not generate generic diagrams. Use real .NET types (DbContext, IRepository, MediatR), real .NET tools (EF Core, MassTransit, YARP), and real .NET patterns (middleware pipeline, DI registration).

2. **Keep diagrams under 50 nodes** -- larger diagrams render poorly on GitHub and doc sites. Split complex architectures into multiple focused diagrams (context, container, component) rather than one monolithic diagram.

3. **Use `<br/>` for line breaks in node labels, not `\n`** -- Mermaid renders `\n` literally as text. Multi-line labels require `<br/>` HTML tags.

4. **Test Mermaid syntax before committing** -- syntax errors cause GitHub to render raw text instead of a diagram. Use the Mermaid Live Editor (https://mermaid.live) or a local preview tool to validate.

5. **ER diagram relationship notation follows Mermaid syntax, not UML** -- use `||--o{` for one-to-many, `||--||` for one-to-one. Do not use UML multiplicity notation.

6. **Use the `neutral` theme for GitHub compatibility** -- `%%{init: {'theme': 'neutral'}}%%` provides the best rendering in both light and dark modes.

7. **Sequence diagram participant names cannot contain special characters** -- use `participant DB as "SQL Server"` alias syntax for names with spaces or special characters.

8. **Nested generics (`Task~List~T~~`) may not render on all Mermaid versions** -- the double `~~` at the end of nested generic types requires Mermaid v10.3+. Test rendering in your target environment before committing complex generic type diagrams.

9. **Do not use Font Awesome icon syntax (`fa:fa-user`) in diagrams intended for GitHub** -- GitHub's native Mermaid renderer does not load Font Awesome CSS. Icons render as literal text. Use plain text labels instead.

10. **Do not configure Mermaid rendering in doc platforms** -- platform setup (Starlight remark plugin, Docusaurus theme, DocFX template) belongs to [skill:dotnet-documentation-strategy]. This skill provides the diagram content only.
