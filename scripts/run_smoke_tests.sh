#!/usr/bin/env bash
set -euo pipefail

mkdir -p examples/smoke

python scripts/dot_trace_minimal_simulator_v01.py \
  --agents 4 --steps 3 --interactions-per-step 3 \
  --out examples/smoke/minimal >/dev/null

python scripts/dot_trace_predictive_simulator_v02.py \
  --agents 4 --steps 3 --interactions-per-step 3 \
  --out examples/smoke/predictive >/dev/null

python scripts/dot_trace_validation_runner_v01.py \
  --agents 4 --steps 3 --interactions-per-step 3 \
  --seeds 1,2 --out examples/smoke/validation >/dev/null

python scripts/dot_trace_prediction_lift_runner_v01.py \
  --agents 4 --steps 3 --interactions-per-step 3 \
  --seeds 1 2 --out examples/smoke/prediction_lift >/dev/null

python scripts/dot_trace_trainable_validation_runner_v01.py \
  --simulator scripts/dot_trace_predictive_simulator_v02.py \
  --agents 4 --steps 12 --interactions-per-step 3 \
  --seeds 2 --epochs 30 --out examples/smoke/trainable >/dev/null

echo "Smoke tests passed. Outputs written to examples/smoke/"
