from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from gemma_table.core import render_table
from gemma_table.evaluation import evaluate_table_response


PROMPT_TEMPLATE = "User: {question}\nAssistant:"


@dataclass(frozen=True)
class TableCase:
    case_id: str
    question: str


def build_cases() -> list[TableCase]:
    prompts = [
        "table of 2",
        "table of 3",
        "table of 5",
        "table of 7",
        "table of 9",
        "table of 11",
        "table of 12",
        "table of 15",
        "table of 17",
        "table of 19",
    ]
    return [TableCase(case_id=f"table-{idx+1}", question=prompt) for idx, prompt in enumerate(prompts)]


class ModelRunner:
    def __init__(self, tokenizer, model) -> None:
        self.tokenizer = tokenizer
        self.model = model
        self.model.eval()

    def answer(self, question: str, max_new_tokens: int = 180) -> str:
        import torch

        prompt = PROMPT_TEMPLATE.format(question=question)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        if text.startswith(prompt):
            text = text[len(prompt):].lstrip()
        return text.strip()


def build_report(results: dict[str, object], output_path: Path) -> None:
    lines = [
        "# Table Mastery Check: Gemma 270M vs Fine-Tuned Table Adapter",
        "",
        "## Setup",
        "",
        "- Original model: `google/gemma-3-270m-it`",
        "- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`",
        "- Number of prompts: 10",
        "- Evaluation rule: exact table-match plus arithmetic/format validation",
        "",
        "## Prompt Used For Both Models",
        "",
        "```text",
        PROMPT_TEMPLATE.replace("{question}", "<question>"),
        "```",
        "",
        "## Overall Accuracy",
        "",
        f"- Original model exact-match accuracy: {results['overall']['base_exact_match']}/{results['overall']['total']} = {results['overall']['base_accuracy']:.1%}",
        f"- Fine-tuned model exact-match accuracy: {results['overall']['ft_exact_match']}/{results['overall']['total']} = {results['overall']['ft_accuracy']:.1%}",
        "",
        "## Case Results",
        "",
        "| Prompt | Base | Fine-Tuned |",
        "|---|---:|---:|",
    ]
    for row in results["rows"]:
        lines.append(
            f"| {row['question']} | {'PASS' if row['base_exact_match'] else 'FAIL'} | {'PASS' if row['ft_exact_match'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Sample Outputs",
            "",
        ]
    )
    for row in results["rows"][:4]:
        lines.extend(
            [
                f"### {row['question']}",
                "",
                "**Original Model**",
                "",
                "```text",
                row["base_output"],
                "```",
                "",
                "**Fine-Tuned Model**",
                "",
                "```text",
                row["ft_output"],
                "```",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    parser = argparse.ArgumentParser(description="Benchmark base Gemma vs fine-tuned adapter on 10 table prompts.")
    parser.add_argument("--model-id", default="google/gemma-3-270m-it")
    parser.add_argument("--adapter-dir", default="research/models/gemma-table-lora-run1")
    parser.add_argument("--output-json", default="research/table_benchmark_results.json")
    parser.add_argument("--output-report", default="research/table_benchmark_report.md")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN or HUGGINGFACE_HUB_TOKEN is required")

    cases = build_cases()
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, token=token)
    base_model = AutoModelForCausalLM.from_pretrained(args.model_id, token=token)
    ft_base = AutoModelForCausalLM.from_pretrained(args.model_id, token=token)
    ft_model = PeftModel.from_pretrained(ft_base, args.adapter_dir)

    base_runner = ModelRunner(tokenizer, base_model)
    ft_runner = ModelRunner(tokenizer, ft_model)

    rows = []
    for case in cases:
        base_output = base_runner.answer(case.question)
        ft_output = ft_runner.answer(case.question)
        base_eval = evaluate_table_response(case.question, base_output)
        ft_eval = evaluate_table_response(case.question, ft_output)
        rows.append(
            {
                **asdict(case),
                "expected": render_table(int(case.question.split()[-1])),
                "base_output": base_output,
                "ft_output": ft_output,
                "base_exact_match": base_eval.exact_match,
                "ft_exact_match": ft_eval.exact_match,
                "base_evaluation": base_eval.to_dict(),
                "ft_evaluation": ft_eval.to_dict(),
            }
        )

    total = len(rows)
    base_exact_match = sum(int(row["base_exact_match"]) for row in rows)
    ft_exact_match = sum(int(row["ft_exact_match"]) for row in rows)
    results = {
        "overall": {
            "total": total,
            "base_exact_match": base_exact_match,
            "ft_exact_match": ft_exact_match,
            "base_accuracy": base_exact_match / total,
            "ft_accuracy": ft_exact_match / total,
        },
        "prompt_template": PROMPT_TEMPLATE,
        "rows": rows,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(results, indent=2, ensure_ascii=True), encoding="utf-8")
    build_report(results, Path(args.output_report))


if __name__ == "__main__":
    main()
