# CKGB Engineering Object Lifecycle

Status: current-known-good candidate
Control ID: CKGB-ENG-LIFECYCLE-001

## Purpose

Apply lifecycle discipline beyond architecture decisions to tests, failure handling, workflows, artifacts, branches, worktrees, checkouts and generated engineering state.

CREATE -> OWN -> USE -> OBSERVE -> COMPLETE_OR_SUPERSEDE -> RETIRE -> PROVE_ABSENCE

Creation is incomplete without ownership and retirement semantics. Temporary objects should be ephemeral by design instead of relying on later global cleanup.

## Creation-time contract

Persistent or externally visible generated objects should define, where applicable: object type, stable identity or correlation ID, creator, lifecycle owner, authority scope, retention class, completion condition, supersession rule, cleanup trigger, cleanup owner, local cleanup, remote cleanup and absence evidence.

## Test management

Tests can become deadwalkers when they still execute successfully while proving a superseded property. Test evidence should distinguish CURRENT, DIAGNOSTIC, SUPERSEDED, FORBIDDEN and HISTORICAL. New suites must classify overlapping suites, status contexts, workflow triggers and merge requirements.

## Failure management

Failure handling progresses through detection, classification, bounded response, recovery evidence, closure and reusable prevention. Temporary retries, bypasses, quarantines, workarounds and special diagnostics require explicit retirement conditions.

## GitHub workflow lifecycle

Workflows are executable authority. Replacing one requires classification of its triggers, required checks or status contexts, callers, dispatch surfaces, documentation and consumer demand declarations. Simultaneously selectable old and new workflow authority is lifecycle drift.

## Artifact lifecycle

Build, test and release artifacts, caches, receipts and temporary evidence require creation-time retention semantics. Valuable provenance can be durable and immutable. Intermediate packages, duplicate logs and temporary test bundles should normally have bounded retention.

## Merge-completion hygiene

A merged PR is not operationally complete while temporary development state remains active without purpose. Where platform and safety constraints permit, merge completion should idempotently retire the merged remote source branch, managed local worktrees or checkouts, branch-bound claims and reservations, and ephemeral validation state.

Cleanup must be identity-bound. Delete only objects proven to belong to the merged PR, branch or correlation ID. Broad name-pattern deletion is not acceptable authority.

The component that creates or manages local state owns its normal cleanup. Repository or delivery lifecycle owns remote branch cleanup. DRJ may detect hygiene drift, but observation does not grant global janitor authority.

Preferred model:

CREATE_TEMPORARY -> ATTACH_IDENTITY_AND_CLEANUP_CONTRACT -> USE -> COMPLETE -> CLEANUP -> PROVE_ABSENCE

The anti-pattern is indefinite creation followed by a periodic global cleanup process that has to guess what is safe to delete.

## Relationship to current controls

CKGB-ARCH-LIFECYCLE-001 remains CURRENT / SPECIALIZED for architecture decisions and maturity.
CKGB-CTRL-HARD-CUT-RULE-REPLACEMENT-001 remains CURRENT / SPECIALIZED for incompatible authority replacement.
CKGB-CTRL-DEADWALKER-QUARANTINE-001 remains CURRENT / SPECIALIZED for stale authority and evidence resurrection.
The EDCP baseline remains CURRENT / INTEGRATED for delivery and test lifecycle execution semantics.

This control is CURRENT / UMBRELLA for engineering-object creation, ownership, completion and retirement. It integrates rather than silently supersedes the specialized controls above.
