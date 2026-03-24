from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ANSWER_PROMPT_TEMPLATE = (
    "You are answering KG and Class 1 questions.\n"
    "Reply with only the final short answer.\n"
    "Question: {question}\n"
    "Answer:"
)

JUDGE_PROMPT = """You are grading student answers.
Decide if each candidate answer should count as correct for the question.

Rules:
- First isolate the answer to the original question.
- Treat the answer as the text before the first later self-generated follow-up such as a new 'Question:' line.
- If there is no later 'Question:' line, use the full candidate text.
- The expected answers list contains valid short answers.
- Only grade whether the candidate answered the original question.
- Ignore any later self-generated continuation such as extra 'Question:' or 'Answer:' lines.
- Ignore extra words if the answer to the original question is still clearly correct.
- If the answer starts correctly but then rambles, it can still be CORRECT.
- Mark INCORRECT if the answer gives the wrong value, wrong fact, or no answer.
- Be strict about factual correctness and arithmetic correctness.
- Do not judge the correctness of any later generated follow-up questions.
"""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "base_verdict": {"type": "string", "enum": ["CORRECT", "INCORRECT"]},
        "base_reason": {"type": "string"},
        "ft_verdict": {"type": "string", "enum": ["CORRECT", "INCORRECT"]},
        "ft_reason": {"type": "string"},
    },
    "required": ["base_verdict", "base_reason", "ft_verdict", "ft_reason"],
    "additionalProperties": False,
}


@dataclass
class JudgeResult:
    verdict: str
    reason: str


class OpenAIJudge:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def judge_pair(self, question: str, expected: list[str], base_answer: str, ft_answer: str) -> tuple[JudgeResult, JudgeResult]:
        base_text = base_answer.strip() or "<NO_ANSWER>"
        ft_text = ft_answer.strip() or "<NO_ANSWER>"
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": JUDGE_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\n"
                        f"Expected Answers: {', '.join(expected)}\n"
                        f"Base Candidate Answer:\n{base_text}\n\n"
                        f"Fine-Tuned Candidate Answer:\n{ft_text}"
                    ),
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "judge_pair_verdict",
                    "schema": JUDGE_SCHEMA,
                    "strict": True,
                }
            },
        }

        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        last_error: Exception | None = None
        for attempt in range(8):
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    body = json.loads(response.read().decode("utf-8"))
                text = self._extract_text(body)
                parsed = json.loads(text)
                base_verdict = parsed.get("base_verdict", "INCORRECT")
                ft_verdict = parsed.get("ft_verdict", "INCORRECT")
                if base_verdict not in {"CORRECT", "INCORRECT"}:
                    base_verdict = "INCORRECT"
                if ft_verdict not in {"CORRECT", "INCORRECT"}:
                    ft_verdict = "INCORRECT"
                return (
                    JudgeResult(verdict=base_verdict, reason=parsed.get("base_reason", "") or "no reason returned"),
                    JudgeResult(verdict=ft_verdict, reason=parsed.get("ft_reason", "") or "no reason returned"),
                )
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code == 429:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    if retry_after and retry_after.isdigit():
                        time.sleep(int(retry_after))
                    else:
                        time.sleep(min(60, 5 * (attempt + 1)))
                    continue
                time.sleep(1)
            except Exception as exc:
                last_error = exc
                time.sleep(1)
        error = f"judge_error: {last_error}"
        return (
            JudgeResult(verdict="INCORRECT", reason=error),
            JudgeResult(verdict="INCORRECT", reason=error),
        )

    @staticmethod
    def _extract_text(body: dict) -> str:
        if body.get("output_text"):
            return body["output_text"]
        for item in body.get("output", []):
            if item.get("type") != "message":
                continue
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    return content["text"]
        return ""


