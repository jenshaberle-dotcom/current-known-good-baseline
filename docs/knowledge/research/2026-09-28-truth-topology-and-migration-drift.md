# Research: truth topology, supersession and drift in AI-maintained systems

Status: researched candidate for CKGB adoption  
Date: 2026-09-28  
Origin: repeated RCC architecture migrations; related JAP/PED/WBAA authority-replacement failures  
Scope: long-lived repositories, agent-assisted engineering, architecture migrations, documentation/versioning systems

## Question

How large can an AI-maintained system become, or how many update loops can it survive, before rule-based maintenance becomes unreliable because old and new truths coexist?

And, during a material redesign, should we:

- hard-delete old truth;
- create a new repository and harvest working assets;
- replace everything on a branch and promote that branch to main;
- or migrate incrementally?

## Short answer

There is no useful fixed threshold in lines of code, repository size, or number of update loops.

The more predictive variable is the **active truth surface**: how many artifacts can currently influence a decision, how many consumers resolve them, whether those consumers use the same precedence rules, and whether superseded artifacts remain discoverable or executable.

A large system can remain tractable when:

1. each concern has one current authority;
2. historical rationale is preserved separately from current operational truth;
3. migrations may temporarily contain two implementations, but only under one explicit migration authority/router;
4. superseded executable or machine-interpretable truth is physically removed from the active surface;
5. architecture/documentation invariants are machine-checked;
6. agents receive a small navigation map and retrieve deeper context progressively instead of ingesting an ever-growing manual.

The failure mode is therefore better described as **truth-topology drift** than as an intrinsic model hallucination problem.

## External evidence

### Agent-first repository design

OpenAI's 2026 report on an agent-first codebase is directly relevant. The team reports operating a roughly million-line, agent-generated codebase while treating repository knowledge as the system of record. Their early attempt to use one large `AGENTS.md` failed because context is scarce, large instruction sets become hard to navigate, stale rules accumulate, and monolithic guidance is difficult to verify mechanically.

Their replacement model uses:

- a short `AGENTS.md` as a map rather than an encyclopedia;
- structured repository-local documentation;
- progressive disclosure;
- versioned plans and technical-debt records;
- linters/CI that check documentation structure and freshness;
- recurring documentation/cleanup work to remove entropy.

This is evidence that repository size itself is not the decisive limit. The authority/navigation structure around the repository matters more.

Source: https://openai.com/index/harness-engineering/

### Context rot is measurable

Treude and Baltes (2026) describe stale persistent context in coding-agent configuration as **context rot**. They connect the problem to older documentation-consistency research and report that an existing README/wiki consistency checker found stale code-element references in 23.0% of a statistically representative sample of 356 repositories.

The useful CKGB interpretation is not that 23% is a universal failure threshold. It is that persistent agent context should be treated as a consistency-controlled software artifact, not as prose that can safely accumulate indefinitely.

Source: https://arxiv.org/abs/2606.09090

### Decision history must not masquerade as current truth

Current ADR guidance from Martin Fowler and Microsoft recommends an append-only decision history: accepted decisions are not silently rewritten; when direction changes, a new ADR supersedes the previous one and the records link to each other.

This preserves historical reasoning without requiring the previous decision to remain active operational authority.

Sources:

- https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record

### Incremental replacement is valid when duality is bounded

Established migration patterns deliberately permit old and new implementations to coexist temporarily:

- **Branch by Abstraction** routes consumers through one abstraction while implementations are replaced behind it.
- **Parallel Change / Expand-Migrate-Contract** first expands compatibility, migrates all consumers, then contracts by removing the old interface.
- **Strangler Fig / legacy displacement** moves slices of behavior or assets into the replacement while maintaining explicit ownership boundaries.

The important property is not "only one implementation exists at every instant." It is:

> Only one migration authority determines which implementation is current for a given consumer/domain, and the migration contains an explicit exit condition that removes the obsolete path.

Sources:

- https://martinfowler.com/bliki/BranchByAbstraction.html
- https://martinfowler.com/bliki/ParallelChange.html
- https://martinfowler.com/bliki/StranglerFigApplication.html
- https://martinfowler.com/articles/patterns-legacy-displacement/

### Architectural rules scale better when executable

Thoughtworks' evolutionary-architecture work uses architectural fitness functions: automated tests/metrics that continuously verify important architectural characteristics. This changes architecture from prose-only guidance into mechanically enforced constraints.

For CKGB, absence tests and authority-resolution tests are architectural fitness functions.

Source: https://www.thoughtworks.com/en-de/insights/articles/fitness-function-driven-development

## Core distinction: implementation duality vs truth duality

A migration can safely have two implementations:

`OLD_IMPLEMENTATION + NEW_IMPLEMENTATION`

provided there is one controlling authority:

`CURRENT_MIGRATION_CONTRACT -> resolver/router -> effective implementation`

Unsafe state:

`OLD_RULE -> consumer A`  
`NEW_RULE -> consumer B`  
`README -> agent C`  
`old test fixture -> agent D`  
`workflow default -> runtime E`

with no single resolver able to explain which one is authoritative.

