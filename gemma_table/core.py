from __future__ import annotations

import re
from dataclasses import dataclass

TABLE_QUERY_RE = re.compile(
    r"\b(?:(?:what\s+is|show|give|tell)\s+me\s+)?(?:the\s+)?(?:multiplication\s+)?table(?:\s+of)?\s+(-?\d+)\b",
    re.IGNORECASE,
)
TABLE_LINE_RE = re.compile(r"^\s*(-?\d+)\s*x\s*(\d+)\s*=\s*(-?\d+)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class TableRequest:
    value: int
    query: str


def parse_table_request(query: str) -> TableRequest | None:
    match = TABLE_QUERY_RE.search(query.strip())
    if not match:
        return None
    return TableRequest(value=int(match.group(1)), query=query)


def render_table(value: int) -> str:
    lines = [f"Table of {value}"]
    for multiplier in range(1, 11):
        lines.append(f"{value} x {multiplier} = {value * multiplier}")
    return "\n".join(lines)


def expected_output_for_query(query: str) -> str | None:
    parsed = parse_table_request(query)
    if not parsed:
        return None
    return render_table(parsed.value)


def normalize_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())
