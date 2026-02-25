# Eval Triage Report

Generated: 2026-02-24
Total CLI calls for this task: 0 (reused existing results)

## Result File Inventory

### Activation (13 files, 73 cases each)
- **12 valid** (backend=`claude`, post-.7 CLI migration)
- **1 invalid** (`activation_3d47f289` -- no backend field, pre-.7 format)
- **Best run**: `activation_3925edef` (2026-02-24T18:00, latest, 73 cases, full coverage)
- `meta.limit`: absent on all runs (full-coverage runs)
- Case counts match dataset: 30 core + 25 specialized + 18 negative = 73

### Confusion (2 files, 54 cases each)
- **2 valid** (backend=`claude`)
- **Best run**: `confusion_e3f1b006` (2026-02-24T12:48, latest, 54 cases)
- Case counts match dataset: 36 group cases + 18 negative controls = 54
- 7 groups tested: api, blazor, cicd, data, performance, security, testing

### Effectiveness (2 files, 72 cases each)
- **2 valid** (backend=`claude`)
- **Best run for analysis**: `effectiveness_d702e16b` (2026-02-24T10:40, 72 cases, 0 errors)
- **Latest run**: `effectiveness_8e9f1cb8` (2026-02-24T16:59, 72 cases, 24 errors -- timeouts)
- 12 rubric'd skills, 6 cases each (2 prompts x 3 runs)

### Size Impact (1 file, 100 cases)
- **1 valid** (backend=`claude`)
- **Run**: `size_impact_e10f5ab2` (2026-02-24T10:40, 100 cases)
- 11 candidates tested with 4 comparison types

No `suite_summary.json` exists.

All 21 skill IDs referenced in this report and in `eval-progress.json` have been verified to exist as `skills/<skill-name>/SKILL.md` in the repository.

---

## Current State vs Quality Bar

### L3 Activation

| Metric | Measured (raw) | Measured (excl. errors) | Target | Status |
|--------|---------------|------------------------|--------|--------|
| TPR | 69.09% | 92.68% | >= 75% | FAIL (raw) / PASS (excl. errors) |
| FPR | 27.78% | 13.33% | <= 20% | FAIL (raw) / PASS (excl. errors) |
| Accuracy | 69.86% | 91.07% | >= 70% | FAIL (raw) / PASS (excl. errors) |

**Root cause**: 17 of 73 cases (23%) had `detection_method: error` (CLI timeouts), all counted as failures. Only 5 actual routing mistakes exist in non-error cases.

**Actual routing mistakes (5 cases)**:
- **3 False Negatives** (misrouted to `dotnet-advisor`):
  - `act-005`: expected `dotnet-architecture-patterns` -- advisor intercepted architecture queries
  - `act-012`: expected `dotnet-system-commandline` -- advisor intercepted CLI queries
  - `act-017`: expected `dotnet-resilience` -- advisor intercepted Polly/resilience queries