This is the recurrent RCC/JAP/PED/WBAA failure class.

## CKGB model: current truth, transition truth, historical truth

Truth should be split into three classes.

### 1. CURRENT

May influence current planning, execution, validation, re-entry or runtime behavior.

For one concern, cardinality should normally be exactly one canonical authority.

### 2. TRANSITION

May temporarily contain old and new implementation details, but must have:

- one named migration owner/contract;
- one direction of travel;
- explicit consumer inventory;
- explicit cutover/contract condition;
- explicit expiry or completion criterion;
- tests proving resolution for each consumer;
- no independent claim by both implementations to be current authority.

### 3. HISTORICAL

Preserves why a previous decision existed.

Historical material may remain in Git history, superseded ADRs, completed migration records or an explicitly non-authoritative archive. It must not be discoverable as current configuration/instructions by normal execution or agent navigation paths.

## No fixed "number of update loops"

A repository does not become unsafe after update loop N.

Repeated updates are risky when each loop adds authority but does not retire authority.

A useful conceptual model is:

`Drift pressure ~= authority multiplicity x consumer fan-out x resolution ambiguity x change rate`

This is a CKGB diagnostic heuristic, not an empirical formula.

The practical implication is important:

- 100 sequential migrations can remain manageable if each completes contraction and leaves one current authority.
- 3 migrations can become unmanageable if each leaves behind active docs, tests, defaults, workflows and examples from previous generations.

Therefore **age and loop count are weak proxies; unresolved authority accumulation is the real debt**.

## Suggested measurable indicators

These are candidate CKGB diagnostics rather than industry-standard thresholds.

### Authority cardinality

For each architectural concern:

- target: exactly 1 CURRENT authority;
- TRANSITION may reference multiple implementations but exactly 1 migration authority;
- HISTORICAL artifacts must not be executable/current.

### Unclassified legacy references

Count references to superseded identifiers, labels, workflow names, defaults, paths and role descriptions.

Target after cutover: 0 unclassified references.

Allowed references must be explicitly historical, migration evidence, or negative regression tests.

### Consumer-resolution coverage

For every known consumer, answer:

`consumer -> lookup path -> resolver -> effective authority`

Target for high-risk migrations: 100% known-consumer coverage.

### Negative architecture tests

Do not only test that the new path works.

Also test that forbidden old:

- labels;
- workflow selectors;
- config keys;
- paths;
- role names;
- defaults;
- provider routes;
- documentation entrypoints

cannot return unnoticed.

### Migration half-life

A transition must have a contract/end state. An indefinitely open compatibility layer is treated as an architecture-debt signal.

No universal number of days is proposed because acceptable duration depends on external consumers and reversibility.

## Decision matrix for major redesigns

### A. Hard cut inside the existing repository

Use when:

- all relevant consumers are controlled;
- old and new semantics are incompatible;
- coexistence adds more risk than cutover;
- rollback is available through Git/release history;
- the replacement can be validated before merge.

Method:

`Introduce -> Rebind Consumers -> Destroy Old Authority -> Prove Absence -> Prove E2E`

This should be the default for **authority replacement** such as runner labels, ownership rules, routing rules, canonical config, role contracts and agent instructions.

### B. Branch by Abstraction

Use when:

- replacement is large but a stable seam can be created;
- the system must stay releasable during migration;
- clients can be moved incrementally.

The abstraction, not either implementation, becomes the current authority during transition.

Delete the old implementation after the last consumer moves.

### C. Expand-Migrate-Contract

Use for:

- APIs;
- schemas;
- file formats;
- database fields;
- interfaces with multiple consumers.

The dangerous failure is stopping after "migrate" and never executing "contract."

The contract phase is therefore a mandatory completion gate.

### D. Strangler / sliced replacement

Use when:

- a large subsystem cannot be safely replaced atomically;
- ownership can be partitioned by domain, asset, route or capability;
- each migrated slice can have one clear system of record.

Do not allow both systems to remain system-of-record for the same slice without an explicit synchronization authority.

### E. Disposable replacement branch with moving main and proof-gated promotion

Use when:

- most of the active tree or one architectural concern must change coherently;
- incremental coexistence inside the productive path would create excessive semantic ambiguity;
- the replacement can be developed and qualified outside the productive authority surface.

Main does **not** need to freeze. Main remains the single productive/current authority and may continue to receive normal work.

Rules:

- the replacement branch is a candidate, not a second current truth;
- the branch should be disposable if the approach does not carry;
- changes landing on main during the experiment must be reconciled into the candidate before promotion;
- if main changes the same architectural concern, explicitly classify whether the candidate must absorb, supersede or restart from that change;
- immediately before promotion, rebase/merge against the latest main and run the complete positive and negative proof suite on that reconciled head;
- promotion is allowed only from a candidate proven against current main, not against an old branch point;
- after successful promotion, the replacement branch is deleted; after failed qualification, it is abandoned/deleted and a new attempt may start from current main.

This permits two moving Git histories while preserving only one productive authority. The dangerous state is not "main and a branch both receive commits"; it is allowing the candidate branch to acquire independent production authority or promoting a candidate that was only proven against stale main.

