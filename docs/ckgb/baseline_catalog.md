# CKGB Baseline Catalog

Status: initial expanded baseline
Scope: project-start selection, lessons learned, governance baseline
Truth boundary: current known good, not best practice

## Purpose

This catalog captures what we wish had been known before starting DON and the job-application-pipeline.

Each item is selectable. CKGB is intentionally over-complete.

## Activation levels

| Level | Meaning |
|---|---|
| Foundation | normally selected for serious projects |
| Recommended | useful by default, may be skipped with reason |
| Advanced / Conditional | selected based on risk, AI, autonomy, data, compliance or lifecycle |

## Baseline entries

| Item | Activation | Origin lesson | Selection criteria | Non-selection criteria |
|---|---|---|---|---|
| Repo is truth | Foundation | Chat and file handovers drifted; repository state must decide | Always | Never for serious project work |
| Ruff before first feature code | Foundation | Retrofitted linting is expensive | Python project | Non-Python project with equivalent lint |
| Pytest baseline | Foundation | Validation must be executable | Python project | Non-Python project with equivalent tests |
| Secret scanning | Foundation | Secret leakage is high-impact and cheap to detect | Repo with config, keys or external calls | No secrets possible and private toy repo |
| Dependency scanning | Foundation | Dependency risk should be visible early | Project with dependencies | No external dependencies |
| Explicit ownership | Foundation | Agents, gates and connectors need bounded responsibility | Multi-component system | Single-file toy script |
| Fail closed | Foundation | Unsafe state must stop, not continue | Automation, data, AI, external calls | Pure read-only docs |
| Structured operational state | Foundation | CSV/export/file handoffs must not become hidden truth | Systems with runtime state | Static docs only |
| Documentation as contract | Recommended | Docs can protect architecture and governance from drift | Long-lived project | Short prototype |
| ADRs | Recommended | Decisions need navigation and history | Architecture choices exist | Tiny project |
| Evidence chain | Recommended | Recommendations must be explainable and reviewable | AI, automation, governance | Static utility |
| Risk register light | Recommended | Findings and assumptions need risk context | Meaningful project | Toy project |
| Control catalog | Advanced / Conditional | Reusable controls need purpose and evidence | Governance-heavy project | Small app without controls |
| AI risk register | Advanced / Conditional | AI systems need risk and treatment records | AI decisions, users, money, safety, compliance | No AI component |
| Human oversight | Advanced / Conditional | Automation must not silently replace critical judgment | Agentic workflow | Pure read-only tooling |
| Authorization scope | Advanced / Conditional | Agent rights must be explicit | Agents, apply, commit, DB, provider calls | No automation rights |
| Side-effect boundary | Advanced / Conditional | External effects must be controlled | File/DB/network/provider mutation possible | Read-only docs |
| Read-only proof | Advanced / Conditional | Planning must prove it did not mutate target | Inspection/planning agent | Human-only repo work |
| Tool lifecycle | Recommended | Tools need clean/degraded/deprecated states | Multiple diagnostics or gates | One-off project |
| Diagnostic vs validation distinction | Recommended | Findings are not automatically failures | Diagnostic stack | Very small project |
| Coverage diagnostic | Recommended | Coverage blind spots are evidence gaps | Maintained code | Documentation-only repo |
| Static typing diagnostic | Recommended | Typing improves boundary confidence | Python library/control-plane | Simple scripts |
| Security lint diagnostic | Recommended | Security findings should be visible early | Automation/security code | Static docs |
| Drift taxonomy | Advanced / Conditional | Handover, scoring, governance and tool drift can damage systems | AI-assisted or long-lived projects | Stable static repo |
| No self-certification | Advanced / Conditional | LLMs may analyze but not certify their own success | AI/agent systems | No AI recommendations |
| DVI | Advanced / Conditional | Decision value and integrity need measurement | AI-assisted governance/control-plane | No AI/governance decisions |
| TRUST ledger | Advanced / Conditional | Recommendation review must be auditable over time | Recommendation systems | No recommendations |
| NIST AI RMF mapping | Advanced / Conditional | Shared AI governance language helps explain controls | AI governance/client-facing project | No AI relevance |
| ISO/IEC 42001 mapping | Advanced / Conditional | AI management system language supports maturity explanation | AI governance project | No AI relevance |
| Provider/API budget guard | Advanced / Conditional | Real provider calls cost money and need admission control | LLM/API usage | No external provider calls |
| Lessons-learned loop | Recommended | CKGB must improve from real work | Repeated project family | One-off experiment |
| Non-selection record | Recommended | Skipped controls need reason and review trigger | Projects using CKGB | Tiny throwaway work |
