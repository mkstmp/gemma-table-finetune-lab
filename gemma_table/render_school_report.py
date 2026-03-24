from __future__ import annotations

import argparse
import json
from pathlib import Path

from gemma_table.school_benchmark import build_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-render the KG/Class 1 benchmark report from saved JSON.")
    parser.add_argument("--input-json", default="research/kg_class1_benchmark_results.json")
    parser.add_argument("--output-report", default="research/kg_class1_benchmark_report.md")
    args = parser.parse_args()

    data = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    build_report(data, Path(args.output_report))


if __name__ == "__main__":
    main()
