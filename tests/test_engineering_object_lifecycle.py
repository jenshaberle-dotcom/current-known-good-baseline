from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def test_engineering_lifecycle_is_umbrella_without_silent_supersession() -> None:
    text = read("docs/ckgb/engineering_object_lifecycle.md")
    for term in (
        "CKGB-ENG-LIFECYCLE-001",
        "CURRENT / UMBRELLA",
        "CKGB-ARCH-LIFECYCLE-001",
        "CKGB-CTRL-HARD-CUT-RULE-REPLACEMENT-001",
        "CKGB-CTRL-DEADWALKER-QUARANTINE-001",
        "CURRENT / SPECIALIZED",
        "EDCP baseline remains CURRENT / INTEGRATED",
    ):
        assert term in text

def test_creation_and_retirement_are_one_contract() -> None:
    text = read("docs/ckgb/engineering_object_lifecycle.md")
    for term in (
        "Creation is incomplete without ownership and retirement semantics",
        "cleanup trigger",
        "cleanup owner",
        "local cleanup",
        "remote cleanup",
        "absence evidence",
        "merged remote source branch",
        "managed local worktrees or checkouts",
    ):
        assert term in text

def test_architecture_lifecycle_declares_specialization() -> None:
    text = read("docs/ckgb/architecture_lifecycle.md")
    assert "CKGB-ENG-LIFECYCLE-001" in text
    assert "CURRENT / SPECIALIZED" in text
    assert "lifecycle changes must themselves classify" in text

def test_catalog_exposes_engineering_lifecycle() -> None:
    text = read("docs/ckgb/baseline_catalog.md")
    assert "Engineering object lifecycle / creation-time hygiene" in text
    assert "Native merged-branch retirement" in text

def test_edcp_consumes_engineering_lifecycle() -> None:
    text = read("docs/ckgb/engineering_delivery_control_plane.md")
    for term in (
        "CKGB-ENG-LIFECYCLE-001",
        "Test plans, status contexts, temporary evidence",
        "superseded workflow",
        "RCC owns cleanup of RCC-created execution state",
        "DRJ may report lifecycle drift",
    ):
        assert term in text


def test_pr_repositories_default_to_native_branch_retirement() -> None:
    text = read("docs/ckgb/engineering_object_lifecycle.md")
    for term in (
        "merged source-branch retirement is the default baseline",
        "delete_branch_on_merge=true",
        "exact remote source branch is absent",
        "PROTECTED",
        "DEPENDENCY_BOUND",
        "branch head moved",
        "one-time full branch census",
        "old branches are not grandfathered",
        "complete pagination",
        "absence proof",
    ):
        assert term in text


def test_merge_success_alone_is_not_lifecycle_completion() -> None:
    text = read("docs/ckgb/engineering_object_lifecycle.md")
    assert "Merge success alone is insufficient completion evidence" in text
    assert "Broad name-pattern/prefix deletion is not acceptable authority" in text