class GeminiJudge:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def judge_pair(self, question: str, expected: list[str], base_answer: str, ft_answer: str) -> tuple[JudgeResult, JudgeResult]:
        base_text = base_answer.strip() or "<NO_ANSWER>"
        ft_text = ft_answer.strip() or "<NO_ANSWER>"
        prompt = (
            f"{JUDGE_PROMPT}\n\n"
            f"Question: {question}\n"
            f"Expected Answers: {', '.join(expected)}\n"
            f"Base Candidate Answer:\n{base_text}\n\n"
            f"Fine-Tuned Candidate Answer:\n{ft_text}"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseJsonSchema": JUDGE_SCHEMA,
                "temperature": 0,
                "maxOutputTokens": 512,
            },
        }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(self.model, safe='')}:generateContent?key={urllib.parse.quote(self.api_key, safe='')}"
        )
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        last_error: Exception | None = None
        for attempt in range(8):
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    body = json.loads(response.read().decode("utf-8"))
                text = self._extract_text(body)
                parsed = json.loads(text)
                base_verdict = parsed.get("base_verdict", "INCORRECT")
                ft_verdict = parsed.get("ft_verdict", "INCORRECT")
                if base_verdict not in {"CORRECT", "INCORRECT"}:
                    base_verdict = "INCORRECT"
                if ft_verdict not in {"CORRECT", "INCORRECT"}:
                    ft_verdict = "INCORRECT"
                return (
                    JudgeResult(verdict=base_verdict, reason=parsed.get("base_reason", "") or "no reason returned"),
                    JudgeResult(verdict=ft_verdict, reason=parsed.get("ft_reason", "") or "no reason returned"),
                )
            except urllib.error.HTTPError as exc:
                last_error = exc
                if exc.code in {429, 529}:
                    retry_after = exc.headers.get("Retry-After") if exc.headers else None
                    if retry_after and retry_after.isdigit():
                        time.sleep(int(retry_after))
                    else:
                        time.sleep(min(60, 5 * (attempt + 1)))
                    continue
                time.sleep(1)
            except Exception as exc:
                last_error = exc
                time.sleep(1)
        error = f"judge_error: {last_error}"
        return (
            JudgeResult(verdict="INCORRECT", reason=error),
            JudgeResult(verdict="INCORRECT", reason=error),
        )

    @staticmethod
    def _extract_text(body: dict) -> str:
        candidates = body.get("candidates", [])
        for candidate in candidates:
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                if part.get("text"):
                    return part["text"]
        return ""


