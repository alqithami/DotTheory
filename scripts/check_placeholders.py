#!/usr/bin/env python3
"""Scan selected files for development-stage placeholders."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"placeholder",
    r"to come",
    r"next step",
    r"minimum publishable",
    r"publication strategy",
    r"working paper",
    r"formal article",
    r"this version",
]


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        paths = [Path("paper/main.tex")]
    failures: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in PATTERNS:
            if re.search(pat, text, flags=re.IGNORECASE):
                failures.append(f"{path}: matched {pat!r}")
    if failures:
        print("Placeholder/draft-language scan failed:")
        for failure in failures:
            print("-", failure)
        return 1
    print("Placeholder/draft-language scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
