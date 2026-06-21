from pathlib import Path


def test_core_documents_exist() -> None:
    required = [
        "README.md",
        "docs/ckgb/principles.md",
        "docs/project-start/project_selection_record_template.md",
        "docs/lessons-learned/lesson_record_template.md",
        "docs/governance/framework_language.md",
        "docs/tooling/tooling_baseline.md",
        "docs/security/security_baseline.md",
        "docs/ai-governance/ai_governance_baseline.md",
    ]

    for path in required:
        assert Path(path).exists(), path


def test_ckgb_does_not_claim_best_practice() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "not a best-practice claim" in text.lower()
    assert "current known good baseline" in text.lower()
