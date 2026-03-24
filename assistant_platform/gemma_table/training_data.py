from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from assistant_platform.gemma_table.core import render_table


@dataclass(frozen=True)
class SupervisedExample:
    prompt: str
    response: str
    split: str
    metadata: dict[str, object]


def build_supervised_examples(max_value: int = 50) -> list[SupervisedExample]:
    prompt_templates = [
        "table of {n}",
        "table {n}",
        "multiplication table of {n}",
        "show me table of {n}",
        "show me the table of {n}",
        "give me table of {n}",
    ]
    examples: list[SupervisedExample] = []
    for value in range(1, max_value + 1):
        split = "train" if value <= int(max_value * 0.8) else "validation"
        for template in prompt_templates:
            examples.append(
                SupervisedExample(
                    prompt=template.format(n=value),
                    response=render_table(value),
                    split=split,
                    metadata={"value": value, "template": template},
                )
            )
    return examples


def write_dataset(output_path: Path, max_value: int = 50) -> dict[str, int]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    examples = build_supervised_examples(max_value=max_value)
    counts = {"train": 0, "validation": 0}
    with output_path.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(asdict(example), ensure_ascii=True) + "\n")
            counts[example.split] += 1
    return counts
