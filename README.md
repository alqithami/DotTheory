# Dot-Trace Theory

**Dot-Trace Theory: A Formal Theory of Agentic Social Memory** is a theory of memory-sensitive social multi-agent systems. It proposes that persistent, socially accessible interaction traces — called **dots** — mediate the co-evolution of agent behavior, memory structure, and social topology.

This repository contains the foundation manuscript, LaTeX source, BibTeX bibliography, simulator prototypes, validation runners, experiment scaffolding, example outputs, and review/planning documents.

## Repository status

This repository is prepared as a comprehensive manuscript companion and reproducibility package. Before formal publication, complete the author metadata, license choice, and venue-specific statements listed in [`docs/publication_metadata_to_complete.md`](docs/publication_metadata_to_complete.md).

The computational scripts are **reference prototypes**. They support theory development, reproducibility checks, and synthetic validation design. They are not empirical evidence about real-world social systems.

## What is in this repository

```text
.
├── paper/                      # Canonical LaTeX source, BibTeX file, compiled PDF
├── scripts/                    # Reference simulators, validation runners, experiment runner
├── configs/                    # Reproducible experiment configurations
├── examples/                   # Example output files from simulator/validation runs
├── docs/                       # Theory notes, experiment docs, review reports, strategy docs
├── tests/                      # Lightweight repository checks
├── .github/workflows/          # GitHub Actions examples for Python and LaTeX checks
├── CITATION.cff                # Citation metadata template
├── Makefile                    # Local build/check/experiment commands
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

The scripts are dependency-free Python 3 prototypes and require Python 3.9 or newer.

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

## Experiment 1: dot-field prediction lift

Experiment 1 is a reproducible synthetic demonstration of the paper's central validation signature. It asks whether a full dot-field predictor improves held-out prediction of future cooperation relative to reduced baselines when actions depend on retrieved social traces.

The main runner is:

```text
scripts/run_experiment_01_prediction_lift.py
```

The default configuration is:

```text
configs/experiment_01_prediction_lift.json
```

Run a quick local check:

```bash
make experiment-01-quick
```

Run the full configured experiment:

```bash
make experiment-01
```

Or run manually:

```bash
python scripts/run_experiment_01_prediction_lift.py \
  --config configs/experiment_01_prediction_lift.json \
  --out results/experiment_01
```

Expected outputs include:

```text
results/experiment_01/experiment_01_summary.json
results/experiment_01/paper_results_table.csv
results/experiment_01/figures/prediction_lift_full.svg
results/experiment_01/figures/negative_control_degradation.svg
results/experiment_01/figures/ablation_lift_by_condition.svg
```

See [`docs/experiments/experiment_01_prediction_lift.md`](docs/experiments/experiment_01_prediction_lift.md) for the research question, design, outputs, interpretation rules, and reporting cautions.

## Repository checks

```bash
make check
```

This runs:

- Python syntax checks,
- lightweight repository tests,
- placeholder/draft-language scan on the paper source,
- citation-key consistency check,
- simulator smoke tests.

## Publication and reproducibility documents

| File | Purpose |
|---|---|
| [`docs/reproducibility_statement.md`](docs/reproducibility_statement.md) | Build, environment, and reproducibility notes |
| [`docs/code_availability_statement.md`](docs/code_availability_statement.md) | Suggested manuscript code-availability wording |
| [`docs/repository_submission_checklist.md`](docs/repository_submission_checklist.md) | Pre-submission repository checklist |
| [`docs/publication_metadata_to_complete.md`](docs/publication_metadata_to_complete.md) | Author, license, and venue metadata still requiring confirmation |

## Main files

| File | Purpose |
|---|---|
| [`paper/main.tex`](paper/main.tex) | Canonical LaTeX manuscript source |
| [`paper/references.bib`](paper/references.bib) | BibTeX bibliography |
| [`scripts/dot_trace_minimal_simulator_v01.py`](scripts/dot_trace_minimal_simulator_v01.py) | Minimal dot-field simulator |
| [`scripts/dot_trace_predictive_simulator_v02.py`](scripts/dot_trace_predictive_simulator_v02.py) | Predictive simulator with action-level forecasts |
| [`scripts/dot_trace_validation_runner_v01.py`](scripts/dot_trace_validation_runner_v01.py) | Condition-grid validation runner |
| [`scripts/dot_trace_prediction_lift_runner_v01.py`](scripts/dot_trace_prediction_lift_runner_v01.py) | Prediction-lift benchmark runner |
| [`scripts/dot_trace_trainable_validation_runner_v01.py`](scripts/dot_trace_trainable_validation_runner_v01.py) | Trainable held-out validation runner |
| [`scripts/run_experiment_01_prediction_lift.py`](scripts/run_experiment_01_prediction_lift.py) | Experiment 1 orchestration runner |
| [`configs/experiment_01_prediction_lift.json`](configs/experiment_01_prediction_lift.json) | Default Experiment 1 configuration |
| [`docs/experiments/experiment_01_prediction_lift.md`](docs/experiments/experiment_01_prediction_lift.md) | Experiment 1 documentation |
| [`docs/review/prepublication_audit_v0.43.md`](docs/review/prepublication_audit_v0.43.md) | Current pre-publication audit |
| [`docs/strategy/core_article_blueprint_v0.42.md`](docs/strategy/core_article_blueprint_v0.42.md) | Plan for extracting a shorter submission article |

## Citation

Use [`CITATION.cff`](CITATION.cff) as the repository citation template. Confirm the author metadata before formal publication or DOI archival.

## License

The license is intentionally marked as pending because author/publication decisions are not yet finalized. See [`LICENSE.md`](LICENSE.md).

## Disclaimer

The included simulators and Experiment 1 runner are reference prototypes for theory exploration and validation design. They are not empirical evidence for the theory and should not be used for consequential social decisions.
