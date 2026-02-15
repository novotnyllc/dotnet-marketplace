# Fleet Skill Review Rubric

This document defines the evaluation rubric, scoring guidance, output templates, category batch assignments, and worker agent instructions for the dotnet-artisan fleet skill review sweep.

---

## 1. Evaluation Rubric

Each skill is evaluated on 11 dimensions. Every dimension receives a verdict of **pass**, **warn**, or **fail**.

### Dimension 1: Description Quality

Evaluates whether the `description` frontmatter field follows the formula: **[What it does] + [When to use it]**.

| Verdict | Criteria |
|---------|----------|
| **pass** | Description follows `[What] + [When/Triggers]` formula, is specific and actionable, and is under 120 characters |
| **warn** | Description is functional but missing activation context (no WHEN clause) or slightly over 120 characters (121-140) |
| **fail** | Description is vague ("helps with X"), over 140 characters, or missing entirely |

Reference: CONTRIBUTING-SKILLS.md section 3 ("Writing Effective Descriptions").

### Dimension 2: Description Triggering

Evaluates whether Claude would correctly activate this skill from typical user requests. Checks for over-triggering (too generic) and under-triggering (too narrow).

| Verdict | Criteria |
|---------|----------|
| **pass** | Description contains trigger phrases a user would actually say; activation scope matches skill content |
| **warn** | Triggers are present but overly broad (would fire for unrelated requests) or overly narrow (misses common phrasings) |
| **fail** | No discernible trigger phrases; skill would never activate or would activate for everything |

### Dimension 3: Instruction Clarity

Evaluates whether the SKILL.md body provides specific, actionable guidance rather than vague statements.

| Verdict | Criteria |
|---------|----------|
| **pass** | Instructions are concrete and actionable; critical steps are explicit; no ambiguous phrasing |
| **warn** | Mostly clear but some sections use vague language ("consider using...", "you might want to...") |
| **fail** | Predominantly vague or hand-wavy; agent cannot determine what to actually do |

### Dimension 4: Progressive Disclosure

Evaluates whether SKILL.md is focused on core instructions, with detailed references linked rather than inlined.

| Verdict | Criteria |
|---------|----------|
| **pass** | SKILL.md focuses on core guidance; extended content is in `details.md` or linked externally; SKILL.md is under 5,000 words |
| **warn** | SKILL.md is slightly bloated (3,000-5,000 words) but has no `details.md` companion, or has verbose examples that could be extracted |
| **fail** | SKILL.md exceeds 5,000 words, or has massive inline code blocks that should be in `details.md` |

Reference: CONTRIBUTING-SKILLS.md section 4 ("Progressive Disclosure").

### Dimension 5: Cross-References

Evaluates whether cross-references use `[skill:name]` syntax and are accurate.

| Verdict | Criteria |
|---------|----------|
| **pass** | All skill references use `[skill:skill-name]` syntax; references point to existing skills; bidirectional references present where appropriate |
| **warn** | Most references use correct syntax but one or two use bare text names; or minor missing bidirectional links |
| **fail** | Multiple bare-text skill references; references point to non-existent skills; no cross-references where they would be expected |

Reference: CLAUDE.md ("Cross-Reference Syntax").

### Dimension 6: Error Handling

Evaluates whether the skill includes troubleshooting or common pitfalls for its .NET domain.

| Verdict | Criteria |
|---------|----------|
| **pass** | Includes Agent Gotchas section or explicit troubleshooting guidance; covers common pitfalls for the domain |
| **warn** | Has some error handling guidance but incomplete; missing Agent Gotchas where peer skills have one |
| **fail** | No error handling, troubleshooting, or pitfall guidance in a domain where mistakes are common |

### Dimension 7: Examples

Evaluates whether the skill includes concrete code examples showing the skill in action.

| Verdict | Criteria |
|---------|----------|
| **pass** | Contains real .NET code examples (not pseudocode); examples are correct and compilable; NuGet packages are listed where needed |
| **warn** | Has examples but they are incomplete, use pseudocode, or are missing package references for third-party APIs |
| **fail** | No code examples in a skill that clearly needs them; or examples contain errors that would cause compilation failures |

