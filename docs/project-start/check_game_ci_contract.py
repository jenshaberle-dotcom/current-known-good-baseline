#!/usr/bin/env python3
"""Fail closed when NOVI-family game CI drifts from the shared queue-hygiene contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXPECTED_GROUP = "group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref_name }}"
VALID_CLASSES = {
    "development-validation",
    "alpha-handoff",
    "infrastructure-smoke",
    "post-merge",
}
MUTABLE_ACTION_REF = re.compile(
    r"(?m)^\s*uses:\s+[^\s@]+@(?:v\d+(?:\.\d+)*|main|master|latest)\s*$"
)


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
    elif workflow_class == "infrastructure-smoke":
        if not dispatch:
            fail(errors, path, "infrastructure-smoke requires workflow_dispatch")
        if pull_request or push:
            fail(errors, path, "infrastructure-smoke must be manual-only")
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
        fail(errors, path, "GitHub Actions must be pinned to immutable commit SHAs")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    workflows = sorted((root / ".github" / "workflows").glob("*.y*ml"))
    if not workflows:
        print("FAIL: no GitHub Actions workflows found", file=sys.stderr)
        return 1

    errors: list[str] = []
    for workflow in workflows:
        validate_workflow(workflow, errors)

    if errors:
        print("NOVI game CI contract violations:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: {len(workflows)} workflow(s) satisfy NOVI game CI contract v1.0.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
