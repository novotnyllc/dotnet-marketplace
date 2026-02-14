# Conventions

Project patterns discovered during work. Not in CLAUDE.md but important.

<!-- Entries added manually via `flowctl memory add` -->

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
