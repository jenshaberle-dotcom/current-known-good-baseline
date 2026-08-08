from pathlib import Path


def test_expanded_ckgb_documents_exist() -> None:
    required = [
        "docs/ckgb/baseline_catalog.md",
        "docs/registers/risk_register_template.md",
        "docs/controls/control_catalog_template.md",
        "docs/customer-profiles/ckgb_as_don_customer.md",
        "docs/score-impact/t_score_impact_hypothesis.md",
        "docs/lessons-learned/glossary.md",
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
        "Lessons-learned glossary",
    ]
    for term in required_terms:
        assert term in text


def test_lessons_learned_glossary_contains_named_patterns() -> None:
    text = Path("docs/lessons-learned/glossary.md").read_text(encoding="utf-8")
    required_terms = [
        "Deadwalker",
        "Scope Hydra",
        "Priority Reflex",
        "Priority Bootstrap Paradox",
        "Cut one head, cauterize the boundary.",
    ]
    for term in required_terms:
        assert term in text
