"""Score a completed stage log against BATADAL ground truth.

Groups a stage's window-calls by (model, coords, replicate), reconstructs each run's
window_results by re-slicing the source dataset for timestamps, and reports hourly
P/R/F1, detection latency, and the S_TTD/S_CLF/S composites (Ch.4 §4.6).

    python -m harness.evaluate --stage 0
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from harness.run import load_config, real_windows
from harness.batadal import load_attack_windows, hourly_ground_truth
from harness.score import score


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True)
    ap.add_argument("--config", default="config/experiment.yaml")
    args = ap.parse_args()
    cfg = load_config(args.config)

    attacks = load_attack_windows(cfg["inputs"]["labels"])
    # Row order is preserved across variants, so the native window_id -> timestamps
    # map aligns obfuscated runs too (the label-safe key backs this).
    df_wins = real_windows(cfg, "native")
    tsmap_native = {w.window_id: w.timestamps for w in df_wins}
    all_ts = [t for w in df_wins for t in w.timestamps]
    import pandas as pd
    labels = hourly_ground_truth(pd.DataFrame({"DATETIME": all_ts}), "DATETIME", attacks)

    logpath = f"runs/stage{args.stage}.jsonl"
    groups = defaultdict(list)
    with open(logpath) as f:
        for line in f:
            r = json.loads(line)
            groups[(r["model"], r["coords"], r["replicate"])].append(r)

    print(f"{'model':<16}{'coords':<28}{'rep':>3}  {'F1':>5} {'S_CLF':>6} {'S_TTD':>6} {'S':>5}  det")
    for (model, coords, rep), rows in sorted(groups.items()):
        wr = [{"timestamps": tsmap_native.get(r["window_id"], []),
               "flagged_offsets": r.get("flagged_offsets", [])} for r in rows]
        s = score(wr, labels, attacks)
        h, c, l = s["hourly"], s["composite"], s["latency"]
        print(f"{model:<16}{coords:<28}{rep:>3}  {h['f1']:>5} {c['S_CLF']:>6} "
              f"{c['S_TTD']:>6} {c['S']:>5}  {l['attacks_detected']}/{l['n_attacks']}")


if __name__ == "__main__":
    main()
