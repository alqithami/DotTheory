# Dot-Trace Theory

**Dot-Trace Theory: A Formal Theory of Agentic Social Memory** is a theory of memory-sensitive social multi-agent systems. It proposes that persistent, socially accessible interaction traces - called **dots** - mediate the co-evolution of agent behavior, memory structure, and social topology.

This repository contains the current foundation manuscript, LaTeX source, bibliography, simulator prototypes, validation runners, example outputs, and review/planning documents.

## Repository status

Current packaged version: **v0.43.0**  
Date packaged: **2026-05-18**

This repository is prepared for GitHub use as a comprehensive foundation package. Before public release or formal publication, complete the author metadata, license choice, and venue-specific statements listed in [`docs/publication_metadata_to_complete.md`](docs/publication_metadata_to_complete.md).

## What is in this repository

```text
.
├── paper/                      # Canonical LaTeX source, BibTeX file, compiled PDF
├── scripts/                    # Reference simulators and validation runners
├── examples/                   # Example output files from simulator/validation runs
├── docs/                       # Review reports, strategic notes, version history
├── tests/                      # Lightweight repository checks
├── .github/workflows/          # GitHub Actions examples for Python and LaTeX checks
├── CITATION.cff                # Citation metadata template
├── Makefile                    # Local build/check commands
└── README.md
```

## Core theoretical claim

The reduced agent-edge state

\[
Z_t=(A,E_t,X_t,\bar S_t)
\]

may be insufficient in memory-sensitive social systems. Dot-Trace Theory augments this representation with a dot field containing persistent traces, dot-dot relations, agent-dot access relations, memory weights, effective retrievable strengths, lineage, institutional stores, and correction state.

The augmented state is written as

\[
\Omega_t^{aug}=(\Omega_t^{core},\mathbf M_t,Q_t,L_t,I_t,C_t),
\]

where

\[
\Omega_t^{core}=(A,E_t,X_t,\bar S_t,D_t,R_t^D,B_t).
\]

The theory is organized around a theorem spine:

1. Representational insufficiency
2. Dot-field Markov restoration
3. Consensus and fragmentation
4. Temporal sequencing and non-commutativity
5. Integrated mixed-mechanism dynamics
6. Recursive topology-feedback stability

## Build the paper locally

The paper is in [`paper/main.tex`](paper/main.tex), with bibliography in [`paper/references.bib`](paper/references.bib).

From the repository root:

```bash
make paper
```

Or manually:

```bash
cd paper
pdflatex -interaction=nonstopmode main.tex
bibtex8 main || bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The included compiled check PDF is:

```text
paper/dot_trace_theory_foundation_v0.43.pdf
```

## Run simulator smoke tests

The scripts are dependency-free Python 3 prototypes.

```bash
make smoke
```

Equivalent manual commands:

```bash
python scripts/dot_trace_minimal_simulator_v01.py --agents 4 --steps 3 --interactions-per-step 3 --out examples/smoke/minimal
python scripts/dot_trace_predictive_simulator_v02.py --agents 4 --steps 3 --interactions-per-step 3 --out examples/smoke/predictive
python scripts/dot_trace_validation_runner_v01.py --agents 4 --steps 3 --interactions-per-step 3 --seeds 1,2 --out examples/smoke/validation
python scripts/dot_trace_prediction_lift_runner_v01.py --agents 4 --steps 3 --interactions-per-step 3 --seeds 1 2 --out examples/smoke/prediction_lift
python scripts/dot_trace_trainable_validation_runner_v01.py --simulator scripts/dot_trace_predictive_simulator_v02.py --agents 4 --steps 12 --interactions-per-step 3 --seeds 2 --epochs 30 --out examples/smoke/trainable
```

## Repository checks

```bash
make check
```

This runs:

- placeholder/draft-language scan on the paper source,
- citation-key consistency check,
- Python syntax checks,
- simulator smoke tests.

## Main files

| File | Purpose |
|---|---|
| [`paper/main.tex`](paper/main.tex) | Canonical LaTeX manuscript source |
| [`paper/references.bib`](paper/references.bib) | BibTeX bibliography |
| [`paper/dot_trace_theory_foundation_v0.43.pdf`](paper/dot_trace_theory_foundation_v0.43.pdf) | Compiled PDF check |
| [`scripts/dot_trace_minimal_simulator_v01.py`](scripts/dot_trace_minimal_simulator_v01.py) | Minimal dot-field simulator |
| [`scripts/dot_trace_predictive_simulator_v02.py`](scripts/dot_trace_predictive_simulator_v02.py) | Predictive simulator with action-level forecasts |
| [`scripts/dot_trace_validation_runner_v01.py`](scripts/dot_trace_validation_runner_v01.py) | Condition-grid validation runner |
| [`scripts/dot_trace_prediction_lift_runner_v01.py`](scripts/dot_trace_prediction_lift_runner_v01.py) | Prediction-lift benchmark runner |
| [`scripts/dot_trace_trainable_validation_runner_v01.py`](scripts/dot_trace_trainable_validation_runner_v01.py) | Trainable held-out validation runner |
| [`docs/review/prepublication_audit_v0.43.md`](docs/review/prepublication_audit_v0.43.md) | Current pre-publication audit |
| [`docs/strategy/core_article_blueprint_v0.42.md`](docs/strategy/core_article_blueprint_v0.42.md) | Plan for extracting shorter submission article |

## Citation

Use [`CITATION.cff`](CITATION.cff) as a template. Replace the placeholder author metadata before public release.

## License

The license is intentionally marked as pending because author/publication decisions are not yet finalized. See [`LICENSE.md`](LICENSE.md).

Recommended default, once approved by the author(s):

- manuscript and documentation: **CC BY 4.0**,
- code: **MIT** or **Apache-2.0**.

## Disclaimer

The included simulators are reference prototypes for theory exploration and validation design. They are not empirical evidence for the theory and should not be used for consequential social decisions.
