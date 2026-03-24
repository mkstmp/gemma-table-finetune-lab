# Gemma Table Fine-Tuning Lab

This workspace contains:

- a FastAPI UI for comparing the original Gemma model and the fine-tuned solution
- a LoRA fine-tuning workflow for `google/gemma-3-270m-it`
- benchmark scripts for:
  - narrow target-task evaluation on `table of N`
  - broader KG/Class 1 evaluation
- research reports and experiment logs

## Main paths

- App entrypoint: `app.py`
- Gemma workflow code: `gemma_table`
- Research outputs: `research`

## Run locally

### Base app

```bash
cd /Users/mukesh/assistant2
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic pyyaml python-dateutil
uvicorn app:app --reload
```

Open:

- `http://127.0.0.1:8000/gemma-table`

### Fine-tune environment

```bash
cd /Users/mukesh/assistant2
python3 -m venv .venv-gemma
source .venv-gemma/bin/activate
pip install --upgrade pip setuptools wheel
pip install mlx mlx-lm datasets accelerate peft torch transformers
```

Set your Hugging Face token before model download or training:

```bash
export HF_TOKEN=...
```

## Fine-tune

```bash
cd /Users/mukesh/assistant2
HF_TOKEN=... .venv-gemma/bin/python -m gemma_table.train \
  --workspace-root . \
  --num-train-epochs 1 \
  --per-device-train-batch-size 1 \
  --gradient-accumulation-steps 4 \
  --max-length 192 \
  --output-dir research/models/gemma-table-lora-run1
```

## Benchmarks

### Table benchmark

```bash
HF_TOKEN=... .venv-gemma/bin/python -m gemma_table.table_benchmark
```

### KG/Class 1 benchmark

```bash
HF_TOKEN=... .venv-gemma/bin/python -m gemma_table.school_benchmark
```

## Hosting summary

- Google Cloud VM: best option for this project
- Hugging Face Spaces: possible, but gated model access and heavier dependencies make it less convenient
- GitHub: good for code hosting only, not model inference hosting

See `research/deployment_options.md` for deployment notes.
