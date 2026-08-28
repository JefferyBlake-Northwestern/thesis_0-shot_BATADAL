"""Deterministic baseline detector (the F1 anchor, Ch.4 §3.6.1 / §5.3.2).

Ported from train.py::run_deterministic. Gate set as in the source: z-score,
rate-of-change, and mutual-deviation (correlation-residual). NOTE: reconcile with
your current detector if it carries a distinct mass-balance integral gate (G4) -- the
committed run_deterministic in the old repo implements the three gates below."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd


def load_model(model_dir):
    d = Path(model_dir)
    def load(name):
        with open(d / name) as f:
            return json.load(f)
    return {
        "registry":        load("column_registry.json"),
        "baselines":       load("baselines.json"),
        "rate_baselines":  load("rate_baselines.json"),
        "correlation_map": load("correlation_map.json"),
        "thresholds":      load("thresholds.json"),
    }


def run_deterministic(df, model, ts_col):
    baselines       = model["baselines"]
    rate_baselines  = model["rate_baselines"]
    correlation_map = model["correlation_map"]
    thresholds      = model["thresholds"]
    signals = []

    for col, stats in baselines.items():
        if col not in df.columns:
            continue
        if "mean" in stats and stats.get("std"):
            z = (df[col] - stats["mean"]) / stats["std"]
            for idx in z[z.abs() > thresholds["z_score_cutoff"]].dropna().index:
                signals.append((df.at[idx, ts_col], col, "zscore"))
        if col in rate_baselines:
            limit  = rate_baselines[col]["p99_rate"] * thresholds["rate_cutoff_multiplier"]
            deltas = df[col].diff().abs()
            for idx in deltas[deltas > limit].dropna().index:
                signals.append((df.at[idx, ts_col], col, "rate"))

    mdc = thresholds["mutual_deviation_cutoff"]
    for _, pair in correlation_map.items():
        ca, cb = pair["col_a"], pair["col_b"]
        if ca not in df.columns or cb not in df.columns:
            continue
        if ca not in baselines or cb not in baselines:
            continue
        sa, sb = baselines[ca]["std"], baselines[cb]["std"]
        r = pair["pearson_r"]
        da, dbb = df[ca].diff(), df[cb].diff()
        residual = (dbb - r * da * (sb / (sa + 1e-9))).abs()
        thr = mdc * sb
        for idx in residual[residual > thr].dropna().index:
            signals.append((df.at[idx, ts_col], cb, "mutual_dev"))

    return signals   # list of (timestamp, column, gate)
