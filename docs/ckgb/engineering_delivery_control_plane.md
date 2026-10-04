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

## Trigger plane and identity independence

A delivery control plane is incomplete if a valid test request can only be initiated from one historical developer host or from credentials whose authority exists accidentally because that host's interactive user is a repository administrator.

The project should separate four concerns:

```text
REQUESTER
  -> AUTHENTICATED TRIGGER CONTRACT
  -> DELIVERY / TEST POLICY
  -> RCC OR OTHER EXECUTION PLANE
  -> EVIDENCE
```

A Work chat, engineering agent, CLI, repository event or operator UI may all be request surfaces. None should need to become the CI authority itself.

The trigger contract should accept bounded intent such as:

- repository and exact source/ref;
- requested lifecycle/test class or named suite;
- reason/correlation ID;
- effect/cost class;
- optional suite parameters permitted by policy.

The delivery control plane resolves that intent to the currently valid test selection and execution policy. The requester must not need runner identity, runner labels, physical topology or a privileged shell on a particular host.

### Identity and authorization baseline

For serious agent-assisted projects:

- prefer workload/service identity with least privilege over a developer's long-lived personal admin credential;
- authenticate the trigger at the repository/control-plane boundary and authorize the requested action separately;
- bind execution and resulting evidence to the exact requested source revision;
- make repository scope and allowed lifecycle/test classes explicit;
- require stronger approval for effectful, destructive, release or high-cost suites;
- use short-lived/federated credentials where the platform supports them;
- keep secrets and privileged publisher/host authority outside chat context and outside ordinary test requests;
- record requester identity, policy decision, selected suite, source identity and result as durable evidence.

A Work chat therefore triggers CI **indirectly**: it submits authenticated test intent to a stable trigger surface. The delivery policy selects the suite and RCC (or another execution plane) supplies capacity. The chat does not depend on whichever developer machine happens to have an administrator login.

### Trigger availability invariant

If remote/agent-driven engineering is a supported operating mode, at least one supported trigger surface must be reachable without the developer's historical workstation.

A project must not claim chat/agent-operable CI when the only working path is effectively:

```text
chat -> human -> privileged local host -> personal admin token -> workflow
```

That path may remain an emergency/operator fallback, but it is not the normal delivery architecture.

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
