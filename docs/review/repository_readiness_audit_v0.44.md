# Repository Readiness Audit v0.44.0

Date: 2026-06-24

Repository: `https://github.com/alqithami/DotTheory`

## Summary

The repository is now prepared as a publication-facing **code and reproducibility companion** for the Dot-Trace Theory manuscript. It contains simulator prototypes, validation runners, a reproducible synthetic Experiment 1 workflow, documentation, repository checks, and GitHub Actions workflow files.

The repository can be cited in the paper as the location of code, synthetic experiment scaffolding, and reproducibility documentation.

## Current readiness status

| Area | Status | Notes |
|---|---|---|
| README | Ready | Describes theory, repository scope, commands, Experiment 1, and cautions |
| Simulator scripts | Ready | Minimal, predictive, validation, prediction-lift, and trainable-validation scripts are documented |
| Experiment 1 | Ready as synthetic scaffold | Runner, configuration, documentation, generated-output paths, ablations, and negative controls are defined |
| Makefile | Ready | Includes checks, smoke tests, and Experiment 1 targets |
| Tests | Ready | Lightweight repository smoke test added |
| GitHub Actions | Ready | Python checks and guarded LaTeX build workflow added |
| Citation metadata | Provisional | Repository URL corrected; author details must be confirmed |
| Code availability statement | Ready | Draft wording provided for manuscript use |
| Reproducibility statement | Ready | Environment, commands, and interpretation boundaries documented |
| License | Pending author decision | License remains intentionally pending |
| Manuscript source in repo | Optional / not currently included | `paper/README.md` documents how to add full manuscript source if this repository becomes the source archive |

## Commands to run before citing the repository

```bash
make check
make experiment-01-quick
```

If the full synthetic experiment is to be reported in the paper, also run:

```bash
make experiment-01
```

If `paper/main.tex` and `paper/references.bib` are added to the repository, run:

```bash
make paper
```

## Suggested manuscript repository statement

If the repository is cited as the code and reproducibility companion:

> Code, synthetic experiment scaffolding, reference simulators, and reproducibility documentation are available at `https://github.com/alqithami/DotTheory`.

If the manuscript source is later added and archived with a DOI:

> The manuscript source, code, reference simulators, and reproducibility documentation are archived at [DOI] and mirrored at `https://github.com/alqithami/DotTheory`.

## Remaining decisions before formal submission

1. Confirm author name, affiliation, email, and optional ORCID.
2. Update `AUTHORS.md`, `CITATION.cff`, `pyproject.toml`, and `paper/main.tex` if manuscript source is included.
3. Select a repository license and update `LICENSE.md`.
4. Decide whether to cite the GitHub URL directly or create a DOI-bearing release.
5. If Experiment 1 is included in the paper, run `make experiment-01` and report the generated table and figures honestly.

## Interpretation boundary

The repository's computational experiment is synthetic. It demonstrates operational coherence of the formal dot-field mechanisms under a controlled simulator. It does not establish external empirical validity in real social systems.