Reference: Pitfalls memory -- "Skill code examples that use third-party NuGet APIs must list those packages explicitly."

### Dimension 8: Composability

Evaluates whether the skill works well alongside other skills without assuming it is the only loaded skill.

| Verdict | Criteria |
|---------|----------|
| **pass** | Skill uses "Out of scope" markers with attribution to owning skills; does not duplicate content covered by other skills; references companion skills appropriately |
| **warn** | Minor overlap with other skills but no harmful conflict; missing "Out of scope" markers in one or two places |
| **fail** | Significant content duplication with other skills; contradicts guidance in peer skills; assumes it is the only active skill |

### Dimension 9: Consistency

Evaluates whether the skill follows the same patterns as peer skills in its category.

| Verdict | Criteria |
|---------|----------|
| **pass** | Section headers, code example format, cross-reference placement, and Agent Gotchas presence match category peers |
| **warn** | Minor structural deviations (different heading levels, inconsistent code block language tags) |
| **fail** | Completely different structure from category peers; missing standard sections that all peers have |

### Dimension 10: Registration and Budget

Evaluates whether the skill is properly registered in plugin.json and whether its description stays within budget.

| Verdict | Criteria |
|---------|----------|
| **pass** | Registered in plugin.json `skills` array; description under 120 characters; aggregate budget impact acceptable |
| **warn** | Registered but description is 121-140 characters, pushing aggregate budget toward the 12,000-char warning threshold |
| **fail** | Not registered in plugin.json; or description so long it pushes aggregate budget past the 15,000-char hard limit |

Reference: CLAUDE.md ("Description Budget"), validation output `BUDGET_STATUS`.

### Dimension 11: Progressive Disclosure Compliance

Evaluates whether the skill properly uses a `details.md` companion file when needed.

| Verdict | Criteria |
|---------|----------|
| **pass** | SKILL.md under ~3,000 words and self-contained; or SKILL.md over ~3,000 words with a properly referenced `details.md` companion |
| **warn** | SKILL.md is 3,000-4,000 words with extensive code examples that could be extracted but has no `details.md` |
| **fail** | SKILL.md over 4,000 words with no `details.md`; or `details.md` exists but is not referenced from SKILL.md |

Reference: CONTRIBUTING-SKILLS.md section 2 ("Companion Files").

---

## 2. Scoring Guidance

### Per-Dimension Verdicts

- **pass** -- Meets or exceeds expectations. No changes needed.
- **warn** -- Functional but could be improved. Flag for high-value improvement.
- **fail** -- Broken, missing, or actively harmful. Flag as critical issue.

### Overall Skill Assessment

Derive an overall assessment from the per-dimension verdicts:

| Overall | Rule |
|---------|------|
| **Clean** | All 11 dimensions pass |
| **Needs Work** | One or more dimensions at warn, none at fail |
| **Critical** | One or more dimensions at fail |

### Priority Classification for Improvements

When recording findings, classify each issue:

| Priority | Definition | Examples |
|----------|------------|----------|
| **Critical** | Broken functionality or violated hard constraints | Unregistered skill, broken cross-refs, description over 140 chars, missing frontmatter |
| **High** | Significantly degrades skill quality or triggering | Vague description missing triggers, no Agent Gotchas in error-prone domain, stale code examples |
| **Low** | Polish or minor formatting | Inconsistent heading level, minor wording improvement, extra whitespace |

---

## 3. Per-Skill Output Template

For each skill reviewed, produce a structured entry using this template:

```markdown
### <skill-name>

**Category:** <category>
**Overall:** Clean | Needs Work | Critical

| # | Dimension | Verdict | Notes |
|---|-----------|---------|-------|
| 1 | Description Quality | pass/warn/fail | <brief note if not pass> |
| 2 | Description Triggering | pass/warn/fail | <brief note if not pass> |
| 3 | Instruction Clarity | pass/warn/fail | <brief note if not pass> |
| 4 | Progressive Disclosure | pass/warn/fail | <brief note if not pass> |
| 5 | Cross-References | pass/warn/fail | <brief note if not pass> |
| 6 | Error Handling | pass/warn/fail | <brief note if not pass> |
| 7 | Examples | pass/warn/fail | <brief note if not pass> |
| 8 | Composability | pass/warn/fail | <brief note if not pass> |
| 9 | Consistency | pass/warn/fail | <brief note if not pass> |
| 10 | Registration & Budget | pass/warn/fail | <brief note if not pass> |
| 11 | Progressive Disclosure Compliance | pass/warn/fail | <brief note if not pass> |

**Issues:**
- [Critical/High/Low] <issue description> -- <suggested fix>
- [Critical/High/Low] <issue description> -- <suggested fix>

**Proposed description:** (only if current description needs changes)
```

