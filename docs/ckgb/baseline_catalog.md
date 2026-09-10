# CKGB Baseline Catalog

Status: expanded baseline with 2026-09 active-portfolio harvest
Scope: project-start selection, lessons learned, governance baseline
Truth boundary: current known good, not best practice

## Purpose

This catalog captures what we wish had been known before starting and operating the active project portfolio, including DON, JAP, RCC, WBAA, PED, DRJ and NOVI-family projects.

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
| Session-independent re-entry | Recommended | Interrupted sessions and delayed external work make blind replay unsafe | Multi-session, agent-assisted, autonomous or interruption-prone work | Tiny human-only toy work |
| Re-Entry is projection, not authority | Foundation | Re-Entry can become stale or accidentally redefine canonical contracts | Multi-session/agent-assisted work | Tiny single-session toy work |
| E2E outcome lock | Recommended | Real product tasks repeatedly expanded into architecture/migration programmes | Product delivery with automation, shared infrastructure or agents | Pure architecture research with no active delivery outcome |
| Evidence-driven failure classification | Foundation | Fixed attempt counts caused premature stops while unchanged retries created disguised loops | Automation, AI-assisted engineering or iterative repair | Static documentation only |
| No-progress retry rejection | Recommended | Blind retries repeated identical failures and consumed operator/provider budget | CI, automation, LLM/provider loops, lifecycle operations | Single deterministic one-shot operation |
| Search-surface readiness classification | Recommended | WBAA observed repository access while 8/10 active repos lacked connected code-search readiness | Agentic engineering, large/unfamiliar repositories, exhaustive repo-wide claims | Small repo where exact known paths are sufficient |
| Deadwalker quarantine / authority freshness | Recommended | Historically valid authority can be superseded while a run/effect is still in flight and later regain current influence | Long-lived, evolving-authority, agent-assisted or CI-driven systems | Short-lived work with no changing authority or delayed effects |
| Ruff before first feature code | Foundation | Retrofitted linting is expensive | Python project | Non-Python project with equivalent lint |
| Pytest baseline | Foundation | Validation must be executable | Python project | Non-Python project with equivalent tests |
| Secret scanning | Foundation | Secret leakage is high-impact and cheap to detect | Repo with config, keys or external calls | No secrets possible and private toy repo |
| Dependency scanning | Foundation | Dependency risk should be visible early | Project with dependencies | No external dependencies |
| Explicit ownership | Foundation | Agents, gates and connectors need bounded responsibility | Multi-component system | Single-file toy script |
| Fail closed | Foundation | Unsafe state must stop, not continue | Automation, data, AI, external calls | Pure read-only docs |
| Structured operational state | Foundation | CSV/export/file handoffs must not become hidden truth | Systems with runtime state | Static docs only |
| Separate source and runtime/effect authority | Foundation | Clean source state does not authorize host, release, runner, retention or provider effects | Any project with CI, local runtime or external effects | Static/read-only repository |
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
| Preserve conflicting truth domains | Recommended | RCC produced false certainty when local host activity and GitHub BUSY telemetry were collapsed | Systems combining scheduler, host, runtime or external telemetry | Single authoritative state source |
| No self-certification | Advanced / Conditional | LLMs may analyze but not certify their own success | AI/agent systems | No AI recommendations |
| DVI | Advanced / Conditional | Decision value and integrity need measurement | AI-assisted governance/control-plane | No AI/governance decisions |
| TRUST ledger | Advanced / Conditional | Recommendation review must be auditable over time | Recommendation systems | No recommendations |
| NIST AI RMF mapping | Advanced / Conditional | Shared AI governance language helps explain controls | AI governance/client-facing project | No AI relevance |
| ISO/IEC 42001 mapping | Advanced / Conditional | AI management system language supports maturity explanation | AI governance project | No AI relevance |
| Provider/API budget guard | Advanced / Conditional | Real provider calls cost money and need admission control | LLM/API usage | No external provider calls |
| Lessons-learned loop | Recommended | CKGB must improve from real work | Repeated project family | One-off experiment |
| Architecture promotion lifecycle | Recommended | Attractive platform ideas repeatedly expanded active delivery scope before real consumer proof | Shared infrastructure, reusable control planes, cross-project architecture | Single-project implementation with no reuse intent |
| Shared-infrastructure migration contract | Advanced / Conditional | Warmrunner and Janitor migrations showed that safe replacement needs bounded consumer proof before portfolio cutover | Replacing shared infrastructure, runners, control planes, storage/runtime ownership | Additive feature with no legacy replacement or cross-project adoption |
| Release-management core + profiles | Recommended | RCC, PED and JAP showed that source/version/release/install truth can diverge and operator installability may be a distinct gate | Versioned products, local apps, control planes or externally consumed artifacts | Throwaway/internal code with no release lifecycle |
| Immutable GitHub Release delivery | Recommended for distributable products | RCC/JAP proved exact source/tag/version plus immutable assets and checksum make application delivery auditable and updateable without source rebuild | Versioned downloadable application/artifact hosted in GitHub | No distributable release artifact |
| Explicit release-intent orchestration | Candidate / pilot only | PED exposed the need to request a release explicitly without making every product merge release-bearing or manually editing version identity | Versioned products where operators want deliberate patch/minor/major release intent separated from ordinary development and from publication | No release lifecycle, or projects that intentionally release every qualifying merge and need no separate operator intent |
| Privileged release publisher boundary | Advanced / Conditional | RCC needed local signing authority without giving CI the publisher private-key boundary | Signed/privileged local apps or control planes | No privileged signing/host authority |
| Consumer update without source rebuild | Recommended for local apps | Routine source clone/build/sign on consumer hosts makes update identity and dependencies drift | Released local applications with updater/install path | Development-only tooling where source build is the product |
| NOVI-family game project baseline | Foundation for NOVI-family games | DOI/COTD exposed CI queue fan-out, signing/path drift and repeated cold-start provisioning on persistent runners | Every new NOVI-family game repository | Non-game projects or games intentionally outside the NOVI family |
| Persistent self-hosted toolchain lifecycle | Recommended for persistent runners; Foundation for NOVI-family games | Rebuilding unchanged verified dependencies on every job wasted runner capacity and caused timeout/queue pressure | Persistent self-hosted CI with expensive stable dependencies | Disposable hosted runners or deliberately explicit clean-room validation |
| Explicit runner-root contract | Recommended for self-hosted runners | Runner migration/discovery became fragile when roots were inferred from host layout | Persistent self-hosted runners, WSL/Windows cross-OS execution | Hosted-only disposable CI |
| Separate runner root and managed toolchain root | Recommended for persistent runners | Runner registration lifecycle and stable dependency provisioning have different ownership/replacement semantics | Warm/persistent runners with cached/provisioned toolchains | Disposable hosted runners |
| Application installer vs runner provisioner separation | Recommended when both exist | JAP/RCC expose app installers while RCC separately owns runner lifecycle/profile provisioning | Local app plus self-hosted runner/control-plane environment | Project has only one of these surfaces |
| Warm preferred + explicit hosted fallback | Advanced / Conditional | Warm runners can sleep/offline; portable work should not queue indefinitely when a safe hosted surface exists | Portable CI with persistent self-hosted acceleration | Workload requires local-only hardware/effects/state |
| Scarce-platform authority | Recommended | Platform-independent twin jobs consumed scarce native runners without adding distinct evidence | CI with one or more capacity-constrained platform runners | Fully disposable symmetric hosted CI where duplication cost is negligible |
| Non-selection record | Recommended | Skipped controls need reason and review trigger | Projects using CKGB | Tiny throwaway work |

## Harvested profile documents

- `docs/lessons-learned/active-portfolio-harvest-2026-09.md` — cross-project evidence and lessons.
- `docs/tooling/github-release-delivery-baseline.md` — exact-source GitHub Release, `gh` publication, immutable assets, update and rollback profile.
- `docs/tooling/explicit-release-intent-orchestration.md` — candidate control for explicit release request, exact-source locking, deterministic semantic version preparation and delegation to one canonical publisher.
- `docs/tooling/runner-installation-and-path-baseline.md` — application install roots vs runner roots vs managed toolchain roots, runner provisioning and fallback.

See `architecture_lifecycle.md` for maturity, migration, adoption and release-profile semantics.
