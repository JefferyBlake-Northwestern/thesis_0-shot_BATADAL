"""Cell enumeration + run loop + logging.

Dry-run uses the mock client and synthetic windows to validate the whole path with no
key and no real data. Live runs swap in the real client and load windows from disk.

    python -m harness.run --stage 0 --dry-run           # mock, no key
    python -m harness.run --stage 0 --client anthropic   # live (needs ANTHROPIC_API_KEY)
"""
from __future__ import annotations
import argparse, itertools, subprocess, time, yaml
from harness.client import get_client
from harness.prompt import build_prompt
from harness.parse import parse_response
from harness import windows as W
from harness.batadal import ingest
from harness.runlog import run_id, seen, append


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def get_prompt_sha():
    """Return short git SHA, appended with '-dirty' if there are uncommitted
    changes, or 'unknown' if not in a git repo. Called once per stage run."""
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return f"{sha}-dirty" if dirty else sha
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"

def enumerate_cells(cfg, stage):
    s = cfg["stages"][stage]
    cp = cfg["center_point"]
    grids = dict(
        model=s["models"],
        A=s.get("framing", [cp["framing"]]),
        B=s.get("representation", [cp["representation"]]),
        C=s.get("reference", [cp["reference"]]),
        D=s.get("authenticity", cp["authenticity"]),
        rep=range(cfg["experiment"]["replicates"]),
    )
    keys = list(grids)
    for combo in itertools.product(*grids.values()):
        yield dict(zip(keys, combo))



_WIN_CACHE = {}

def real_windows(cfg, authenticity):
    """Ingest the configured CSV for this authenticity and slice into 24h windows.
    Cached so a stage ingests each dataset once, not once per cell."""
    if authenticity not in _WIN_CACHE:
        key = {"native": "native_csv",
               "obfuscated": "obfuscated_csv",
               "schema_preserved": "schema_preserved_csv"}[authenticity]
        src = cfg["inputs"][key]
        df, ts, num, bina = ingest(src)
        _WIN_CACHE[authenticity] = W.slice_windows(
            df, ts, num, bina, cfg["experiment"]["window_hours"], authenticity)
    return _WIN_CACHE[authenticity]


def run_stage(stage, client_name, dry=False, config_path="config/experiment.yaml"):
    cfg = load_config(config_path)
    mlu = {m["id"]: m for m in cfg["models"]}
    logpath = f"runs/stage{stage}.jsonl"
    done = seen(logpath)
    temp = cfg["experiment"]["temperature"]
    prompt_sha = get_prompt_sha()
    n_calls = n_ok = n_skip = 0

    for cell in enumerate_cells(cfg, stage):
        mrec = mlu[cell["model"]]
        kind = "mock" if dry else (mrec["client"] if client_name == "auto" else client_name)
        c = get_client(kind)
        wins = W.synth_windows(2, cell["D"]) if dry else real_windows(cfg, cell["D"])
        for win in wins:
            coords = f"{cell['A']}-{cell['B']}-{cell['C']}-{cell['D']}"
            rid = run_id(stage, cell["model"], coords, cell["rep"], win.window_id)
            if rid in done:
                n_skip += 1
                continue
            system, user = build_prompt(win, cell["A"], cell["B"], cell["C"])
            comp = c.complete(system, user, mrec["model_string"], temp)
            pr = parse_response(comp.text)
            append(logpath, {
                "run_id": rid, "stage": stage, "model": cell["model"],
                "model_version": comp.model_version, "coords": coords,
                "replicate": cell["rep"], "window_id": win.window_id,
                "authenticity": cell["D"], "verdict": pr.verdict,
                "flagged_offsets": pr.flagged_hours, "parse_ok": pr.ok,
                "latency_s": round(comp.latency_s, 3), "ts": round(time.time(), 3),
                "prompt_sha": prompt_sha,
                "response_text": comp.text,
                "response_stop_reason": (comp.raw.get("stop_reason") if isinstance(comp.raw, dict) else None),
                "response_output_tokens": (comp.raw.get("usage", {}).get("output_tokens") if isinstance(comp.raw, dict) else None),
            })
            n_calls += 1
            n_ok += int(pr.ok)
    return {"stage": stage, "calls": n_calls, "parsed_ok": n_ok,
            "skipped_resume": n_skip, "log": logpath,
            "prompt_sha": prompt_sha}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, required=True)
    ap.add_argument("--client", default="auto")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--config", default="config/experiment.yaml")
    args = ap.parse_args()
    result = run_stage(args.stage, args.client, dry=args.dry_run, config_path=args.config)
    print("DRY-RUN OK" if args.dry_run else "RUN COMPLETE")
    for k, v in result.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
