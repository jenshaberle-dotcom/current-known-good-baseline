# Active Portfolio Lessons Harvest — 2026-09

Status: harvested current-known-good evidence
Owner issue: #25
Scope: reusable engineering practices observed in active projects

## Purpose

This document captures lessons that have been exercised in real project work and are useful beyond the project that discovered them. It does not make the source projects identical and it does not turn CKGB into a mandatory control plane.

The governing filter is simple:

> Harvest proven friction, failure handling and successful operating patterns. Do not promote an attractive architecture merely because it is reusable.

Primary evidence for this harvest comes from WBAA, RCC, JAP and the CKGB/DRJ contracts as observed on 2026-09-08.

## 1. Repository truth outranks conversational continuity

### Observed friction

Long-running AI-assisted projects repeatedly crossed chat boundaries, operator interruptions, local worktrees, CI runs and delayed effects. Chat summaries were useful for navigation but became stale whenever repository or runtime state changed independently.

### Current-known-good rule

Use an explicit truth order for engineering continuation:

1. live repository and runtime evidence;
2. canonical repository contracts;
3. current Re-Entry projection;
4. issue/checkpoint evidence;
5. chat or memory.

Re-Entry is a navigator/projection. It may point to canonical paths and current work, but it must not silently widen or redefine canonical authority.

### Consequence

A continuation flow should resolve repository identity and exact current main before replaying a previous next action. If current live truth contradicts Re-Entry, reconcile the projection first.

Evidence: WBAA `docs/reentry/WBAA-ENGINEERING-REENTRY.json`; RCC `docs/lessons-learned.md`.

## 2. Real E2E outcome first; architecture follows evidence

### Observed friction

A concrete product task can expand into runner migration, framework extraction, orchestration redesign or generic governance work. Each subproblem may be legitimate while still delaying the requested outcome.

### Current-known-good rule

For an active outcome use:

```text
REAL MISSION
  -> CONCRETE FAILURE
  -> SMALLEST GENERIC REPAIR
  -> SAME MISSION RESUMES
```

New architecture work interrupts the active path only when it blocks the next safe outcome step, no safe bypass exists, and the proposed repair is the smallest sufficient safe change.

### Consequence

Generalization, portfolio rollout and cleanup are separate decisions after the real path works. A useful architecture idea can be recorded immediately without gaining implementation authority immediately.

Evidence: WBAA Issue #134 / `WBAA-ENGINEERING-REENTRY.json`; CKGB `docs/ckgb/architecture_lifecycle.md`.

## 3. Retry count is not diagnosis

### Observed friction

Blind retries can repeat the same failure indefinitely; fixed attempt counts can also stop a repair even though new evidence is still being produced.

### Current-known-good rule

Retry only when the next attempt is materially different or new evidence can change the result. Detect identical/no-progress retries and stop them. Timeouts, incomplete provider responses and partial lifecycle operations require post-failure evidence before deciding whether to retry, repair, re-plan or stop.

### Consequence

Bounded retry policy should track reason, changed input/repair, prior output/effect state and whether the preceding attempt settled safely.

Evidence: WBAA bounded convergence work; RCC timeout/recovery lessons.

## 4. Search readiness is part of repository understanding

### Observed friction

WBAA found that all ten active repositories were repository-discoverable, while only 2/10 exposed a ready connected code-search index. Eight repositories remained a provider limitation with no supported reindex write control exposed.

### Current-known-good rule

Do not conflate:

- repository discovery/metadata access;
- code-search index readiness;
- semantic/Copilot-style indexing.

When index readiness is false or unknown, a zero-result indexed search is not proof that code is absent.

### Degraded path

If an exact local checkout is available, exact-head tracked-path enumeration and literal `git grep` can provide deterministic provider-independent discovery. Exact-path/API reads remain valid for bounded questions. Exhaustive semantic claims still fail closed without a proven exhaustive/semantic surface.

### Retry rule

Only a genuinely observable `PENDING` state should enter bounded polling. `UNKNOWN` should not become an automatic polling loop.

Evidence: WBAA Issue #147, PR #149 and `docs/reentry/WBAA-PRIORITY-BLOCKERS.json`.

## 5. Retention state is not project work admission

### Observed friction

Repository cleanup and retention work can become an accidental global gate even when it is unrelated to the product task. Conversely, treating old/duplicate-looking state as disposable can destroy unique work.

### Current-known-good rule

Separate semantic preservation authority from technical reconciliation/effect execution:

