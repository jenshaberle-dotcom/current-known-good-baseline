# Control: Temporal Authority Drift / Deadwalker Detection

Control ID: CKGB-CTRL-TEMPORAL-AUTHORITY-DRIFT-001
Status: current known good baseline
Codename: Deadwalker Detector
Origin: obsolete but historically real engineering rules re-entered current reasoning and authority after supersession

## Purpose

Detect, classify, measure, and contain rules, assumptions, permissions, requirements, or decisions that were once valid but have since been superseded, revoked, or made historical and later reappear as if they were current authority.

This is a temporal-authority control, not a generic hallucination detector.

## Core model

An authority-bearing statement has a lifecycle. A minimal lifecycle is:

- `ACTIVE` — currently authoritative inside its declared scope;
- `SUPERSEDED` — replaced by a newer authority;
- `REVOKED` — explicitly no longer authorized;
- `HISTORICAL` — retained as evidence or context but not current authority.

A historical mention of an obsolete rule is not a failure. The failure occurs when obsolete semantics regain current reasoning or behavioral authority.

## Deadwalker event

A **Deadwalker Event** occurs when all of the following are true:

1. an authority-bearing rule, requirement, assumption, permission, or decision existed at time `T1`;
2. it was superseded, revoked, or made historical at time `T2`;
3. at a later time `T3 > T2`, the obsolete semantics are used as current authority;
4. the later use is not an explicitly historical comparison, migration test, compatibility fixture, or other bounded non-authoritative reference.

In short:

> Something that was once legitimately alive is dead as authority, but walks back into the current system.

## Parent drift class

**Temporal Authority Drift** is the broader class: current reasoning, documentation, automation, or behavior diverges from the valid time-bounded authority state.

Deadwalker resurrection is one high-value subtype. Other temporal-authority defects may include stale permissions, expired exceptions, superseded architecture decisions, revoked customer requirements, or historical defaults treated as current.

## Detection layers

Deadwalker detection should combine several evidence layers.

### 1. Deterministic identity checks

Prefer explicit identifiers and lifecycle metadata where available:

- rule or decision IDs;
- `status: SUPERSEDED` / `REVOKED` / `HISTORICAL` markers;
- `superseded_by` links;
- effective-from / effective-until timestamps;
- revoked authority records;
- references to known stale files, issues, prompts, or templates.

### 2. Lexical and structural signatures

Search for known obsolete phrases, aliases, copied blocks, stale references, and inherited templates.

Lexical matches produce candidates, not automatic behavioral findings.

### 3. Semantic equivalence checks

Detect paraphrases or functional restatements whose wording changed while the obsolete rule semantics remained.

Example: an obsolete `stop after three attempts` rule may reappear as `classified blocker exceeds three repair attempts` even though the exact original phrase is absent.

Semantic detection must preserve counterexamples. The number `3` alone is not evidence of a Deadwalker.

### 4. Behavioral trace checks

Where execution evidence exists, determine whether the obsolete rule actually affected:

- planning;
- eligibility;
- ranking;
- safe-stop decisions;
- mutation;
- operator escalation;
- CI behavior;
- deployment or other side effects.

Behavioral influence is stronger evidence than textual presence alone.

## Temporal Authority Ledger

Projects using this control should be able to represent at least the following fields for important evolving rules or decisions:

```yaml
authority_id: RULE-EXAMPLE-001
subject: example_rule
status: SUPERSEDED
introduced_at: <timestamp-or-commit>
superseded_at: <timestamp-or-commit>
superseded_by: RULE-EXAMPLE-002
scope: <where-this-authority-applied>
forbidden_as_current_authority: true
aliases:
  - <known historical wording>
source_evidence:
  - <commit/ADR/issue/contract>
```

The ledger may be explicit or derivable from structured project records. The invariant is that current authority and historical existence can be distinguished reproducibly.

## Severity model

