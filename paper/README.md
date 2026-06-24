# Paper Source

This directory is reserved for the manuscript source when the repository is used as a full paper-source archive.

At the current repository stage, the GitHub repository functions primarily as the code, experiment, documentation, and reproducibility companion for the Dot-Trace Theory manuscript. If the repository is to be cited as containing the full manuscript source, add the following files before archival release:

```text
paper/main.tex
paper/references.bib
```

Optional generated artifacts:

```text
paper/main.pdf
paper/dot_trace_theory_foundation_vX.Y.pdf
```

## Build command

After adding `paper/main.tex` and `paper/references.bib`, run:

```bash
make paper
```

The Makefile is intentionally guarded: if the manuscript source is not present, `make paper` reports this and exits rather than silently building a placeholder document.

## Manuscript-to-repository reference

If the paper source is not stored in this repository, cite this repository as a **code and reproducibility companion**, not as the canonical manuscript-source archive.

Suggested wording:

> The accompanying code and reproducibility repository is available at `https://github.com/alqithami/DotTheory`.

If the full manuscript source is added and archived with a DOI, use:

> The manuscript source, reference simulators, and reproducibility materials are archived at [DOI] and mirrored at `https://github.com/alqithami/DotTheory`.
