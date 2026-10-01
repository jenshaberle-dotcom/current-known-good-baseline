from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
DEMAND = ROOT / ".rcc" / "workload-demands.json"

FORBIDDEN_PATHS = (
    ROOT / ".rcc" / "runner-contract.json",
    ROOT / ".rcc" / "runner-profiles",
    WORKFLOWS / "warm-runner-heartbeat.yml",
    WORKFLOWS / "warm-runner-route.yml",
    WORKFLOWS / "rcc-warm-profile-contract.yml",
)

FORBIDDEN_TOKENS = (
    "WARM_PREFERRED_GITHUB_HOSTED",
    "cngb-linux",
    "cngb-linux-warm",
    "warm-runner-heartbeat.yml",
    "warm-runner-route.yml",
    ".rcc/runner-contract.json",
    ".rcc/runner-profiles",
    "hosted_runs_on_json",
    "ubuntu-latest",
    "windows-latest",
)

CURRENT_AUTHORITY = (
    ROOT / "PROJECT-REENTRY.json",
    ROOT / "README.md",
    ROOT / "docs" / "tooling" / "runner-installation-and-path-baseline.md",
)


def main() -> None:
    for path in FORBIDDEN_PATHS:
        assert not path.exists(), f"retired runner authority returned: {path}"

    demand = json.loads(DEMAND.read_text(encoding="utf-8"))
    assert demand["schema_version"] == "cngb.rcc_workload_demands.v2"
    authority = demand["authority"]
    assert authority["allocation"] == "RCC_AUTO_ONLY"
    assert authority["reservation"] == "RCC_ATOMIC"
    assert authority["physical_selection"] == "RCC_ONLY"
    assert authority["facade_selection"] == "RCC_ONLY"
    assert authority["github_hosted_fallback"] is False
    assert authority["broad_project_routing"] is False
    assert authority["consumer_runner_lifecycle"] is False
    assert authority["consumer_runner_profile_ownership"] is False

    for path in CURRENT_AUTHORITY:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_TOKENS:
            assert token not in text, f"{path}: retired runner token returned: {token}"

    workflows = {path.name for path in WORKFLOWS.glob("*.yml")}
    assert workflows == {"rcc-assignment-proof.yml", "rcc-demand-validation.yml"}

    declared = set(demand["workflow_demands"])
    assert declared == workflows

    print("CNGB_GENERAL_POOL_HARDCUT=PASS")


if __name__ == "__main__":
    main()