When a dimension passes, the Notes column should be left empty or contain a dash. Only document issues for warn/fail dimensions.

---

## 4. Category Batch Assignments

Skill counts are verified against both on-disk directories and `.claude-plugin/plugin.json` registration. There are **99 registered skills** in plugin.json and **101 skill directories** on disk (2 multi-targeting skills exist on disk but are not registered).

### Batch A -- Foundation, Core C#, Project Structure, Release Management (20 skills)

All 20 are registered in plugin.json.

| Category | Count | Skills |
|----------|-------|--------|
| foundation | 4 | dotnet-advisor, dotnet-version-detection, dotnet-project-analysis, plugin-self-publish |
| core-csharp | 9 | dotnet-csharp-modern-patterns, dotnet-csharp-coding-standards, dotnet-csharp-async-patterns, dotnet-csharp-nullable-reference-types, dotnet-csharp-dependency-injection, dotnet-csharp-configuration, dotnet-csharp-source-generators, dotnet-csharp-code-smells, dotnet-roslyn-analyzers |
| project-structure | 6 | dotnet-project-structure, dotnet-scaffold-project, dotnet-add-analyzers, dotnet-add-ci, dotnet-add-testing, dotnet-modernize |
| release-management | 1 | dotnet-release-management |

### Batch B -- Architecture, Serialization, Security, Multi-Targeting (19 skills)

17 registered in plugin.json + 2 unregistered multi-targeting skills = 19 on disk.

| Category | Count | Registered | Skills |
|----------|-------|------------|--------|
| architecture | 10 | 10/10 | dotnet-architecture-patterns, dotnet-background-services, dotnet-resilience, dotnet-http-client, dotnet-observability, dotnet-efcore-patterns, dotnet-efcore-architecture, dotnet-data-access-strategy, dotnet-containers, dotnet-container-deployment |
| serialization | 4 | 4/4 | dotnet-grpc, dotnet-realtime-communication, dotnet-serialization, dotnet-service-communication |
| security | 3 | 3/3 | dotnet-security-owasp, dotnet-secrets-management, dotnet-cryptography |
| multi-targeting | 2 | 0/2 | dotnet-multi-targeting, dotnet-version-upgrade |

**Note:** The 2 multi-targeting skills are NOT registered in plugin.json. The audit must flag this as a Critical issue under Dimension 10 (Registration & Budget).

### Batch C -- Testing, CI/CD (18 skills)

All 18 are registered in plugin.json.

| Category | Count | Skills |
|----------|-------|--------|
| testing | 10 | dotnet-testing-strategy, dotnet-xunit, dotnet-integration-testing, dotnet-ui-testing-core, dotnet-blazor-testing, dotnet-maui-testing, dotnet-uno-testing, dotnet-playwright, dotnet-snapshot-testing, dotnet-test-quality |
| cicd | 8 | dotnet-gha-patterns, dotnet-gha-build-test, dotnet-gha-publish, dotnet-gha-deploy, dotnet-ado-patterns, dotnet-ado-build-test, dotnet-ado-publish, dotnet-ado-unique |

### Batch D -- API Development, CLI Tools, Performance, Native AOT (18 skills)

All 18 are registered in plugin.json.

| Category | Count | Skills |
|----------|-------|--------|
| api-development | 5 | dotnet-minimal-apis, dotnet-api-versioning, dotnet-openapi, dotnet-api-security, dotnet-input-validation |
| cli-tools | 5 | dotnet-system-commandline, dotnet-cli-architecture, dotnet-cli-distribution, dotnet-cli-packaging, dotnet-cli-release-pipeline |
| performance | 4 | dotnet-benchmarkdotnet, dotnet-performance-patterns, dotnet-profiling, dotnet-ci-benchmarking |
| native-aot | 4 | dotnet-native-aot, dotnet-aot-architecture, dotnet-trimming, dotnet-aot-wasm |

