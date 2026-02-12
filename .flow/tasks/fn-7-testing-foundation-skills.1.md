# fn-7-testing-foundation-skills.1 Core testing skills: strategy, xUnit, integration

## Description
Create three foundational testing skills that form the base of the testing category.

**Skills delivered:**
- `skills/testing/dotnet-testing-strategy/SKILL.md` -- Decision tree for unit vs integration vs E2E, test organization, naming conventions, mock/fake/stub guidance
- `skills/testing/dotnet-xunit/SKILL.md` -- xUnit v3 features (Fact/Theory, fixtures, parallelism, IAsyncLifetime, analyzers) with v2 compatibility notes
- `skills/testing/dotnet-integration-testing/SKILL.md` -- WebApplicationFactory, Testcontainers, Aspire testing, database fixtures, test isolation

**File ownership:** This task exclusively owns `skills/testing/dotnet-testing-strategy/`, `skills/testing/dotnet-xunit/`, and `skills/testing/dotnet-integration-testing/`. No other task creates or modifies these directories. This task does NOT modify `plugin.json` (Task 4 handles registration).

## Acceptance
- [ ] Three SKILL.md files created with required frontmatter (`name`, `description`)
- [ ] Each skill has: scope boundary, prerequisites, cross-references per matrix, >=2 code examples, gotchas section, references
- [ ] Testing strategy includes unit/integration/E2E decision tree with concrete criteria
- [ ] xUnit skill covers v3 features with v2 compatibility notes where behavior differs
- [ ] Integration testing documents WebApplicationFactory + Testcontainers + Aspire patterns
- [ ] Version assumptions stated: xUnit v3 primary (v2 compat notes), Testcontainers 3.x+, .NET 8.0+ baseline
- [ ] Cross-references match the epic cross-reference matrix
- [ ] No overlap with `dotnet-add-testing` (scaffolding) -- reference it, do not duplicate
- [ ] Skill content complete and ready for registration by Task 4

## Done summary
Created three foundational testing skills: dotnet-testing-strategy (unit/integration/E2E decision tree, naming conventions, mock/fake/stub guidance), dotnet-xunit (xUnit v3 features with v2 compatibility notes), and dotnet-integration-testing (WebApplicationFactory, Testcontainers, Aspire testing, database fixtures, test isolation).
## Evidence
- Commits: cb5e14a, 5b9f000, 53ba45f
- Tests: grep cross-reference validation, frontmatter validation
- PRs: