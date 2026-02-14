# fn-21-documentation-skills.3 Integration — plugin registration, advisor catalog, agent creation, validation

## Description
Register all 5 fn-21 documentation skills in `plugin.json`, update the advisor catalog, create the `dotnet-docs-generator` agent, and run validation. This task depends on fn-21.1 and fn-21.2 completing first. Single owner of `plugin.json` changes — eliminates merge conflicts.

**Plugin registration:**
- Add 5 skill paths to `.claude-plugin/plugin.json` `skills` array:
  - `skills/documentation/dotnet-documentation-strategy`
  - `skills/documentation/dotnet-mermaid-diagrams`
  - `skills/documentation/dotnet-github-docs`
  - `skills/documentation/dotnet-xml-docs`
  - `skills/documentation/dotnet-api-docs`
- Add 1 agent path to `.claude-plugin/plugin.json` `agents` array:
  - `agents/dotnet-docs-generator.md`

**Advisor catalog updates in `skills/foundation/dotnet-advisor/SKILL.md`:**
- Section 18 ("Documentation"): change `planned` to `implemented`
- Verify all 5 skill names in advisor match their SKILL.md `name` frontmatter values exactly

**Agent creation (`agents/dotnet-docs-generator.md`):**
- Frontmatter: `name`, `description`, `model: sonnet`, `capabilities` (bullet list), `tools` (Read, Grep, Glob, Bash, Edit, Write)
- Preloaded skills: `[skill:dotnet-documentation-strategy]`, `[skill:dotnet-mermaid-diagrams]`, `[skill:dotnet-xml-docs]`
- Workflow: 1) Analyze project structure and detect existing docs 2) Recommend documentation tooling 3) Generate Mermaid architecture diagrams 4) Write XML doc comment skeletons for public APIs 5) Scaffold GitHub-native docs (README, CONTRIBUTING, templates)
- Trigger lexicon: "generate docs", "add documentation", "create README", "document this project", "add XML docs", "generate architecture diagram"
- Explicit boundaries: does NOT own CI deployment (defer to `[skill:dotnet-gha-deploy]`), does NOT own OpenAPI generation (defer to `[skill:dotnet-openapi]`), does NOT own changelog generation (defer to `[skill:dotnet-release-management]`)
- Example prompts for common documentation tasks

**Cross-reference reconciliation:**
- Search for `<!-- TODO(fn-21) -->` placeholders in all skills — resolve with canonical cross-refs (currently none exist, but verify)
- Search for bare "fn-21" mentions in other skills — update to canonical `[skill:dotnet-*]` cross-refs where appropriate

**Validation:**
- Run repo-wide skill name uniqueness check
- Run `./scripts/validate-skills.sh`
- Validate cross-references present in all 5 skills
- Verify advisor section updates
- Verify agent file structure matches existing agent patterns

**Files created:**
- `agents/dotnet-docs-generator.md`

**Files modified:**
- `.claude-plugin/plugin.json`
- `skills/foundation/dotnet-advisor/SKILL.md`

## Acceptance
- [ ] All 5 skill paths registered in `plugin.json` `skills` array
- [ ] Agent `agents/dotnet-docs-generator.md` registered in `plugin.json` `agents` array
- [ ] Advisor section 18 updated from `planned` to `implemented`
- [ ] Advisor skill names match SKILL.md `name` frontmatter values exactly
- [ ] `agents/dotnet-docs-generator.md` exists with proper frontmatter (`name`, `description`, `model: sonnet`, `capabilities`, `tools`)
- [ ] Agent preloads `[skill:dotnet-documentation-strategy]`, `[skill:dotnet-mermaid-diagrams]`, `[skill:dotnet-xml-docs]`
- [ ] Agent workflow includes: analyze project, recommend tooling, generate diagrams, write XML doc skeletons, scaffold GitHub docs
- [ ] Agent has explicit boundary statements (no CI deployment, no OpenAPI generation, no changelog generation)
- [ ] Agent includes trigger lexicon and example prompts
- [ ] `grep -r 'TODO(fn-21)' skills/` returns empty
- [ ] `grep -rh "^name:" skills/*/*/SKILL.md | sort | uniq -d` returns empty (no duplicate names)
- [ ] `./scripts/validate-skills.sh` passes
- [ ] Cross-references validated in all 5 skills
- [ ] plugin.json syntax is valid JSON (`python3 -m json.tool .claude-plugin/plugin.json > /dev/null`)

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