def build_report(results: dict[str, object], output_path: Path) -> None:
    def preview(text: str, limit: int = 90) -> str:
        if not text or not text.strip():
            return "<NO_ANSWER>"
        single_line = text.replace("\n", " ↩ ").replace("|", "/").strip()
        if len(single_line) <= limit:
            return single_line
        return single_line[: limit - 3].rstrip() + "..."

    lines = [
        "# Classroom Check: Gemma 270M vs Fine-Tuned Table Adapter on 100 KG & Class 1 Questions",
        "",
        "## Setup",
        "",
        "- Original model: `google/gemma-3-270m-it`",
        "- Fine-tuned model: `google/gemma-3-270m-it` + LoRA adapter `gemma-table-lora-run1`",
        f"- Judge model: `{results['judge_model']}` via OpenAI Responses API",
        "- Number of questions: 100",
        "- Evaluation rule: external LLM judge decides whether each answer is correct",
        "",
        "## Prompt Used For Answering",
        "",
        "```text",
        ANSWER_PROMPT_TEMPLATE.replace("{question}", "<question>"),
        "```",
        "",
        "## Prompt Used For Judging",
        "",
        "```text",
        JUDGE_PROMPT,
        "",
        "Question: <question>",
        "Expected Answers: <expected_answers>",
        "Base Candidate Answer:",
        "<base_model_answer>",
        "",
        "Fine-Tuned Candidate Answer:",
        "<fine_tuned_model_answer>",
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
            "## Sample Errors",
            "",
            "| Query | Expected Answer | Base Answer | Fine-Tuned Answer | Base Result | Fine-Tuned Result |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in results["sample_errors"]:
        lines.append(
            f"| {row['question']} | {', '.join(row['expected'])} | {preview(row['base_output'])} | {preview(row['ft_output'])} | {row['base_result']} | {row['ft_result']} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_results(rows: list[dict[str, object]], judge_model: str) -> dict[str, object]:
    category_stats: dict[str, dict[str, int]] = {}
    for row in rows:
        stats = category_stats.setdefault(row["category"], {"count": 0, "base_correct": 0, "ft_correct": 0})
        stats["count"] += 1
        stats["base_correct"] += int(bool(row["base_correct"]))
        stats["ft_correct"] += int(bool(row["ft_correct"]))

    total = len(rows)
    base_correct = sum(int(bool(r["base_correct"])) for r in rows)
    ft_correct = sum(int(bool(r["ft_correct"])) for r in rows)
    by_category = [
        {
            "category": category,
            "count": stats["count"],
            "base_correct": stats["base_correct"],
            "ft_correct": stats["ft_correct"],
        }
        for category, stats in sorted(category_stats.items())
    ]
    sample_errors: list[dict[str, object]] = []
    seen_questions: set[str] = set()
    grouped_errors: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        if row["base_correct"] and row["ft_correct"]:
            continue
        grouped_errors.setdefault(row["category"], []).append(row)

    for category in sorted(grouped_errors):
        for row in grouped_errors[category][:2]:
            sample_errors.append(
                {
                    "question": row["question"],
                    "expected": row["expected"],
                    "base_output": row["base_output"],
                    "ft_output": row["ft_output"],
                    "base_result": "Correct" if row["base_correct"] else "Incorrect",
                    "ft_result": "Correct" if row["ft_correct"] else "Incorrect",
                }
            )
            seen_questions.add(row["question"])

    if len(sample_errors) < 15:
        for row in rows:
            if row["base_correct"] and row["ft_correct"]:
                continue
            if row["question"] in seen_questions:
                continue
            sample_errors.append(
                {
                    "question": row["question"],
                    "expected": row["expected"],
                    "base_output": row["base_output"],
                    "ft_output": row["ft_output"],
                    "base_result": "Correct" if row["base_correct"] else "Incorrect",
                    "ft_result": "Correct" if row["ft_correct"] else "Incorrect",
                }
            )
            seen_questions.add(row["question"])
            if len(sample_errors) >= 15:
                break

    sample_errors = sample_errors[:15]
    return {
        "overall": {
            "total": total,
            "base_correct": base_correct,
            "ft_correct": ft_correct,
            "base_accuracy": (base_correct / total) if total else 0.0,
            "ft_accuracy": (ft_correct / total) if total else 0.0,
        },
        "by_category": by_category,
        "judge_model": judge_model,
        "rows": rows,
        "sample_errors": sample_errors,
    }


def has_judge_error(row: dict[str, object]) -> bool:
    return str(row.get("base_judge", {}).get("reason", "")).startswith("judge_error:") or str(
        row.get("ft_judge", {}).get("reason", "")
    ).startswith("judge_error:")


def main() -> None:
    parser = argparse.ArgumentParser(description="Use an external LLM judge to re-score the saved school benchmark outputs.")
    parser.add_argument("--input-json", default="research/kg_class1_benchmark_results.json")
    parser.add_argument("--output-json", default="research/kg_class1_benchmark_results_llm_judged.json")
    parser.add_argument("--output-report", default="research/kg_class1_benchmark_report_llm_judged.md")
    parser.add_argument("--judge-provider", choices=["openai", "gemini"], default="gemini")
    parser.add_argument("--judge-model", default="gemini-2.5-flash")
    parser.add_argument("--max-workers", type=int, default=1)
    parser.add_argument("--delay-seconds", type=float, default=2.0)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if args.judge_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        judge = OpenAIJudge(api_key=api_key, model=args.judge_model)
    else:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is required")
        judge = GeminiJudge(api_key=api_key, model=args.judge_model)

    source = json.loads(Path(args.input_json).read_text(encoding="utf-8"))

    rows: list[dict[str, object] | None] = [None] * len(source["rows"])
    total_rows = len(source["rows"])
    output_json = Path(args.output_json)
    output_report = Path(args.output_report)
    existing_by_qid: dict[str, dict[str, object]] = {}
    if args.resume and output_json.exists():
        existing = json.loads(output_json.read_text(encoding="utf-8"))
        existing_by_qid = {row["qid"]: row for row in existing.get("rows", []) if "qid" in row}

    def judge_one(index: int, row: dict[str, object]) -> tuple[int, dict[str, object]]:
        base_judge, ft_judge = judge.judge_pair(row["question"], row["expected"], row["base_output"], row["ft_output"])
        base_ok = base_judge.verdict == "CORRECT"
        ft_ok = ft_judge.verdict == "CORRECT"
        updated = {
            **row,
            "base_correct": base_ok,
            "ft_correct": ft_ok,
            "base_judge": {"verdict": base_judge.verdict, "reason": base_judge.reason},
            "ft_judge": {"verdict": ft_judge.verdict, "reason": ft_judge.reason},
        }
        return index, updated

    completed = 0
    for index, row in enumerate(source["rows"]):
        existing_row = existing_by_qid.get(row["qid"])
        if existing_row and not has_judge_error(existing_row):
            rows[index] = existing_row
            completed += 1
            print(f"[{completed}/{total_rows}] kept {row['qid']} base={existing_row['base_judge']['verdict']} ft={existing_row['ft_judge']['verdict']}", flush=True)
            continue

        index, updated = judge_one(index, row)
        rows[index] = updated
        completed += 1
        committed_rows = [committed for committed in rows if committed is not None]
        results = build_results(committed_rows, args.judge_model)
        output_json.write_text(json.dumps(results, indent=2, ensure_ascii=True), encoding="utf-8")
        build_report(results, output_report)
        print(
            f"[{completed}/{total_rows}] judged {updated['qid']} base={updated['base_judge']['verdict']} ft={updated['ft_judge']['verdict']}",
            flush=True,
        )
        if args.delay_seconds > 0:
            time.sleep(args.delay_seconds)


if __name__ == "__main__":
    main()
