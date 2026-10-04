# Current Known Good Baseline Research State

Status: knowledge decision-mode projection
Last reviewed: 2026-09-28
Portfolio contract: `Data-Retention-Janitor/docs/contracts/KNOWLEDGE-RESEARCH-LAYER-v1.md`
Project activity authority: `PROJECT-REENTRY.json` -> canonical CKGB Re-Entry

## Operating state

- mode: `execution`
- research_required: `false`
- research_reason: none
- current_research: none

This file owns Knowledge/Research decision state only. It does not declare whether CKGB is dormant, active, blocked or at safe stop; project activity and next-action truth are resolved through `PROJECT-REENTRY.json` and the canonical project Re-Entry on `main`.

## Accepted knowledge

- Outcome-oriented execution remains primary.
- Continue execution without a new research loop while work stays inside the already-decided solution space.
- Before a material directional change not covered by accepted project knowledge, perform focused internal + external research and choose `REUSE`, `ADOPT`, `EXTEND` or `BUILD`.
- For architecture/rule replacement, bound the active truth surface: one CURRENT authority per concern, explicitly bounded TRANSITION state, and HISTORICAL material that cannot act as current authority.
- Repeated deep scans are recovery/audit evidence, not the steady-state mechanism for repository coherence; prefer executable absence/resolution checks.

## Rejected approaches

- Mandatory research before every implementation step: rejected as unnecessary process overhead.
- Research only at kickoff: rejected because material direction changes can occur during an existing mission.
- Using Knowledge/Research state as project activity or work-admission authority: rejected because Re-Entry owns activity/continuation truth.

## Open knowledge gaps

None created by this projection. Add only gaps tied to a concrete outcome or directional decision.

## Research records

Create focused records under `docs/knowledge/research/YYYY-MM-DD-<topic>.md`. Preserve rejected alternatives and their reasons. Promote durable architectural decisions into the repository's existing decision/ADR mechanism where appropriate.

- `docs/knowledge/research/2026-09-28-truth-topology-and-migration-drift.md` — external research and CKGB synthesis for redundant truth, bounded migration duality, hard cuts, branch replacement, strangler migration and new-repository harvest decisions.
