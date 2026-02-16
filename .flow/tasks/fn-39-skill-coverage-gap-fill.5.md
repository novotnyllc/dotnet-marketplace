# fn-39-skill-coverage-gap-fill.5 Create dotnet-aspire-patterns and dotnet-semantic-kernel skills

## Description
Create 2 new skills covering cloud orchestration and AI integration gaps:

1. **dotnet-aspire-patterns** (`skills/architecture/dotnet-aspire-patterns/SKILL.md`) — .NET Aspire orchestration patterns: AppHost configuration, service discovery, component model, health checks, distributed tracing integration, local development with dashboard, Aspire vs manual container orchestration, when to use Aspire.
2. **dotnet-semantic-kernel** (`skills/ai/dotnet-semantic-kernel/SKILL.md`) — Microsoft Semantic Kernel for AI/LLM orchestration in .NET: kernel setup, plugin/function calling, prompt templates, memory/vector stores, planners, agents, integration with Azure OpenAI and local models. Placed under `skills/ai/` as a domain-specific AI capability distinct from architecture patterns.

**Size:** M
**Files:** `skills/architecture/dotnet-aspire-patterns/SKILL.md`, `skills/ai/dotnet-semantic-kernel/SKILL.md`

## Approach
- Follow existing SKILL.md frontmatter pattern (name, description only)
- Each description under 120 characters (target ~100 chars for budget headroom)
- dotnet-aspire-patterns cross-refs: `[skill:dotnet-containers]`, `[skill:dotnet-observability]`, `[skill:dotnet-csharp-dependency-injection]`, `[skill:dotnet-background-services]`
- dotnet-semantic-kernel cross-refs: `[skill:dotnet-csharp-async-patterns]`, `[skill:dotnet-csharp-dependency-injection]`
- Create the `skills/ai/` category directory for dotnet-semantic-kernel
- Use latest stable package versions (Aspire 9.x, Semantic Kernel 1.x)
- No fn-N spec references
- Aspire skill is distinct from existing container skills (those cover Docker/K8s directly, Aspire covers the orchestration abstraction)
## Acceptance
- [ ] dotnet-aspire-patterns SKILL.md created with frontmatter
- [ ] Covers AppHost, service discovery, component model, dashboard, health checks
- [ ] Distinct from dotnet-containers (orchestration abstraction vs raw Docker/K8s)
- [ ] dotnet-semantic-kernel SKILL.md created with frontmatter
- [ ] Covers kernel setup, plugins, prompt templates, memory stores, agents
- [ ] Placed under `skills/ai/` category (new directory created)
- [ ] All cross-references use `[skill:...]` syntax
- [ ] All descriptions under 120 characters
- [ ] All SKILL.md files under 5,000 words
- [ ] Latest stable package versions
- [ ] No fn-N spec references
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
