# Explicit Release Intent Orchestration

Status: current-known-good candidate
Control ID: CKGB-RELEASE-INTENT-001
Maturity: `CANDIDATE`
Origin: PED release-control work, Issue #382 / PR #383
Extends: `CKGB-RELEASE-GITHUB-001`
Owner issue: #27

## Purpose

Separate the decision **"we want a release now"** from ordinary development merges and from the mechanics that publish release artifacts.

The reusable control is an explicit release-intent orchestrator. It accepts a bounded semantic intent, binds that intent to exact current source, prepares canonical version identity, and delegates publication to the project's existing canonical publisher.

It does **not** infer release intent from arbitrary source changes and it does not create a second release publisher.

## Observed friction

PED exposed a gap between two otherwise sound controls:

- normal product PRs were qualified before merge;
- a release workflow could publish an immutable application release from canonical release metadata.

What was missing was an operator-facing control that could explicitly say **release this known-good product state now** without manually editing several version files or making every product merge release-bearing.

That gap creates three bad alternatives:

1. release every qualifying product merge whether wanted or not;
2. manually edit version metadata whenever a release is desired;
3. duplicate publication logic in an ad-hoc release helper.

The candidate control removes that ambiguity.

## Core invariant

Release intent, release preparation and release publication are separate authorities:

```text
ordinary development
    -> qualified main

explicit release intent
    -> exact-source lock
    -> deterministic version preparation
    -> canonical publisher
    -> immutable release verification
```

No explicit release intent means no release effect.

## Generic operator contract

A project selects one or more explicit operator entry points. The intent vocabulary should remain small and deterministic. For SemVer projects the default candidate vocabulary is:

```text
patch | minor | major
```

Equivalent project-native vocabularies are acceptable when they map deterministically to version impact.

The control should support at least one direct administrative entry point such as a manually dispatched workflow. A ChatOps surface may be added when it is useful, but it must be bounded to an authenticated/authorized actor and an exact command grammar.

Example ChatOps grammar:

```text
/release patch
/release minor
/release major
```

Unknown actors, unknown commands and ambiguous intent fail closed.

## Canonical orchestration flow

```text
EXPLICIT INTENT
  -> AUTHORIZE ACTOR
  -> CAPTURE CURRENT MAIN SHA
  -> RESOLVE CURRENT RELEASE BASELINE
  -> VALIDATE CANONICAL VERSION IDENTITY
  -> COMPUTE NEXT VERSION DETERMINISTICALLY
  -> REFUSE EXISTING TARGET TAG / RELEASE CONFLICT
  -> PREPARE ONLY CANONICAL VERSION IDENTITY
  -> RECHECK MAIN == CAPTURED SOURCE SHA
  -> COMMIT / PUBLISH VERSION PREPARATION
  -> INVOKE EXISTING CANONICAL PUBLISHER
  -> WAIT FOR PUBLISHER TERMINAL STATE
  -> VERIFY TAG + EXACT SOURCE + REQUIRED ASSETS + DIGESTS
  -> RECORD RELEASE OUTCOME
```

The exact implementation may use a version commit, a release PR or another deterministic preparation artifact. What matters is that the release source and prepared version identity remain exact and reviewable.

## Exact-source / stale-main rule

The orchestrator must capture the intended release source before version preparation.

Immediately before any mutation that makes the release version authoritative, re-read the target branch. If it no longer equals the captured source, stop and require a new release intent.

Do not silently release a newer `main` merely because development moved while the release request was being prepared.

This is a release-specific application of CKGB authority freshness / Deadwalker handling.

## Canonical version identity

A project must define which files/fields constitute release identity. The orchestrator may update only that declared set.

A local application commonly binds:

```text
product/version manifest
package/project version
native host/build identity
```

Before mutation, those fields must agree on the current version. After mutation, they must agree on the next version. Pre-existing drift fails closed instead of being normalized opportunistically.

The version preparation step should prove that no unrelated file changed.

## Deterministic version semantics

For SemVer:

- `patch`: `X.Y.Z -> X.Y.(Z+1)`
- `minor`: `X.Y.Z -> X.(Y+1).0`
- `major`: `X.Y.Z -> (X+1).0.0`

Projects may use a different version scheme, but the mapping from intent to next version must be deterministic and testable.

A release orchestrator must not guess semantic impact from changed filenames or commit wording unless that inference mechanism is itself a separately governed project contract.

## Single-publisher rule

The release-intent orchestrator prepares and requests a release. It does not independently build/sign/publish a second copy of the product.

