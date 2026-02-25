# Conventions

Project patterns discovered during work. Not in CLAUDE.md but important.

<!-- Entries added manually via `flowctl memory add` -->

## 2026-02-12 manual [convention]
All work must be done in the main branch. Do not create branches in the repository

## 2026-02-12 manual [convention]
Agent .md frontmatter requires name field in addition to description, capabilities, and tools

## 2026-02-12 manual [convention]
Always validate JSON field types with jq predicates (type=="string" and length>0), not just emptiness checks

## 2026-02-12 manual [convention]
When an epic's skills overlap with other epics, add an explicit scope boundary table mapping which epic owns scaffolding vs depth for each concern

## 2026-02-12 manual [convention]
When multiple tasks touch a shared file (e.g., plugin.json), assign registration to one dedicated task or final consolidation step — keeps skill-authoring tasks file-disjoint and parallelizable

## 2026-02-12 manual [convention]
When adding skills, validate name uniqueness both repo-wide AND against marketplace catalog metadata to prevent cross-plugin skill ID collisions

## 2026-02-12 manual [convention]
When epic acceptance criteria reference validation (e.g. cross-ref matrix, deprecated patterns), task specs must include executable grep commands that verify each requirement — not just intent statements

## 2026-02-12 manual [convention]
When multiple skills share a concern (e.g. deprecated patterns), designate a canonical owner in the epic spec and have other skills cross-reference it — avoids scope ambiguity and duplication

## 2026-02-12 manual [convention]
Agent workflow steps must be executable with the agent declared toolset -- do not reference CLI commands if Bash is not in tools list

## 2026-02-12 manual [convention]
Per-subsection acceptance: when skill definition says 'each section MUST include X', the AC and task checkboxes must enforce X per subsection, not just globally

## 2026-02-12 manual [convention]
Every skill section (overview, prerequisites, slopwatch, etc.) MUST use explicit ## headers, not inline bold labels — spec validation checks for headers

## 2026-02-13 manual [convention]
Agent preloaded skills must include foundation skills (version-detection, project-analysis) used in workflow steps, not just domain skills — match the dotnet-architect pattern

## 2026-02-13 manual [convention]
Quick command counts (grep -c) break when other epics add files to the same directory — use explicit per-file checks instead

## 2026-02-13 manual [convention]
New framework epics must match fn-13 parity: scope table, content coverage tables, agent schema with trigger lexicon, scope boundaries matrix, cross-ref classification (hard/soft), serial task deps, quick commands, 15+ acceptance criteria, and restructure validation task (task N) to match cross-refs+validate pattern

## 2026-02-14 manual [convention]
Epic specs must include Dependencies (hard/soft epic deps), .NET Version Policy (baseline + version-gating), and Conventions sections for peer-epic parity

## 2026-02-14 manual [convention]
Epic specs need task decomposition section mapping each task to exact file paths and deliverables (following fn-5 pattern)

## 2026-02-14 manual [convention]
Create dedicated integration task (like fn-5.6, fn-18.4) as single owner of plugin.json to prevent merge conflicts in parallel workflows

## 2026-02-14 manual [convention]
Scope boundary table in epic spec prevents duplication across epics - must map what epic owns vs cross-references to other epics

## 2026-02-14 manual [convention]
Epic specs must include scope boundary table, .NET version policy, task decomposition with file paths, cross-ref classification, and testable AC with validation commands — not just intent statements

## 2026-02-14 manual [convention]
Task specs for validation/doc tasks should include concrete code snippets matching the existing script's conventions (variable names, path prefixes)

## 2026-02-14 manual [convention]
Configuration lists (agent names, tool prefixes) should be read from canonical source files (e.g. plugin.json) at runtime, not hardcoded -- eliminates drift when the source is updated

## 2026-02-15 manual [convention]
Epic specs must include: scope boundary table, Out of Scope section, .NET Version Policy, Dependencies, Conventions, and Task Decomposition table -- all are required for plan review SHIP

## 2026-02-15 manual [convention]
Task specs for skills must require Agent Gotchas, Prerequisites, and References sections with grep-verifiable verification commands

## 2026-02-15 manual [convention]
Always add a dedicated integration task (task .N) that owns plugin.json registration, README/CLAUDE.md/AGENTS.md count updates, and trigger-corpus entries -- prevents merge conflicts when multiple skill tasks touch plugin.json

## 2026-02-17 manual [convention]
When creating metadata files for repo-level discovery, clarify in spec whether they're marketplace-level or per-component; single-component repos can use repo root, but document scalability path for multi-component architectures

## 2026-02-19 manual [convention]
Task specs that reference audit data should say 'per the baseline report' instead of hardcoding counts -- counts change as detection logic improves

## 2026-02-24 manual [convention]
Eval runners must record a result for every dataset case including skipped ones (e.g. classification=skipped) so coverage gaps are visible in results and baseline comparisons

## 2026-02-24 manual [convention]
Retry logic should distinguish non-retryable config errors (missing binary, bad flags) from transient failures (timeout, rate limit) -- use a custom exception type that retry_with_backoff re-raises immediately to avoid stalling on deterministic failures

## 2026-02-25 manual [convention]
When a JSON state file drives multi-task workflows, track each status dimension independently (e.g., routing_status + content_status) rather than a single ambiguous status field

## 2026-02-25 manual [convention]
Triage/analysis documents that reference entity IDs should verify those IDs exist in the codebase before shipping, and state the verification was done

## 2026-02-25 manual [convention]
When metrics exclude error/timeout cases, explicitly define the gating policy (what counts, what is excluded, and why) so downstream consumers do not misinterpret raw vs clean numbers
