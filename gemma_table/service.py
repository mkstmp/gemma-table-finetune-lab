from __future__ import annotations

import importlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from gemma_table.backends import (
    Backend,
    FineTuneSupportBackend,
    FineTunedScriptBackend,
    OllamaBackend,
    PromptedTableBackend,
    RoutedTableBackend,
)
from gemma_table.evaluation import build_benchmark_cases, evaluate_table_response
from gemma_table.research import ResearchLog


@dataclass
class CompareResult:
    query: str
    original: dict[str, Any]
    new_solution: dict[str, Any]
    original_evaluation: dict[str, Any] | None
    new_solution_evaluation: dict[str, Any] | None
    recommendation: str


def _normalize_review_result(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"correct", "incorrect"}:
        return normalized
    return None


class GemmaTableService:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.school_results_path = workspace_root / "research" / "kg_class1_benchmark_results.json"
        self.school_gemini_judged_path = workspace_root / "research" / "kg_class1_benchmark_results_gemini_full.json"
        self.school_llm_judged_path = workspace_root / "research" / "kg_class1_benchmark_results_llm_judged.json"
        self.school_review_path = workspace_root / "research" / "kg_class1_verified_judgments.json"
        self.research = ResearchLog(workspace_root / "research")
        self.original_backend = OllamaBackend("gemma3:270m")
        self.prompt_backend = PromptedTableBackend(self.original_backend)
        self._original_backend_failure: dict[str, Any] | None = None
        self.new_backend = self._select_new_backend()

    def _select_new_backend(self) -> Backend:
        adapter_dir = self.workspace_root / "research" / "models" / "gemma-table-lora-run1"
        if adapter_dir.exists():
            routed_backend = RoutedTableBackend(
                table_backend=FineTunedScriptBackend(self.workspace_root, adapter_dir),
                fallback_backend=self.original_backend,
            )
            self.research.record(
                title="Fine-tuned adapter selected",
                category="strategy",
                status="success",
                summary="Using the saved LoRA adapter for table queries and the original model for everything else.",
                details={"backend": routed_backend.name, "adapter_dir": str(adapter_dir)},
            )
            return routed_backend

        fine_tune_reason = self._fine_tune_unavailable_reason()
        if fine_tune_reason:
            self.research.record(
                title="Fine-tuning environment check",
                category="environment",
                status="blocked",
                summary="Dependency stack is not ready for a Gemma LoRA run.",
                details={"reason": fine_tune_reason},
            )
            self.research.record(
                title="Prompted-model fallback selected",
                category="strategy",
                status="success",
                summary="Using a static prompt-engineered Gemma path until fine-tuning is available.",
                details={"backend": self.prompt_backend.name},
            )
            return self.prompt_backend
        return FineTuneSupportBackend("fine-tuned Gemma weights are not wired into inference yet")

    def _fine_tune_unavailable_reason(self) -> str | None:
        checks = {
            "transformers": None,
            "datasets": None,
            "peft": None,
        }
        for module_name in list(checks):
            try:
                importlib.import_module(module_name)
            except Exception as exc:
                checks[module_name] = f"{type(exc).__name__}: {exc}"
        missing = {name: reason for name, reason in checks.items() if reason is not None}
        if not missing:
            return None
        return "; ".join(f"{name} -> {reason}" for name, reason in missing.items())

    def compare(self, query: str) -> CompareResult:
        original = self._run_original(query)
        new_solution = self.new_backend.generate(query)
        original_eval = evaluate_table_response(query, original.output if original.success else "")
        new_eval = evaluate_table_response(query, new_solution.output if new_solution.success else "")

        self.research.record(
            title="Side-by-side compare",
            category="inference",
            status="success" if new_solution.success else "partial",
            summary=f"Compared original backend with {self.new_backend.name}.",
            details={
                "query": query,
                "original_backend": original.backend,
                "original_success": original.success,
                "original_error": original.error,
                "new_backend": new_solution.backend,
                "new_success": new_solution.success,
                "new_error": new_solution.error,
            },
        )
        self.research.publish_report()

        if original.success:
            recommendation = "Base model responded. Use benchmark results to decide whether fine-tuning is necessary."
        else:
            recommendation = (
                "Base model execution is not reliable in the current environment. "
                "The current new solution is still model-based, but it uses a static prompt wrapper rather than a deterministic rule."
            )
        return CompareResult(
            query=query,
            original=original.to_dict(),
            new_solution=new_solution.to_dict(),
            original_evaluation=original_eval.to_dict() if original_eval.recognized else None,
            new_solution_evaluation=new_eval.to_dict() if new_eval.recognized else None,
            recommendation=recommendation,
        )

    def benchmark(self) -> dict[str, Any]:
        cases = build_benchmark_cases()
        results: list[dict[str, Any]] = []
        original_exact = 0
        new_exact = 0
        for case in cases:
            original_result = self._run_original(case.query)
            new_result = self.new_backend.generate(case.query)
            original_eval = evaluate_table_response(case.query, original_result.output if original_result.success else "")
            new_eval = evaluate_table_response(case.query, new_result.output if new_result.success else "")
            original_exact += int(original_eval.exact_match)
            new_exact += int(new_eval.exact_match)
            results.append(
                {
                    "case_id": case.case_id,
                    "split": case.split,
                    "query": case.query,
                    "original_backend": original_result.to_dict(),
                    "new_backend": new_result.to_dict(),
                    "original_evaluation": original_eval.to_dict(),
                    "new_evaluation": new_eval.to_dict(),
                }
            )

        summary = {
            "total_cases": len(cases),
            "original_exact_match_count": original_exact,
            "new_exact_match_count": new_exact,
            "original_exact_match_rate": round(original_exact / len(cases), 3),
            "new_exact_match_rate": round(new_exact / len(cases), 3),
            "fine_tune_needed": original_exact < len(cases),
            "selected_solution": self.new_backend.name,
        }
        self.research.record(
            title="Baseline benchmark",
            category="evaluation",
            status="success" if original_exact == len(cases) else "partial",
            summary="Measured original and new solution on table-of-N benchmark cases.",
            details=summary,
        )
        self.research.publish_report()
        return {"summary": summary, "cases": results}

    def _run_original(self, query: str) -> Any:
        if self._original_backend_failure is not None:
            cached = dict(self._original_backend_failure)
            cached["metadata"] = {**cached.get("metadata", {}), "cached_failure": True}
            from gemma_table.backends import BackendResult

            return BackendResult(**cached)

        result = self.original_backend.generate(query)
        if not result.success:
            self._original_backend_failure = result.to_dict()
        return result

    def workflow_status(self) -> dict[str, Any]:
        reason = self._fine_tune_unavailable_reason()
        return {
            "original_backend": self.original_backend.name,
            "prompt_backend": self.prompt_backend.name,
            "new_solution_backend": self.new_backend.name,
            "fine_tune_ready": reason is None,
            "fine_tune_blocker": reason,
            "research_log": str(self.research.events_path),
            "research_report": str(self.research.report_path),
        }

    def publish_report(self) -> dict[str, str]:
        return {
            "path": str(self.research.report_path),
            "content": self.research.publish_report(),
        }

    def review_dataset(self) -> dict[str, Any]:
        source = self._load_json(self.school_results_path)
        review_state = self._load_json(self.school_review_path, default={"rows": {}})
        llm_state = self._load_json(self._preferred_judged_results_path(), default={"rows": []})
        llm_rows = {row["qid"]: row for row in llm_state.get("rows", []) if "qid" in row}
        overrides = review_state.get("rows", {})

        rows: list[dict[str, Any]] = []
        stats = {
            "total_questions": 0,
            "categories": {},
            "base_llm_available": 0,
            "ft_llm_available": 0,
            "base_human_verified": 0,
            "ft_human_verified": 0,
            "rows_with_any_human_review": 0,
            "rows_needing_review": 0,
            "rows_with_disagreement": 0,
            "base_effective_correct": 0,
            "ft_effective_correct": 0,
        }

        for row in source.get("rows", []):
            qid = row["qid"]
            llm_row = llm_rows.get(qid, {})
            override = overrides.get(qid, {})
            base_llm = self._extract_llm_verdict(llm_row.get("base_judge"))
            ft_llm = self._extract_llm_verdict(llm_row.get("ft_judge"))
            base_human = _normalize_review_result(override.get("base_human_result"))
            ft_human = _normalize_review_result(override.get("ft_human_result"))

            merged = {
                "question_id": qid,
                "category": row["category"],
                "question": row["question"],
                "expected_answers": row["expected"],
                "base_answer": row["base_output"],
                "fine_tuned_answer": row["ft_output"],
                "base_heuristic_result": "correct" if row.get("base_correct") else "incorrect",
                "fine_tuned_heuristic_result": "correct" if row.get("ft_correct") else "incorrect",
                "base_llm_result": base_llm.get("result"),
                "base_llm_reason": base_llm.get("reason"),
                "fine_tuned_llm_result": ft_llm.get("result"),
                "fine_tuned_llm_reason": ft_llm.get("reason"),
                "base_human_result": base_human,
                "fine_tuned_human_result": ft_human,
                "reviewer": override.get("reviewer", ""),
                "note": override.get("note", ""),
                "updated_at": override.get("updated_at"),
                "base_effective_result": base_human or base_llm.get("result"),
                "fine_tuned_effective_result": ft_human or ft_llm.get("result"),
                "has_human_review": (base_human is not None) or (ft_human is not None),
                "needs_review": (base_human is None) or (ft_human is None),
                "has_disagreement": (base_human is not None and base_llm.get("result") is not None and base_human != base_llm.get("result"))
                or (ft_human is not None and ft_llm.get("result") is not None and ft_human != ft_llm.get("result")),
            }
            rows.append(merged)

            stats["total_questions"] += 1
            stats["categories"][row["category"]] = stats["categories"].get(row["category"], 0) + 1
            stats["base_llm_available"] += int(base_llm.get("result") is not None)
            stats["ft_llm_available"] += int(ft_llm.get("result") is not None)
            stats["base_human_verified"] += int(base_human is not None)
            stats["ft_human_verified"] += int(ft_human is not None)
            stats["rows_with_any_human_review"] += int(merged["has_human_review"])
            stats["rows_needing_review"] += int(merged["needs_review"])
            stats["rows_with_disagreement"] += int(merged["has_disagreement"])
            stats["base_effective_correct"] += int(merged["base_effective_result"] == "correct")
            stats["ft_effective_correct"] += int(merged["fine_tuned_effective_result"] == "correct")

        return {"summary": stats, "rows": rows}

    def save_review_decision(
        self,
        question_id: str,
        base_human_result: str | None,
        fine_tuned_human_result: str | None,
        reviewer: str,
        note: str,
    ) -> dict[str, Any]:
        dataset = self.review_dataset()
        known_ids = {row["question_id"] for row in dataset["rows"]}
        if question_id not in known_ids:
            raise ValueError(f"unknown question_id: {question_id}")

        state = self._load_json(self.school_review_path, default={"rows": {}})
        rows = state.setdefault("rows", {})
        rows[question_id] = {
            "base_human_result": _normalize_review_result(base_human_result),
            "ft_human_result": _normalize_review_result(fine_tuned_human_result),
            "reviewer": reviewer.strip(),
            "note": note.strip(),
            "updated_at": datetime.now(UTC).isoformat(),
        }
        self.school_review_path.write_text(json.dumps(state, indent=2, ensure_ascii=True), encoding="utf-8")
        self.research.record(
            title="Human review saved",
            category="review",
            status="success",
            summary="Saved human verification for KG/Class 1 judged row.",
            details={"question_id": question_id},
        )
        return {"ok": True, "question_id": question_id}

    def next_review_question_id(self) -> str | None:
        dataset = self.review_dataset()
        for row in dataset["rows"]:
            if row["needs_review"] or row["has_disagreement"]:
                return row["question_id"]
        return dataset["rows"][0]["question_id"] if dataset["rows"] else None

    def publish_verified_review_report(self) -> dict[str, str]:
        dataset = self.review_dataset()
        report_path = self.workspace_root / "research" / "kg_class1_verified_review_report.md"
        lines = [
            "# KG/Class 1 Verified Review Report",
            "",
            "This report is generated from the human-review layer.",
            "",
            "## Summary",
            "",
            f"- Total questions: {dataset['summary']['total_questions']}",
            f"- Rows needing review: {dataset['summary']['rows_needing_review']}",
            f"- Rows with any human review: {dataset['summary']['rows_with_any_human_review']}",
            f"- Rows with human-vs-LLM disagreement: {dataset['summary']['rows_with_disagreement']}",
            f"- Base effective correct: {dataset['summary']['base_effective_correct']}/{dataset['summary']['total_questions']}",
            f"- Fine-tuned effective correct: {dataset['summary']['ft_effective_correct']}/{dataset['summary']['total_questions']}",
            "",
            "## Full Table",
            "",
            "| QuestionId | Category | Query | Expected Answer | Base LLM | Base Human | Base Effective | Fine-Tuned LLM | Fine-Tuned Human | Fine-Tuned Effective |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for row in dataset["rows"]:
            lines.append(
                f"| {row['question_id']} | {row['category']} | {row['question'].replace('|', '/')} | {', '.join(row['expected_answers'])} | "
                f"{row['base_llm_result'] or 'unset'} | {row['base_human_result'] or 'unset'} | {row['base_effective_result'] or 'unset'} | "
                f"{row['fine_tuned_llm_result'] or 'unset'} | {row['fine_tuned_human_result'] or 'unset'} | {row['fine_tuned_effective_result'] or 'unset'} |"
            )
        content = "\n".join(lines) + "\n"
        report_path.write_text(content, encoding="utf-8")
        return {"path": str(report_path), "content": content}

    def _extract_llm_verdict(self, payload: dict[str, Any] | None) -> dict[str, str | None]:
        if not payload:
            return {"result": None, "reason": None}
        verdict = str(payload.get("verdict", "")).strip().lower()
        reason = str(payload.get("reason", "")).strip() or None
        if reason and reason.startswith("judge_error:"):
            return {"result": None, "reason": reason}
        if verdict not in {"correct", "incorrect"}:
            return {"result": None, "reason": reason}
        return {"result": verdict, "reason": reason}

    def _load_json(self, path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
        if not path.exists():
            return {} if default is None else default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {} if default is None else default

    def _preferred_judged_results_path(self) -> Path:
        if self.school_gemini_judged_path.exists():
            return self.school_gemini_judged_path
        return self.school_llm_judged_path
