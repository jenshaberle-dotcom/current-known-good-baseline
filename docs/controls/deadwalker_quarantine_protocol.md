# CKGB control: Deadwalker quarantine and authority freshness

Status: current-known-good candidate
Control ID: CKGB-CTRL-DEADWALKER-QUARANTINE-001
Technical class: temporal authority resurrection / prepared-effect authority TOCTOU

## Origin

The Deadwalker class originated in DON/MCP, not in CKGB. The initial repeated case was an obsolete fixed-count engineering stop rule returning through stale governance/context. Later DON self-application exposed the broader failure: stale projections and prepared effects can retain influence after the authority that justified them has changed.

DON issue #563 names the broader family `AUTHORITY-LINEAGE-INTEGRITY` and includes `PREPARED_EFFECT_AUTHORITY_TOCTOU`, stale active projections, generated-context contamination and effect-side current-authority proof.

CKGB's earlier Draft PR #2 documented detection semantics but never became canonical main and later diverged from main. That stale draft is quarantined historical evidence, not template authority.

## Core rule

A result may be technically valid for authority revision A and still be invalid as **current authority** after revision B supersedes A.

Before a governance-sensitive effect consumes prepared evidence, the effect side must independently re-observe current authority and compare an authority anchor/digest.

If identity, lifecycle, revision or digest changed:

`prepared result -> QUARANTINED -> fresh reconciliation or historical-only`

Never:

`prepared result -> stale success -> current effect`

## Authority lifecycle

Minimum states:

- `ACTIVE`
- `SUPERSEDED`
- `REVOKED`
- `HISTORICAL`
- `QUARANTINED`

Historical presence is not a defect. Regained current influence is.

## Quarantine blocks

Unreconciled superseded evidence must not authorize:

- merge or canonical adoption;
- provider/network execution;
- repository/runner mutation;
- deploy/release;
- operator escalation or stop recommendation;
- budget reservation;
- re-entry continuation;
- claims that an old qualification proves a current head;
- replay of a prepared effect.

## Quarantine record

Persist at least:

- source artifact/run/PR/checkpoint;
- prepared authority anchor;
- independently observed current authority anchor;
- supersession evidence;
- source attribution;
- severity;
- current influence/effect;
- forbidden effects;
- remediation state;
- release condition.

## Severity

- `D0` historical/current residue without authority defect;
- `D1` resurrection candidate detected before current influence;
- `D2` reasoning/planning contamination;
- `D3` behavioral escape into gate, stop, escalation, mutation or equivalent effect;
- `D4` recurrence after remediation.

## Release from quarantine

Release requires new authority-bearing evidence:

1. prove the original anchor is still current; or
2. freshly re-evaluate/qualify against current authority; or
3. mark old material `HISTORICAL` and derive a new candidate from current authority; or
4. obtain an explicit operator decision where operator authority is required, itself bound to current authority.

Rewording, retrying, rebasing or a new chat/session never clears quarantine by itself.

## Required re-entry behavior

Repository truth outranks chat. Re-entry must read unresolved D2-D4 quarantine state before selecting the next governance-sensitive action. A timeout or agent replacement reconciles first and closes only the unproved delta.

## Reference incident

RCC PR #69 / engineering run `32041020417` attempt 2 completed green after RCC main authority changed during the run. That stale success later influenced an operator-adoption recommendation. Classification: D3 Deadwalker, contained before canonical merge.