A useful pattern is:

`CURRENT_MAIN(A) + DISPOSABLE_CANDIDATE(B)`

-> `reconcile candidate with latest CURRENT_MAIN`

-> `prove B + prove absence/conflict resolution`

-> `promote`

-> `CURRENT_MAIN(B)`

A failed candidate becomes evidence, not architecture. Harvest lessons/ADRs from it, then discard its active implementation state.

### F. New repository + harvest

Use only when the architecture itself is intentionally sacrificial or the active truth surface is so contaminated that separating current from historical authority is more expensive/risky than establishing a clean root.

Suitable signals:

- most modules would be deleted rather than migrated;
- dependency/ownership boundaries are being redrawn almost completely;
- tests encode the old architecture rather than product behavior;
- CI/workflows/config/docs would need wholesale replacement;
- a small set of assets can be explicitly harvested and re-qualified;
- consumers can be deliberately cut over;
- the old repository can be archived/read-only or clearly demoted.

A new repository is **not** a substitute for understanding behavior. Harvested assets must be treated as imports that require re-qualification, not as automatically trusted truth.

Fowler's "Sacrificial Architecture" supports planned replacement as a legitimate lifecycle choice, but it does not make rewrites inherently safer.

Source: https://martinfowler.com/bliki/SacrificialArchitecture.html

## Recommended default for RCC-style architecture changes

For RCC-like shared infrastructure, prefer:

1. define the new architecture and authority map;
2. freeze creation of new legacy patterns;
3. inventory consumers and authority paths;
4. create a single migration resolver/profile contract if incremental migration is required;
5. migrate consumers;
6. perform a hard contraction: delete old code/config/tests/docs/workflows from the active surface;
7. add negative regression guards;
8. prove the new path on representative consumers;
9. keep old rationale only as Git history/superseded decision evidence.

This combines incremental migration where needed with a hard-cut completion rule.

## Why repeated manual deep scans are not the target state

Multiple independent deep scans are useful during recovery because each pass may discover a different representation of old authority.

They are not a scalable steady-state control because their completeness is difficult to prove and their cost grows with repository size.

A better steady state is:

- deterministic forbidden-pattern inventories;
- machine-readable authority IDs;
- consumer manifests where practical;
- architecture fitness tests;
- documentation/reference linting;
- explicit CURRENT/TRANSITION/HISTORICAL state;
- automatic failure when a removed authority reappears.

Deep scans remain a final audit technique, not the primary mechanism that keeps the repository coherent.

## Agent instruction architecture

For AI-maintained repositories:

### Keep the root instructions small

Root agent instructions should answer:

- where current truth lives;
- how to discover task-specific truth;
- which commands prove correctness;
- which boundaries must not be crossed;
- how superseded/historical material is marked.

They should not duplicate all architecture and migration history.

### Progressive disclosure

Use a shallow navigation hierarchy:

`agent entrypoint -> architecture/index -> concern-specific current authority -> evidence/tests`

Avoid:

`agent entrypoint -> huge mixed history/current manual`

### Historical docs must be retrieval-safe

If historical material remains in the repository, it should be clearly separated and excluded from normal current-context discovery where tooling allows.

A filename containing "legacy" is not sufficient if semantic search, grep, tests or examples still surface its content as actionable current guidance.

## Proposed CKGB invariant

> **One concern, one current authority. Multiple implementations are allowed only inside an explicitly bounded transition controlled by one migration authority. Superseded operational truth must leave the active authority surface; historical rationale remains append-only and explicitly non-authoritative.**

## Proposed migration state machine

`CURRENT_A`

-> `TRANSITION(A,B; one resolver; explicit exit criteria)`

-> `CURRENT_B`

Illegal stable states:

- `CURRENT_A + CURRENT_B` with independent resolution;
- `TRANSITION` without completion criteria;
- `CURRENT_B` while old authority remains executable/discoverable and unclassified;
- historical records that can still drive current execution.

## Consequence for CKGB

The existing control `docs/controls/hard-cut-rule-replacement.md` is directionally correct and should remain the single control for this concern.

Do **not** create a second overlapping "truth drift" control.

Instead, extend that control with:

- the CURRENT / TRANSITION / HISTORICAL distinction;
- bounded-duality semantics;
- migration strategy selection;
- measurable absence/resolution checks;
- the rule that deep scans are recovery/audit tools, not the steady-state operating model.

This avoids reproducing the very redundancy problem being studied.

## Research conclusion

The RCC experience should not be classified primarily as an LLM hallucination problem.

It is an architecture-of-truth problem amplified by agents:

- agents reproduce discoverable repository patterns;
- stale documentation/configuration can look equally legitimate to the model;
- every unretired rule increases the number of plausible resolution paths;
- repeated migrations compound this ambiguity.

The scalable response is therefore not "use a smarter model" or "scan harder forever."

It is to make the repository easier to reason about:

**single current authority, bounded transitions, append-only history, destructive contraction, executable invariants, progressive context disclosure, continuous garbage collection.**
