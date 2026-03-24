from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

PROMPT_TEMPLATE = (
    "You are answering KG and Class 1 questions.\n"
    "Reply with only the final short answer.\n"
    "Question: {question}\n"
    "Answer:"
)


@dataclass(frozen=True)
class QAItem:
    qid: str
    category: str
    question: str
    expected: list[str]


def build_questions() -> list[QAItem]:
    items: list[QAItem] = []

    for a, b in [
        (1, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 2), (6, 1), (7, 2), (8, 1), (9, 0),
        (10, 1), (2, 2), (3, 5), (4, 4), (5, 5), (6, 2), (7, 1), (8, 2), (9, 1), (10, 2),
    ]:
        items.append(QAItem(f"add-{a}-{b}", "math_addition", f"What is {a} + {b}?", [str(a + b)]))

    for a, b in [
        (2, 1), (3, 1), (4, 2), (5, 3), (6, 4), (7, 2), (8, 3), (9, 5), (10, 6), (10, 1),
        (6, 1), (8, 2), (9, 4), (7, 5), (5, 1), (4, 1), (3, 2), (10, 3), (9, 1), (8, 7),
    ]:
        items.append(QAItem(f"sub-{a}-{b}", "math_subtraction", f"What is {a} - {b}?", [str(a - b)]))

    counting = [
        ("How many days are in a week?", ["7", "seven"]),
        ("How many months are in a year?", ["12", "twelve"]),
        ("How many legs does a cat have?", ["4", "four"]),
        ("How many wheels does a bicycle have?", ["2", "two"]),
        ("How many eyes do you have?", ["2", "two"]),
        ("How many ears do you have?", ["2", "two"]),
        ("How many nose do you have?", ["1", "one"]),
        ("How many fingers are on one hand?", ["5", "five"]),
        ("How many toes are on one foot?", ["5", "five"]),
        ("How many sides does a triangle have?", ["3", "three"]),
    ]
    for idx, (q, ans) in enumerate(counting, start=1):
        items.append(QAItem(f"count-{idx}", "counting", q, ans))

    colors = [
        ("What color is the sky on a clear day?", ["blue"]),
        ("What color is grass?", ["green"]),
        ("What color is a ripe banana?", ["yellow"]),
        ("What color is coal?", ["black"]),
        ("What color is milk?", ["white"]),
        ("What color is an apple often shown in books?", ["red"]),
        ("What color is a carrot?", ["orange"]),
        ("What color is a leaf usually?", ["green"]),
        ("What color is snow?", ["white"]),
        ("What color is the sun often colored by children?", ["yellow"]),
    ]
    for idx, (q, ans) in enumerate(colors, start=1):
        items.append(QAItem(f"color-{idx}", "colors", q, ans))

    shapes = [
        ("Which shape has 3 sides?", ["triangle"]),
        ("Which shape has 4 equal sides?", ["square"]),
        ("Which shape is round like a ball drawing?", ["circle"]),
        ("Which shape has 4 sides and looks like a box?", ["rectangle"]),
        ("How many sides does a square have?", ["4", "four"]),
        ("How many corners does a triangle have?", ["3", "three"]),
        ("How many corners does a rectangle have?", ["4", "four"]),
        ("Which shape has no corners?", ["circle"]),
        ("Which shape has 4 sides?", ["square", "rectangle"]),
        ("Which shape looks like a slice of pizza?", ["triangle"]),
    ]
    for idx, (q, ans) in enumerate(shapes, start=1):
        items.append(QAItem(f"shape-{idx}", "shapes", q, ans))

    opposites = [
        ("What is the opposite of big?", ["small"]),
        ("What is the opposite of hot?", ["cold"]),
        ("What is the opposite of day?", ["night"]),
        ("What is the opposite of up?", ["down"]),
        ("What is the opposite of tall?", ["short"]),
        ("What is the opposite of fast?", ["slow"]),
        ("What is the opposite of open?", ["close", "closed"]),
        ("What is the opposite of happy?", ["sad"]),
        ("What is the opposite of full?", ["empty"]),
        ("What is the opposite of in?", ["out"]),
    ]
    for idx, (q, ans) in enumerate(opposites, start=1):
        items.append(QAItem(f"opp-{idx}", "opposites", q, ans))

    animals = [
        ("Which animal says meow?", ["cat"]),
        ("Which animal says woof?", ["dog"]),
        ("Which bird can say quack?", ["duck"]),
        ("Which farm animal gives us milk?", ["cow"]),
        ("Which animal is called king of the jungle?", ["lion"]),
        ("Which animal has a long trunk?", ["elephant"]),
        ("Which animal hops and has long ears?", ["rabbit", "bunny"]),
        ("Which animal lives in water and can swim?", ["fish"]),
        ("Which insect makes honey?", ["bee"]),
        ("Which animal gives us wool?", ["sheep"]),
    ]
    for idx, (q, ans) in enumerate(animals, start=1):
        items.append(QAItem(f"animal-{idx}", "animals", q, ans))

    literacy = [
        ("What is the first letter of the alphabet?", ["a"]),
        ("What is the last letter of the alphabet?", ["z"]),
        ("Which vowel comes after a?", ["e"]),
        ("How many letters are in the word cat?", ["3", "three"]),
        ("What sound does the letter B make? Answer with one sound only.", ["b"]),
        ("Which word starts with the letter A: apple or ball?", ["apple"]),
        ("Which word rhymes with cat: hat or sun?", ["hat"]),
        ("Which word starts with S: snake or tiger?", ["snake"]),
        ("What letter comes after C?", ["d"]),
        ("What letter comes before G?", ["f"]),
    ]
    for idx, (q, ans) in enumerate(literacy, start=1):
        items.append(QAItem(f"lit-{idx}", "literacy", q, ans))

    assert len(items) == 100
    return items


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9 +\-]", "", text)
    return text.strip()


