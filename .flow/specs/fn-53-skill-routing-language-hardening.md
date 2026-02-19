# Skill Routing Language Hardening

## Overview

Standardize routing language across all 130 SKILL.md files and 14 agent files so skills are discovered reliably from non-specific prompts. Descriptions stay concise/high-signal within the 12K char budget, inter-skill references use canonical `[skill:name]` syntax everywhere, and scope/out-of-scope boundaries are explicit. Harden validation scripts and CI gates to enforce these standards going forward. Detect and prevent semantic overlap between descriptions that could cause routing confusion.

## Scope

**In scope:**
- All 130 `skills/**/SKILL.md` files (description, scope, out-of-scope, cross-references)
- All 14 `agents/*.md` files (bare-text references → `[skill:]` syntax)
- `scripts/_validate_skills.py` and `scripts/validate-skills.sh` (new checks)
- `tests/agent-routing/check-skills.cs` and `cases.json` (assertion hardening)
- `CONTRIBUTING-SKILLS.md`, `CONTRIBUTING.md`, `CLAUDE.md` (guidance updates)
- `.github/workflows/validate.yml` (CI gate updates)
- **Semantic similarity overlap detection** — stdlib-only multi-signal Python script (`scripts/validate-similarity.py`) that computes pairwise description similarity using set Jaccard + `difflib.SequenceMatcher` + category-aware adjustment. CI-gatable with suppression list for known-acceptable pairs.

**Out of scope:**
- Changing skill functionality or body content beyond routing sections
- Adding new skills or removing existing ones
- Changing the routing architecture (advisor → domain skill chain)
- `README.md` delegation flow diagrams (content lives there, not in AGENTS.md)
- Embedding-based similarity (sentence-transformers, OpenAI embeddings) — stdlib approach is sufficient for 130 descriptions

## Key Context

- Budget is at WARN threshold: ~12,345 chars current vs 12,000 warn / 15,600 fail (thresholds from `validate-skills.sh --warn-threshold 12000 --fail-threshold 15600`). All description changes must be budget-neutral or budget-negative.
- Research shows assertive cues in descriptions create 7x selection bias; position bias gives 80.2% selection rate to first-listed tools. Descriptions must be factual, not promotional.
- 58 skills have zero routing markers (no trigger, scope, or out-of-scope) per T1 baseline audit (`docs/skill-routing-audit-baseline.md`). These need markers added from scratch.
- All 14 agent files have bare-text references (64 total) per T1 baseline audit. These need normalization to `[skill:]` syntax.
- CI currently runs without `STRICT_REFS=1`, so cross-ref validation is lenient. Must enable strict mode.
- Prior art: fn-29 (fleet review), fn-37 (cleanup sweep), fn-49 (compliance review), fn-51 (frontmatter).
- **Historical reference**: `.flow/specs/skill-routing-language-hardening-plan.md` is the prior plan snapshot. The authoritative plan is THIS spec (`.flow/specs/fn-53-skill-routing-language-hardening.md`).

## Semantic Similarity Detection Design

**Problem**: Two descriptions sharing too much vocabulary cause routing confusion — the LLM picks the wrong skill. With 130 skills (8,385 pairs), manual review is infeasible.

**Approach**: Multi-signal composite score using Python stdlib only (no numpy, sklearn, sentence-transformers). Standalone script `scripts/validate-similarity.py`.

**Signals and composite formula:**

```
composite = 0.4 * set_jaccard + 0.4 * seqmatcher + (0.15 if same_category else 0.0)
```

1. **Set Jaccard** (0.4 weight): Tokenize → lowercase → strip domain stopwords → convert to `set(tokens)` → compute `|A ∩ B| / |A ∪ B|`. Use `set()`, NOT `Counter` (Jaccard is set-based, not multiset).
2. **SequenceMatcher ratio** (0.4 weight): `difflib.SequenceMatcher(a, b).ratio()` for structural/character-level similarity. Operates on raw descriptions (NOT stopword-stripped).
3. **Same-category adjustment** (+0.15 additive): If both items share the same category directory, add +0.15 directly to composite (intra-category overlap is MORE concerning). This is a flat additive boost, not a weighted signal.

**Agent category convention**: All 14 agents reside in the `agents/` directory, so all agent-agent pairs receive the +0.15 same-category boost. This is intentional — agents sharing a directory have higher confusion risk. If this produces excessive WARN pairs for agent-agent comparisons, address via the suppression list (add entries with rationale), not by exempting agents from the category boost.

**Domain stopwords** (authoritative list — stripped before set Jaccard only, NOT before SequenceMatcher):
`dotnet`, `net`, `apps`, `building`, `designing`, `using`, `writing`, `implementing`, `adding`, `creating`, `configuring`, `managing`, `choosing`, `analyzing`, `working`, `patterns`, `for`

