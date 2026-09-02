# Re-entry, failure classification and authority freshness

Status: current-known-good candidate
Scope: multi-session, agent-assisted, autonomous or interruption-prone engineering

## Repository truth first

Repository state, live branch/head, current status/re-entry records, active issue/PR state and explicit authority records outrank chat summaries and remembered handovers.

## Reconcile before replay

After interruption or delayed external execution, classify the prior action before continuing:

- never started;
- prepared but not observed;
- completed and still current;
- completed externally;
- partial/ambiguous;
- completed under authority that has since changed.

The last class is a Deadwalker candidate and must enter quarantine before any effect is consumed.

## Mutation checkpoints

Prefer durable states such as:

- `SLICE_ACTIVATED`
- `MUTATION_PREPARED`
- `MUTATION_OBSERVED`
- `VALIDATION_CLASSIFIED`
- `AUTHORITY_REVALIDATED`
- `QUARANTINED` when freshness fails
- `MERGED_SEALED` or equivalent terminal state

## Failure handling

Classify meaningful failures before retry/replan. Infrastructure, permission, governance, implementation, convergence, hypothesis and evidence-gap failures are not interchangeable.

A fixed number of engineering failures is not by itself a valid stop condition.

## Effect-side authority freshness

Immediately before merge/adoption, provider/network effect, mutation, deploy/release, operator stop/escalation, budget reservation or replay of a prepared effect:

1. independently resolve current authority;
2. compare it with the authority anchor used to prepare the action;
3. if the anchor changed, quarantine the old evidence/effect;
4. re-evaluate against current authority before proceeding.

See `../controls/deadwalker_quarantine_protocol.md`.

## Safe stop

Stop for a genuine scope/authority/budget/safety/irreversibility boundary, contradictory evidence that cannot be resolved inside current authority, exhausted viable hypotheses, or an explicit operator decision gate.

Do not stop merely because a chat ended, a stale projection says stop, or an arbitrary attempt count expired.
