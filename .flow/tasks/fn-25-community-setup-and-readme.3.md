# fn-25-community-setup-and-readme.3 Update CLAUDE.md and AGENTS.md with plugin instructions

## Description
Update both `CLAUDE.md` and `AGENTS.md` with substantive plugin-specific content. Currently `CLAUDE.md` is a one-line `@AGENTS.md` redirect and `AGENTS.md` contains only Flow-Next boilerplate. Both need real content.

### CLAUDE.md — Expand to standalone plugin instructions

Replace the `@AGENTS.md` redirect with standalone content. CLAUDE.md is the primary instruction surface for Claude Code sessions working in this repository.

**Required content:**
1. **Project overview** — dotnet-artisan plugin: 97 skills, 9 agents, hooks, MCP
2. **Key conventions** — SKILL.md frontmatter (`name`, `description` required), cross-reference syntax `[skill:name]`, description budget (<120 chars), directory structure `skills/<category>/<skill-name>/SKILL.md`
3. **Validation commands** — The 4 commands that must pass: `validate-skills.sh`, `validate-marketplace.sh`, `generate_dist.py --strict`, `validate_cross_agent.py`
4. **Development workflow** — Edit skills → validate locally → commit → CI validates
5. **File structure overview** — Key directories: `skills/`, `agents/`, `hooks/`, `scripts/`, `.claude-plugin/`, `dist/` (generated)
6. **Reference to AGENTS.md** — "See AGENTS.md for skill routing index and agent delegation patterns"
7. **Reference to CONTRIBUTING.md** — "See CONTRIBUTING.md for contribution guidelines"

### AGENTS.md — Add skill routing and agent delegation

Preserve the existing Flow-Next section at the bottom. Add new content above it.

**Required new content (above Flow-Next section):**
1. **Plugin overview** — Brief intro: dotnet-artisan provides .NET development skills for Claude Code
2. **Skill routing index** — Condensed table: Category | Skills (count) | When to use. This complements (does not duplicate) the `dotnet-advisor` skill's internal catalog. The index here is for human readers and agents reading AGENTS.md.
3. **Agent delegation patterns** — Table of 9 agents: Agent | Domain | Preloaded skills | When to delegate. Explains which agent handles which domain.
4. **Cross-references** — Links to README.md (full skill catalog), CONTRIBUTING.md (authoring guide)

**Must not conflict with `dotnet-advisor` skill's routing logic** — the AGENTS.md index is a complement for broader context, not a replacement.

**Files modified:** `CLAUDE.md`, `AGENTS.md`
**Files NOT modified:** `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `plugin.json`

## Acceptance
- [ ] `CLAUDE.md` has standalone content (not just `@AGENTS.md` redirect)
- [ ] `CLAUDE.md` lists validation commands, key conventions, file structure overview
- [ ] `CLAUDE.md` references AGENTS.md and CONTRIBUTING.md
- [ ] `AGENTS.md` has skill routing index table (18 categories)
- [ ] `AGENTS.md` has agent delegation patterns table (9 agents)
- [ ] `AGENTS.md` preserves existing Flow-Next section
- [ ] Content is consistent with README.md skill catalog and CONTRIBUTING.md authoring guide
- [ ] Does not conflict with `dotnet-advisor` routing logic
- [ ] Quick commands pass:
  ```bash
  lines=$(wc -l < CLAUDE.md)
  [[ "$lines" -gt 5 ]]  # Not just a redirect
  grep -qi "validate-skills" CLAUDE.md  # Has validation commands
  grep -qi "skill" AGENTS.md  # Has skill content
  grep -qi "flow-next" AGENTS.md  # Flow-Next preserved
  grep -qi "agent" AGENTS.md  # Has agent delegation
  ```

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
