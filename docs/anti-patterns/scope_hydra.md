# Anti-Pattern: Scope Hydra

Technical name: uncontrolled scope multiplication during an active bounded slice
Status: prohibited unless explicitly re-scoped and re-authorized
Origin: repeated project growth where one repair or feature silently pulled adjacent features, architecture work, or unrelated cleanup into the same execution unit

## Metaphor

A bounded problem starts with one head.

While solving it, new heads appear: one adjacent feature, one architectural cleanup, one migration, one "while we are here" improvement, then several more.

> **Cut one head, cauterize the boundary.**

## Definition

A Scope Hydra exists when an active bounded task silently expands into materially new work without an explicit scope decision.

The new work may be individually sensible. The anti-pattern is allowing it to become part of the active slice merely because it was discovered nearby.

## Common heads

- adjacent features that are not required for the activated outcome;
- speculative refactors;
- architecture changes discovered during implementation;
- unrelated cleanup;
- queued future ideas pulled forward because they are convenient;
- new integrations or providers;
- broader data or schema work;
- new product behavior needed only by a future slice;
- technology migrations introduced without separate activation.

## Why it fails

Uncontrolled scope multiplication:

- destroys the original acceptance boundary;
- makes validation ambiguous;
- increases rollback cost and blast radius;
- hides which change produced which outcome;
- creates long-running branches and stale projections;
- turns useful discoveries into accidental commitments;
- makes re-entry harder because the active task no longer has one coherent meaning.

## Required response

When a new head appears:

1. decide whether it is strictly required to complete the currently activated outcome;
2. if not required, record it as a separate candidate, backlog item, issue, or future slice;
3. keep the current implementation inside its declared path, behavior, and authority boundaries;
4. if the new work truly invalidates the current scope, persist an explicit replan rather than silently expanding;
5. after the required repair, re-close the original boundary before continuing.

## Boundary test

Ask:

> If this newly discovered work had been known before slice activation, would it have changed the stated problem, acceptance criteria, allowed paths, risk, authority, or validation plan?

If yes, it is probably a new head and requires explicit treatment.

## Legitimate scope change

Scope change is not forbidden.

A project may deliberately re-scope when new evidence makes the old boundary invalid. The change must be explicit, persisted, and validated against authority and risk. Silent growth is the anti-pattern.

## Core rule

> Solve the activated problem. Capture adjacent discoveries. Do not let discovery silently redefine execution.

Or, in the shorter CKGB form:

> **Cut one head, cauterize the boundary.**
