from pathlib import Path


def test_expanded_ckgb_documents_exist() -> None:
    required = [
        "docs/ckgb/baseline_catalog.md",
        "docs/registers/risk_register_template.md",
        "docs/controls/control_catalog_template.md",
        "docs/customer-profiles/ckgb_as_don_customer.md",
        "docs/score-impact/t_score_impact_hypothesis.md",
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
    ]
    for term in required_terms:
        assert term in text
