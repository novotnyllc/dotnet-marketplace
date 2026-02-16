# fn-38-expert-domain-agents-and-luminary.4 Create testing, cloud/Aspire, and code review specialist agents

## Description
Create 3 additional domain-named specialist agents to cover the remaining agent gaps:

1. **dotnet-testing-specialist** — Test architecture and strategy agent. Covers test pyramid design, E2E test architecture, test data management, microservice testing strategies, when to use integration vs unit vs E2E. Preloads: `dotnet-testing-strategy`, `dotnet-xunit`, `dotnet-integration-testing`, `dotnet-snapshot-testing`, `dotnet-playwright`.
2. **dotnet-cloud-specialist** — Cloud deployment and .NET Aspire orchestration agent. Covers AKS/Azure deployment, GitHub Actions multi-stage pipelines, Aspire service discovery, distributed tracing, infrastructure-as-code for .NET apps. Preloads: `dotnet-containers`, `dotnet-container-deployment`, `dotnet-observability`, `dotnet-ado-patterns`.
3. **dotnet-code-review-agent** — General code review agent combining performance, security, architecture, and correctness review. Routes to specialist agents for deep dives. Preloads: a broad set of core skills. Triggers on: "review this", "code review", "PR review", "what's wrong with this code".

**Size:** M
**Files:** `agents/dotnet-testing-specialist.md`, `agents/dotnet-cloud-specialist.md`, `agents/dotnet-code-review-agent.md`, `.claude-plugin/plugin.json`

## Approach
- Follow agent frontmatter pattern from `agents/dotnet-csharp-concurrency-specialist.md`
- All agents domain-named, NOT person-named
- Each agent < 3,000 tokens, with focused scope and explicit boundaries
- Include "Does NOT" boundary sections to prevent overlap with existing agents
- Testing specialist: does NOT handle performance benchmarking (use benchmark-designer), does NOT handle security auditing (use security-reviewer)
- Cloud specialist: does NOT handle general architecture (use architect), does NOT handle container image optimization (covered in container skills)
- Code review agent: triages and routes to specialists, does NOT replace specialized reviewers for deep domain analysis
- Register all in `.claude-plugin/plugin.json` agents array
## Acceptance
- [ ] dotnet-testing-specialist agent created with frontmatter and decision tree
- [ ] dotnet-cloud-specialist agent created with frontmatter and decision tree
- [ ] dotnet-code-review-agent created with frontmatter and triage workflow
- [ ] All 3 agents have explicit "Does NOT" boundary sections
- [ ] All 3 agents under 3,000 tokens each
- [ ] All 3 registered in `.claude-plugin/plugin.json` agents array
- [ ] No overlap with existing agents (concurrency, performance, security, Blazor, Uno, MAUI)
- [ ] All four validation commands pass
## Done summary
Created three specialist agents: dotnet-testing-specialist (test architecture and strategy), dotnet-cloud-specialist (.NET Aspire and cloud deployment), and dotnet-code-review-agent (multi-dimensional code review with triage routing). All agents include frontmatter, decision trees, explicit boundary sections, trigger lexicons, and are registered in plugin.json.
## Evidence
- Commits: 0b43289dfd764fcd010a8ba138ccad0d6f5bf641
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: