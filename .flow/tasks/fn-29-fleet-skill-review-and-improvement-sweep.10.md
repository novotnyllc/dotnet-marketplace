# fn-29-fleet-skill-review-and-improvement-sweep.10 Implement improvements: Batches C+D

## Description

Apply all Critical and High-value improvements from consolidated findings to skills in Batches C (testing, cicd) and D (api-development, cli-tools, performance, native-aot). Improvements will be listed in consolidated-findings.md with skill name, category, issue description, and proposed fix. Implement changes by editing SKILL.md or details.md files directly, following the pattern established in batch-a-findings.md "Recommended Changes" section (Critical must-fix, High should-fix, Low nice-to-have). Commit per-category with conventional commit messages.

**File ownership:** This task modifies only `SKILL.md` and `details.md` files within its assigned category directories. Does NOT modify plugin.json, AGENTS.md, or README.md (owned by task 12).

**Description changes:** Do not modify descriptions without verifying aggregate budget impact against the projection in consolidated findings. Proposed descriptions in consolidated findings are pre-calculated to fit within the 12K warn threshold.

### Files

- **Input:** `docs/review-reports/consolidated-findings.md`
- **Modified:** `skills/testing/*/SKILL.md`, `skills/cicd/*/SKILL.md`, `skills/api-development/*/SKILL.md`, `skills/cli-tools/*/SKILL.md`, `skills/performance/*/SKILL.md`, `skills/native-aot/*/SKILL.md`

## Acceptance
- [ ] All Critical improvements for Batches C+D implemented
- [ ] All High-value improvements for Batches C+D implemented
- [ ] Per-category commits with conventional commit messages
- [ ] `./scripts/validate-skills.sh` passes after all changes
- [ ] No modifications to plugin.json, AGENTS.md, or README.md

## Done summary
Implemented all Critical and High improvements for Batches C+D: trimmed 8 over-budget descriptions (4 Critical over 140 chars, 4 High in 121-140 range), wrapped 41 bare skill references with [skill:] syntax across all 8 CI/CD and 2 testing skills, fixed xUnit v3 IAsyncLifetime signatures (Task->ValueTask) in dotnet-maui-testing, and updated stale "not yet landed" reference in dotnet-benchmarkdotnet. All four validation commands pass. Budget reduced from 11,822 to 11,640 chars.
## Evidence
- Commits: 21d62b2c32d3e4a4da38d9d23d26b1e89b1f3b43, 11799eea9e3e6175abaabffc9f12e7e91ee9d3c1, 3f2e71ac5d9d4ac21966e328d8b1dae4a7433277
- Tests: ./scripts/validate-skills.sh, ./scripts/validate-marketplace.sh, python3 scripts/generate_dist.py --strict, python3 scripts/validate_cross_agent.py
- PRs: