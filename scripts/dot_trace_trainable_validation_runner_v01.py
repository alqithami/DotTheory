#!/usr/bin/env python3
"""
Trainable validation runner for Dot-Trace Theory, v0.1.

This script uses the predictive Dot-Trace simulator to create action-level
prediction records, then fits trainable predictors on a temporal training split
and evaluates them on held-out future records. It also evaluates negative-control
variants that preserve marginal feature distributions while destroying one or
more dot-field alignments.

The runner is intentionally dependency-free. It implements a small L2-regularized
logistic regression estimator with feature standardization, paired log-loss lift,
paired standard errors, and simple negative controls.

Example:
    python dot_trace_trainable_validation_runner_v01.py \
        --simulator dot_trace_predictive_simulator_v02.py \
        --seeds 10 --steps 70 --agents 10 --out dtt_trainable_validation
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import random
import statistics
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

EPS = 1e-12


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def clip_prob(p: float) -> float:
    return max(EPS, min(1.0 - EPS, p))


def safe_log_loss(y: int, p: float) -> float:
    p = clip_prob(p)
    return -(y * math.log(p) + (1 - y) * math.log(1.0 - p))


def brier_loss(y: int, p: float) -> float:
    return (float(y) - p) ** 2


def roc_auc(y: Sequence[int], p: Sequence[float]) -> Optional[float]:
    pos = [prob for label, prob in zip(y, p) if label == 1]
    neg = [prob for label, prob in zip(y, p) if label == 0]
    if not pos or not neg:
        return None
    wins = 0.0
    total = len(pos) * len(neg)
    for pp in pos:
        for pn in neg:
            if pp > pn:
                wins += 1.0
            elif pp == pn:
                wins += 0.5
    return wins / total


def expected_calibration_error(y: Sequence[int], p: Sequence[float], bins: int = 10) -> Optional[float]:
    if not y:
        return None
    n = len(y)
    ece = 0.0
    for b in range(bins):
        lo = b / bins
        hi = (b + 1) / bins
        idx = [i for i, prob in enumerate(p) if (lo <= prob < hi) or (b == bins - 1 and prob == hi)]
        if not idx:
            continue
        conf = sum(p[i] for i in idx) / len(idx)
        acc = sum(y[i] for i in idx) / len(idx)
        ece += (len(idx) / n) * abs(acc - conf)
    return ece


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def stderr(xs: Sequence[float]) -> float:
    if len(xs) < 2:
        return float("nan")
    return statistics.stdev(xs) / math.sqrt(len(xs))


def import_simulator(path: Path):
    spec = importlib.util.spec_from_file_location("dtt_predictive_simulator", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import simulator at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Standardizer:
    def __init__(self) -> None:
        self.mu: List[float] = []
        self.sd: List[float] = []

    def fit(self, X: Sequence[Sequence[float]]) -> "Standardizer":
        if not X or not X[0]:
            self.mu = []
            self.sd = []
            return self
        d = len(X[0])
        self.mu = []
        self.sd = []
        for j in range(d):
            col = [row[j] for row in X]
            m = mean(col)
            var = sum((v - m) ** 2 for v in col) / max(1, len(col) - 1)
            s = math.sqrt(var)
            if s < 1e-9:
                s = 1.0
            self.mu.append(m)
            self.sd.append(s)
        return self

    def transform(self, X: Sequence[Sequence[float]]) -> List[List[float]]:
        if not X:
            return []
        if not self.mu:
            return [[] for _ in X]
        return [[(row[j] - self.mu[j]) / self.sd[j] for j in range(len(self.mu))] for row in X]


class LogisticRegressionL2:
    def __init__(self, l2: float = 1e-3, learning_rate: float = 0.12, epochs: int = 1500) -> None:
        self.l2 = l2
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights: List[float] = []

    def fit(self, X: Sequence[Sequence[float]], y: Sequence[int]) -> "LogisticRegressionL2":
        n = len(y)
        if n == 0:
            raise ValueError("Empty training set")
        d = len(X[0]) if X and X[0] else 0
        base = min(max(mean([float(v) for v in y]), 1e-4), 1.0 - 1e-4)
        intercept = math.log(base / (1.0 - base))
        self.weights = [intercept] + [0.0] * d
        if d == 0:
            return self
        lr = self.learning_rate / math.sqrt(max(1, d))
        for _ in range(self.epochs):
            grad = [0.0] * (d + 1)
            for row, label in zip(X, y):
                z = self.weights[0] + sum(self.weights[j + 1] * row[j] for j in range(d))
                p = sigmoid(z)
                err = p - label
                grad[0] += err
                for j in range(d):
                    grad[j + 1] += err * row[j]
            grad[0] /= n
            for j in range(d):
                grad[j + 1] = grad[j + 1] / n + self.l2 * self.weights[j + 1]
            for j in range(d + 1):
                self.weights[j] -= lr * grad[j]
        return self

    def predict_proba(self, X: Sequence[Sequence[float]]) -> List[float]:
        d = len(self.weights) - 1
        out: List[float] = []
        for row in X:
            z = self.weights[0] + sum(self.weights[j + 1] * row[j] for j in range(d))
            out.append(clip_prob(sigmoid(z)))
        return out


def features(rows: Sequence[Dict[str, float]], cols: Sequence[str]) -> List[List[float]]:
    return [[float(r[c]) for c in cols] for r in rows]


def evaluate(y: Sequence[int], p: Sequence[float]) -> Dict[str, Optional[float]]:
    if not y:
        return {"log_loss": None, "brier": None, "accuracy": None, "auc": None, "ece": None}
    return {
        "log_loss": mean([safe_log_loss(label, prob) for label, prob in zip(y, p)]),
        "brier": mean([brier_loss(label, prob) for label, prob in zip(y, p)]),
        "accuracy": mean([1.0 if (prob >= 0.5) == bool(label) else 0.0 for label, prob in zip(y, p)]),
        "auc": roc_auc(y, p),
        "ece": expected_calibration_error(y, p),
    }


def generate_records(sim_module, args: argparse.Namespace) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    for s in range(args.seeds):
        cfg = sim_module.Config(
            agents=args.agents,
            steps=args.steps,
            interactions_per_step=args.interactions_per_step,
            seed=args.base_seed + s,
            top_k=args.top_k,
            condition="full",
            mutation_enabled=args.mutation,
            correction_enabled=args.correction,
            p_counter=args.p_counter,
            p_transmit=args.p_transmit,
            p_institutional=args.p_institutional,
            beta_z=args.beta_z,
            transmission_enabled=not args.no_transmission,
            topology_feedback_enabled=not args.no_topology_feedback,
        )
        sim = sim_module.DotTraceSimulator(cfg)
        sim.run()
        for rec in sim.state.predictions:
            row = asdict(rec)
            row["run_seed"] = args.base_seed + s
            row["condition"] = "full"
            rows.append(row)
    return rows


def add_negative_control_columns(rows: List[Dict[str, float]], seed: int) -> None:
    rng = random.Random(seed)
    n = len(rows)
    idx = list(range(n))

    # Global pressure permutation: preserves marginal pressure distribution, destroys alignment.
    perm = idx[:]
    rng.shuffle(perm)
    for out_i, in_i in enumerate(perm):
        rows[out_i]["pressure_full_perm"] = rows[in_i]["pressure_full"]

    # Access permutation: preserves count distributions, destroys access-action alignment.
    perm = idx[:]
    rng.shuffle(perm)
    for out_i, in_i in enumerate(perm):
        rows[out_i]["retrieved_count_perm"] = rows[in_i]["retrieved_count"]
        rows[out_i]["accessible_target_dots_perm"] = rows[in_i]["accessible_target_dots"]

    # Temporal reversal within each run: preserves run-level values but reverses sequence alignment.
    by_seed: Dict[int, List[int]] = {}
    for i, r in enumerate(rows):
        by_seed.setdefault(int(r["run_seed"]), []).append(i)
    for seed_key, indices in by_seed.items():
        ordered = sorted(indices, key=lambda k: (int(rows[k]["time"]), int(rows[k]["actor"]), int(rows[k]["target"])))
        reversed_order = list(reversed(ordered))
        for out_i, in_i in zip(ordered, reversed_order):
            rows[out_i]["pressure_full_reversed"] = rows[in_i]["pressure_full"]

    # Target/time shuffle: preserves same-time event intensity but destroys target-specific binding when possible.
    by_seed_time: Dict[Tuple[int, int], List[int]] = {}
    for i, r in enumerate(rows):
        by_seed_time.setdefault((int(r["run_seed"]), int(r["time"])), []).append(i)
    for _, indices in by_seed_time.items():
        values = [rows[i]["pressure_full"] for i in indices]
        rng.shuffle(values)
        for i, v in zip(indices, values):
            rows[i]["pressure_full_target_shuffle"] = v


def temporal_split(rows: Sequence[Dict[str, float]], train_fraction: float) -> Tuple[List[Dict[str, float]], List[Dict[str, float]]]:
    train: List[Dict[str, float]] = []
    test: List[Dict[str, float]] = []
    max_time_by_seed: Dict[int, int] = {}
    for r in rows:
        seed = int(r["run_seed"])
        max_time_by_seed[seed] = max(max_time_by_seed.get(seed, -1), int(r["time"]))
    cut_by_seed = {seed: math.floor(train_fraction * (mx + 1)) for seed, mx in max_time_by_seed.items()}
    for r in rows:
        if int(r["time"]) < cut_by_seed[int(r["run_seed"] )]:
            train.append(dict(r))
        else:
            test.append(dict(r))
    return train, test


def fit_and_evaluate(
    name: str,
    cols: Sequence[str],
    train_rows: Sequence[Dict[str, float]],
    test_rows: Sequence[Dict[str, float]],
    args: argparse.Namespace,
) -> Tuple[Dict[str, object], List[float], LogisticRegressionL2]:
    y_train = [int(r["actual"]) for r in train_rows]
    y_test = [int(r["actual"]) for r in test_rows]
    X_train_raw = features(train_rows, cols)
    X_test_raw = features(test_rows, cols)
    scaler = Standardizer().fit(X_train_raw)
    X_train = scaler.transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)
    model = LogisticRegressionL2(l2=args.l2, learning_rate=args.learning_rate, epochs=args.epochs).fit(X_train, y_train)
    p_test = model.predict_proba(X_test)
    metrics = evaluate(y_test, p_test)
    out: Dict[str, object] = {
        "model": name,
        "features": ",".join(cols) if cols else "intercept_only",
        "n_train": len(train_rows),
        "n_test": len(test_rows),
        "intercept": model.weights[0],
        "num_features": len(cols),
    }
    for k, v in metrics.items():
        out[k] = v
    return out, p_test, model


def paired_lift(y: Sequence[int], p_baseline: Sequence[float], p_full: Sequence[float]) -> Dict[str, float]:
    diffs = [safe_log_loss(label, pb) - safe_log_loss(label, pf) for label, pb, pf in zip(y, p_baseline, p_full)]
    m = mean(diffs)
    se = stderr(diffs)
    return {
        "mean": m,
        "se": se,
        "ci95_low": m - 1.96 * se if not math.isnan(se) else float("nan"),
        "ci95_high": m + 1.96 * se if not math.isnan(se) else float("nan"),
    }


def run_validation(args: argparse.Namespace) -> Dict[str, object]:
    sim_module = import_simulator(Path(args.simulator))
    rows = generate_records(sim_module, args)
    add_negative_control_columns(rows, args.base_seed + 10000)
    train_rows, test_rows = temporal_split(rows, args.train_fraction)

    feature_sets: Dict[str, List[str]] = {
        "b0": [],
        "edge": ["trust"],
        "private_flat": ["trust", "pressure_private_flat"],
        "bag": ["trust", "pressure_bag", "accessible_target_dots"],
        "full": ["trust", "pressure_full", "retrieved_count", "accessible_target_dots"],
        "control_pressure_shuffle": ["trust", "pressure_full_perm", "retrieved_count", "accessible_target_dots"],
        "control_access_shuffle": ["trust", "pressure_full", "retrieved_count_perm", "accessible_target_dots_perm"],
        "control_temporal_reverse": ["trust", "pressure_full_reversed", "retrieved_count", "accessible_target_dots"],
        "control_target_shuffle": ["trust", "pressure_full_target_shuffle", "retrieved_count", "accessible_target_dots"],
    }

    metrics_rows: List[Dict[str, object]] = []
    predictions: Dict[str, List[float]] = {}
    models: Dict[str, LogisticRegressionL2] = {}
    for name, cols in feature_sets.items():
        metric, pred, model = fit_and_evaluate(name, cols, train_rows, test_rows, args)
        metrics_rows.append(metric)
        predictions[name] = pred
        models[name] = model

    y_test = [int(r["actual"]) for r in test_rows]
    full_pred = predictions["full"]
    lift_summary: Dict[str, Dict[str, float]] = {}
    for name in ["b0", "edge", "private_flat", "bag"]:
        lift_summary[f"full_vs_{name}"] = paired_lift(y_test, predictions[name], full_pred)
    control_degradation: Dict[str, Dict[str, float]] = {}
    # Positive degradation means the control has higher log loss than the aligned full model.
    for name in ["control_pressure_shuffle", "control_access_shuffle", "control_temporal_reverse", "control_target_shuffle"]:
        diffs = [safe_log_loss(label, pc) - safe_log_loss(label, pf) for label, pc, pf in zip(y_test, predictions[name], full_pred)]
        m = mean(diffs)
        se = stderr(diffs)
        control_degradation[name] = {
            "mean_log_loss_degradation_vs_full": m,
            "se": se,
            "ci95_low": m - 1.96 * se if not math.isnan(se) else float("nan"),
            "ci95_high": m + 1.96 * se if not math.isnan(se) else float("nan"),
        }

    # Attach lift columns to metrics rows for concise CSV inspection.
    full_ll = next(float(r["log_loss"]) for r in metrics_rows if r["model"] == "full")
    edge_ll = next(float(r["log_loss"]) for r in metrics_rows if r["model"] == "edge")
    bag_ll = next(float(r["log_loss"]) for r in metrics_rows if r["model"] == "bag")
    for r in metrics_rows:
        r["log_loss_lift_full_vs_model"] = float(r["log_loss"]) - full_ll
        r["log_loss_lift_model_vs_edge"] = edge_ll - float(r["log_loss"])
        r["log_loss_lift_model_vs_bag"] = bag_ll - float(r["log_loss"])

    test_prediction_rows: List[Dict[str, object]] = []
    for idx, r in enumerate(test_rows):
        out = dict(r)
        for name, probs in predictions.items():
            out[f"p_hat_{name}"] = probs[idx]
        test_prediction_rows.append(out)

    output_prefix = Path(args.out)
    records_path = output_prefix.with_name(output_prefix.name + "_records.csv")
    metrics_path = output_prefix.with_name(output_prefix.name + "_metrics.csv")
    preds_path = output_prefix.with_name(output_prefix.name + "_test_predictions.csv")
    summary_path = output_prefix.with_name(output_prefix.name + "_summary.json")

    def write_csv(path: Path, data: Sequence[Dict[str, object]]) -> None:
        if not data:
            path.write_text("", encoding="utf-8")
            return
        keys: List[str] = []
        for row in data:
            for key in row.keys():
                if key not in keys:
                    keys.append(key)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    write_csv(records_path, rows)
    write_csv(metrics_path, metrics_rows)
    write_csv(preds_path, test_prediction_rows)

    summary: Dict[str, object] = {
        "config": vars(args),
        "n_records": len(rows),
        "n_train": len(train_rows),
        "n_test": len(test_rows),
        "temporal_train_fraction": args.train_fraction,
        "feature_sets": feature_sets,
        "metrics": metrics_rows,
        "paired_log_loss_lift": lift_summary,
        "negative_control_degradation": control_degradation,
        "files": {
            "records": records_path.as_posix(),
            "metrics": metrics_path.as_posix(),
            "test_predictions": preds_path.as_posix(),
            "summary": summary_path.as_posix(),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trainable Dot-Trace validation runner")
    parser.add_argument("--simulator", type=str, default="dot_trace_predictive_simulator_v02.py")
    parser.add_argument("--out", type=str, default="dtt_trainable_validation")
    parser.add_argument("--agents", type=int, default=10)
    parser.add_argument("--steps", type=int, default=70)
    parser.add_argument("--interactions-per-step", type=int, default=10)
    parser.add_argument("--seeds", type=int, default=10)
    parser.add_argument("--base-seed", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--train-fraction", type=float, default=0.70)
    parser.add_argument("--mutation", action="store_true", default=True)
    parser.add_argument("--no-mutation", action="store_false", dest="mutation")
    parser.add_argument("--correction", action="store_true", default=True)
    parser.add_argument("--no-correction", action="store_false", dest="correction")
    parser.add_argument("--no-transmission", action="store_true")
    parser.add_argument("--no-topology-feedback", action="store_true")
    parser.add_argument("--p-counter", type=float, default=0.05)
    parser.add_argument("--p-transmit", type=float, default=0.08)
    parser.add_argument("--p-institutional", type=float, default=0.05)
    parser.add_argument("--beta-z", type=float, default=1.25)
    parser.add_argument("--l2", type=float, default=1e-3)
    parser.add_argument("--learning-rate", type=float, default=0.16)
    parser.add_argument("--epochs", type=int, default=1600)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = run_validation(args)
    print(json.dumps({
        "summary": summary["files"]["summary"],
        "metrics": summary["files"]["metrics"],
        "test_predictions": summary["files"]["test_predictions"],
        "n_records": summary["n_records"],
        "n_train": summary["n_train"],
        "n_test": summary["n_test"],
        "full_vs_edge_log_loss_lift": summary["paired_log_loss_lift"]["full_vs_edge"],
        "full_vs_bag_log_loss_lift": summary["paired_log_loss_lift"]["full_vs_bag"],
        "negative_controls": summary["negative_control_degradation"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