- the project decides semantic value and desired preservation state;
- DRJ may independently revalidate technical identity and execute the exact authorized retention effect;
- pending retention reconciliation alone does not block unrelated project work;
- destructive effects fail closed on dirty, unpushed, divergent, ambiguous, unique or otherwise unclassified state.

### Consequence

`closed_unmerged`, `unknown`, `review` and `harvest_pending` are preservation states, not deletion authority.

Evidence: CKGB `PROJECT-DRJ.json`; WBAA Re-Entry retention gate.

## 6. Source authority and runtime/effect authority are separate

### Observed friction

A clean source decision does not imply authority to mutate a host, publish a release, stop a runner, delete retained state or spend provider budget. Mixing these domains makes safe source work wait on unrelated operational state and can also grant effects too broadly.

### Current-known-good rule

Record source governance separately from runtime/effect authority. Revalidate effect authority immediately before the effect when the environment can change between plan and execution.

### Consequence

A PR can be review-ready while host installation, auto-merge, release publication or external side effects remain intentionally unauthorized.

Evidence: WBAA runtime/effect boundaries; RCC release publisher boundary; DRJ effect executor contract.

## 7. Warm runners are capacity, not source authority

### Observed friction

Persistent self-hosted runners improve latency but can be asleep, offline, stale or partially provisioned. Treating "warm profile exists" as "runner is currently routable" causes queued jobs and misleading readiness.

### Current-known-good rule

Model runner capacity explicitly:

- project-level `.rcc/runner-contract.json` declares desired slots, routing labels and fallback policy;
- warm capacity has heartbeat/freshness evidence;
- portable workloads may opt into GitHub-hosted fallback;
- sleep may be intentional when `min_active=0` / `sleep_allowed=true`;
- source truth never moves into the runner working directory merely because the runner is persistent.

RCC and JAP currently use `WARM_PREFERRED_GITHUB_HOSTED` with a heartbeat and an explicit hosted fallback for portable workloads.

Evidence: RCC and JAP `.rcc/runner-contract.json`.

## 8. Runner paths are contracts, not guesses

### Observed friction

Runner discovery, migration and installers became fragile when path assumptions were implicit or when application install roots, GitHub Actions runner roots and dependency/toolchain roots were treated as one thing.

### Current-known-good rule

Keep three path classes separate:

1. **application install root** — where a released local application lives;
2. **GitHub Actions runner root** — persistent runner payload/registration/work area;
3. **managed toolchain root** — cached/provisioned dependencies used by persistent runners.

A runner path that crosses an OS boundary must be explicit, absolute and persisted. Do not rediscover it by directory-name heuristics during routine operation.

Current live examples, retained as evidence rather than universal defaults:

- RCC WSL runner root: `/home/jens_h/actions-runner`;
- RCC known Windows runner roots: `C:\actions-runner`, `C:\actions-runners`, `%USERPROFILE%\actions-runner`;
- RCC Windows managed toolchain: `%PUBLIC%\DeepOceanInfrastructure\RunnerToolchain` (with CommonApplicationData fallback);
- RCC Linux managed toolchain: `$HOME/.cache/DeepOceanInfrastructure/RunnerToolchain`.

Evidence: RCC `src/RunnerControlCenter/config.json` and `RunnerProfileVersioning.cs`.

## 9. Workload repositories must not become arbitrary host provisioners

### Observed friction

Persistent runner convenience can tempt each workload repository to ship fallback installer shell for missing dependencies. That makes host state unbounded and difficult to audit.

### Current-known-good rule

Runner profile requirements are declarative. A central/owned provisioning surface may satisfy supported requirements; unsupported mismatches remain explicit stale/profile failures rather than allowing each workload repository to mutate the host arbitrarily.

Evidence: RCC `RunnerProfileProvisioningService.cs` explicitly rejects remaining unsupported requirements instead of accepting workload-supplied fallback install shell.

## 10. Release publication needs immutable identity

### Observed friction

Source version, Git tag, release assets, installed version and the local running binary can diverge while each looks individually plausible.

### Current-known-good rule

For release-capable products, bind together:

```text
repository identity
+ exact source SHA
+ VERSION
+ release tag
+ package manifest
+ artifact checksum
+ publisher/signing identity where applicable
```

Before publication, refuse a pre-existing tag/release that resolves to another source or lacks required assets.

Evidence: RCC GitHub release protocol and `.github/workflows/rcc-github-release-sync.yml`; JAP desktop release workflow/contracts.

## 11. Build/sign/probe before replacing the known-good installation

### Observed friction

RCC caught generated-source/compile failures after static validation. Earlier lifecycle work also showed that a timeout or partial operation can leave intermediate state that must be diagnosed rather than blindly deleted.

