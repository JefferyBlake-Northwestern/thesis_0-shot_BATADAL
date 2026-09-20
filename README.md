# Zero-Shot LLM Anomaly Detection on BATADAL

Experimental harness, results, and reasoning traces for an MS thesis at
Northwestern University (CIS 590), evaluating three current-generation
frontier LLMs (Anthropic Opus 5, OpenAI GPT-5.6 Sol, xAI Grok 4) on the
BATADAL water distribution attack detection benchmark under a three-condition
data authenticity design.

**Thesis:** [Title], Jeffery Blake, Northwestern University, 2026.

---

## Repository contents

```
harness/                  Python execution harness
├── prompt.py             Frozen prompt template (domain framing + JSON contract)
├── client.py             Model-agnostic client (Anthropic, OpenAI, xAI)
├── run.py                Cell enumeration and run loop
├── runlog.py             JSONL logging with provenance capture
├── windows.py            24-hour window slicing and rendering
├── batadal.py            BATADAL ingest and ground-truth alignment
├── obfuscate.py          Contamination-control transform
├── parse.py              JSON output-contract parser
└── score_run.py          Hourly-granularity scoring and composites

config/experiment.yaml    Frozen center point + staged design
runs/stage1.jsonl         Definitive Stage 1 evaluation log (2,376 rows)
runs/stage9.jsonl         Schema-preserved probe log
reasoning_samples.md      108-trace representative catalog (Appendix B)
scripts/                  Analysis scripts for thesis figures
monitor.sh                Interactive menu for running scripts/*.sh
requirements.txt          Pinned Python dependencies
LICENSE                   MIT
```

## Data files (not distributed)

The BATADAL benchmark dataset is not redistributed in this repository to
preserve the original dataset's separate licensing terms. To reproduce the
Stage 1 evaluation, obtain the dataset directly from the source and regenerate
the transformed variants using the obfuscation harness.

**Native dataset:**

Download the BATADAL test dataset and attack-list files from the source paper's
supplemental materials:

> Taormina, R., Galelli, S., Tippenhauer, N. O., Salomons, E., Ostfeld, A.,
> et al. (2018). The battle of the attack detection algorithms: Disclosing
> cyber attacks on water distribution networks. *Journal of Water Resources
> Planning and Management, 144*(8). DOI: 10.1061/(ASCE)WR.1943-5452.0000969

Place the files in a `data/` directory at the repository root:

```
data/
├── BATADAL_test_dataset.csv
└── BATADAL_test_attack_list.csv
```

**Transformed variants (correlational, schema-preserved):**

Regenerate the obfuscated variants using the harness with `seed=0` (which
matches the values presented to the models during the thesis's Stage 1 run):

```bash
python -m harness.obfuscate \
    --input data/BATADAL_test_dataset.csv \
    --variant correlational \
    --out-csv data/BATADAL_test_dataset.correlational.csv \
    --key-json data/BATADAL_test_dataset.correlational.key.json \
    --seed 0

python -m harness.obfuscate \
    --input data/BATADAL_test_dataset.csv \
    --variant schema_preserved \
    --out-csv data/BATADAL_test_dataset.schema_preserved.csv \
    --key-json data/BATADAL_test_dataset.schema_preserved.key.json \
    --seed 0
```

The label-safe key files (`*.key.json`) are used only by the scoring pipeline
to align obfuscated windows back to ground-truth attack labels. They are never
shown to the models during inference.

## Reproducing Stage 1

The Stage 1 evaluation reproduced below matches the design described in
Chapter 4 of the thesis: 3 models × 3 data authenticity conditions × 3
replicates × 88 windows = 2,376 API calls.

**1. Environment setup**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.11 (tested on 3.11.15).

**2. Set provider API keys**

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export XAI_API_KEY=xai-...
```

**3. Fetch data and regenerate variants** (see "Data files" section above)

**4. Run Stage 1**

```bash
caffeinate -is python -m harness.run --stage 1 --client auto
```

Or without `caffeinate` (macOS-specific keep-alive):

```bash
python -m harness.run --stage 1 --client auto
```

Expected wall-clock time: approximately 60 hours. Anthropic accounts for the
bulk of both time and cost; Sol and Grok complete substantially faster per
call.

**5. Score results**

```bash
python -m harness.score_run --jsonl runs/stage1.jsonl \
    --model opus-5 --authenticity native

python -m harness.score_run --compare \
    runs/stage1.jsonl:opus-5:native \
    runs/stage1.jsonl:opus-5:schema_preserved \
    runs/stage1.jsonl:opus-5:obfuscated
```

## Provider API caveats

Frontier model APIs are non-deterministic and drift over time.
Current-generation flagship models do not accept explicit sampling parameters
(temperature, top-p, seed); the harness accepts these arguments for interface
compatibility but does not send them to the API. Within-cell variance across
replicates therefore reflects server-controlled sampling.

Re-execution of Stage 1 will produce results within the replicate variance
reported in the thesis but will not reproduce specific numerical values
exactly. Model versions actually served during the thesis run are recorded
in `runs/stage1.jsonl` under the `model_version` field.

Approximate cost of a full Stage 1 replication (as of September 2026):
approximately $240 for Anthropic; smaller amounts for OpenAI and xAI,
dominated by the 9 cells × 3 replicates × 88 windows call volume rather than
by per-token pricing.

## Reasoning traces

`reasoning_samples.md` contains 108 representative reasoning traces sampled
from the Stage 1 log, organized into 36 buckets by (model, condition,
confusion-matrix outcome). The catalog corresponds to Appendix B of the
thesis.

## Analysis scripts

`scripts/` contains the ad-hoc scripts used to produce the figures in
Chapter 5 and Appendix A (verdict distribution, parse rate, cell latency,
execution timeline, attack vs normal parse rate, and others). Each operates
on `runs/stage1.jsonl` and prints tab-delimited summaries.

Run individual scripts directly:

```bash
scripts/verdict_distr.sh
scripts/cell_latency.sh
```

Or use the interactive menu:

```bash
./monitor.sh
```

## License

MIT. See `LICENSE`.

The BATADAL dataset is a separate work with its own licensing terms; obtain
it directly from the source paper.

## Citation

If you use this code or reference the results, please cite:

```bibtex
@mastersthesis{blake2026zeroshot,
  author = {Blake, Jeffery},
  title  = {[Thesis title]},
  school = {Northwestern University},
  year   = {2026},
  url    = {https://github.com/JefferyBlake-Northwestern/thesis_0-shot_BATADAL}
}
```

## Contact

For questions about the thesis or replication, contact the author through
the GitHub repository issue tracker.