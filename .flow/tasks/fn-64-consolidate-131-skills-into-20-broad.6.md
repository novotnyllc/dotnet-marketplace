# fn-64-consolidate-131-skills-into-20-broad.6 Consolidate DevOps skills: dotnet-cicd-gha, dotnet-cicd-ado, dotnet-containers, dotnet-packaging

## Description
Create consolidated `dotnet-tooling` skill directory. Merge ~34 build, performance, AOT, CLI, project setup, docs generation, and meta-skills into one skill with companion files. This is the largest consolidation group. Remove source skill directories and update `plugin.json`.

**Size:** M
**Files:** `skills/dotnet-tooling/SKILL.md` + `references/*.md` (new), `.claude-plugin/plugin.json`, ~34 source skill dirs (delete)

## Approach

- Follow consolidation map from task .1
- Write SKILL.md: developer tooling overview, routing table with rich keyword hints, scope/out-of-scope, ToC (~4-5KB given breadth)
- Create `references/` dir. Expected companion files:
  - `references/project-setup.md` — project structure, scaffolding, artifacts output, add-analyzers, add-ci, add-testing, modernize
  - `references/msbuild.md` — MSBuild authoring, tasks, build optimization, build analysis, csproj reading
  - `references/performance.md` — patterns, profiling, GC/memory, LINQ optimization
  - `references/native-aot.md` — Native AOT, AOT architecture, trimming, WASM AOT
  - `references/cli-apps.md` — System.CommandLine, CLI architecture, distribution, packaging, release pipeline
  - `references/terminal-ui.md` — Spectre.Console, Terminal.Gui
  - `references/tool-management.md` — dotnet tool install, local tools, solution navigation
  - `references/documentation.md` — strategy, Mermaid diagrams, GitHub docs, XML docs, API docs
  - `references/version-management.md` — version detection, version upgrade, multi-targeting
  - `references/agent-meta.md` — agent gotchas, slopwatch, build-analysis tips
  - (exact list per task .1 output)

## Key context

- This is the broadest consolidation (~34 source skills) — intentionally a grab-bag per epic decision #9
- The SKILL.md routing table must have strong keyword differentiation since sub-topics are diverse
- Several source skills are user-invocable (scaffold-project, add-analyzers, add-ci, add-testing, modernize, slopwatch, version-upgrade) — decide per task .1 which user-invocable designation the consolidated skill gets
- `dotnet-version-detection` and `dotnet-project-analysis` are shared foundations used by 5 agents — companion file must be prominent in ToC
- If post-implementation this feels too broad, splitting into build/performance/cli is a single-task change (epic decision #9)
## Approach

- Follow consolidation map from task .1
- `dotnet-cicd-gha` merges: gha-patterns, gha-build-test, gha-publish, gha-deploy
- `dotnet-cicd-ado` merges: ado-patterns, ado-build-test, ado-publish, ado-unique
- `dotnet-containers` merges: containers, container-deployment
- `dotnet-packaging` merges: nuget-authoring, msix, github-releases, release-management
## Acceptance
- [ ] `skills/dotnet-tooling/SKILL.md` exists with overview, routing table, scope, out-of-scope, ToC
- [ ] `skills/dotnet-tooling/references/` contains ~10 companion files covering all sub-domains
- [ ] All ~34 source tooling skill directories deleted
- [ ] `plugin.json` updated
- [ ] Valid frontmatter
- [ ] No content lost from source skills
- [ ] User-invocable designation decided and set correctly
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
