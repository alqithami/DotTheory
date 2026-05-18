#!/usr/bin/env python3
"""
Prediction-lift runner for the predictive Dot-Trace simulator.

Runs matched seeds across mechanism conditions and reports predictive losses
for B0, edge-only, private-flat, bag-of-dots, and full retrieved-dot-field
predictors. The script is dependency-free and imports
`dot_trace_predictive_simulator_v02.py` from the same directory.

Example:
    python dot_trace_prediction_lift_runner_v01.py --seeds 1 2 3 4 5 --out dtt_lift
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path
from statistics import mean, pstdev
from typing import Dict, Iterable, List, Tuple


HERE = Path(__file__).resolve().parent
SIM_PATH = HERE / "dot_trace_predictive_simulator_v02.py"


def load_sim_module():
    spec = importlib.util.spec_from_file_location("dot_trace_predictive_simulator_v02", SIM_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load simulator module at {SIM_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


simmod = load_sim_module()


def condition_config(name: str, seed: int, args: argparse.Namespace):
    cfg = simmod.Config(
        agents=args.agents,
        steps=args.steps,
        interactions_per_step=args.interactions_per_step,
        top_k=args.top_k,
        seed=seed,
        condition=name,
        p_transmit=args.p_transmit,
        p_institutional=args.p_institutional,
        p_counter=args.p_counter,
        beta_z=args.beta_z,
    )
    if name == "edge_only_generator":
        cfg.beta_z = 0.0
        cfg.transmission_enabled = False
        cfg.mutation_enabled = False
        cfg.correction_enabled = False
        cfg.p_institutional = 0.0
        cfg.topology_feedback_enabled = True
    elif name == "private_memory":
        cfg.transmission_enabled = False
        cfg.mutation_enabled = False
        cfg.correction_enabled = False
        cfg.p_institutional = 0.0
    elif name == "social_transmission":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = False
        cfg.correction_enabled = False
        cfg.p_institutional = 0.0
    elif name == "mutation":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = True
        cfg.correction_enabled = False
        cfg.p_institutional = 0.0
    elif name == "institutional":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = False
        cfg.correction_enabled = False
        cfg.p_institutional = max(args.p_institutional, 0.12)
    elif name == "correction":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = False
        cfg.correction_enabled = True
        cfg.p_counter = max(args.p_counter, 0.06)
    elif name == "no_topology_feedback":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = True
        cfg.correction_enabled = True
        cfg.p_counter = max(args.p_counter, 0.06)
        cfg.p_institutional = max(args.p_institutional, 0.12)
        cfg.topology_feedback_enabled = False
    elif name == "full":
        cfg.transmission_enabled = True
        cfg.mutation_enabled = True
        cfg.correction_enabled = True
        cfg.p_counter = max(args.p_counter, 0.06)
        cfg.p_institutional = max(args.p_institutional, 0.12)
    else:
        raise ValueError(f"Unknown condition: {name}")
    return cfg


def flatten_metrics(condition: str, seed: int, summary: Dict[str, object]) -> Dict[str, object]:
    metrics = summary["metrics"]  # type: ignore[index]
    pred = summary["prediction_metrics"]  # type: ignore[index]
    row: Dict[str, object] = {
        "condition": condition,
        "seed": seed,
        "prediction_records": summary["prediction_records"],
        "dot_count": summary["dot_count"],
        "event_count": summary["event_count"],
    }
    for k, v in metrics.items():
        if not str(k).startswith("pred_"):
            row[k] = v
    for model_name, model_metrics in pred.items():
        for metric_name, value in model_metrics.items():
            if value is not None:
                row[f"{model_name}_{metric_name}"] = value
    return row


def aggregate(rows: List[Dict[str, object]]) -> Dict[str, object]:
    by_condition: Dict[str, List[Dict[str, object]]] = {}
    for row in rows:
        by_condition.setdefault(str(row["condition"]), []).append(row)
    numeric_keys = sorted({
        key for row in rows for key, value in row.items()
        if key not in {"condition", "seed"} and isinstance(value, (int, float))
    })
    summary: Dict[str, object] = {}
    for condition, condition_rows in by_condition.items():
        summary[condition] = {"runs": len(condition_rows)}
        for key in numeric_keys:
            vals = [float(r[key]) for r in condition_rows if isinstance(r.get(key), (int, float))]
            if not vals:
                continue
            summary[condition][f"{key}_mean"] = mean(vals)
            summary[condition][f"{key}_sd"] = pstdev(vals) if len(vals) > 1 else 0.0
    # A compact cross-condition comparison against the full condition.
    if "full" in by_condition:
        full_mean_lift = mean(float(r.get("lift_log_loss_vs_edge", 0.0)) for r in by_condition["full"])
        summary["headline"] = {
            "full_mean_log_loss_lift_vs_edge": full_mean_lift,
            "interpretation": "Positive values mean the full retrieved-dot-field predictor had lower log loss than the edge-only predictor on matched action records."
        }
    return summary


def write_csv(rows: List[Dict[str, object]], path: Path) -> None:
    keys = sorted({key for row in rows for key in row.keys()})
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Dot-Trace prediction-lift validation")
    parser.add_argument("--agents", type=int, default=8)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--interactions-per-step", type=int, default=8)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    parser.add_argument("--conditions", nargs="+", default=[
        "edge_only_generator", "private_memory", "social_transmission",
        "mutation", "institutional", "correction", "no_topology_feedback", "full"
    ])
    parser.add_argument("--p-transmit", type=float, default=0.08)
    parser.add_argument("--p-institutional", type=float, default=0.05)
    parser.add_argument("--p-counter", type=float, default=0.05)
    parser.add_argument("--beta-z", type=float, default=1.25)
    parser.add_argument("--out", type=str, default="dtt_prediction_lift")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows: List[Dict[str, object]] = []
    for condition in args.conditions:
        for seed in args.seeds:
            cfg = condition_config(condition, seed, args)
            sim = simmod.DotTraceSimulator(cfg)
            sim.run()
            rows.append(flatten_metrics(condition, seed, sim.summary()))
    out_prefix = Path(args.out)
    csv_path = out_prefix.with_name(out_prefix.name + "_runs.csv")
    summary_path = out_prefix.with_name(out_prefix.name + "_summary.json")
    write_csv(rows, csv_path)
    summary = {
        "config": {
            "agents": args.agents,
            "steps": args.steps,
            "interactions_per_step": args.interactions_per_step,
            "top_k": args.top_k,
            "seeds": args.seeds,
            "conditions": args.conditions,
        },
        "aggregate": aggregate(rows),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"runs": csv_path.as_posix(), "summary": summary_path.as_posix()}, indent=2))


if __name__ == "__main__":
    main()
