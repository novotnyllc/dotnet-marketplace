# fn-9-agent-meta-skills.1 Agent gotchas and build analysis skills

## Description
Create two meta-skills focused on "what goes wrong" for agents working with .NET:

1. **`dotnet-agent-gotchas`** at `skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md` — covers 9 mistake categories. Each category includes: brief warning, anti-pattern code, corrected code, and `[skill:...]` cross-reference. No full implementation walkthroughs (per overlap rubric).

2. **`dotnet-build-analysis`** at `skills/agent-meta-skills/dotnet-build-analysis/SKILL.md` — covers 5 subsections. Each subsection includes: example output snippet, diagnosis steps, and fix pattern.

Both skills follow the required section structure: frontmatter, overview/scope, prerequisites, main content, slopwatch anti-patterns section, cross-references, references.

## File Ownership
- `skills/agent-meta-skills/dotnet-agent-gotchas/SKILL.md` (create)
- `skills/agent-meta-skills/dotnet-build-analysis/SKILL.md` (create)
- Does NOT modify `plugin.json` — fn-9.2 owns plugin registration

## Acceptance
### dotnet-agent-gotchas
- [ ] SKILL.md created with frontmatter (`name`, `description`)
- [ ] Has required sections: overview/scope, prerequisites, main content, slopwatch, cross-refs, references
- [ ] Category 1 (async/await misuse): warning + anti-pattern code + corrected code + `[skill:dotnet-csharp-async-patterns]`
- [ ] Category 2 (NuGet errors): warning + anti-pattern code + corrected code + cross-ref
- [ ] Category 3 (deprecated APIs): warning + anti-pattern code + corrected code + `[skill:dotnet-security-owasp]`
- [ ] Category 4 (project structure): warning + anti-pattern code + corrected code + cross-ref
- [ ] Category 5 (NRT errors): warning + anti-pattern code + corrected code + `[skill:dotnet-csharp-nullable-reference-types]`
- [ ] Category 6 (source gen misconfig): warning + anti-pattern code + corrected code + `[skill:dotnet-csharp-source-generators]`
- [ ] Category 7 (trimming/AOT suppression): warning + anti-pattern code + corrected code + cross-ref
- [ ] Category 8 (test org anti-patterns): warning + anti-pattern code + corrected code + `[skill:dotnet-testing-strategy]`
- [ ] Category 9 (DI errors): warning + anti-pattern code + corrected code + `[skill:dotnet-csharp-dependency-injection]`
- [ ] Dedicated "## Slopwatch Anti-Patterns" section covering all 5 checks (disabled tests, warning suppressions, empty catch blocks, silenced analyzers, removed assertions)
- [ ] All 6 required outbound cross-refs present per matrix
- [ ] No full implementation walkthroughs — brief warning + cross-ref only per overlap rubric

### dotnet-build-analysis
- [ ] SKILL.md created with frontmatter (`name`, `description`)
- [ ] Has required sections: overview/scope, prerequisites, main content, slopwatch, cross-refs, references
- [ ] Subsection (a) error code prefixes: >=5 prefixes (CS, MSB, NU, IDE, CA) each with example output + diagnosis + fix
- [ ] Subsection (b) NuGet restore failures: example output + diagnosis + fix
- [ ] Subsection (c) analyzer warnings: example output + interpretation guidance + suppression guidance
- [ ] Subsection (d) multi-targeting: example output showing TFM-specific differences + diagnosis
- [ ] Subsection (e) CI drift: example scenario + diagnosis + fix pattern
- [ ] Dedicated "## Slopwatch Anti-Patterns" section covering: warning suppressions, silenced analyzers
- [ ] All 3 required outbound cross-refs present per matrix

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
