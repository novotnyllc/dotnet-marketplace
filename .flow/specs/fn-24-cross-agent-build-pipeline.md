# fn-24: Cross-Agent Build Pipeline

## Problem/Goal
Create dotnet tool for inner loop validation and GitHub Action for cross-agent format generation, producing Claude Code plugin, GitHub Copilot instructions, and OpenAI Codex AGENTS.md from canonical SKILL.md source.

## Acceptance Checks
- [ ] dotnet tool created for local development (validates skill format, frontmatter, cross-references, generates dist/ outputs)
- [ ] GitHub Action workflow generates dist/claude/, dist/copilot/, dist/codex/ on push/release
- [ ] Action publishes to Claude Code marketplace
- [ ] Action creates GitHub Release with all artifacts
- [ ] Build pipeline validates skill format, frontmatter, cross-references, markdown lint
- [ ] Cross-agent conformance test suite validates behavioral equivalence across generated outputs
- [ ] Cross-references to CI/CD skills, packaging skills

## Cross-Agent Conformance Tests

Generation success ≠ behavioral equivalence. The build pipeline must include a conformance test suite:

### Required Tests
1. **Routing parity**: Every canonical SKILL.md trigger phrase appears in all generated agent formats (Claude plugin description, Copilot `applyTo` instructions, Codex AGENTS.md sections)
2. **Trigger coverage**: Spot-check that sample queries would activate the same skill across all three agent formats
3. **Graceful degradation**: Verify that Claude-only features (hooks, MCP, agents) are cleanly omitted from Copilot/Codex outputs without broken references or dangling cross-refs
4. **Semantic diff**: Detect unintended content drift between canonical SKILL.md and generated outputs (beyond expected format transformations)
5. **Cross-reference integrity**: All `[skill:name]` references in generated outputs resolve to valid targets within that agent's format

### Implementation
- Tests run as part of the dotnet tool validation (`dotnet artisan validate --cross-agent`)
- CI gate: conformance failures block merge
- Report format: per-skill pass/fail with diff for failures

## Dependencies
- fn-19 (CI/CD Skills) — pipeline patterns and workflow templates
- fn-23 (Hooks & MCP Integration) — conformance tests must validate against the fully-featured Claude baseline including hooks and MCP, not a partial implementation

## Trigger Corpus
Trigger coverage tests (item 2 above) must use a **deterministic minimum corpus** of at least 20 representative queries spanning all skill categories. The corpus is a maintained test artifact (not ad-hoc spot checks) and must be updated when skills are added or renamed.

## Key Context
- Canonical source is skills/ directory using Agent Skills SKILL.md format
- Cross-agent compatibility via build-time generation (not manual duplication)
- Inner loop validation prevents broken commits
- Publishing workflow uses NBGV for versioning
