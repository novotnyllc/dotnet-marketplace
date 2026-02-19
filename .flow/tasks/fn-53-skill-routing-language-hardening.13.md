# fn-53-skill-routing-language-hardening.13 Semantic Similarity Overlap Detection Script

## Description
Build a standalone Python 3 script (`scripts/validate-similarity.py`) that computes pairwise semantic similarity between all skill AND agent descriptions using a multi-signal composite score. Zero external dependencies (stdlib only). CI-gatable with suppression list for known-acceptable pairs.

**Size:** M
**Files:**
- `scripts/validate-similarity.py` (new — ~150-200 lines)
- `scripts/similarity-suppressions.json` (new — known-acceptable pairs)
- `scripts/similarity-baseline.json` (new — committed baseline of pairs above WARN)

**File ownership boundary:** T13 delivers the standalone script and its data files. T13 does NOT edit `scripts/validate-skills.sh` or `.github/workflows/validate.yml` — those integrations are owned by T3. T13 does NOT create or modify `scripts/_agent_frontmatter.py` — T3 owns that file. T13 **imports** `_agent_frontmatter.py` as a dependency.

## Approach

**Multi-signal composite score** (all Python stdlib):

Composite formula (authoritative — matches epic spec):
```
composite = 0.4 * set_jaccard + 0.4 * seqmatcher + (0.15 if same_category else 0.0)
```

1. **Set Jaccard** (weight 0.4): Tokenize description → lowercase → strip domain stopwords → convert to `set(tokens)` (NOT Counter/multiset) → compute `|A ∩ B| / |A ∪ B|`. Handle empty-after-stripping edge case (return 0.0, do not crash).

2. **SequenceMatcher ratio** (weight 0.4): `difflib.SequenceMatcher(a=desc_a, b=desc_b).ratio()`. Operates on raw descriptions (NOT stopword-stripped) to capture character-level structural similarity.

3. **Same-category adjustment** (+0.15 additive): If both items share the same category directory, add +0.15 directly to composite. This is a flat additive boost, not a weighted signal. Cross-category pairs get +0.0.

**Agent category convention**: All agents reside in the `agents/` directory, so all agent-agent pairs receive the +0.15 same-category boost. This is intentional. If this produces excessive WARN pairs for agent-agent comparisons, address via the suppression list with explicit rationale, not by exempting agents from the category boost.

**Domain stopwords** (authoritative list — matches epic spec, stripped before set Jaccard only):
`dotnet`, `net`, `apps`, `building`, `designing`, `using`, `writing`, `implementing`, `adding`, `creating`, `configuring`, `managing`, `choosing`, `analyzing`, `working`, `patterns`, `for`

This is the initial starting point. During implementation, run against all 144 descriptions, identify terms appearing in >30% of descriptions, and add them. Changes to stopwords require regenerating baseline in the same PR.

**Canonical pair identity**: Pairs identified by sorted tuple `(min(id_a, id_b), max(id_a, id_b))`. This ensures deterministic ordering in all output, baseline, and suppression files.

**Thresholds** (calibrate against actual data — see Key context):
- INFO: composite >= 0.40 (reported in JSON, not flagged)
- WARN: composite >= 0.55 (needs review)
- ERROR: composite >= 0.75 (must differentiate or suppress)

**Suppression list** (`scripts/similarity-suppressions.json`):
```json
[
  {
    "id_a": "dotnet-ado-publish",
    "id_b": "dotnet-gha-publish",
    "rationale": "Intentional parallel descriptions for different CI systems"
  }
]
```
Where `id_a < id_b` (sorted). Field names use `id_a`/`id_b` (not `skill_a`/`skill_b`) because the tool operates on both skill and agent IDs. Suppressed pairs:
- Produce INFO-level output regardless of score
- Are excluded from "new WARN" baseline regression detection
- Are NOT counted in `PAIRS_ABOVE_WARN` or `PAIRS_ABOVE_ERROR`

**Input scope**: Process all 130 skill descriptions from `skills/**/SKILL.md` AND all 14 agent descriptions from `agents/*.md`. Total: 144 items, 10,296 pairs.

