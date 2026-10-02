# Engineering Delivery Control Plane (EDCP)

Status: current-known-good architectural baseline  
Origin: RCC / WBAA / JAP Cloud / JAP Classic delivery orchestration gap, 2026-10-02  
Operational parent: RCC issue #727  
Truth boundary: CKGB records the reusable architecture lesson; it does not own runtime delivery authority.

## Problem

A portfolio can have correct CI runners and still lack a coherent software-delivery lifecycle.

Observed portfolio evidence showed that:

- consumer repositories declare different validation workflows;
- RCC already owns shared execution admission, runtime materialization and exact assignment;
- PR/main/release/nightly/effectful validation semantics are not yet uniformly modeled;
- an expected validation can currently be represented by absence of a check;
- release, provider, experiment and recovery gates have grown independently across projects.

The missing layer is not another runner system. It is a portfolio-level **Engineering Delivery Control Plane** that defines which delivery lifecycle transition requires which evidence.

## Baseline principle

Separate **delivery intent**, **delivery lifecycle policy** and **execution capacity**.

A useful authority split is:

| Layer | Authority |
|---|---|
| Product / consumer repository | test assertions, product quality rules, build/release semantics, required capabilities |
| Engineering Delivery Control Plane | lifecycle/test classes, trigger semantics, blocking/effect/cost policy, evidence transitions and status model |
| RCC | workload admission, runtime/profile materialization, capacity, allocation, exact assignment, dispatch and execution evidence transport |
| WBAA or other engineering agents | bounded engineering execution when authorized |
| DON / observation layers | drift, optimization, planning signals; not delivery certification authority |
| CKGB | reusable baseline, project-start guidance and lessons learned; no runtime authority |

## Initial delivery lifecycle classes

### PR validation

Purpose: determine whether an exact proposed source revision is eligible to merge.

Typical properties:

- exact PR-head binding;
- automatic on relevant PR creation/update;
- provider-free by default;
- blocking by default;
- deterministic tests, static checks, architecture/contract guards.

### Main integration

Purpose: verify that current main remains coherent after integration.

Typical properties:

- exact current-main binding;
- broader integration/schema/build verification;
- may include cross-component checks that are too expensive for every PR.

### Scheduled validation

Purpose: detect time-based drift and run longer evidence cycles.

Examples:

- nightly E2E;
- source/connector census;
- dependency or environment drift;
- long-running reliability suites.

### Release qualification

Purpose: prove that a release candidate is distributable/promotable, not merely source-valid.

Examples:

- packaging;
- artifact identity;
- signing;
- installability;
- runtime startup;
- upgrade/rollback gates.

### Effectful validation

Purpose: verify behavior that requires real external systems, providers or product effects.

Requirements:

- explicit effect semantics;
- explicit provider/cost authority when relevant;
- no silent promotion into ordinary PR CI.

### Operator-gated experiment

Purpose: run novel, destructive, expensive or deliberately experimental validation.

Requirements:

- explicit approval;
- bounded scope;
- durable evidence and re-entry state.

## Required lifecycle semantics

A mature delivery contract should be able to declare at least:

- lifecycle/test class;
- trigger event;
- exact source binding;
- branch/ref scope;
- blocking vs advisory;
- validation-only vs effectful;
- provider allowed/forbidden;
- cost/budget class where applicable;
- concurrency/priority class;
- required execution capabilities;
- expected status contexts;
- retry/recovery semantics;
- promotion/unblock transition.

## Observability invariant

**Expected validation must never be represented by absence.**

For an expected lifecycle check, the source revision should expose an explicit state such as:

- admission pending;
- capacity pending;
- running;
- success;
- failure;
- blocked;
- superseded/cancelled.

No visible check is not equivalent to success and must not be an acceptable steady state for a required validation.

## Selection guidance

Select this baseline when a project has one or more of:

- PR-based engineering;
- shared CI infrastructure;
- multiple validation classes;
- release/promotion gates;
- external/provider effects;
- agent-driven engineering;
- cross-repository dependencies;
- significant cost, safety or recovery concerns.

A tiny project with one deterministic local test and no release lifecycle may not need a formal EDCP contract.

## Anti-patterns

- Runner infrastructure deciding project-specific test assertions.
- Every workflow implicitly inventing its own lifecycle semantics.
- Treating a pool-proof or infrastructure-proof workflow as normal product PR validation.
- Missing CI being indistinguishable from successful CI.
- Running provider/effectful tests automatically just because they are technically available.
- Reintroducing consumer-side runner selection to make a trigger easier.
- Creating a second scheduler when an existing execution plane can consume a declarative lifecycle contract.

## Current portfolio placement

RCC is the present operational host because it already owns the highest shared execution-orchestration layer through Demand-v2.

This is a pragmatic placement, not a permanent statement that EDCP must remain inside RCC forever.

A separate EDCP product/repository becomes justified only when it gains independent runtime authority, persistence, lifecycle state or consumers that no longer fit proportionately inside RCC.

## Project-start question

Before implementing CI/CD, ask:

> Which lifecycle transitions exist for this product, what evidence is required for each transition, who owns that evidence, and how is a missing or blocked validation made visible?

That question should be answered before choosing runner labels or workflow syntax.
