> **HISTORICAL REFERENCE** — This is the prior plan snapshot (T1-T12, T6A-D, T7A-B structure). The authoritative plan is `.flow/specs/fn-53-skill-routing-language-hardening.md`.

# Plan: Skill Routing Language Hardening

**Generated**: 2026-02-19

## Overview
Standardize routing language across all `SKILL.md` files so skills are discovered reliably from non-specific prompts, descriptions stay concise/high-signal, and inter-skill references are explicit and unambiguous. Include optional extraction/refactoring only when it reduces overlap, with mandatory content-preservation verification.

## Prerequisites
- Repo write access on active PR branch
- Local CLIs: `bash`, `rg`, `dotnet`
- Existing validators/scripts:
  - `scripts/validate-skills.sh`
  - `scripts/_validate_skills.py`
  - `scripts/validate-marketplace.sh`
- Existing routing runner:
  - `tests/agent-routing/check-skills.cs`
  - `tests/agent-routing/cases.json`

## Dependency Graph

```text
T1 -> T2 -> T3 -> {T8, T9} -> T4 -> T5 -> {T6A, T6B, T6C, T6D}
{T6A, T6B, T6C, T6D} -> T7B -> T10 -> T11 -> T12
{T6A, T6B, T6C, T6D} -> T7A(optional) -> T7B
```

## Tasks

### T1: Baseline Audit + Ownership Manifest
- **depends_on**: []
- **location**: `skills/**/SKILL.md`, `tests/agent-routing/cases.json`
- **description**: Build baseline inventory for every skill: description length, overlap risk, cross-skill references, and routing hotspots. Produce an explicit ownership manifest mapping each skill path to exactly one downstream editing task (no overlapping edits).
- **validation**: Create `docs/skill-routing-audit-baseline.md` and `docs/skill-routing-ownership-manifest.md` covering 100% of skills.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T2: Canonical Routing Language Spec
- **depends_on**: [T1]
- **location**: `docs/skill-routing-style-guide.md`, `CONTRIBUTING-SKILLS.md`
- **description**: Define canonical rules for descriptions and references:
  - classifier-style descriptions (target <=120 chars)
  - explicit scope boundaries
  - normalized reference language (`see [skill:x] for y`)
  - router precedence language (baseline-first, domain-next)
- **validation**: Style guide has positive/negative examples and migration checklist.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T3: Validator and Policy Hardening
- **depends_on**: [T2]
- **location**: `scripts/_validate_skills.py`, `scripts/validate-skills.sh`
- **description**: Add/extend checks for routing-language quality and define CI policy: `zero errors` and `zero new warnings vs baseline` (with explicit allowlist file if needed).
- **validation**: Validator output is deterministic and policy documented in script/docs.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T8: Strengthen Routing Test Assertions (Early)
- **depends_on**: [T3]
- **location**: `tests/agent-routing/check-skills.cs`, `tests/agent-routing/cases.json`, `docs/agent-routing-tests.md`
- **description**: Improve assertions to prefer definitive evidence (`Skill` tool invocation / launch lines) and reduce false positives from incidental text mentions.
- **validation**: Target cases produce deterministic proof lines in `tool-use-proof.log`.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T9: Routing Compliance Report Tooling (Early)
- **depends_on**: [T3, T1]
- **location**: `scripts/` (new report script), `docs/`
- **description**: Add a report command that outputs per-skill compliance, overlap alerts, malformed reference language, and unresolved reference quality issues.
- **validation**: One reproducible command generates report consumed by PR review.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T4: Normalize Foundation Router Language
- **depends_on**: [T2, T8, T9]
- **location**: `skills/foundation/dotnet-advisor/SKILL.md`, `skills/foundation/dotnet-version-detection/SKILL.md`
- **description**: Make baseline-first routing explicit and consistent, including generic app-request behavior and cross-skill escalation language.
- **validation**: Targeted routing checks show foundation skill + baseline dependency invocation for non-specific prompts.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T5: Normalize Highest-Traffic Skills from Corpus
- **depends_on**: [T1, T2, T4, T8, T9]
- **location**: skills listed in `tests/agent-routing/cases.json`
- **description**: Apply canonical language to highest-traffic skills first. Enforce exclusive ownership using the T1 manifest so no skill is edited in later category sweeps.
- **validation**: Representative routing checks pass; no policy regressions in validator output.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T6A: Category Sweep - Core/Architecture/Performance/Build
- **depends_on**: [T5]
- **location**: subset from `docs/skill-routing-ownership-manifest.md`
- **description**: Apply canonical routing language to assigned skills only (no overlap with T6B/T6C/T6D).
- **validation**: Emit `docs/skill-routing-sweep-core-architecture-performance-build.md` with before/after stats and unresolved items.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T6B: Category Sweep - API/Security/Testing/CI
- **depends_on**: [T5]
- **location**: subset from `docs/skill-routing-ownership-manifest.md`
- **description**: Standardize trigger/out-of-scope wording and cross-skill references for assigned skills only.
- **validation**: Emit `docs/skill-routing-sweep-api-security-testing-ci.md` with before/after stats and unresolved items.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T6C: Category Sweep - UI/NativeAOT/CLI/TUI
- **depends_on**: [T5]
- **location**: subset from `docs/skill-routing-ownership-manifest.md`
- **description**: Align platform classifier wording and related-skill routing language for assigned skills only.
- **validation**: Emit `docs/skill-routing-sweep-ui-nativeaot-cli-tui.md` with before/after stats and unresolved items.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T6D: Category Sweep - Remaining Long Tail
- **depends_on**: [T1, T5]
- **location**: residual skill list from `docs/skill-routing-ownership-manifest.md`
- **description**: Normalize all remaining skills not covered by T6A/B/C. Residual list must be concrete and closed-form (no implicit “remaining” edits).
- **validation**: Emit `docs/skill-routing-sweep-long-tail.md`; ownership manifest shows 100% completed coverage.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T7A: Optional Extraction/Refactor of Overlap
- **depends_on**: [T6A, T6B, T6C, T6D]
- **location**: affected `skills/**/SKILL.md`
- **description**: Optionally extract duplicated/overlapping routing or guidance into clearer primary skills where beneficial.
- **validation**: Every extraction has a trace entry in migration map and no unresolved references.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T7B: Mandatory Content-Preservation Verification
- **depends_on**: [T6A, T6B, T6C, T6D] (and T7A if T7A is executed)
- **location**: `docs/skill-content-migration-map.md`, validation/report scripts
- **description**: Mandatory verification that all intended content remains represented after normalization/refactors. Include source-section to destination-section mapping and automated checks for dropped sections, broken references, and invalid self/cyclic cross-links.
- **validation**: Migration map complete; automated section/reference checks pass.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T10: Contributor Guidance + Templates Update
- **depends_on**: [T2, T7B]
- **location**: `CONTRIBUTING-SKILLS.md`, docs/templates
- **description**: Update authoring docs and templates to codify routing-language standards, clear inter-skill reference wording, and extraction content-preservation rules.
- **validation**: New examples conform to style guide and validator policy.
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T11: End-to-End Validation and CI Gate Updates
- **depends_on**: [T4, T5, T7B, T8, T9, T10] (and T7A if T7A is executed)
- **location**: `.github/workflows/*.yml`, `test.sh`, `scripts/validate-*.sh`
- **description**: Run full static + routing validation and update CI gates to enforce policy (`zero errors`, `zero new warnings vs baseline`).
- **validation**:
  - `./scripts/validate-skills.sh`
  - `./scripts/validate-marketplace.sh`
  - targeted `./test.sh` suites
  - CI green on PR with updated policy
- **status**: Not Completed
- **log**:
- **files edited/created**:

### T12: Rollout and Follow-Up Backlog
- **depends_on**: [T11]
- **location**: PR summary, issues
- **description**: Publish migration summary and backlog any deferred optional refactors (from T7A) with explicit owners and acceptance criteria.
- **validation**: PR includes final compliance summary + tracked follow-up items.
- **status**: Not Completed
- **log**:
- **files edited/created**:

## Parallel Execution Groups

| Wave | Tasks | Can Start When |
|------|-------|----------------|
| 1 | T1 | Immediately |
| 2 | T2 | T1 complete |
| 3 | T3 | T2 complete |
| 4 | T8, T9 | T3 complete |
| 5 | T4 | T8, T9 complete |
| 6 | T5 | T4 complete |
| 7 | T6A, T6B, T6C, T6D | T5 complete (disjoint ownership only) |
| 8 | T7A (optional) | T6A, T6B, T6C, T6D complete |
| 9 | T7B | T6A, T6B, T6C, T6D complete (and T7A if executed) |
| 10 | T10 | T7B complete |
| 11 | T11 | T10 complete plus T4, T5, T8, T9, T7B complete (and T7A if executed) |
| 12 | T12 | T11 complete |

## Testing Strategy
- Static quality:
  - `./scripts/validate-skills.sh`
  - routing compliance report from T9
- Routing behavior:
  - targeted `./test.sh --agents claude,codex,copilot --case-id ...`
  - verify definitive proof in `tests/agent-routing/artifacts/tool-use-proof.log`
- Policy checks:
  - compare warnings to baseline/allowlist
- CI verification:
  - validation workflows + routing workflow gates

## Risks & Mitigations
- Risk: Category sweeps collide on same files.
  - Mitigation: T1 ownership manifest is authoritative; each skill path owned by exactly one edit task.
- Risk: Optional extraction creates schedule drag.
  - Mitigation: T7A optional; T7B mandatory verification path does not require extraction.
- Risk: Content lost during refactor.
  - Mitigation: mandatory migration map + automated section/reference checks in T7B.
- Risk: Live routing checks are flaky.
  - Mitigation: definitive skill-invocation evidence, smaller deterministic suites, proof-log retention.
- Risk: CI policy ambiguity around warnings.
  - Mitigation: explicit `zero new warnings vs baseline` rule with committed allowlist.
- Risk: Merge/rebase churn across large edits.
  - Mitigation: wave-by-wave branches/checkpoints and required per-wave integration before next wave.
