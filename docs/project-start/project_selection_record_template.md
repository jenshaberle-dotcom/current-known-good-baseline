# Project Selection Record Template

Project:

Date:

Project type:

AI involvement:

Autonomy level:

Data sensitivity:

External/user impact:

Regulatory relevance:

Expected lifetime:

Production/cloud likelihood:

Distribution audience: `none | single managed workstation | managed fleet | arbitrary consumers`

Persistent local/desktop product: `yes | no`

Release/update lifecycle expected: `yes | no`

Update compatibility line:

Signing requirement / signing authority:

Staging provider:

Bootstrap/update separation:

Consumer-only prerequisites (must not silently include CI runner, WSL, project checkout or developer credentials):

## Selected CKGB baseline

### Foundation

- [ ] Ruff / lint baseline
- [ ] Pytest validation baseline
- [ ] CI-compatible validation commands
- [ ] Secret scanning
- [ ] Dependency scanning
- [ ] Repository hygiene and branch rules

### Recommended

- [ ] Coverage diagnostic
- [ ] Static typing diagnostic
- [ ] Security lint diagnostic
- [ ] Governance vocabulary
- [ ] Decision/evidence records
- [ ] Lightweight risk register
- [ ] Lessons-learned loop
- [ ] Product distribution/update baseline for versioned desktop/local products
- [ ] Immutable release identity for distributable artifacts
- [ ] Consumer update without source rebuild
- [ ] Stage-before-consent update state machine
- [ ] Explicit bootstrap vs routine-update contract

### Advanced / Conditional

- [ ] NIST AI RMF mapping
- [ ] ISO/IEC 42001 mapping
- [ ] AI risk register
- [ ] Control catalog
- [ ] Human oversight model
- [ ] Authorization scope
- [ ] Side-effect boundary
- [ ] Provider/API budget guard
- [ ] Drift monitoring
- [ ] Platform-native code signing with centralized signing authority

## Product distribution decision

For a versioned desktop/local application expected to run beyond one developer workstation, select `CKGB-PRODUCT-UPDATE-001` unless a non-selection reason and review trigger are recorded.

Default target:

`hosted build/test/package -> central signing authority (when selected) -> immutable release -> consumer-local managed staging -> verification -> consent/policy -> isolated apply -> verify/rollback`

A self-hosted CI runner, WSL, project checkout or developer credential MUST NOT become an undocumented routine consumer-update prerequisite. A local runner may be selected temporarily as a managed-development staging provider only when the staged-state boundary is replaceable by a later product-local update agent.

## Not selected

| CKGB item | Reason | Review trigger |
|---|---|---|
| | | |
