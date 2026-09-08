# Runner Installation and Path Baseline

Status: current-known-good conditional baseline
Control ID: CKGB-RUNNER-PATH-001
Origin: RCC + JAP warm-runner and local application work

## Purpose

Persistent self-hosted runners reduce setup latency, but they create durable host state. That state must be explicit enough that discovery, provisioning, migration, cleanup and application installation do not guess ownership from directory names.

This baseline distinguishes **application installation** from **GitHub Actions runner installation/provisioning** and from **managed runner toolchains**.

## Three path classes

### 1. Application install root

The released product lives here. It is governed by the product's release/install contract.

Current examples:

- JAP Windows Control Center: `%LOCALAPPDATA%\JAP-Control-Center`;
- RCC Windows app: `%LOCALAPPDATA%\RunnerControlCenterWinUI`;
- RCC persistent application state: `%LOCALAPPDATA%\RunnerControlCenter`.

Application state should be separated from replaceable application binaries where practical.

### 2. GitHub Actions runner root

The Actions runner payload, registration and work directory live here. It is governed by the runner/control-plane contract, not by the application installer.

Current RCC evidence includes:

- WSL runner root: `/home/jens_h/actions-runner`;
- known Windows discovery roots: `C:\actions-runner`, `C:\actions-runners`, `%USERPROFILE%\actions-runner`.

These are **evidence examples**, not universal CKGB defaults. New projects should declare their own canonical runner root/profile rather than copy a user-specific absolute path.

### 3. Managed runner toolchain root

Stable dependencies provisioned for persistent runners live separately from the Actions runner payload.

Current RCC implementation uses:

- Windows: `%PUBLIC%\DeepOceanInfrastructure\RunnerToolchain` with CommonApplicationData fallback;
- Linux/WSL: `$HOME/.cache/DeepOceanInfrastructure/RunnerToolchain`.

This separation lets a runner registration be replaced or migrated without silently redefining dependency ownership.

## Core rules

1. **No path guessing for effects.** Discovery roots may be hints, but destructive/provisioning actions require exact repository/runner identity and current evidence.
2. **Persist cross-OS runner paths.** If a Windows application invokes a WSL runner/runtime, pass the absolute Linux path explicitly and persist it.
3. **Do not use the source checkout as durable runner state.** A persistent runner is execution capacity, not source authority.
4. **Do not put managed toolchains inside arbitrary workload repos.** Toolchains belong to an owned provisioning surface.
5. **Do not let workload repos supply arbitrary fallback host-install shell.** Declarative profile mismatches should either be repaired by the authorized provisioner or remain explicit stale/unsupported state.
6. **Partial state is evidence.** A runner directory without registration/service/work markers may be a safe orphan only after all ownership and deletion predicates are revalidated.
7. **Heartbeat and routing are separate from installation.** An installed warm runner can legitimately be sleeping/offline. Current routability must be observed rather than inferred from directory existence.

## Project runner contract

A serious self-hosted project should carry a machine-readable runner contract, e.g. `.rcc/runner-contract.json`, describing at least:

```text
repository_id
project_key
slot/profile id
platform
routing labels
desired/min/max active capacity
sleep policy
runtime capabilities
fallback policy
heartbeat/freshness contract
```

Where workloads are portable, the current-known-good pattern is warm preferred with an explicit GitHub-hosted fallback and workflow opt-in. Fallback is a controlled routing decision, not silent execution drift.

## Runner profile provisioning

Provisioning should be profile-driven:

```text
desired profile
-> probe current host
-> classify mismatches
-> repair only supported requirements
-> re-probe
-> persist qualification evidence
```

Unsupported remaining requirements should produce a clear stale/profile error. Do not hide them by running arbitrary install commands supplied by the workload repository.

## Application installer entry points — current examples

### JAP

- WSL install entry: `scripts/install_jap_windows_control_center.sh`
- WSL runtime entry: `scripts/run_jap_windows_control_center.sh`
- Windows installer: `install-jap-control-center.ps1`
- default app root: `%LOCALAPPDATA%\JAP-Control-Center`

The Windows installer requires an explicit `WslInstalledRunnerPath`, validates that it is an absolute Linux path and persists it. This is the preferred pattern when one operating-system surface launches another: **resolve once from authority, pass explicitly, persist, verify**.

### RCC

- released/transition application installer: `install-rcc-control-center.ps1`
- developer/local build-install helper: `tools/windows/Build-Install-RccLocal.ps1`
- app install root in the helper: `%LOCALAPPDATA%\RunnerControlCenterWinUI`
- app state root: `%LOCALAPPDATA%\RunnerControlCenter`

`Build-Install-RccLocal.ps1` also demonstrates an important boundary: it validates repository identity, clean source and required local tools before a local developer build. That path must not be confused with routine GitHub-Release consumption.

## Runner provisioning vs application installation

Use this vocabulary consistently:

| Surface | Owns | Must not own by implication |
|---|---|---|
| Product installer/updater | released app binaries, app provenance, app state migration, rollback | GitHub Actions runner registration |
| Runner lifecycle/control plane | runner payload, registration/service, routing, sleep/wake, runner identity | product source/release truth |
| Runner profile provisioner | supported stable toolchain/dependency requirements | arbitrary workload-defined host mutation |
| Workload repository | desired runner contract/profile and portable workload | host-wide installation authority |

## Migration rule

A runner migration is not complete because a new directory exists. Require evidence for the relevant lifecycle:

```text
old identity classified
-> new target/provisioning prepared
-> profile qualified
-> registration/routing proven
-> real workload/heartbeat proof
-> old target reconciled
-> legacy retirement only after replacement proof
```

Never recursively delete a partially migrated runner merely because it is not the desired final state.

## Hosted fallback

RCC and JAP currently demonstrate a useful conditional policy:

```text
strategy = WARM_PREFERRED_GITHUB_HOSTED
provider = GITHUB_HOSTED_STANDARD
portable_workloads_only = true
required_workflow_opt_in = true
```

Use hosted fallback when the workload is genuinely portable and no local-only effect/capability is required. A fallback that cannot satisfy the workload contract must fail closed rather than pretending to be equivalent.

## Selection guidance

Select this baseline when any of these are true:

- self-hosted GitHub Actions runners persist across jobs;
- WSL/Windows paths cross an OS boundary;
- warm runners can sleep/wake or be migrated;
- stable toolchains are cached/provisioned outside individual repositories;
- a local application also controls or invokes runner/runtime processes.

Hosted-only disposable CI can usually omit persistent runner-root management.

## Evidence origins

- RCC `.rcc/runner-contract.json`
- RCC `src/RunnerControlCenter/config.json`
- RCC `src/RunnerControlCenter/Services/RunnerProfileVersioning.cs`
- RCC `src/RunnerControlCenter/Services/RunnerProfileProvisioningService.cs`
- RCC `docs/lessons-learned.md`
- JAP `.rcc/runner-contract.json`
- JAP `install-jap-control-center.ps1`
- JAP `scripts/install_jap_windows_control_center.sh`
- JAP `scripts/run_jap_windows_control_center.sh`
