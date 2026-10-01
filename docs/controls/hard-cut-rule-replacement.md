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


## Truth classes

Authority-bearing repository material must be classified conceptually as one of:

- `CURRENT`: may influence current planning, execution, validation, re-entry or runtime behavior;
- `TRANSITION`: temporary migration material governed by one explicit migration authority, direction and completion condition;
- `HISTORICAL`: preserved rationale/evidence that must not act as current configuration or instruction.

For one architectural concern, `CURRENT` authority cardinality should normally be exactly one.

Historical truth belongs in Git history, superseded ADRs, completed migration records or an explicitly non-authoritative archive. Retaining history does not justify retaining obsolete operational authority on the active execution/context surface.

## Bounded duality during migration

This control does **not** require one physical implementation to exist at every instant.

Established migration techniques such as Branch by Abstraction, Expand-Migrate-Contract and Strangler-style displacement may require old and new implementations to coexist temporarily.

Safe duality requires:

1. one migration contract/resolver is current authority;
2. every consumer has an explainable resolution path;
3. the direction of travel is explicit;
4. cutover/contract conditions are explicit;
5. the old implementation cannot independently present itself as current authority;
6. the migration finishes with destructive contraction of superseded operational truth.

Therefore:

> **Two implementations may coexist. Two independent current truths may not.**

A stable state of `CURRENT_A + CURRENT_B` is forbidden when both can independently resolve the same concern.

The intended state machine is:

`CURRENT_A -> TRANSITION(A,B; one resolver; exit criteria) -> CURRENT_B`

## Strategy selection

Choose the replacement mechanism based on the shape of the change:

- **Hard cut in the existing repository**: default for controlled authority replacement such as runner labels, ownership rules, routing rules, agent instructions, canonical configuration and role contracts.
- **Branch by Abstraction**: use when a large supplier/component can be replaced incrementally behind a stable seam while keeping the system releasable.
- **Expand-Migrate-Contract**: use for APIs, schemas, file formats and interfaces with multiple consumers. The contract/removal phase is a mandatory completion gate.
- **Strangler / sliced replacement**: use when a large subsystem must move domain-by-domain or asset-by-asset. Each migrated slice must have one clear system of record.
- **Short-lived replacement branch + atomic cutover**: use when most of the active tree must change together and incremental coexistence would create more ambiguity than safety. Do not allow two long-lived moving baselines.
- **New repository + harvest**: reserve for intentionally sacrificial architecture or cases where most of the old active surface would be discarded and a small set of assets can be explicitly re-qualified. The old repository must be archived/demoted rather than remain a competing current baseline.

Repository size alone is not a reason to choose a new repository.

## Scale rule: bound active truth, not repository size

There is no CKGB threshold in lines of code or number of update loops after which agent-assisted maintenance is assumed to fail.

The controlling concern is accumulated unresolved authority.

Use this diagnostic heuristic only as a reasoning aid, not as an empirical formula:

`drift pressure ~= authority multiplicity x consumer fan-out x resolution ambiguity x change rate`

A repository may survive many migrations if each finishes contraction and leaves one current authority. A small repository may drift after only a few changes if old docs, tests, defaults, workflows and examples remain active.

## Measurable completion evidence

For high-risk replacement, prefer measurable evidence over repeated interpretive scans:

- **Authority cardinality**: one `CURRENT` authority per concern.
- **Unclassified legacy references**: zero after cutover; any retained reference is explicitly historical, migration evidence or a negative regression test.
- **Consumer-resolution coverage**: every known consumer maps through `consumer -> lookup -> resolver -> effective authority`.
- **Negative architecture tests**: forbidden legacy labels, paths, config keys, role names, workflow selectors or defaults fail CI if reintroduced.
- **Migration completion condition**: every `TRANSITION` has an explicit exit/contract criterion.
- **Documentation/context checks**: stale current instructions and broken cross-links are mechanically detectable where practical.

These are architectural fitness functions: they prove not only that the new path works, but that the removed path cannot silently regain authority.

## Deep scans are recovery tools, not the steady-state control

Multiple independent deep scans are useful when repairing a repository that already contains contradictory truth because different passes can expose different representations of the old authority.

They do not scale as the primary operating model.

The target steady state is deterministic:

- machine-readable authority identifiers where practical;
- explicit consumer inventories for high-risk shared infrastructure;
- forbidden-pattern searches;
- architecture fitness tests;
- CURRENT/TRANSITION/HISTORICAL separation;
- automatic failure on resurrection.

Use deep scans as final audit/recovery evidence, not as the mechanism required after every routine change.

## Agent-context rule

For AI-maintained repositories, the root instruction file should be a map, not a duplicated architecture manual.

Prefer progressive disclosure:

`agent entrypoint -> architecture/index -> concern-specific current authority -> tests/evidence`

Do not copy the same operational rule into multiple agent instructions, READMEs, plans and examples unless one is generated from the canonical source or mechanically checked for equivalence.

Historical documents must be retrieval-safe: merely naming a file `legacy` or `deprecated` is insufficient if normal semantic search, grep, examples or tests still surface it as actionable current guidance.

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

## Research basis

See `../knowledge/research/2026-09-28-truth-topology-and-migration-drift.md` for the external research, migration-pattern comparison and RCC-oriented synthesis that extends this control.