This list is the initial starting point. T13 calibrates empirically: run against all descriptions, identify terms appearing in >30% of descriptions, add them. Changes to the stopword list require regenerating the similarity baseline in the same PR.

**Thresholds** (calibrated against actual data — max real pair: `dotnet-ado-publish` / `dotnet-gha-publish` at 0.71 SequenceMatcher):
- **INFO** at composite >= 0.40: reported but not flagged
- **WARN** at composite >= 0.55: needs review during sweeps
- **ERROR** at composite >= 0.75: must be differentiated or suppressed

**Canonical pair identity**: Pairs are identified by sorted tuple `(min(id_a, id_b), max(id_a, id_b))`. This ensures deterministic ordering in baseline/suppression files and stable diffs.

**Suppression list** (`scripts/similarity-suppressions.json`): JSON array of `{id_a, id_b, rationale}` where `id_a < id_b` (sorted). Field names use `id_a`/`id_b` (not `skill_a`/`skill_b`) because the similarity tool operates on both skill IDs and agent IDs. Suppressed pairs:
- Produce INFO-level output regardless of score
- Are excluded from "new WARN" baseline regression detection
- Are NOT counted in `PAIRS_ABOVE_WARN` or `PAIRS_ABOVE_ERROR`

**Baseline file** (`scripts/similarity-baseline.json`): JSON with `{version: 1, pairs: [...]}` where pairs are unsuppressed sorted tuples above WARN threshold. Suppressed pairs are excluded from the baseline. Schema-versioned for stable diffs. Sorted output for deterministic git diffs.

**Scope**: Both skill descriptions (130) AND agent descriptions (14) = 144 items, 10,296 pairs. Agent-skill confusion is just as problematic as skill-skill confusion.

**Output**: JSON report to stdout with per-pair detail + summary stats. Stable CI output keys on stderr: `MAX_SIMILARITY_SCORE`, `PAIRS_ABOVE_WARN`, `PAIRS_ABOVE_ERROR`.

**Exit code semantics**:
- Exit 0: No unsuppressed ERRORs AND no new WARNs (when baseline provided)
- Exit 1: Any unsuppressed ERROR pairs exist, OR any new WARN+ pairs not in baseline/suppressions (when baseline provided)
- Exit 2: Script error (bad args, missing files)

Both conditions are checked; either triggers exit 1. Counts for each condition are emitted separately in summary (`unsuppressed_errors`, `new_warns_vs_baseline`).

**Shared agent frontmatter parser**: Both T3 (`_validate_skills.py`) and T13 (`validate-similarity.py`) need agent description extraction. Factor the parser into a shared helper module (`scripts/_agent_frontmatter.py`). **Ownership: T3 creates and owns this file.** T13 imports it as a dependency but does not modify it. This prevents merge conflicts between parallel tasks.

**Parsing contract for `_agent_frontmatter.py`**: Parse only top-level scalar fields `name:` and `description:` with zero indentation. Supported value forms: plain scalars (`description: Some text`), single-quoted strings (`description: 'text'`), double-quoted strings (`description: "text"`), and block scalars (`|` / `>` with indented continuation lines). The parser MUST ignore sequences, flow constructs, and nested mappings — it returns `None` for fields it cannot parse. Both T3 and T13 import and call the same function; no duplicated parsing logic.

**Agent description extraction**: Agent frontmatter uses full YAML with sequences. The similarity script extracts `description:` values using the shared `_agent_frontmatter.py` module described above. This is the same code path used by T3's agent validation.

### Similarity CI Gate Phasing

Integration of similarity into CI happens in two phases to prevent baseline churn during sweeps:

1. **Phase 1 (T3, wave 3)**: `validate-skills.sh` invokes `validate-similarity.py` in **error-only mode** — no `--baseline` flag. CI fails only on unsuppressed ERROR pairs (composite >= 0.75). This prevents new egregious overlap but does not require baseline maintenance during sweeps. The invocation is guarded: `if [[ -f scripts/validate-similarity.py ]]; then ...`. This allows T3 to land wiring code before T13 delivers the script.

2. **Phase 2 (T12, wave 7)**: After all sweeps (T5-T10) and verification (T11) are complete, T12 enables `--baseline` regression gating. CI command becomes: `python3 scripts/validate-similarity.py --repo-root . --baseline scripts/similarity-baseline.json --suppressions scripts/similarity-suppressions.json`. This prevents new WARN+ pairs from regressing the post-sweep baseline.

