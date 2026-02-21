# fn-57-copilot-testing-and-progressive.4 CI hardening for Copilot gate

## Description

Harden CI to make Copilot a functional gate on PRs, pin Copilot CLI version, add frontmatter safety checks, and handle auth/availability gracefully. Use a "soft infra, hard functional" policy with deterministic rules for when infra_error is acceptable.

**Size:** M
**Files:** .github/workflows/validate.yml, .github/workflows/agent-live-routing.yml, docs/agent-routing-tests.md

## Approach

1. **Add Copilot smoke subset to `validate.yml` (Option A)**: The current `agent-live-routing.yml` only runs on `workflow_dispatch` and `schedule`, so it cannot block PRs. Add a new job `copilot-smoke` to `validate.yml` (which runs on `pull_request`) that runs a lightweight Copilot smoke subset:
   - **Job name**: `copilot-smoke`
   - **What it runs**: A subset of the smoke cases from fn-57.1 (5-10 deterministic, non-flaky cases covering direct activation, advisor routing, and one negative control). The gated subset must exclude any case marked `"flaky": true` in the baseline.
   - **Output format**: `results.json` matching the baseline comparison format from fn-57.1
   - **Gate behavior**: Compare results against the committed baseline; fail on unexpected regressions
   - Keep `agent-live-routing.yml` for comprehensive scheduled/manual testing with full 25+ cases across all providers.

2. **Copilot CLI install and auth in CI** — two-phase approach:
   - **Phase 1 (first step of T4)**: Create a throwaway GitHub Actions workflow (`copilot-install-proof.yml`) that proves `copilot` binary install + `copilot plugin marketplace add` + `copilot plugin marketplace list` all work on `ubuntu-latest`. Record the exact install command, binary path, and auth env vars that work. This proof gates the rest of T4.
   - **Phase 2 (after proof)**: Add the proven install steps to `validate.yml`:
     - **Auth**: Use `env: { GITHUB_TOKEN: ${{ github.token }} }` (the built-in Actions token). If that's insufficient for Copilot auth, use a dedicated `${{ secrets.COPILOT_TOKEN }}` secret instead.
     - **Availability check**: `copilot auth status` (or `copilot --version`) must exit 0. If it fails → `infra_error`.
     - **Plugin registration** (from `test.sh:prepare_copilot_plugin()`):
       ```
       copilot plugin marketplace add "$REPO_ROOT"
       copilot plugin install dotnet-artisan@dotnet-artisan
       ```
     - **Discovery verification**: `copilot plugin marketplace list | grep -F "dotnet-artisan"`
     - **Permissions**: If install-proof requires broader permissions than `contents: read`, update `validate.yml` workflow `permissions:` to the minimal set that makes auth succeed, and document the change.

3. **"Soft infra, hard functional" gating in `validate.yml`** (fork/no-secrets rule for `copilot-smoke` job):
   - If `github.event.pull_request.head.repo.fork == true` OR `copilot auth status` exits non-zero → produce synthetic `results.json` with `status: "infra_error"`, exit 0 with annotation "Copilot skipped (fork/no auth)"
   - Otherwise → `infra_error` is a failure (Copilot should be available on non-fork PRs)
   - The smoke runner must support a `--require-copilot` flag (or env var `REQUIRE_COPILOT=true`): when set, outputs `infra_error` AND exits non-zero if Copilot is unavailable. The `validate.yml` job sets this flag on non-fork PRs so infra_error is never silently swallowed.

4. **Simplify `agent-live-routing.yml` Copilot handling**:
   - Remove `continue-on-error: ${{ matrix.agent == 'copilot' }}` from the Copilot matrix job
   - **Schedule runs**: Hard-code `fail_on_infra=true` behavior (schedule has no inputs). If Copilot infra is down during a scheduled run, it should fail to surface the issue.
   - **Manual (`workflow_dispatch`) runs**: Keep existing `fail_on_infra` input (current default: `false`). Update default to `true` to match schedule behavior.
   - Update `summarize` job to handle `infra_error` status: count as "failed" when `fail_on_infra=true` (schedule or explicit), "skipped" when `fail_on_infra=false` (manual override only)

5. **Verify frontmatter safety checks run in CI**: The `validate.yml` workflow runs `./scripts/validate-skills.sh` which calls `_validate_skills.py`. Verify that the Copilot frontmatter checks added in fn-56.2 (BOM, quoted description, missing license, metadata ordering) are treated as ERRORs and thus fail the validation workflow.

6. **Add skill count assertion to CI**: `find skills -name SKILL.md -maxdepth 2 | wc -l` must equal 131. Add to `validate.yml`.

7. **Add flat layout guard to CI**: Verify `_validate_skills.py`'s flat layout guard (from fn-56.3) runs in CI and ERRORs on nested skills.

8. **Define exit criteria documentation**: Add a section to `docs/agent-routing-tests.md`:
   - What "Copilot passes" means (evidence patterns, baseline comparison)
   - Deterministic rules for when `infra_error` is acceptable: fork/no-secrets in PR CI, `fail_on_infra=false` manual override
   - How to update baselines when intentional behavior changes
   - Fork behavior documentation

## Key context

- Current CI: `agent-live-routing.yml` runs on `workflow_dispatch` + `schedule` ONLY (not on PRs!)
- `validate.yml` runs on `push` and `pull_request` — this is where PR-blocking Copilot checks go
- Copilot has been soft-failure since fn-54 (via `continue-on-error: ${{ matrix.agent == 'copilot' }}`)
- The `summarize` job in `agent-live-routing.yml` hardcodes `PROVIDERS=(claude codex copilot)` — must handle missing/infra_error results
- Forks can't access repo secrets → Copilot tests naturally skip on fork PRs
- `test.sh` already has `prepare_copilot_plugin()` with the exact `copilot plugin marketplace add/install` flow
- `agent-live-routing.yml` already has `fail_on_infra` workflow input (default: `false`); schedule runs currently have no equivalent

## Acceptance
- [ ] `copilot-smoke` job added to `validate.yml` running a deterministic smoke subset on PRs
- [ ] Smoke job compares results against committed baseline (not percentage thresholds)
- [ ] Copilot CLI install proven on `ubuntu-latest` via throwaway workflow (exact install command + auth env documented)
- [ ] Copilot CLI pinned version in CI workflow
- [ ] Plugin registration uses same mechanism as `test.sh:prepare_copilot_plugin()`
- [ ] Auth mechanism implemented (token source documented, `copilot --version` health check gates execution)
- [ ] Smoke runner supports `--require-copilot` flag: non-fork PRs exit non-zero on infra_error
- [ ] `validate.yml`: fork/no-secrets → accept infra_error; non-fork with secrets → infra_error is failure (enforced via `--require-copilot`)
- [ ] `agent-live-routing.yml`: `continue-on-error` removed; schedule hard-codes `fail_on_infra=true`; `workflow_dispatch` default changed to `true`
- [ ] `summarize` job handles `infra_error` status: "failed" when `fail_on_infra=true`, "skipped" otherwise
- [ ] Frontmatter safety checks verified running in CI as ERRORs
- [ ] Flat layout guard verified running in CI
- [ ] Skill count assertion (131) added to CI
- [ ] Exit criteria documented in docs/agent-routing-tests.md with deterministic infra_error rules per workflow
- [ ] Fork CI behavior documented and tested