### Current-known-good rule

The release/install pipeline should order destructive promotion last:

```text
exact source
-> restore/build/publish
-> sign if required
-> verify signature/checksum/manifest
-> staged runtime probe
-> atomic/same-volume swap
-> post-install verification
```

Keep rollback material until the new installation is proven.

Evidence: RCC `docs/lessons-learned.md`, release protocol and stable-swap tooling; JAP installer staging/rollback path.

## 12. GitHub Release is the application delivery ledger, not host authority

### Observed friction

Repository-local release metadata and source checkouts made application delivery ambiguous. At the other extreme, a GitHub Release alone cannot safely authorize a privileged host mutation.

### Current-known-good rule

For versioned local applications, prefer an immutable GitHub Release/tag as the visible canonical delivery surface. Use `gh release view`, `gh api` and `gh release create` in a qualified release workflow/broker to classify existing releases, bind tags to exact source, publish immutable assets and verify the resulting ledger.

Privileged signing/host mutation remains a separate authority boundary. The release workflow may consume locally signed/proven assets but must not infer local publisher authority from `contents: write` alone.

Evidence: RCC `RCC-GITHUB-RELEASE-PROTOCOL-v1.md` and `rcc-github-release-sync.yml`.

## 13. Routine consumer update must not rebuild source

### Observed friction

When a user machine clones source, restores SDKs, builds and signs during every update, source authority, build environment and release identity become part of the runtime install path.

### Current-known-good rule

A normal consumer update should download the exact release artifact, verify checksum/manifest/signature as applicable, stage/probe it and swap it into place. Rebuilding source belongs to release production/qualification, not routine update consumption.

JAP and RCC both retain explicit installer/update entry points while moving routine application delivery to GitHub Release assets.

## 14. Application installer and runner installer/provisioner are distinct surfaces

### Current evidence

JAP currently has:

- WSL application install entry: `scripts/install_jap_windows_control_center.sh`;
- WSL runtime entry: `scripts/run_jap_windows_control_center.sh`;
- Windows application installer: `install-jap-control-center.ps1`;
- default Windows app root: `%LOCALAPPDATA%\JAP-Control-Center`;
- an explicit `WslInstalledRunnerPath` handed into the Windows installer and persisted for later use.

RCC currently has:

- Windows application installer: `install-rcc-control-center.ps1`;
- local developer build/install helper: `tools/windows/Build-Install-RccLocal.ps1`;
- released application install root used by the helper: `%LOCALAPPDATA%\RunnerControlCenterWinUI`;
- separate persistent application state under `%LOCALAPPDATA%\RunnerControlCenter`;
- separate runner and managed-toolchain roots.

### Current-known-good rule

Document both installer surfaces, but never call an application installer a runner installer. Runner lifecycle/provisioning should be owned by the runner/control-plane contract; application installation should be owned by the product release contract.

## 15. Conflicting telemetry should remain conflicting telemetry

### Observed friction

RCC once merged local worker evidence and GitHub scheduler BUSY state into a single capacity number, producing impossible-looking states.

### Current-known-good rule

Do not average or OR together independent truth domains simply to get one status. Preserve disagreement as explicit drift and use each signal for the decision it can actually support.

Examples:

- local worker/process evidence for physical host activity;
- GitHub runner/BUSY state for scheduler safety;
- repository state for source authority;
- runtime probe for installed application health.

Evidence: RCC `docs/lessons-learned.md`.

## 16. Partial state is evidence

A partially created runner directory, staged release, incomplete migration or timeout residue is not automatically garbage. Diagnose ownership and effect state first. Cleanup requires the same identity and safety discipline as creation.

Evidence: RCC safe-orphan lifecycle lesson and DRJ preserve-by-default rules.

## Adoption summary

These lessons should influence new serious projects by default, but adoption remains profile-based:

- all serious projects: repo truth, evidence-driven failure handling, bounded effects, retention separation;
- agentic/large repos: search readiness classification and degraded discovery;
- self-hosted CI: runner contract, explicit roots, heartbeat/fallback, managed toolchain separation;
- versioned local apps: GitHub Release delivery, exact identity, checksums/manifests, staged probe, rollback;
- privileged Windows apps/control planes: add signing/publisher authority and host proof.

See also:

- `docs/ckgb/baseline_catalog.md`
- `docs/ckgb/architecture_lifecycle.md`
- `docs/tooling/github-release-delivery-baseline.md`
- `docs/tooling/runner-installation-and-path-baseline.md`