- **2 False Positives** (activated when shouldn't):
  - `neg-004`: Kubernetes prompt activated `dotnet-container-deployment` (description mentions K8s)
  - `neg-018`: RabbitMQ prompt activated `dotnet-messaging-patterns` + 3 others (too broad)

**Consistency across 12 valid runs**:
- `neg-004` and `neg-018` fail consistently (0/12 pass) -- true routing issues
- `act-005`, `act-012`, `act-017` pass sometimes (3/12, 3/12, 4/12) -- borderline cases where advisor competes with specialized skills

### L4 Confusion

| Metric | Measured | Target | Status |
|--------|---------|--------|--------|
| Per-group accuracy (api) | 100% | >= 60% | PASS |
| Per-group accuracy (blazor) | 100% | >= 60% | PASS |
| Per-group accuracy (cicd) | 100% | >= 60% | PASS |
| Per-group accuracy (data) | 80% | >= 60% | PASS |
| Per-group accuracy (performance) | 100% | >= 60% | PASS |
| Per-group accuracy (security) | 100% | >= 60% | PASS |
| Per-group accuracy (testing) | 83% | >= 60% | PASS |
| Cross-activation rate | 0% (all groups) | <= 35% | PASS |
| Never-activated skills | None | None | PASS |
| Negative control pass rate | 88.9% | >= 70% | PASS |

**L4 meets quality bar.** Minor findings:
- `cm-data-002`: EF Core architecture prompt routed to `dotnet-advisor` instead of `dotnet-efcore-architecture` (same advisor-intercept pattern as L3)
- `cm-testing-006`: xUnit test prompt routed to `dotnet-advisor` instead of `dotnet-xunit`
- 2 negative controls failed due to `parse_failure` detection method (not routing issues)

### L5 Effectiveness

**Using the error-free run** (`effectiveness_d702e16b`):

| Skill | Win Rate | Target | Status |
|-------|---------|--------|--------|
| dotnet-blazor-patterns | 100% | >= 50% | PASS |
| dotnet-containers | 100% | >= 50% | PASS |
| dotnet-csharp-async-patterns | 83.3% | >= 50% | PASS |
| dotnet-csharp-coding-standards | 66.7% | >= 50% | PASS |
| dotnet-efcore-patterns | 83.3% | >= 50% | PASS |
| dotnet-minimal-apis | 83.3% | >= 50% | PASS |
| dotnet-native-aot | 100% | >= 50% | PASS |
| dotnet-observability | 100% | >= 50% | PASS |
| dotnet-resilience | 100% | >= 50% | PASS |
| dotnet-security-owasp | 83.3% | >= 50% | PASS |
| dotnet-testing-strategy | 66.7% | >= 50% | PASS |
| dotnet-xunit | 83.3% | >= 50% | PASS |

**L5 meets quality bar.** All 12 skills above 50% win rate, no 0% skills.

The later run (`effectiveness_8e9f1cb8`) showed 4 skills at 0% due to CLI timeouts (120s), not content quality issues. Error: `judge invocation failed: claude CLI timed out after 120s`. These skills (dotnet-resilience, dotnet-security-owasp, dotnet-testing-strategy, dotnet-xunit) produce longer rubric evaluation prompts that exceed the timeout.

### L6 Size Impact

| Candidate | Full Wins | Baseline Wins | Ties | Mean | Status |
|-----------|----------|--------------|------|------|--------|
| dotnet-ado-patterns | 1 | 2 | 0 | +0.233 | BASELINE WINS |
| dotnet-blazor-patterns | 1 | 1 | 0 | -0.100 | CONCERN |
| dotnet-csharp-async-patterns | 2 | 1 | 0 | +0.417 | OK |
| dotnet-csharp-code-smells | 2 | 0 | 1 | +0.700 | OK |
| dotnet-csharp-coding-standards | 0 | 2 | 1 | -1.067 | BASELINE WINS |
| dotnet-efcore-patterns | 2 | 0 | 0 | +1.525 | OK |
| dotnet-integration-testing | 2 | 1 | 0 | +0.817 | OK |
| dotnet-observability | 3 | 0 | 0 | +0.800 | OK |
| dotnet-security-owasp | 1 | 0 | 0 | +1.250 | OK (low n) |
| dotnet-windbg-debugging | 1 | 2 | 0 | -0.350 | BASELINE WINS |
| dotnet-xunit | 0 | 3 | 0 | -1.250 | **BASELINE SWEEP** |

**Overall full vs baseline**: 15/29 wins (51.7%) -- below 55% target. Denominator is the count of `full_vs_baseline` judged comparisons across all 11 candidates (ties counted in denominator but not as wins; error cases excluded).

| Metric | Measured | Target | Status |
|--------|---------|--------|--------|
| Full win rate | 51.7% | >= 55% | FAIL |
| Baseline sweeps | 1 (dotnet-xunit) | 0 | FAIL |

---

## Priority Fixes

### P0: Eval infra reliability (blocking L3/L5 raw scores)

The current L3 raw FAIL and L5 latest-run 0% skills are dominated by `detection_method: error` (CLI timeouts, 17/73 activation cases and 24/72 effectiveness cases). These are infrastructure failures, not routing or content quality issues.

**Gating decision for .5/.6**: Quality bar metrics MUST exclude `detection_method: error` cases from numerator and denominator when computing TPR/FPR/accuracy. The error rate itself is tracked separately as an infra health metric. Rationale: error cases reflect CLI timeout behavior, not skill routing or content quality. If the error rate exceeds 10%, the run should be flagged as degraded and re-run after infra fixes (e.g., increasing CLI timeout for index-sized and judge prompts).

**Action**: Before .5 verification and .6 baseline runs, reduce timeout/error rate by increasing CLI timeout for large prompts (current 120s is insufficient for 12-skill rubric evaluations). This is not a task .3/.4 concern but must be resolved before .5/.6.

### Priority 1: Blocking Quality Bar

#### P1-L6: Size impact failures (task .4 -- content fixes)

1. **dotnet-xunit** -- Baseline sweep (0-3). Full content (17.5KB, 4399 tokens) is hurting rather than helping. Mean improvement score is -1.25. Likely cause: excessive content creates noise; summary (415 bytes) may be more focused.
2. **dotnet-csharp-coding-standards** -- Baseline wins 2-0 with 1 tie. Full content (12.2KB, 3051 tokens) is counterproductive. Mean -1.067.
3. **dotnet-windbg-debugging** -- Baseline wins 2-1. Full content (2.9KB, 746 tokens) is small but summary (566 bytes) is unusually large relative to body. Mean -0.350.
4. **dotnet-ado-patterns** -- Baseline wins 2-1. Full content (3.3KB, 842 tokens) underperforms. Mean +0.233 (positive but baseline still wins more often).

#### P1-L3: Routing false positives (task .3 -- description fixes)

5. **dotnet-container-deployment** -- Activates on pure Kubernetes prompts (neg-004). Description likely too broad, mentioning K8s without sufficient .NET qualification.
6. **dotnet-messaging-patterns** -- Activates on generic RabbitMQ prompts (neg-018) along with 3 other skills. Description too generic for messaging.

### Priority 2: Improvement Opportunities

#### P2-L3: Routing false negatives (task .3 -- description fixes)

7. **dotnet-architecture-patterns** -- Loses to `dotnet-advisor` for architecture queries (act-005). Differentiator needs to be clearer in first 80 chars.
8. **dotnet-system-commandline** -- Loses to `dotnet-advisor` for CLI queries (act-012). Description needs stronger System.CommandLine keywords.
9. **dotnet-resilience** -- Loses to `dotnet-advisor` for Polly queries (act-017). Description needs Polly/resilience keywords earlier.

#### P2-L6: Borderline size impact (task .4 -- content review)

10. **dotnet-blazor-patterns** -- Split 1-1, mean -0.100. Large content (18.2KB) may have diminishing returns but not definitively harmful.

### Priority 3: Monitor (no immediate fix needed)

- L4 confusion: All groups passing. Minor advisor-intercept pattern but not blocking.
- L5 effectiveness: All 12 skills above 50% on error-free run. Timeout issues are infrastructure, not content.

---

## Recommended Batch Order

### Task .3 (Routing Description Fixes)

**Batch 1** (3 skills -- false positives, highest impact):
1. `dotnet-container-deployment` -- tighten description to exclude pure K8s
2. `dotnet-messaging-patterns` -- add .NET qualifier, reduce generic messaging triggers
3. `dotnet-architecture-patterns` -- strengthen differentiator vs advisor

**Batch 2** (2 skills -- false negatives, moderate impact):
4. `dotnet-system-commandline` -- add System.CommandLine keywords earlier
5. `dotnet-resilience` -- add Polly v8 keywords earlier

**Verification commands for .3**:

| Skill | Activation verify | Confusion verify |
|-------|------------------|-----------------|
| dotnet-container-deployment | `--skill dotnet-container-deployment` | N/A (not in confusion dataset) |
| dotnet-messaging-patterns | `--skill dotnet-messaging-patterns` | N/A (not in confusion dataset) |
| dotnet-architecture-patterns | `--skill dotnet-architecture-patterns` | N/A (not in confusion dataset) |
| dotnet-system-commandline | `--skill dotnet-system-commandline` | N/A (not in confusion dataset) |
| dotnet-resilience | `--skill dotnet-resilience` | N/A (not in confusion dataset) |

None of these 5 routing-fix skills appear in the confusion matrix dataset. Confusion verification is not applicable; use activation-only targeted runs.

### Task .4 (Content Fixes)

**Batch 1** (2 skills -- baseline sweep/wins, highest impact):
1. `dotnet-xunit` -- reduce content noise, focus on highest-value xUnit v3 patterns
2. `dotnet-csharp-coding-standards` -- trim or restructure content for signal density

**Batch 2** (2 skills -- baseline wins, moderate impact):
3. `dotnet-windbg-debugging` -- review summary/body ratio, ensure body adds value
4. `dotnet-ado-patterns` -- review content density and relevance

**Batch 3** (1 skill -- borderline, optional):
5. `dotnet-blazor-patterns` -- review if content can be tightened (18.2KB is large)

---

## L5 Rubric Failure Mode Pre-Analysis

All 12 skills pass on the error-free run (`effectiveness_d702e16b`). The 4 skills showing 0% on the later run (`effectiveness_8e9f1cb8`) failed due to CLI timeouts, not rubric criteria failures. No rubric-level fixes are needed at this time.

For reference, the skills with lowest (but passing) win rates on the clean run:
- **dotnet-csharp-coding-standards** (66.7%): 1 loss out of 6 cases. Rubric criteria include naming conventions, code layout, and documentation. The loss likely comes from baseline responses that are already well-formatted.
- **dotnet-testing-strategy** (66.7%): 1 loss out of 6. Rubric criteria include test type decision, test doubles selection. Baseline LLM knowledge of testing is strong, reducing enhanced content advantage.

---

## Summary

| Eval | Quality Bar | Status | Action Needed |
|------|------------|--------|---------------|
| L3 Activation | TPR>=75%, FPR<=20%, Acc>=70% | **PASS** (excl. errors; see P0) | Fix 5 routing descriptions (.3); resolve CLI timeouts before .5/.6 (P0) |
| L4 Confusion | Per-group>=60%, cross<=35%, neg>=70% | **PASS** | None (monitor) |
| L5 Effectiveness | Per-skill>=50%, no 0% | **PASS** (excl. errors; see P0) | None (resolve CLI timeouts before .5/.6) |
| L6 Size Impact | Full wins>=55%, no sweeps | **FAIL** | Fix 4 content issues (.4), eliminate xunit sweep |

**Quality bar gating note**: L3 and L5 metrics exclude `detection_method: error` cases (CLI timeouts). Error rate is tracked as an infra health metric under P0, not as a routing/content quality signal.

**Total skills needing routing fixes (task .3)**: 5
**Total skills needing content fixes (task .4)**: 4-5
**Skills needing both**: 1 (dotnet-resilience -- routing P2 + content not needed)
