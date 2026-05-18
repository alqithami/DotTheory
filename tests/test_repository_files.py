#!/usr/bin/env python3
"""Minimal repository integrity checks."""
from pathlib import Path

REQUIRED = [
    "README.md",
    "paper/main.tex",
    "paper/references.bib",
    "scripts/dot_trace_minimal_simulator_v01.py",
    "scripts/dot_trace_predictive_simulator_v02.py",
    "scripts/dot_trace_validation_runner_v01.py",
]


def test_required_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in REQUIRED if not (root / path).exists()]
    assert not missing, f"Missing required files: {missing}"


if __name__ == "__main__":
    test_required_files_exist()
    print("Repository file test passed.")
