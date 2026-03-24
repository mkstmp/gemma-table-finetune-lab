from __future__ import annotations

import argparse
import json
from pathlib import Path


def preview(text: str, limit: int = 90) -> str:
    if not text or not text.strip():
        return "<NO_ANSWER>"
    single_line = text.replace("\n", " ↩ ").replace("|", "/").strip()
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3].rstrip() + "..."


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a full 100-row KG/Class 1 benchmark table from saved JSON.")
    parser.add_argument("--input-json", default="research/kg_class1_benchmark_results.json")
    parser.add_argument("--output-report", default="research/kg_class1_benchmark_full_table.md")
    args = parser.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    lines = [
        "# Classroom Check: Full 100-Question Table",
        "",
        "Per-row verdicts below come from the cached benchmark run in `research/kg_class1_benchmark_results.json`.",
        "",
        "| Query | Expected Answer | Base Answer | FineTunedAnswer | BaseResult | FineTuneResult |",
        "|---|---|---|---|---|---|",
    ]
    for row in data["rows"]:
        base_result = "Correct" if row.get("base_correct") else "Incorrect"
        ft_result = "Correct" if row.get("ft_correct") else "Incorrect"
        lines.append(
            f"| {row['question']} | {', '.join(row['expected'])} | {preview(row['base_output'])} | {preview(row['ft_output'])} | {base_result} | {ft_result} |"
        )

    output_path = Path(args.output_report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
