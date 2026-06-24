# Reproducibility Statement

This repository is intended to make the Dot-Trace Theory manuscript and its synthetic computational demonstrations reproducible.

## Repository components

| Component | Location | Reproducibility role |
|---|---|---|
| Manuscript source | `paper/main.tex` | Canonical LaTeX source for the foundation manuscript |
| Bibliography | `paper/references.bib` | Structured BibTeX references used by the manuscript |
| Minimal simulator | `scripts/dot_trace_minimal_simulator_v01.py` | Small reference implementation of dot-field dynamics |
| Predictive simulator | `scripts/dot_trace_predictive_simulator_v02.py` | Simulator that emits action-level prediction records |
| Validation runner | `scripts/dot_trace_trainable_validation_runner_v01.py` | Fits held-out predictive baselines and negative controls |
| Experiment 1 runner | `scripts/run_experiment_01_prediction_lift.py` | Orchestrates prediction-lift experiment and ablations |
| Experiment config | `configs/experiment_01_prediction_lift.json` | Fixed default parameters for Experiment 1 |

## Environment

The core scripts are designed for Python 3.9 or newer and avoid mandatory third-party Python packages. LaTeX compilation requires a TeX distribution with `pdflatex` and either `bibtex8` or `bibtex`.

Recommended local setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Then run:

```bash
make check
```

## Paper build

```bash
make paper
```

Manual equivalent:

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex8 main || bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Experiment 1

Quick check:

```bash
make experiment-01-quick
```

Full configured run:

```bash
make experiment-01
```

The full run writes outputs under:

```text
results/experiment_01/
```

The result directory is intentionally ignored by Git because generated outputs should not be committed unless a specific archival release is being prepared.

## Determinism and random seeds

The configuration file records seed counts and base seeds. The simulator is deterministic conditional on the script version, Python version, configuration, and pseudorandom seed stream. Small numerical differences may occur across Python implementations or platforms, but the direction of major synthetic validation signatures should be checked across multiple seeds rather than one run.

## Interpretation boundary

The computational experiments are synthetic mechanism checks. They do not establish that the theory is empirically true in real-world social systems. External validation requires dot extraction, observability assessment, negative controls, and causal or predictive evaluation on appropriate data.

## Archival recommendation

Before citing a specific repository state in a paper, create a tagged GitHub release and archive it through a DOI provider such as Zenodo, OSF, or institutional archival infrastructure. The manuscript should cite the repository URL and, when available, the release DOI.