### Batch E -- UI Frameworks, Agent Meta-Skills (17 skills)

All 17 are registered in plugin.json.

| Category | Count | Skills |
|----------|-------|--------|
| ui-frameworks | 13 | dotnet-blazor-patterns, dotnet-blazor-components, dotnet-blazor-auth, dotnet-uno-platform, dotnet-uno-targets, dotnet-uno-mcp, dotnet-maui-development, dotnet-maui-aot, dotnet-winui, dotnet-wpf-modern, dotnet-wpf-migration, dotnet-winforms-basics, dotnet-ui-chooser |
| agent-meta-skills | 4 | dotnet-agent-gotchas, dotnet-build-analysis, dotnet-csproj-reading, dotnet-solution-navigation |

### Batch F -- Documentation, Packaging, Localization (9 skills)

All 9 are registered in plugin.json.

| Category | Count | Skills |
|----------|-------|--------|
| documentation | 5 | dotnet-documentation-strategy, dotnet-mermaid-diagrams, dotnet-github-docs, dotnet-xml-docs, dotnet-api-docs |
| packaging | 3 | dotnet-nuget-authoring, dotnet-msix, dotnet-github-releases |
| localization | 1 | dotnet-localization |

### Summary

| Batch | Categories | Skill Count (on disk) | Registered in plugin.json |
|-------|------------|----------------------|---------------------------|
| A | foundation, core-csharp, project-structure, release-management | 20 | 20 |
| B | architecture, serialization, security, multi-targeting | 19 | 17 |
| C | testing, cicd | 18 | 18 |
| D | api-development, cli-tools, performance, native-aot | 18 | 18 |
| E | ui-frameworks, agent-meta-skills | 17 | 17 |
| F | documentation, packaging, localization | 9 | 9 |
| **Total** | **18 categories** | **101** | **99** |

**Reconciliation note:** The epic spec estimated 99 skills across 18 categories. Actual count is 101 skill directories on disk across 18 non-empty categories (plus 2 empty categories: containers, data-access). Of the 101 on disk, 99 are registered in plugin.json. The 2 unregistered skills are in the multi-targeting category.

**Empty categories on disk:** `skills/containers/` and `skills/data-access/` exist as directories but contain no skills. These are likely remnants or placeholders and should be noted but do not affect the review.

---

## 5. Worker Agent Instructions

Each worker agent receives a batch assignment (one of Batches A-F) and produces a findings report. The worker needs only this rubric document and CONTRIBUTING-SKILLS.md to perform the review.

### Prerequisites

Before starting, the worker agent must have access to:

1. **This rubric** -- `docs/fleet-review-rubric.md` (defines what to evaluate and how to score)
2. **CONTRIBUTING-SKILLS.md** -- skill authoring conventions and validation commands
3. **The skills directories** for the assigned batch categories
4. **`.claude-plugin/plugin.json`** -- to verify registration status

### Review Procedure

For each skill in the assigned batch, perform these steps in order:

**Step 1 -- Read the skill files.**

```bash
cat skills/<category>/<skill-name>/SKILL.md
cat skills/<category>/<skill-name>/details.md 2>/dev/null || echo "(no details.md)"
```

**Step 2 -- Check registration.**

```bash
jq -e --arg p "skills/<category>/<skill-name>" \
  '.skills[] | select(. == $p)' .claude-plugin/plugin.json > /dev/null 2>&1 \
  && echo "REGISTERED" || echo "NOT REGISTERED"
```

**Step 3 -- Measure description length.**

Extract the `description` field from the frontmatter and count characters. The validation script already reports per-skill warnings, but verify independently:

```bash
# Extract description from frontmatter (between --- fences)
awk '/^---$/{n++; next} n==1{print}' skills/<category>/<skill-name>/SKILL.md \
  | grep '^description:' | sed 's/^description: *//' | sed 's/^"//' | sed 's/"$//' | wc -c
```

**Step 4 -- Evaluate all 11 dimensions.**

