"""BATADAL ingest + ground-truth labels. Ported from the original ingest.py and
score.py (label side). Carries the dayfirst=True timestamp fix. Agent/registry-
validation machinery dropped; only what the zero-shot harness needs is kept."""
from __future__ import annotations
from pathlib import Path
import pandas as pd


def ingest(path):
    """Load a BATADAL CSV, coerce the timestamp column with dayfirst=True, sort.
    Returns (df, ts_col, numeric_cols, binary_cols)."""
    df = pd.read_csv(path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    ts_col = next((c for c in df.columns
                   if any(k in c.lower() for k in ("time", "date", "datetime", "ts"))), None)
    if ts_col:
        df[ts_col] = pd.to_datetime(df[ts_col], format="%d/%m/%y %H", errors="coerce")   # the fix
        df = df.sort_values(ts_col).reset_index(drop=True)
    numeric, binary = [], []
    for c in df.columns:
        if c == ts_col or c.lower() == "row_id":
            continue
        s = df[c].dropna()
        if s.empty:
            continue
        if set(s.unique()).issubset({0, 1, True, False, 0.0, 1.0}):
            binary.append(c)
        elif pd.api.types.is_numeric_dtype(df[c]):
            numeric.append(c)
    return df, ts_col, numeric, binary


def load_attack_windows(labels_path):
    """Parse a BATADAL attack-list CSV into attack intervals. Ported verbatim in
    logic from score.py::load_attack_windows."""
    df = pd.read_csv(labels_path)
    df.columns = [c.strip() for c in df.columns]
    start_col = next(c for c in df.columns if "Starting" in c or "Start" in c)
    end_col   = next(c for c in df.columns if "Ending" in c or "End" in c)
    id_col    = next(c for c in df.columns if c.strip() == "ID")
    desc_col  = next((c for c in df.columns if "Description" in c), None)
    out = []
    for _, row in df.iterrows():
        try:
            start = pd.to_datetime(str(row[start_col]).strip(), dayfirst=True)
            end   = pd.to_datetime(str(row[end_col]).strip(),   dayfirst=True)
            out.append({
                "id": int(row[id_col]), "start": start, "end": end,
                "duration_h": int((end - start).total_seconds() / 3600),
                "description": str(row[desc_col]).strip() if desc_col else "",
            })
        except Exception as e:
            print(f"[batadal] skipped attack row: {e}")
    return out


def hourly_ground_truth(df, ts_col, attack_windows):
    """Return a dict {timestamp -> 0/1} for every row, 1 inside any attack interval."""
    labels = {}
    for ts in df[ts_col]:
        lab = 0
        for w in attack_windows:
            if w["start"] <= ts <= w["end"]:
                lab = 1
                break
        labels[ts] = lab
    return labels
