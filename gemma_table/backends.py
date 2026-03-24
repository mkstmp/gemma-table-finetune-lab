from __future__ import annotations

import subprocess
from pathlib import Path
from dataclasses import asdict, dataclass, field
from typing import Any

from gemma_table.core import expected_output_for_query, parse_table_request, render_table


@dataclass
class BackendResult:
    backend: str
    success: bool
    output: str = ""
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Backend:
    name = "backend"

    def generate(self, query: str) -> BackendResult:
        raise NotImplementedError


class OllamaBackend(Backend):
    def __init__(self, model_name: str, timeout_seconds: int = 30) -> None:
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds
        self.name = f"ollama:{model_name}"

    def generate(self, query: str) -> BackendResult:
        try:
            completed = subprocess.run(
                ["ollama", "run", self.model_name, query],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except FileNotFoundError:
            return BackendResult(backend=self.name, success=False, error="ollama executable not found")
        except subprocess.TimeoutExpired:
            return BackendResult(backend=self.name, success=False, error="ollama timed out")
        except Exception as exc:
            return BackendResult(backend=self.name, success=False, error=f"{type(exc).__name__}: {exc}")

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        if completed.returncode != 0:
            error = stderr or stdout or f"ollama exited with status {completed.returncode}"
            return BackendResult(
                backend=self.name,
                success=False,
                error=error,
                metadata={"returncode": completed.returncode},
            )
        return BackendResult(
            backend=self.name,
            success=True,
            output=stdout,
            metadata={"returncode": completed.returncode},
        )


class PromptedTableBackend(Backend):
    def __init__(self, inner: Backend) -> None:
        self.inner = inner
        self.name = f"prompted:{inner.name}"

    def generate(self, query: str) -> BackendResult:
        prompt = (
            "You are a math helper for children.\n"
            "When the user asks for 'table of N', 'table N', or 'multiplication table of N', "
            "respond with only the multiplication table from 1 to 10.\n"
            "Use this format exactly:\n"
            "Table of N\n"
            "N x 1 = ...\n"
            "...\n"
            "N x 10 = ...\n"
            "Do not add extra commentary.\n\n"
            f"User request: {query}"
        )
        result = self.inner.generate(prompt)
        result.backend = self.name
        return result


class DeterministicTableBackend(Backend):
    def __init__(self, fallback: Backend | None = None) -> None:
        self.fallback = fallback
        self.name = "deterministic-table"

    def generate(self, query: str) -> BackendResult:
        parsed = parse_table_request(query)
        if parsed:
            return BackendResult(
                backend=self.name,
                success=True,
                output=render_table(parsed.value),
                metadata={"mode": "deterministic"},
            )
        if self.fallback is None:
            return BackendResult(
                backend=self.name,
                success=False,
                error="query does not match a supported 'table of N' request",
            )
        result = self.fallback.generate(query)
        result.backend = self.name
        result.metadata["mode"] = "fallback"
        return result


class FineTuneSupportBackend(Backend):
    def __init__(self, reason_unavailable: str) -> None:
        self.reason_unavailable = reason_unavailable
        self.name = "fine-tune-planned"

    def generate(self, query: str) -> BackendResult:
        expected = expected_output_for_query(query)
        if expected:
            return BackendResult(
                backend=self.name,
                success=False,
                output=expected,
                error=f"Fine-tuned backend not available yet: {self.reason_unavailable}",
            )
        return BackendResult(
            backend=self.name,
            success=False,
            error=f"Fine-tuned backend not available yet: {self.reason_unavailable}",
        )


class FineTunedScriptBackend(Backend):
    def __init__(self, workspace_root: Path, adapter_dir: Path, timeout_seconds: int = 120) -> None:
        self.workspace_root = workspace_root
        self.adapter_dir = adapter_dir
        self.timeout_seconds = timeout_seconds
        self.name = f"finetuned:{adapter_dir.name}"

    def generate(self, query: str) -> BackendResult:
        script_python = self.workspace_root / ".venv-gemma" / "bin" / "python"
        if not script_python.exists():
            return BackendResult(backend=self.name, success=False, error="fine-tune venv is missing")
        if not self.adapter_dir.exists():
            return BackendResult(backend=self.name, success=False, error="fine-tuned adapter directory is missing")

        try:
            completed = subprocess.run(
                [
                    str(script_python),
                    "-m",
                    "gemma_table.infer",
                    "--adapter-dir",
                    str(self.adapter_dir),
                    "--query",
                    query,
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
                cwd=str(self.workspace_root),
            )
        except Exception as exc:
            return BackendResult(backend=self.name, success=False, error=f"{type(exc).__name__}: {exc}")

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
        if completed.returncode != 0:
            return BackendResult(
                backend=self.name,
                success=False,
                error=stderr or stdout or f"inference exited with status {completed.returncode}",
                metadata={"returncode": completed.returncode},
            )
        return BackendResult(
            backend=self.name,
            success=True,
            output=stdout,
            metadata={"returncode": completed.returncode, "adapter_dir": str(self.adapter_dir)},
        )


class RoutedTableBackend(Backend):
    def __init__(self, table_backend: Backend, fallback_backend: Backend) -> None:
        self.table_backend = table_backend
        self.fallback_backend = fallback_backend
        self.name = f"routed:{table_backend.name}"

    def generate(self, query: str) -> BackendResult:
        if parse_table_request(query):
            result = self.table_backend.generate(query)
            result.metadata["route"] = "table_backend"
            return result
        result = self.fallback_backend.generate(query)
        result.backend = self.name
        result.metadata["route"] = "fallback_backend"
        return result
