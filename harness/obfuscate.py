"""Contamination-control transform (Ch.4 §4.3.4).

NOTE: obfuscate_batadal.py was produced in design and never committed to the old repo,
so this is a faithful RECONSTRUCTION of that design, not a line port. Reconcile with
your original script if you kept it.

Two variants:
  correlational    -- per-column affine y = a*x + b (a>0). Defeats value recall and
                      benchmark recognition; preserves temporal shape and pairwise
                      Pearson correlation (affine maps leave r unchanged).
  physics_preserving -- one positive scale per UNIT GROUP (L_/F_/P_ prefixes), so
                      within-group ratios -- and the storage/mass-balance relations
                      among like-unit quantities -- survive. Weaker de-identification.

Both: rename columns to opaque tokens, shuffle column order, shift the calendar, and
strip DATETIME semantics from the model-facing frame. A label-safe key (row_id ->
original timestamp, plus the column-name map) is written SEPARATELY so the scorer can
re-align; it never enters the model-facing CSV.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd


def _unit_group(col):
    for p in ("L_", "F_", "P_", "S_"):
        if col.upper().startswith(p):
            return p
    return "OTHER"


def obfuscate(df, ts_col, numeric, binary, variant="correlational", seed=0):
    rng = np.random.default_rng(seed)
    out = df.copy()

    if variant == "correlational":
        for c in numeric:
            a = float(rng.uniform(0.5, 2.0))
            b = float(rng.uniform(-5.0, 5.0))
            out[c] = a * out[c] + b
    elif variant == "schema_preserved":
        for c in numeric:
            a = float(rng.uniform(0.5, 2.0))
            b = float(rng.uniform(-5.0, 5.0))
            out[c] = a * out[c] + b
    elif variant == "physics_preserving":
        groups = {g: float(rng.uniform(0.5, 2.0))
                  for g in {_unit_group(c) for c in numeric}}
        for c in numeric:
            out[c] = groups[_unit_group(c)] * out[c]
    else:
        raise ValueError(f"unknown variant: {variant}")

    # Binary/status columns pass through unscaled (scaling 0/1 would corrupt them).

    # Calendar shift + strip original timestamp semantics.
    key = {"variant": variant, "seed": seed, "row_timestamps": {}, "column_map": {}}
    if ts_col:
        shift = pd.Timedelta(hours=int(rng.integers(1000, 9000)))
        shifted = out[ts_col] + shift
        for i, ts in enumerate(df[ts_col]):
            key["row_timestamps"][str(i)] = str(ts)      # true label alignment
        out[ts_col] = range(len(out))                    # opaque row index, model-facing
        out = out.rename(columns={ts_col: "row_id"})

    # Opaque column renaming + shuffle (numeric + binary only).
    # Skipped for schema_preserved: column names are the recognition channel
    # we deliberately leave open in that variant.
    if variant != "schema_preserved":
        data_cols = numeric + binary
        tokens = [f"col_{i:04d}" for i in range(len(data_cols))]
        rng.shuffle(tokens)
        colmap = dict(zip(data_cols, tokens))
        key["column_map"] = {v: k for k, v in colmap.items()}
        out = out.rename(columns=colmap)
        shuffled = list(rng.permutation([c for c in out.columns if c != "row_id"]))
        order = (["row_id"] if "row_id" in out.columns else []) + shuffled
        out = out[order]
    return out, key

    data_cols = numeric + binary
    tokens = [f"col_{i:04d}" for i in range(len(data_cols))]
    rng.shuffle(tokens)
    colmap = dict(zip(data_cols, tokens))
    key["column_map"] = {v: k for k, v in colmap.items()}   # token -> original
    out = out.rename(columns=colmap)
    shuffled = list(rng.permutation([c for c in out.columns if c != "row_id"]))
    order = (["row_id"] if "row_id" in out.columns else []) + shuffled
    out = out[order]
    return out, key


def write_variant(df, ts_col, numeric, binary, out_csv, key_json, variant="correlational", seed=0):
    obf, key = obfuscate(df, ts_col, numeric, binary, variant, seed)
    obf.to_csv(out_csv, index=False)
    with open(key_json, "w") as f:
        json.dump(key, f, indent=2)
    return out_csv, key_json


if __name__ == "__main__":
    import argparse
    from harness.batadal import ingest
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--variant", default="correlational",
                    choices=["correlational", "schema_preserved", "physics_preserving"])
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--key-json", required=True)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    df, ts, num, bina = ingest(a.input)
    write_variant(df, ts, num, bina, a.out_csv, a.key_json, a.variant, a.seed)
    print(f"[obfuscate] {a.variant} -> {a.out_csv}  (key -> {a.key_json})")