**Stderr/stdout routing**: T13 prints stable CI keys to stderr per spec. T3's `validate-skills.sh` integration must capture similarity stderr and re-emit the keys to stdout so the existing CI capture mechanism (`tee` + `grep`) can parse them. Implementation: `python3 scripts/validate-similarity.py ... 2>&1` within the validate-skills.sh invocation, or parse stderr separately and echo keys to stdout.

**Wrapper `exec` removal**: The current `validate-skills.sh` uses `exec python3 _validate_skills.py ...` which replaces the shell process, preventing any subsequent commands. T3 must replace `exec` with a regular invocation, capture the validator's exit code, then run the guarded similarity check, and compose a final exit code (non-zero if either check fails).

## Cross-Reference Conventions

**Unified `[skill:]` syntax** — `[skill:name]` refers to any routable artifact (skills OR agents). The validator resolves references against the **union** of skill directory names + agent file names (stems without `.md`). This is consistent with how both skills and agents are loaded via the skill system. T3 must build a single "known IDs" set = `{skill directory names} ∪ {agent file stems}` for validation.

**ID collision detection** — The validator must check that the known IDs set has no collisions between skill directory names and agent file stems. If `skill_dirs ∩ agent_stems` is non-empty, emit a validation error: "ID collision between skill and agent: {name}. Rename one to avoid ambiguity." This is checked once at startup.

**Self-references** — A skill referencing itself via `[skill:]` is always an error.

**Cycles** — Bidirectional references (e.g., `dotnet-advisor` ↔ `dotnet-version-detection`) are legitimate and expected for hub skills. Cycle detection produces a **report** (informational), not validation errors. Self-references are the only structural error.

## Agent File Validation Strategy

Agent frontmatter uses full YAML with sequences (e.g., `preloaded-skills` lists). The SKILL validator's subset YAML parser (`_validate_skills.py`) rejects sequences. Therefore, agent validation uses a **dedicated `parse_agent_frontmatter()` function** from the shared `scripts/_agent_frontmatter.py` module. It does NOT reuse the SKILL YAML parser and does NOT attempt to parse sequences.

## Bare-Reference Detection Strategy

Bare-ref detection (backtick-wrapped or bold-wrapped identifiers like `` `dotnet-testing-specialist` ``) uses an **allowlist of known IDs**: the union of skill directory names and agent file stems. Only tokens matching known IDs are flagged. This avoids false positives on .NET CLI tools (`dotnet-counters`, `dotnet-trace`, `dotnet-dump`, etc.) and other non-skill identifiers.

**Exclusion rule**: Bare-ref scanning must **ignore any occurrence within `[skill:...]` spans** (and within link URLs). A naive regex match for bare `dotnet-foo` would false-positive on every valid `[skill:dotnet-foo]` reference. The implementation must strip or skip `[skill:...]` spans before scanning for bare refs.

**Scope**: Bare-ref detection applies to both individual `agents/*.md` files AND `AGENTS.md`. The same allowlist and exclusion rule are used in both contexts.

## Budget Threshold Semantics

- Acceptance criterion: `CURRENT_DESC_CHARS < 12,000` (strictly less than). All tasks must use this exact comparison.
- `BUDGET_STATUS` in validator output reflects CURRENT chars only. T3 must update `_validate_skills.py` to **decouple projected from budget status**: `BUDGET_STATUS` = `OK` if `CURRENT_DESC_CHARS < 12,000`, `WARN` if `>= 12,000`, `FAIL` if `>= 15,600`. The current validator conflates projected and current in its status computation — T3 fixes this.
- `PROJECTED_DESC_CHARS` is reported as a separate informational metric, not included in `BUDGET_STATUS`.
- The validator's WARN condition triggers at `>= 12,000`, so reaching exactly 12,000 counts as WARN. Acceptance requires being below this threshold.

## Routing Warnings Baseline

The committed baseline file (`scripts/routing-warnings-baseline.json`) contains **per-key stable counters** (e.g., `MISSING_SCOPE_COUNT`, `MISSING_OOS_COUNT`, `SELF_REF_COUNT`, `AGENT_BARE_REF_COUNT`, `AGENTSMD_BARE_REF_COUNT`), NOT the aggregate `Warnings: N` total. CI compares each individual key against its baseline value. This prevents false regressions from one check improving while another regresses. Format: `{"version": 1, "keys": {"MISSING_SCOPE_COUNT": 0, ...}}`.

## Routing Test Evidence Invariant

