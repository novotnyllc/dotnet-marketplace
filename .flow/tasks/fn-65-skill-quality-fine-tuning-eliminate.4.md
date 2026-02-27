# fn-65-skill-quality-fine-tuning-eliminate.4 Update docs and extend validator for reference file checks

## Description
Update stale documentation and extend the validator to check reference files, encoding the new conventions from Tasks 1-3.

**Size:** M
**Files:** `CONTRIBUTING-SKILLS.md`, `docs/skill-routing-style-guide.md`, `scripts/_validate_skills.py`

## Approach

### 1. Fix CONTRIBUTING-SKILLS.md

Replace all `details.md` references with the `references/` multi-file pattern:

- **Lines 60-68** (folder structure diagram): Change `details.md` to `references/` directory with 2-3 example files.
- **Line 105**: Change "extract it into a `details.md` file" to "extract it into files under `references/`".
- **Line 108**: Change the `details.md` example to a `references/` example.
- **Lines 262, 289**: Update progressive disclosure layers and size limit sections from `details.md` to `references/`.
- **Line 111** already mentions `references/` correctly — ensure surrounding text is consistent.

### 2. Fix style guide

- **Line 3**: Remove stale "T5--T10 sweep tasks" reference. Just state this is the canonical reference.
- **Line 134**: Replace `dotnet-version-detection` (deleted skill) in cycle detection example with a current skill name (e.g., `dotnet-tooling`).
- **Lines 236-251**: Replace the invocation contract positive example (drawn from deleted `dotnet-version-detection`) with an example from a current 8-skill name (use `dotnet-csharp` or `dotnet-tooling`).
- **Line 277**: Update "130+ skills" rollout language to "8 skills".
- **Add a new section** on the `references/` companion file convention: when to use, naming convention (human-readable Title Case), no Scope/OOS required, progressive disclosure role.
- **Add explicit documentation** that `[skill:]` syntax is used for both skills and agents. The `<id>` must match either a skill directory name or an agent file stem. This clarifies the existing convention.

### 3. Extend validator for reference files

Add checks to `scripts/_validate_skills.py` for files matching `skills/*/references/*.md`:

- **Title check (fence-aware)**: Every reference file must have an H1 title (`# ...`). The validator must scan for the first H1 outside code fences (between ``` markers), not just the first line. Title must NOT start with `# dotnet-` (slug-style). **Note:** The existing `extract_refs()` function is NOT fence-aware — write a new fence-aware reference extractor for reference files rather than modifying the existing SKILL/agent validation behavior.

- **No Scope/OOS**: Reference files must NOT have `## Scope` or `## Out of scope` headings.

- **Stale cross-ref check (fence-aware)**: Write a new fence-aware `[skill:X]` extractor that skips content inside code fences. Any `[skill:X]` reference outside code fences must resolve against `known_ids` (the union of skill directory names and agent file stems, same set used for SKILL.md validation). Report unresolved refs as ERRORs. This is a **new function** — do not modify the existing `extract_refs()` to avoid changing SKILL/agent validation outputs.

- **Stale cross-ref severity**: Reference files are always strict — unresolved `[skill:]` refs are ERRORs regardless of `--allow-planned-refs`. This is intentional: reference files should never contain planned/future skill names.

- **Routing table file existence**: For each SKILL.md that contains a `## Routing Table` section (the 7 domain skills), parse it and validate companion-file existence. Skip skills without that section (the advisor has no routing table). Locate the `Companion File` column by matching the table header row by column name (not by position index). For each file path in that column, verify the file exists on disk. Report missing files as ERRORs.

**Architecture notes:**
- Reuse the existing `known_ids` set (skills + agents) for cross-ref resolution. Do NOT create a separate "reference-only" allowlist.
- Add reference checks as a new function called from the main validation loop, respecting the existing WARN/FAIL severity model.
- The fence-aware extractor should track whether the current line is inside a code fence (between ``` markers) and skip `[skill:]` extraction and H1 detection for fenced lines.

## Key context

- The validator currently processes only `SKILL.md` and agent files. Reference files are invisible to it.
- The existing filler-phrase detection (line 94-100) and invocation contract checks are good patterns to follow for new reference file checks.
- The valid `known_ids` for cross-ref resolution are constructed from skill directory names + agent file stems. This is already computed in the validator.
- CONTRIBUTING-SKILLS.md is 480 lines. The `details.md` pattern appears in 5 locations. Replace all consistently.
- Task 4 lands LAST after Tasks 1-3 so the validator encodes the final conventions.

## Acceptance
- [ ] CONTRIBUTING-SKILLS.md has zero references to `details.md`
- [ ] CONTRIBUTING-SKILLS.md folder structure shows `references/` directory pattern
- [ ] Style guide positive example uses a current 8-skill name (not `dotnet-version-detection`)
- [ ] Style guide has no "T5--T10" references
- [ ] Style guide says "8 skills" not "130+ skills" in rollout section
- [ ] Style guide has a new section documenting the `references/` companion file convention
- [ ] Style guide explicitly documents that `[skill:]` is used for both skills and agents
- [ ] Validator title check is fence-aware (finds first H1 outside code fences)
- [ ] Validator stale cross-ref check is fence-aware (skips refs inside code fences)
- [ ] Validator uses `known_ids` (skills + agents) for reference file cross-ref resolution
- [ ] Validator routing table check parses `Companion File` column by header name, not position
- [ ] `./scripts/validate-skills.sh` passes (including new reference checks)
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] Running validator against a reference file with stale `[skill:dotnet-minimal-apis]` ref outside a code fence reports an error
- [ ] Running validator against a reference file with `[skill:dotnet-minimal-apis]` inside a code fence does NOT report an error

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
