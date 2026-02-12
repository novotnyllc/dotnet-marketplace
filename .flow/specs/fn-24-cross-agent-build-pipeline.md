# fn-24: Cross-Agent Build Pipeline

## Problem/Goal
Create dotnet tool for inner loop validation and GitHub Action for cross-agent format generation, producing Claude Code plugin, GitHub Copilot instructions, and OpenAI Codex AGENTS.md from canonical SKILL.md source.

## Acceptance Checks
- [ ] dotnet tool created for local development (validates skill format, frontmatter, cross-references, generates dist/ outputs)
- [ ] GitHub Action workflow generates dist/claude/, dist/copilot/, dist/codex/ on push/release
- [ ] Action publishes to Claude Code marketplace
- [ ] Action creates GitHub Release with all artifacts
- [ ] Build pipeline validates skill format, frontmatter, cross-references, markdown lint
- [ ] Cross-references to CI/CD skills, packaging skills

## Key Context
- Canonical source is skills/ directory using Agent Skills SKILL.md format
- Cross-agent compatibility via build-time generation (not manual duplication)
- Inner loop validation prevents broken commits
- Publishing workflow uses NBGV for versioning
