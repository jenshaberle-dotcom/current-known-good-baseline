# NOVI-family game project baseline

Status: current known good baseline for new NOVI-family game repositories
Applies when: a new game is intended to join the same local development/product family as Deep Ocean Intelligence and Children of the Deep.

## Principle

A new game gets a new product repository and game-specific tests, but it does **not** invent a new Windows trust identity, local filesystem convention, CI queue policy, runner lifecycle, timeout scheme or toolchain provisioning strategy.

The normal development environment is persistent and verified. A fresh machine is an explicit clean-room evidence mode, not the default for every commit.

## Required project-start adoption

Copy these four retained family files into the new game repository:

- `docs/project-start/NOVI-GAME-CI-CONTRACT.json` -> `docs/governance/NOVI-GAME-CI-CONTRACT.json`
- `docs/project-start/check_game_ci_contract.py` -> `tools/ci/check_game_ci_contract.py`
- `docs/project-start/Ensure-NoviRunnerToolchain.ps1` -> `tools/runner/Ensure-NoviRunnerToolchain.ps1`
- `docs/project-start/ensure_novi_runner_toolchain.sh` -> `tools/runner/ensure_novi_runner_toolchain.sh`

The retained files are copied byte-for-byte. Every GitHub Actions workflow declares one contract workflow class and a normal validation workflow executes the checker.

The project may add deeper or different game tests. It may not weaken family invariants merely to reduce CI latency.

## Persistent runner lifecycle

Normal self-hosted development jobs use the lifecycle:

1. `HIT` — requested engine/toolchain version and integrity already match; reuse it immediately.
2. `REPAIR` — only a missing or drifted component is repaired.
3. `REBUILD` — only a version/integrity-invalid component is rebuilt from verified source.
4. `CLEAN_ROOM` — deliberately fresh environment, used only through an explicit/manual clean-room workflow.

Do not erase or re-download an unchanged verified toolchain merely because a new commit arrived.

The Windows family toolchain root is:

- `%PUBLIC%\NOVI\RunnerToolchain`

It holds shared verified engine/cache state. The provisioner may repair the active runner service profile's local Godot/template view from that shared state. Concurrent provisioning must be serialized per tool/version and component replacement must be atomic.

Linux runners use the same lifecycle with a persistent runner-local cache/root.

## Windows runner is scarce Product Authority

Do not create Windows twins for platform-independent checks.

Repository identity, provenance, governance/static policy and Linux game parity belong on Linux. Windows capacity is reserved for behavior that actually requires Windows, such as:

- native Windows technical execution;
- Windows export/runtime behavior;
- offline endpoint probing of the Windows executable;
- Authenticode/trust boundaries;
- Windows alpha packaging/handoff.

Prefer one Windows Product Authority job per PR head. Build a verified Windows export once and reuse that same export for downstream Windows evidence instead of rebuilding it in separate workflows.

## Family timeout classes

Use these defaults unless a documented workload-specific reason requires a stricter lower bound:

- metadata/static: 10 minutes;
- Linux game validation: 15 minutes;
- Windows Product Authority: 30 minutes;
- explicit clean room: 45 minutes.

A timeout increase is not a substitute for fixing repeated cold-start work.

## Local Windows family layout

Installed private alphas are siblings:

- `%LOCALAPPDATA%\Programs\NOVI <Game Name> Alpha`

Per-game local data lives under:

- `%LOCALAPPDATA%\NOVI\<Game-Slug>\Logs`
- `%LOCALAPPDATA%\NOVI\<Game-Slug>\Diagnostics`
- `%LOCALAPPDATA%\NOVI\<Game-Slug>\Build`

The shared interactive developer signing authority is singular:

- `%LOCALAPPDATA%\NOVI\Signing\publisher.json`
- publisher subject: `CN=Jens Haberle`

Do not create a certificate/signing identity per game unless a later explicit legal/publisher/store boundary requires separation.

A self-hosted service runner may use the shared bridge only for unsigned handoffs:

- `C:\Users\Public\NOVI\Handoffs\<Game-Slug>\current`

The runner must not receive or create the interactive developer private key. The human-account signing step must fail closed if the shared publisher authority is missing or inconsistent.

## CI family invariants

- Feature-branch game validation runs through `pull_request` plus optional `workflow_dispatch`, not duplicate `push` + PR execution.
- All recurring validation/handoff workflows use latest-head concurrency and `cancel-in-progress: true`.
- Runner/infrastructure smoke checks are manual-only unless a separately bounded infrastructure incident explicitly requires otherwise.
- Normal PRs do not run clean-room provisioning automatically.
- GitHub Actions references use immutable commit SHAs.
- Native Windows interactive play remains Product Authority; CI remains technical evidence.
- Test/security/provenance depth may not be reduced just to shorten a queue.
- Normal Windows/AVG/Defender protections are not disabled or excluded to make the build pass.

## Re-entry requirement

Every game repository's canonical engineering re-entry contract must list its copied `NOVI-GAME-CI-CONTRACT.json` and runner ensure scripts as required reads and must record the current toolchain lifecycle, timeout classes, local-alpha paths and shared publisher authority. Current-state files must not retain superseded alpha/install or cold-start runner assumptions.

## Adoption rule for future contract versions

The contract is versioned. A new version is not silently assumed by sibling games. Create a bounded adoption task for every active NOVI-family game repository and migrate each at a safe repository head. The checker makes local drift fail closed after adoption.
