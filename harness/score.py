"""Scoring: hourly P/R/F1 (Ch.4 §4.6.1), detection latency (§4.6.2), and the BATADAL
competition composites S_TTD / S_CLF / S (§4.6.3).

Label side ported from score.py. The competition composite is implemented to the
BATADAL 2017 definition (S = 0.5*S_TTD + 0.5*S_CLF); VERIFY the constants against the
competition spec before publishing leaderboard positioning.

Input contract from the harness: a list of window results,
  {"timestamps": [...24...], "flagged_offsets": [int,...]}
where flagged_offsets index the hours the model called attack within that window.
"""
from __future__ import annotations
import numpy as np


def _predicted_positive_hours(window_results):
    pos = set()
    for wr in window_results:
        ts = wr["timestamps"]
        for off in wr.get("flagged_offsets", []):
            if 0 <= off < len(ts):
                pos.add(ts[off])
    return pos


def score(window_results, hourly_labels, attack_windows):
    covered = [ts for wr in window_results for ts in wr["timestamps"]]
    pred_pos = _predicted_positive_hours(window_results)

    tp = fp = fn = tn = 0
    for ts in covered:
        actual = hourly_labels.get(ts, 0)
        pred = 1 if ts in pred_pos else 0
        if pred and actual:   tp += 1
        elif pred:            fp += 1
        elif actual:          fn += 1
        else:                 tn += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall    = tp / (tp + fn) if tp + fn else 0.0
    f1        = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    tpr = recall
    tnr = tn / (tn + fp) if tn + fp else 0.0
    s_clf = (tpr + tnr) / 2.0

    # Per-attack detection latency + normalized delay for S_TTD.
    norm_delays, per_attack = [], []
    for w in attack_windows:
        hits = sorted(ts for ts in pred_pos if w["start"] <= ts <= w["end"])
        dur_h = max(w["duration_h"], 1)
        if hits:
            ttd_h = int((hits[0] - w["start"]).total_seconds() / 3600)
            norm_delays.append(min(ttd_h / dur_h, 1.0))
            per_attack.append({"id": w["id"], "detected": True, "ttd_h": ttd_h})
        else:
            norm_delays.append(1.0)   # undetected = maximum delay
            per_attack.append({"id": w["id"], "detected": False, "ttd_h": None})
    s_ttd = 1.0 - float(np.mean(norm_delays)) if norm_delays else 0.0
    s = 0.5 * s_ttd + 0.5 * s_clf

    detected = [a for a in per_attack if a["detected"]]
    ttds = [a["ttd_h"] for a in detected]
    return {
        "hourly": {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                    "precision": round(precision, 3), "recall": round(recall, 3),
                    "f1": round(f1, 3)},
        "latency": {"attacks_detected": len(detected), "n_attacks": len(attack_windows),
                     "mean_ttd_h": round(float(np.mean(ttds)), 1) if ttds else None},
        "composite": {"S_TTD": round(s_ttd, 3), "S_CLF": round(s_clf, 3), "S": round(s, 3)},
        "per_attack": per_attack,
    }
