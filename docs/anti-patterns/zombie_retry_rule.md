# Anti-Pattern: Zombie Retry Rule

Technical name: fixed-count retry anti-pattern
Deadwalker codename: The Deadwalker
Status: prohibited legacy pattern
Origin: repeated DON/MCP governance drift and cross-project reappearance of an obsolete fixed-attempt stop rule

## Metaphor

The rule is dead, but it keeps returning.

It does not eat brains. It creates dumb stops.

A Deadwalker is not an invented rule. It is more dangerous precisely because it was once legitimately alive: historically real authority that has been superseded but later walks back into current reasoning or behavior.

## Definition

A fixed retry count such as "stop after three failed attempts" must not be used as a substitute for failure classification, evidence assessment, or hypothesis management.

The number of previous failures is not, by itself, evidence that the current problem is exhausted or that another justified action is unsafe.

## Why it fails

A numeric retry counter treats fundamentally different events as equivalent, including:

- infrastructure or tooling failure;
- permission or environment blockage;
- newly exposed downstream defect;
- implementation defect;
- governance inconsistency;
- validation failure;
- missing evidence;
- genuinely falsified technical hypothesis.

This creates two opposite failure modes.

### Premature stop

Solvable work is abandoned because unrelated failures consumed an arbitrary retry budget.

### Disguised loop

Essentially identical actions are repeated until the counter expires even though no new information, changed hypothesis, or changed environment justifies the repetition.

## Required replacement

Use `docs/governance/reentry_and_failure_replan.md`.

After a meaningful failure:

1. persist the observed state and evidence;
2. classify the failure cause;
3. determine whether the current solution hypothesis was actually falsified;
4. do not replay an unchanged action without a material reason;
5. continue when new evidence, a changed environment, a materially different implementation, or a materially different hypothesis justifies further work;
6. safe-stop only when a genuine boundary or exhaustion condition is reached.

## Core rule

> Progress is bounded by evidence and viable hypotheses, not by an arbitrary attempt counter.

## Zombie containment

Removing the rule once is not sufficient.

Fixed retry-count rules must not be reintroduced through:

- copied governance text;
- inherited templates;
- stale re-entry records;
- generated task definitions;
- compatibility logic;
- chat handovers;
- historical examples treated as current authority.

If such a rule is discovered, classify it as **governance drift** and replace it with the current evidence-driven failure/replan policy.

When the obsolete rule was historically valid and later re-enters current authority, classify the event under the broader **Temporal Authority Drift** control as a Deadwalker candidate or confirmed Deadwalker according to evidence and behavioral effect.

See `../controls/temporal_authority_drift_control.md`.

## Detection smell

Typical phrases include:

- "after N attempts, stop";
- "retry budget" where the budget counts failures rather than materially distinct hypotheses;
- counters that decrement on infrastructure or permission failures;
- a safe-stop decision justified only by the number of prior executions.

A retry counter may still be valid for operational rate limiting, API protection, transient infrastructure retries, or other bounded mechanical safeguards. It must not masquerade as engineering reasoning or hypothesis governance.
