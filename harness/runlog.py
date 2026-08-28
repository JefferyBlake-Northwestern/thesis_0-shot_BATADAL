"""Append-only JSONL run log, one row per window-call, with idempotent resume."""
from __future__ import annotations
import json, os, hashlib


def run_id(stage, model, coords, replicate, window_id):
    key = f"{stage}|{model}|{coords}|{replicate}|{window_id}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def seen(logpath):
    ids = set()
    if os.path.exists(logpath):
        with open(logpath) as f:
            for line in f:
                try:
                    ids.add(json.loads(line)["run_id"])
                except Exception:
                    pass
    return ids


def append(logpath, row):
    os.makedirs(os.path.dirname(logpath) or ".", exist_ok=True)
    with open(logpath, "a") as f:
        f.write(json.dumps(row) + "\n")
