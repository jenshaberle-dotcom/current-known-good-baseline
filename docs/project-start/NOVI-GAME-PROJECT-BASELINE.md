# NOVI-family game project baseline

Status: current known good baseline for new NOVI-family game repositories
Applies when: a new game is intended to join the same local development/product family as Deep Ocean Intelligence and Children of the Deep.

## Principle

A new game gets a new product repository and new game-specific tests, but it does **not** invent a new Windows trust identity, local filesystem convention, or CI queue policy.

## Required project-start adoption

Copy these two files from this CKGB profile into the new game repository:

- `docs/governance/NOVI-GAME-CI-CONTRACT.json`
- `tools/ci/check_game_ci_contract.py`

Every GitHub Actions workflow in the game repository declares one of the contract workflow classes and an existing validation workflow executes the checker.

The project may add deeper or different game tests. It may not weaken the family invariants merely to reduce CI latency.

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
- GitHub Actions references use immutable commit SHAs.
- Native Windows interactive play remains Product Authority; CI remains technical evidence.
- Test/security/provenance depth may not be reduced just to shorten a queue.
- Normal Windows/AVG/Defender protections are not disabled or excluded to make the build pass.

## Re-entry requirement

Every game repository's canonical engineering re-entry contract must list its copied `NOVI-GAME-CI-CONTRACT.json` as a required read and must record its current local-alpha paths and shared publisher authority. Current-state files must not retain superseded alpha/install paths.

## Adoption rule for future contract versions

The contract is versioned. A new version is not silently assumed by sibling games. Create a bounded adoption task for every active NOVI-family game repository and migrate each at a safe repository head. The checker makes local drift fail closed after adoption.
