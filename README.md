# Current Known Good Baseline

CKGB is a living project-start template based on lessons learned from DON/MCP, JAP, NOVI-family projects and the shared infrastructure portfolio.

It is not a timeless best-practice claim. It records the current known-good architecture supported by current evidence.

The template is intentionally over-complete. Project starts select the relevant product controls, but runner architecture is no longer project-specific.

## Current runner baseline

All normal repository CI and engineering workloads are consumers of the RCC General Pool.

- RCC owns the physical Linux/Windows runner fleet, cardinality, allocation, reservation, exact facade assignment, qualification and lifecycle.
- Consumer repositories declare workload platform/runtime/capabilities only through Demand-v2.
- Consumers do not own physical runner names, counts, profiles, heartbeat routing, hosted fallback or runner lifecycle.
- PowerShell 7 is an RCC fleet baseline capability where required.
- Non-baseline tools such as Kaggle CLI, Godot/export templates, alternate Python versions, Azure/Bicep, Docker and .NET variants are RCC-owned prepackaged/content-addressed capabilities materialized on demand.
- A specialist physical runner is allowed only after evidence proves the General Pool plus overlays cannot satisfy the workload.

For versioned desktop/local products, start the release/update decision with `docs/tooling/product-distribution-update-baseline.md`. Build/package/release qualification uses the same RCC General-Pool execution architecture; product installation/update remains a separate consumer-device concern.

For NOVI-family game repositories, start with `docs/project-start/NOVI-GAME-PROJECT-BASELINE.md`. Engine/toolchain differences are capability demand, not a reason to create project-specific physical runners.
