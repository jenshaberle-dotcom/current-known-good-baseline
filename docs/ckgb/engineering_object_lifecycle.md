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

For every PR-based repository, merged source-branch retirement is the default baseline, not optional tidying.

Repository setup MUST enable the hosting platform's native delete-branch-on-merge capability when available. On GitHub this means `delete_branch_on_merge=true`. A project that intentionally cannot enable native deletion must record the reason and provide an equivalent identity-bound lifecycle mechanism.

A merged PR is not lifecycle-complete until its exact remote source branch is absent, unless the branch has an explicit current `PROTECTED` or `DEPENDENCY_BOUND` exception. Merge success alone is insufficient completion evidence.

Cleanup must be identity-bound to the exact PR head repository, branch and observed head identity. Delete only objects proven to belong to that merge. Broad name-pattern/prefix deletion is not acceptable authority. If the branch moved after the merged PR head, automatic deletion must stop and the branch must be reclassified rather than assuming the newer commits were merged.

The normal path is:

```text
PR MERGED
  -> NATIVE DELETE-BRANCH-ON-MERGE
  -> EXACT BRANCH ABSENT
  -> MERGE LIFECYCLE COMPLETE
```

The component that creates or manages local state owns its normal cleanup. Repository/delivery lifecycle owns remote branch retirement. DRJ may detect hygiene drift, but observation does not grant global janitor authority.

### Existing-repository bootstrap

Adopting this baseline in an existing repository requires a one-time full branch census; old branches are not grandfathered.

For each remote branch associated with a closed PR:

- merged PR + unchanged exact head -> retirement candidate;
- merged PR + branch head moved -> stop and classify; never delete the newer head on historical merge evidence;
- closed/unmerged PR -> preserve until explicitly classified as abandoned/superseded and safe to retire;
- protected/dependency-bound -> retain with explicit lifecycle reason;
- no identifiable owner/history -> quarantine for reconciliation rather than pattern deletion.

Bootstrap exit requires complete pagination, identity-bound retirement of eligible merged branches and absence proof. Thereafter native delete-on-merge prevents recurrence and lifecycle validation detects exceptions/drift.

Preferred model:

CREATE_TEMPORARY -> ATTACH_IDENTITY_AND_CLEANUP_CONTRACT -> USE -> COMPLETE -> CLEANUP -> PROVE_ABSENCE

The anti-pattern is indefinite creation followed by a periodic global cleanup process that has to guess what is safe to delete.

## Relationship to current controls

CKGB-ARCH-LIFECYCLE-001 remains CURRENT / SPECIALIZED for architecture decisions and maturity.
CKGB-CTRL-HARD-CUT-RULE-REPLACEMENT-001 remains CURRENT / SPECIALIZED for incompatible authority replacement.
CKGB-CTRL-DEADWALKER-QUARANTINE-001 remains CURRENT / SPECIALIZED for stale authority and evidence resurrection.
The EDCP baseline remains CURRENT / INTEGRATED for delivery and test lifecycle execution semantics.

This control is CURRENT / UMBRELLA for engineering-object creation, ownership, completion and retirement. It integrates rather than silently supersedes the specialized controls above.


## Unified artifact and product lifecycle

Branch hygiene is one specialization of the same engineering-object lifecycle. Projects must not
invent unrelated cleanup semantics for CI artifacts, packages, OCI images, releases and deployed
products.

### Artifact lifecycle

Every persistent build/test/release artifact should carry or be reconstructibly bound to:

- stable artifact identity and type;
- exact source revision;
- producer and lifecycle owner;
- creation time;
- retention class;
- qualification/promotion state;
- supersession relationship;
- cleanup condition and owner;
- protected references;
- absence evidence when retirement requires deletion.

Baseline states are `EPHEMERAL -> CANDIDATE -> QUALIFIED -> RELEASED -> SUPERSEDED -> RETIRED`,
with `PROTECTED` as an orthogonal retention condition rather than a promotion state.

No artifact may become release authority solely because it exists or because its source tests
passed. Qualification must bind the exact immutable artifact identity/digest to its exact source
and evidence.

### Product lifecycle

Product state is distinct from artifact state:

```text
SOURCE_CANDIDATE
  -> ARTIFACT_QUALIFIED
  -> RELEASE_CANDIDATE
  -> RELEASED
  -> DEPLOYED
  -> ACCEPTED
  -> SUPERSEDED
  -> RETIRED
```

`DEPLOYED != ACCEPTED`. Acceptance requires the project's explicit product E2E evidence against
the exact deployed artifact/runtime identity. A status-file edit cannot promote a product without
the transition evidence.

A replacement product may become current only after its required acceptance transition. The prior
accepted product becomes SUPERSEDED, not immediately disposable; rollback/retention policy decides
when it can retire.

### Retention classes

At minimum distinguish:

- `EPHEMERAL`: delete after the owning transition completes;
- `ROLLBACK`: retain the bounded accepted release set required for rollback;
- `EVIDENCE`: retain durable provenance according to evidence policy;
- `FAILURE_EVIDENCE`: retain until the failure/uncertainty is reconciled and retention permits retirement;
- `PRODUCT_CURRENT`: never generic-cleanup eligible;
- `USER_DATA`: governed by the product privacy/data-retention lifecycle, never generic engineering cleanup.

### Enforcement invariant

For authority-bearing engineering objects:

```text
UNKNOWN + AUTHORITY/EXECUTABLE = FAIL
SUPERSEDED + SELECTABLE_AS_CURRENT = FAIL
EXPIRED + ACTIVE = FAIL
RETIRED + PRESENT_WHERE_ABSENCE_REQUIRED = FAIL
PROMOTION_WITHOUT_TRANSITION_EVIDENCE = FAIL
```

CKGB defines these invariants. Each consuming repository defines its concrete artifact/product
types and transition evidence. EDCP/CI enforces the transition contract; RCC supplies execution
capacity/evidence transport and does not become product authority.
