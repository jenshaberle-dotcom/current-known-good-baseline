# CKGB Architecture Lifecycle

Status: current-known-good candidate
Control ID: CKGB-ARCH-LIFECYCLE-001
Scope: shared architecture, cross-project infrastructure, release, migration and platform evolution
Owner issue: #21

## Purpose

CKGB records shared architecture only after real project evidence exists. A useful architecture idea is not automatically portfolio authority.

The default operating rule is:

> Product delivery keeps moving. Shared architecture is harvested, proven on bounded real consumers, and promoted separately.

Architecture work may enter the active product path only when it is directly required for the next safe product outcome, no safe bypass exists, and the selected change is the smallest sufficient safe solution.

## Architecture maturity

Every shared architecture item uses one explicit maturity state:

- `SIGNAL` — friction or repeated effort observed; no design authority.
- `CANDIDATE` — plausible reusable design recorded; no consumer obligation.
- `POC` — bounded implementation proves technical feasibility.
- `PILOTED` — one real consumer uses it in a normal path with known-good fallback.
- `PROVEN` — repeated real workload evidence exists; failure/recovery/rollback behavior is understood.
- `STANDARD` — CKGB-approved default or conditional baseline with explicit adoption semantics.

Planned behavior may not be described as proven behavior.

## Default authority

Unless a later explicit promotion says otherwise:

```text
blocks_product = false
migration_authority = false
```

An architecture candidate may block only its own unsafe effect or a directly dependent operation. It must not become a generic project work-admission gate.

Examples:

- DRJ reconciliation debt does not block unrelated product work.
- A Fleet Registry candidate does not block a product merely because the product has not migrated to it yet.
- A release-management improvement does not block ordinary source development unless the work is at the release/promotion boundary it governs.

## Outcome lock and Delivery-before-Platform

When an E2E outcome is active, newly discovered work is classified before it can expand scope.

Admit it into the active delivery path only when all are true:

1. it blocks the next outcome step;
2. there is no safe bypass or known-good fallback;
3. the chosen repair is the smallest sufficient safe change.

Otherwise harvest it to the platform/architecture backlog and continue the E2E outcome.

Root-cause learning is still required. Generalization, framework extraction and portfolio rollout are separate decisions.

## Shared architecture migration contract

Default migration sequence:

```text
DISCOVER
  -> POC
  -> ONE REAL CONSUMER PILOT
  -> PARALLEL / SHADOW OPERATION
  -> REAL WORKLOAD PROOF
  -> CONSUMER CUTOVER
  -> SOAK
  -> SECOND CONSUMER
  -> STANDARD ACCEPTANCE
  -> LEGACY RETIREMENT
```

Migration rules:

- new infrastructure never destroys the known-good fallback before proof;
- migration is not a prerequisite for the POC;
- migrate one bounded consumer first, not the portfolio;
- prefer `adopt_on_touch` over `migrate_all_now` unless a concrete risk or incompatibility requires coordinated migration;
- legacy retirement requires replacement proof, reconciliation and rollback/recovery evidence;
- failed consumer adoption stops that consumer's cutover, not unrelated projects;
- ambiguous current state fails closed for the effect, not for unrelated work;
- migration implementation must not silently expand into a general framework unless that expansion is separately promoted.

## Adoption modes

A `STANDARD` must declare one adoption mode:

- `new_projects` — default only for newly created projects.
- `adopt_on_touch` — existing projects adopt when the relevant subsystem is next materially changed.
- `mandatory` — portfolio migration is required; this needs explicit reason, scope, transition plan, rollback and completion criteria.

`mandatory` is exceptional and must not be inferred from architectural quality alone.

## Release-management core

A release-capable project should converge on the following shared release truth where applicable:

- exact source SHA;
- semantic release impact (`MAJOR | FEATURE | FIX | NONE` or equivalent);
- monotonic version lineage;
- candidate qualification bound to exact source/version;
- visible GitHub Release/tag ledger;
- release notes and known limitations;
- idempotent publication/adoption;
- release/install/update state must fail closed on identity mismatch.

Profiles refine the core instead of forcing one implementation on every project.

### Ordinary repository/product profile

CI-qualified exact source plus GitHub Release/tag and release notes may be sufficient.

### Local application profile

Add real operator-path installability, side-by-side candidate or atomic replacement, preserved runtime/user state, update smoke and rollback/recovery proof.

### Privileged host/control-plane profile

Add local host proof, signing/provenance where required, exact installed-source/version binding and rollback. GitHub Release is visible evidence and release metadata; it is not by itself executable host authority.

## Architecture register minimum fields

A promoted or tracked shared architecture item should record at least:

```text
architecture_id
source_project
observed_friction
claimed_benefit
maturity
pilot_consumer
proof_refs
known_good_fallback
blocks_product
migration_authority
adoption_mode
rollback_or_recovery
known_limitations
```

## Promotion gate

Promotion to `STANDARD` requires evidence of all applicable items:

- observed project friction or measurable repeated cost;
- bounded implementation proof;
- at least one real consumer path;
- normal-workload evidence, not only fixtures;
- known failure mode and recovery/rollback behavior;
- explicit authority boundary;
- measurable benefit or clear risk reduction;
- explicit non-selection/adoption criteria;
- no unresolved contradiction with current CKGB principles.

A second real consumer is normally required before portfolio-wide `mandatory` adoption.

## Evidence origins for this contract

- RCC Cold-to-Warm migration: correct safety rules coexisted with scope expansion into fleet identity, routing, profiles, base layout, registry and migration UX.
- RCC release/version work: release impact, version monotonicity and host-proof boundaries need explicit release authority.
- DRJ extraction: read-only parity, destructive parity, host proof and only then ownership transfer/legacy removal; DRJ also proves retention state must not become unrelated project admission authority.
- PED release/installer work: real operator install/update path and host policy are release gates for local products.
- PED retention work: lifecycle and retention should increasingly be defined at creation time instead of repaired later by cleanup.
- JAP/WBAA: E2E product outcomes and real customer flights should prove reusable orchestration/LLM/worker architecture before portfolio promotion.

## Anti-goals

This contract does not:

- create a new runtime control plane;
- authorize any current project migration;
- force current projects to adopt candidates;
- grant runner, provider, cleanup, release or host effects;
- replace project-specific product authority;
- justify architecture work merely because it is reusable or elegant.
