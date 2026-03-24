from __future__ import annotations

import argparse
import os

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference with the fine-tuned Gemma adapter.")
    parser.add_argument("--adapter-dir", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model-id", default="google/gemma-3-270m-it")
    parser.add_argument("--max-new-tokens", type=int, default=160)
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained(args.adapter_dir, token=token)
    base = AutoModelForCausalLM.from_pretrained(args.model_id, token=token)
    model = PeftModel.from_pretrained(base, args.adapter_dir)
    model.eval()

    prompt = f"User: {args.query}\nAssistant:"
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    prefix = prompt
    if text.startswith(prefix):
        text = text[len(prefix):].lstrip()
    print(text)


if __name__ == "__main__":
    main()
