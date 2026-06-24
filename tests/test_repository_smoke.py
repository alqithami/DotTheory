#!/usr/bin/env python3
"""Lightweight smoke checks for the Dot-Trace Theory repository.

These tests are intentionally dependency-free. They are suitable for local runs,
GitHub Actions, and pre-submission repository checks.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "Makefile",
        "CITATION.cff",
        "LICENSE.md",
        "paper/main.tex",
        "paper/references.bib",
        "scripts/dot_trace_minimal_simulator_v01.py",
        "scripts/dot_trace_predictive_simulator_v02.py",
        "scripts/dot_trace_trainable_validation_runner_v01.py",
        "scripts/run_experiment_01_prediction_lift.py",
        "configs/experiment_01_prediction_lift.json",
        "docs/experiments/experiment_01_prediction_lift.md",
        "docs/reproducibility_statement.md",
        "docs/code_availability_statement.md",
        "docs/repository_submission_checklist.md",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).exists()]
    assert not missing, "Missing required repository files: " + ", ".join(missing)


def test_experiment_runner_importable() -> None:
    path = REPO_ROOT / "scripts" / "run_experiment_01_prediction_lift.py"
    spec = importlib.util.spec_from_file_location("experiment_runner", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "main")


def test_no_obvious_placeholder_tokens_in_readme() -> None:
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    disallowed = ["<owner>", "<repository>", "TODO", "TBD"]
    found = [token for token in disallowed if token in text]
    assert not found, "README contains placeholder tokens: " + ", ".join(found)


if __name__ == "__main__":
    test_required_files_exist()
    test_experiment_runner_importable()
    test_no_obvious_placeholder_tokens_in_readme()
    print("Repository smoke tests passed.")
