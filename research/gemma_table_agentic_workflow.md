# Gemma Table-of-N Agentic Workflow

## Purpose

This workflow first proves whether the base model already solves the task. It only fine-tunes when the benchmark shows a real gap.

## Agents

### 1. Probe Agent

- Sends benchmark prompts to the base model.
- Uses variants like:
  - `table of 5`
  - `table 7`
  - `multiplication table of 12`
  - `show me the table of 17`

### 2. Judge Agent

- Parses the model output.
- Checks:
  - correct header
  - exactly 10 multiplication lines
  - correct arithmetic on each line
  - exact-match success

### 3. Decision Agent

- Reads benchmark scores.
- If base model passes the threshold, stops and recommends no fine-tuning.
- If base model fails, triggers dataset generation and training.

### 4. Data Builder Agent

- Generates supervised prompt/response pairs for `table of N`.
- Produces train/validation data.
- Keeps the target output fixed and exact.

### 5. Trainer Agent

- Loads Gemma weights.
- Applies LoRA to attention and MLP projection modules.
- Runs SFT on the synthetic dataset.
- Saves adapters and tokenizer output.

### 6. Regression Agent

- Re-runs the same benchmark against:
  - original base model
  - prompted model
  - fine-tuned model
- Verifies the fine-tuned model did not just learn one or two tables.

### 7. Report Agent

- Publishes:
  - setup used
  - commands executed
  - failures encountered
  - fixes applied
  - benchmark before/after results

## Current implementation in this workspace

- Benchmark and evaluator:
  - `assistant_platform/gemma_table/evaluation.py`
- Side-by-side service:
  - `assistant_platform/gemma_table/service.py`
- UI route:
  - `assistant_platform/api/routes_gemma_table.py`
- Dataset generator:
  - `assistant_platform/gemma_table/training_data.py`
- LoRA training script:
  - `assistant_platform/gemma_table/train.py`
- Workflow runner:
  - `assistant_platform/gemma_table/run_workflow.py`

## Why this scales to 3B

The structure stays the same for `gemma-3-3b-it`:

1. swap the model ID
2. keep the same judge and benchmark
3. regenerate or reuse the same synthetic dataset
4. increase memory-aware training settings
5. compare before/after on the same evaluation set

The key point is that the benchmark and judge are model-size agnostic, so the workflow can be reused directly.