T4 must update both `cases.json` evidence patterns AND the `BuildRequiredAllEvidence()` method in `check-skills.cs`. Currently, `BuildRequiredAllEvidence()` injects both generic `"SKILL.md"` and skill-specific `"<expectedSkill>/SKILL.md"` for non-Claude agents. The new invariant: when `ExpectedSkill` is present, require **only** the skill-specific path (`"<expectedSkill>/SKILL.md"`), not the generic `"SKILL.md"`. This prevents false-positive matches from incidental `SKILL.md` mentions. Claude evidence (Skill tool invocation tokens) is unchanged.

**Failure taxonomy update**: T4 must also update `ClassifyFailure()` to recognize the new skill-specific evidence pattern. Currently `ClassifyFailure()` detects `MissingSkillFileEvidence` via `MissingAll.Contains("SKILL.md")`. After T4's change, the generic string won't be in the required set. Update to: detect missing skill-file evidence as any missing token that `EndsWith("/SKILL.md")`. This preserves the failure taxonomy guarantee for downstream CI/reporting. Claude agents remain excluded from skill-file evidence as designed.

## Quick commands

```bash
# Validate skills
./scripts/validate-skills.sh

# Validate marketplace
./scripts/validate-marketplace.sh

# Run similarity check
python3 scripts/validate-similarity.py --repo-root .

# Run routing tests (single case)
./test.sh --agents claude --case-id foundation-routing
```

## Acceptance

- [ ] All 130 SKILL.md descriptions follow canonical style guide from task 2
- [ ] All cross-references in skills AND agent files use `[skill:name]` syntax (unified syntax for skills and agents)
- [ ] All skills have explicit scope/out-of-scope sections
- [ ] Validator enforces new routing-language quality checks (skills and agents via separate code paths)
- [ ] Routing compliance report generates per-skill compliance data
- [ ] Routing test assertions use definitive proof (Skill tool invocation, not text mentions)
- [ ] Semantic similarity script detects pairwise description overlap using multi-signal composite score (stdlib-only)
- [ ] Similarity CI gate prevents new high-overlap pairs (baseline + suppression list)
- [ ] Similarity WARN pairs reduced vs pre-sweep baseline after T5-T9 sweeps
- [ ] `./scripts/validate-skills.sh` passes with zero errors
- [ ] `./scripts/validate-marketplace.sh` passes
- [ ] CI gates updated: `STRICT_REFS=1` enabled, zero errors enforced, zero new warnings vs per-key baseline
- [ ] CONTRIBUTING-SKILLS.md, CLAUDE.md, CONTRIBUTING.md updated with canonical conventions (including similarity avoidance guidance)
- [ ] CHANGELOG.md entry added
- [ ] `CURRENT_DESC_CHARS < 12,000` (strictly below WARN threshold)

## Dependency Graph

```text
T1 → T2 → {T3, T4, T13} → T5 → {T6, T7, T8, T9, T10} → T11 → T12
```

Note: T5 explicitly depends on T1 (ownership manifest), T3, T4, and T13.

**T3/T13 parallel strategy**: T3 and T13 execute in parallel in wave 3. T3 implements all core validator checks independently and **creates `scripts/_agent_frontmatter.py`** (sole owner). T3 also writes the similarity wiring code in `validate-skills.sh` and `validate.yml` against T13's documented CLI interface, guarded by `if [[ -f scripts/validate-similarity.py ]]`. T13 **imports** `_agent_frontmatter.py` when available but has a **skills-only fallback**: if the module is absent, T13 processes only the 130 skill descriptions (skips agents) with a stderr warning. This means both T3 and T13 are independently landable in any order. Once both have landed, re-running similarity produces the full 144-item result. Full integration testing of similarity wiring happens in T11.

Waves:
1. T1 (audit)
2. T2 (spec)
3. T3 + T4 + T13 (tooling + similarity, parallel)
4. T5 (foundation + high-traffic)
5. T6 + T7 + T8 + T9 + T10 (sweeps + agents, parallel)
6. T11 (verification)
7. T12 (docs + CI + rollout)

## References

- Agent Skills spec: https://agentskills.io/specification
- Anthropic best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Existing validator: `scripts/_validate_skills.py`
- Routing tests: `tests/agent-routing/check-skills.cs`
- Prior art — similarity validation: KentoShimizu/sw-agent-skills `validate_skill_similarity.py` (difflib-based)
- Prior art — multi-signal pattern similarity: nibzard/awesome-agentic-patterns (Jaccard + Levenshtein + category, 3.3K stars)
- Prior art — tool boundary analysis: Abdulk084/tool-boundary-analyzer (TF-IDF + semantic, pip-installable)
- Research — MCP tool description smells: arxiv 2602.14878v1 (97.1% have quality issues)
- Research — tool deduplication threshold: arxiv 2511.01854 (0.82 cosine optimal for merging)
