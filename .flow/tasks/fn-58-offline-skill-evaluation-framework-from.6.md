# fn-58-offline-skill-evaluation-framework-from.6 Size impact and progressive disclosure evals

## Description

Add size impact evals (L6 runner) that test whether skill content format affects output quality: full SKILL.md body vs deterministic summary extract vs no skill. Uses shared infrastructure from `_common.py` and judge from `judge_prompt.py` (task .3).

**Size:** M
**Files:**
- `tests/evals/run_size_impact.py` (L6 runner)
- `tests/evals/datasets/size_impact/candidates.yaml` (skills selected for size testing, with size metadata and sibling allowlists)

## Approach

- For each candidate skill, generate code under three conditions:
  1. **Full**: Complete SKILL.md body (frontmatter stripped, explicit delimiters)
  2. **Summary**: Deterministic summary extraction (see algorithm below)
  3. **Baseline**: No skill content

- **Deterministic Summary Extraction Algorithm**:
  1. Strip YAML frontmatter (between first/second `---`)
  2. Extract `## Scope` section (from heading to next `##` or EOF)
  3. Strip code fences and contents (regex: triple-backtick blocks)
  4. Strip `[skill:...]` cross-references (keep surrounding text)
  5. Concatenate: frontmatter `description` + newline + extracted scope text
  6. Record exact bytes and estimated token count per condition in results

- Judge all three pairwise via `judge_prompt.invoke_judge()`:
  - Full vs Baseline, Full vs Summary, Summary vs Baseline
  - Call signature: `judge_prompt.invoke_judge(client, user_prompt, response_a, response_b, criteria, judge_model, temperature=0.0, max_retries=2)`
  - Returns dict: `{"parsed": dict|None, "raw_judge_text": str, "cost": float, "attempts": int, "judge_error": str|None}`
  - Parsed JSON shape: `{"criteria": [{"name", "score_a", "score_b", "reasoning"}], "overall_winner": "A"|"B"|"tie"}`
  - Scores are integers 1-5; remap score_a/score_b to condition labels based on your A/B assignment
<!-- Updated by plan-sync: fn-58...from.3 — judge_prompt.invoke_judge() API finalized with above signature and return shape -->

- **Candidate selection** (8-10 skills in `candidates.yaml`):
  - Small (<5KB body), Medium (5-15KB), Large (>15KB)
  - Note: no skills in the 131-skill catalog have a body under 2KB (min ~3KB), so thresholds are adapted from the original <2KB/2-5KB/>5KB to produce meaningful tier separation
  - Skills with sibling files: define in `candidates.yaml` with explicit allowlist:
    ```yaml
    - skill: dotnet-example
      siblings: ["details.md", "reference.md"]
      max_sibling_bytes: 10000
    ```
  - Total sibling cap per skill to avoid pulling huge files

- **Sibling testing**: For skills with `siblings` defined, add a fourth condition:
  - **Full + Siblings**: SKILL.md body + concatenated sibling contents (ordered per allowlist)
  - Compare: Full vs Full+Siblings (do siblings add value?)

- Resume/replay: generations cached in `results/generations/`

## Key context

- Progressive disclosure validated as right solution for oversized skills.
- Summary extraction must be deterministic for reproducible results.
- Sibling testing uses explicit allowlists, not glob patterns, to prevent accidental large file inclusion.

## Acceptance
- [ ] `run_size_impact.py` (L6) generates code under Full, Summary, and Baseline conditions
- [ ] Summary extraction uses deterministic algorithm (strip frontmatter -> extract Scope -> strip fences -> strip cross-refs -> concatenate)
- [ ] Exact bytes and estimated token count recorded per condition per case
- [ ] At least 8 candidate skills spanning small, medium, and large sizes
- [ ] Pairwise comparisons scored by LLM judge via `judge_prompt.py`
- [ ] `--dry-run` mode supported
- [ ] `--skill <name>` filters to a single candidate (errors if not in candidates.yaml)
- [ ] At least 2 skills with sibling files tested; siblings defined via explicit allowlist in `candidates.yaml` with `max_sibling_bytes` cap
- [ ] Results include per-skill size tier, per-comparison scores, winner, injected bytes/estimated tokens
- [ ] Resume/replay supported: generations cached
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
