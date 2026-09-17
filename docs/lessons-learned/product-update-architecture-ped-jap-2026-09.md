# Product Update Architecture Lessons — PED and JAP

Date: 2026-09-17
Status: harvested lesson
Origin: PED updater acceptance work and JAP Windows Control Center comparison

## Context

PED and JAP converged on two different strengths and exposed two different failure modes.

JAP has the simpler operational update lifecycle on the currently managed workstation:

- GitHub-hosted Windows build;
- immutable GitHub Release bound to an exact source/tag/version;
- local self-hosted Linux/WSL runner stages the exact release under the managed Windows install root;
- SHA-256 and source/version compatibility are verified before update state is published;
- the desktop application only polls `pending-update.json`, asks for consent, freezes accepted state, starts a hidden applier, and exits;
- no executable update source is discovered, downloaded or materialized by the GUI after consent.

PED added a stronger local publisher trust boundary:

- a local Windows publisher broker owned a private Authenticode key;
- release components were signed locally and verified by publisher subject/thumbprint;
- the installed application and applier enforced matching publisher signatures.

That gave PED more defense in depth, but also created an additional local release authority, local key dependency, separate broker lifecycle, extra manifests, signature checks and more transition states. In real updater acceptance this complexity repeatedly became a source of fragility and interacted badly with endpoint security when executable PowerShell was materialized late or from temporary paths.

## Lesson 1 — Update lifecycle simplicity matters

The most important operational property was not where the release was signed. It was **when and where executable update material appeared**.

The reliable pattern is:

```text
release exists
  -> exact update is staged under a managed install root
  -> integrity/identity verification completes
  -> pending state is published
  -> user consents
  -> accepted state is frozen
  -> hidden applier installs only the already-staged target
  -> restart / rollback result is recorded
```

No network discovery, download, archive extraction or executable materialization should occur after user consent unless the product explicitly requires it and carries an equivalent trust proof.

## Lesson 2 — A self-hosted runner is useful infrastructure, not a product dependency

JAP's current local runner model is a good development and managed-workstation solution because the runner can reach the real `%LOCALAPPDATA%`, perform WSL/Windows interop and stage an update before the GUI sees it.

It is **not** the desired distribution model for a product that may be installed on arbitrary systems. Requiring every consumer machine to run a GitHub self-hosted runner, WSL, project checkout or GitHub CLI/authentication creates an operational dependency that does not scale as a normal product contract.

Therefore:

- self-hosted runners MAY own development, acceptance, integration or managed-fleet staging;
- self-hosted runners MUST NOT be the default consumer-update prerequisite for a distributable product;
- the update contract should be designed so the staging provider can later be replaced by a small product update agent without changing GUI consent or apply semantics.

## Lesson 3 — Signing is valuable; local developer-machine signing is not the target architecture

PED's Authenticode concept remains valuable for a real distributable product. The problematic part was not code signing itself, but binding release publication to an interactive local developer/publisher workstation and local private-key availability.

For a product-ready architecture the preferred trust chain is:

```text
source/tag
  -> hosted build + tests + package
  -> central signing authority
  -> immutable signed release
  -> consumer staging
  -> checksum + signature verification
  -> consent
  -> atomic apply / rollback
```

The signing authority should be centralized and automatable, ideally HSM/cloud-backed or equivalent. A developer workstation may be used only as an explicitly documented temporary exception, not as the normal release contract.

## Lesson 4 — Build, signing, publication, staging, consent and apply are separate authorities

Future projects should not collapse these responsibilities into one script or one machine.

The default authority split is:

1. **Build authority** — creates reproducible artifacts from exact source.
2. **Signing authority** — attests publisher identity for executable artifacts where signing is selected.
3. **Publication authority** — creates immutable release metadata/assets.
4. **Staging authority** — retrieves and verifies an exact release on the target system before consent.
5. **Consent authority** — interactive product UX, when an interactive update policy is selected.
6. **Apply authority** — installs only the frozen accepted target and records success/failure/rollback.

These authorities may run on the same platform, but their contracts remain explicit and testable.

## Lesson 5 — Bootstrap and routine update are different products

The first installation/bootstrap may need broader privileges or migration logic than routine updates. That does not justify carrying bootstrap complexity into every later update.

Projects should define:

- bootstrap contract;
- routine direct-update compatibility line;
- state schema for pending/accepted/result;
- rollback truth;
- explicit compatibility-breaking bridge when a direct update is no longer safe.

## Current portfolio decision

PED will **not** be converted to the full arbitrary-consumer product architecture during the current updater repair. That would widen the active scope from product work into a new distribution/signing programme.

Instead PED will temporarily adopt the proven current JAP update model so updater complexity stops dominating product development:

```text
GitHub-hosted release build/publish
  -> local warm runner stages/verifies target
  -> pending state
  -> PED GUI consent
  -> hidden applier
  -> restart/result
```

The local publisher-broker/signing special architecture is retired from the normal PED path. The local warm runner is accepted as transitional development/managed-workstation infrastructure, not as the final product distribution design.

PED or JAP can later become the first migration candidate for the full product-ready architecture described below, but that migration is intentionally deferred.

## Future-project default

New desktop/local products should start with this target architecture rather than rediscover it late:

```text
exact source/tag
      |
      v
hosted CI build + tests + package
      |
      v
central signing authority (when executable signing is selected)
      |
      v
immutable release / package channel
      |
      v
consumer-local update agent or updater
      |
      +-- resolve exact target
      +-- download into managed stage
      +-- verify source/version/checksum/signature
      +-- publish pending state
      v
product consent UX
      |
      v
hidden/isolated applier
      |
      +-- atomically install
      +-- verify installed identity
      +-- rollback on failure
      +-- record result
```

The consumer must not need a project source checkout, WSL, GitHub Actions runner or developer credentials for routine updates.

## Selection rule

If a project is expected to produce a versioned desktop/local application with more than one deployment target or plausible future external users, the product-distribution/update baseline is selected at project start unless an explicit non-selection reason and review trigger are recorded.
