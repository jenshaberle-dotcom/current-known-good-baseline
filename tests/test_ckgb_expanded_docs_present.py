from pathlib import Path


def test_expanded_ckgb_documents_exist() -> None:
    required = [
        "docs/ckgb/baseline_catalog.md",
        "docs/registers/risk_register_template.md",
        "docs/controls/control_catalog_template.md",
        "docs/customer-profiles/ckgb_as_don_customer.md",
        "docs/score-impact/t_score_impact_hypothesis.md",
        "docs/controls/deadwalker_quarantine_protocol.md",
        "docs/governance/reentry_and_failure_replan.md",
        "docs/controls/hard-cut-rule-replacement.md",
        "docs/knowledge/research/2026-09-28-truth-topology-and-migration-drift.md",
    ]
    for path in required:
        assert Path(path).exists(), path


def test_baseline_catalog_contains_key_lessons() -> None:
    text = Path("docs/ckgb/baseline_catalog.md").read_text(encoding="utf-8")
    required_terms = [
        "Repo is truth",
        "Ruff before first feature code",
        "No self-certification",
        "DVI",
        "NIST AI RMF mapping",
        "ISO/IEC 42001 mapping",
        "Provider/API budget guard",
        "Deadwalker quarantine / authority freshness",
        "Session-independent re-entry",
        "Evidence-driven failure classification",
    ]
    for term in required_terms:
        assert term in text


def test_deadwalker_quarantine_contains_effect_side_freshness() -> None:
    text = Path("docs/controls/deadwalker_quarantine_protocol.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "prepared-effect authority TOCTOU",
        "QUARANTINED",
        "effect side",
        "operator escalation",
        "D3",
        "DON/MCP",
    ]
    for term in required_terms:
        assert term in text


def test_hard_cut_rule_replacement_has_truth_topology_contract() -> None:
    text = Path("docs/controls/hard-cut-rule-replacement.md").read_text(
        encoding="utf-8"
    )
    required_terms = [
        "Replace = Introduce + Destroy + Prove Absence",
        "CURRENT",
        "TRANSITION",
        "HISTORICAL",
        "Two implementations may coexist. Two independent current truths may not.",
        "Negative architecture tests",
        "Deep scans are recovery tools, not the steady-state control",
        "agent entrypoint -> architecture/index",
    ]
    for term in required_terms:
        assert term in text
