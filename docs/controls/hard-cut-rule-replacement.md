# CKGB control: Hard-cut rule replacement and single-current-authority

Status: current-known-good candidate
Control ID: CKGB-CTRL-HARD-CUT-RULE-REPLACEMENT-001
Technical class: authority coexistence / deadwalker prevention / semantic drift

## Origin

JAP/PED updater replacement and the WBAA Sol-first model-routing cut exposed the same failure class: installing a new rule does not reliably neutralize an old rule while both remain discoverable, executable or machine-interpretable in the repository.

A repository that is treated as current truth must not contain multiple incompatible current authorities and rely on consumers to infer which one wins.

## Core rule

**Replace = Introduce + Destroy + Prove Absence.**

A rule replacement is incomplete until:

1. the new authority exists and is bound to its consumers;
2. every superseded executable or machine-interpretable current-authority artifact is physically removed from the active repository surface;
3. retained history is explicitly non-authoritative and cannot be consumed as current configuration;
4. regression guards prove that the superseded authority cannot silently return.

Adding a new rule beside an old rule, marking the old rule deprecated, or relying on documentation precedence is not a completed replacement when the old artifact can still influence execution, planning, validation, defaults, tests, re-entry or agent context.

## Why coexistence is unsafe

Different consumers resolve authority differently. A workflow may use a hard-coded default while an agent reads a current plan, a test preserves an old contract, a CLI uses another default and a re-entry projection points elsewhere.

Therefore the important question is not only **which rule is declared canonical**, but:

> **Which rule wins for each real consumer and execution path, and why?**

Coexisting incompatible authority creates deadwalker potential even when the intended new rule is correct.

## Required search-and-destroy surface

For a superseded rule, inspect at least:

- executable code;
- configuration and schemas;
- CI/CD workflows and triggers;
- tests and fixtures;
- CLI defaults;
- re-entry/current-status projections;
- planning/governance documents consumed by agents;
- generated context or templates;
- examples that can be copied or executed;
- authority IDs, sentinel strings and legacy campaign/rule identifiers.

Git history may preserve historical truth. The active checkout must not preserve obsolete current authority merely for history.

## Authority-resolution proof

A hard cut should record:

- old authority identity;
- new authority identity;
- known consumers;
- previous resolution paths;
- artifacts deleted or converted to historical-only;
- remaining allowed references and why they cannot carry current authority;
- regression guard;
- target-native/full-suite qualification.

Where practical, validate the chain:

`Declared Authority -> Discoverable Authority -> Consumer -> Resolution Path -> Effective Authority -> Runtime Outcome`

## Drift / deadwalker classes

- `DORMANT_DEADWALKER`: obsolete authority remains discoverable but has no proven current consumer.
- `CONDITIONAL_DEADWALKER`: old or new authority wins depending on entry path.
- `AUTHORITY_INVERSION`: declared new authority exists but an old authority wins in an actual path.
- `SPLIT_TRUTH`: different current consumers simultaneously resolve incompatible authorities.
- `RESURRECTION`: a previously inactive superseded authority regains influence after a later change.

These extend, rather than replace, the temporal authority freshness controls in `deadwalker_quarantine_protocol.md`.

## Role-change rule

A component or agent role change uses the same hard-cut semantics:

**Define New Authority -> Inventory Old Authority -> Classify Keep/Transfer/Delete -> Hard Delete Conflicts -> Install New Authority -> Prove Absence -> Prove New E2E Role.**

Do not preserve an old capability merely because it already exists. If it conflicts with the new role, it must leave the active authority surface or be converted into demonstrably non-authoritative historical evidence.

## Regression requirement

For high-risk authority replacement, add a machine-executable guard that fails when forbidden legacy paths, identifiers, direct defaults or equivalent authority patterns reappear.

A green new-path test without an absence proof is insufficient.

## Reference incidents

- JAP/PED updater work: legacy update paths and documentation could compete with replacement architecture until physically removed and regression-guarded.
- WBAA Sol-first routing: stale Astra-first workflows, defaults and tests survived introduction of the new router and attempted to preserve old behavior. The corrective pattern is a hard cut: Astra remains available only through the central evidence-based escalation authority; direct Astra-first authority is removed.

## Consequence for autonomous systems

Autonomous agents must not be expected to resolve contradictory repository authority through judgment alone. Reduce ambiguity before execution. A planner or drift detector should flag authority coexistence before an execution agent spends provider budget or performs external effects.
