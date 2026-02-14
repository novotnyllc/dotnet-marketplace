# fn-25-community-setup-and-readme.2 Create CONTRIBUTING.md and CHANGELOG.md

## Description
Create `CONTRIBUTING.md` and `CHANGELOG.md` at the repo root. These files enable community contributions and document the project's release history.

### CONTRIBUTING.md

**Required sections:**
1. **Welcome / Overview** — Brief intro to contributing to dotnet-artisan, reference to Agent Skills open standard
2. **Prerequisites** — Python 3 (for validation scripts), `jq` (for marketplace validation). No .NET SDK required for the plugin repo itself.
3. **Skill Authoring Guide**:
   - SKILL.md frontmatter: required fields are `name` and `description` only
   - Cross-reference syntax: `[skill:skill-name]`
   - Description budget: target < 120 characters per skill description
   - Out-of-scope boundary: "**Out of scope:**" paragraph with epic ownership attribution
   - Directory convention: `skills/<category>/<skill-name>/SKILL.md`
   - Code examples: use real .NET code, Mermaid diagrams, YAML/Markdown where appropriate
4. **Agent Authoring** — Brief guide for contributing agents: frontmatter, preloaded skills, tool declarations, file location (`agents/<name>.md`)
5. **PR Process** — Fork → branch → implement → validate locally → submit PR
6. **Validation Requirements** — All 4 validation commands that must pass before merge:
   - `./scripts/validate-skills.sh` — Skill frontmatter and structure
   - `./scripts/validate-marketplace.sh` — Plugin/marketplace JSON consistency
   - `python3 scripts/generate_dist.py --strict` — Cross-agent dist generation
   - `python3 scripts/validate_cross_agent.py` — Cross-agent conformance checks
7. **Hooks & MCP** — Reference to `docs/hooks-and-mcp-guide.md` for hook/MCP contribution context
8. **Code of Conduct** — Brief statement or reference

### CHANGELOG.md

**Format:** Keep a Changelog (https://keepachangelog.com/) with SemVer versioning.

**Content:**
- Header with Keep a Changelog and SemVer references
- `## [0.1.0]` — Initial release (version MUST match `plugin.json` version field: 0.1.0)
- **Added** section listing major milestones:
  - Plugin skeleton and infrastructure (fn-2)
  - Core C# skills — 7 skills covering modern patterns, async, DI, configuration, source generators
  - Project structure skills — 6 skills for project setup, analyzers, CI, testing, modernization
  - Architecture skills — 10 skills for patterns, resilience, EF Core, containers
  - API development skills — 5 skills for minimal APIs, versioning, OpenAPI, security
  - Security skills — 3 skills for OWASP, secrets, cryptography
  - UI framework skills — 13 skills for Blazor, MAUI, Uno Platform, WinUI, WPF, WinForms
  - Testing skills — 10 skills for strategy, xUnit, integration, UI, Playwright, snapshots
  - Serialization & communication skills — 4 skills for gRPC, SignalR, serialization
  - Performance skills — 4 skills for benchmarking, profiling, CI benchmarking
  - Native AOT skills — 4 skills for AOT, trimming, WASM
  - CLI tools skills — 5 skills for System.CommandLine, architecture, distribution
  - CI/CD skills — 8 skills for GitHub Actions and Azure DevOps
  - Agent meta-skills — 4 skills for agent-specific .NET patterns
  - Packaging & publishing skills — 4 skills for NuGet, MSIX, GitHub Releases, release management
  - Documentation skills — 5 skills for doc strategy, Mermaid, GitHub docs, XML docs, API docs
  - Localization skill — 1 skill
  - 9 specialist agents for architecture, security, Blazor, Uno, MAUI, performance, benchmarks, concurrency, docs
  - Hooks for session start context and post-edit validation
  - MCP integration (Context7, Uno Platform, Microsoft Learn)
  - Cross-agent build pipeline for Claude/Copilot/Codex output
  - Foundation skills — advisor routing, version detection, project analysis, self-publish

**Files created:** `CONTRIBUTING.md`, `CHANGELOG.md`
**Files NOT modified:** `README.md`, `CLAUDE.md`, `AGENTS.md`, `plugin.json`

## Acceptance
- [ ] `CONTRIBUTING.md` exists at repo root
- [ ] Contains skill authoring guide with frontmatter requirements (`name`, `description`), cross-ref syntax, description budget
- [ ] Contains PR process (fork → branch → validate → submit)
- [ ] Lists all 4 validation commands: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py`, `validate_cross_agent.py`
- [ ] References Agent Skills open standard
- [ ] References `docs/hooks-and-mcp-guide.md` for hooks/MCP contribution
- [ ] Lists prerequisites (Python 3, jq)
- [ ] `CHANGELOG.md` exists at repo root
- [ ] Uses Keep a Changelog format with "Keep a Changelog" reference
- [ ] Initial release version is `[0.1.0]` (matches plugin.json)
- [ ] Added section covers all major skill categories and agent/hook/MCP milestones
- [ ] Quick commands pass:
  ```bash
  for cmd in "validate-skills" "validate-marketplace" "generate_dist" "validate_cross_agent"; do
    grep -q "$cmd" CONTRIBUTING.md
  done
  grep -q "Keep a Changelog" CHANGELOG.md
  grep -q "\[0.1.0\]" CHANGELOG.md
  grep -qi "Agent Skills" CONTRIBUTING.md
  ```

## Done summary
Created CONTRIBUTING.md with skill authoring guide (frontmatter requirements, cross-reference syntax, description budget), agent authoring guide, PR process, all 4 validation commands, hooks/MCP reference, and prerequisites. Created CHANGELOG.md in Keep a Changelog format with v0.1.0 initial release documenting all 97 skills across 18 categories, 9 agents, hooks, MCP integrations, and cross-agent build pipeline.
## Evidence
- Commits: da26c8fafa119e84961bf36f092b02f76edb8972
- Tests: grep validation commands in CONTRIBUTING.md, grep Keep a Changelog in CHANGELOG.md, grep version 0.1.0 in CHANGELOG.md, grep Agent Skills in CONTRIBUTING.md
- PRs: