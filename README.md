# zsl-batadal-harness

Zero-shot BATADAL benchmarking harness. Center-point-and-spokes design over four
models (Ch.4 §4.3-§4.4). One row per window-call, idempotent resume, model-agnostic
client, contamination-controlled data variants, and a scorer that emits hourly P/R/F1,
detection latency, and the BATADAL S_TTD/S_CLF/S composites.

## Pipeline
    ingest -> slice 24h windows -> prompt -> client -> parse -> log -> evaluate(score)

## Quick start
    pip install -r requirements.txt

    # 1. Mock dry-run: no key, no data, validates the whole path
    python -m harness.run --stage 0 --dry-run

    # 2. Build the obfuscated variant (contamination control, Factor D)
    python -m harness.obfuscate --input data/BATADAL_test_dataset.csv \
        --variant correlational \
        --out-csv data/BATADAL_test_dataset.correlational.csv \
        --key-json data/BATADAL_test_dataset.correlational.key.json

    # 3. Full mock run over REAL windows + score (still no key)
    python -m harness.run --stage 0 --client mock
    python -m harness.evaluate --stage 0

    # 4. Go live against Opus 5 (your key, your machine)
    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python -m harness.run --stage 0 --client anthropic
    python -m harness.evaluate --stage 0

## Data (not shipped; drop your copies in data/)
    BATADAL_test_dataset.csv          # blind test telemetry
    BATADAL_test_attack_list.csv      # ground-truth labels
    trained_model_test_labeled/       # baseline artifacts (for harness/baseline.py)

## Ported from NU_CIS590_project (clean port, agents/orchestration/ablation dropped)
    harness/batadal.py   <- ingest.py (dayfirst=True fix) + score.py label side
    harness/score.py     <- score.py TP/FP/TTD core, + hourly P/R/F1 + S_TTD/S_CLF/S
    harness/baseline.py  <- train.py::run_deterministic (z-score, rate, mutual-dev gates)
    harness/windows.py   <- 24h slicer (new) + derived features (rate-of-change, storage delta)
    harness/obfuscate.py <- RECONSTRUCTED (never committed): correlational + physics-preserving

## Reconcile before publishing
- baseline.py implements the THREE gates in the committed run_deterministic. If your
  current detector carries a distinct mass-balance integral gate (G4), port it in.
- obfuscate.py is a reconstruction of the Aug design; diff against your original if kept.
- score.py composites follow the BATADAL 2017 definition; verify constants vs the spec.
- verify model_string values in config/experiment.yaml against provider docs.

## Seams still open
- harness/prompt.py : FROZEN TEMPLATE is a placeholder (center-point decision, §4.4.1)
- harness/client.py : GoogleClient is a stub (needed for Gemini in Stages 1-4)
- reference-augmented (Factor C) : window.reference_csv not yet populated
