"""Score a run's JSONL against BATADAL ground truth.

Bridges the per-row model responses in runs/*.jsonl to score.py's P/R/F1 and
BATADAL composite metrics (S, S_TTD, S_CLF). Groups by replicate; unparseable
rows contribute empty flags (conservative: missed attacks count as FN).

For obfuscated / schema_preserved authenticities, translates window row indices
back to real DATETIME values via the .key.json produced during obfuscation, so
scoring aligns to the native ground truth labels.

Usage — single cell:
    python -m harness.score_run --jsonl runs/stage9.jsonl \\
        --model opus-5 --authenticity schema_preserved

Usage — three-way comparison for the advisor meeting:
    python -m harness.score_run --compare \\
        runs/stage0.jsonl:opus-5:native \\
        runs/stage9.jsonl:opus-5:schema_preserved \\
        runs/stage0.jsonl:opus-5:obfuscated
"""
from __future__ import annotations
import argparse
import json
from statistics import mean, stdev

import pandas as pd
import yaml

from harness.batadal import ingest, load_attack_windows, hourly_ground_truth
from harness.windows import slice_windows
from harness.score import score


AUTH_TO_CSV_KEY = {
    "native":            "native_csv",
    "obfuscated":        "obfuscated_csv",
    "schema_preserved":  "schema_preserved_csv",
}


def load_config(path="config/experiment.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def _key_json_path(csv_path):
    return str(csv_path).replace(".csv", ".key.json")


def build_windows(cfg, authenticity, window_hours=24):
    """Slice the source CSV into windows with real DATETIME timestamps.
    For obfuscated variants, translates row indices via the key JSON so the
    scorer can align flagged offsets to the native ground truth."""
    csv_path = cfg["inputs"][AUTH_TO_CSV_KEY[authenticity]]
    df, ts_col, numeric, binary = ingest(csv_path)
    windows = slice_windows(df, ts_col, numeric, binary, window_hours, authenticity)
    if authenticity != "native":
        with open(_key_json_path(csv_path)) as f:
            row_ts = {int(k): pd.to_datetime(v)
                      for k, v in json.load(f)["row_timestamps"].items()}
        for w in windows:
            w.timestamps = [row_ts.get(int(t), t) for t in w.timestamps]
    return windows


def load_labels(cfg):
    """Ground truth lives on native timestamps; load once and reuse."""
    df, ts_col, _, _ = ingest(cfg["inputs"]["native_csv"])
    attacks = load_attack_windows(cfg["inputs"]["labels"])
    labels = hourly_ground_truth(df, ts_col, attacks)
    return labels, attacks


def _dig(obj, path):
    for p in path:
        obj = obj[p]
    return obj


def score_condition(jsonl_path, model_id, authenticity, cfg=None, window_hours=24):
    """Score one (model, authenticity) cell, aggregating across replicates."""
    if cfg is None:
        cfg = load_config()

    rows = []
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r["model"] == model_id and r["authenticity"] == authenticity:
                rows.append(r)
    if not rows:
        return {"error": f"no rows matching model={model_id}, auth={authenticity} in {jsonl_path}"}

    windows = build_windows(cfg, authenticity, window_hours)
    win_by_id = {w.window_id: w for w in windows}
    labels, attacks = load_labels(cfg)

    parse_ok = sum(1 for r in rows if r["parse_ok"])
    parse_rate = parse_ok / len(rows)

    by_rep = {}
    for r in rows:
        by_rep.setdefault(r["replicate"], []).append(r)

    per_rep = {}
    for rep, rep_rows in sorted(by_rep.items()):
        window_results = []
        for r in rep_rows:
            w = win_by_id.get(r["window_id"])
            if w is None:
                continue
            flags = (r.get("flagged_offsets") or []) if r["parse_ok"] else []
            window_results.append({"timestamps": w.timestamps, "flagged_offsets": flags})
        per_rep[rep] = score(window_results, labels, attacks)

    def agg(path):
        vals = [_dig(s, path) for s in per_rep.values()]
        return {"mean":  round(mean(vals), 3),
                "stdev": round(stdev(vals), 3) if len(vals) > 1 else 0,
                "n":     len(vals)}

    aggregate = {
        "f1":                agg(["hourly", "f1"]),
        "precision":         agg(["hourly", "precision"]),
        "recall":            agg(["hourly", "recall"]),
        "S":                 agg(["composite", "S"]),
        "S_TTD":             agg(["composite", "S_TTD"]),
        "S_CLF":             agg(["composite", "S_CLF"]),
        "attacks_detected":  agg(["latency", "attacks_detected"]),
    }
    return {
        "cell": {
            "jsonl":         str(jsonl_path),
            "model":         model_id,
            "authenticity":  authenticity,
            "n_rows":        len(rows),
            "parse_rate":    round(parse_rate, 3),
            "n_replicates":  len(per_rep),
        },
        "aggregate": aggregate,
        "per_replicate": {str(k): v for k, v in per_rep.items()},
    }


def compare(cells, cfg=None):
    if cfg is None:
        cfg = load_config()
    return [score_condition(*c.split(":"), cfg=cfg) for c in cells]


def print_table(results):
    hdr = f"{'condition':32s} {'parse':>7s} {'F1':>16s} {'S':>16s} {'S_CLF':>16s} {'S_TTD':>16s} {'atks/7':>7s}"
    print(hdr)
    print("-" * len(hdr))
    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['error']}")
            continue
        c, a = r["cell"], r["aggregate"]
        label = f"{c['authenticity']} ({c['model']})"
        fmt = lambda k: f"{a[k]['mean']:.3f} ± {a[k]['stdev']:.3f}"
        print(f"{label:32s} {c['parse_rate']:>7.3f} {fmt('f1'):>16s} {fmt('S'):>16s} "
              f"{fmt('S_CLF'):>16s} {fmt('S_TTD'):>16s} {a['attacks_detected']['mean']:>7.1f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", help="Score one cell from this JSONL")
    ap.add_argument("--model", default="opus-5")
    ap.add_argument("--authenticity",
                    choices=list(AUTH_TO_CSV_KEY.keys()))
    ap.add_argument("--compare", nargs="+", metavar="JSONL:MODEL:AUTH",
                    help="Compare cells across multiple JSONLs")
    a = ap.parse_args()
    if a.compare:
        results = compare(a.compare)
        print_table(results)
        print("\nFull results:")
        print(json.dumps(results, indent=2, default=str))
    elif a.jsonl and a.authenticity:
        r = score_condition(a.jsonl, a.model, a.authenticity)
        print(json.dumps(r, indent=2, default=str))
    else:
        ap.error("provide --jsonl + --authenticity, or --compare")


if __name__ == "__main__":
    main()
