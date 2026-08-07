# Re-Entry and Evidence-Driven Failure/Replan Policy

Status: current known good baseline
Scope: multi-session, agent-assisted, autonomous, interruption-prone, or long-lived engineering work
Origin: DON/MCP and NOVI session-continuity and failure-governance lessons

## Purpose

Engineering work must be able to survive interrupted chats, agent replacement, local machine changes, CI delays, and partially completed actions without guessing what happened.

Continuation is reconstructed from durable project evidence. Failure handling is driven by classified evidence and viable hypotheses, not by an arbitrary retry counter.

## Core principles

### Repository truth outranks conversational memory

Repository state, live branch and commit heads, persisted checkpoints, issue state, CI evidence, and explicit authority records are canonical.

Chat handovers, summaries, generated status text, and human memory are useful bootstrap projections. They are not current truth until reconciled with live evidence.

### Reconcile, do not replay

After an interruption, do not blindly repeat the last remembered action.

First determine whether the action:

- never started,
- was prepared but not observed,
- completed successfully,
- completed partially,
- completed externally while the session was absent,
- or now conflicts with current repository truth.

Only then choose continuation, repair, replan, or safe stop.

### Persist mutation boundaries

For meaningful mutations, prefer durable checkpoints that distinguish intent from observation.

A useful minimum vocabulary is:

1. `SLICE_ACTIVATED`
2. `MUTATION_PREPARED`
3. `MUTATION_OBSERVED`
4. `VALIDATION_CLASSIFIED`
5. `REPLAN_ACCEPTED` when required
6. `MERGE_PREPARED` when applicable
7. `MERGED_SEALED` or another explicit terminal checkpoint

The exact schema may differ by project. The invariant is that a future session can distinguish what was intended from what was actually observed.

## Re-entry procedure

Before planning, mutation, or continuation after interruption:

1. Resolve live repository identity, default branch, active branch, and relevant commit heads.
2. Read the project's current-status and re-entry records if present.
3. Read the active task or slice record and its immutable base or equivalent anchor.
4. Inspect live diff, issue or task state, validation evidence, and unresolved decisions.
5. Compare live evidence with the persisted projection.
6. Classify the re-entry state.
7. Continue only inside the currently valid authority and scope envelope.

## Recommended re-entry classifications

- `EXACT_CONTINUATION` — live truth matches the persisted checkpoint; continue from the next declared action.
- `RECOVERABLE_ADVANCE` — the project advanced in a compatible way; adopt the newer truth and continue.
- `RECOVERABLE_EXTERNAL_PROGRESS` — an external actor or system completed relevant work; reconcile it before continuing.
- `STALE_PROJECTION` — the saved projection is outdated but live truth is coherent; refresh state before mutation.
- `CONTRADICTORY_STATE` — evidence conflicts materially; stop mutation until the contradiction is resolved.
- `AUTHORITY_BLOCKED` — the next action requires authority that is not currently granted.

These names are defaults, not mandatory literals. Projects may refine them while preserving the semantics.

## Evidence-driven failure classification

Every meaningful failure is classified before deciding whether to retry, repair, replan, or stop.

Useful classes include:

- `OPERATIONAL_BLOCKAGE` — tooling, environment, permissions, runner, network, or unavailable runtime.
- `GOVERNANCE_DEFECT` — inconsistent scope, authority, evidence binding, or process state.
- `IMPLEMENTATION_DEFECT` — the implementation does not satisfy its intended technical behavior.
- `CONVERGENCE_DEFECT` — local behavior works but repository-wide integration does not.
- `PRODUCT_OR_HYPOTHESIS_DEFECT` — implementation evidence rejects the intended product or solution hypothesis.
- `EVIDENCE_GAP` — the system cannot yet justify a conclusion because required evidence is missing.

Projects may add domain-specific classes.

## Hypothesis-aware continuation

A failure does not automatically mean that the current technical hypothesis failed.

After classification:

1. Persist the observed failure and relevant evidence.
2. Identify which hypothesis, assumption, environment condition, or governance binding was actually challenged.
3. Decide whether the current solution hypothesis remains viable.
4. Never replay an unchanged action without a material reason.
5. Continue autonomously when new evidence, a changed environment, a materially different implementation, or a materially different hypothesis justifies another action.
6. Persist a clean replan when the next action changes materially.

## Safe-stop conditions

Stop or request operator input when at least one of the following is true:

- no justified next hypothesis remains;
- available evidence is insufficient to choose safely and cannot be obtained inside the current authority envelope;
- live project state is materially contradictory;
- the next action would exceed scope, authority, budget, legal, safety, or irreversible-effect boundaries;
- a product or governance decision requires human authority;
- the active slice is no longer bounded enough to execute safely.

A fixed number of failed attempts is **not** a valid safe-stop condition by itself.

## Prohibited legacy behavior

Do not introduce or preserve fixed retry counters as a substitute for failure classification and hypothesis management.

Rules such as "stop after three attempts" are a legacy anti-pattern. If discovered in current governance, templates, re-entry records, generated task files, or copied project text, classify them as governance drift and replace them with this policy.

See `docs/anti-patterns/zombie_retry_rule.md`.
