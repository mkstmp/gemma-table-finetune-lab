from __future__ import annotations

import importlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from assistant_platform.gemma_table.backends import (
    Backend,
    FineTuneSupportBackend,
    FineTunedScriptBackend,
    OllamaBackend,
    PromptedTableBackend,
    RoutedTableBackend,
)
from assistant_platform.gemma_table.evaluation import build_benchmark_cases, evaluate_table_response
from assistant_platform.gemma_table.research import ResearchLog


@dataclass
class CompareResult:
    query: str
    original: dict[str, Any]
    new_solution: dict[str, Any]
    original_evaluation: dict[str, Any] | None
    new_solution_evaluation: dict[str, Any] | None
    recommendation: str


class GemmaTableService:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
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
            from assistant_platform.gemma_table.backends import BackendResult

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
