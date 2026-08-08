# CKGB Lessons-Learned Glossary

Status: living vocabulary
Truth boundary: memorable names are retrieval aids; technical definitions and observed evidence carry authority

## Purpose

CKGB accumulates lessons from real project friction, failures, repairs, and validated improvements. Some recurring patterns acquire memorable names because they make a failure mode or control easier to recognize across projects.

This glossary keeps those names from becoming folklore detached from their technical meaning.

Each entry therefore records:

- the memorable name;
- the precise technical meaning;
- what the term does **not** mean;
- its evidence/status inside CKGB;
- related controls or anti-patterns where available.

A memorable term must never create governance authority by itself.

## Quick index

| Term | Technical meaning | CKGB status |
|---|---|---|
| **Deadwalker** | Temporal authority resurrection: historically valid but retired authority regains current reasoning or behavioral influence | Established, evidence-backed anti-pattern/control vocabulary |
| **Scope Hydra** | Uncontrolled scope multiplication inside an active bounded slice | Established, evidence-backed anti-pattern |
| **Priority Reflex** | Evidence-triggered investment-view freshness check that recommends reassessment after material accepted evidence | Emerging, evidence-backed capability concept; not yet a CKGB baseline control |
| **Priority Bootstrap Paradox** | The first need for a reassessment-trigger capability must be noticed through the older process because the capability does not yet exist to trigger its own prioritization | Observed bootstrap phenomenon; not a control or bypass authority |

## Deadwalker

**Technical name:** temporal authority resurrection / Temporal Authority Drift

A Deadwalker is a rule, permission, decision, status projection, assumption, or other authority-bearing state that was once legitimately current, was later superseded, revoked, or retired, and then re-enters present reasoning or behavior as if it were current again.

The dangerous property is not age. The dangerous property is **regained authority**.

A stale document is therefore not automatically a Deadwalker. It becomes a Deadwalker when stale or retired semantics influence a current decision, validation result, configuration, execution path, or other authority-bearing behavior.

### Origin evidence

DON/MCP repeatedly resurfaced an obsolete fixed-count engineering stop rule. Later self-application of the Deadwalker capability found a stronger behavioral case in DON's own re-entry handling: stale projection state could regain prepared-effect execution influence before freshness/coherence checks. The defect was then repaired and regression-tested.

This moved the concept beyond a naming convention: it demonstrated real fault-discovery and governance value on the system that created the detector.

### Related CKGB material

- [Zombie Retry Rule — The Deadwalker](../anti-patterns/zombie_retry_rule.md)
- [Temporal Authority Drift / Deadwalker Detection](../controls/temporal_authority_drift_control.md)

### Core distinction

> Historical presence is not the defect. Historical authority walking back into the present is.

## Scope Hydra

**Technical name:** uncontrolled scope multiplication during an active bounded slice

A Scope Hydra appears when one bounded task silently grows new heads: adjacent features, refactors, migrations, cleanup, integrations, or architecture work are pulled into the active execution unit merely because they were discovered nearby.

The newly discovered work may be useful. The failure is allowing discovery to silently redefine the activated scope.

### Required response

Capture the new head separately unless it is strictly required for the already-activated outcome. If new evidence invalidates the old boundary, perform an explicit replan rather than silently expanding it.

### Related CKGB material

- [Scope Hydra anti-pattern](../anti-patterns/scope_hydra.md)

### Canonical phrase

> **Cut one head, cauterize the boundary.**

## Priority Reflex

**Technical name:** evidence-triggered investment reassessment signal

Priority Reflex is the capability concept that material newly accepted evidence should cause the current investment/prioritization view to be checked for freshness and, when warranted, emit an explicit reassessment recommendation.

The narrow intended transition is:

`material accepted evidence -> investment-view freshness check -> REASSESSMENT_RECOMMENDED`

It is deliberately **not**:

`new evidence -> automatic rerank -> activate winner`

Priority Reflex should make evidence-responsive prioritization harder to forget without becoming a parallel ranking engine, scheduler, or execution authority.

### Origin evidence

In DON/MCP, the Deadwalker capability moved from synthetic/internal validation to real self-application evidence after it found and helped drive repair of a genuine behavioral resurrection. That materially changed its product and governance value. The need to revisit investment priority was recognized by the supervisor/operator process rather than by a first-class evidence-to-reassessment mechanism.

The observed gap is therefore evidence-backed, but the capability is still being governed normally: discovery and strong evidence do not equal implementation priority or activation authority.

### CKGB status

**Emerging lesson / capability concept.** Evidence-backed, but not yet a selected CKGB baseline control. Before promotion it needs a stable definition of material evidence, trigger freshness, debounce/diminishing-return behavior, negative controls, and an explicit governance boundary.

### Core rule

> New evidence may invalidate an old priority without authorizing the new one.

## Priority Bootstrap Paradox

**Technical name:** bootstrap dependency in evidence-responsive prioritization

The Priority Bootstrap Paradox describes the first introduction of Priority Reflex:

The capability that would automatically recognize when material evidence should trigger prioritization reassessment does not yet exist. Therefore its own first need must be noticed by the pre-existing human/governance process and submitted through that same governed backlog and investment pipeline.

That bootstrap event is not a defect and must not be treated as an exception.

The paradox is resolved by using the old process exactly once to introduce the capability that can later reduce reliance on that old manual recognition step.

### Anti-bypass rule

The bootstrap observation may provide **evidence for grooming and reassessment**, but it may not grant itself rank, implementation readiness, or execution authority.

### Core rule

> The mechanism that detects stale priorities cannot retroactively have detected the evidence that justified building the mechanism.

## Vocabulary admission rule

A new memorable term belongs here when all of the following are true:

1. it describes a reusable engineering, governance, product, or operational pattern rather than a one-off joke;
2. there is concrete project evidence or repeated observed friction behind it;
3. a precise technical definition can distinguish positive cases from false positives;
4. its status is explicit: established control, anti-pattern, emerging concept, or descriptive phenomenon;
5. the metaphor does not silently become authority.

Good names improve retrieval and shared understanding. The evidence and technical definition remain the specification.
