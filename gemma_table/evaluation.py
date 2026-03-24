from __future__ import annotations

from dataclasses import asdict, dataclass

from gemma_table.core import normalize_text, parse_table_request, render_table, TABLE_LINE_RE


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    query: str
    split: str


@dataclass
class TableEvaluation:
    query: str
    expected: str
    actual: str
    recognized: bool
    exact_match: bool
    header_ok: bool
    line_count_ok: bool
    arithmetic_ok: bool
    details: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_benchmark_cases() -> list[BenchmarkCase]:
    train_queries = [
        ("train-2-basic", "table of 2"),
        ("train-5-basic", "table of 5"),
        ("train-7-basic", "table of 7"),
        ("train-9-basic", "table of 9"),
        ("train-12-basic", "table of 12"),
        ("train-3-show", "show me table of 3"),
        ("train-8-multiplication", "multiplication table of 8"),
        ("train-11-plain", "table 11"),
    ]
    holdout_queries = [
        ("holdout-4-basic", "table of 4"),
        ("holdout-6-show", "show me the table of 6"),
        ("holdout-10-multiplication", "multiplication table of 10"),
        ("holdout-13-plain", "table 13"),
        ("holdout-15-request", "give me table of 15"),
    ]
    cases = [BenchmarkCase(case_id=case_id, query=query, split="train") for case_id, query in train_queries]
    cases.extend(BenchmarkCase(case_id=case_id, query=query, split="holdout") for case_id, query in holdout_queries)
    return cases


def evaluate_table_response(query: str, actual: str) -> TableEvaluation:
    parsed = parse_table_request(query)
    if not parsed:
        return TableEvaluation(
            query=query,
            expected="",
            actual=actual,
            recognized=False,
            exact_match=False,
            header_ok=False,
            line_count_ok=False,
            arithmetic_ok=False,
            details=["query was not recognized as a supported 'table of N' request"],
        )

    expected = render_table(parsed.value)
    normalized_actual = normalize_text(actual)
    exact_match = normalize_text(expected) == normalized_actual
    lines = normalized_actual.splitlines() if normalized_actual else []
    details: list[str] = []

    header_ok = bool(lines) and lines[0].strip() == f"Table of {parsed.value}"
    if not header_ok:
        details.append("header did not match expected format")

    table_lines = lines[1:]
    line_count_ok = len(table_lines) == 10
    if not line_count_ok:
        details.append(f"expected 10 multiplication lines, found {len(table_lines)}")

    arithmetic_ok = True
    if line_count_ok:
        for idx, line in enumerate(table_lines, start=1):
            match = TABLE_LINE_RE.match(line)
            if not match:
                arithmetic_ok = False
                details.append(f"line {idx} did not match 'N x i = result' format")
                continue
            lhs_value = int(match.group(1))
            multiplier = int(match.group(2))
            rhs_value = int(match.group(3))
            if lhs_value != parsed.value or multiplier != idx or rhs_value != parsed.value * idx:
                arithmetic_ok = False
                details.append(f"line {idx} had incorrect arithmetic")
    else:
        arithmetic_ok = False

    if exact_match:
        details.append("response matched expected output exactly")

    return TableEvaluation(
        query=query,
        expected=expected,
        actual=actual,
        recognized=True,
        exact_match=exact_match,
        header_ok=header_ok,
        line_count_ok=line_count_ok,
        arithmetic_ok=arithmetic_ok,
        details=details,
    )