Using the rubric definitions in section 1, assign a pass/warn/fail verdict for each dimension. Record notes for any non-pass verdict.

**Step 5 -- Check cross-references.**

For each `[skill:name]` reference in the SKILL.md, verify the target exists:

```bash
grep -o '\[skill:[^]]*\]' skills/<category>/<skill-name>/SKILL.md | while read ref; do
  target=$(echo "$ref" | sed 's/\[skill:\(.*\)\]/\1/')
  if [ -d "skills/*/$target" ] 2>/dev/null || find skills -type d -name "$target" | grep -q .; then
    echo "OK: $target"
  else
    echo "MISSING: $target"
  fi
done
```

Also check for bare-text skill references (skill names mentioned without the `[skill:]` wrapper):

```bash
# Look for known skill directory names mentioned as plain text (not in [skill:] syntax)
# This is a heuristic check -- review manually for false positives
```

**Step 6 -- Check consistency with category peers.**

Compare the skill's structure (sections, headings, code block language tags, Agent Gotchas presence) against other skills in the same category. Note any significant deviations.

**Step 7 -- Record findings.**

Fill in the per-skill output template from section 3. Include all issues found with their priority classification.

### Output Format

Each worker produces a findings report at `docs/review-reports/batch-<letter>-findings.md` with this structure:

```markdown
# Batch <Letter> Findings: <Category Names>

## Summary

| Metric | Count |
|--------|-------|
| Skills reviewed | <N> |
| Clean | <N> |
| Needs Work | <N> |
| Critical | <N> |
| Total issues | <N> |
| Critical issues | <N> |
| High issues | <N> |
| Low issues | <N> |

## Current Description Budget Impact

| Metric | Value |
|--------|-------|
| Total description chars (this batch) | <N> |
| Skills over 120 chars | <N> |
| Projected savings if all trimmed to 120 | <N> chars |

## Findings by Skill

### <category-name>

<per-skill output template for each skill in category>

## Cross-Cutting Observations

<patterns that affect multiple skills in this batch>

## Recommended Changes

### Critical (must fix)
- <issue> in <skill> -- <fix>

### High (should fix)
- <issue> in <skill> -- <fix>

### Low (nice to have)
- <issue> in <skill> -- <fix>
```

### Timing and Dependencies

- Workers for Batches A-F can run in parallel (they read disjoint skill sets)
- No worker should modify any skill files during the audit phase
- Workers must not modify `plugin.json`, `AGENTS.md`, or `README.md` (owned by task 12)
- After all batch reports are complete, task 8 consolidates findings into `docs/review-reports/consolidated-findings.md`

### Quality Checks for Workers

Before submitting a findings report, verify:

1. Every skill in the assigned categories has an entry in the report
2. The skill count in the summary table matches the batch assignment table above
3. All cross-reference checks have been performed (not just sampled)
4. Description character counts are accurate (not estimated)
5. Priority classifications are consistent with the rubric definitions

---

## 6. Validation Baseline

Before any audit work begins, capture the current validation state as a baseline. Run all four validation commands and record the output:

```bash
./scripts/validate-skills.sh
./scripts/validate-marketplace.sh
python3 scripts/generate_dist.py --strict
python3 scripts/validate_cross_agent.py
```

The baseline as of this rubric's creation:

- **validate-skills.sh**: PASSED (0 errors, 33 warnings -- 32 description length warnings + 1 unresolved planned cross-ref)
- **Current description budget**: 12,458 / 15,000 chars (WARN status)
- **Skills validated**: 101 (99 registered + 2 unregistered multi-targeting)
- **Projected budget at 120 chars each**: 12,000 chars

This baseline allows workers to verify they are not introducing regressions during the implementation phase.

---

## References

- [CONTRIBUTING-SKILLS.md](../CONTRIBUTING-SKILLS.md) -- skill authoring conventions
- [CLAUDE.md](../CLAUDE.md) -- project conventions and validation commands
- [.claude-plugin/plugin.json](../.claude-plugin/plugin.json) -- skill registration
- [Anthropic Skill Authoring Guide](https://github.com/anthropics/agent-skills/blob/main/docs/skill-authoring-guide.md) -- upstream best practices
