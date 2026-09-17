# Product Distribution and Update Baseline

Status: current-known-good baseline
Control ID: CKGB-PRODUCT-UPDATE-001
Maturity: `RECOMMENDED`
Origin: JAP Windows update path + PED updater/signing acceptance lessons

## Purpose

Define the default architecture for versioned desktop/local products that may eventually be installed on arbitrary systems.

The baseline is deliberately product-oriented: development infrastructure may accelerate build, test and acceptance, but consumer systems must not inherit developer-only dependencies as routine update prerequisites.

## Default product contract

```text
EXACT SOURCE / TAG
  -> HOSTED BUILD + TEST
  -> PACKAGE
  -> CENTRAL SIGNING AUTHORITY (when signing is selected)
  -> IMMUTABLE RELEASE
  -> CONSUMER-LOCAL MANAGED STAGING
  -> IDENTITY + INTEGRITY + SIGNATURE VERIFICATION
  -> PENDING UPDATE STATE
  -> USER / POLICY CONSENT
  -> FROZEN ACCEPTED STATE
  -> HIDDEN / ISOLATED APPLIER
  -> VERIFY INSTALLED IDENTITY
  -> SUCCESS OR ROLLBACK RESULT
```

## Core invariants

### 1. Exact-source release identity

Every published product version binds to exact source identity and immutable version/tag metadata. Rebuilding a consumer installation from mutable source is not a routine update mechanism.

### 2. Build is not consumer installation

Build dependencies, compilers, source checkout and CI tooling belong to build infrastructure. Consumer machines receive already-built artifacts.

### 3. Self-hosted CI runners are not consumer prerequisites

A self-hosted runner may perform local acceptance, managed-fleet deployment or development staging. A distributable product must not require a GitHub Actions runner, WSL, developer source checkout or GitHub CLI credentials on every consumer system for routine updates.

When a project temporarily uses such infrastructure, document it as a **transitional staging provider** behind a replaceable staging boundary.

### 4. Stage before consent

Executable update material is resolved, downloaded/materialized and verified under a managed staging root before interactive consent is requested.

After consent, the apply path consumes only the frozen, already-staged target. Network discovery, release selection or late archive extraction after consent is forbidden by default.

### 5. Frozen accepted target

The exact target presented for consent is copied/frozen into accepted state. Apply must refuse target drift between staging, consent and installation.

### 6. Integrity and publisher identity

At minimum, immutable release identity and cryptographic digest verification are required.

For executable products intended for broader distribution, platform-native code signing is recommended. Signing should be performed by a centralized signing authority rather than a routine interactive developer workstation. HSM/cloud-backed signing is preferred when practical.

### 7. Separate authorities

Keep explicit contracts for:

- build;
- signing;
- publication;
- staging;
- consent;
- apply;
- restart/result/rollback.

They may share infrastructure, but one authority must not silently redefine another.

### 8. Bootstrap is separate from routine update

First install/bootstrap may require special migration logic or elevated privileges. Routine updates should use the smallest stable compatibility contract possible.

A breaking compatibility change requires an explicit bridge or fresh-install policy rather than silently growing permanent updater complexity.

### 9. Update state is structured

Default state machine:

```text
NONE
  -> STAGED
  -> PENDING
  -> ACCEPTED
  -> APPLYING
  -> COMPLETE
      or FAILED -> ROLLED_BACK / RETRYABLE
```

State should carry exact version/source/artifact identity and be safely recoverable after process or machine interruption.

### 10. Product GUI is not the downloader

For an interactive desktop product, the main GUI owns user-visible consent and status, not release discovery or arbitrary source materialization.

A dedicated local update agent/process may own discovery/staging. The GUI consumes already-prepared state and launches the bounded applier.

## Minimal project-start decisions

A project selecting this baseline records:

- product type and supported OS/architecture;
- expected distribution audience: single managed workstation, managed fleet, arbitrary consumers;
- release channel and immutable identity scheme;
- signing requirement and signing authority;
- staging provider;
- update compatibility line;
- consent policy;
- rollback strategy;
- bootstrap/update separation;
- whether any developer-only infrastructure is temporarily present on the target system.

## Transitional profile — managed development workstation

A project may temporarily use a local self-hosted runner as the staging provider when that is the fastest safe route to stable product work.

Allowed shape:

```text
hosted build/publish
  -> local runner stages + verifies
  -> pending state
  -> product consent
  -> hidden applier
```

This profile is acceptable only when all of the following are true:

- the system is explicitly a managed development/acceptance workstation;
- the runner is not described as a product requirement;
- pending/apply contracts do not depend on runner internals beyond the staged-state schema;
- a later product-local update agent can replace the runner without redesigning GUI consent or apply semantics.

## Full product profile

For arbitrary consumer systems:

```text
hosted build/test/package
  -> centralized signing
  -> immutable release/CDN/store
  -> installed product-local update agent
  -> managed staging + verification
  -> consent/policy gate
  -> isolated applier
  -> atomic adoption + rollback
```

Routine update must work without project checkout, WSL, CI runner, developer credentials or private build infrastructure.

## Non-selection

This baseline may be skipped for:

- throwaway prototypes;
- source-distributed developer tools where source build intentionally is the product;
- static artifacts with no installation/update lifecycle.

The non-selection record must include a review trigger such as "first external user", "second installation target", or "first persistent desktop release".

## Evidence origin

JAP demonstrated a simple and reliable stage-before-consent lifecycle on a managed workstation, but its local self-hosted runner is not an appropriate permanent dependency for arbitrary consumer machines.

PED demonstrated the security value of publisher signing, but also the cost of coupling routine publication and update adoption to an interactive local signing broker and multiple local trust transitions.

The combined baseline preserves JAP's lifecycle simplicity and PED's publisher-integrity lesson while removing developer-machine and self-hosted-runner dependencies from the eventual product contract.
