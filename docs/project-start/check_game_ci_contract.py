#!/usr/bin/env python3
"""Fail closed when NOVI-family game CI drifts from the shared queue/toolchain contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CONTRACT_VERSION = "1.1.0"
EXPECTED_GROUP = "group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref_name }}"
VALID_CLASSES = {
    "development-validation",
    "alpha-handoff",
    "infrastructure-smoke",
    "clean-room-validation",
    "post-merge",
}
MUTABLE_ACTION_REF = re.compile(
    r"(?m)^\s*uses:\s+[^\s@]+@(?:v\d+(?:\.\d+)*|main|master|latest)\s*$"
)
PUBLIC_DESKTOP_WRITE = re.compile(
    r"(?i)(?:\$env:PUBLIC|C:\\Users\\Public)[^\r\n]{0,100}Desktop"
)
WINDOWS_SELF_HOSTED = re.compile(
    r"(?im)^\s*runs-on:\s*.*(?:project-novi-windows|cotd-windows|self-hosted[^\r\n]*windows|windows[^\r\n]*self-hosted)"
)
WINDOWS_COLD_START = re.compile(
    r"(?is)(?:Godot_v[^\r\n]*win64|export_templates\.tpz).{0,1200}(?:Invoke-WebRequest|curl\.exe)|(?:Invoke-WebRequest|curl\.exe).{0,1200}(?:Godot_v[^\r\n]*win64|export_templates\.tpz)"
)
TIMEOUT = re.compile(r"(?m)^\s*timeout-minutes:\s*(\d+)\s*$")


def has_top_level_trigger(text: str, name: str) -> bool:
    return re.search(rf"(?m)^  {re.escape(name)}:\s*$", text) is not None


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.as_posix()}: {message}")


def validate_workflow(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    class_match = re.search(r"(?m)^# novi-ci-class:\s*([a-z-]+)\s*$", text)
    if not class_match:
        fail(errors, path, "missing '# novi-ci-class: <class>' declaration")
        return

    workflow_class = class_match.group(1)
    if workflow_class not in VALID_CLASSES:
        fail(errors, path, f"unknown workflow class '{workflow_class}'")
        return

    pull_request = has_top_level_trigger(text, "pull_request")
    push = has_top_level_trigger(text, "push")
    dispatch = has_top_level_trigger(text, "workflow_dispatch")

    if workflow_class in {"development-validation", "alpha-handoff"}:
        if not pull_request or not dispatch:
            fail(errors, path, f"{workflow_class} requires pull_request + workflow_dispatch")
        if push:
            fail(errors, path, f"{workflow_class} must not run on feature-branch push")
    elif workflow_class in {"infrastructure-smoke", "clean-room-validation"}:
        if not dispatch:
            fail(errors, path, f"{workflow_class} requires workflow_dispatch")
        if pull_request or push:
            fail(errors, path, f"{workflow_class} must be manual-only")
    elif workflow_class == "post-merge":
        if not push or not dispatch:
            fail(errors, path, "post-merge requires explicit push + workflow_dispatch")
        if '"**"' in text or "'**'" in text:
            fail(errors, path, "post-merge push branches must be explicit; '**' is forbidden")

    if "concurrency:" not in text:
        fail(errors, path, "missing concurrency block")
    if EXPECTED_GROUP not in text:
        fail(errors, path, f"concurrency group must be exactly '{EXPECTED_GROUP}'")
    if re.search(r"(?m)^\s*cancel-in-progress:\s*true\s*$", text) is None:
        fail(errors, path, "cancel-in-progress: true is required")

    if MUTABLE_ACTION_REF.findall(text):
        fail(errors, path, "GitHub Actions must be pinned to immutable commit SHAs, not mutable major/main/latest refs")

    if PUBLIC_DESKTOP_WRITE.search(text):
        fail(errors, path, "service-runner workflows must not write to the Public Desktop")

    uses_windows = WINDOWS_SELF_HOSTED.search(text) is not None
    if uses_windows and workflow_class == "development-validation":
        fail(errors, path, "platform-independent/development validation must not consume the scarce Windows runner; move native Windows behavior into alpha-handoff")
    if uses_windows and workflow_class == "alpha-handoff":
        if "Ensure-NoviRunnerToolchain.ps1" not in text:
            fail(errors, path, "self-hosted Windows authority must call Ensure-NoviRunnerToolchain.ps1")
        if WINDOWS_COLD_START.search(text):
            fail(errors, path, "normal self-hosted Windows authority must not cold-download Godot/toolchain assets")
        timeouts = [int(value) for value in TIMEOUT.findall(text)]
        if not timeouts or max(timeouts) < 30:
            fail(errors, path, "Windows product-authority workflow requires a >=30 minute job timeout budget")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    contract = root / "docs" / "governance" / "NOVI-GAME-CI-CONTRACT.json"
    windows_ensure = root / "tools" / "runner" / "Ensure-NoviRunnerToolchain.ps1"
    linux_ensure = root / "tools" / "runner" / "ensure_novi_runner_toolchain.sh"
    errors: list[str] = []

    for required in (contract, windows_ensure, linux_ensure):
        if not required.is_file():
            fail(errors, required, "required NOVI-family CI/toolchain file is missing")

    if contract.is_file():
        text = contract.read_text(encoding="utf-8")
        if f'"contract_version": "{CONTRACT_VERSION}"' not in text:
            fail(errors, contract, f"expected contract_version {CONTRACT_VERSION}")

    workflows = sorted((root / ".github" / "workflows").glob("*.y*ml"))
    if not workflows:
        print("FAIL: no GitHub Actions workflows found", file=sys.stderr)
        return 1

    for workflow in workflows:
        validate_workflow(workflow, errors)

    if errors:
        print("NOVI game CI contract violations:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: {len(workflows)} workflow(s) satisfy NOVI game CI contract v{CONTRACT_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
