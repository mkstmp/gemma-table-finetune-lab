from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ExperimentRecord:
    timestamp: str
    title: str
    category: str
    status: str
    summary: str
    details: dict[str, Any]


class ResearchLog:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.events_path = self.root / "gemma_table_experiments.jsonl"
        self.report_path = self.root / "gemma_table_research.md"

    def record(self, title: str, category: str, status: str, summary: str, details: dict[str, Any]) -> None:
        sanitized_details = {key: self._sanitize_value(value) for key, value in details.items()}
        entry = ExperimentRecord(
            timestamp=datetime.now().astimezone().isoformat(timespec="seconds"),
            title=title,
            category=category,
            status=status,
            summary=summary,
            details=sanitized_details,
        )
        if self._is_duplicate(entry):
            return
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(entry), ensure_ascii=True) + "\n")

    def _sanitize_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {key: self._sanitize_value(inner) for key, inner in value.items()}
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, str) and len(value) > 600:
            return value[:600] + "... [truncated]"
        return value

    def _is_duplicate(self, entry: ExperimentRecord) -> bool:
        if not self.events_path.exists():
            return False
        lines = self.events_path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return False
        last = json.loads(lines[-1])
        return (
            last.get("title") == entry.title
            and last.get("category") == entry.category
            and last.get("status") == entry.status
            and last.get("summary") == entry.summary
            and last.get("details") == entry.details
        )

    def publish_report(self) -> str:
        lines = [
            "# Gemma 270M Table-of-N Workflow Research",
            "",
            "This report is generated from the local experiment log.",
            "",
        ]
        if self.events_path.exists():
            records = [
                json.loads(line)
                for line in self.events_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
        else:
            records = []
        if not records:
            lines.append("No experiments recorded yet.")
        else:
            for record in records:
                lines.append(f"## {record['title']}")
                lines.append(f"- Time: {record['timestamp']}")
                lines.append(f"- Category: {record['category']}")
                lines.append(f"- Status: {record['status']}")
                lines.append(f"- Summary: {record['summary']}")
                details = record.get("details") or {}
                if details:
                    lines.append("- Details:")
                    for key, value in details.items():
                        lines.append(f"  - {key}: {value}")
                lines.append("")
        report = "\n".join(lines).rstrip() + "\n"
        self.report_path.write_text(report, encoding="utf-8")
        return report