**Agent description extraction**: Import `scripts/_agent_frontmatter.py` (created and owned by T3). Use the shared `parse_agent_frontmatter()` function — do not duplicate or modify the parsing logic. **Skills-only fallback**: If `_agent_frontmatter.py` is not present at import time (T3 hasn't landed yet), run in skills-only mode: process only the 130 skill descriptions, skip agent descriptions, and log a warning to stderr ("_agent_frontmatter.py not found — running in skills-only mode, agent descriptions excluded"). This preserves true parallelism: T13 can land independently of T3. Once both have landed, re-running produces the full 144-item result.

**Output**: JSON report to stdout with:
- `pairs`: array of `{id_a, id_b, composite, jaccard, seqmatcher, same_category, level}` for all pairs above INFO, sorted by composite descending
- `summary`: `{total_items, total_pairs, max_score, pairs_above_warn, pairs_above_error, suppressed_count, unsuppressed_errors, new_warns_vs_baseline}`
- Stable CI output keys printed to stderr: `MAX_SIMILARITY_SCORE=<float>`, `PAIRS_ABOVE_WARN=<N>`, `PAIRS_ABOVE_ERROR=<N>`

**Exit code semantics** (both conditions checked; either triggers exit 1):
- Exit 0: No unsuppressed ERROR pairs AND no new WARNs vs baseline (when baseline provided)
- Exit 1: Any unsuppressed ERROR pairs exist, OR any new WARN+ pairs not in baseline/suppressions
- Exit 2: Script error (bad args, missing files)
Counts for each condition emitted separately in summary.

**Baseline file** (`scripts/similarity-baseline.json`):
```json
{"version": 1, "pairs": [["dotnet-foo", "dotnet-bar"], ...]}
```
Schema-versioned. Pairs are sorted tuples above WARN threshold, sorted lexicographically. Deterministic output for stable git diffs.

**CLI interface**:
```bash
python3 scripts/validate-similarity.py --repo-root . [--suppressions scripts/similarity-suppressions.json] [--warn-threshold 0.55] [--error-threshold 0.75] [--baseline scripts/similarity-baseline.json]
```

## Key context

- **Actual similarity data** (from gap analysis live run): highest real pair is `dotnet-ado-publish` / `dotnet-gha-publish` at 0.71 SequenceMatcher. This is an intentional parallel pair. Next: `dotnet-data-access-strategy` / `dotnet-service-communication` at 0.62, `dotnet-gha-deploy` / `dotnet-gha-publish` at 0.61. Thresholds must account for these.
- **Prior art**: KentoShimizu/sw-agent-skills `validate_skill_similarity.py` (difflib.SequenceMatcher, threshold 0.96, zero deps). Our approach adds set Jaccard and category awareness for better precision on short domain-specific text.
- **No external deps**: Validator is stdlib-only. Similarity script follows same constraint. Only use: `difflib`, `collections`, `re`, `argparse`, `json`, `sys`, `pathlib`, `math`.
- **Performance**: 10,296 pairs with tokenization + 2 similarity computations each. Typically <2 seconds on modern hardware; acceptance gate is <5 seconds.
- **File ownership**: T13 does NOT edit `validate-skills.sh` or `validate.yml` (T3 owns). T13 does NOT create or modify `_agent_frontmatter.py` (T3 owns). T13 imports `_agent_frontmatter.py`.
- Memory pitfall: "Proposed replacement descriptions must have character counts verified" — similarity script must use consistent tokenization across runs for deterministic scores.

## Acceptance
- [ ] `scripts/validate-similarity.py` exists, runs with `python3`, zero external dependencies
- [ ] Composite formula matches epic spec: `0.4 * set_jaccard + 0.4 * seqmatcher + (0.15 if same_category else 0.0)`
- [ ] Set Jaccard uses `set(tokens)` (NOT Counter/multiset)
- [ ] Domain stopwords match epic spec authoritative list, stripped before Jaccard only
- [ ] Processes both skill descriptions (130) AND agent descriptions (14) — 144 items total
- [ ] Agent descriptions extracted via shared `_agent_frontmatter.py` (imported from T3, not duplicated)
- [ ] Canonical pair identity: sorted tuple `(min(id_a, id_b), max(id_a, id_b))`
- [ ] JSON output with per-pair detail + summary stats, sorted by composite descending
- [ ] Stable CI output keys on stderr: `MAX_SIMILARITY_SCORE`, `PAIRS_ABOVE_WARN`, `PAIRS_ABOVE_ERROR`
- [ ] Suppression list (`scripts/similarity-suppressions.json`) with `id_a < id_b` ordering; at least `dotnet-ado-publish` / `dotnet-gha-publish` pair
- [ ] Suppressed pairs produce INFO, excluded from WARN/ERROR counts and baseline regression
- [ ] Baseline mode (`--baseline`) detects NEW pairs above WARN not in baseline or suppression list
- [ ] `scripts/similarity-baseline.json` committed with `{version: 1, pairs: [...]}` schema, sorted output
- [ ] Exit code 0 when no unsuppressed ERRORs AND no new WARNs vs baseline; exit 1 otherwise; exit 2 on script error
- [ ] Thresholds calibrated against actual data: zero false-positive ERRORs on current descriptions (after suppression)
- [ ] Empty/missing descriptions handled without crash (return 0.0 for pair, skip from results)
- [ ] Deterministic output: same input → same JSON output
- [ ] Performance: completes in < 5 seconds for 144 items
- [ ] Skills-only fallback: runs in skills-only mode (130 items) with stderr warning if `_agent_frontmatter.py` not present
- [ ] Does NOT create, modify, or duplicate `_agent_frontmatter.py` (T3 owns that file)
- [ ] Does NOT edit `validate-skills.sh` or `validate.yml` (T3 owns those)
- [ ] `./scripts/validate-skills.sh` still passes
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
