#!/usr/bin/env python3
"""Lightweight citation-key consistency checker for LaTeX + BibTeX."""
from __future__ import annotations

import re
import sys
from pathlib import Path

CITE_RE = re.compile(r"\\(?:cite|citet|citep|citealp|citealt|citeauthor|citeyear)(?:\[[^\]]*\])*\{([^}]*)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def split_keys(raw: str) -> set[str]:
    return {part.strip() for part in raw.split(",") if part.strip()}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: check_citations.py paper/main.tex paper/references.bib")
        return 2
    tex_path = Path(sys.argv[1])
    bib_path = Path(sys.argv[2])
    tex = tex_path.read_text(encoding="utf-8", errors="ignore")
    bib = bib_path.read_text(encoding="utf-8", errors="ignore")

    cited: set[str] = set()
    for match in CITE_RE.finditer(tex):
        cited |= split_keys(match.group(1))
    bib_keys = set(BIB_RE.findall(bib))

    missing = sorted(cited - bib_keys)
    unused = sorted(bib_keys - cited)

    if missing:
        print("Missing bibliography keys:")
        for key in missing:
            print("-", key)
        return 1
    print(f"Citation check passed: {len(cited)} cited keys, {len(bib_keys)} bibliography keys.")
    if unused:
        print(f"Note: {len(unused)} unused bibliography keys are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