| Level | Name | Meaning |
|---|---|---|
| D0 | Historical residue | Obsolete material is mentioned correctly as historical; no current-authority defect. |
| D1 | Resurrection candidate | Obsolete semantics appear in a current-looking surface but authority or effect is not yet established. |
| D2 | Reasoning contamination | Obsolete semantics influence planning, assessment, eligibility, or recommendation. |
| D3 | Behavioral escape | Obsolete semantics cause a stop, mutation, escalation, gate result, or other behavior. |
| D4 | Persistent resurrection | The same obsolete semantics reappear after prior detection or remediation. |

D0 is not a control failure. D1 requires classification. D2-D4 are confirmed Deadwalker defects.

## Metrics

A project may report the following metrics over a declared scan window and authority surface:

### Deadwalker Count

Number of confirmed D2-D4 Deadwalker events.

### Deadwalker Rate

`confirmed Deadwalker events / authority-bearing decisions or artifacts assessed`

Always report the denominator and scan scope.

### Time to Resurrection

Elapsed time from supersession or revocation (`T2`) to first confirmed post-supersession resurrection (`T3`).

### Detection Latency

Elapsed time from first confirmed resurrection to detection.

### Escape Rate

`D3-D4 behavioral escapes / confirmed D2-D4 Deadwalker events`

### Recurrence Rate

Fraction of remediated Deadwalker identities that later recur as D2-D4.

### Correction Cost

Project-specific effort or impact attributable to the event, such as wasted runs, operator interventions, reverted mutations, blocked slices, or elapsed repair time.

### Source Attribution

Distribution of confirmed events by the source that reintroduced obsolete authority, for example:

- stale current-status or re-entry artifact;
- historical documentation promoted accidentally;
- copied template or task;
- chat handover or model context;
- code or configuration;
- issue or PR text;
- generated artifact;
- unknown.

### Deadwalker Resistance

For a controlled evaluation set with known resurrection cases:

`cases detected before behavioral escape / all known resurrection cases`

This metric is most meaningful in seeded or retrospectively labeled evaluations where the denominator is known.

## Required distinctions

The detector must not confuse these cases:

- historical mention versus current-authority use;
- a legitimate bounded operational retry counter versus a retry count masquerading as engineering hypothesis governance;
- superseded wording whose semantics were intentionally retained versus semantics that were explicitly invalidated;
- stale projection versus authoritative live state;
- harmless duplicate text versus behavior-affecting resurrection.

## Control evidence

A credible implementation should retain:

- declared authority sources and precedence;
- supersession or revocation evidence;
- scan scope and timestamp/commit anchors;
- candidate matches and classification rationale;
- semantic counterexamples used to measure false positives;
- behavioral evidence for D2-D4 findings;
- remediation status;
- metric output with denominators.

## Minimum acceptance criteria

For an activated project:

1. at least one authoritative lifecycle source can distinguish current from superseded authority;
2. current authority-bearing surfaces are explicitly enumerated or reproducibly discovered;
3. known obsolete-rule fixtures are detected even when paraphrased;
4. legitimate counterexamples are not promoted to confirmed Deadwalkers without authority evidence;
5. D2-D4 findings include source, supersession evidence, current occurrence, severity, and remediation state;
6. scan results are reproducible from a pinned repository state;
7. unresolved D2-D4 findings are visible rather than silently ignored.

## Reference case: Zombie Retry Rule

The CKGB `Zombie Retry Rule` is the initial reference case for this control.

The relevant obsolete semantics are not the literal number three. The obsolete semantics are:

> A fixed count of failed engineering attempts is sufficient, by itself, to terminate or escalate work instead of classifying the failure, preserving evidence, and evaluating whether a viable materially different hypothesis remains.

A detector should therefore flag a current authority surface that reinstates those semantics after documented supersession, while not flagging legitimate bounded transient retries merely because their configured limit happens to be three.

See:

- `../anti-patterns/zombie_retry_rule.md`
- `../governance/reentry_and_failure_replan.md`
