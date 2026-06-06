#!/usr/bin/env python3
"""
Run Experiment 1 for Dot-Trace Theory: dot-field prediction lift.

This orchestration script is intentionally dependency-free. It calls the existing
trainable validation runner, evaluates a full dot-field condition and mechanism
ablations, then writes a compact experiment summary, a paper-ready CSV table, and
simple SVG figures.

The experiment is synthetic. Its purpose is not to validate Dot-Trace Theory in
real-world data, but to test whether the reference simulator exhibits the
theoretical validation signature: dot-field features should improve held-out
prediction when action depends on retrieved social traces, and corrupted dot
features should degrade performance.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "experiment_01_prediction_lift.json"
TRAINABLE_RUNNER = REPO_ROOT / "scripts" / "dot_trace_trainable_validation_runner_v01.py"
PREDICTIVE_SIMULATOR = REPO_ROOT / "scripts" / "dot_trace_predictive_simulator_v02.py"


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))


def maybe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        v = float(value)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


def add_common_args(cmd: List[str], config: Mapping[str, Any]) -> None:
    """Append arguments understood by dot_trace_trainable_validation_runner_v01.py."""
    mapping = {
        "agents": "--agents",
        "steps": "--steps",
        "interactions_per_step": "--interactions-per-step",
        "seeds": "--seeds",
        "base_seed": "--base-seed",
        "top_k": "--top-k",
        "train_fraction": "--train-fraction",
        "p_counter": "--p-counter",
        "p_transmit": "--p-transmit",
        "p_institutional": "--p-institutional",
        "beta_z": "--beta-z",
        "epochs": "--epochs",
        "learning_rate": "--learning-rate",
        "l2": "--l2",
    }
    for key, flag in mapping.items():
        if key in config:
            cmd.extend([flag, str(config[key])])


def run_condition(
    name: str,
    condition: Mapping[str, Any],
    base_config: Mapping[str, Any],
    outdir: Path,
    dry_run: bool = False,
) -> Tuple[Path, Dict[str, Any]]:
    """Run one trainable-validation condition and return its summary."""
    prefix = outdir / name / name
    prefix.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(TRAINABLE_RUNNER),
        "--simulator",
        str(PREDICTIVE_SIMULATOR),
        "--out",
        str(prefix),
    ]
    add_common_args(cmd, base_config)

    if condition.get("no_transmission", False):
        cmd.append("--no-transmission")
    if condition.get("no_topology_feedback", False):
        cmd.append("--no-topology-feedback")
    if condition.get("no_mutation", False):
        cmd.append("--no-mutation")
    if condition.get("no_correction", False):
        cmd.append("--no-correction")

    log_path = prefix.with_name(prefix.name + "_stdout_stderr.log")
    command_path = prefix.with_name(prefix.name + "_command.txt")
    command_path.write_text(" ".join(cmd) + "\n", encoding="utf-8")

    if dry_run:
        print("[dry-run]", " ".join(cmd))
        return prefix, {"condition": name, "dry_run": True, "command": cmd}

    print(f"\n=== Running condition: {name} ===")
    print(" ".join(cmd))
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log_path.write_text(proc.stdout, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(
            f"Condition {name!r} failed with exit code {proc.returncode}. "
            f"See {log_path}"
        )

    summary_path = prefix.with_name(prefix.name + "_summary.json")
    if not summary_path.exists():
        raise FileNotFoundError(f"Expected summary not found: {summary_path}")
    summary = read_json(summary_path)
    summary["condition"] = name
    summary["command"] = cmd
    summary["stdout_stderr_log"] = str(log_path)
    return prefix, summary


def extract_lift(summary: Mapping[str, Any], key: str) -> Dict[str, Optional[float]]:
    lift = summary.get("paired_log_loss_lift", {}).get(key, {})
    return {
        "mean": maybe_float(lift.get("mean")),
        "se": maybe_float(lift.get("se")),
        "ci95_low": maybe_float(lift.get("ci95_low")),
        "ci95_high": maybe_float(lift.get("ci95_high")),
    }


def extract_control(summary: Mapping[str, Any], key: str) -> Dict[str, Optional[float]]:
    control = summary.get("negative_control_degradation", {}).get(key, {})
    return {
        "mean": maybe_float(control.get("mean_log_loss_degradation_vs_full")),
        "se": maybe_float(control.get("se")),
        "ci95_low": maybe_float(control.get("ci95_low")),
        "ci95_high": maybe_float(control.get("ci95_high")),
    }


def flatten_condition_summary(name: str, summary: Mapping[str, Any]) -> Dict[str, Any]:
    edge = extract_lift(summary, "full_vs_edge")
    bag = extract_lift(summary, "full_vs_bag")
    private = extract_lift(summary, "full_vs_private_flat")
    b0 = extract_lift(summary, "full_vs_b0")
    target = extract_control(summary, "control_target_shuffle")
    access = extract_control(summary, "control_access_shuffle")
    temporal = extract_control(summary, "control_temporal_reverse")
    pressure = extract_control(summary, "control_pressure_shuffle")

    return {
        "condition": name,
        "n_records": summary.get("n_records"),
        "n_train": summary.get("n_train"),
        "n_test": summary.get("n_test"),
        "lift_full_vs_b0_mean": b0["mean"],
        "lift_full_vs_edge_mean": edge["mean"],
        "lift_full_vs_edge_ci95_low": edge["ci95_low"],
        "lift_full_vs_edge_ci95_high": edge["ci95_high"],
        "lift_full_vs_private_flat_mean": private["mean"],
        "lift_full_vs_bag_mean": bag["mean"],
        "lift_full_vs_bag_ci95_low": bag["ci95_low"],
        "lift_full_vs_bag_ci95_high": bag["ci95_high"],
        "ncd_pressure_shuffle_mean": pressure["mean"],
        "ncd_access_shuffle_mean": access["mean"],
        "ncd_temporal_reverse_mean": temporal["mean"],
        "ncd_target_shuffle_mean": target["mean"],
    }


def svg_bar_chart(
    path: Path,
    title: str,
    labels: Sequence[str],
    values: Sequence[Optional[float]],
    ylabel: str,
    width: int = 960,
    height: int = 520,
) -> None:
    """Write a simple dependency-free SVG bar chart."""
    clean_values = [0.0 if v is None else float(v) for v in values]
    max_abs = max([abs(v) for v in clean_values] + [1e-9])
    margin_left = 110
    margin_right = 40
    margin_top = 70
    margin_bottom = 120
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    zero_y = margin_top + plot_h / 2
    scale = (plot_h / 2) / max_abs
    n = max(1, len(labels))
    slot = plot_w / n
    bar_w = slot * 0.55

    def esc(s: str) -> str:
        return (
            str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width/2}" y="32" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" font-weight="700">{esc(title)}</text>',
        f'<text x="24" y="{height/2}" transform="rotate(-90 24 {height/2})" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">{esc(ylabel)}</text>',
        f'<line x1="{margin_left}" y1="{zero_y:.2f}" x2="{width-margin_right}" y2="{zero_y:.2f}" stroke="#333" stroke-width="1.2"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#333" stroke-width="1.2"/>',
    ]

    for i, (label, value) in enumerate(zip(labels, clean_values)):
        x = margin_left + i * slot + (slot - bar_w) / 2
        y = zero_y - max(value, 0) * scale
        h = abs(value) * scale
        if value < 0:
            y = zero_y
        fill = "#4C78A8" if value >= 0 else "#E45756"
        parts.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{h:.2f}" fill="{fill}" opacity="0.9"/>')
        parts.append(f'<text x="{x+bar_w/2:.2f}" y="{height-margin_bottom+24}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{esc(label)}</text>')
        parts.append(f'<text x="{x+bar_w/2:.2f}" y="{(y-8 if value >= 0 else y+h+18):.2f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12">{value:.4f}</text>')

    parts.append(f'<text x="{margin_left-10}" y="{margin_top+4}" text-anchor="end" font-family="Arial, sans-serif" font-size="11">{max_abs:.4f}</text>')
    parts.append(f'<text x="{margin_left-10}" y="{zero_y+4}" text-anchor="end" font-family="Arial, sans-serif" font-size="11">0</text>')
    parts.append(f'<text x="{margin_left-10}" y="{height-margin_bottom+4}" text-anchor="end" font-family="Arial, sans-serif" font-size="11">-{max_abs:.4f}</text>')
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts), encoding="utf-8")


def build_figures(outdir: Path, table_rows: Sequence[Mapping[str, Any]]) -> Dict[str, str]:
    figures_dir = outdir / "figures"
    full_row = next((r for r in table_rows if r.get("condition") == "full"), None)
    if full_row is None and table_rows:
        full_row = table_rows[0]

    paths: Dict[str, str] = {}
    if full_row:
        lift_labels = ["vs edge", "vs private", "vs bag"]
        lift_values = [
            maybe_float(full_row.get("lift_full_vs_edge_mean")),
            maybe_float(full_row.get("lift_full_vs_private_flat_mean")),
            maybe_float(full_row.get("lift_full_vs_bag_mean")),
        ]
        path = figures_dir / "prediction_lift_full.svg"
        svg_bar_chart(path, "Dot-field held-out log-loss lift", lift_labels, lift_values, "Log-loss lift")
        paths["prediction_lift_full_svg"] = str(path)

        control_labels = ["pressure", "access", "temporal", "target"]
        control_values = [
            maybe_float(full_row.get("ncd_pressure_shuffle_mean")),
            maybe_float(full_row.get("ncd_access_shuffle_mean")),
            maybe_float(full_row.get("ncd_temporal_reverse_mean")),
            maybe_float(full_row.get("ncd_target_shuffle_mean")),
        ]
        path2 = figures_dir / "negative_control_degradation.svg"
        svg_bar_chart(path2, "Negative-control degradation vs aligned full model", control_labels, control_values, "Log-loss degradation")
        paths["negative_control_degradation_svg"] = str(path2)

    ablation_rows = [r for r in table_rows if r.get("condition") != "full"]
    if ablation_rows:
        labels = [str(r["condition"]).replace("no_", "no\n") for r in ablation_rows]
        values = [maybe_float(r.get("lift_full_vs_edge_mean")) for r in ablation_rows]
        path3 = figures_dir / "ablation_lift_by_condition.svg"
        svg_bar_chart(path3, "Prediction lift under mechanism ablations", labels, values, "Log-loss lift vs edge")
        paths["ablation_lift_by_condition_svg"] = str(path3)

    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Dot-Trace Theory Experiment 1: prediction lift")
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG), help="Path to JSON experiment config")
    parser.add_argument("--out", type=str, default="results/experiment_01", help="Output directory")
    parser.add_argument("--quick", action="store_true", help="Use fast settings for local sanity checks")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them")
    parser.add_argument("--conditions", nargs="*", default=None, help="Optional subset of conditions to run")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = (REPO_ROOT / config_path).resolve()
    config = read_json(config_path)

    base_config = dict(config.get("base", {}))
    if args.quick:
        quick = config.get("quick_overrides", {})
        base_config.update(quick)

    condition_configs: Dict[str, Dict[str, Any]] = dict(config.get("conditions", {}))
    if args.conditions:
        wanted = set(args.conditions)
        condition_configs = {k: v for k, v in condition_configs.items() if k in wanted}
        missing = wanted - set(condition_configs)
        if missing:
            raise SystemExit(f"Unknown requested condition(s): {', '.join(sorted(missing))}")

    outdir = Path(args.out)
    if not outdir.is_absolute():
        outdir = (REPO_ROOT / outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    manifest: Dict[str, Any] = {
        "experiment": "Experiment 1: Dot-field prediction lift in a synthetic social memory system",
        "config_path": str(config_path),
        "output_directory": str(outdir),
        "quick": bool(args.quick),
        "dry_run": bool(args.dry_run),
        "base_config": base_config,
        "conditions": list(condition_configs.keys()),
    }

    summaries: Dict[str, Any] = {}
    table_rows: List[Dict[str, Any]] = []

    for name, condition in condition_configs.items():
        _, summary = run_condition(name, condition, base_config, outdir, dry_run=args.dry_run)
        summaries[name] = summary
        if not args.dry_run:
            table_rows.append(flatten_condition_summary(name, summary))

    if args.dry_run:
        write_json(outdir / "experiment_01_dry_run_manifest.json", manifest)
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return

    table_path = outdir / "paper_results_table.csv"
    write_csv(table_path, table_rows)

    figure_paths = build_figures(outdir, table_rows)

    aggregate = {
        **manifest,
        "paper_results_table": str(table_path),
        "figures": figure_paths,
        "summaries": {
            name: {
                "n_records": s.get("n_records"),
                "n_train": s.get("n_train"),
                "n_test": s.get("n_test"),
                "paired_log_loss_lift": s.get("paired_log_loss_lift"),
                "negative_control_degradation": s.get("negative_control_degradation"),
                "files": s.get("files"),
            }
            for name, s in summaries.items()
        },
    }
    summary_path = outdir / "experiment_01_summary.json"
    write_json(summary_path, aggregate)

    print("\nExperiment 1 complete.")
    print(f"Summary: {summary_path}")
    print(f"Paper table: {table_path}")
    for name, path in figure_paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
