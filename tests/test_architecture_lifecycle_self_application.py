from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_architecture_lifecycle_classifies_existing_authority_controls() -> None:
    lifecycle = (ROOT / "docs/ckgb/architecture_lifecycle.md").read_text(encoding="utf-8")
    required = [
        "CKGB-CTRL-HARD-CUT-RULE-REPLACEMENT-001",
        "CKGB-CTRL-DEADWALKER-QUARANTINE-001",
        "CURRENT / SPECIALIZED",
        "CKGB self-application invariant",
        "SUPERSEDED",
        "FORBIDDEN",
        "HISTORICAL",
    ]
    for term in required:
        assert term in lifecycle, term


def test_hard_cut_is_specialized_not_parallel_lifecycle() -> None:
    text = (ROOT / "docs/controls/hard-cut-rule-replacement.md").read_text(encoding="utf-8")
    assert "CKGB-ARCH-LIFECYCLE-001" in text
    assert "CURRENT / SPECIALIZED" in text
    assert "not" in text.lower() and "universal architecture-evolution lifecycle" in text


def test_deadwalker_states_map_to_lifecycle() -> None:
    text = (ROOT / "docs/controls/deadwalker_quarantine_protocol.md").read_text(encoding="utf-8")
    for term in [
        "CKGB-ARCH-LIFECYCLE-001",
        "CURRENT / SPECIALIZED",
        "FORBIDDEN",
        "QUARANTINED",
        "not an architecture-decision authority state",
    ]:
        assert term in text, term
