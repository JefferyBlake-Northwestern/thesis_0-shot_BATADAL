"""Window loading and feature rendering.

Two modes:
  synth_windows()   -> throwaway windows for the mock dry-run (no data/key needed).
  slice_windows()   -> real, non-overlapping 24h windows sliced from an ingested
                       BATADAL df, each carrying its wall-clock hours so the scorer
                       can align flagged offsets back to timestamps.

Feature construction (render) ports the derived quantities the design calls for:
per-column rate-of-change and an aggregate tank-storage delta (a mass-balance proxy;
SEAM: replace with true C-Town topology if you want the exact hydraulic identity).
Labels are NEVER placed in the model-facing matrix -- they travel beside the window.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import pandas as pd


@dataclass
class Window:
    window_id: str
    authenticity: str
    timestamps: list            # wall-clock hour timestamps, len == n rows
    rows: list                  # list of {col -> value}, model-facing telemetry only
    numeric: list = field(default_factory=list)
    binary: list = field(default_factory=list)
    reference_csv: Optional[str] = None

    def render(self, representation="raw") -> str:
        if not self.rows:
            return ""
        base_cols = list(self.rows[0].keys())
        frame = pd.DataFrame(self.rows)
        if representation == "raw":
            out = frame[base_cols]
        else:
            derived = {}
            for c in self.numeric:
                derived[f"d_{c}"] = frame[c].diff().fillna(0).round(4)
            level_cols = [c for c in self.numeric if c.upper().startswith("L_")]
            if level_cols:
                derived["storage_delta"] = frame[level_cols].diff().sum(axis=1).fillna(0).round(4)
            dframe = pd.DataFrame(derived)
            if representation == "derived_only":
                out = dframe
            else:  # raw_derived
                out = pd.concat([frame[base_cols], dframe], axis=1)
        head = ",".join(out.columns)
        body = "\n".join(",".join(str(v) for v in row) for row in out.itertuples(index=False))
        return f"{head}\n{body}"


def slice_windows(df, ts_col, numeric, binary, window_hours=24, authenticity="native"):
    """Non-overlapping consecutive windows of `window_hours` rows."""
    model_cols = numeric + binary
    windows = []
    n = len(df)
    for i, start in enumerate(range(0, n, window_hours)):
        chunk = df.iloc[start:start + window_hours]
        if chunk.empty:
            continue
        rows = [{c: chunk.iloc[j][c] for c in model_cols} for j in range(len(chunk))]
        stamps = list(chunk[ts_col]) if ts_col else list(range(start, start + len(chunk)))
        windows.append(Window(
            window_id=f"w{i:04d}",
            authenticity=authenticity,
            timestamps=stamps,
            rows=rows, numeric=numeric, binary=binary,
        ))
    return windows


def synth_windows(n=2, authenticity="native"):
    out = []
    for i in range(n):
        rows = [{"L_T1": round(3.1 + h * 0.01, 3),
                 "P_J280": round(40.0 - h * 0.02, 3),
                 "S_PU1": h % 2} for h in range(24)]
        out.append(Window(f"synth_{authenticity}_{i}", authenticity,
                           list(range(24)), rows, numeric=["L_T1", "P_J280"], binary=["S_PU1"]))
    return out
