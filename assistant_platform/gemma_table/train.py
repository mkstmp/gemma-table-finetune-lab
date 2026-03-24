from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

from assistant_platform.gemma_table.research import ResearchLog
from assistant_platform.gemma_table.training_data import write_dataset


PROMPT_TEMPLATE = "User: {prompt}\nAssistant:"


@dataclass(frozen=True)
class ScriptConfig:
    model_id: str
    dataset_path: Path
    output_dir: Path
    workspace_root: Path
    num_train_epochs: int
    learning_rate: float
    per_device_train_batch_size: int
    gradient_accumulation_steps: int
    max_length: int


def load_jsonl(path: Path, split: str) -> Dataset:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item["split"] == split:
            rows.append(item)
    return Dataset.from_list(rows)


def choose_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def tokenize_dataset(dataset: Dataset, tokenizer: AutoTokenizer, max_length: int) -> Dataset:
    def transform(example: dict[str, object]) -> dict[str, object]:
        prompt = PROMPT_TEMPLATE.format(prompt=example["prompt"])
        response = str(example["response"])
        full_text = f"{prompt}\n{response}{tokenizer.eos_token or ''}"
        prompt_tokens = tokenizer(prompt, add_special_tokens=False)
        full_tokens = tokenizer(
            full_text,
            add_special_tokens=True,
            truncation=True,
            max_length=max_length,
        )
        prompt_length = min(len(prompt_tokens["input_ids"]), len(full_tokens["input_ids"]))
        labels = list(full_tokens["input_ids"])
        labels[:prompt_length] = [-100] * prompt_length
        return {
            "input_ids": full_tokens["input_ids"],
            "attention_mask": full_tokens["attention_mask"],
            "labels": labels,
        }

    return dataset.map(transform, remove_columns=dataset.column_names)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune Gemma 270M for 'table of N' prompts.")
    parser.add_argument("--model-id", default="google/gemma-3-270m-it")
    parser.add_argument("--dataset-path", default="research/data/gemma_table_sft.jsonl")
    parser.add_argument("--output-dir", default="research/models/gemma-table-lora")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--num-train-epochs", type=int, default=3)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--per-device-train-batch-size", type=int, default=1)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=256)
    args = parser.parse_args()

    config = ScriptConfig(
        model_id=args.model_id,
        dataset_path=Path(args.dataset_path),
        output_dir=Path(args.output_dir),
        workspace_root=Path(args.workspace_root).resolve(),
        num_train_epochs=args.num_train_epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.per_device_train_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        max_length=args.max_length,
    )

    research = ResearchLog(config.workspace_root / "research")
    counts = write_dataset(config.dataset_path, max_value=50)
    research.record(
        title="Synthetic SFT dataset generated",
        category="data",
        status="success",
        summary="Prepared supervised prompt/response pairs for table-of-N fine-tuning.",
        details={"dataset_path": str(config.dataset_path), **counts},
    )

    device = choose_device()
    research.record(
        title="Training device selected",
        category="training",
        status="success",
        summary="Selected training device for Gemma LoRA run.",
        details={"device": device},
    )

    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained(config.model_id, token=token)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(config.model_id, token=token)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "up_proj", "down_proj", "gate_proj"],
    )
    model = get_peft_model(model, lora_config)
    if device != "cpu":
        model = model.to(device)

    train_dataset = tokenize_dataset(load_jsonl(config.dataset_path, "train"), tokenizer, config.max_length)
    eval_dataset = tokenize_dataset(load_jsonl(config.dataset_path, "validation"), tokenizer, config.max_length)

    training_args = TrainingArguments(
        output_dir=str(config.output_dir),
        num_train_epochs=config.num_train_epochs,
        learning_rate=config.learning_rate,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="epoch",
        report_to=[],
        remove_unused_columns=False,
        use_cpu=(device == "cpu"),
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()
    trainer.save_model(str(config.output_dir))
    tokenizer.save_pretrained(str(config.output_dir))
    research.record(
        title="Gemma LoRA training completed",
        category="training",
        status="success",
        summary="Saved LoRA adapter and tokenizer for the table-of-N specialization.",
        details={"output_dir": str(config.output_dir), "model_id": config.model_id},
    )
    research.publish_report()


if __name__ == "__main__":
    main()
