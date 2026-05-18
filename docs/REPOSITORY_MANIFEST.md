# Repository Manifest

## Paper

- `paper/main.tex`: canonical LaTeX manuscript source.
- `paper/references.bib`: bibliography.
- `paper/dot_trace_theory_foundation_v0.43.pdf`: compiled PDF check.
- `paper/figures/README.md`: notes on figure handling; most figures are currently TikZ figures embedded in `main.tex`.

## Scripts

- `scripts/dot_trace_minimal_simulator_v01.py`: minimal reference simulator.
- `scripts/dot_trace_predictive_simulator_v02.py`: simulator with prediction records.
- `scripts/dot_trace_validation_runner_v01.py`: condition-grid runner.
- `scripts/dot_trace_prediction_lift_runner_v01.py`: prediction-lift runner.
- `scripts/dot_trace_trainable_validation_runner_v01.py`: held-out trainable validation runner.
- `scripts/check_citations.py`: citation consistency checker.
- `scripts/check_placeholders.py`: draft-marker checker.
- `scripts/run_smoke_tests.sh`: small smoke-test suite.

## Examples

- `examples/minimal/`: one minimal simulator run.
- `examples/predictive/`: prediction-record run.
- `examples/validation/`: validation and prediction-lift outputs.
- `examples/trainable_validation/`: trainable validation outputs.

## Docs

- `docs/review/`: pre-publication audit and visual QA artifacts.
- `docs/strategy/`: readiness review, core article blueprint, split map.
- `docs/version_history/`: selected changelog files from development.
- `docs/publication_metadata_to_complete.md`: metadata checklist.
- `docs/THEORY_OVERVIEW.md`: short conceptual overview.
