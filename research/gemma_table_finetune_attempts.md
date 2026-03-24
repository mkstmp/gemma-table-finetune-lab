# Gemma 270M Fine-Tuning Attempts

## Goal

Fine-tune `google/gemma-3-270m-it` so queries like `table of 17` produce the full multiplication table from `1` to `10`.

## Attempt 1: Prompt-only Gemma

- Result: not sufficient
- What happened:
  - Base Gemma sometimes returned incomplete or off-format output.
  - Prompted Gemma improved formatting slightly, but still failed capability-level correctness.
- Example:
  - Query: `table of 17`
  - Observed failure modes: only the header, generic text, or no valid table lines.
- Conclusion:
  - Fine-tuning is justified. Prompting alone is not reliable enough.

## Attempt 2: MLX / MLX-LM local fine-tuning on Apple Silicon

- Result: blocked
- What I tried:
  - Created `.venv-gemma`
  - Installed `mlx`, `mlx-lm`, and `datasets`
- Error:
  - Importing `mlx` immediately crashed with native Metal initialization failure:
  - `NSRangeException: *** -[__NSArray0 objectAtIndex:]: index 0 beyond bounds for empty array`
- What I changed:
  - Switched away from MLX to a PyTorch + PEFT LoRA workflow.
- Conclusion:
  - On this Mac and current MLX stack, MLX is not stable enough for the fine-tune run.

## Attempt 3: PyTorch + PEFT LoRA environment

- Result: setup completed
- What I tried:
  - Installed `torch`, `accelerate`, `peft`, `datasets`, `transformers`
  - Added a LoRA training script in `assistant_platform/gemma_table/train.py`
  - Added dataset generation in `assistant_platform/gemma_table/training_data.py`
- Findings:
  - Imports work in `.venv-gemma`
  - `torch.backends.mps.is_available()` is `False`
- What that means:
  - Training would run on CPU unless GPU support is made available some other way.

## Attempt 4: Download Gemma weights from Hugging Face

- Result: blocked
- What I tried:
  - Attempted to download `config.json` from `google/gemma-3-270m-it`
- Error:
  - `401 Unauthorized`
  - `GatedRepoError: Access to model google/gemma-3-270m-it is restricted`
- What is needed:
  - Hugging Face login or token on this machine with access to Gemma
- Conclusion:
  - This is the current hard blocker for the actual fine-tune run.

## Attempt 5: Authenticated PyTorch + PEFT LoRA fine-tune

- Result: success
- What I tried:
  - Used the provided Hugging Face token to access `google/gemma-3-270m-it`
  - Ran a 1-epoch LoRA fine-tune with:
    - batch size `1`
    - gradient accumulation `4`
    - max length `192`
- First error:
  - `TrainingArguments.__init__() got an unexpected keyword argument 'overwrite_output_dir'`
- Fix:
  - Removed `overwrite_output_dir` from the script because the installed `transformers` API does not accept it.
- Final training result:
  - `train_loss`: about `0.044`
  - `eval_loss`: about `0.032`
  - adapter saved to `/Users/mukesh/assistant2/research/models/gemma-table-lora-run1`
- Validation sample:
  - Query: `table of 17`
  - Output: exact full multiplication table

## Attempt 6: Fine-tuned inference validation

- Result: partial success
- What I tried:
  - Loaded the saved LoRA adapter on top of `google/gemma-3-270m-it`
  - Tested `table of 17`, `table of 9`, and `what is 2+3`
- Outcome:
  - `table of 17`: exact success
  - `table of 9`: exact success
  - `what is 2+3`: overfit behavior, model tried to turn it into a table-style answer
- Conclusion:
  - Fine-tuning succeeded for the target behavior.
  - The adapter is specialized and not a good general-purpose replacement for unrestricted math queries.

## What is implemented now

- Side-by-side UI for Original vs New model path
- Evaluator that checks exact match, formatting, and arithmetic
- Synthetic SFT dataset generator for `table of N`
- LoRA training script for Gemma
- Workflow runner that benchmarks first and only trains if needed

## Current blocker summary

1. Apple MLX crashed, so the working path is PyTorch + PEFT.
2. MPS is not available here, so local training falls back to CPU on this machine.
3. The fine-tuned adapter is task-specialized and overfits non-table prompts, so it should be used only for the intended table-of-N workflow unless we broaden the dataset and training objective.
