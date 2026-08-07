# CKGB Anti-Patterns

Status: living catalog
Truth boundary: observed failure modes, not universal best-practice claims

## Purpose

This catalog preserves failure patterns that repeatedly caused wasted work, hidden drift, false confidence, premature stops, or uncontrolled scope growth.

Each anti-pattern uses two names:

- a memorable metaphor that makes the failure mode easy to recognize;
- a precise technical name that defines what is actually prohibited.

Metaphors are mnemonic labels. Governance decisions must rely on the technical definition and observable evidence.

## Current anti-patterns

| Metaphor | Technical name | Core failure |
|---|---|---|
| [Zombie Retry Rule](zombie_retry_rule.md) | Fixed-count retry anti-pattern | An arbitrary attempt counter replaces failure classification, evidence assessment, and hypothesis management. |
| [Scope Hydra](scope_hydra.md) | Uncontrolled scope multiplication | One bounded task silently grows new features, architectural changes, or unrelated repair work inside the same active slice. |

## Catalog rule

An anti-pattern is added only when there is credible project evidence that the failure mode caused real friction, drift, wasted effort, misleading validation, or unsafe behavior.

When an anti-pattern is discovered in an active project:

1. classify the observed instance;
2. preserve enough evidence to understand why it occurred;
3. apply the documented replacement control;
4. remove stale governance text that could regenerate the pattern;
5. feed any genuinely new lesson back into CKGB.
