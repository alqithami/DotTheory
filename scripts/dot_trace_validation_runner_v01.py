#!/usr/bin/env python3
"""
Validation runner for the minimal Dot-Trace Theory simulator.

This script executes a small condition-by-seed benchmarking grid and reports
condition summaries plus matched-seed divergence from the full dot-field
condition. It is intentionally simple and dependency-free so it can be copied
into Overleaf-adjacent research folders or run locally with Python 3.

Usage:
    python dot_trace_validation_runner_v01.py --seeds 1,2,3,4,5 --out dtt_validation
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from dot_trace_minimal_simulator_v01 import Config, DotTraceSimulator


def condition_grid() -> Dict[str, Dict[str, Any]]:
    """Return condition-specific Config overrides."""
    return {
        "edge_only": {
            "top_k": 0,
            "beta_z": 0.0,
            "p_transmit": 0.0,
            "p_institutional": 0.0,
            "correction_enabled": False,
            "mutation_enabled": False,
        },
        "private_dot": {
            "top_k": 5,
            "p_transmit": 0.0,
            "p_institutional": 0.0,
            "correction_enabled": False,
            "mutation_enabled": False,
        },
        "social_transmission": {
            "top_k": 5,
            "p_transmit": 0.10,
            "p_institutional": 0.0,
            "correction_enabled": False,
            "mutation_enabled": False,
        },
        "mutation": {
            "top_k": 5,
            "p_transmit": 0.10,
            "p_institutional": 0.0,
            "correction_enabled": False,
            "mutation_enabled": True,
            "mutation_epsilon": 0.10,
        },
        "institutional": {
            "top_k": 5,
            "p_transmit": 0.10,
            "p_institutional": 0.25,
            "correction_enabled": False,
            "mutation_enabled": False,
        },
        "correction": {
            "top_k": 5,
            "p_transmit": 0.10,
            "p_institutional": 0.0,
            "correction_enabled": True,
            "p_counter": 0.20,
            "mutation_enabled": False,
        },
        "topology_feedback_disabled": {
            "top_k": 5,
            "p_transmit": 0.10,
            "p_institutional": 0.10,
            "correction_enabled": False,
            "mutation_enabled": False,
            "eta_edge": 0.0,
        },
        "full_dot_field": {
            "top_k": 5,
            "p_transmit": 0.12,
            "p_institutional": 0.15,
            "correction_enabled": True,
            "p_counter": 0.15,
            "mutation_enabled": True,
            "mutation_epsilon": 0.08,
        },
    }


def make_config(base: Dict[str, Any], seed: int, overrides: Dict[str, Any]) -> Config:
    params = dict(base)
    params.update(overrides)
    params["seed"] = seed
    return Config(**params)


def run_once(condition: str, seed: int, config: Config) -> Dict[str, Any]:
    sim = DotTraceSimulator(config)
    sim.run()
    metrics = sim.metrics()
    summary = sim.summary()
    row: Dict[str, Any] = {
        "condition": condition,
        "seed": seed,
        "dot_count": summary["dot_count"],
        "event_count": summary["event_count"],
    }
    row.update(metrics)
    return row


def mean_sd(values: Iterable[float]) -> Dict[str, float]:
    vals = [float(v) for v in values]
    if not vals:
        return {"mean": 0.0, "sd": 0.0}
    if len(vals) == 1:
        return {"mean": vals[0], "sd": 0.0}
    return {"mean": statistics.mean(vals), "sd": statistics.stdev(vals)}


def aggregate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    metrics = [
        "cooperation_rate",
        "mean_trust",
        "active_dots",
        "access_count",
        "anchored_dots",
        "fragmentation_proxy",
        "dot_count",
        "event_count",
    ]
    out: Dict[str, Any] = {}
    for condition in sorted({r["condition"] for r in rows}):
        crows = [r for r in rows if r["condition"] == condition]
        out[condition] = {m: mean_sd(r[m] for r in crows) for m in metrics}
    return out


def matched_divergence(rows: List[Dict[str, Any]], reference: str = "full_dot_field") -> Dict[str, Any]:
    metrics = ["cooperation_rate", "mean_trust", "fragmentation_proxy", "active_dots", "access_count"]
    by_key = {(r["condition"], r["seed"]): r for r in rows}
    seeds = sorted({r["seed"] for r in rows if r["condition"] == reference})
    out: Dict[str, Any] = {}
    for condition in sorted({r["condition"] for r in rows}):
        if condition == reference:
            continue
        diffs: Dict[str, List[float]] = {m: [] for m in metrics}
        for seed in seeds:
            ref = by_key.get((reference, seed))
            cur = by_key.get((condition, seed))
            if not ref or not cur:
                continue
            for metric in metrics:
                diffs[metric].append(abs(float(ref[metric]) - float(cur[metric])))
        out[condition] = {m: mean_sd(vals) for m, vals in diffs.items()}
    return out


def parse_seeds(seed_text: str) -> List[int]:
    return [int(s.strip()) for s in seed_text.split(",") if s.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Dot-Trace validation condition grid")
    parser.add_argument("--agents", type=int, default=8)
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--interactions-per-step", type=int, default=6)
    parser.add_argument("--seeds", type=str, default="1,2,3,4,5")
    parser.add_argument("--out", type=str, default="dtt_validation")
    args = parser.parse_args()

    base = {
        "agents": args.agents,
        "steps": args.steps,
        "interactions_per_step": args.interactions_per_step,
    }
    seeds = parse_seeds(args.seeds)
    conditions = condition_grid()
    rows: List[Dict[str, Any]] = []
    configs: Dict[str, Dict[str, Any]] = {}

    for condition, overrides in conditions.items():
        configs[condition] = {**base, **overrides}
        for seed in seeds:
            cfg = make_config(base, seed, overrides)
            rows.append(run_once(condition, seed, cfg))

    prefix = Path(args.out)
    csv_path = prefix.with_name(prefix.name + "_runs.csv")
    json_path = prefix.with_name(prefix.name + "_summary.json")

    fieldnames = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "base_config": base,
        "seeds": seeds,
        "condition_overrides": configs,
        "aggregate": aggregate(rows),
        "matched_divergence_from_full_dot_field": matched_divergence(rows),
    }
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"runs_csv": str(csv_path), "summary_json": str(json_path)}, indent=2))


if __name__ == "__main__":
    main()