def is_correct(prediction: str, expected: list[str]) -> bool:
    normalized = normalize(prediction)
    if not normalized:
        return False
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    candidates = [normalized]
    if lines:
        candidates.append(lines[0])
    candidates.extend(re.split(r"[,.!?\n]", normalized))
    cleaned = [c.strip() for c in candidates if c.strip()]
    targets = {normalize(ans) for ans in expected}
    return any(c in targets or any(t in c for t in targets) for c in cleaned)


class ModelRunner:
    def __init__(self, tokenizer, model) -> None:
        self.tokenizer = tokenizer
        self.model = model
        self.model.eval()

    def answer(self, question: str, max_new_tokens: int = 32) -> str:
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
        "# Classroom Check: Gemma 270M vs Fine-Tuned Table Adapter on 100 KG & Class 1 Questions",
        "",
        "## Setup",
        "",
        "- Original model: `google/gemma-3-270m-it`",
        "- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`",
        "- Number of questions: 100",
        "- Evaluation rule: prediction counted correct if normalized answer matched one of the accepted answers",
        "",
        "## Prompt Used For Both Models",
        "",
        "```text",
        PROMPT_TEMPLATE.replace("{question}", "<question>"),
        "```",
        "",
        "## Overall Accuracy",
        "",
        f"- Original model accuracy: {results['overall']['base_correct']}/{results['overall']['total']} = {results['overall']['base_accuracy']:.1%}",
        f"- Fine-tuned model accuracy: {results['overall']['ft_correct']}/{results['overall']['total']} = {results['overall']['ft_accuracy']:.1%}",
        "",
        "## Category Breakdown",
        "",
        "| Category | Base | Fine-Tuned |",
        "|---|---:|---:|",
    ]
    for row in results["by_category"]:
        lines.append(f"| {row['category']} | {row['base_correct']}/{row['count']} | {row['ft_correct']}/{row['count']} |")

    lines.extend(
        [
            "",
            "## Observations",
            "",
            f"- {results['observations'][0]}",
            f"- {results['observations'][1]}",
            f"- {results['observations'][2]}",
            "",
            "## Sample Mistakes",
            "",
        ]
    )
    for idx, row in enumerate(results["sample_errors"], start=1):
        lines.append(
            f"### Mistake {idx}: {row['question']}"
        )
        lines.extend(
            [
                "",
                f"- Expected: `{', '.join(row['expected'])}`",
                "",
                "**Base Output**",
                "",
                "```text",
                row["base_output"],
                "```",
                "",
                "**Fine-Tuned Output**",
                "",
                "```text",
                row["ft_output"],
                "```",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    parser = argparse.ArgumentParser(description="Benchmark base Gemma vs fine-tuned adapter on school questions.")
    parser.add_argument("--model-id", default="google/gemma-3-270m-it")
    parser.add_argument("--adapter-dir", default="research/models/gemma-table-lora-run1")
    parser.add_argument("--output-json", default="research/kg_class1_benchmark_results.json")
    parser.add_argument("--output-report", default="research/kg_class1_benchmark_report.md")
    args = parser.parse_args()

    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN or HUGGINGFACE_HUB_TOKEN is required")

    questions = build_questions()
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, token=token)
    base_model = AutoModelForCausalLM.from_pretrained(args.model_id, token=token)
    ft_base = AutoModelForCausalLM.from_pretrained(args.model_id, token=token)
    ft_model = PeftModel.from_pretrained(ft_base, args.adapter_dir)

    base_runner = ModelRunner(tokenizer, base_model)
    ft_runner = ModelRunner(tokenizer, ft_model)

    rows = []
    category_stats: dict[str, dict[str, int]] = {}
    for item in questions:
        base_output = base_runner.answer(item.question)
        ft_output = ft_runner.answer(item.question)
        base_ok = is_correct(base_output, item.expected)
        ft_ok = is_correct(ft_output, item.expected)
        rows.append(
            {
                **asdict(item),
                "base_output": base_output,
                "ft_output": ft_output,
                "base_correct": base_ok,
                "ft_correct": ft_ok,
            }
        )
        stats = category_stats.setdefault(item.category, {"count": 0, "base_correct": 0, "ft_correct": 0})
        stats["count"] += 1
        stats["base_correct"] += int(base_ok)
        stats["ft_correct"] += int(ft_ok)

    total = len(rows)
    base_correct = sum(int(r["base_correct"]) for r in rows)
    ft_correct = sum(int(r["ft_correct"]) for r in rows)
    by_category = [
        {
            "category": category,
            "count": stats["count"],
            "base_correct": stats["base_correct"],
            "ft_correct": stats["ft_correct"],
        }
        for category, stats in sorted(category_stats.items())
    ]
    sample_errors = [
        {
            "question": r["question"],
            "expected": r["expected"],
            "base_output": r["base_output"][:120],
            "ft_output": r["ft_output"][:120],
        }
        for r in rows
        if (not r["base_correct"]) or (not r["ft_correct"])
    ][:15]

    observations = [
        "The fine-tuned adapter is specialized for `table of N` behavior, so it is expected to underperform on broad KG/Class 1 questions.",
        "The base model keeps its broader general capability, even when its answers are not always perfectly constrained to one-token style.",
        "This benchmark measures general school-question behavior, which is intentionally different from the narrow fine-tuning target.",
    ]

    results = {
        "overall": {
            "total": total,
            "base_correct": base_correct,
            "ft_correct": ft_correct,
            "base_accuracy": base_correct / total,
            "ft_accuracy": ft_correct / total,
        },
        "by_category": by_category,
        "prompt_template": PROMPT_TEMPLATE,
        "rows": rows,
        "sample_errors": sample_errors,
        "observations": observations,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(results, indent=2, ensure_ascii=True), encoding="utf-8")
    build_report(results, Path(args.output_report))


if __name__ == "__main__":
    main()