There must be one canonical publisher for a release namespace.

For projects selecting `CKGB-RELEASE-GITHUB-001`, the orchestrator delegates to the existing GitHub Release publisher, which remains responsible for:

- exact release-source checkout;
- build/package production;
- signing/provenance where applicable;
- checksum/manifest generation;
- immutable tag/release creation;
- required-asset verification.

This prevents release intent from becoming a parallel release channel.

## Provider / platform boundary

The **release-intent abstraction** is provider-independent:

```text
intent -> authority -> source lock -> deterministic version preparation -> canonical publisher -> verification
```

A repository may implement the entry and publication adapters with GitHub Actions, another CI system, or a local governed broker.

Do not import a third-party release framework merely to obtain this state machine unless that dependency provides clear project value. The orchestration contract should remain project-owned and portable.

The GitHub implementation observed in PED uses:

- `workflow_dispatch` for direct explicit intent;
- an owner-gated issue-comment command surface for optional ChatOps;
- the pre-existing canonical GitHub Release workflow as publisher.

Those are implementation adapters, not the architecture itself.

## Authority and permissions

Keep permissions minimal by phase.

The release-intent path may need authority to update canonical version identity and request the canonical publisher. Publication authority remains with the publisher. Signing/private-key or privileged host authority remains a separate boundary where required.

A ChatOps implementation must additionally bind:

- exact repository;
- dedicated issue/control surface or equivalent bounded channel;
- authenticated actor identity;
- exact allowed command grammar;
- one serialized release-intent concurrency domain.

## Concurrency and idempotency

Serialize release-intent execution for a release namespace.

Before preparing a target version, resolve the current published baseline and target tag/release. Refuse a conflicting existing target.

If the exact intended immutable release already exists with the expected source and complete asset contract, classify it as already released rather than creating another equivalent release.

If source, version, tag or assets disagree, fail closed.

## Qualification contract

At minimum test:

- each valid semantic bump;
- malformed/unsupported intent rejection;
- unauthorized actor rejection for ChatOps;
- canonical identity drift rejection;
- stale-main race rejection;
- duplicate/conflicting target tag rejection;
- only canonical version files may change during preparation;
- canonical publisher is invoked rather than duplicated;
- publisher failure does not get converted into a second publication path;
- successful publication resolves to the exact expected source and required asset set.

## Consumer separation

This control decides and produces a release. It does not define how a consumer installs it.

Consumer update/install behavior remains governed by the selected release-delivery profile, including checksum/manifest verification, staged probe, swap and rollback where applicable.

## Failure rules

Fail closed on:

- missing or ambiguous release intent;
- unauthorized actor;
- stale target branch after source capture;
- inconsistent current version identity;
- non-deterministic or invalid next version;
- unexpected file changes in version preparation;
- existing conflicting tag/release;
- canonical publisher failure;
- published tag resolving to the wrong source;
- missing required release assets or digest evidence.

A failed release intent does not authorize force-pushing `main`, retargeting an immutable tag, editing an existing release in place, or publishing through a fallback channel.

## Known-good fallback

Until this candidate is proven, projects keep their existing explicit/manual release procedure. Adoption of the candidate must not remove that known-good recovery path before the first real release and recovery behavior are observed.

## Maturity and promotion

Current maturity is `CANDIDATE`.

Reason:

- the friction is real and reusable;
- PED has implemented the bounded design in PR #383;
- the mechanism has not yet completed a normal real PED release through the new intent path at the time of harvest.

Promotion path:

```text
CANDIDATE
  -> PED implementation qualification
  -> real PED release through explicit intent
  -> failure/recovery evidence
  -> PILOTED
  -> second consumer or repeated normal-workload evidence
  -> PROVEN / possible STANDARD decision
```

Do not describe the mechanism as portfolio-proven until that evidence exists.

## Adoption semantics

While `CANDIDATE`:

```text
blocks_product = false
migration_authority = false
adoption_mode = none
```

Projects may evaluate or pilot it voluntarily. No existing project is required to migrate its release process.

## Evidence origins

PED source project:

- Issue #382 — persistent explicit release-control surface;
- PR #383 — release-intent orchestrator candidate;
- existing PED Control Center publisher — immutable release workflow reused as the sole publisher.

Related CKGB controls:

- `docs/tooling/github-release-delivery-baseline.md` (`CKGB-RELEASE-GITHUB-001`);
- `docs/ckgb/architecture_lifecycle.md` (`CKGB-ARCH-LIFECYCLE-001`);
- Deadwalker / authority-freshness controls for stale-source protection.
